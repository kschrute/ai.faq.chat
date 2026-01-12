from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import asyncio
import context
import numpy as np
import os


app = FastAPI(lifespan=context.lifespan)


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:5173"],  # Allow React app origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


class Query(BaseModel):
    question: str


@app.post("/ask")
async def ask(query: Query):
    # Add a 1 second delay in development mode (when DEBUG or DEV env variable is set)
    if os.getenv("DEBUG") == "1" or os.getenv("DEV") == "1":
        await asyncio.sleep(1)

    # Check if model and data are loaded
    if context.model is None or context.index is None or context.answers is None:
        raise HTTPException(
            status_code=503,
            detail="Service is still initializing. Please try again in a moment."
        )
    
    # await asyncio.sleep(0.9)
    embedding = context.model.encode([query.question])
    distances, indices = context.index.search(np.array(embedding), k=1)  # Top 1 match
    # If distance is too large (low similarity), return null
    similarity_threshold = 0.9  # Adjust based on testing; lower means stricter
    if distances[0][0] > similarity_threshold:  # Higher distance = less similar
        return {"answer": False}
    return {"answer": context.answers[indices[0][0]]}


# Serve built frontend from /app/web_dist (copied in Docker image)
try:
    app.mount("/", StaticFiles(directory="/app/web_dist", html=True), name="static")
except Exception:
    # In dev or if assets missing, skip mounting
    pass
