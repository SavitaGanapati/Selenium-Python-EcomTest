import pytest

from GenAI.client.ollama_client import (
    OllamaClient,
    OllamaClientError
)


@pytest.fixture
def ollama_client():
    return OllamaClient()


def test_ollama_service_health(ollama_client):
    assert ollama_client.health_check() is True


def test_model_returns_valid_response(ollama_client):

    result = ollama_client.generate(
        "Return exactly: GENAI_TEST_SUCCESS"
    )

    assert result["model"] == "qwen3.5:4b"
    assert result["done"] is True
    assert result["response"].strip() == "GENAI_TEST_SUCCESS"


def test_model_returns_generation_metadata(ollama_client):

    result = ollama_client.generate(
        "Return exactly: METADATA_TEST_SUCCESS"
    )

    assert "total_duration" in result
    assert result["total_duration"] > 0
    assert "eval_count" in result


def test_empty_prompt_is_rejected(ollama_client):

    with pytest.raises(ValueError):
        ollama_client.generate("")