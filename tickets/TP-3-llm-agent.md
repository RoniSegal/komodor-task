# TP-3: LLM Triage Agent

**Status:** pending  
**Phase:** 1  
**Depends on:** TP-2

## Goal

Integrate Anthropic Claude with tool-use structured output and wire the full triage flow.

## Acceptance Criteria

- [ ] System and user prompts in `app/agent/prompt.py`
- [ ] Signal formatting: `[{source}] {message}` per line
- [ ] Anthropic client calls `submit_triage` tool with Pydantic-derived JSON Schema
- [ ] `tool_choice` forces structured output; Pydantic validates response
- [ ] `order_id` overridden from request if model omits it
- [ ] Single retry on validation failure; 502 on persistent failure
- [ ] Unit tests with mocked Anthropic client

## Completion Evidence

(pending)
