"""Host configuration for vps_mcp.

Two sources are merged, in this order of precedence:

1. A JSON hosts file (``VPS_HOSTS_FILE``, default ``~/.config/vps-mcp/hosts.json``)
   that may describe several named hosts and a ``default`` entry.
2. Flat environment variables describing one host, registered under the name
   given by ``VPS_NAME`` (default ``"default"``):

   ``VPS_HOST``            hostname or IP (required for this source)
   ``VPS_PORT``            SSH port (default 22)
   ``VPS_USER``            SSH username (default: current OS user)
   ``VPS_KEY_PATH``        path to a private key file
   ``VPS_KEY_PASSPHRASE``  passphrase for that key
   ``VPS_PASSWORD``        password authentication
   ``VPS_KNOWN_HOSTS``     known_hosts path, or ``"none"`` to skip host-key checks
   ``VPS_CONNECT_TIMEOUT`` seconds (default 15)

Secrets never have to live in the hosts file: a host entry may name an
environment variable with ``password_env`` / ``key_passphrase_env`` instead.
"""

from __future__ import annotations

import getpass
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional

DEFAULT_HOSTS_FILE = Path("~/.config/vps-mcp/hosts.json")
DEFAULT_PORT = 22
DEFAULT_CONNECT_TIMEOUT = 15.0


class ConfigError(ValueError):
    """Raised when host configuration is missing or invalid."""


@dataclass(frozen=True)
class HostConfig:
    """Everything needed to open one SSH connection."""

    name: str
    host: str
    port: int = DEFAULT_PORT
    username: str = field(default_factory=getpass.getuser)
    key_path: Optional[str] = None
    key_passphrase: Optional[str] = None
    password: Optional[str] = None
    known_hosts: Optional[str] = None  # None => use OpenSSH defaults; "none" => disable
    connect_timeout: float = DEFAULT_CONNECT_TIMEOUT

    def public_summary(self) -> Dict[str, Any]:
        """Return a description safe to show to an LLM (no secrets)."""
        return {
            "name": self.name,
            "host": self.host,
            "port": self.port,
            "username": self.username,
            "auth": self._auth_method(),
            "host_key_checking": self.known_hosts != "none",
        }

    def _auth_method(self) -> str:
        if self.key_path:
            return "key"
        if self.password:
            return "password"
        return "agent/default-keys"

    def asyncssh_kwargs(self) -> Dict[str, Any]:
        """Translate into keyword arguments for ``asyncssh.connect``."""
        kwargs: Dict[str, Any] = {
            "host": self.host,
            "port": self.port,
            "username": self.username,
            "connect_timeout": self.connect_timeout,
        }
        if self.key_path:
            kwargs["client_keys"] = [_expand(self.key_path)]
        if self.key_passphrase:
            kwargs["passphrase"] = self.key_passphrase
        if self.password:
            kwargs["password"] = self.password
        if self.known_hosts == "none":
            kwargs["known_hosts"] = None
        elif self.known_hosts:
            kwargs["known_hosts"] = _expand(self.known_hosts)
        return kwargs


def _expand(path: str) -> str:
    return str(Path(path).expanduser())


def _env_secret(entry: Dict[str, Any], direct_key: str, env_key: str) -> Optional[str]:
    if entry.get(direct_key):
        return str(entry[direct_key])
    env_name = entry.get(env_key)
    if env_name:
        return os.environ.get(str(env_name)) or None
    return None


def _host_from_entry(name: str, entry: Dict[str, Any]) -> HostConfig:
    if not isinstance(entry, dict) or not entry.get("host"):
        raise ConfigError(f"Host entry '{name}' must be an object with a 'host' field.")
    known_hosts = entry.get("known_hosts")
    if known_hosts is False:
        known_hosts = "none"
    return HostConfig(
        name=name,
        host=str(entry["host"]),
        port=int(entry.get("port", DEFAULT_PORT)),
        username=str(entry.get("username") or getpass.getuser()),
        key_path=entry.get("key_path"),
        key_passphrase=_env_secret(entry, "key_passphrase", "key_passphrase_env"),
        password=_env_secret(entry, "password", "password_env"),
        known_hosts=str(known_hosts) if known_hosts else None,
        connect_timeout=float(entry.get("connect_timeout", DEFAULT_CONNECT_TIMEOUT)),
    )


def _host_from_env(env: Dict[str, str]) -> Optional[HostConfig]:
    host = env.get("VPS_HOST")
    if not host:
        return None
    known_hosts = env.get("VPS_KNOWN_HOSTS")
    return HostConfig(
        name=env.get("VPS_NAME", "default"),
        host=host,
        port=int(env.get("VPS_PORT", DEFAULT_PORT)),
        username=env.get("VPS_USER") or getpass.getuser(),
        key_path=env.get("VPS_KEY_PATH") or None,
        key_passphrase=env.get("VPS_KEY_PASSPHRASE") or None,
        password=env.get("VPS_PASSWORD") or None,
        known_hosts=known_hosts.lower() if known_hosts and known_hosts.lower() == "none" else (known_hosts or None),
        connect_timeout=float(env.get("VPS_CONNECT_TIMEOUT", DEFAULT_CONNECT_TIMEOUT)),
    )


@dataclass
class Registry:
    """All configured hosts plus the name of the default one."""

    hosts: Dict[str, HostConfig]
    default: Optional[str]

    def get(self, name: Optional[str]) -> HostConfig:
        """Resolve a host by name, falling back to the default host."""
        if not self.hosts:
            raise ConfigError(
                "No VPS hosts are configured. Set VPS_HOST (and VPS_USER, VPS_KEY_PATH or "
                "VPS_PASSWORD), or create a hosts file at "
                f"{DEFAULT_HOSTS_FILE} (see hosts.example.json)."
            )
        target = name or self.default
        if target is None:
            if len(self.hosts) == 1:
                return next(iter(self.hosts.values()))
            raise ConfigError(
                "Several hosts are configured and no default is set. Pass the 'host' "
                f"argument explicitly. Available: {', '.join(sorted(self.hosts))}."
            )
        try:
            return self.hosts[target]
        except KeyError:
            raise ConfigError(
                f"Unknown host '{target}'. Available: {', '.join(sorted(self.hosts)) or 'none'}."
            ) from None


def load_registry(
    env: Optional[Dict[str, str]] = None, hosts_file: Optional[Path] = None
) -> Registry:
    """Build the host registry from the hosts file and environment variables."""
    env = dict(os.environ if env is None else env)
    hosts: Dict[str, HostConfig] = {}
    default: Optional[str] = None

    path = hosts_file or Path(env.get("VPS_HOSTS_FILE") or DEFAULT_HOSTS_FILE)
    path = path.expanduser()
    if path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ConfigError(f"Hosts file {path} is not valid JSON: {exc}") from exc
        entries = data.get("hosts", {}) if isinstance(data, dict) else {}
        if not isinstance(entries, dict):
            raise ConfigError(f"Hosts file {path}: 'hosts' must be an object.")
        for name, entry in entries.items():
            hosts[name] = _host_from_entry(name, entry)
        default = data.get("default") if isinstance(data, dict) else None

    env_host = _host_from_env(env)
    if env_host:
        hosts[env_host.name] = env_host
        if default is None:
            default = env_host.name

    if default is not None and default not in hosts:
        raise ConfigError(f"Default host '{default}' is not defined in the hosts file.")
    return Registry(hosts=hosts, default=default)
