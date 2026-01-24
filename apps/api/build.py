import json

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from settings import settings


def main() -> None:
    print(f"Loading model: {settings.model_name}")
    model = SentenceTransformer(settings.model_name)

    print("Loading FAQ data...")
    try:
        with open("faq.json") as f:
            faq = json.load(f)
    except FileNotFoundError:
        print("Error: faq.json not found.")
        return

    questions = [q["question"] for q in faq]
    answers = [q["answer"] for q in faq]

    print("Generating embeddings...")
    embeddings = model.encode(questions)

    # Faiss index
    print("Building FAISS index...")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    embeddings = np.array(embeddings, dtype=np.float32)
    index.add(embeddings)

    print(f"Saving index to {settings.faiss_index_path}...")
    faiss.write_index(index, settings.faiss_index_path)

    # Save answers (for retrieval)
    print(f"Saving answers to {settings.answers_json_path}...")
    with open(settings.answers_json_path, "w") as f:
        json.dump(answers, f)

    print("Done!")


if __name__ == "__main__":
    main()
