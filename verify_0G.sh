#!/usr/bin/env bash
set -euo pipefail

TARGET_URL=${1:-"http://localhost:3001"}

echo "0G Reviewer Verification"
echo "Target: $TARGET_URL"

curl -fsS "$TARGET_URL/health" | grep -q '"status":"healthy"'
echo "[PASS] health endpoint"

curl -fsS "$TARGET_URL/api/templates" | grep -q '"success":true'
echo "[PASS] templates endpoint"

curl -fsS "$TARGET_URL/api/templates" | grep -q 'architecture-deep-dive'
echo "[PASS] architecture template present"

echo "[PASS] Local architecture verified"
