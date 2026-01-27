# -------------------------------------------------------------------------------------------------------------------- #
# Web Builder                                                                                                          #
# -------------------------------------------------------------------------------------------------------------------- #

FROM node:20-alpine AS web-builder

WORKDIR /app

# Enable pnpm via corepack and align version
RUN corepack enable && corepack prepare pnpm@10.10.0 --activate

# Use root workspace lockfile for deterministic, workspace-aware install
COPY pnpm-lock.yaml pnpm-workspace.yaml package.json ./

# Pre-copy package manifests to maximize caching
COPY apps/web/package.json ./apps/web/package.json
COPY packages/tsconfig/package.json ./packages/tsconfig/package.json

# Install with dev deps and filter to web workspace
RUN pnpm -w install --frozen-lockfile --prod=false --filter @ai-faq-chat/web...

# Copy the actual sources and build
COPY packages/tsconfig ./packages/tsconfig
COPY apps/web ./apps/web

# Build the web app
# RUN pnpm -w --filter @ai-faq-chat/web build
RUN pnpm --filter @ai-faq-chat/web build

# -------------------------------------------------------------------------------------------------------------------- #
# Python Builder                                                                                                       #
# -------------------------------------------------------------------------------------------------------------------- #

FROM python:3.11-slim AS python-builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System dependency for faiss-cpu (OpenMP)
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv and verify installation
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:/root/.local/bin:$PATH"
RUN uv --version

# WORKDIR /app
WORKDIR /app/apps/api

# Copy Python project files for dependency installation
# COPY apps/api/pyproject.toml apps/api/uv.lock ./apps/api/
COPY apps/api/pyproject.toml apps/api/uv.lock ./

# Install Python dependencies using uv
# WORKDIR /app/apps/api
RUN uv sync --frozen

# Pre-download the embedding model to reduce cold start
RUN uv run python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# -------------------------------------------------------------------------------------------------------------------- #
# Runtime                                                                                                              #
# -------------------------------------------------------------------------------------------------------------------- #

FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# System dependency for faiss-cpu (OpenMP)
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the backend app and data files (index.faiss, answers.json)
COPY apps/api ./apps/api

# Copy built web assets from the web builder stage
COPY --from=web-builder /app/apps/web/dist /app/web_dist

# Copy only the virtual environment from the builder stage
COPY --from=python-builder /app/apps/api/.venv ./apps/api/.venv

# Set PATH to use the virtual environment's Python and binaries
ENV PATH="/app/apps/api/.venv/bin:$PATH"

# -------------------------------------------------------------------------------------------------------------------- #
# Environment                                                                                                          #
# -------------------------------------------------------------------------------------------------------------------- #

WORKDIR /app/apps/api

# PyTorch memory optimizations
ENV PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128
ENV OMP_NUM_THREADS=1
ENV MKL_NUM_THREADS=1
ENV NUMEXPR_NUM_THREADS=1

# Disable telemetry
ENV TURBO_TELEMETRY_DISABLED=1
ENV DO_NOT_TRACK=1

ENV MODEL="all-MiniLM-L6-v2"
ENV PORT=8000

EXPOSE 8000

CMD ["sh", "-c", "/app/apps/api/.venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
