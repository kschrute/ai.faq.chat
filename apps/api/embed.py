"""
Build FAISS index from FAQ data.

This script reads FAQ questions, generates embeddings using a sentence transformer,
and creates a FAISS index for semantic search.

Usage:
    python embed.py
"""

import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from config import Config

FAQ_FILE = "faq.json"


def build_index() -> None:
    """Build FAISS index from FAQ data and save to disk."""
    faq_path = Path(FAQ_FILE)
    if not faq_path.exists():
        raise FileNotFoundError(f"FAQ file not found: {faq_path}")

    model_name = Config.get_model_name()
    print(f"Loading model: {model_name}")
    model = SentenceTransformer(model_name)

    print(f"Loading FAQ data from: {faq_path}")
    with open(faq_path) as f:
        faq = json.load(f)

    if not faq:
        raise ValueError("FAQ file is empty")

    questions = [q["question"] for q in faq]
    answers = [q["answer"] for q in faq]

    print(f"Generating embeddings for {len(questions)} questions...")
    embeddings = model.encode(questions)
    embeddings = np.array(embeddings, dtype=np.float32)

    print("Building FAISS index...")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    print(f"Saving index to: {Config.FAISS_INDEX_PATH}")
    faiss.write_index(index, Config.FAISS_INDEX_PATH)

    print(f"Saving answers to: {Config.ANSWERS_JSON_PATH}")
    with open(Config.ANSWERS_JSON_PATH, "w") as f:
        json.dump(answers, f)

    print(f"Index built successfully with {len(questions)} entries.")


if __name__ == "__main__":
    build_index()
