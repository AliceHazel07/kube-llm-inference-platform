from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, HTTPException

from gateway.app.backend_registry import Backend, BackendRegistry
from gateway.app.models import (
    BackendStatus,
    ChatCompletionRequest,
)


registry = BackendRegistry()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    registry.register(
        Backend(
            name="mock-vllm-1",
            base_url="http://localhost:8001",
        )
    )
    registry.register(
        Backend(
            name="mock-vllm-2",
            base_url="http://localhost:8002",
        )
    )
    yield


app = FastAPI(
    title="Kubernetes LLM Inference Gateway",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/backends", response_model=list[BackendStatus])
async def list_backends() -> list[BackendStatus]:
    return [
        BackendStatus(
            name=backend.name,
            base_url=backend.base_url,
            healthy=backend.healthy,
            active_requests=backend.active_requests,
        )
        for backend in registry.list_healthy()
    ]


@app.post("/v1/chat/completions")
async def create_chat_completion(
    request: ChatCompletionRequest,
) -> dict[str, object]:
    try:
        backend = registry.select_least_loaded()
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return {
        "model": request.model,
        "selected_backend": backend.name,
        "message_count": len(request.messages),
        "status": "routing_only",
    }
