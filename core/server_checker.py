from PySide6.QtCore import QObject, Signal, QRunnable, QThreadPool
from core.ssh_client import SSHClient


class ServerCheckSignals(QObject):
    finished = Signal(str, bool)

class ServerCheckTask(QRunnable):

    def __init__(self, server: dict, key: str):
        super().__init__()

        self.server = server
        self.key = key

        self.signals = ServerCheckSignals()

    def run(self):
        online = False
        client = None

        try:
            client = SSHClient(
                host=self.server["host"],
                username=self.server["user"],
                password=self.server.get("password"),
                key_path=self.server.get("key_path"),
                port=self.server.get("port", 22),
            )

            client.connect()

            online = True

        except Exception:
            online = False

        finally:
            if client:
                client.close()

        self.signals.finished.emit(self.key, online)


class ServerChecker:

    def __init__(self):
        self.pool = QThreadPool.globalInstance()

        self.pool.setMaxThreadCount(10)

    def check(self, server: dict, key: str, callback):
        task = ServerCheckTask(server, key)

        task.signals.finished.connect(callback)

        self.pool.start(task)