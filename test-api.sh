#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8000}"
BASE_URL="${BASE_URL:-http://${HOST}:${PORT}}"

if [[ -f "$ROOT/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$ROOT/.env"
  set +a
fi

echo "Checking ${BASE_URL}/health ..."
health_code="$(curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}/health")"
if [[ "$health_code" != "200" ]]; then
  echo "Error: server not reachable at ${BASE_URL} (health returned ${health_code})." >&2
  echo "Start the API first: ./run.sh" >&2
  exit 1
fi

echo "POST ${BASE_URL}/triage with task example payload ..."
response_file="$(mktemp)"
http_code="$(
  curl -s -S -o "$response_file" -w "%{http_code}" \
    -X POST "${BASE_URL}/triage" \
    -H "Content-Type: application/json" \
    -d @- <<'EOF'
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
EOF
)"

if [[ "$http_code" != "200" ]]; then
  echo "Error: POST /triage returned HTTP ${http_code}" >&2
  cat "$response_file" >&2
  rm -f "$response_file"
  exit 1
fi

echo "Success (HTTP ${http_code})"
if command -v jq >/dev/null 2>&1; then
  jq . "$response_file"
else
  cat "$response_file"
  echo
fi

rm -f "$response_file"
