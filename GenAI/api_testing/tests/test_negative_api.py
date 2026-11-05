import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

import pytest

from GenAI.config.model_config import ModelConfig


# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

API_URL = ModelConfig.GENERATE_ENDPOINT
MODEL_NAME = ModelConfig.MODEL_NAME

EVIDENCE_DIR = (
    Path(__file__).resolve().parents[2]
    / "reports"
    / "api_evidence"
)

REQUEST_DIR = EVIDENCE_DIR / "request"
RESPONSE_DIR = EVIDENCE_DIR / "response"

REQUEST_DIR.mkdir(parents=True, exist_ok=True)
RESPONSE_DIR.mkdir(parents=True, exist_ok=True)

TIMEOUT = ModelConfig.TIMEOUT_SECONDS


# ---------------------------------------------------------
# COMMON TEST DATA
# ---------------------------------------------------------

def load_valid_payload():
    """Load the approved valid API request."""
    request_file = (
        Path(__file__).resolve().parents[1]
        / "requests"
        / "valid_generation.json"
    )

    with open(request_file, "r", encoding="utf-8") as file:
        return json.load(file)


# ---------------------------------------------------------
# API EXECUTION AND EVIDENCE CAPTURE
# ---------------------------------------------------------

def execute_api_request(
    test_id,
    scenario,
    payload=None,
    content_type="application/json",
    raw_body=None,
):
    """Execute an API request and preserve request/response evidence."""

    execution_id = datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%S%fZ"
    )

    if raw_body is not None:
        request_body = raw_body
    else:
        request_body = json.dumps(payload).encode("utf-8")

    request_evidence = {
        "test_id": test_id,
        "scenario": scenario,
        "execution_id": execution_id,
        "url": API_URL,
        "method": "POST",
        "content_type": content_type,
        "request_body": request_body.decode(
            "utf-8", errors="replace"
        ),
    }

    request_file = REQUEST_DIR / (
        f"{execution_id}_{test_id}_request.json"
    )

    response_file = RESPONSE_DIR / (
        f"{execution_id}_{test_id}_response.json"
    )

    with open(request_file, "w", encoding="utf-8") as file:
        json.dump(request_evidence, file, indent=4)

    request = Request(
        url=API_URL,
        data=request_body,
        headers={"Content-Type": content_type},
        method="POST",
    )

    status_code = None
    response_headers = {}
    response_body_raw = ""
    response_body_json = None
    transport_error = None

    try:
        with urlopen(request, timeout=TIMEOUT) as response:
            status_code = response.status
            response_headers = dict(response.headers.items())
            response_body_raw = response.read().decode(
                "utf-8", errors="replace"
            )

    except HTTPError as exc:
        status_code = exc.code
        response_headers = dict(exc.headers.items())
        response_body_raw = exc.read().decode(
            "utf-8", errors="replace"
        )

    except (URLError, TimeoutError, OSError) as exc:
        transport_error = str(exc)

    try:
        if response_body_raw:
            response_body_json = json.loads(response_body_raw)
    except json.JSONDecodeError:
        response_body_json = None

    evidence = {
        "test_id": test_id,
        "scenario": scenario,
        "execution_id": execution_id,
        "http_status_code": status_code,
        "response_headers": response_headers,
        "response_body_raw": response_body_raw,
        "response_body_json": response_body_json,
        "transport_error": transport_error,
        "assertions": [],
        "test_result": "NOT_VALIDATED",
    }

    with open(response_file, "w", encoding="utf-8") as file:
        json.dump(evidence, file, indent=4)

    evidence["request_evidence_file"] = str(request_file)
    evidence["response_evidence_file"] = str(response_file)

    return evidence


# ---------------------------------------------------------
# ASSERTIONS AND FINAL EVIDENCE STATUS
# ---------------------------------------------------------

