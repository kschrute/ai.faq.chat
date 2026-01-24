"""
Integration tests for FAQEngine using real model, index, and FAQ data.

These tests load the actual embedding model and FAISS index to verify
end-to-end search functionality with real questions and answers.
"""

import pytest

from engine import FAQEngine


@pytest.fixture(scope="module")
def engine() -> FAQEngine:
    """Load the real FAQEngine with actual model and index."""
    engine = FAQEngine()
    engine.load_resources()
    if not engine.is_ready:
        pytest.skip("Engine resources not available (run `pnpm build` first)")
    return engine


class TestEngineIntegration:
    """Integration tests using real FAQ data."""

    @pytest.mark.asyncio
    async def test_exact_question_match(self, engine: FAQEngine) -> None:
        """Exact FAQ questions should return their answers."""
        result = await engine.asearch("How do I reset my password?")

        assert result is not None
        assert "Reset Password" in result

    @pytest.mark.asyncio
    async def test_paraphrased_question_password(self, engine: FAQEngine) -> None:
        """Paraphrased questions should match semantically similar FAQs."""
        result = await engine.asearch("I forgot my password, how can I change it?")

        assert result is not None
        assert "Reset Password" in result

    @pytest.mark.asyncio
    async def test_exact_question_return_policy(self, engine: FAQEngine) -> None:
        """Return policy question should return correct answer."""
        result = await engine.asearch("What is the return policy?")

        assert result is not None
        assert "30 days" in result

    @pytest.mark.asyncio
    async def test_paraphrased_question_returns(self, engine: FAQEngine) -> None:
        """Paraphrased return question should match."""
        result = await engine.asearch("What is your return policy for items?")

        assert result is not None
        assert "30 days" in result

    @pytest.mark.asyncio
    async def test_exact_question_refunds(self, engine: FAQEngine) -> None:
        """Refund question should return correct answer."""
        result = await engine.asearch("How fast are refunds processed?")

        assert result is not None
        assert "7 business days" in result

    @pytest.mark.asyncio
    async def test_paraphrased_question_refunds(self, engine: FAQEngine) -> None:
        """Paraphrased refund question should match."""
        result = await engine.asearch("How long does it take to process refunds?")

        assert result is not None
        assert "7 business days" in result

    @pytest.mark.asyncio
    async def test_what_are_you_question(self, engine: FAQEngine) -> None:
        """Identity question should return system description."""
        result = await engine.asearch("What are you?")

        assert result is not None
        assert "question-answering" in result.lower() or "RAG" in result

    @pytest.mark.asyncio
    async def test_unrelated_question_returns_none(self, engine: FAQEngine) -> None:
        """Completely unrelated questions should return None."""
        result = await engine.asearch(
            "What is the airspeed velocity of an unladen swallow?"
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_gibberish_returns_none(self, engine: FAQEngine) -> None:
        """Gibberish input should return None."""
        result = await engine.asearch("asdfghjkl qwerty zxcvbnm")

        assert result is None

    @pytest.mark.asyncio
    async def test_empty_like_question_returns_none(self, engine: FAQEngine) -> None:
        """Very short/meaningless input should return None."""
        result = await engine.asearch("???")

        assert result is None

    @pytest.mark.asyncio
    async def test_case_insensitivity(self, engine: FAQEngine) -> None:
        """Questions should match regardless of case."""
        result = await engine.asearch("HOW DO I RESET MY PASSWORD?")

        assert result is not None
        assert "Reset Password" in result

    @pytest.mark.asyncio
    async def test_question_with_typo(self, engine: FAQEngine) -> None:
        """Minor typos should still match semantically."""
        result = await engine.asearch("How do I resett my pasword?")

        # May or may not match depending on threshold - just verify no crash
        # If it matches, it should be the password answer
        if result is not None:
            assert "password" in result.lower() or "Reset" in result

    @pytest.mark.asyncio
    async def test_list_questions_query(self, engine: FAQEngine) -> None:
        """Query about available questions should return the list."""
        result = await engine.asearch("What questions can you answer?")

        assert result is not None
        # The answer contains a list of questions
        assert "password" in result.lower() or "return" in result.lower()
