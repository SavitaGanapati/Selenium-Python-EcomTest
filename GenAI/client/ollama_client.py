import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from GenAI.config.model_config import ModelConfig


class OllamaClientError(Exception):
    """Raised when communication with Ollama fails."""


class OllamaClient:
    """Client for communicating with a locally hosted Ollama model."""

    def __init__(self):
        self.base_url = ModelConfig.BASE_URL
        self.model = ModelConfig.MODEL_NAME
        self.timeout = ModelConfig.TIMEOUT_SECONDS

    def generate(
        self,
        prompt,
        temperature=None,
        context_length=None
    ):
        """
        Generate a response from the configured local LLM.

        Args:
            prompt: Input prompt for the model.
            temperature: Optional generation temperature.
            context_length: Optional context window size.

        Returns:
            Dictionary containing the model response and timings.
        """

        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt must be a non-empty string.")

        options = {
            "temperature": (
                ModelConfig.TEMPERATURE
                if temperature is None
                else temperature
            ),
            "num_ctx": (
                ModelConfig.CONTEXT_LENGTH
                if context_length is None
                else context_length
            ),
        }

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": options,
        }

        request = Request(
            url=ModelConfig.GENERATE_ENDPOINT,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json"
            },
            method="POST",
        )

        try:
            with urlopen(
                request,
                timeout=self.timeout
            ) as response:

                response_data = json.loads(
                    response.read().decode("utf-8")
                )

        except HTTPError as exc:
            error_body = exc.read().decode(
                "utf-8",
                errors="replace"
            )

            raise OllamaClientError(
                f"Ollama HTTP error {exc.code}: {error_body}"
            ) from exc

        except URLError as exc:
            raise OllamaClientError(
                f"Cannot connect to Ollama: {exc.reason}"
            ) from exc

        except TimeoutError as exc:
            raise OllamaClientError(
                f"Ollama request timed out after {self.timeout} seconds."
            ) from exc

        except json.JSONDecodeError as exc:
            raise OllamaClientError(
                "Ollama returned an invalid JSON response."
            ) from exc

        if response_data.get("done") is not True:
            raise OllamaClientError(
                "Model generation did not complete successfully."
            )

        if "response" not in response_data:
            raise OllamaClientError(
                "Ollama response is missing the response field."
            )

        return response_data

    def health_check(self):
        """Check whether the Ollama service is reachable."""

        request = Request(
            url=f"{self.base_url}/api/tags",
            method="GET",
        )

        try:
            with urlopen(
                request,
                timeout=10
            ) as response:

                return response.status == 200

        except (HTTPError, URLError, TimeoutError):
            return False