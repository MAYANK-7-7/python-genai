# vps-mcp

An [MCP](https://modelcontextprotocol.io) server that connects Claude (Claude
Desktop, Claude Code, or any MCP client) **directly to your VPS over SSH/SFTP**.
No agent has to be installed on the server: it only needs a running `sshd`.

## What it can do

| Tool | Purpose |
|------|---------|
| `vps_list_hosts` | Show configured hosts and the default one (never shows secrets) |
| `vps_status` | Hostname, OS, uptime, load, memory, disk, IPs in one call |
| `vps_run_command` | Run any shell command with timeout, cwd, stdin, optional sudo |
| `vps_list_directory` | SFTP directory listing with type, size, mode, owner, mtime, paging |
| `vps_read_file` | Read a text file, with byte offset / max size paging |
| `vps_write_file` | Create, overwrite or append a file; optional `.bak` backup, chmod, mkdir -p |
| `vps_upload_file` | Push a local file or directory to the VPS (like `scp`) |
| `vps_download_file` | Pull a file or directory from the VPS |
| `vps_service` | `systemctl` status / start / stop / restart / reload / enable / disable |
| `vps_tail_log` | Tail a log file or `journalctl` for a unit, with regex filter |
| `vps_list_processes` | `ps` sorted by CPU or memory, with filter |
| `vps_docker_ps` | Running (or all) Docker containers |
| `vps_disconnect` | Drop the cached SSH connection (reconnects on next call) |

Connections are opened lazily, kept alive and reused across tool calls, and
reopened automatically if they drop. Several hosts can be configured and
selected per call with the `host` argument.

## Install

```sh
cd vps_mcp
pip install -e .          # or: pip install -e ".[dev]" to run the tests
```

Requires Python 3.10+ and `mcp>=2.0`.

## Configure the VPS connection

### Option A: environment variables (one host)

| Variable | Meaning |
|----------|---------|
| `VPS_HOST` | hostname or IP (**required**) |
| `VPS_PORT` | SSH port, default `22` |
| `VPS_USER` | SSH user, default: your local username |
| `VPS_KEY_PATH` | private key file, e.g. `~/.ssh/id_ed25519` |
| `VPS_KEY_PASSPHRASE` | passphrase for that key |
| `VPS_PASSWORD` | password auth (prefer keys) |
| `VPS_KNOWN_HOSTS` | known_hosts file; `none` disables host-key checking |
| `VPS_CONNECT_TIMEOUT` | seconds, default `15` |
| `VPS_NAME` | name for this host, default `default` |

If none of the key/password variables are set, the SSH agent and the default
keys in `~/.ssh` are tried, exactly like the `ssh` command.

### Option B: hosts file (several hosts)

Create `~/.config/vps-mcp/hosts.json` (or point `VPS_HOSTS_FILE` /
`--hosts-file` at any path). See [`hosts.example.json`](hosts.example.json):

```json
{
  "default": "prod",
  "hosts": {
    "prod":    { "host": "203.0.113.10", "username": "deploy", "key_path": "~/.ssh/id_ed25519" },
    "staging": { "host": "staging.example.com", "port": 2222, "username": "ubuntu",
                 "password_env": "VPS_STAGING_PASSWORD", "known_hosts": false }
  }
}
```

Secrets can stay out of the file: `password_env` and `key_passphrase_env` name
an environment variable to read instead. Both sources can be combined; the
environment host is added under `VPS_NAME`.

Validate the configuration without starting the server:

```sh
vps-mcp --check
```

### Host-key checking

By default the server verifies the VPS host key against `~/.ssh/known_hosts`,
like `ssh`. On first use run:

```sh
ssh-keyscan -H your.vps.ip >> ~/.ssh/known_hosts
```

or set `known_hosts` to `"none"` / `VPS_KNOWN_HOSTS=none` if you accept the
man-in-the-middle risk.

## Connect to Claude

### Claude Code

```sh
claude mcp add vps -e VPS_HOST=203.0.113.10 -e VPS_USER=deploy -e VPS_KEY_PATH=~/.ssh/id_ed25519 -- vps-mcp
```

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "vps": {
      "command": "vps-mcp",
      "env": {
        "VPS_HOST": "203.0.113.10",
        "VPS_USER": "deploy",
        "VPS_KEY_PATH": "/home/me/.ssh/id_ed25519"
      }
    }
  }
}
```

If `vps-mcp` is not on Claude Desktop's PATH, use the full interpreter path:
`"command": "/path/to/python", "args": ["-m", "vps_mcp"]`.

### Remote MCP clients (HTTP)

```sh
vps-mcp --transport streamable-http --host 0.0.0.0 --port 8765
```

The endpoint is `http://<server>:8765/mcp`. This transport has **no
authentication built in**; put it behind a reverse proxy with auth or a VPN,
never expose it directly to the internet.

## Security notes

- The server runs commands as the configured SSH user. Give Claude a dedicated,
  least-privilege user on the VPS rather than `root`.
- `sudo=true` relies on passwordless sudo (`NOPASSWD` in `sudoers`) for that
  user; scope it to the commands you actually need.
- `vps_run_command` executes exactly what it is given. The tool descriptions
  tell the model to confirm destructive commands with you first, but the
  decision is yours: review commands before approving them in your MCP client.
- Credentials are read from the environment or the hosts file and are never
  returned by any tool.

## Development

```sh
pip install -e ".[dev]"
pytest
```

The tests start an in-process SSH server (via `asyncssh`) that executes
commands with the local shell and serves SFTP, so every tool is exercised end
to end without a real VPS.
