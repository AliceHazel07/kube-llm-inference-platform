FROM python:3.11-slim

WORKDIR /app

# Install minimal build deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml /app/
COPY README.md /app/

RUN pip install --no-cache-dir "fastapi[standard]>=0.128.8" "httpx>=0.28.1"

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "gateway.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
