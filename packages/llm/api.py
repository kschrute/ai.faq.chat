from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np
from pydantic import BaseModel
import asyncio

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow React app origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index('faq_index.faiss')
with open('answers.json', 'r') as f:
    answers = json.load(f)

class Query(BaseModel):
    question: str

@app.post('/ask')
async def ask(query: Query):
    await asyncio.sleep(0.9)
    embedding = model.encode([query.question])
    distances, indices = index.search(np.array(embedding), k=1)  # Top 1 match
    # If distance is too large (low similarity), return null
    similarity_threshold = 0.9  # Adjust based on testing; lower means stricter
    if distances[0][0] > similarity_threshold:  # Higher distance = less similar
        return {'answer': False}
    return {'answer': answers[indices[0][0]]}
