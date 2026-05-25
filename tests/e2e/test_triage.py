import os

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.response import TriageReport
from tests.fixtures import SAMPLE_PAYLOAD


@pytest.fixture(scope="module")
def require_api_key() -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        pytest.fail("ANTHROPIC_API_KEY must be set for e2e tests (real Anthropic call required)")
    return api_key


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_triage_malformed_request_returns_422(client: TestClient) -> None:
    response = client.post("/triage", json={"order_id": "ord-1"})
    assert response.status_code == 422


@pytest.mark.timeout(30)
def test_triage_end_to_end_with_real_anthropic(client: TestClient, require_api_key: str) -> None:
    response = client.post("/triage", json=SAMPLE_PAYLOAD)

    assert response.status_code == 200
    report = TriageReport.model_validate(response.json())
    assert report.order_id == SAMPLE_PAYLOAD["order_id"]
    assert report.confidence in {"high", "medium", "low"}
    assert report.likely_root_cause
    assert report.reasoning_trace
    assert len(report.recommended_actions) >= 1
    for action in report.recommended_actions:
        assert action.priority >= 1
        assert action.action
        assert action.rationale
    assert isinstance(report.missing_signals, list)
