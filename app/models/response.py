from typing import Literal

from pydantic import BaseModel, Field


class RecommendedAction(BaseModel):
    priority: int = Field(ge=1)
    action: str
    rationale: str


class TriageReport(BaseModel):
    order_id: str
    likely_root_cause: str
    confidence: Literal["high", "medium", "low"]
    recommended_actions: list[RecommendedAction]
    missing_signals: list[str]
    reasoning_trace: str
