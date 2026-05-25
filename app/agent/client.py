import os
from typing import Any

from anthropic import Anthropic
from pydantic import ValidationError

from app.agent.prompt import build_system_prompt, build_user_prompt
from app.models.request import OrderTriageRequest
from app.models.response import TriageReport

MODEL = "claude-sonnet-4-6"
TOOL_NAME = "submit_triage"


def _tool_schema() -> dict[str, Any]:
    schema = TriageReport.model_json_schema()
    schema.pop("title", None)
    return schema


def _extract_tool_input(response: Any) -> dict[str, Any]:
    for block in response.content:
        if block.type == "tool_use" and block.name == TOOL_NAME:
            return block.input
    raise ValueError("Anthropic response did not include submit_triage tool output")


class TriageAgent:
    def __init__(self, client: Anthropic | None = None) -> None:
        self._client = client or Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    def triage(self, request: OrderTriageRequest) -> TriageReport:
        messages = [{"role": "user", "content": build_user_prompt(request)}]
        system = build_system_prompt(request)
        tools = [
            {
                "name": TOOL_NAME,
                "description": "Submit the structured triage report for the distressed order.",
                "input_schema": _tool_schema(),
            }
        ]

        last_error: str | None = None
        for attempt in range(2):
            response = self._client.messages.create(
                model=MODEL,
                max_tokens=1024,
                system=system,
                messages=messages,
                tools=tools,
                tool_choice={"type": "tool", "name": TOOL_NAME},
            )

            try:
                payload = _extract_tool_input(response)
                payload["order_id"] = request.order_id
                return TriageReport.model_validate(payload)
            except (ValidationError, ValueError) as exc:
                last_error = str(exc)
                messages.append({"role": "assistant", "content": response.content})
                messages.append(
                    {
                        "role": "user",
                        "content": (
                            "Your tool output was invalid. "
                            f"Error: {last_error}. "
                            "Call submit_triage again with a valid payload."
                        ),
                    }
                )

        raise RuntimeError(last_error or "Failed to produce a valid triage report")
