import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# ---------------------------------------------------------
# 1. PROJECT CONFIGURATION
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]

REQUEST_FILE = (
    PROJECT_ROOT
    / "GenAI"
    / "api_testing"
    / "requests"
    / "valid_generation.json"
)

EVIDENCE_ROOT = (
    PROJECT_ROOT
    / "GenAI"
    / "reports"
    / "api_evidence"
)

REQUEST_EVIDENCE_DIR = EVIDENCE_ROOT / "request"
RESPONSE_EVIDENCE_DIR = EVIDENCE_ROOT / "response"

ENDPOINT = "http://localhost:11434/api/generate"
TIMEOUT_SECONDS = 180


# ---------------------------------------------------------
# 2. EVIDENCE UTILITY
# ---------------------------------------------------------

def save_evidence(directory, filename, data):
    directory.mkdir(parents=True, exist_ok=True)

    file_path = directory / filename

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    return file_path


# ---------------------------------------------------------
# 3. LOAD BASELINE REQUEST
# ---------------------------------------------------------

with REQUEST_FILE.open("r", encoding="utf-8") as file:
    valid_payload = json.load(file)


# ---------------------------------------------------------
# 4. DEFINE NEGATIVE TEST SCENARIOS
# ---------------------------------------------------------

invalid_model_payload = valid_payload.copy()
invalid_model_payload["model"] = "model-that-does-not-exist"

missing_model_payload = valid_payload.copy()
missing_model_payload.pop("model")

missing_prompt_payload = valid_payload.copy()
missing_prompt_payload.pop("prompt")

negative_scenarios = [
    {
        "test_id": "GEN-API-002",
        "scenario": "Invalid model name",
        "body": invalid_model_payload,
        "content_type": "application/json",
    },
    {
        "test_id": "GEN-API-003",
        "scenario": "Missing model field",
        "body": missing_model_payload,
        "content_type": "application/json",
    },
    {
        "test_id": "GEN-API-004",
        "scenario": "Missing prompt field",
        "body": missing_prompt_payload,
        "content_type": "application/json",
    },
    {
        "test_id": "GEN-API-005",
        "scenario": "Malformed JSON",
        "body": '{"model": "qwen3.5:4b", "prompt": ',
        "content_type": "application/json",
    },
    {
        "test_id": "GEN-API-006",
        "scenario": "Incorrect Content-Type",
        "body": valid_payload,
        "content_type": "text/plain",
    },
]


# ---------------------------------------------------------
# 5. EXECUTE AND CAPTURE EACH SCENARIO
# ---------------------------------------------------------

for scenario in negative_scenarios:

    test_id = scenario["test_id"]
    execution_id = datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%S%fZ"
    )

    body = scenario["body"]

    if isinstance(body, str):
        request_body = body.encode("utf-8")
        body_evidence = {"raw": body}
    else:
        request_body = json.dumps(body).encode("utf-8")
        body_evidence = body

    headers = {
        "Content-Type": scenario["content_type"],
        "Accept": "application/json",
    }

    request_evidence = {
        "test_id": test_id,
        "scenario": scenario["scenario"],
        "execution_id": execution_id,
        "method": "POST",
        "endpoint": ENDPOINT,
        "headers": headers,
        "body": body_evidence,
    }

    request_path = save_evidence(
        REQUEST_EVIDENCE_DIR,
        f"{execution_id}_{test_id}_request.json",
        request_evidence,
    )

    http_request = Request(
        url=ENDPOINT,
        data=request_body,
        headers=headers,
        method="POST",
    )

    status_code = None
    response_headers = {}
    raw_response = ""
    transport_error = None

    try:
        with urlopen(
            http_request,
            timeout=TIMEOUT_SECONDS,
        ) as response:
            status_code = response.status
            response_headers = dict(response.headers.items())
            raw_response = response.read().decode(
                "utf-8",
                errors="replace",
            )

    except HTTPError as error:
        status_code = error.code
        response_headers = dict(error.headers.items())
        raw_response = error.read().decode(
            "utf-8",
            errors="replace",
        )

    except (URLError, TimeoutError, OSError) as error:
        transport_error = str(error)

    try:
        parsed_response = json.loads(raw_response) if raw_response else None
    except json.JSONDecodeError:
        parsed_response = None

    response_evidence = {
        "test_id": test_id,
        "scenario": scenario["scenario"],
        "execution_id": execution_id,
        "http_status_code": status_code,
        "response_headers": response_headers,
        "response_body_raw": raw_response,
        "response_body_json": parsed_response,
        "transport_error": transport_error,
    }

    response_path = save_evidence(
        RESPONSE_EVIDENCE_DIR,
        f"{execution_id}_{test_id}_response.json",
        response_evidence,
    )

    print("\n" + "=" * 65)
    print(f"TEST ID       : {test_id}")
    print(f"SCENARIO      : {scenario['scenario']}")
    print(f"HTTP STATUS   : {status_code}")
    print(f"TRANSPORT ERR : {transport_error}")
    print(f"REQUEST FILE  : {request_path}")
    print(f"RESPONSE FILE : {response_path}")

    if raw_response:
        print(f"RESPONSE BODY : {raw_response[:500]}")