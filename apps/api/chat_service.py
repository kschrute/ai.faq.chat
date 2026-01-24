"""
Business logic for chat/FAQ operations.
Separates business logic from API route handlers.
"""

import asyncio
from typing import Any

import numpy as np
from fastapi import HTTPException

import response
from config import Config
from context import AppContext
from response import ChatCompletionMessage, ChatCompletionResponse


class ChatService:
    """Service class for handling FAQ chat operations."""

    def __init__(self, similarity_threshold: float = 0.9):
        """
        Initialize chat service.

        Args:
            similarity_threshold: Maximum L2 distance for considering a match valid.
                                  Lower values = stricter matching.
        """
        self.similarity_threshold = similarity_threshold

    def validate_context(self, ctx: AppContext | None) -> AppContext:
        """
        Validate that the application context is loaded and ready.

        Args:
            ctx: The application context from dependency injection.

        Returns:
            The validated AppContext.

        Raises:
            HTTPException: If context is not initialized.
        """
        if ctx is None:
            raise HTTPException(
                status_code=503,
                detail="Service is still initializing. Please try again in a moment.",
            )
        return ctx

    def extract_user_question(self, messages: list[ChatCompletionMessage]) -> str:
        """
        Extract the user's question from the messages array.

        Args:
                messages: List of chat completion messages.

        Returns:
                The content of the last user message.

        Raises:
                HTTPException: If no user message is found or content is empty.
        """
        user_messages = [msg for msg in messages if msg.role == "user"]
        if not user_messages:
            raise HTTPException(
                status_code=400, detail="No user message found in messages array"
            )

        last_user_message = user_messages[-1]
        if not last_user_message.content:
            raise HTTPException(status_code=400, detail="User message content is empty")

        return last_user_message.content

    async def search_faq(self, question: str, ctx: AppContext) -> str | None:
        """
        Search for the most relevant FAQ answer using semantic similarity.
        Runs blocking model operations in a separate thread.

        Args:
            question: The user's question to search for.
            ctx: The application context with model and index.

        Returns:
            The matching answer if found and distance is below threshold,
            None otherwise.

        Raises:
            HTTPException: If model encoding fails.
        """
        model = ctx.model
        index: Any = ctx.index  # Cast to Any for FAISS SWIG bindings
        answers = ctx.answers

        loop = asyncio.get_running_loop()

        def _search_operation() -> tuple[Any, Any]:
            # Blocking operation: Model encoding
            embedding = model.encode([question])
            # Blocking operation: FAISS search
            distances, indices = index.search(
                np.array(embedding), k=Config.TOP_K_RESULTS
            )
            return distances, indices

        try:
            distances, indices = await loop.run_in_executor(None, _search_operation)
        except AttributeError as e:
            raise HTTPException(
                status_code=503,
                detail=(
                    f"Model encoding failed: {e}. "
                    "Model may not be properly initialized."
                ),
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error during search operation: {e}"
            ) from e

        # Check if similarity is acceptable (distance < threshold)
        # Note: Using L2 distance, so lower is better/more similar
        if distances[0][0] > self.similarity_threshold:
            return None

        return answers[indices[0][0]]

    async def process_chat_request(
        self, messages: list[ChatCompletionMessage], ctx: AppContext | None
    ) -> ChatCompletionResponse:
        """
        Process a chat request and return an appropriate response.

        This is the main business logic method that coordinates validation,
        question extraction, FAQ search, and response building.

        Args:
            messages: List of chat completion messages from the request.
            ctx: The application context from dependency injection.

        Returns:
            ChatCompletionResponse with the answer or null content if no match.

        Raises:
            HTTPException: If validation fails or service is not ready.
        """
        validated_ctx = self.validate_context(ctx)
        question = self.extract_user_question(messages)
        answer = await self.search_faq(question, validated_ctx)
        return response.build_chat_completion_response(content=answer)
