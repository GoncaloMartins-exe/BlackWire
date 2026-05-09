from PySide6.QtCore import QObject, Signal, QRunnable, QThreadPool
from core.ssh_client import SSHClient


class ServerCheckSignals(QObject):
    finished = Signal(str, bool, object)

class ServerCheckTask(QRunnable):

    def __init__(self, server: dict, key: str, existing_client=None):
        super().__init__()

        self.server = server
        self.key = key
        self.existing_client = existing_client
        self.signals = ServerCheckSignals()

    def run(self):
        # caso a ligação já exista
        if self.existing_client:
            try:
                transport = self.existing_client.client.get_transport()
                if transport and transport.is_active():
                    self.signals.finished.emit(self.key, True, self.existing_client)
                    return
            except Exception:
                pass
            # dead end
            try:
                self.existing_client.close()
            except Exception:
                pass

        # Nova ligação
        client = None
        online = False
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
            if client:
                try:
                    client.close()
                except Exception:
                    pass
            client = None

        self.signals.finished.emit(self.key, online, client)


class ServerChecker:

    def __init__(self):
        self.pool = QThreadPool.globalInstance()

        self.pool.setMaxThreadCount(10)
        self.connections: dict = {}
        self._tasks: set = set()          # mantém tasks vivas até terminarem

    def check(self, server: dict, key: str, callback):
        existing = self.connections.get(key)
        task = ServerCheckTask(server, key, existing_client=existing)
        self._tasks.add(task)
        task.signals.finished.connect(
            lambda k, online, client: self._on_checked(k, online, client, callback, task)
        )
        self.pool.start(task)

    def get_connection(self, key: str):
        return self.connections.get(key)

    def disconnect(self, key: str):
        client = self.connections.pop(key, None)
        if client:
            client.close()

    def _on_checked(self, key: str, online: bool, client, callback, task):
        self._tasks.discard(task)

        if online:
            if client is not self.connections.get(key):
                old = self.connections.pop(key, None)
                if old and old is not client:
                    try:
                        old.close()
                    except Exception:
                        pass
                self.connections[key] = client
        else:
            self.connections.pop(key, None)

        callback(key, online)