from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from app.agent.client import TriageAgent
from app.models.request import OrderTriageRequest
from tests.fixtures import SAMPLE_PAYLOAD


def _tool_block(payload: dict) -> SimpleNamespace:
    return SimpleNamespace(type="tool_use", name="submit_triage", input=payload)


def _text_block(text: str) -> SimpleNamespace:
    return SimpleNamespace(type="text", text=text)


def _response(*blocks: SimpleNamespace) -> SimpleNamespace:
    return SimpleNamespace(content=list(blocks))


VALID_REPORT = {
    "order_id": "ignored",
    "likely_root_cause": "Restaurant overload causing prep delays",
    "confidence": "high",
    "recommended_actions": [
        {
            "priority": 1,
            "action": "Contact restaurant ops",
            "rationale": "High cancellation rate indicates kitchen distress",
        }
    ],
    "missing_signals": ["live_kitchen_capacity"],
    "reasoning_trace": "Restaurant health signals dominate.",
}


def test_triage_agent_parses_tool_output() -> None:
    client = MagicMock()
    client.messages.create.return_value = _response(_tool_block(VALID_REPORT))

    request = OrderTriageRequest.model_validate(SAMPLE_PAYLOAD)
    report = TriageAgent(client=client).triage(request)

    assert report.order_id == "ord-8821"
    assert report.confidence == "high"
    assert len(report.recommended_actions) == 1
    client.messages.create.assert_called_once()


def test_triage_agent_retries_on_invalid_tool_output() -> None:
    client = MagicMock()
    client.messages.create.side_effect = [
        _response(_tool_block({"confidence": "high"})),
        _response(_tool_block(VALID_REPORT)),
    ]

    request = OrderTriageRequest.model_validate(SAMPLE_PAYLOAD)
    report = TriageAgent(client=client).triage(request)

    assert report.order_id == "ord-8821"
    assert client.messages.create.call_count == 2


def test_triage_agent_raises_after_retry_exhausted() -> None:
    client = MagicMock()
    client.messages.create.return_value = _response(_text_block("no tool here"))

    request = OrderTriageRequest.model_validate(SAMPLE_PAYLOAD)
    with pytest.raises(RuntimeError, match="submit_triage"):
        TriageAgent(client=client).triage(request)

    assert client.messages.create.call_count == 2
