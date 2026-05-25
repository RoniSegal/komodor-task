# TP-2: Input Validation & Triage Route

**Status:** pending  
**Phase:** 1  
**Depends on:** TP-1

## Goal

Define Pydantic request/response models and wire `POST /triage` with input validation.

## Acceptance Criteria

- [ ] `OrderTriageRequest` and `Signal` models with min-length validation
- [ ] `TriageReport`, `RecommendedAction` response models
- [ ] `POST /triage` returns 422 on malformed input with field errors
- [ ] Reject empty `signals` array
- [ ] Unit tests for validation (valid payload, missing fields, empty signals)

## Completion Evidence

(pending)
