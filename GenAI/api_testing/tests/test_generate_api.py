import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from jsonschema import Draft202012Validator, FormatChecker


# ---------------------------------------------------------
# 1. PROJECT PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]

REQUEST_FILE = (
    PROJECT_ROOT
    / "GenAI"
    / "api_testing"
    / "requests"
    / "valid_generation.json"
)

SCHEMA_FILE = (
    PROJECT_ROOT
    / "GenAI"
    / "api_testing"
    / "schemas"
    / "generate_response.schema.json"
)

EVIDENCE_ROOT = (
    PROJECT_ROOT
    / "GenAI"
    / "reports"
    / "api_evidence"
)

REQUEST_EVIDENCE_DIR = EVIDENCE_ROOT / "request"
RESPONSE_EVIDENCE_DIR = EVIDENCE_ROOT / "response"


# ---------------------------------------------------------
# 2. API CONFIGURATION
# ---------------------------------------------------------

BASE_URL = "http://localhost:11434"
ENDPOINT = f"{BASE_URL}/api/generate"

HTTP_TIMEOUT_SECONDS = 180


# ---------------------------------------------------------
# 3. HELPER: SAVE JSON EVIDENCE
# ---------------------------------------------------------

def save_json_evidence(directory, filename, data):
    """Save JSON test evidence to the specified directory."""

    directory.mkdir(parents=True, exist_ok=True)

    file_path = directory / filename

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    return file_path


# ---------------------------------------------------------
# 4. API TEST: VALID GENERATION REQUEST
# ---------------------------------------------------------

def test_generate_api_valid_request():

    # Step 4.1: Load request JSON
    with REQUEST_FILE.open("r", encoding="utf-8") as file:
        request_payload = json.load(file)

    # Step 4.2: Load response JSON Schema
    with SCHEMA_FILE.open("r", encoding="utf-8") as file:
        response_schema = json.load(file)

    # Step 4.3: Create unique execution identifier
    execution_id = datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%S%fZ"
    )

    # Step 4.4: Build HTTP request
    request_body = json.dumps(request_payload).encode("utf-8")

    http_request = Request(
        url=ENDPOINT,
        data=request_body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        method="POST"
    )

    # Step 4.5: Capture request evidence
    request_evidence = {
        "test_id": "GEN-API-001",
        "execution_id": execution_id,
        "method": "POST",
        "endpoint": ENDPOINT,
        "headers": {
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        "body": request_payload
    }

    request_evidence_path = save_json_evidence(
        REQUEST_EVIDENCE_DIR,
        f"{execution_id}_GEN-API-001_request.json",
        request_evidence
    )

    # Step 4.6: Execute HTTP request and capture response
    try:
        with urlopen(
            http_request,
            timeout=HTTP_TIMEOUT_SECONDS
        ) as http_response:

            status_code = http_response.status
            response_headers = dict(http_response.headers.items())
            raw_response = http_response.read().decode("utf-8")

    except HTTPError as error:
        error_body = error.read().decode("utf-8", errors="replace")

        raise AssertionError(
            f"API returned HTTP {error.code}: {error_body}"
        ) from error

    except URLError as error:
        raise AssertionError(
            f"Could not connect to Ollama API: {error.reason}"
        ) from error

    # Step 4.7: Validate HTTP status code
    assert status_code == 200, (
        f"Expected HTTP 200, received HTTP {status_code}"
    )

    # Step 4.8: Validate response Content-Type
    content_type = response_headers.get("Content-Type", "")

    assert "application/json" in content_type.lower(), (
        f"Expected application/json, received {content_type}"
    )

    # Step 4.9: Parse response JSON
    try:
        response_data = json.loads(raw_response)

    except json.JSONDecodeError as error:
        raise AssertionError(
            "API returned an invalid JSON response"
        ) from error

    # Step 4.10: Validate response against JSON Schema
    validator = Draft202012Validator(
        response_schema,
        format_checker=FormatChecker()
    )

    schema_errors = sorted(
        validator.iter_errors(response_data),
        key=lambda error: list(error.absolute_path)
    )

    assert not schema_errors, (
        "Response JSON Schema validation failed:\n"
        + "\n".join(error.message for error in schema_errors)
    )

    # Step 4.11: Validate expected functional behavior
    assert response_data["model"] == request_payload["model"], (
        "Returned model does not match requested model"
    )

    assert response_data["done"] is True, (
        "Model generation did not complete"
    )

    assert (
        response_data["response"].strip()
        == "GENAI_API_CONTRACT_SUCCESS"
    ), "Model returned unexpected response content"

    # Step 4.12: Capture response evidence
    response_evidence = {
        "test_id": "GEN-API-001",
        "execution_id": execution_id,
        "http_status_code": status_code,
        "response_headers": response_headers,
        "response_body": response_data,
        "validations": {
            "http_status": "PASSED",
            "content_type": "PASSED",
            "json_parsing": "PASSED",
            "json_schema": "PASSED",
            "model_name": "PASSED",
            "generation_completed": "PASSED",
            "expected_response": "PASSED"
        }
    }

    response_evidence_path = save_json_evidence(
        RESPONSE_EVIDENCE_DIR,
        f"{execution_id}_GEN-API-001_response.json",
        response_evidence
    )

    # Step 4.13: Display execution evidence locations
    print(f"\nRequest evidence: {request_evidence_path}")
    print(f"Response evidence: {response_evidence_path}")
    print(f"HTTP status code: {status_code}")
    print("JSON Schema validation: PASSED")
    print("Functional validation: PASSED")