# FlockSRE — Claude Context

Same as AGENTS.md. Read AGENTS.md and STATUS.md before starting any ticket work.

## Key decisions

- Python/FastAPI over Go for Pydantic + Anthropic tool schema parity
- Model: `claude-sonnet-4-6`
- E2E tests require live `ANTHROPIC_API_KEY` (no mock fallback)
- Phase 2 (deferred): payment_gateway prompt extension, DESIGN.md scaling notes
