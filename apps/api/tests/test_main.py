# Ensure the API package (apps/api) is on the import path when running tests

from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from exceptions import ModelError
from main import app, get_chat_service, lifespan


@pytest.fixture
def mock_engine() -> Mock:
    """Create a mock FAQEngine."""
    engine = Mock()
    engine.is_ready = True
    engine.asearch = AsyncMock(return_value="Mocked answer")
    engine.load_resources = Mock()
    return engine


@pytest.fixture
def test_client(mock_engine: Mock) -> TestClient:
    """Create a test client with mocked engine."""
    app.state.engine = mock_engine
    return TestClient(app, raise_server_exceptions=False)


class TestChatEndpoint:
    def test_chat_returns_answer(
        self, test_client: TestClient, mock_engine: Mock
    ) -> None:
        response = test_client.post(
            "/chat",
            json={"messages": [{"role": "user", "content": "How do I reset?"}]},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["object"] == "chat.completion"
        assert data["choices"][0]["message"]["content"] == "Mocked answer"
        assert data["choices"][0]["message"]["role"] == "assistant"

    def test_chat_returns_null_when_no_match(
        self, test_client: TestClient, mock_engine: Mock
    ) -> None:
        mock_engine.asearch.return_value = None

        response = test_client.post(
            "/chat",
            json={"messages": [{"role": "user", "content": "Unknown"}]},
        )

        assert response.status_code == 200
        assert response.json()["choices"][0]["message"]["content"] is None

    def test_chat_returns_400_for_empty_messages(self, test_client: TestClient) -> None:
        response = test_client.post("/chat", json={"messages": []})

        assert response.status_code == 400
        assert "No valid user question" in response.json()["detail"]

    def test_chat_returns_400_for_no_user_message(
        self, test_client: TestClient
    ) -> None:
        response = test_client.post(
            "/chat",
            json={"messages": [{"role": "assistant", "content": "Hello"}]},
        )

        assert response.status_code == 400

    def test_chat_returns_503_when_not_ready(
        self, test_client: TestClient, mock_engine: Mock
    ) -> None:
        mock_engine.is_ready = False

        response = test_client.post(
            "/chat",
            json={"messages": [{"role": "user", "content": "Test"}]},
        )

        assert response.status_code == 503
        assert "initializing" in response.json()["detail"].lower()

    def test_chat_returns_405_for_get(self, test_client: TestClient) -> None:
        response = test_client.get("/chat")

        assert response.status_code == 405

    def test_chat_accepts_optional_fields(
        self, test_client: TestClient, mock_engine: Mock
    ) -> None:
        response = test_client.post(
            "/chat",
            json={
                "model": "faq-chat",
                "messages": [{"role": "user", "content": "Test"}],
                "temperature": 0.7,
                "max_tokens": 100,
                "stream": False,
            },
        )

        assert response.status_code == 200


class TestExceptionHandlers:
    def test_service_not_ready_returns_503(
        self, test_client: TestClient, mock_engine: Mock
    ) -> None:
        mock_engine.is_ready = False

        response = test_client.post(
            "/chat",
            json={"messages": [{"role": "user", "content": "Test"}]},
        )

        assert response.status_code == 503

    def test_model_error_returns_500(
        self, test_client: TestClient, mock_engine: Mock
    ) -> None:
        mock_engine.asearch.side_effect = ModelError("Model failed")

        response = test_client.post(
            "/chat",
            json={"messages": [{"role": "user", "content": "Test"}]},
        )

        assert response.status_code == 500
        assert "internal model error" in response.json()["detail"].lower()

    def test_invalid_input_returns_400(
        self, test_client: TestClient, mock_engine: Mock
    ) -> None:
        mock_engine.is_ready = True

        response = test_client.post(
            "/chat",
            json={"messages": [{"role": "system", "content": "Only system"}]},
        )

        assert response.status_code == 400


class TestLifespan:
    @pytest.mark.asyncio
    async def test_lifespan_initializes_engine(self) -> None:
        test_app = FastAPI()

        with patch("main.FAQEngine") as mock_engine_class:
            mock_engine = Mock()
            mock_engine_class.return_value = mock_engine

            async with lifespan(test_app):
                assert test_app.state.engine is mock_engine
                mock_engine.load_resources.assert_called_once()


class TestDependencies:
    def test_get_chat_service_returns_service_with_engine(
        self, mock_engine: Mock
    ) -> None:
        mock_request = Mock()
        mock_request.app.state.engine = mock_engine

        service = get_chat_service(mock_request)

        assert service.engine is mock_engine
