from typing import Any

import httpx

from gateway.app.backend_registry import Backend
from gateway.app.models import ChatCompletionRequest


class BackendRequestError(RuntimeError):
    pass


async def forward_chat_completion(
    backend: Backend,
    request: ChatCompletionRequest,
) -> dict[str, Any]:
    url = f"{backend.base_url}/v1/chat/completions"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=request.model_dump(),
                timeout=30.0,
            )

        response.raise_for_status()
        return response.json()

    except httpx.TimeoutException as exc:
        raise BackendRequestError(f"Backend request timed out: {backend.name}") from exc

    except httpx.HTTPStatusError as exc:
        raise BackendRequestError(
            f"Backend returned HTTP {exc.response.status_code}: {backend.name}"
        ) from exc

    except httpx.RequestError as exc:
        raise BackendRequestError(f"Could not reach backend: {backend.name}") from exc
