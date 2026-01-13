from chat_service import ChatService
from config import Config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from response import ChatCompletionResponse, ChatCompletionMessage
from typing import Optional
import asyncio
import context


app = FastAPI(lifespan=context.lifespan)

# Initialize chat service
chat_service = ChatService(similarity_threshold=Config.get_similarity_threshold())

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.get_cors_origins(),
    allow_credentials=Config.CORS_ALLOW_CREDENTIALS,
    allow_methods=Config.CORS_ALLOW_METHODS,
    allow_headers=Config.CORS_ALLOW_HEADERS,
)


class ChatCompletionRequest(BaseModel):
    """OpenAI chat completion request format."""

    model: Optional[str] = None
    messages: list[ChatCompletionMessage]
    # Optional fields for OpenAI compatibility (not used but accepted)
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    stream: Optional[bool] = None


@app.post("/chat", response_model=ChatCompletionResponse)
async def chat(request: ChatCompletionRequest) -> ChatCompletionResponse:
    """
    Handle chat completion requests.

    Processes user messages and returns FAQ answers using semantic similarity search.
    """
    # Add a delay in development mode
    if Config.is_dev_mode():
        await asyncio.sleep(Config.DEV_DELAY_SECONDS)

    # Delegate business logic to service layer
    return chat_service.process_chat_request(request.messages)


# Serve built frontend from /app/web_dist (copied in Docker image)
try:
    app.mount(
        "/", StaticFiles(directory=Config.WEB_DIST_PATH, html=True), name="static"
    )
except Exception:
    # In dev or if assets missing, skip mounting
    pass
