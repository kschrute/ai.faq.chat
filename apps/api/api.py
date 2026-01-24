import asyncio

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

import context
from chat_service import ChatService
from config import Config
from exceptions import InvalidInputError, ModelError, ServiceNotReadyError
from response import ChatCompletionRequest, ChatCompletionResponse

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
    return await chat_service.process_chat_request(request.messages)


# Serve built frontend from /app/web_dist (copied in Docker image)
try:
    app.mount(
        "/", StaticFiles(directory=Config.WEB_DIST_PATH, html=True), name="static"
    )
except Exception:
    # In dev or if assets missing, skip mounting
    pass
