# FlockSRE — Agent Context

## Project

FlockSRE is a lightweight AI triage agent for Flock food delivery ops. It exposes `POST /triage` to analyze operational signals for a distressed order and return a structured triage report via Claude (Anthropic).

## Stack

- Python 3.11+
- FastAPI + Uvicorn
- Pydantic v2 (request/response schemas + Anthropic tool JSON Schema)
- Anthropic SDK (`claude-sonnet-4-6`)
- pytest + httpx TestClient

## Architecture

```
POST /triage → Pydantic validation → TriageAgent → Anthropic tool_use (submit_triage) → TriageReport JSON
```

## Conventions

- `ANTHROPIC_API_KEY` from environment; never commit secrets
- Structured LLM output via Anthropic tool `submit_triage` (not free-form JSON parsing)
- Unit tests mock Anthropic; e2e tests use real API calls
- Commits: conventional format `feat(TP-N): ...` on `main`

## Layout

```
app/
  main.py
  routes/triage.py
  models/{request,response}.py
  agent/{prompt,client,triage}.py
tests/
  unit/
  e2e/
tickets/TP-*.md
```
