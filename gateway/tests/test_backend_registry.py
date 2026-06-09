from gateway.app.backend_registry import Backend, BackendRegistry


def test_selects_least_loaded_backend() -> None:
    registry = BackendRegistry()

    registry.register(
        Backend(
            name="backend-1",
            base_url="http://backend-1",
            active_requests=3,
        )
    )
    registry.register(
        Backend(
            name="backend-2",
            base_url="http://backend-2",
            active_requests=1,
        )
    )

    selected = registry.select_least_loaded()

    assert selected.name == "backend-2"


def test_active_request_count_never_becomes_negative() -> None:
    registry = BackendRegistry()

    registry.register(
        Backend(
            name="backend-1",
            base_url="http://backend-1",
        )
    )

    registry.decrement_active_requests("backend-1")

    backend = registry.list_healthy()[0]
    assert backend.active_requests == 0
