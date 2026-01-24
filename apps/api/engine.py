import asyncio
import json
import logging
import os
from typing import Any, cast

import faiss
import numpy as np
import torch
from sentence_transformers import SentenceTransformer

from settings import settings

logger = logging.getLogger(__name__)


class FAQEngine:
    """
    Encapsulates the RAG (Retrieval-Augmented Generation) logic.
    Handles model loading, embedding, and vector search.
    """

    def __init__(self) -> None:
        self.model: SentenceTransformer | None = None
        self.index: faiss.Index | None = None
        self.answers: list[str] | None = None
        self._ready = False

    def load_resources(self) -> None:
        """Load the ML model, FAISS index, and answer map."""
        try:
            logger.info("Loading ML model and FAQ data...")

            # Optimization for CPU
            torch.set_num_threads(1)
            os.environ["TOKENIZERS_PARALLELISM"] = "false"

            self.model = SentenceTransformer(
                settings.model_name,
                device="cpu",
                model_kwargs={"dtype": torch.float32},
            )
            self.model.eval()

            self.index = faiss.read_index(settings.faiss_index_path)

            with open(settings.answers_json_path) as f:
                self.answers = cast(list[str], json.load(f))

            self._ready = True
            logger.info("Engine loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load engine resources: {e}")
            self._ready = False
            # We don't raise here to allow the app to start,
            # but liveness probes should fail or requests will 503.

    @property
    def is_ready(self) -> bool:
        return self._ready

    async def asearch(self, query: str) -> str | None:
        """
        Async wrapper for the blocking search operation.
        """
        if not self.is_ready:
            raise RuntimeError("Engine is not ready")

        loop = asyncio.get_running_loop()
        # Run CPU-bound search in a thread pool
        return await loop.run_in_executor(None, self._search_sync, query)

    def _search_sync(self, query: str) -> str | None:
        """Blocking internal search implementation."""
        # Type guards
        if self.model is None or self.index is None or self.answers is None:
            return None

        try:
            embedding = self.model.encode([query])

            # Cast for type safety with FAISS
            index = cast(Any, self.index)
            distances, indices = index.search(
                np.array(embedding), k=settings.top_k_results
            )

            # Note: Using L2 distance, so lower is better/more similar
            if distances[0][0] > settings.similarity_threshold:
                return None

            idx = indices[0][0]
            if 0 <= idx < len(self.answers):
                return self.answers[idx]
            return None

        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise
