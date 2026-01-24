import json
import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import cast

import faiss
import torch
from fastapi import FastAPI, Request
from sentence_transformers import SentenceTransformer

from config import Config


@dataclass
class AppContext:
    """Application context holding ML model and FAQ data."""

    model: SentenceTransformer
    index: faiss.Index
    answers: list[str]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """FastAPI lifespan context manager for startup/shutdown."""
    # Startup: Load model and data once when app starts
    try:
        print("Loading ML model and FAQ data...")

        # Memory optimizations for PyTorch
        torch.set_num_threads(1)
        os.environ["TOKENIZERS_PARALLELISM"] = "false"

        # Load model with memory-efficient settings
        model = SentenceTransformer(
            Config.get_model_name(),
            device="cpu",
            model_kwargs={"dtype": torch.float32},
        )
        model.eval()  # Set to evaluation mode to reduce memory

        index = faiss.read_index(Config.FAISS_INDEX_PATH)
        with open(Config.ANSWERS_JSON_PATH) as f:
            answers = cast(list[str], json.load(f))

        app.state.context = AppContext(model=model, index=index, answers=answers)
        print("ML model and FAQ data loaded successfully!")
    except Exception as e:
        print(f"Error loading model or data: {e}")
        app.state.context = None

    yield

    # Shutdown: Cleanup
    print("Shutting down...")
    if hasattr(app.state, "context") and app.state.context is not None:
        del app.state.context
        import gc

        gc.collect()


def get_context(request: Request) -> AppContext | None:
    """Dependency to get the application context from request."""
    return getattr(request.app.state, "context", None)
