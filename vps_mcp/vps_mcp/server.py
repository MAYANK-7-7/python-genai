#!/usr/bin/env python3
"""vps_mcp - MCP server that connects directly to a VPS over SSH/SFTP.

Run with ``python -m vps_mcp`` (stdio, the default for Claude Desktop / Claude
Code) or ``python -m vps_mcp --transport streamable-http --port 8765`` to expose
it over HTTP for remote MCP clients.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import posixpath
import shlex
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

import asyncssh
from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations
from pydantic import Field

from . import __version__
from .config import ConfigError, Registry, load_registry
from .ssh import CommandResult, ConnectionPool, VPSError

INSTRUCTIONS = """\
This server gives you a direct SSH/SFTP connection to one or more VPS hosts.

Start with `vps_list_hosts` to see what is configured and `vps_status` for a
health snapshot. Use `vps_run_command` for anything shell-based, the file tools
(`vps_list_directory`, `vps_read_file`, `vps_write_file`, `vps_upload_file`,
`vps_download_file`) for files, `vps_service` for systemd units, `vps_tail_log`
for logs and `vps_list_processes` / `vps_docker_ps` for what is running.

Commands run as the configured SSH user. Pass `sudo=true` only when the user
has passwordless sudo. Destructive commands (rm -rf, mkfs, reboot, ...) are
executed exactly as given - confirm with the human before running them.
"""

mcp = MCPServer(
    "vps_mcp",
    title="VPS MCP",
    instructions=INSTRUCTIONS,
    version=__version__,
)

_pool: Optional[ConnectionPool] = None


def get_pool() -> ConnectionPool:
    """Return the process-wide connection pool, creating it on first use."""
    global _pool
    if _pool is None:
        _pool = ConnectionPool(load_registry())
    return _pool


def set_registry(registry: Registry) -> ConnectionPool:
    """Replace the host registry (used by tests and by ``--hosts-file``)."""
    global _pool
    _pool = ConnectionPool(registry)
    return _pool


# ----------------------------------------------------------------------------- helpers
READ_ONLY = ToolAnnotations(read_only_hint=True, destructive_hint=False, idempotent_hint=True, open_world_hint=True)
MUTATING = ToolAnnotations(read_only_hint=False, destructive_hint=True, idempotent_hint=False, open_world_hint=True)
IDEMPOTENT_WRITE = ToolAnnotations(read_only_hint=False, destructive_hint=True, idempotent_hint=True, open_world_hint=True)

HostArg = Optional[str]
_HOST_DESC = (
    "Name of the configured host to target (see vps_list_hosts). "
    "Omit to use the default host."
)


def _error(exc: Exception) -> Dict[str, Any]:
    """Uniform error payload. Tools return this instead of raising so the LLM sees the message."""
    if isinstance(exc, (VPSError, ConfigError)):
        return {"error": str(exc)}
    if isinstance(exc, asyncssh.SFTPNoSuchFile):
        return {"error": f"No such file or directory on the VPS: {exc.reason}"}
    if isinstance(exc, asyncssh.SFTPPermissionDenied):
        return {"error": f"Permission denied on the VPS: {exc.reason}. Try sudo via vps_run_command or check ownership."}
    if isinstance(exc, asyncssh.SFTPError):
        return {"error": f"SFTP error: {exc.reason}"}
    if isinstance(exc, asyncio.TimeoutError):
        return {"error": "Operation timed out."}
    return {"error": f"{type(exc).__name__}: {exc}"}


def _result_payload(result: CommandResult) -> Dict[str, Any]:
    return {
        "ok": result.ok,
        "exit_status": result.exit_status,
        "timed_out": result.timed_out,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "command": result.command,
    }


def _mode_string(mode: Optional[int]) -> str:
    return stat.filemode(mode) if mode is not None else "?"


def _ts(seconds: Optional[float]) -> Optional[str]:
    if seconds is None:
        return None
    return datetime.fromtimestamp(seconds, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


async def _remote_home(host: HostArg) -> str:
    return (await get_pool().run_checked("printf %s \"$HOME\"", host, timeout=10)).strip() or "/"


async def _abs_remote(path: str, host: HostArg) -> str:
    """Expand ``~`` and make the remote path absolute (SFTP has no notion of cwd)."""
    if path.startswith("~"):
        path = (await _remote_home(host)) + path[1:]
    if not path.startswith("/"):
        path = posixpath.join(await _remote_home(host), path)
    return posixpath.normpath(path)


# ------------------------------------------------------------------------------ tools
@mcp.tool(name="vps_list_hosts", annotations=READ_ONLY)
async def vps_list_hosts() -> Dict[str, Any]:
    """List the VPS hosts this server can connect to and which one is the default.

    Returns name, address, port, username, authentication method and whether
    host-key checking is enabled for each host. No secrets are included.
    Call this first when you are unsure which `host` value to pass to other tools.
    """
    try:
        registry = get_pool().registry
        return {
            "default": registry.default,
            "hosts": [cfg.public_summary() for cfg in registry.hosts.values()],
        }
    except Exception as exc:  # noqa: BLE001
        return _error(exc)


@mcp.tool(name="vps_status", annotations=READ_ONLY)
async def vps_status(
    host: HostArg = Field(default=None, description=_HOST_DESC),
) -> Dict[str, Any]:
    """Connect to the VPS and return a health snapshot.

    Includes hostname, OS, kernel, uptime, load average, memory, disk usage of
    mounted filesystems, logged-in user and the server's current time. Use it to
    verify connectivity and to spot resource pressure before digging deeper.
    """
    script = r"""
