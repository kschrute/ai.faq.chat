import json
import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import cast

import faiss
import torch
from fastapi import FastAPI
from sentence_transformers import SentenceTransformer

from config import Config

# Global variables to store loaded model and data
model: SentenceTransformer | None = None
index: faiss.Index | None = None
answers: list[str] | None = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup: Load model and data once when app starts
    global model, index, answers
    try:
        print("Loading ML model and FAQ data...")

        # Memory optimizations for PyTorch
        torch.set_num_threads(1)
        os.environ["TOKENIZERS_PARALLELISM"] = "false"

        # Load model with memory-efficient settings
        model = SentenceTransformer(
            Config.get_model_name(),
            device="cpu",  # Explicitly use CPU
            model_kwargs={
                "dtype": torch.float32
            },  # Use float32 instead of float16 for CPU
        )
        model.eval()  # Set to evaluation mode to reduce memory

        index = faiss.read_index(Config.FAISS_INDEX_PATH)
        with open(Config.ANSWERS_JSON_PATH) as f:
            answers = cast(list[str], json.load(f))
        print("ML model and FAQ data loaded successfully!")
    except Exception as e:
        print(f"Error loading model or data: {e}")
        # Keep model, index, answers as None - endpoints will return 503
        model = None
        index = None
        answers = None

    yield
    # Shutdown: Cleanup if needed (optional)
    print("Shutting down...")
    # Clear model from memory
    if model is not None:
        del model
        import gc

        gc.collect()
