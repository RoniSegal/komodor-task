from app.agent.prompt import (
    PAYMENT_GATEWAY_PROMPT,
    SYSTEM_PROMPT,
    build_system_prompt,
    build_user_prompt,
    format_signals,
)
from app.models.request import OrderTriageRequest, Signal
from tests.fixtures import SAMPLE_PAYLOAD


def test_format_signals() -> None:
    request = OrderTriageRequest.model_validate(SAMPLE_PAYLOAD)
    formatted = format_signals(request)
    assert "[order_tracker]" in formatted
    assert "[driver_dispatch]" in formatted
    assert formatted.count("\n") == len(request.signals) - 1


def test_build_user_prompt_includes_order_and_city() -> None:
    request = OrderTriageRequest.model_validate(SAMPLE_PAYLOAD)
    prompt = build_user_prompt(request)
    assert "ord-8821" in prompt
    assert "Tel Aviv" in prompt
    assert "Produce your triage report." in prompt


def test_build_system_prompt_without_payment() -> None:
    request = OrderTriageRequest.model_validate(SAMPLE_PAYLOAD)
    assert build_system_prompt(request) == SYSTEM_PROMPT


def test_build_system_prompt_with_payment_gateway() -> None:
    request = OrderTriageRequest(
        order_id="ord-1",
        city="NYC",
        signals=[
            Signal(source="payment_gateway", message="Authorization pending for 12 minutes."),
        ],
    )
    prompt = build_system_prompt(request)
    assert PAYMENT_GATEWAY_PROMPT.strip() in prompt
