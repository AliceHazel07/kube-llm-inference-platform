from fastapi.testclient import TestClient

from gateway.app.main import app


def test_health() -> None:
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_chat_request_selects_backend() -> None:
    payload = {
        "model": "test-model",
        "messages": [
            {
                "role": "user",
                "content": "hello",
            }
        ],
    }

    with TestClient(app) as client:
        response = client.post(
            "/v1/chat/completions",
            json=payload,
        )

    assert response.status_code == 200
    assert response.json()["selected_backend"] == "mock-vllm-1"
