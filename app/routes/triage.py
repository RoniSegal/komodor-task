from fastapi import APIRouter, HTTPException

from app.agent.triage import run_triage
from app.models.request import OrderTriageRequest
from app.models.response import TriageReport

router = APIRouter()


@router.post("/triage", response_model=TriageReport)
def triage_order(request: OrderTriageRequest) -> TriageReport:
    try:
        return run_triage(request)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
