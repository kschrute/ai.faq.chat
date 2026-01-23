# FAQ Chat

[![CI/CD](https://github.com/kschrute/ai-faq-chat/actions/workflows/ci.yml/badge.svg)](https://github.com/kschrute/ai-faq-chat/actions/workflows/ci.yml)

A lightweight, privacy-focused question-answering system using Retrieval-Augmented Generation (RAG).

Instead of fine-tuning a Large Language Model (LLM), this project leverages **Sentence Transformers** to embed questions and **FAISS** for similarity search. This approach is:
- **Fast:** No heavy model inference.
- **Private:** Runs entirely locally (or on your server).
- **Deterministic:** Returns pre-written answers, eliminating hallucinations.
- **Easy to Update:** Just add to a JSON file and rebuild the index.

## Features

- 🧠 **Semantic Search:** Understands the intent behind questions, not just keywords.
- 🚀 **Modern Stack:** Built with Turborepo, React 19, Vite, FastAPI, and Python.
- ⚡ **High Performance:** Uses FAISS for efficient vector similarity search.
- 🐳 **Docker Ready:** Includes Dockerfile and Fly.io configuration for easy deployment.

## Demo

The demo is available at [ai-faq-chat.fly.dev](https://ai-faq-chat.fly.dev)

![Demo](demo.jpeg)

## Architecture

The project is structured as a monorepo managed by **Turborepo**:

- `apps/api`: Python (FastAPI) backend. Handles embeddings (SentenceTransformers) and vector search (FAISS).
- `apps/web`: React 19 (Vite) frontend. Uses UnoCSS for styling.
- `packages/`: Shared configurations (TypeScript, etc.).

For a detailed deep-dive into the AI architecture, see [AGENTS.md](./AGENTS.md).

## Prerequisites

- [pnpm](https://pnpm.io) (Package manager)
- [uv](https://astral.sh/uv) (Python toolchain)

## Getting Started

1. **Install Dependencies**
   
   This command installs Node.js dependencies and sets up the Python virtual environments via `uv`.

   ```shell
   pnpm deps
   ```

2. **Start Development Server**

   Starts both the API (port 8000) and Web App (port 5173).

   ```shell
   pnpm dev
   ```
   
   - Web App: [http://localhost:5173](http://localhost:5173)
   - API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## Managing Content

### Updating the FAQ

1. Edit the source file at `apps/api/faq.json`.
   ```json
   [
     {
       "question": "How do I reset my password?",
       "answer": "Go to settings and click 'Reset Password'."
     }
   ]
   ```

2. Rebuild the vector index:
   ```shell
   pnpm build
   ```
   This generates the embeddings and updates the FAISS index (`apps/api/index.faiss`).

### Configuration

You can tweak the model and similarity thresholds in `apps/api/config.py`:
- `SIMILARITY_THRESHOLD`: Adjust matching strictness (default: 0.85).
- `MODEL_NAME`: Change the embedding model (default: `all-MiniLM-L6-v2`).

## Development Commands

- **Build:** `pnpm build` (Builds web assets and vector index)
- **Lint:** `pnpm lint` (Runs Biome for JS/TS and Ruff for Python)
- **Typecheck:** `pnpm typecheck`
- **Test:** `pnpm test`

## API Usage

The API is compatible with the OpenAI Chat Completion format, making it easy to integrate with existing tools.

**Example Request:**

```shell
curl -X POST http://localhost:8000/chat \
    -H "Content-Type: application/json" \
    -d '{"model": "faq-chat", "messages": [{"role": "user", "content": "How do I reset my password?"}]}'
```

**Example Response:**

```json
{
  "id": "chatcmpl-...",
  "object": "chat.completion",
  "created": 1768231509,
  "model": "faq-chat",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "Go to settings and click 'Reset Password'."
    },
    "finish_reason": "stop"
  }]
}
```
