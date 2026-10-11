from __future__ import annotations

import json
from pathlib import Path

import pytest

from vps_mcp import server as srv
from vps_mcp.config import ConfigError, Registry, load_registry
from tests.conftest import PASSWORD


async def call(tool: str, **args):
    result = await srv.mcp.call_tool(tool, args)
    return json.loads(result.content[0].text)


async def test_list_hosts(pool):
    data = await call("vps_list_hosts")
    assert data["default"] == "test"
    assert data["hosts"][0]["auth"] == "password"
    assert PASSWORD not in json.dumps(data)


async def test_status(pool):
    data = await call("vps_status")
    assert "error" not in data, data
    assert data["hostname"]
    assert data["kernel"]
    assert data["load_average"]["1m"] is not None
    assert data["disks"], data


async def test_run_command(pool, workdir):
    data = await call("vps_run_command", command="echo hello; echo oops >&2; exit 3", cwd=str(workdir))
    assert data["exit_status"] == 3
    assert data["ok"] is False
    assert data["stdout"].strip() == "hello"
    assert data["stderr"].strip() == "oops"

    data = await call("vps_run_command", command="pwd", cwd=str(workdir))
    assert data["stdout"].strip() == str(workdir)

    data = await call("vps_run_command", command="cat", stdin="piped in")
    assert data["stdout"] == "piped in"


async def test_run_command_timeout(pool):
    data = await call("vps_run_command", command="sleep 5", timeout=1)
    assert data["timed_out"] is True
    assert data["ok"] is False


async def test_run_command_truncation(pool):
    data = await call("vps_run_command", command="head -c 5000 /dev/zero | tr '\\0' x", max_output=1000)
    assert "output truncated" in data["stdout"]


async def test_write_read_list(pool, workdir):
    target = workdir / "sub" / "hello.txt"
    data = await call("vps_write_file", path=str(target), content="line1\n", create_dirs=True, mode="600")
    assert data["action"] == "created"
    assert target.read_text() == "line1\n"
    assert oct(target.stat().st_mode & 0o777) == "0o600"

    data = await call("vps_write_file", path=str(target), content="line2\n", append=True)
    assert data["action"] == "appended"

    data = await call("vps_write_file", path=str(target), content="fresh\n", backup=True)
    assert data["action"] == "overwritten"
    assert data["backup"] == str(target) + ".bak"
    assert (workdir / "sub" / "hello.txt.bak").read_text() == "line1\nline2\n"

    data = await call("vps_read_file", path=str(target))
    assert data["content"] == "fresh\n"
    assert data["truncated"] is False

    data = await call("vps_read_file", path=str(target), max_bytes=2)
    assert data["content"] == "fr"
    assert data["truncated"] is True and data["next_offset"] == 2
    data = await call("vps_read_file", path=str(target), offset=2, max_bytes=100)
    assert data["content"] == "esh\n"

    data = await call("vps_list_directory", path=str(workdir / "sub"))
    names = [e["name"] for e in data["entries"]]
    assert names == ["hello.txt", "hello.txt.bak"]
    assert data["entries"][0]["type"] == "file"
    assert data["entries"][0]["mode"] == "-rw-------"

    data = await call("vps_list_directory", path=str(workdir / "sub"), limit=1)
    assert data["has_more"] is True and data["next_offset"] == 1


async def test_read_missing_file(pool, workdir):
    data = await call("vps_read_file", path=str(workdir / "nope.txt"))
    assert "No such file" in data["error"]


async def test_home_expansion(pool):
    data = await call("vps_list_directory", path="~")
    assert data["path"] == str(Path.home())


async def test_upload_download(pool, workdir):
    src = workdir / "local.bin"
    src.write_bytes(bytes(range(256)))
    remote = workdir / "remote.bin"
    data = await call("vps_upload_file", local_path=str(src), remote_path=str(remote))
    assert data["bytes"] == 256
    assert remote.read_bytes() == src.read_bytes()

    back = workdir / "down" / "copy.bin"
    data = await call("vps_download_file", remote_path=str(remote), local_path=str(back))
    assert data["bytes"] == 256
    assert back.read_bytes() == src.read_bytes()

    data = await call("vps_upload_file", local_path=str(workdir / "missing"), remote_path=str(remote))
    assert "does not exist" in data["error"]


