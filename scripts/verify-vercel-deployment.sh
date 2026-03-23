#!/bin/bash

# Vercel Deployment Verification Script
# Usage: ./scripts/verify-vercel-deployment.sh <deployment-url>

set -e

DEPLOYMENT_URL="${1:-https://your-project.vercel.app}"
FAILED_CHECKS=0
TOTAL_CHECKS=0

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
check_passed() {
  echo -e "${GREEN}✅ $1${NC}"
  TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
}

check_failed() {
  echo -e "${RED}❌ $1${NC}"
  FAILED_CHECKS=$((FAILED_CHECKS + 1))
  TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
}

check_warning() {
  echo -e "${YELLOW}⚠️  $1${NC}"
  TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
}

# Start verification
echo "======================================"
echo "Vercel Deployment Verification"
echo "======================================"
echo "URL: $DEPLOYMENT_URL"
echo "Time: $(date)"
echo "======================================"
echo ""

# Check 1: Homepage accessibility
echo "🔍 Checking homepage..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$DEPLOYMENT_URL" 2>/dev/null || echo "000")
if [ "$HTTP_STATUS" == "200" ]; then
  check_passed "Homepage accessible (HTTP $HTTP_STATUS)"
else
  check_failed "Homepage failed (HTTP $HTTP_STATUS)"
fi

# Check 2: Mobile viewport configuration
echo "🔍 Checking mobile viewport..."
VIEWPORT_CHECK=$(curl -s "$DEPLOYMENT_URL" 2>/dev/null | grep -c 'viewport.*width=device-width' || echo "0")
if [ "$VIEWPORT_CHECK" -gt 0 ]; then
  check_passed "Mobile viewport configured"
else
  check_warning "Mobile viewport meta tag missing"
fi

# Check 3: Static JavaScript assets
echo "🔍 Checking JavaScript assets..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${DEPLOYMENT_URL}/pi-forge-integration.js" 2>/dev/null || echo "000")
if [ "$HTTP_STATUS" == "200" ]; then
  check_passed "JavaScript assets loading (HTTP $HTTP_STATUS)"
else
  check_warning "JavaScript assets returned HTTP $HTTP_STATUS"
fi

# Check 4: Frontend directory
echo "🔍 Checking frontend pages..."
PAGES=(
  "ceremonial_interface.html"
  "resonance_dashboard.html"
  "spectral_command_shell.html"
)

for page in "${PAGES[@]}"; do
  HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${DEPLOYMENT_URL}/${page}" 2>/dev/null || echo "000")
  if [ "$HTTP_STATUS" == "200" ]; then
    check_passed "$page accessible (HTTP $HTTP_STATUS)"
  else
    check_failed "$page failed (HTTP $HTTP_STATUS)"
  fi
done

# Check 5: Frontend subdirectory
echo "🔍 Checking frontend subdirectory..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${DEPLOYMENT_URL}/frontend/index.html" 2>/dev/null || echo "000")
if [ "$HTTP_STATUS" == "200" ]; then
  check_passed "Frontend subdirectory accessible (HTTP $HTTP_STATUS)"
else
  check_warning "Frontend subdirectory returned HTTP $HTTP_STATUS"
fi

# Check 6: API endpoint (may return 405 for GET, which is expected)
echo "🔍 Checking API endpoint..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${DEPLOYMENT_URL}/api/pi-identify" 2>/dev/null || echo "000")
if [ "$HTTP_STATUS" == "405" ] || [ "$HTTP_STATUS" == "200" ]; then
  check_passed "API endpoint responding (HTTP $HTTP_STATUS, expected 405 for GET)"
else
  check_warning "API endpoint returned HTTP $HTTP_STATUS"
fi

# Check 7: Security headers
echo "🔍 Checking security headers..."
HEADERS=$(curl -s -I "$DEPLOYMENT_URL" 2>/dev/null)

if echo "$HEADERS" | grep -qi "X-Frame-Options"; then
  check_passed "X-Frame-Options header present"
else
  check_warning "X-Frame-Options header missing"
fi

if echo "$HEADERS" | grep -qi "X-Content-Type-Options"; then
  check_passed "X-Content-Type-Options header present"
else
  check_warning "X-Content-Type-Options header missing"
fi

# Check 8: HTTPS enforcement
echo "🔍 Checking HTTPS..."
if [[ "$DEPLOYMENT_URL" == https://* ]]; then
  check_passed "HTTPS enabled"
else
  check_warning "HTTPS not detected in URL"
fi

# Check 9: Response time
echo "🔍 Checking response time..."
RESPONSE_TIME=$(curl -s -o /dev/null -w "%{time_total}" "$DEPLOYMENT_URL" 2>/dev/null || echo "99")
RESPONSE_TIME_MS=$(echo "$RESPONSE_TIME * 1000" | bc | cut -d. -f1)

if [ "$RESPONSE_TIME_MS" -lt 1000 ]; then
  check_passed "Response time: ${RESPONSE_TIME_MS}ms (excellent)"
elif [ "$RESPONSE_TIME_MS" -lt 2000 ]; then
  check_passed "Response time: ${RESPONSE_TIME_MS}ms (good)"
else
  check_warning "Response time: ${RESPONSE_TIME_MS}ms (slow)"
fi

# Check 10: Content size
echo "🔍 Checking content size..."
CONTENT_SIZE=$(curl -s -w "%{size_download}" -o /dev/null "$DEPLOYMENT_URL" 2>/dev/null || echo "0")
CONTENT_SIZE_KB=$(echo "$CONTENT_SIZE / 1024" | bc)

if [ "$CONTENT_SIZE_KB" -gt 0 ]; then
  check_passed "Content size: ${CONTENT_SIZE_KB}KB"
else
  check_warning "Content size could not be determined"
fi

# Check 11: Compression
echo "🔍 Checking compression..."
ENCODING=$(curl -s -I "$DEPLOYMENT_URL" 2>/dev/null | grep -i "content-encoding" | cut -d: -f2 | tr -d ' \r\n')
if [ -n "$ENCODING" ]; then
  check_passed "Compression enabled: $ENCODING"
else
  check_warning "Compression not detected"
fi

# Summary
echo ""
echo "======================================"
echo "Verification Summary"
echo "======================================"
echo "Total checks: $TOTAL_CHECKS"
echo "Passed: $((TOTAL_CHECKS - FAILED_CHECKS))"
echo "Failed: $FAILED_CHECKS"
echo "======================================"

if [ $FAILED_CHECKS -eq 0 ]; then
  echo -e "${GREEN}✅ All critical checks passed!${NC}"
  echo "Deployment verified successfully."
  exit 0
else
  echo -e "${RED}❌ $FAILED_CHECKS check(s) failed${NC}"
  echo "Please review the failures above."
  exit 1
fi
