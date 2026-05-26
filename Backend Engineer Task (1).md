# Backend Engineer Home Task
## AI-Powered Delivery Operations Triage Agent

**Time estimate:** 30–40 minutes  
**Tools allowed:** Anything — Claude Code, Cursor, Copilot, agents, whatever you prefer. We care about the result, not how you got there.

---

## Background

You're a backend engineer at **Flock**, a food delivery platform operating in multiple cities. Flock has an internal ops tool used by on-call engineers when something goes wrong — orders stalling, drivers disappearing, restaurants going dark.

Your job: build the core of **FlockSRE**, a lightweight AI agent that ingests operational signals from a troubled order and produces a structured triage report — so an on-call engineer can act fast.

This is a simplified but realistic slice of production tooling. Design it like it's going to production.

---

## The Task

Build a small HTTP service (Go or Python) with **one endpoint**:

```
POST /triage
```

### Input

A distressed order and its associated operational signals:

```json
{
  "order_id": "ord-8821",
  "city": "Tel Aviv",
  "signals": [
    {
      "source": "order_tracker",
      "message": "Order stuck in 'restaurant_accepted' state for 23 minutes. Expected max: 5 minutes."
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
      "message": "Customer contacted support: 'Where is my food? It's been 40 minutes.'"
    }
  ]
}
```

### What the service must do

1. **Aggregate** the incoming signals into a coherent operational context
2. **Call an LLM** (use Claude via the Anthropic API, or any model you prefer) with a well-crafted prompt to:
   - Identify the most likely root cause of the order being stuck
   - Produce a prioritized list of actions the on-call engineer should take
   - Flag any missing signals that would help confirm the diagnosis
3. **Return** a structured JSON response:

```json
{
  "order_id": "ord-8821",
  "likely_root_cause": "...",
  "confidence": "high | medium | low",
  "recommended_actions": [
    { "priority": 1, "action": "...", "rationale": "..." }
  ],
  "missing_signals": ["..."],
  "reasoning_trace": "..."
}
```

---

## Requirements

### Functional
- The endpoint must work end-to-end with a real LLM call
- The LLM response must be reliably parsed into the output schema
- Include basic input validation — reject malformed requests with a meaningful error

### Bonus (optional, ~10 extra minutes)
Choose **one** if you have time:

- **Multi-signal reasoning:** Add support for a `"source": "payment_gateway"` signal type. When present, the agent should adjust its reasoning — payment issues have a different resolution path than dispatch or restaurant issues. Show this in your prompt design.
- **DESIGN.md:** How would you scale this to triage 500 concurrent distressed orders? What changes if the LLM has a p99 latency of 8 seconds?


---

## Submission

- A Git repo (GitHub/GitLab) or a zip
- A `README.md` with: how to run it, any assumptions made, and one thing you'd do differently with more time

---

> **No single correct solution.** We're more interested in *how* you think about the problem than whether your JSON schema is pixel-perfect. The debrief conversation matters as much as the code.
