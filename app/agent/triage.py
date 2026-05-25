from app.agent.client import TriageAgent
from app.models.request import OrderTriageRequest
from app.models.response import TriageReport


def run_triage(request: OrderTriageRequest, agent: TriageAgent | None = None) -> TriageReport:
    triage_agent = agent or TriageAgent()
    return triage_agent.triage(request)
