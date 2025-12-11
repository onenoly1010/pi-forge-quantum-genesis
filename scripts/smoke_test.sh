#!/usr/bin/env bash
# Lightweight smoke tests for deployed services (used by CI)
set -euo pipefail

BASE_URL_GUARDIAN=${GUARDIAN_API_URL:-http://localhost:8001}
BASE_URL_FASTAPI=${FASTAPI_URL:-http://localhost:8000}
BASE_URL_FLASK=${FLASK_URL:-http://localhost:5000}
BASE_URL_GRADIO=${GRADIO_URL:-http://localhost:7860}

echo "Checking guardian-api /health..."
curl --fail -s ${BASE_URL_GUARDIAN}/health | jq .

echo "Checking fastapi-server root..."
curl --fail -s ${BASE_URL_FASTAPI}/ | head -n 20

echo "Checking flask-dashboard root..."
curl --fail -s ${BASE_URL_FLASK}/ | head -n 20

echo "Checking gradio-interface root..."
curl --fail -s ${BASE_URL_GRADIO}/ | head -n 20

echo "Smoke tests passed."
