# FAQ Chat

[![CI/CD](https://github.com/kschrute/ai-faq-chat/actions/workflows/ci.yml/badge.svg)](https://github.com/kschrute/ai-faq-chat/actions/workflows/ci.yml)

Question-answering system for an FAQ without fine-tuning a language model. Instead of training a model, it uses Retrieval-Augmented Generation (RAG), leveraging a pre-trained embedding model and a vector search index to retrieve answers from a pre-existing FAQ dataset. 

This approach is simpler and faster to set up than fine-tuning, as it requires no model training, making it ideal for small FAQ datasets or rapid prototyping. It embeds FAQ questions into a vector space, searches for the most similar question to a user’s query, and returns the corresponding answer. If no sufficiently similar question is found, it returns `false`.

## Demo

The demo is available at [ai-faq-chat.fly.dev](https://ai-faq-chat.fly.dev)

![Demo](demo.jpeg)

## Tech Stack

### Frontend (apps/web)
- **React 19** with TypeScript
- **Vite** for build tooling and dev server
- **UnoCSS** for utility-first CSS
- **React Compiler** for automatic optimization

### Backend (apps/api)
- **FastAPI** for the REST API
- **FAISS** (Facebook AI Similarity Search) for vector similarity search
- **Sentence Transformers** for text embeddings
- **Python 3.11+** with type hints
- **uv** for fast Python package management

### Tooling
- **pnpm** for JavaScript package management
- **Turbo** for monorepo build orchestration
- **Biome** for JavaScript/TypeScript formatting
- **Ruff** for Python linting and formatting
- **Husky** for git hooks

## How It Works

This system uses **Retrieval-Augmented Generation (RAG)** to answer FAQ questions without requiring model fine-tuning:

1. **Embedding Generation**: FAQ questions are converted into high-dimensional vectors using a pre-trained sentence transformer model
2. **Vector Indexing**: These embeddings are stored in a FAISS index for efficient similarity search
3. **Query Processing**: When a user asks a question, it's embedded using the same model
4. **Similarity Search**: The system searches the FAISS index to find the most similar FAQ question
5. **Answer Retrieval**: If the similarity score exceeds a threshold, the corresponding answer is returned; otherwise, `null` is returned

This approach is faster to implement than fine-tuning and doesn't require training data or GPU resources.

## Project Structure

This is a monorepo managed with pnpm workspaces and Turbo:

```
ai-faq-chat/
├── apps/
│   ├── api/          # FastAPI backend
│   │   ├── api.py           # Main API endpoints
│   │   ├── chat_service.py  # Chat logic and embedding search
│   │   ├── embed.py         # Script to generate embeddings
│   │   ├── faq.json         # FAQ questions and answers
│   │   └── index.faiss      # FAISS vector index (generated)
│   └── web/          # React frontend
│       └── src/             # React application source
├── packages/         # Shared packages (if any)
└── turbo.json        # Turbo configuration
```

## Prerequisites

- [pnpm](https://pnpm.io)
- [uv](https://astral.sh/uv)

## Getting Started

To install the dependencies run:

```shell
pnpm deps
```

And to start the API and the Web app run this after:

```shell
pnpm dev
```

## Updating FAQ

If you update FAQ in the `apps/api/faq.json` file, run the following to rebuild the index:

```shell
pnpm build
```

## Testing the API

You can use `curl` to test the API or use the UI at http://localhost:5173

```shell
curl -X POST http://localhost:8000/chat \
    -H "Content-Type: application/json" \
    -d '{"model": "faq-chat", "messages": [{"role": "user", "content": "How do I reset my password?"}]}'
```

You should see a response like this:

```json
{
  "id": "chatcmpl-ad02cfa696a1",
  "object": "chat.completion",
  "created": 1768231509,
  "model": "faq-chat",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Go to settings and click 'Reset Password'."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "total_tokens": 0
  }
}
```

And if you ask something that's not in the FAQ:

```shell
curl -X POST http://localhost:8000/chat \
    -H "Content-Type: application/json" \
    -d '{"model": "faq-chat", "messages": [{"role": "user", "content": "What is quantum computing?"}]}'
```

The response should be:

```json
{
  "id": "chatcmpl-8d069d933415",
  "object": "chat.completion",
  "created": 1768231526,
  "model": "faq-chat",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": null
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "total_tokens": 0
  }
}
```
