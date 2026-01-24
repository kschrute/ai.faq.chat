"""
Integration tests for FAQEngine using real model with test-specific FAQ data.

These tests load the actual embedding model but use a separate test index
to verify end-to-end search functionality without depending on production data.
"""

import faiss
import numpy as np
import pytest
from sentence_transformers import SentenceTransformer

from engine import FAQEngine
from settings import settings

# Test FAQ data - independent from production faq.json
TEST_FAQ_DATA = [
    {
        "question": "How do I contact support?",
        "answer": "Email us at support@example.com or call 1-800-SUPPORT.",
    },
    {
        "question": "What payment methods do you accept?",
        "answer": "We accept Visa, Mastercard, PayPal, and Apple Pay.",
    },
    {
        "question": "How do I cancel my subscription?",
        "answer": "Go to Account Settings > Subscription > Cancel.",
    },
    {
        "question": "What is your shipping policy?",
        "answer": "Free shipping on orders over $50. Delivery takes 3-5 business days.",
    },
    {
        "question": "Do you offer international shipping?",
        "answer": "Yes, we ship to over 100 countries. Takes 7-14 business days.",
    },
]


def _build_test_engine() -> FAQEngine:
    """Build a FAQEngine with test-specific FAQ data (not production data)."""
    import torch

    torch.set_num_threads(1)

    engine = FAQEngine()

    # Load model
    engine.model = SentenceTransformer(settings.model_name, device="cpu")
    engine.model.eval()

    # Generate embeddings for test questions
    questions = [item["question"] for item in TEST_FAQ_DATA]
    answers = [item["answer"] for item in TEST_FAQ_DATA]

    embeddings = engine.model.encode(questions)

    # Build in-memory FAISS index (no file I/O needed)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype("float32"))

    engine.index = index
    engine.answers = answers
    engine._ready = True

    return engine


# Module-level engine instance (created once, reused across tests)
_test_engine: FAQEngine | None = None


@pytest.fixture(scope="module")
def engine() -> FAQEngine:
    """Get or create the test FAQEngine with test-specific FAQ data."""
    global _test_engine
    if _test_engine is None:
        _test_engine = _build_test_engine()
    return _test_engine


class TestEngineIntegration:
    """Integration tests using test-specific FAQ data."""

    @pytest.mark.asyncio
    async def test_exact_question_contact_support(self, engine: FAQEngine) -> None:
        """Exact FAQ questions should return their answers."""
        result = await engine.asearch("How do I contact support?")

        assert result is not None
        assert "support@example.com" in result

    @pytest.mark.asyncio
    async def test_paraphrased_question_support(self, engine: FAQEngine) -> None:
        """Paraphrased questions should match semantically similar FAQs."""
        result = await engine.asearch("How can I reach customer service?")

        assert result is not None
        assert "support" in result.lower() or "1-800" in result

    @pytest.mark.asyncio
    async def test_exact_question_payment(self, engine: FAQEngine) -> None:
        """Payment question should return correct answer."""
        result = await engine.asearch("What payment methods do you accept?")

        assert result is not None
        assert "Visa" in result

    @pytest.mark.asyncio
    async def test_paraphrased_question_payment(self, engine: FAQEngine) -> None:
        """Paraphrased payment question should match."""
        result = await engine.asearch("What payment options are available?")

        assert result is not None
        assert "Visa" in result or "PayPal" in result

    @pytest.mark.asyncio
    async def test_exact_question_cancel_subscription(self, engine: FAQEngine) -> None:
        """Subscription cancellation question should return correct answer."""
        result = await engine.asearch("How do I cancel my subscription?")

        assert result is not None
        assert "Account Settings" in result

    @pytest.mark.asyncio
    async def test_paraphrased_question_subscription(self, engine: FAQEngine) -> None:
        """Paraphrased subscription question should match."""
        result = await engine.asearch("I want to unsubscribe from the service")

        assert result is not None
        assert "Cancel" in result or "Subscription" in result

    @pytest.mark.asyncio
    async def test_exact_question_shipping(self, engine: FAQEngine) -> None:
        """Shipping policy question should return correct answer."""
        result = await engine.asearch("What is your shipping policy?")

        assert result is not None
        assert "3-5 business days" in result

    @pytest.mark.asyncio
    async def test_exact_question_international(self, engine: FAQEngine) -> None:
        """International shipping question should return correct answer."""
        result = await engine.asearch("Do you offer international shipping?")

        assert result is not None
        assert "100 countries" in result

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
        result = await engine.asearch("HOW DO I CONTACT SUPPORT?")

        assert result is not None
        assert "support@example.com" in result

    @pytest.mark.asyncio
    async def test_question_with_typo(self, engine: FAQEngine) -> None:
        """Minor typos should still match semantically."""
        result = await engine.asearch("How do I cancle my subscriptin?")

        # May or may not match depending on threshold - just verify no crash
        if result is not None:
            assert "Cancel" in result or "Subscription" in result
