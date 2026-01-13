"""
Application configuration settings.
Centralizes constants and environment-specific configuration.
"""

import os
from typing import Optional


class Config:
    """Application configuration class."""

    # Model settings
    DEFAULT_MODEL_NAME: str = "all-MiniLM-L6-v2"
    SIMILARITY_THRESHOLD: float = 0.9  # Maximum distance for FAQ matching

    # Search settings
    TOP_K_RESULTS: int = 1  # Number of top results to retrieve

    # File paths
    FAISS_INDEX_PATH: str = "index.faiss"
    ANSWERS_JSON_PATH: str = "answers.json"
    WEB_DIST_PATH: str = "/app/web_dist"

    # CORS settings
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    # Development settings
    DEV_DELAY_SECONDS: float = 1.0

    @staticmethod
    def get_cors_origins() -> list[str]:
        """Get CORS allowed origins from environment or use defaults."""
        origins = ["http://localhost:5173"]

        # Add custom CORS origin if specified
        custom_origin = os.getenv("CORS_ORIGIN")
        if custom_origin:
            origins.insert(0, custom_origin)
        else:
            # Default to allow all origins if not specified
            origins.insert(0, "*")

        return origins

    @staticmethod
    def get_model_name() -> str:
        """Get the model name from environment or use default."""
        return os.getenv("MODEL") or Config.DEFAULT_MODEL_NAME

    @staticmethod
    def is_dev_mode() -> bool:
        """Check if running in development mode."""
        return os.getenv("DEBUG") == "1" or os.getenv("DEV") == "1"

    @staticmethod
    def get_similarity_threshold() -> float:
        """
        Get similarity threshold from environment or use default.

        Returns:
            Float value for similarity threshold. Can be configured via
            SIMILARITY_THRESHOLD environment variable.
        """
        threshold_str = os.getenv("SIMILARITY_THRESHOLD")
        if threshold_str:
            try:
                return float(threshold_str)
            except ValueError:
                pass
        return Config.SIMILARITY_THRESHOLD


# Create a singleton config instance
config = Config()
