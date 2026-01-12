FROM node:20-alpine AS web-builder

WORKDIR /app

# Enable pnpm via corepack and align version
RUN corepack enable && corepack prepare pnpm@10.10.0 --activate

# Use root workspace lockfile for deterministic, workspace-aware install
COPY pnpm-lock.yaml pnpm-workspace.yaml package.json ./

# Pre-copy package manifest to maximize caching
COPY apps/web/package.json ./apps/web/package.json

# Install with dev deps and filter to web workspace
RUN pnpm -w install --frozen-lockfile --prod=false --filter @ai.faq/web...

# Copy the actual sources and build
COPY apps/web ./apps/web
# RUN pnpm -w --filter @ai.faq/web build
RUN pnpm --filter web run build

FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# System dependency for faiss-cpu (OpenMP)
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first to leverage Docker layer caching
COPY apps/api/requirements.txt ./apps/api/requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --no-compile --only-binary=:all: -r ./apps/api/requirements.txt

# Pre-download the embedding model to reduce cold start
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Copy the backend app and data files (index.faiss, answers.json)
COPY apps/api ./apps/api

# Copy built web assets from the web builder stage
COPY --from=web-builder /app/apps/web/dist /app/web_dist

# Run from the backend package directory
WORKDIR /app/apps/api

# Fly sets PORT at runtime; default to 8000 locally
ENV MODEL="all-MiniLM-L6-v2"
ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000}"]
