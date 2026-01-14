"""
Business logic for chat/FAQ operations.
Separates business logic from API route handlers.
"""

from typing import cast

import numpy as np
from fastapi import HTTPException

import context
import response
from config import Config
from response import ChatCompletionMessage, ChatCompletionResponse


class ChatService:
    """Service class for handling FAQ chat operations."""

    def __init__(self, similarity_threshold: float = 0.9):
        """
        Initialize chat service.

        Args:
            similarity_threshold: Maximum distance for considering a match valid.
                                 Higher values = stricter matching.
        """
        self.similarity_threshold = similarity_threshold

    def validate_service_ready(self) -> None:
        """
        Validate that the service dependencies are loaded and ready.

        Raises:
            HTTPException: If model, index, or answers are not initialized.
        """
        if context.model is None or context.index is None or context.answers is None:
            raise HTTPException(
                status_code=503,
                detail="Service is still initializing. Please try again in a moment.",
            )

        # Validate that the model is properly initialized
        if len(context.model) == 0 or context.model[0] is None:
            raise HTTPException(
                status_code=503,
                detail="Model is not properly initialized. Please check server logs.",
            )

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

    def search_faq(self, question: str) -> str | None:
        """
        Search for the most relevant FAQ answer using semantic similarity.

        Args:
            question: The user's question to search for.

        Returns:
            The matching answer if found and similarity is above threshold,
            None otherwise.

        Raises:
            HTTPException: If model encoding fails.
        """
        # Ensure model and resources are available (for mypy and runtime safety)
        if context.model is None or context.index is None or context.answers is None:
            raise HTTPException(
                status_code=503,
                detail="Service dependencies not initialized",
            )

        try:
            embedding = context.model.encode([question])
        except AttributeError as e:
            raise HTTPException(
                status_code=503,
                detail=(
                    f"Model encoding failed: {str(e)}. "
                    "Model may not be properly initialized."
                ),
            ) from e

        # Search for the most similar FAQ
        distances, indices = context.index.search(
            np.array(embedding), k=Config.TOP_K_RESULTS
        )

        # Check if similarity is above threshold
        if distances[0][0] > self.similarity_threshold:
            # Distance too large = low similarity
            return None

        # Retrieve the answer
        answer = cast(str, context.answers[indices[0][0]])
        return answer

    def process_chat_request(
        self, messages: list[ChatCompletionMessage]
    ) -> ChatCompletionResponse:
        """
        Process a chat request and return an appropriate response.

        This is the main business logic method that coordinates validation,
        question extraction, FAQ search, and response building.

        Args:
            messages: List of chat completion messages from the request.

        Returns:
            ChatCompletionResponse with the answer or null content if no match.

        Raises:
            HTTPException: If validation fails or service is not ready.
        """
        # Validate service is ready
        self.validate_service_ready()

        # Extract user question
        question = self.extract_user_question(messages)

        # Search for matching FAQ
        answer = self.search_faq(question)

        # Build and return response
        return response.build_chat_completion_response(content=answer)
