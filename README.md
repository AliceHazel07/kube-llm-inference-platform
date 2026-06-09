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

```
uv sync
uv run fastapi dev gateway/app/main.py
```

