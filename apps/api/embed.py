import json

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from config import Config


def main() -> None:
    print(f"Loading model: {Config.get_model_name()}")
    model = SentenceTransformer(Config.get_model_name())

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

    print(f"Saving index to {Config.FAISS_INDEX_PATH}...")
    faiss.write_index(index, Config.FAISS_INDEX_PATH)

    # Save answers (for retrieval)
    print(f"Saving answers to {Config.ANSWERS_JSON_PATH}...")
    with open(Config.ANSWERS_JSON_PATH, "w") as f:
        json.dump(answers, f)

    print("Done!")


if __name__ == "__main__":
    main()
