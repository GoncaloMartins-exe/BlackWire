import paramiko


class SSHClient:

    def __init__(
        self,
        host,
        username,
        password=None,
        key_path=None,
        port=22
    ):
        self.host = host
        self.username = username
        self.password = password
        self.key_path = key_path
        self.port = port

        self.client = None

    def connect(self):
        self.client = paramiko.SSHClient()

        self.client.set_missing_host_key_policy(
            paramiko.AutoAddPolicy()
        )

        kwargs = {
            "hostname": self.host,
            "port": self.port,
            "username": self.username,
            "timeout": 1,
            "banner_timeout": 1,
            "auth_timeout": 1,
        }

        if self.key_path:
            kwargs["key_filename"] = self.key_path
            kwargs["look_for_keys"] = False
            kwargs["allow_agent"] = False

        else:
            kwargs["password"] = self.password

        self.client.connect(**kwargs)

    def execute(self, command, timeout=3):
        if not self.client:
            raise RuntimeError("SSH não conectado.")

        try:
            stdin, stdout, stderr = self.client.exec_command(command, timeout=timeout)
            
            stdout.channel.settimeout(timeout)
            stderr.channel.settimeout(timeout)

            return {
                "stdout": stdout.read().decode(errors="ignore"),
                "stderr": stderr.read().decode(errors="ignore"),
            }
        except Exception as e:
            raise ConnectionError(f"Ligação perdida ou expirada: {e}")
    
    def is_active(self):
        if self.client and self.client.get_transport():
            return self.client.get_transport().is_active()
        return False

    def close(self):
        if self.client:
            self.client.close()
            self.client = None