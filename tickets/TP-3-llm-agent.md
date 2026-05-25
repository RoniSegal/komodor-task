# TP-3: LLM Triage Agent

**Status:** done  
**Phase:** 1  
**Depends on:** TP-2

## Goal

Integrate Anthropic Claude with tool-use structured output and wire the full triage flow.

## Acceptance Criteria

- [x] System and user prompts in `app/agent/prompt.py`
- [x] Signal formatting: `[{source}] {message}` per line
- [x] Anthropic client calls `submit_triage` tool with Pydantic-derived JSON Schema
- [x] `tool_choice` forces structured output; Pydantic validates response
- [x] `order_id` overridden from request if model omits it
- [x] Single retry on validation failure; 502 on persistent failure
- [x] Unit tests with mocked Anthropic client

## Completion Evidence

- `tests/unit/test_agent.py` — 3 tests passing
- `tests/unit/test_prompt.py` — 4 tests passing
- `tests/unit/test_route.py` — 2 tests passing
- `app/agent/client.py`, `app/agent/triage.py`
