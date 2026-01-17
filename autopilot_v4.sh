#!/bin/bash
# AUTOPILOT v4 — Self-Healing System

set -e

echo "?? AUTOPILOT v4 — SELF HEALING ONLINE"

URL="https://quantumpiforgeee4091.pinet.com/validation-key.txt"

health_check() {
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" $URL)
    echo $STATUS
}

repair() {
    echo "?? Running Auto-Repair..."
    git pull origin main
    netlify deploy --prod --dir=public
    echo "Repair attempt complete."
}

STATUS=$(health_check)

if [ "$STATUS" == "200" ]; then
    echo "?? Health OK — System Stable"
else
    echo "?? Health FAIL ($STATUS)"
    repair

    STATUS2=$(health_check)

    if [ "$STATUS2" == "200" ]; then
        echo "?? System Recovered Successfully"
    else
        echo "?? FATAL: Manual Intervention Needed"
    fi
fi

echo "?? AUTOPILOT v4 COMPLETE"
