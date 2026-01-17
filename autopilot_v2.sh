#!/bin/bash
# Quantum Pi Forge — Autopilot v2
# Full redeploy, health checks, validation updater

set -e

echo "?? AUTOPILOT v2 — FULL REDEPLOY SEQUENCE"

# 1 — Input Pi validation key
read -p "?? Enter Pi validation key: " KEY

mkdir -p public
echo "$KEY" > public/validation-key.txt

# 2 — Commit push
git add public/validation-key.txt
git commit -m "Auto v2: update validation key"
git push origin main

# 3 — Netlify deploy
echo "?? Deploying to Netlify..."
netlify deploy --prod --dir=public

sleep 8

# 4 — Health check
URL="https://quantumpiforgeee4091.pinet.com/validation-key.txt"
echo "?? Checking validation file at:"
echo "$URL"

STATUS=$(curl -s -o /dev/null -w "%{http_code}" $URL)

if [ "$STATUS" == "200" ]; then
    echo "? Domain Verification File is LIVE"
else
    echo "? Health Check Failed. Status: $STATUS"
fi

echo "?? AUTOPILOT v2 COMPLETE"
