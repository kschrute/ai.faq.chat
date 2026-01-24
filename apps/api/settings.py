from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration using Pydantic Settings.
    Reads from environment variables and/or .env file.
    """

    # Model settings
    model_name: str = "all-MiniLM-L6-v2"
    similarity_threshold: float = 0.9

    # Search settings
    top_k_results: int = 1

    # Security / Input validation
    max_question_length: int = 1000
    max_messages_limit: int = 20

    # File paths
    faiss_index_path: str = "index.faiss"
    answers_json_path: str = "answers.json"
    web_dist_path: str = "/app/web_dist"

    # CORS settings
    cors_origins: list[str] = ["http://localhost:5173"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["GET", "POST", "OPTIONS"]
    cors_allow_headers: list[str] = ["content-type", "authorization", "accept"]

    # Development settings
    debug: bool = False
    dev_delay_seconds: float = 1.0

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


# Singleton settings instance
settings = Settings()
