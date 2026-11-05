# GenAI API Test Evidence

## Purpose
This directory stores request and response evidence generated during GenAI API testing.

## Directory Structure
- request/: Captured API requests.
- response/: Captured API responses.

## Evidence Naming Convention
`<UTC_TIMESTAMP>_<TEST_ID>_<REQUEST_OR_RESPONSE>.json`

Example:
`20261105T035701530301Z_GEN-API-001_request.json`

## Test Coverage

| Test ID | Scenario |
|---|---|
| GEN-API-001 | Valid generation request |
| GEN-API-002 | Invalid model |
| GEN-API-003 | Missing model |
| GEN-API-004 | Missing prompt |
| GEN-API-005 | Malformed JSON |
| GEN-API-006 | Incorrect Content-Type |

## Evidence Management
- Preserve request and response pairs.
- Use UTC timestamps to identify executions.
- Retain failed-test evidence for investigation.
- Do not store credentials, secrets or sensitive production data.
- Associate evidence with its test ID.
- Do not treat a passing characterization test as proof that the observed API behaviour is ideal.
