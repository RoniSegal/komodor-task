# TP-4: Payment Gateway Signal (Bonus)

**Status:** done  
**Phase:** 2  
**Depends on:** TP-3

## Goal

Extend prompt to handle `payment_gateway` signals with distinct resolution paths.

## Acceptance Criteria

- [x] System prompt includes payment-specific guidance when `payment_gateway` source present
- [x] Unit test fixture with payment signal; actions mention payment-related steps

## Completion Evidence

- `PAYMENT_GATEWAY_PROMPT` appended in `build_system_prompt()` when source detected
- `tests/unit/test_prompt.py::test_build_system_prompt_with_payment_gateway`
