# FlockSRE

AI-powered delivery operations triage agent for Flock. Ingests operational signals for a distressed order and returns a structured triage report via Claude.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your-key-here
uvicorn app.main:app --reload
```

## Example

```bash
curl -s -X POST http://localhost:8000/triage \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": "ord-8821",
    "city": "Tel Aviv",
    "signals": [
      {
        "source": "order_tracker",
        "message": "Order stuck in '\''restaurant_accepted'\'' state for 23 minutes. Expected max: 5 minutes."
      },
      {
        "source": "driver_dispatch",
        "message": "3 consecutive driver assignment attempts failed. Last failure reason: no_drivers_nearby."
      },
      {
        "source": "restaurant_health",
        "message": "Pasta Palace (id: rest-441) has had 7 orders cancelled in the last 15 minutes. Average prep time today: 34 min vs. 12 min baseline."
      },
      {
        "source": "customer_support",
        "message": "Customer contacted support: '\''Where is my food? It'\''s been 40 minutes.'\''"
      }
    ]
  }'
```

## Assumptions

- `ANTHROPIC_API_KEY` is provided via environment
- Model: `claude-sonnet-4-6`
- Structured output via Anthropic tool use (`submit_triage`), validated with Pydantic
- E2E tests require live Anthropic access

## Test

```bash
pytest tests/unit/          # mocked Anthropic — fast
pytest tests/e2e/           # real Anthropic API — requires ANTHROPIC_API_KEY
```

## One thing I'd do differently with more time

Add an async job queue (e.g. Redis/SQS) so triage runs out-of-band for high-volume incidents, with idempotency keys per `order_id`, circuit breaking on Anthropic latency spikes, and OpenTelemetry traces per triage run.
