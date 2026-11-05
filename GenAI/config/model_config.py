import os


class ModelConfig:
    """Central configuration for the local Ollama GenAI test environment."""

    BASE_URL = os.getenv(
        "OLLAMA_BASE_URL",
        "http://localhost:11434"
    )

    MODEL_NAME = os.getenv(
        "OLLAMA_MODEL",
        "qwen3.5:4b"
    )

    GENERATE_ENDPOINT = f"{BASE_URL}/api/generate"

    TIMEOUT_SECONDS = int(
        os.getenv("OLLAMA_TIMEOUT_SECONDS", "180")
    )

    TEMPERATURE = 0

    CONTEXT_LENGTH = 4096

    @classmethod
    def display(cls):
        """Display active model configuration."""

        return {
            "base_url": cls.BASE_URL,
            "model": cls.MODEL_NAME,
            "endpoint": cls.GENERATE_ENDPOINT,
            "timeout": cls.TIMEOUT_SECONDS,
            "temperature": cls.TEMPERATURE,
            "context_length": cls.CONTEXT_LENGTH,
        }