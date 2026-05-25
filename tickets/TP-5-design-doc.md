# TP-5: Scaling Design Doc (Bonus)

**Status:** done  
**Phase:** 2  
**Depends on:** TP-3

## Goal

Document how to scale FlockSRE to 500 concurrent distressed orders with p99 LLM latency of 8s.

## Acceptance Criteria

- [x] `DESIGN.md` covers async workers, queue, idempotency, circuit breaker, observability

## Completion Evidence

- `DESIGN.md` — queue architecture, worker sizing (~80 workers), idempotency, circuit breaker, observability