async def test_tail_log(pool, workdir):
    log = workdir / "app.log"
    log.write_text("\n".join(f"line {i} {'ERROR' if i % 3 == 0 else 'info'}" for i in range(20)) + "\n")
    data = await call("vps_tail_log", path=str(log), lines=5)
    assert data["line_count"] == 5
    assert data["lines"][-1] == "line 19 info"
    data = await call("vps_tail_log", path=str(log), lines=20, grep="error")
    assert data["line_count"] == 7
    data = await call("vps_tail_log", path=str(log), lines=20, grep="nomatch")
    assert data["line_count"] == 0


async def test_list_processes(pool):
    data = await call("vps_list_processes", filter="python", limit=5)
    assert data["count"] >= 1
    assert all("python" in p["command"].lower() for p in data["processes"])
    assert data["processes"][0]["pid"] > 0


async def test_service_validation(pool):
    data = await call("vps_service", action="status")
    assert "name" in data["error"]
    data = await call("vps_service", action="restart", name="nginx; rm -rf /")
    assert "unexpected characters" in data["error"]


async def test_docker_missing_or_present(pool):
    data = await call("vps_docker_ps")
    assert "containers" in data or "error" in data


async def test_disconnect_and_reconnect(pool):
    await call("vps_status")
    data = await call("vps_disconnect")
    assert data["closed"] == 1
    data = await call("vps_run_command", command="echo back")
    assert data["stdout"].strip() == "back"


async def test_bad_credentials(ssh_server):
    from vps_mcp.config import HostConfig

    cfg = HostConfig(name="bad", host="127.0.0.1", port=ssh_server, username="x", password="wrong", known_hosts="none", connect_timeout=5)
    srv.set_registry(Registry(hosts={"bad": cfg}, default="bad"))
    try:
        data = await call("vps_status")
        assert "Authentication" in data["error"]
    finally:
        srv._pool = None


async def test_unreachable_host():
    from vps_mcp.config import HostConfig

    cfg = HostConfig(name="dead", host="127.0.0.1", port=1, username="x", password="x", known_hosts="none", connect_timeout=2)
    srv.set_registry(Registry(hosts={"dead": cfg}, default="dead"))
    try:
        data = await call("vps_run_command", command="true")
        assert "Could not connect" in data["error"]
    finally:
        srv._pool = None


# ----------------------------------------------------------------------------- config
def test_registry_from_env():
    reg = load_registry(env={"VPS_HOST": "1.2.3.4", "VPS_USER": "root", "VPS_KEY_PATH": "~/.ssh/id", "VPS_KNOWN_HOSTS": "NONE"}, hosts_file=Path("/nonexistent"))
    cfg = reg.get(None)
    assert cfg.host == "1.2.3.4" and cfg.username == "root" and cfg.known_hosts == "none"
    kw = cfg.asyncssh_kwargs()
    assert kw["known_hosts"] is None and kw["client_keys"][0].endswith("/.ssh/id")


def test_registry_from_file(tmp_path, monkeypatch):
    monkeypatch.setenv("STAGING_PW", "s3cret")
    hosts = tmp_path / "hosts.json"
    hosts.write_text(json.dumps({
        "default": "prod",
        "hosts": {
            "prod": {"host": "prod.example", "username": "deploy", "key_path": "~/.ssh/k"},
            "staging": {"host": "stg.example", "port": 2222, "password_env": "STAGING_PW", "known_hosts": False},
        },
    }))
    reg = load_registry(env={"STAGING_PW": "s3cret"}, hosts_file=hosts)
    assert reg.get(None).name == "prod"
    stg = reg.get("staging")
    assert stg.port == 2222 and stg.password == "s3cret" and stg.known_hosts == "none"
    with pytest.raises(ConfigError, match="Unknown host"):
        reg.get("qa")


def test_registry_empty():
    reg = load_registry(env={}, hosts_file=Path("/nonexistent"))
    with pytest.raises(ConfigError, match="No VPS hosts"):
        reg.get(None)


def test_registry_bad_default(tmp_path):
    hosts = tmp_path / "hosts.json"
    hosts.write_text(json.dumps({"default": "x", "hosts": {"a": {"host": "h"}}}))
    with pytest.raises(ConfigError, match="Default host"):
        load_registry(env={}, hosts_file=hosts)
