from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from response import ChatCompletionResponse
import asyncio
import context
import numpy as np
import os
import response


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


@app.post("/chat", response_model=ChatCompletionResponse)
async def chat(query: Query) -> ChatCompletionResponse:
    # Add a 1 second delay in development mode (when DEBUG or DEV env variable is set)
    if os.getenv("DEBUG") == "1" or os.getenv("DEV") == "1":
        await asyncio.sleep(1)

    # Check if model and data are loaded
    if context.model is None or context.index is None or context.answers is None:
        raise HTTPException(
            status_code=503,
            detail="Service is still initializing. Please try again in a moment."
        )
    
    embedding = context.model.encode([query.question])
    distances, indices = context.index.search(np.array(embedding), k=1)  # Top 1 match
    # If distance is too large (low similarity), return null
    similarity_threshold = 0.9  # Adjust based on testing; lower means stricter
    if distances[0][0] > similarity_threshold:  # Higher distance = less similar
        # Return OpenAI format with null content when no match found
        return response.build_chat_completion_response(content=None)
    
    answer = context.answers[indices[0][0]]
    
    # Return OpenAI chat API format
    return response.build_chat_completion_response(content=answer)


# Serve built frontend from /app/web_dist (copied in Docker image)
try:
    app.mount("/", StaticFiles(directory="/app/web_dist", html=True), name="static")
except Exception:
    # In dev or if assets missing, skip mounting
    pass
