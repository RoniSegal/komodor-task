# TP-2: Input Validation & Triage Route

**Status:** done  
**Phase:** 1  
**Depends on:** TP-1

## Goal

Define Pydantic request/response models and wire `POST /triage` with input validation.

## Acceptance Criteria

- [x] `OrderTriageRequest` and `Signal` models with min-length validation
- [x] `TriageReport`, `RecommendedAction` response models
- [x] `POST /triage` returns 422 on malformed input with field errors
- [x] Reject empty `signals` array
- [x] Unit tests for validation (valid payload, missing fields, empty signals)

## Completion Evidence

- `tests/unit/test_validation.py` — 4 tests passing
- `app/models/request.py`, `app/models/response.py`, `app/routes/triage.py`
