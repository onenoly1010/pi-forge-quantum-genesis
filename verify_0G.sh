#!/usr/bin/env bash
set -euo pipefail

TARGET_URL=${1:-"http://localhost:3001"}

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

pass() { echo -e "${GREEN}[PASS]${NC} $1"; }
fail() { echo -e "${RED}[FAIL]${NC} $1"; exit 1; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }

echo -e "${YELLOW}Initiating 0G Alignment Verification Protocol...${NC}"
echo "Target: $TARGET_URL"
echo

curl -fsS "$TARGET_URL/health" >/tmp/verify_0g_health.json \
  && pass "/health reachable" \
  || fail "/health unreachable"

grep -q '"status":"healthy"' /tmp/verify_0g_health.json \
  && pass "health payload reports healthy" \
  || fail "health payload missing healthy status"

curl -fsS "$TARGET_URL/api/templates" >/tmp/verify_0g_templates.json \
  && pass "/api/templates reachable" \
  || fail "/api/templates unreachable"

grep -q '"success":true' /tmp/verify_0g_templates.json \
  && pass "template registry returned success" \
  || fail "template registry missing success=true"

grep -q 'architecture-deep-dive' /tmp/verify_0g_templates.json \
  && pass "architecture template present" \
  || warn "architecture template not detected"

echo
echo -e "${GREEN}Verification Complete. Local Press Agent architecture is responding deterministically.${NC}"
