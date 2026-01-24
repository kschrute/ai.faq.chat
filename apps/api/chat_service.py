from engine import FAQEngine
from exceptions import InvalidInputError, ServiceNotReadyError
from response import (
    ChatCompletionMessage,
    ChatCompletionResponse,
    build_chat_completion_response,
)


class ChatService:
    """Service class for handling FAQ chat operations using the FAQEngine."""

    def __init__(self, engine: FAQEngine):
        """
        Initialize chat service with a RAG engine.
        """
        self.engine = engine

    async def process_chat_request(
        self, messages: list[ChatCompletionMessage]
    ) -> ChatCompletionResponse:
        """
        Process a chat request and return an appropriate response.

        Args:
                messages: List of chat completion messages from the request.

        Returns:
                ChatCompletionResponse with the answer or null content if no match.

        Raises:
                ServiceNotReadyError: If service is not ready.
                InvalidInputError: If validation fails.
                ModelError: If model fails.
        """
        if not self.engine.is_ready:
            raise ServiceNotReadyError(
                "Service is still initializing. Please try again in a moment."
            )

        question = self._extract_user_question(messages)

        # The service delegates the "how" to the engine
        # Any ModelErrors from engine will propagate up to be handled by exception
        # handlers
        answer = await self.engine.asearch(question)

        return build_chat_completion_response(content=answer)

    def _extract_user_question(self, messages: list[ChatCompletionMessage]) -> str:
        """
        Extract the last user message from the conversation history.
        """
        # Iterate backwards to find the most recent user message
        for msg in reversed(messages):
            if msg.role == "user" and msg.content:
                return msg.content
        raise InvalidInputError("No valid user question found")
