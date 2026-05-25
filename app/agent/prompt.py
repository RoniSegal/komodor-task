from app.models.request import OrderTriageRequest

SYSTEM_PROMPT = """You are FlockSRE, an on-call triage agent for Flock food delivery.

Analyze the operational signals for one distressed order. From the evidence only:
- State the most likely root cause of the order being stuck
- Recommend prioritized actions for the on-call engineer (each with rationale)
- List signals that are missing but would confirm or rule out your diagnosis

If evidence is weak or conflicting, use lower confidence and say what would resolve ambiguity.
Be concise and actionable. Do not invent facts beyond the provided signals."""

PAYMENT_GATEWAY_PROMPT = """
When a signal source is "payment_gateway", treat payment failure or authorization delay as a distinct root-cause class. Prioritize payment verification and customer refund/retry flows before dispatch or restaurant actions."""


def build_system_prompt(request: OrderTriageRequest) -> str:
    prompt = SYSTEM_PROMPT
    if any(signal.source == "payment_gateway" for signal in request.signals):
        prompt += PAYMENT_GATEWAY_PROMPT
    return prompt


def format_signals(request: OrderTriageRequest) -> str:
    return "\n".join(f"[{signal.source}] {signal.message}" for signal in request.signals)


def build_user_prompt(request: OrderTriageRequest) -> str:
    return (
        f"Order: {request.order_id} | City: {request.city}\n\n"
        f"Signals:\n{format_signals(request)}\n\n"
        "Produce your triage report."
    )
