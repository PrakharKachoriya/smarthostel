# ---- Stage 1: Build dependencies ----
FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

# Install system dependencies required to build Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and build wheels
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# ---- Stage 2: Runtime container ----
FROM python:3.12-slim-bookworm

WORKDIR /app

# Copy wheels and install only runtime dependencies
COPY --from=builder /wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt

# Copy your application code
COPY app /app

# Optional: environment and default command
ENV PYTHONUNBUFFERED=1

# Entry point of app
CMD ["uvicorn", "app.main:app", "--ws", "websockets", "--workers",  "8" , "--limit-concurrency", "1000", "--loop", "uvloop", "--host", "0.0.0.0", "--port", "8000"]
    