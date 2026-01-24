from unittest.mock import MagicMock, Mock, patch

import numpy as np
import pytest

from engine import FAQEngine


class TestFAQEngine:
    def test_init_sets_default_state(self) -> None:
        engine = FAQEngine()

        assert engine.model is None
        assert engine.index is None
        assert engine.answers is None
        assert engine.is_ready is False

    def test_is_ready_returns_false_before_load(self) -> None:
        engine = FAQEngine()

        assert engine.is_ready is False

    @patch("engine.SentenceTransformer")
    @patch("engine.faiss.read_index")
    @patch("builtins.open", create=True)
    @patch("engine.json.load")
    def test_load_resources_success(
        self,
        mock_json_load: Mock,
        mock_open: Mock,
        mock_read_index: Mock,
        mock_sentence_transformer: Mock,
    ) -> None:
        mock_model = MagicMock()
        mock_sentence_transformer.return_value = mock_model
        mock_read_index.return_value = MagicMock()
        mock_json_load.return_value = ["Answer 1", "Answer 2"]

        engine = FAQEngine()
        engine.load_resources()

        assert engine.is_ready is True
        assert engine.model is mock_model
        mock_model.eval.assert_called_once()

    @patch("engine.SentenceTransformer")
    def test_load_resources_failure_sets_not_ready(
        self, mock_sentence_transformer: Mock
    ) -> None:
        mock_sentence_transformer.side_effect = Exception("Model load failed")

        engine = FAQEngine()
        engine.load_resources()

        assert engine.is_ready is False

    @pytest.mark.asyncio
    async def test_asearch_raises_when_not_ready(self) -> None:
        engine = FAQEngine()

        with pytest.raises(RuntimeError, match="Engine is not ready"):
            await engine.asearch("test query")

    @pytest.mark.asyncio
    async def test_asearch_returns_answer_when_similar(self) -> None:
        engine = FAQEngine()
        engine._ready = True
        engine.model = MagicMock()
        engine.model.encode.return_value = np.array([[0.1, 0.2, 0.3]])
        engine.index = MagicMock()
        engine.index.search.return_value = (
            np.array([[0.5]]),  # distance below threshold
            np.array([[0]]),  # index
        )
        engine.answers = ["First answer", "Second answer"]

        result = await engine.asearch("test query")

        assert result == "First answer"
        engine.model.encode.assert_called_once_with(["test query"])

    @pytest.mark.asyncio
    async def test_asearch_returns_none_when_distance_exceeds_threshold(self) -> None:
        engine = FAQEngine()
        engine._ready = True
        engine.model = MagicMock()
        engine.model.encode.return_value = np.array([[0.1, 0.2, 0.3]])
        engine.index = MagicMock()
        engine.index.search.return_value = (
            np.array([[2.0]]),  # distance above threshold (default 0.9)
            np.array([[0]]),
        )
        engine.answers = ["Answer"]

        result = await engine.asearch("unrelated query")

        assert result is None

    @pytest.mark.asyncio
    async def test_asearch_returns_none_when_index_out_of_bounds(self) -> None:
        engine = FAQEngine()
        engine._ready = True
        engine.model = MagicMock()
        engine.model.encode.return_value = np.array([[0.1, 0.2, 0.3]])
        engine.index = MagicMock()
        engine.index.search.return_value = (
            np.array([[0.5]]),
            np.array([[99]]),  # index out of bounds
        )
        engine.answers = ["Only one answer"]

        result = await engine.asearch("test")

        assert result is None

    @pytest.mark.asyncio
    async def test_asearch_returns_none_when_negative_index(self) -> None:
        engine = FAQEngine()
        engine._ready = True
        engine.model = MagicMock()
        engine.model.encode.return_value = np.array([[0.1, 0.2, 0.3]])
        engine.index = MagicMock()
        engine.index.search.return_value = (
            np.array([[0.5]]),
            np.array([[-1]]),  # FAISS returns -1 for no match
        )
        engine.answers = ["Answer"]

        result = await engine.asearch("test")

        assert result is None

    def test_search_sync_returns_none_when_model_is_none(self) -> None:
        engine = FAQEngine()
        engine.model = None
        engine.index = MagicMock()
        engine.answers = ["Answer"]

        result = engine._search_sync("test")

        assert result is None

    def test_search_sync_returns_none_when_index_is_none(self) -> None:
        engine = FAQEngine()
        engine.model = MagicMock()
        engine.index = None
        engine.answers = ["Answer"]

        result = engine._search_sync("test")

        assert result is None

    def test_search_sync_returns_none_when_answers_is_none(self) -> None:
        engine = FAQEngine()
        engine.model = MagicMock()
        engine.index = MagicMock()
        engine.answers = None

        result = engine._search_sync("test")

        assert result is None

    def test_search_sync_raises_on_encode_error(self) -> None:
        engine = FAQEngine()
        engine.model = MagicMock()
        engine.model.encode.side_effect = Exception("Encode failed")
        engine.index = MagicMock()
        engine.answers = ["Answer"]

        with pytest.raises(Exception, match="Encode failed"):
            engine._search_sync("test")
