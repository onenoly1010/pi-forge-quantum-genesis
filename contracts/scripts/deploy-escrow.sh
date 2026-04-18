#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# EPI v1.6 – Deterministic Escrow Deployment
# ============================================================
# Requirements:
#   - .env file with: PRIVATE_KEY, RPC_URL (optional)
#   - forge installed (via EPI container)
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MANIFEST="$REPO_ROOT/EPI_v1.1_regenerated.json"

# Load environment (secrets not baked into image)
if [[ -f "$REPO_ROOT/.env" ]]; then
    set -a; source "$REPO_ROOT/.env"; set +a
fi

# Required variables
: "${PRIVATE_KEY:?Set PRIVATE_KEY in .env or environment}"
RPC_URL="${RPC_URL:-https://evmrpc.0g.ai}"

# Deployment settings
CONTRACT_PATH="src/OINIO_Sovereign_Escrow.sol"
CONTRACT_NAME="OINIOSovereignEscrow"
CREATE2_SALT="${CREATE2_SALT:-$(git rev-parse --short HEAD)}"  # deterministic address per commit

echo "🔐 Deploying $CONTRACT_NAME from commit $(git rev-parse HEAD)"

# Build with forced optimization (deterministic)
forge build --force --optimize --optimizer-runs 200

# Deploy using CREATE2 (optional, but gives deterministic address)
if forge create --help | grep -q "create2"; then
    DEPLOY_OUTPUT=$(forge create --rpc-url "$RPC_URL" \
        --private-key "$PRIVATE_KEY" \
        --create2 --salt "$CREATE2_SALT" \
        "$CONTRACT_PATH:$CONTRACT_NAME" 2>&1)
else
    # fallback to normal CREATE
    DEPLOY_OUTPUT=$(forge create --rpc-url "$RPC_URL" \
        --private-key "$PRIVATE_KEY" \
        "$CONTRACT_PATH:$CONTRACT_NAME" 2>&1)
fi

# Extract contract address
CONTRACT_ADDRESS=$(echo "$DEPLOY_OUTPUT" | grep -oP 'Deployed to: \K(0x[a-fA-F0-9]{40})' || echo "")
if [[ -z "$CONTRACT_ADDRESS" ]]; then
    echo "❌ Deployment failed. Output:"
    echo "$DEPLOY_OUTPUT"
    exit 1
fi

TX_HASH=$(echo "$DEPLOY_OUTPUT" | grep -oP 'Transaction hash: \K(0x[a-fA-F0-9]{64})' || echo "unknown")

echo "✅ Deployed at: $CONTRACT_ADDRESS"
echo "🔗 Tx: $TX_HASH"

# Append deployment evidence to manifest (if manifest exists)
if [[ -f "$MANIFEST" ]]; then
    # Create a temporary file with new entry
    jq --arg addr "$CONTRACT_ADDRESS" \
       --arg tx "$TX_HASH" \
       --arg commit "$(git rev-parse HEAD)" \
       '. + [{
           "system_component": "OINIO Sovereign Escrow",
           "reference_type": "deployment",
           "exact_location": "commit: '"$(git rev-parse HEAD)"' (contract: '"$CONTRACT_ADDRESS"')",
           "evidence_type": "on-chain",
           "verifiability_note": "Deployed via EPI hermetic container. Tx hash: '"$TX_HASH"'",
           "file_hash": null
       }]' "$MANIFEST" > "$MANIFEST.tmp"
    mv "$MANIFEST.tmp" "$MANIFEST"
    echo "📝 Updated manifest with deployment evidence."
fi

# Output final SHA-256 of manifest
if [[ -f "$MANIFEST" ]]; then
    HASH=$(sha256sum "$MANIFEST" | awk '{print $1}')
    echo "🔒 Manifest SHA-256 after deployment: $HASH"
fi

echo "🎉 Deployment script finished."