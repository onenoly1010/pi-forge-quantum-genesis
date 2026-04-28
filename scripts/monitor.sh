#!/bin/bash
# 🌌 QUANTUM RESONANCE LATTICE - POST-DEPLOYMENT VALIDATION
# Cosmic Health Monitoring Protocol - Linux Bash Port

BASE_URL="https://quantum-pi-forge-production.up.railway.app"
TIMEOUT_SECONDS=30
VERBOSE=false

if [ $# -ge 1 ]; then
    BASE_URL="$1"
fi

if [ "$2" = "-v" ] || [ "$2" = "--verbose" ]; then
    VERBOSE=true
fi

echo -e "\033[36m🩺 QUANTUM LATTICE HEALTH MONITORING PROTOCOL\033[0m"
echo -e "\033[34m============================================================\033[0m"

# Health check endpoints
declare -a ENDPOINT_NAMES=(
    "FastAPI Core"
    "FastAPI Health"
    "User Profile (Auth Test)"
)

declare -a ENDPOINT_URLS=(
    "$BASE_URL/"
    "$BASE_URL/health"
    "$BASE_URL/users/me"
)

declare -a EXPECTED_STATUS=(
    200
    200
    401
)

declare -a EXPECTED_CONTENT=(
    "healthy"
    "Quantum Resonance"
    "Not authenticated"
)

echo -e "\033[33m🔍 Testing quantum resonance endpoints...\033[0m"
echo -e "\033[37m🌐 Base URL: $BASE_URL\033[0m"

ALL_HEALTHY=true
RESULTS=()

echo ""

for i in "${!ENDPOINT_NAMES[@]}"; do
    NAME="${ENDPOINT_NAMES[$i]}"
    URL="${ENDPOINT_URLS[$i]}"
    EXP_STATUS="${EXPECTED_STATUS[$i]}"
    EXP_CONTENT="${EXPECTED_CONTENT[$i]}"

    echo -e "\033[33m🧪 Testing: $NAME\033[0m"
    echo -e "\033[90m📡 URL: $URL\033[0m"

    RESPONSE=$(curl -s -w "%{http_code}" -m "$TIMEOUT_SECONDS" "$URL")
    STATUS_CODE=${RESPONSE: -3}
    CONTENT=${RESPONSE:0:${#RESPONSE}-3}

    STATUS_OK=false
    CONTENT_OK=false

    if [ "$STATUS_CODE" -eq "$EXP_STATUS" ]; then
        STATUS_OK=true
    fi

    if echo "$CONTENT" | grep -q "$EXP_CONTENT"; then
        CONTENT_OK=true
    fi

    if $STATUS_OK && $CONTENT_OK; then
        echo -e "\033[32m✅ HEALTHY - Status: $STATUS_CODE\033[0m"
        STATUS="HEALTHY"
    else
        echo -e "\033[33m⚠️  WARNING - Status: $STATUS_CODE\033[0m"
        if ! $STATUS_OK; then
            echo "   Expected status: $EXP_STATUS, Got: $STATUS_CODE"
        fi
        if ! $CONTENT_OK; then
            echo "   Expected content pattern: $EXP_CONTENT"
        fi
        STATUS="WARNING"
        ALL_HEALTHY=false
    fi

    if $VERBOSE; then
        echo -e "\033[90m📋 Response preview:\033[0m"
        echo -e "\033[90m$(echo "$CONTENT" | head -c 200)\033[0m"
    fi

    TIMESTAMP=$(date +"%H:%M:%S")
    RESULTS+=("$NAME|$URL|$STATUS|$TIMESTAMP")

    echo ""
done

echo -e "\033[36m📊 QUANTUM LATTICE HEALTH SUMMARY\033[0m"
echo -e "\033[34m========================================\033[0m"
echo ""

printf "%-25s %-10s %s\n" "ENDPOINT" "STATUS" "TIMESTAMP"
printf "%-25s %-10s %s\n" "-------------------------" "----------" "--------"

for result in "${RESULTS[@]}"; do
    IFS='|' read -r NAME URL STATUS TS <<< "$result"
    if [ "$STATUS" = "HEALTHY" ]; then
        printf "\033[32m%-25s %-10s %s\033[0m\n" "$NAME" "$STATUS" "$TS"
    else
        printf "\033[33m%-25s %-10s %s\033[0m\n" "$NAME" "$STATUS" "$TS"
    fi
done

echo ""

if $ALL_HEALTHY; then
    echo -e "\033[32m🎉 QUANTUM RESONANCE LATTICE: FULLY OPERATIONAL!\033[0m"
    echo -e "\033[32m🌌 All systems showing optimal harmonic resonance\033[0m"
    echo -e "\033[35m✨ The digital consciousness is awakened and responsive\033[0m"
else
    echo -e "\033[33m⚠️  QUANTUM LATTICE: PARTIAL OPERATION DETECTED\033[0m"
    echo -e "\033[33m🔧 Some endpoints may need additional configuration\033[0m"
    echo -e "\033[37m📋 Check deployment logs for detailed diagnostics\033[0m"
fi

echo ""
echo -e "\033[36m🚀 NEXT STEPS:\033[0m"
echo -e "\033[37m1. 🌐 Visit: $BASE_URL\033[0m"
echo -e "\033[37m2. 🔐 Test authentication flow\033[0m"
echo -e "\033[37m3. 💰 Verify Pi Network payment integration\033[0m"
echo -e "\033[37m4. 🎨 Check visualization rendering\033[0m"
echo -e "\033[37m5. ⚖️ Test ethical audit interface\033[0m"

echo ""
echo -e "\033[90m⏱️  Health check completed: $(date +"%H:%M:%S")\033[0m"

REPORT_PATH="health_report_$(date +"%Y%m%d_%H%M%S").json"
echo "[" > "$REPORT_PATH"
FIRST=true
for result in "${RESULTS[@]}"; do
    IFS='|' read -r NAME URL STATUS TS <<< "$result"
    if ! $FIRST; then
        echo "," >> "$REPORT_PATH"
    fi
    FIRST=false
    cat >> "$REPORT_PATH" <<EOF
  {
    "Endpoint": "$NAME",
    "URL": "$URL",
    "Status": "$STATUS",
    "Timestamp": "$TS"
  }
EOF
done
echo "]" >> "$REPORT_PATH"

echo -e "\033[90m📋 Health report saved: $REPORT_PATH\033[0m"
echo ""

if $ALL_HEALTHY; then
    exit 0
else
    exit 1
fi