def validate_test_result(evidence, checks):
    """Save assertion outcomes before reporting pytest failures."""

    for description, condition in checks:
        evidence["assertions"].append({
            "description": description,
            "result": "PASSED" if condition else "FAILED",
        })

    evidence["test_result"] = (
        "PASSED"
        if all(condition for _, condition in checks)
        else "FAILED"
    )

    response_file = Path(evidence["response_evidence_file"])

    # Remove internal file-path references from response evidence.
    saved_evidence = {
        key: value
        for key, value in evidence.items()
        if key not in (
            "request_evidence_file",
            "response_evidence_file",
        )
    }

    with open(response_file, "w", encoding="utf-8") as file:
        json.dump(saved_evidence, file, indent=4)

    for description, condition in checks:
        assert condition, (
            f"{evidence['test_id']} FAILED: {description}. "
            f"Evidence: {response_file}"
        )


# ---------------------------------------------------------
# GEN-API-002: INVALID MODEL
# ---------------------------------------------------------

def test_invalid_model_returns_404():

    payload = load_valid_payload()
    payload["model"] = "model-that-does-not-exist"

    evidence = execute_api_request(
        test_id="GEN-API-002",
        scenario="Invalid model name",
        payload=payload,
    )

    body = evidence["response_body_json"] or {}
    error_message = body.get("error", "")

    validate_test_result(evidence, [
        ("HTTP status is 404", evidence["http_status_code"] == 404),
        (
            "Error message identifies missing model",
            "not found" in error_message.lower(),
        ),
        ("No transport error", evidence["transport_error"] is None),
    ])


# ---------------------------------------------------------
# GEN-API-003: MISSING MODEL
# ---------------------------------------------------------

def test_missing_model_returns_404():

    payload = load_valid_payload()
    payload.pop("model")

    evidence = execute_api_request(
        test_id="GEN-API-003",
        scenario="Missing model field",
        payload=payload,
    )

    body = evidence["response_body_json"] or {}
    error_message = body.get("error", "")

    validate_test_result(evidence, [
        ("HTTP status is 404", evidence["http_status_code"] == 404),
        (
            "Error identifies empty model name",
            "model '' not found" in error_message.lower(),
        ),
        ("No transport error", evidence["transport_error"] is None),
    ])


# ---------------------------------------------------------
# GEN-API-004: MISSING PROMPT
# ---------------------------------------------------------

def test_missing_prompt_returns_empty_response():

    payload = load_valid_payload()
    payload.pop("prompt")

    evidence = execute_api_request(
        test_id="GEN-API-004",
        scenario="Missing prompt field",
        payload=payload,
    )

    body = evidence["response_body_json"] or {}

    validate_test_result(evidence, [
        ("HTTP status is 200", evidence["http_status_code"] == 200),
        ("Response is valid JSON", isinstance(body, dict)),
        ("Generation marked complete", body.get("done") is True),
        ("Response is empty", body.get("response") == ""),
        (
            "Done reason is load",
            body.get("done_reason") == "load",
        ),
        ("No transport error", evidence["transport_error"] is None),
    ])


# ---------------------------------------------------------
# GEN-API-005: MALFORMED JSON
# ---------------------------------------------------------

def test_malformed_json_returns_400():

    evidence = execute_api_request(
        test_id="GEN-API-005",
        scenario="Malformed JSON",
        raw_body=b'{"model":',
    )

    body = evidence["response_body_json"] or {}
    error_message = body.get("error", "")

    validate_test_result(evidence, [
        ("HTTP status is 400", evidence["http_status_code"] == 400),
        (
            "Error identifies malformed JSON",
            "unexpected eof" in error_message.lower(),
        ),
        ("No transport error", evidence["transport_error"] is None),
    ])


# ---------------------------------------------------------
# GEN-API-006: INCORRECT CONTENT-TYPE
# ---------------------------------------------------------

def test_incorrect_content_type_is_accepted():

    payload = load_valid_payload()

    evidence = execute_api_request(
        test_id="GEN-API-006",
        scenario="Incorrect Content-Type",
        payload=payload,
        content_type="text/plain",
    )

    body = evidence["response_body_json"] or {}

    validate_test_result(evidence, [
        ("HTTP status is 200", evidence["http_status_code"] == 200),
        ("Response is valid JSON", isinstance(body, dict)),
        (
            "Correct model returned",
            body.get("model") == MODEL_NAME,
        ),
        ("Generation completed", body.get("done") is True),
        (
            "Expected generated text returned",
            body.get("response", "").strip()
            == "GENAI_API_CONTRACT_SUCCESS",
        ),
        ("No transport error", evidence["transport_error"] is None),
    ])