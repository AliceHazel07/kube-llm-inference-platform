from typing import Any

from fastapi.testclient import TestClient

from gateway.app.backend_registry import Backend
from gateway.app.main import app
from gateway.app.models import ChatCompletionRequest


def test_health() -> None:
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_chat_request_forwards_to_backend(monkeypatch: Any) -> None:
    async def mock_forward_chat_completion(
        backend: Backend,
        request: ChatCompletionRequest,
    ) -> dict[str, Any]:
        return {
            "id": "chatcmpl-test",
            "model": request.model,
            "backend": backend.name,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "Mock test response",
                    },
                    "finish_reason": "stop",
                }
            ],
        }

    monkeypatch.setattr(
        "gateway.app.main.forward_chat_completion",
        mock_forward_chat_completion,
    )

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
    assert response.json()["model"] == "test-model"
    assert response.json()["backend"] == "mock-vllm-1"
    assert response.json()["choices"][0]["message"]["content"] == ("Mock test response")
