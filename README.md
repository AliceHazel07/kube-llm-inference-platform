# Kubernetes-Native LLM Inference Platform

A learning-focused infrastructure project for building and operating scalable
LLM inference services on Kubernetes.

## Current scope

- OpenAI-compatible inference gateway
- Backend registration and health tracking
- Least-loaded request routing
- Dockerized gateway
- Kubernetes deployment
- Prometheus metrics and queue-aware autoscaling
- vLLM integration
- Failure injection and performance benchmarking

## Current status

The first milestone implements a minimal FastAPI gateway with backend
registration and routing.

## Run locally

Quick instructions to run the gateway and two mock backends locally using Docker Compose.

Start services:

```bash
docker compose up --build
```

This will expose:

- Gateway: http://localhost:8000
- Mock backend 1: http://localhost:8001
- Mock backend 2: http://localhost:8002

You can also run services directly with `uvicorn` for development:

```bash
# Run gateway
uvicorn gateway.app.main:app --reload --port 8000

# Run mock backend (in separate terminals)
BACKEND_NAME=mock-vllm-1 uvicorn mock_backend.main:app --reload --port 8001
BACKEND_NAME=mock-vllm-2 uvicorn mock_backend.main:app --reload --port 8002
```


