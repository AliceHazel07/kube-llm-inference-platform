from dataclasses import dataclass
from threading import Lock


@dataclass
class Backend:
    name: str
    base_url: str
    healthy: bool = True
    active_requests: int = 0


class BackendRegistry:
    def __init__(self) -> None:
        self._backends: dict[str, Backend] = {}
        self._lock = Lock()

    def register(self, backend: Backend) -> None:
        with self._lock:
            self._backends[backend.name] = backend

    def list_healthy(self) -> list[Backend]:
        with self._lock:
            return [backend for backend in self._backends.values() if backend.healthy]

    def select_least_loaded(self) -> Backend:
        healthy_backends = self.list_healthy()

        if not healthy_backends:
            raise RuntimeError("No healthy inference backends available")

        return min(
            healthy_backends,
            key=lambda backend: backend.active_requests,
        )
