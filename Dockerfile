# AutoAIForge — Docker image
# Multi-stage build: slim production image
# Free tier hosting: Railway, Render, Fly.io, Google Cloud Run

FROM python:3.11-slim AS base

# System deps for sentence-transformers
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ libffi-dev git curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ── Dependency layer (cached unless requirements.txt changes) ─────────────────
FROM base AS deps
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Pre-download the sentence-transformer model so runtime doesn't need internet
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# ── Application layer ─────────────────────────────────────────────────────────
FROM deps AS app
COPY . .

# Ensure data directory exists
RUN mkdir -p /app/data /app/logs /app/generated_tools

# ── Runtime ───────────────────────────────────────────────────────────────────
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# Default: run the pipeline once (for cron-triggered containers)
CMD ["python", "main.py"]