echo "__HOSTNAME__"; hostname 2>/dev/null
echo "__OS__"; . /etc/os-release 2>/dev/null && echo "$PRETTY_NAME" || uname -s
echo "__KERNEL__"; uname -r
echo "__WHOAMI__"; id -un
echo "__DATE__"; date -u +"%Y-%m-%d %H:%M:%S UTC"
echo "__UPTIME__"; uptime 2>/dev/null
echo "__LOADAVG__"; cat /proc/loadavg 2>/dev/null
echo "__MEM__"; free -m 2>/dev/null
echo "__DISK__"; df -hP -x tmpfs -x devtmpfs -x squashfs -x overlay 2>/dev/null || df -hP
echo "__IP__"; hostname -I 2>/dev/null
"""
    try:
        out = await get_pool().run_checked(script, host, timeout=30)
    except Exception as exc:  # noqa: BLE001
        return _error(exc)

    sections: Dict[str, List[str]] = {}
    current = None
    for line in out.splitlines():
        if line.startswith("__") and line.endswith("__"):
            current = line.strip("_").lower()
            sections[current] = []
        elif current:
            sections[current].append(line)

    def one(key: str) -> Optional[str]:
        lines = [l for l in sections.get(key, []) if l.strip()]
        return lines[0].strip() if lines else None

    load = (one("loadavg") or "").split()
    memory = _parse_free(sections.get("mem", []))
    disks = _parse_df(sections.get("disk", []))
    return {
        "host": get_pool().registry.get(host).name,
        "hostname": one("hostname"),
        "os": one("os"),
        "kernel": one("kernel"),
        "user": one("whoami"),
        "server_time": one("date"),
        "ip_addresses": (one("ip") or "").split(),
        "uptime": one("uptime"),
        "load_average": {"1m": _f(load, 0), "5m": _f(load, 1), "15m": _f(load, 2)},
        "memory_mb": memory,
        "disks": disks,
    }


def _f(parts: List[str], i: int) -> Optional[float]:
    try:
        return float(parts[i])
    except (IndexError, ValueError):
        return None


def _parse_free(lines: List[str]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for line in lines:
        parts = line.split()
        if len(parts) >= 3 and parts[0].rstrip(":").lower() in ("mem", "swap"):
            key = parts[0].rstrip(":").lower()
            nums = [int(p) for p in parts[1:] if p.isdigit()]
            entry = {"total": nums[0] if nums else None, "used": nums[1] if len(nums) > 1 else None}
            if key == "mem" and len(nums) >= 6:
                entry["available"] = nums[5]
            out[key] = entry
    return out


def _parse_df(lines: List[str]) -> List[Dict[str, Any]]:
    disks = []
    for line in lines[1:]:
        parts = line.split()
        if len(parts) >= 6:
            disks.append(
                {
                    "filesystem": parts[0],
                    "size": parts[1],
                    "used": parts[2],
                    "available": parts[3],
                    "use_percent": parts[4],
                    "mounted_on": " ".join(parts[5:]),
                }
            )
    return disks


@mcp.tool(name="vps_run_command", annotations=MUTATING)
async def vps_run_command(
    command: str = Field(..., description="Shell command to execute, e.g. 'ls -la /var/www' or 'systemctl --failed'.", min_length=1),
    host: HostArg = Field(default=None, description=_HOST_DESC),
    cwd: Optional[str] = Field(default=None, description="Remote directory to cd into before running."),
    timeout: float = Field(default=60, description="Seconds to wait before killing the command.", ge=1, le=3600),
    stdin: Optional[str] = Field(default=None, description="Text to feed to the command's standard input."),
    sudo: bool = Field(default=False, description="Run via passwordless `sudo -n`. Fails if sudo prompts for a password."),
    max_output: int = Field(default=100_000, description="Truncate stdout/stderr beyond this many characters.", ge=1000, le=2_000_000),
) -> Dict[str, Any]:
    """Run a shell command on the VPS and return its exit status, stdout and stderr.

    The command runs in the SSH user's login shell, so pipes, redirects and
    environment variables work. A non-zero exit status is returned, not raised,
    so inspect `ok` / `exit_status`. Long-running daemons should be started with
    nohup/systemd rather than left attached to this call.

    Use for: package installs, git pulls, nginx reloads, cron inspection, any
    diagnostic. Don't use for reading or writing whole files when
    vps_read_file / vps_write_file would be clearer.
    """
    try:
        result = await get_pool().run(
            command, host, timeout=timeout, cwd=cwd, stdin=stdin, sudo=sudo, max_output=max_output
        )
        return _result_payload(result)
    except Exception as exc:  # noqa: BLE001
        return _error(exc)


@mcp.tool(name="vps_list_directory", annotations=READ_ONLY)
async def vps_list_directory(
    path: str = Field(default="~", description="Remote directory. '~' and relative paths resolve against the SSH user's home."),
    host: HostArg = Field(default=None, description=_HOST_DESC),
    show_hidden: bool = Field(default=False, description="Include dot-files."),
    limit: int = Field(default=200, description="Maximum entries to return.", ge=1, le=5000),
    offset: int = Field(default=0, description="Entries to skip (for pagination).", ge=0),
) -> Dict[str, Any]:
    """List a directory on the VPS over SFTP with type, size, permissions, owner and mtime.

    Entries are sorted by name. Returns `has_more` / `next_offset` when the
    listing was cut by `limit`.
    """
    try:
        pool = get_pool()
        abs_path = await _abs_remote(path, host)
        sftp = await pool.sftp(host)
        try:
            entries = await sftp.readdir(abs_path)
        finally:
            sftp.exit()
    except Exception as exc:  # noqa: BLE001
        return _error(exc)

    rows = []
    for entry in sorted(entries, key=lambda e: e.filename):
        name = entry.filename
        if name in (".", "..") or (not show_hidden and name.startswith(".")):
            continue
        attrs = entry.attrs
        kind = "dir" if attrs.type == asyncssh.FILEXFER_TYPE_DIRECTORY else (
            "symlink" if attrs.type == asyncssh.FILEXFER_TYPE_SYMLINK else "file"
        )
        rows.append(
            {
                "name": name,
                "type": kind,
                "size": attrs.size,
                "mode": _mode_string(attrs.permissions),
                "uid": attrs.uid,
                "gid": attrs.gid,
                "modified": _ts(attrs.mtime),
            }
        )
    page = rows[offset : offset + limit]
    has_more = offset + len(page) < len(rows)
    return {
        "path": abs_path,
        "total": len(rows),
        "count": len(page),
        "offset": offset,
        "has_more": has_more,
        "next_offset": offset + len(page) if has_more else None,
        "entries": page,
    }


@mcp.tool(name="vps_read_file", annotations=READ_ONLY)
async def vps_read_file(
    path: str = Field(..., description="Remote file path, e.g. '/etc/nginx/nginx.conf' or '~/.bashrc'.", min_length=1),
    host: HostArg = Field(default=None, description=_HOST_DESC),
    offset: int = Field(default=0, description="Byte offset to start reading from.", ge=0),
    max_bytes: int = Field(default=200_000, description="Maximum bytes to return.", ge=1, le=5_000_000),
) -> Dict[str, Any]:
    """Read a text file from the VPS over SFTP.

    Returns the content decoded as UTF-8 (invalid bytes replaced), the file size,
    and `truncated` when the file is longer than `max_bytes`; use `offset` to page
    through large files. Binary files are better fetched with vps_download_file.
    """
    try:
        pool = get_pool()
        abs_path = await _abs_remote(path, host)
        sftp = await pool.sftp(host)
        try:
            size = (await sftp.stat(abs_path)).size
            async with sftp.open(abs_path, "rb") as fh:
                await fh.seek(offset)
                data = await fh.read(max_bytes)
        finally:
            sftp.exit()
    except Exception as exc:  # noqa: BLE001
        return _error(exc)
    end = offset + len(data)
    return {
        "path": abs_path,
        "size": size,
        "offset": offset,
        "bytes_returned": len(data),
        "truncated": size is not None and end < size,
        "next_offset": end if size is not None and end < size else None,
        "content": data.decode("utf-8", errors="replace"),
    }


@mcp.tool(name="vps_write_file", annotations=IDEMPOTENT_WRITE)
async def vps_write_file(
    path: str = Field(..., description="Remote file path to create or overwrite.", min_length=1),
    content: str = Field(..., description="Text content to write (UTF-8)."),
    host: HostArg = Field(default=None, description=_HOST_DESC),
    append: bool = Field(default=False, description="Append instead of overwrite."),
    mode: Optional[str] = Field(default=None, description="Octal permissions to apply, e.g. '644' or '0755'.", pattern=r"^0?[0-7]{3}$"),
    create_dirs: bool = Field(default=False, description="Create missing parent directories."),
    backup: bool = Field(default=False, description="Copy an existing file to '<path>.bak' before overwriting."),
) -> Dict[str, Any]:
    """Create or overwrite a text file on the VPS over SFTP.

    Writes as the SSH user, so system files owned by root need either a
    writable location plus `vps_run_command` with sudo to move them, or a
    user with the right permissions. Use `backup=true` when editing config files.
    """
    try:
        pool = get_pool()
        abs_path = await _abs_remote(path, host)
        sftp = await pool.sftp(host)
        try:
            if create_dirs:
                await sftp.makedirs(posixpath.dirname(abs_path), exist_ok=True)
            existed = await sftp.exists(abs_path)
            backup_path = None
            if backup and existed and not append:
                backup_path = abs_path + ".bak"
                await sftp.copy(abs_path, backup_path)
            async with sftp.open(abs_path, "ab" if append else "wb") as fh:
                await fh.write(content.encode("utf-8"))
            if mode:
                await sftp.chmod(abs_path, int(mode, 8))
            size = (await sftp.stat(abs_path)).size
        finally:
            sftp.exit()
    except Exception as exc:  # noqa: BLE001
        return _error(exc)
    return {
        "path": abs_path,
        "action": "appended" if append else ("overwritten" if existed else "created"),
        "bytes_written": len(content.encode("utf-8")),
        "size": size,
        "backup": backup_path,
    }


@mcp.tool(name="vps_upload_file", annotations=IDEMPOTENT_WRITE)
async def vps_upload_file(
    local_path: str = Field(..., description="Path on the machine running this MCP server.", min_length=1),
    remote_path: str = Field(..., description="Destination path on the VPS (file or existing directory).", min_length=1),
    host: HostArg = Field(default=None, description=_HOST_DESC),
    recursive: bool = Field(default=False, description="Upload a whole directory tree."),
    preserve: bool = Field(default=False, description="Preserve permissions and timestamps."),
) -> Dict[str, Any]:
    """Upload a local file or directory to the VPS over SFTP (like `scp`).

    `local_path` is relative to the MCP server process, not the VPS.
    """
    try:
        local = Path(local_path).expanduser()
        if not local.exists():
            return {"error": f"Local path does not exist: {local}"}
        if local.is_dir() and not recursive:
            return {"error": f"{local} is a directory; pass recursive=true to upload it."}
        pool = get_pool()
        remote = await _abs_remote(remote_path, host)
        sftp = await pool.sftp(host)
        try:
            await sftp.put(str(local), remote, recurse=recursive, preserve=preserve)
            info = await sftp.stat(remote) if not local.is_dir() else None
        finally:
            sftp.exit()
    except Exception as exc:  # noqa: BLE001
        return _error(exc)
    return {
        "local_path": str(local),
        "remote_path": remote,
        "bytes": info.size if info else None,
        "recursive": recursive,
    }


@mcp.tool(name="vps_download_file", annotations=IDEMPOTENT_WRITE)
async def vps_download_file(
    remote_path: str = Field(..., description="Source path on the VPS.", min_length=1),
    local_path: str = Field(..., description="Destination on the machine running this MCP server.", min_length=1),
    host: HostArg = Field(default=None, description=_HOST_DESC),
    recursive: bool = Field(default=False, description="Download a whole directory tree."),
    preserve: bool = Field(default=False, description="Preserve permissions and timestamps."),
) -> Dict[str, Any]:
    """Download a file or directory from the VPS to the local machine over SFTP.

    Useful for pulling logs, backups or binary files that vps_read_file cannot
    show as text.
    """
    try:
        pool = get_pool()
        remote = await _abs_remote(remote_path, host)
        local = Path(local_path).expanduser()
        local.parent.mkdir(parents=True, exist_ok=True)
        sftp = await pool.sftp(host)
        try:
            await sftp.get(remote, str(local), recurse=recursive, preserve=preserve)
        finally:
            sftp.exit()
    except Exception as exc:  # noqa: BLE001
        return _error(exc)
    return {
        "remote_path": remote,
        "local_path": str(local),
        "bytes": local.stat().st_size if local.is_file() else None,
        "recursive": recursive,
    }


ServiceAction = Literal["status", "start", "stop", "restart", "reload", "enable", "disable", "is-active", "list-failed"]


@mcp.tool(name="vps_service", annotations=MUTATING)
async def vps_service(
    action: ServiceAction = Field(..., description="systemctl verb to run. 'list-failed' ignores `name`."),
    name: Optional[str] = Field(default=None, description="Unit name, e.g. 'nginx', 'docker', 'myapp.service'."),
    host: HostArg = Field(default=None, description=_HOST_DESC),
    sudo: bool = Field(default=True, description="Use passwordless sudo (required for start/stop/restart on most systems)."),
) -> Dict[str, Any]:
    """Manage a systemd service on the VPS: status, start, stop, restart, reload, enable, disable.

    `status` and `is-active` are safe to call freely. Anything else changes the
    server; confirm with the human first for production services.
    """
    if action != "list-failed" and not name:
        return {"error": "`name` is required for every action except list-failed."}
    if name and not all(c.isalnum() or c in "-_.@:" for c in name):
        return {"error": f"Unit name '{name}' contains unexpected characters."}
    if action == "list-failed":
        cmd = "systemctl --failed --no-pager --plain"
    elif action == "status":
        cmd = f"systemctl status {shlex.quote(name)} --no-pager -l"
    else:
        cmd = f"systemctl {action} {shlex.quote(name)}"
    try:
        result = await get_pool().run(cmd, host, timeout=90, sudo=sudo and action not in ("status", "is-active", "list-failed"))
    except Exception as exc:  # noqa: BLE001
        return _error(exc)
    payload = _result_payload(result)
    payload["action"] = action
    payload["unit"] = name
    if action == "is-active":
        payload["active"] = result.stdout.strip() == "active"
    return payload


@mcp.tool(name="vps_tail_log", annotations=READ_ONLY)
async def vps_tail_log(
    path: Optional[str] = Field(default=None, description="Log file path, e.g. '/var/log/nginx/error.log'. Omit to use journalctl."),
    unit: Optional[str] = Field(default=None, description="systemd unit for journalctl (when `path` is omitted), e.g. 'nginx'."),
    host: HostArg = Field(default=None, description=_HOST_DESC),
    lines: int = Field(default=100, description="Number of trailing lines.", ge=1, le=10_000),
    grep: Optional[str] = Field(default=None, description="Only keep lines matching this extended regex (case-insensitive)."),
    since: Optional[str] = Field(default=None, description="journalctl --since value, e.g. '1 hour ago' or '2026-10-11 08:00'."),
    sudo: bool = Field(default=False, description="Use sudo (needed for logs the SSH user cannot read)."),
) -> Dict[str, Any]:
    """Show the last N lines of a log file or of a systemd unit's journal, optionally filtered.

    Give either `path` (plain file, read with tail) or `unit` (journalctl). With
    neither, the whole system journal is used.
    """
    if path:
        cmd = f"tail -n {int(lines)} {shlex.quote(path)}"
    else:
        cmd = f"journalctl --no-pager -n {int(lines)}"
        if unit:
            cmd += f" -u {shlex.quote(unit)}"
        if since:
            cmd += f" --since {shlex.quote(since)}"
    if grep:
        cmd += f" | grep -Ei {shlex.quote(grep)}"
    try:
        result = await get_pool().run(cmd, host, timeout=60, sudo=sudo)
    except Exception as exc:  # noqa: BLE001
        return _error(exc)
    if result.exit_status not in (0, 1) or result.timed_out:  # grep exits 1 on no match
        return {"error": result.stderr.strip() or f"Command failed with status {result.exit_status}", "command": cmd}
    out_lines = result.stdout.splitlines()
    return {"source": path or (f"journal:{unit}" if unit else "journal"), "line_count": len(out_lines), "lines": out_lines}


@mcp.tool(name="vps_list_processes", annotations=READ_ONLY)
async def vps_list_processes(
    host: HostArg = Field(default=None, description=_HOST_DESC),
    sort_by: Literal["cpu", "mem"] = Field(default="cpu", description="Sort descending by CPU or memory usage."),
    filter: Optional[str] = Field(default=None, description="Case-insensitive substring to match against the command line."),
    limit: int = Field(default=25, description="Maximum processes to return.", ge=1, le=500),
) -> Dict[str, Any]:
    """List running processes on the VPS with PID, user, CPU %, memory % and command."""
    sort = "-%cpu" if sort_by == "cpu" else "-%mem"
    cmd = f"ps -eo pid,user,%cpu,%mem,rss,etime,args --sort={sort} --no-headers"
    try:
        out = await get_pool().run_checked(cmd, host, timeout=30)
    except Exception as exc:  # noqa: BLE001
        return _error(exc)
    procs = []
    for line in out.splitlines():
        parts = line.split(None, 6)
        if len(parts) < 7:
            continue
        if filter and filter.lower() not in parts[6].lower():
            continue
        procs.append(
            {
                "pid": int(parts[0]),
                "user": parts[1],
                "cpu_percent": _f(parts, 2),
                "mem_percent": _f(parts, 3),
                "rss_kb": int(parts[4]) if parts[4].isdigit() else None,
                "elapsed": parts[5],
                "command": parts[6],
            }
        )
    return {"total_matching": len(procs), "count": min(len(procs), limit), "processes": procs[:limit]}


@mcp.tool(name="vps_docker_ps", annotations=READ_ONLY)
async def vps_docker_ps(
    host: HostArg = Field(default=None, description=_HOST_DESC),
    all: bool = Field(default=False, description="Include stopped containers."),
    sudo: bool = Field(default=False, description="Use sudo if the SSH user is not in the docker group."),
) -> Dict[str, Any]:
    """List Docker containers on the VPS (name, image, status, ports). Returns an error if Docker is not installed."""
    cmd = "docker ps --format '{{json .}}'" + (" -a" if all else "")
    try:
        result = await get_pool().run(cmd, host, timeout=30, sudo=sudo)
    except Exception as exc:  # noqa: BLE001
        return _error(exc)
    if result.exit_status != 0:
        err = result.stderr.strip()
        if "not found" in err or "command not found" in err:
            return {"error": "Docker is not installed on this host (or not on PATH)."}
        if "permission denied" in err.lower():
            return {"error": "Permission denied talking to the Docker daemon. Retry with sudo=true."}
        return {"error": err or f"docker ps failed with status {result.exit_status}"}
    containers = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            raw = json.loads(line)
        except json.JSONDecodeError:
            continue
        containers.append(
            {
                "id": raw.get("ID"),
                "name": raw.get("Names"),
                "image": raw.get("Image"),
                "status": raw.get("Status"),
                "state": raw.get("State"),
                "ports": raw.get("Ports"),
                "created": raw.get("CreatedAt"),
            }
        )
    return {"count": len(containers), "containers": containers}


@mcp.tool(name="vps_disconnect", annotations=ToolAnnotations(read_only_hint=False, destructive_hint=False, idempotent_hint=True, open_world_hint=True))
async def vps_disconnect(
    host: HostArg = Field(default=None, description="Host whose cached SSH connection to close. Omit to close all."),
) -> Dict[str, Any]:
    """Close the cached SSH connection(s). The next tool call reconnects automatically.

    Use after changing credentials or when a connection looks stuck.
    """
    try:
        closed = await get_pool().close(host)
    except Exception as exc:  # noqa: BLE001
        return _error(exc)
    return {"closed": closed}


# ------------------------------------------------------------------------------- main
def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(prog="vps-mcp", description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http", "sse"],
        default=os.environ.get("VPS_MCP_TRANSPORT", "stdio"),
        help="MCP transport (default: stdio).",
    )
    parser.add_argument("--host", default=os.environ.get("VPS_MCP_BIND", "127.0.0.1"), help="Bind address for HTTP transports.")
    parser.add_argument("--port", type=int, default=int(os.environ.get("VPS_MCP_PORT", "8765")), help="Port for HTTP transports.")
    parser.add_argument("--hosts-file", default=None, help="Path to a hosts JSON file (overrides VPS_HOSTS_FILE).")
    parser.add_argument("--check", action="store_true", help="Validate configuration, print the host list and exit.")
    args = parser.parse_args(argv)
    logging.getLogger("asyncssh").setLevel(logging.WARNING)

    try:
        registry = load_registry(hosts_file=Path(args.hosts_file) if args.hosts_file else None)
    except ConfigError as exc:
        print(f"vps-mcp: configuration error: {exc}", file=sys.stderr)
        sys.exit(2)
    set_registry(registry)

    if args.check:
        print(json.dumps({"default": registry.default, "hosts": [h.public_summary() for h in registry.hosts.values()]}, indent=2))
        return

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(transport=args.transport, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
