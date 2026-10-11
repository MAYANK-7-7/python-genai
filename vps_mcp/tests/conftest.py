"""Spin up an in-process asyncssh server so the tools can be exercised end to end.

The fake server runs each requested command through the local ``/bin/sh`` and
serves SFTP from the real filesystem, so every tool is tested against real SSH
semantics without needing sshd.
"""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

import asyncssh
import pytest
import pytest_asyncio

from vps_mcp import server as srv
from vps_mcp.config import HostConfig, Registry

PASSWORD = "test-password"


class _Server(asyncssh.SSHServer):
    def begin_auth(self, username: str) -> bool:
        return True

    def password_auth_supported(self) -> bool:
        return True

    def validate_password(self, username: str, password: str) -> bool:
        return password == PASSWORD


async def _handle_process(process: asyncssh.SSHServerProcess) -> None:
    command = process.command or "true"
    proc = await asyncio.create_subprocess_shell(
        command,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdin_data = b""
    try:
        stdin_data = (await asyncio.wait_for(process.stdin.read(), 0.2)).encode()
    except (asyncio.TimeoutError, asyncssh.BreakReceived):
        pass
    out, err = await proc.communicate(stdin_data)
    process.stdout.write(out.decode("utf-8", "replace"))
    process.stderr.write(err.decode("utf-8", "replace"))
    process.exit(proc.returncode or 0)


@pytest_asyncio.fixture
async def ssh_server(tmp_path_factory):
    key = asyncssh.generate_private_key("ssh-ed25519")
    acceptor = await asyncssh.create_server(
        _Server,
        "127.0.0.1",
        0,
        server_host_keys=[key],
        process_factory=_handle_process,
        sftp_factory=True,
        allow_scp=False,
    )
    port = acceptor.sockets[0].getsockname()[1]
    yield port
    acceptor.close()
    await acceptor.wait_closed()


@pytest_asyncio.fixture
async def pool(ssh_server):
    cfg = HostConfig(
        name="test",
        host="127.0.0.1",
        port=ssh_server,
        username=os.environ.get("USER", "tester"),
        password=PASSWORD,
        known_hosts="none",
        connect_timeout=5,
    )
    registry = Registry(hosts={"test": cfg}, default="test")
    p = srv.set_registry(registry)
    yield p
    await p.close()
    srv._pool = None


@pytest.fixture
def workdir(tmp_path: Path) -> Path:
    return tmp_path
