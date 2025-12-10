#!/bin/bash
set -e

echo "🔍 Pi Forge Quantum Genesis - Testnet Smoke Tests"
echo "=================================================="

# Configuration
TESTNET_URL="${TESTNET_URL:-http://localhost:8000}"
TIMEOUT=10
MAX_RETRIES=3

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
check_endpoint() {
    local url=$1
    local name=$2
    local retries=0
    
    echo -n "Testing $name... "
    
    while [ $retries -lt $MAX_RETRIES ]; do
        if curl -f -s -m $TIMEOUT "$url" > /dev/null 2>&1; then
            echo -e "${GREEN}✓ PASS${NC}"
            return 0
        fi
        retries=$((retries + 1))
        sleep 2
    done
    
    echo -e "${RED}✗ FAIL${NC}"
    return 1
}

check_json_response() {
    local url=$1
    local name=$2
    local expected_key=$3
    
    echo -n "Testing $name (JSON)... "
    
    response=$(curl -f -s -m $TIMEOUT "$url" 2>/dev/null)
    
    if echo "$response" | grep -q "$expected_key"; then
        echo -e "${GREEN}✓ PASS${NC}"
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        echo "  Expected key: $expected_key"
        echo "  Response: $response"
        return 1
    fi
}

# Track failures
FAILED_TESTS=0

echo ""
echo "Target: $TESTNET_URL"
echo ""

# Test 1: FastAPI Health
if ! check_endpoint "$TESTNET_URL/" "FastAPI Root Health"; then
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

# Test 2: FastAPI JSON Response
if ! check_json_response "$TESTNET_URL/" "FastAPI Health JSON" "status"; then
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

# Test 3: Health Endpoint
if ! check_endpoint "$TESTNET_URL/health" "Health Endpoint"; then
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

# Test 4: Docs Endpoint
if ! check_endpoint "$TESTNET_URL/docs" "API Documentation"; then
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

# Test 5: Environment Check (if available)
echo -n "Testing environment configuration... "
response=$(curl -f -s -m $TIMEOUT "$TESTNET_URL/" 2>/dev/null || echo "{}")
if echo "$response" | grep -q "testnet\|healthy"; then
    echo -e "${GREEN}✓ PASS${NC}"
else
    echo -e "${YELLOW}⚠ WARNING${NC} (unable to verify APP_ENVIRONMENT)"
fi

echo ""
echo "=================================================="

# Summary
if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}✅ All smoke tests passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ $FAILED_TESTS test(s) failed${NC}"
    exit 1
fi
