from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.response import RecommendedAction, TriageReport
from tests.fixtures import SAMPLE_PAYLOAD


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_triage_route_returns_report(client: TestClient) -> None:
    mock_report = TriageReport(
        order_id="ord-8821",
        likely_root_cause="Restaurant overload",
        confidence="high",
        recommended_actions=[
            RecommendedAction(
                priority=1,
                action="Contact restaurant",
                rationale="High cancellation rate",
            )
        ],
        missing_signals=["kitchen_capacity"],
        reasoning_trace="Restaurant signals dominate.",
    )

    with patch("app.routes.triage.run_triage", return_value=mock_report):
        response = client.post("/triage", json=SAMPLE_PAYLOAD)

    assert response.status_code == 200
    assert response.json()["order_id"] == "ord-8821"


def test_triage_route_returns_502_on_agent_failure(client: TestClient) -> None:
    with patch("app.routes.triage.run_triage", side_effect=RuntimeError("LLM failed")):
        response = client.post("/triage", json=SAMPLE_PAYLOAD)

    assert response.status_code == 502
    assert response.json()["detail"] == "LLM failed"
