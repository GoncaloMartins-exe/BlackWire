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
            "timeout": 10,
        }

        if self.key_path:
            kwargs["key_filename"] = self.key_path
            kwargs["look_for_keys"] = False
            kwargs["allow_agent"] = False

        else:
            kwargs["password"] = self.password

        self.client.connect(**kwargs)

    def execute(self, command):
        if not self.client:
            raise RuntimeError("SSH não conectado.")

        stdin, stdout, stderr = self.client.exec_command(command)

        return {
            "stdout": stdout.read().decode(errors="ignore"),
            "stderr": stderr.read().decode(errors="ignore"),
        }

    def close(self):
        if self.client:
            self.client.close()
            self.client = None