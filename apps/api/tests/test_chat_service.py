from unittest.mock import AsyncMock, Mock

import pytest

from chat_service import ChatService
from exceptions import InvalidInputError, ServiceNotReadyError
from response import ChatCompletionMessage


@pytest.fixture
def mock_engine() -> Mock:
    """Create a mock FAQEngine with default ready state."""
    engine = Mock()
    engine.is_ready = True
    engine.asearch = AsyncMock(return_value="Test answer")
    return engine


@pytest.fixture
def chat_service(mock_engine: Mock) -> ChatService:
    """Create a ChatService with a mock engine."""
    return ChatService(engine=mock_engine)


class TestChatService:
    @pytest.mark.asyncio
    async def test_process_chat_request_returns_answer(
        self, chat_service: ChatService, mock_engine: Mock
    ) -> None:
        messages = [ChatCompletionMessage(role="user", content="How do I reset?")]

        response = await chat_service.process_chat_request(messages)

        mock_engine.asearch.assert_called_once_with("How do I reset?")
        assert response.choices[0].message.content == "Test answer"
        assert response.choices[0].message.role == "assistant"

    @pytest.mark.asyncio
    async def test_process_chat_request_returns_null_when_no_match(
        self, chat_service: ChatService, mock_engine: Mock
    ) -> None:
        mock_engine.asearch.return_value = None
        messages = [ChatCompletionMessage(role="user", content="Unknown question")]

        response = await chat_service.process_chat_request(messages)

        assert response.choices[0].message.content is None

    @pytest.mark.asyncio
    async def test_process_chat_request_raises_when_not_ready(
        self, mock_engine: Mock
    ) -> None:
        mock_engine.is_ready = False
        service = ChatService(engine=mock_engine)
        messages = [ChatCompletionMessage(role="user", content="Test")]

        with pytest.raises(ServiceNotReadyError):
            await service.process_chat_request(messages)

    @pytest.mark.asyncio
    async def test_process_chat_request_extracts_last_user_message(
        self, chat_service: ChatService, mock_engine: Mock
    ) -> None:
        messages = [
            ChatCompletionMessage(role="user", content="First question"),
            ChatCompletionMessage(role="assistant", content="First answer"),
            ChatCompletionMessage(role="user", content="Second question"),
        ]

        await chat_service.process_chat_request(messages)

        mock_engine.asearch.assert_called_once_with("Second question")

    @pytest.mark.asyncio
    async def test_process_chat_request_skips_assistant_messages(
        self, chat_service: ChatService, mock_engine: Mock
    ) -> None:
        messages = [
            ChatCompletionMessage(role="user", content="User question"),
            ChatCompletionMessage(role="assistant", content="Assistant response"),
        ]

        await chat_service.process_chat_request(messages)

        mock_engine.asearch.assert_called_once_with("User question")

    @pytest.mark.asyncio
    async def test_process_chat_request_raises_when_no_user_message(
        self, chat_service: ChatService
    ) -> None:
        messages = [ChatCompletionMessage(role="assistant", content="Only assistant")]

        with pytest.raises(InvalidInputError, match="No valid user question found"):
            await chat_service.process_chat_request(messages)

    @pytest.mark.asyncio
    async def test_process_chat_request_raises_when_empty_messages(
        self, chat_service: ChatService
    ) -> None:
        messages: list[ChatCompletionMessage] = []

        with pytest.raises(InvalidInputError, match="No valid user question found"):
            await chat_service.process_chat_request(messages)

    @pytest.mark.asyncio
    async def test_process_chat_request_skips_empty_user_content(
        self, chat_service: ChatService, mock_engine: Mock
    ) -> None:
        messages = [
            ChatCompletionMessage(role="user", content="Valid question"),
            ChatCompletionMessage(role="user", content=""),
        ]

        await chat_service.process_chat_request(messages)

        mock_engine.asearch.assert_called_once_with("Valid question")

    @pytest.mark.asyncio
    async def test_process_chat_request_response_format(
        self, chat_service: ChatService
    ) -> None:
        messages = [ChatCompletionMessage(role="user", content="Test")]

        response = await chat_service.process_chat_request(messages)

        assert response.object == "chat.completion"
        assert response.model == "faq-chat"
        assert len(response.choices) == 1
        assert response.choices[0].index == 0
        assert response.choices[0].finish_reason == "stop"
