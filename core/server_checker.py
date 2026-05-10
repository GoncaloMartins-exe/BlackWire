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
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    def run(self):
        if self._cancelled:
            return
        
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

        if not self._cancelled:
            self.signals.finished.emit(self.key, online, client)
        elif client:
            try:
                client.close()
            except Exception:
                pass


class ServerChecker:

    def __init__(self):
        self.pool = QThreadPool.globalInstance()

        self.pool.setMaxThreadCount(10)
        self.connections: dict = {}
        self._tasks: set = set()          # mantém tasks vivas até terminarem
        self._running = set()

    def check(self, server: dict, key: str, callback):        
        self._running.add(key)
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
        self._running.discard(key)

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

    def shutdown(self):
        for task in self._tasks:
            task.cancel()
        self._tasks.clear()
        self.pool.waitForDone(0)
        for client in self.connections.values():
            try:
                client.close()
            except Exception:
                pass
        self.connections.clear()

    def reset_running(self):
        self._running.clear()