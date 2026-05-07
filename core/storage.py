import json
import keyring
from pathlib import Path
from platformdirs import user_data_dir

class ServerManager:
    def __init__(self):
        self.app_name = "BlackWire"
        
        self.data_dir = Path(user_data_dir(self.app_name))
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.data_dir / "servers.json"

    def load_servers(self) -> list[dict]:
        if not self.config_file.exists():
            return []
            
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                servers = json.load(f)
            
            for srv in servers:
                if srv.get("auth") == "password":
                    vault_id = f"{srv['user']}@{srv['host']}"
                    password = keyring.get_password(self.app_name, vault_id)
                    srv["password"] = password if password else ""
            return servers
        except Exception as e:
            print(f"Erro ao carregar: {e}")
            return []

    def save_all(self, servers: list[dict]):
        save_data = []
        
        for srv in servers:
            if srv.get("auth") == "password" and srv.get("password"):
                vault_id = f"{srv['user']}@{srv['host']}"
                keyring.set_password(self.app_name, vault_id, srv["password"])
            
            clean_srv = {k: v for k, v in srv.items() if k != "password"}
            save_data.append(clean_srv)

        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(save_data, f, indent=4)

    def delete_server_creds(self, server: dict):
        if server.get("auth") == "password":
            vault_id = f"{server['user']}@{server['host']}"
            try:
                keyring.delete_password(self.app_name, vault_id)
            except keyring.errors.PasswordDeleteError:
                pass