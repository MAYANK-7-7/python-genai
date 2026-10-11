"""SSH connection management for vps_mcp.

One :class:`ConnectionPool` keeps a single live ``asyncssh`` connection per
configured host, opening it lazily on first use and transparently reopening it
if it has dropped.
"""

from __future__ import annotations

import asyncio
import shlex
from dataclasses import dataclass
from typing import Dict, Optional

import asyncssh

from .config import HostConfig, Registry


class VPSError(RuntimeError):
    """A user-facing error. The message is returned to the MCP client verbatim."""


@dataclass
class CommandResult:
    """Outcome of one remote command."""

    command: str
    exit_status: Optional[int]
    stdout: str
    stderr: str
    timed_out: bool = False

    @property
    def ok(self) -> bool:
        return self.exit_status == 0 and not self.timed_out


class ConnectionPool:
    """Lazily opened, reused SSH connections keyed by host name."""

    def __init__(self, registry: Registry) -> None:
        self.registry = registry
        self._conns: Dict[str, asyncssh.SSHClientConnection] = {}
        self._locks: Dict[str, asyncio.Lock] = {}

    # ------------------------------------------------------------------ connect
    def _lock(self, name: str) -> asyncio.Lock:
        if name not in self._locks:
            self._locks[name] = asyncio.Lock()
        return self._locks[name]

    async def get(self, host: Optional[str] = None) -> asyncssh.SSHClientConnection:
        """Return a live connection for ``host`` (or the default host)."""
        cfg = self.registry.get(host)
        async with self._lock(cfg.name):
            conn = self._conns.get(cfg.name)
            if conn is not None and not conn.is_closed():
                return conn
            conn = await self._open(cfg)
            self._conns[cfg.name] = conn
            return conn

    async def _open(self, cfg: HostConfig) -> asyncssh.SSHClientConnection:
        try:
            return await asyncssh.connect(**cfg.asyncssh_kwargs())
        except asyncssh.PermissionDenied as exc:
            raise VPSError(
                f"Authentication to {cfg.username}@{cfg.host}:{cfg.port} was refused "
                f"({exc.reason}). Check the username, key path/passphrase or password "
                "configured for this host."
            ) from exc
        except asyncssh.HostKeyNotVerifiable as exc:
            raise VPSError(
                f"Host key for {cfg.host}:{cfg.port} is not in known_hosts ({exc.reason}). "
                "Add it with `ssh-keyscan -H <host> >> ~/.ssh/known_hosts`, point "
                "known_hosts at a file that contains it, or set known_hosts to \"none\" "
                "for this host if you accept the risk."
            ) from exc
        except (asyncssh.Error, OSError, asyncio.TimeoutError) as exc:
            detail = getattr(exc, "reason", None) or str(exc) or type(exc).__name__
            raise VPSError(
                f"Could not connect to {cfg.username}@{cfg.host}:{cfg.port}: {detail}. "
                "Check the address, port, firewall rules and that sshd is running."
            ) from exc

    async def close(self, host: Optional[str] = None) -> int:
        """Close one connection (or all of them). Returns how many were closed."""
        names = [self.registry.get(host).name] if host else list(self._conns)
        closed = 0
        for name in names:
            conn = self._conns.pop(name, None)
            if conn is not None and not conn.is_closed():
                conn.close()
                await conn.wait_closed()
                closed += 1
        return closed

    # ---------------------------------------------------------------- commands
    async def run(
        self,
        command: str,
        host: Optional[str] = None,
        *,
        timeout: float = 60.0,
        cwd: Optional[str] = None,
        stdin: Optional[str] = None,
        sudo: bool = False,
        max_output: int = 100_000,
    ) -> CommandResult:
        """Run ``command`` through the remote login shell and capture its output."""
        conn = await self.get(host)
        full = command
        if cwd:
            full = f"cd {shlex.quote(cwd)} && {full}"
        if sudo:
            full = f"sudo -n sh -c {shlex.quote(full)}"
        try:
            proc = await conn.run(full, input=stdin, timeout=timeout, check=False)
        except asyncssh.TimeoutError as exc:
            return CommandResult(
                command=full,
                exit_status=None,
                stdout=_clip(_text(exc.stdout), max_output),
                stderr=_clip(_text(exc.stderr), max_output),
                timed_out=True,
            )
        except asyncssh.Error as exc:
            raise VPSError(f"SSH command failed before completing: {exc}") from exc
        return CommandResult(
            command=full,
            exit_status=proc.exit_status,
            stdout=_clip(_text(proc.stdout), max_output),
            stderr=_clip(_text(proc.stderr), max_output),
        )

    async def run_checked(self, command: str, host: Optional[str] = None, **kw) -> str:
        """Run a command that must succeed; return stdout or raise :class:`VPSError`."""
        result = await self.run(command, host, **kw)
        if result.timed_out:
            raise VPSError(f"Command timed out: {command}")
        if result.exit_status != 0:
            err = result.stderr.strip() or result.stdout.strip() or "(no output)"
            raise VPSError(f"Command exited with status {result.exit_status}: {command}\n{err}")
        return result.stdout

    # -------------------------------------------------------------------- sftp
    async def sftp(self, host: Optional[str] = None) -> asyncssh.SFTPClient:
        conn = await self.get(host)
        try:
            return await conn.start_sftp_client()
        except asyncssh.Error as exc:
            raise VPSError(
                f"Could not start an SFTP session: {exc}. The server may have the SFTP "
                "subsystem disabled; vps_run_command still works."
            ) from exc


def _text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def _clip(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    dropped = len(text) - limit
    return text[:limit] + f"\n... [output truncated, {dropped} more characters]"
