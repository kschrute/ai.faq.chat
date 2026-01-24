import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from chat_service import ChatService
from engine import FAQEngine
from exceptions import InvalidInputError, ModelError, ServiceNotReadyError
from response import ChatCompletionRequest, ChatCompletionResponse
from settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Manage the lifecycle of the application resources.
    Initializes the FAQ Engine on startup and cleans up on shutdown.
    """
    # Initialize and load the engine
    engine = FAQEngine()
    engine.load_resources()

    # Store engine in app state for dependency injection
    app.state.engine = engine

    yield

    # Cleanup (if any needed in future)
    pass


app = FastAPI(lifespan=lifespan)


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)


@app.exception_handler(ServiceNotReadyError)
async def service_not_ready_handler(
    request: Request, exc: ServiceNotReadyError
) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={"detail": str(exc)},
    )


@app.exception_handler(ModelError)
async def model_error_handler(request: Request, exc: ModelError) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal model error occurred. Please try again later."},
    )


@app.exception_handler(InvalidInputError)
async def invalid_input_handler(
    request: Request, exc: InvalidInputError
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


def get_chat_service(request: Request) -> ChatService:
    """
    Dependency provider for ChatService.
    Injects the shared FAQEngine instance from app state.
    """
    return ChatService(engine=request.app.state.engine)


@app.post("/chat", response_model=ChatCompletionResponse)
async def chat(
    request: ChatCompletionRequest,
    service: Annotated[ChatService, Depends(get_chat_service)],
) -> ChatCompletionResponse:
    """
    Handle chat completion requests.

    Processes user messages and returns FAQ answers using semantic similarity search.
    """
    # Add a delay in development mode
    if settings.debug:
        await asyncio.sleep(settings.dev_delay_seconds)

    # Delegate business logic to service layer
    return await service.process_chat_request(request.messages)


# Serve built frontend from /app/web_dist (copied in Docker image)
try:
    app.mount(
        "/", StaticFiles(directory=settings.web_dist_path, html=True), name="static"
    )
except Exception:
    # In dev or if assets missing, skip mounting
    pass
