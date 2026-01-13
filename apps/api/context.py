from contextlib import asynccontextmanager
from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
from config import Config
import faiss
import json

# Global variables to store loaded model and data
model = None
index = None
answers = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load model and data once when app starts
    global model, index, answers
    try:
        print("Loading ML model and FAQ data...")
        model = SentenceTransformer(Config.get_model_name())
        index = faiss.read_index(Config.FAISS_INDEX_PATH)
        with open(Config.ANSWERS_JSON_PATH, "r") as f:
            answers = json.load(f)
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
