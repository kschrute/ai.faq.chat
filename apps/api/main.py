import asyncio
import logging
import time
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
from logging_config import setup_logging
from middleware import RateLimitMiddleware, SecurityMiddleware
from response import ChatCompletionRequest, ChatCompletionResponse
from settings import settings

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)


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

# Add security middleware
app.add_middleware(SecurityMiddleware)

# Add rate limiting (100 requests per minute per IP)
app.add_middleware(RateLimitMiddleware, calls=100, period=60)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    # Log incoming request
    logger.info(
        "Request started",
        extra={
            "method": request.method,
            "url": str(request.url),
            "client_host": request.client.host if request.client else None,
        },
    )

    response = await call_next(request)

    # Log response
    process_time = time.time() - start_time
    logger.info(
        "Request completed",
        extra={
            "method": request.method,
            "url": str(request.url),
            "status_code": response.status_code,
            "process_time": process_time,
        },
    )

    return response


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


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Basic health check endpoint."""
    return {"status": "healthy"}


@app.get("/ready")
async def readiness_check(request: Request) -> JSONResponse:
    """Readiness check endpoint - checks if engine is loaded."""
    try:
        if not request.app.state.engine.is_ready:
            return JSONResponse(
                status_code=503,
                content={"status": "not_ready", "detail": "Engine not initialized"},
            )
        return {"status": "ready"}
    except AttributeError:
        # Engine not loaded (e.g., in tests)
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "detail": "Engine not initialized"},
        )


@app.get("/metrics")
async def metrics() -> dict[str, str]:
    """Basic metrics endpoint."""
    return {"status": "ok", "service": "faq-chat", "version": "0.1.0"}


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
