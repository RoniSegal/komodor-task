import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.request import OrderTriageRequest
from tests.fixtures import SAMPLE_PAYLOAD


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_triage_valid_request_shape() -> None:
    request = OrderTriageRequest.model_validate(SAMPLE_PAYLOAD)
    assert request.order_id == "ord-8821"
    assert len(request.signals) == 4


def test_triage_missing_order_id(client: TestClient) -> None:
    payload = {**SAMPLE_PAYLOAD}
    del payload["order_id"]
    response = client.post("/triage", json=payload)
    assert response.status_code == 422


def test_triage_empty_signals(client: TestClient) -> None:
    payload = {**SAMPLE_PAYLOAD, "signals": []}
    response = client.post("/triage", json=payload)
    assert response.status_code == 422


def test_triage_empty_signal_source(client: TestClient) -> None:
    payload = {
        **SAMPLE_PAYLOAD,
        "signals": [{"source": "", "message": "something happened"}],
    }
    response = client.post("/triage", json=payload)
    assert response.status_code == 422
