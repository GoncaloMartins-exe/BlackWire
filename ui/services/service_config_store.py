import json
import os

from ui.widgets.helper import resource_path

_CONFIG_DIR = resource_path("config")
_CONFIG_FILE = os.path.join(_CONFIG_DIR, "services.json")

_DEFAULTS = {
    "wireguard": {
        "display_name": "WireGuard VPN",
        "unit": "wg-quick@wg0",
        "config_path": "/etc/wireguard/wg0.conf",
        "log_lines": 100,
    },
    "samba": {
        "display_name": "Samba NAS",
        "unit": "smbd",
        "config_path": "/etc/samba/smb.conf",
        "log_lines": 100,
    },
}


def _ensure_file():
    os.makedirs(_CONFIG_DIR, exist_ok=True)
    if not os.path.isfile(_CONFIG_FILE):
        with open(_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(_DEFAULTS, f, indent=2, ensure_ascii=False)


def load_all() -> dict:
    _ensure_file()
    with open(_CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_service(service_key: str) -> dict:
    data = load_all()
    return data.get(service_key, _DEFAULTS.get(service_key, {}))


def save_service(service_key: str, config: dict):
    data = load_all()
    data[service_key] = config
    with open(_CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)