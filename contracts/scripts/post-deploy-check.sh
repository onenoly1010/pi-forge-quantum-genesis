#!/bin/bash

# =============================================================================
# POST-DEPLOYMENT HEALTH CHECK SCRIPT
# =============================================================================
# Verifies deployed contracts, tests basic functionality, and outputs status
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[!]${NC} $1"; }
log_error() { echo -e "${RED}[✗]${NC} $1"; }
log_contract() { echo -e "${CYAN}[CONTRACT]${NC} $1"; }

NETWORK="mainnet"
FAILED_CHECKS=0

while [[ $# -gt 0 ]]; do
    case $1 in
        --network)
            NETWORK="$2"
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   POST-DEPLOYMENT HEALTH CHECK                            ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
log_info "Network: $NETWORK"
echo ""

# Load environment
if [ -f ".env" ]; then
    source .env
fi

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

# Check if contract has code deployed
check_contract_deployed() {
    local ADDRESS=$1
    local NAME=$2
    local RPC_URL=$3
    
    if [ -z "$ADDRESS" ] || [ "$ADDRESS" = "0x0000000000000000000000000000000000000000" ]; then
        log_warning "$NAME: Not deployed (address not set)"
        return 1
    fi
    
    log_info "Checking $NAME at $ADDRESS..."
    
    # Get contract code
    CODE=$(curl -s -X POST "$RPC_URL" \
        -H "Content-Type: application/json" \
        -d "{\"jsonrpc\":\"2.0\",\"method\":\"eth_getCode\",\"params\":[\"$ADDRESS\",\"latest\"],\"id\":1}" \
        --max-time 10 | grep -o '"result":"[^"]*"' | cut -d'"' -f4)
    
    if [ "$CODE" = "0x" ] || [ -z "$CODE" ]; then
        log_error "$NAME: No code at address (not deployed or wrong address)"
        ((FAILED_CHECKS++))
        return 1
    else
        CODE_SIZE=$((${#CODE} / 2 - 1))
        log_success "$NAME: Deployed (code size: $CODE_SIZE bytes)"
        return 0
    fi
}

# Call contract view function
call_contract_function() {
    local ADDRESS=$1
    local SIGNATURE=$2
    local NAME=$3
    local RPC_URL=$4
    
    # Encode function signature
    SELECTOR=$(echo -n "$SIGNATURE" | xxd -p | head -c 8)
    
    # Call contract
    RESULT=$(curl -s -X POST "$RPC_URL" \
        -H "Content-Type: application/json" \
        -d "{\"jsonrpc\":\"2.0\",\"method\":\"eth_call\",\"params\":[{\"to\":\"$ADDRESS\",\"data\":\"0x$SELECTOR\"},\"latest\"],\"id\":1}" \
        --max-time 10 | grep -o '"result":"[^"]*"' | cut -d'"' -f4)
    
    if [ -n "$RESULT" ] && [ "$RESULT" != "0x" ]; then
        log_success "$NAME: Function callable"
        return 0
    else
        log_warning "$NAME: Function call failed or returned empty"
        return 1
    fi
}

# =============================================================================
# CHECK DEPLOYED CONTRACTS
# =============================================================================

log_info "═══════════════════════════════════════════════════════════"
log_info "CHECKING DEPLOYED CONTRACTS"
log_info "═══════════════════════════════════════════════════════════"
echo ""

# Determine RPC URLs based on network
if [ "$NETWORK" = "mainnet" ]; then
    PI_RPC="${PI_MAINNET_RPC:-https://rpc.mainnet.pi.network}"
    ZERO_G_RPC="${ZERO_G_RPC:-https://evmrpc.0g.ai}"
else
    PI_RPC="${PI_TESTNET_RPC:-https://api.testnet.minepi.com/rpc}"
    ZERO_G_RPC="${ZERO_G_TESTNET_RPC:-https://evmrpc-testnet.0g.ai}"
fi

# =============================================================================
# CHECK OINIO TOKEN (Pi Network & 0G)
# =============================================================================

log_info "─────────────────────────────────────────────────────────────"
log_info "OINIO Token Contract"
log_info "─────────────────────────────────────────────────────────────"
echo ""

if [ -n "$OINIO_TOKEN_ADDRESS" ]; then
    # Try Pi Network first
    if check_contract_deployed "$OINIO_TOKEN_ADDRESS" "OINIO Token" "$PI_RPC"; then
        log_contract "Address: $OINIO_TOKEN_ADDRESS"
        log_contract "Network: Pi Network $NETWORK"
        
        # Try to call view functions using cast if available
        if command -v cast &> /dev/null; then
            NAME=$(cast call "$OINIO_TOKEN_ADDRESS" "name()(string)" --rpc-url "$PI_RPC" 2>/dev/null || echo "")
            SYMBOL=$(cast call "$OINIO_TOKEN_ADDRESS" "symbol()(string)" --rpc-url "$PI_RPC" 2>/dev/null || echo "")
            DECIMALS=$(cast call "$OINIO_TOKEN_ADDRESS" "decimals()(uint8)" --rpc-url "$PI_RPC" 2>/dev/null || echo "")
            TOTAL_SUPPLY=$(cast call "$OINIO_TOKEN_ADDRESS" "totalSupply()(uint256)" --rpc-url "$PI_RPC" 2>/dev/null || echo "")
            
            if [ -n "$NAME" ]; then
                log_contract "Name: $NAME"
            fi
            if [ -n "$SYMBOL" ]; then
                log_contract "Symbol: $SYMBOL"
            fi
            if [ -n "$DECIMALS" ]; then
                log_contract "Decimals: $DECIMALS"
            fi
            if [ -n "$TOTAL_SUPPLY" ]; then
                # Convert from wei to ether
                SUPPLY_ETHER=$(echo "scale=2; $TOTAL_SUPPLY / 1000000000000000000" | bc)
                log_contract "Total Supply: $SUPPLY_ETHER OINIO"
            fi
        fi
        
        log_success "OINIO Token: HEALTHY ✨"
    else
        # Try 0G as fallback
        check_contract_deployed "$OINIO_TOKEN_ADDRESS" "OINIO Token" "$ZERO_G_RPC" || true
    fi
else
    log_warning "OINIO_TOKEN_ADDRESS not set in .env"
fi

echo ""

# =============================================================================
# CHECK OINIO MODEL REGISTRY
# =============================================================================

log_info "─────────────────────────────────────────────────────────────"
log_info "OINIO Model Registry Contract"
log_info "─────────────────────────────────────────────────────────────"
echo ""

if [ -n "$OINIO_REGISTRY_ADDRESS" ]; then
    if check_contract_deployed "$OINIO_REGISTRY_ADDRESS" "OINIO Registry" "$PI_RPC"; then
        log_contract "Address: $OINIO_REGISTRY_ADDRESS"
        log_contract "Network: Pi Network $NETWORK"
        
        if command -v cast &> /dev/null; then
            NAME=$(cast call "$OINIO_REGISTRY_ADDRESS" "name()(string)" --rpc-url "$PI_RPC" 2>/dev/null || echo "")
            SYMBOL=$(cast call "$OINIO_REGISTRY_ADDRESS" "symbol()(string)" --rpc-url "$PI_RPC" 2>/dev/null || echo "")
            
            if [ -n "$NAME" ]; then
                log_contract "Name: $NAME"
            fi
            if [ -n "$SYMBOL" ]; then
                log_contract "Symbol: $SYMBOL"
            fi
        fi
        
        log_success "OINIO Registry: HEALTHY ✨"
    else
        check_contract_deployed "$OINIO_REGISTRY_ADDRESS" "OINIO Registry" "$ZERO_G_RPC" || true
    fi
else
    log_warning "OINIO_REGISTRY_ADDRESS not set in .env"
fi

echo ""

# =============================================================================
# CHECK DEX CONTRACTS (0G Network)
# =============================================================================

log_info "─────────────────────────────────────────────────────────────"
log_info "DEX Contracts (0G Network)"
log_info "─────────────────────────────────────────────────────────────"
echo ""

# Check W0G
if [ -n "$W0G_ADDRESS" ]; then
    if check_contract_deployed "$W0G_ADDRESS" "W0G (Wrapped 0G)" "$ZERO_G_RPC"; then
        log_contract "Address: $W0G_ADDRESS"
        log_contract "Network: 0G Aristotle Mainnet"
        
        if command -v cast &> /dev/null; then
            NAME=$(cast call "$W0G_ADDRESS" "name()(string)" --rpc-url "$ZERO_G_RPC" 2>/dev/null || echo "")
            SYMBOL=$(cast call "$W0G_ADDRESS" "symbol()(string)" --rpc-url "$ZERO_G_RPC" 2>/dev/null || echo "")
            
            if [ -n "$NAME" ]; then
                log_contract "Name: $NAME"
            fi
            if [ -n "$SYMBOL" ]; then
                log_contract "Symbol: $SYMBOL"
            fi
        fi
        
        log_success "W0G: HEALTHY ✨"
    fi
else
    log_warning "W0G_ADDRESS not set"
fi

echo ""

# Check Factory
if [ -n "$FACTORY_ADDRESS" ]; then
    if check_contract_deployed "$FACTORY_ADDRESS" "UniswapV2Factory" "$ZERO_G_RPC"; then
        log_contract "Address: $FACTORY_ADDRESS"
        log_contract "Network: 0G Aristotle Mainnet"
        
        if command -v cast &> /dev/null; then
            FEE_TO=$(cast call "$FACTORY_ADDRESS" "feeTo()(address)" --rpc-url "$ZERO_G_RPC" 2>/dev/null || echo "")
            
            if [ -n "$FEE_TO" ]; then
                log_contract "Fee Recipient: $FEE_TO"
            fi
        fi
        
        log_success "UniswapV2Factory: HEALTHY ✨"
    fi
else
    log_warning "FACTORY_ADDRESS not set"
fi

echo ""

# Check Router
if [ -n "$ROUTER_ADDRESS" ]; then
    if check_contract_deployed "$ROUTER_ADDRESS" "UniswapV2Router02" "$ZERO_G_RPC"; then
        log_contract "Address: $ROUTER_ADDRESS"
        log_contract "Network: 0G Aristotle Mainnet"
        
        if command -v cast &> /dev/null; then
            FACTORY=$(cast call "$ROUTER_ADDRESS" "factory()(address)" --rpc-url "$ZERO_G_RPC" 2>/dev/null || echo "")
            WETH=$(cast call "$ROUTER_ADDRESS" "WETH()(address)" --rpc-url "$ZERO_G_RPC" 2>/dev/null || echo "")
            
            if [ -n "$FACTORY" ]; then
                log_contract "Factory: $FACTORY"
            fi
            if [ -n "$WETH" ]; then
                log_contract "WETH: $WETH"
            fi
        fi
        
        log_success "UniswapV2Router02: HEALTHY ✨"
    fi
else
    log_warning "ROUTER_ADDRESS not set"
fi

echo ""

# =============================================================================
# CHECK SOROBAN CONTRACTS (Pi Network)
# =============================================================================

log_info "─────────────────────────────────────────────────────────────"
log_info "Soroban Contracts (Pi Network)"
log_info "─────────────────────────────────────────────────────────────"
echo ""

if [ -n "$MEMORIAL_CONTRACT_ID" ]; then
    log_contract "Memorial Bridge Contract ID: $MEMORIAL_CONTRACT_ID"
    
    if command -v soroban &> /dev/null; then
        log_info "Verifying Soroban contract..."
        
        # Try to inspect the contract
        if soroban contract inspect --id "$MEMORIAL_CONTRACT_ID" --network pi-mainnet &> /dev/null; then
            log_success "Memorial Bridge: DEPLOYED ✨"
        else
            log_warning "Could not verify Memorial Bridge contract"
        fi
    else
        log_warning "Soroban CLI not available, skipping verification"
    fi
else
    log_warning "MEMORIAL_CONTRACT_ID not set"
fi

echo ""

# =============================================================================
# CHECK DEPLOYMENT RECORDS
# =============================================================================

log_info "─────────────────────────────────────────────────────────────"
log_info "Deployment Records"
log_info "─────────────────────────────────────────────────────────────"
echo ""

# Check for Hardhat deployment files
if [ -d "hardhat/deployments" ]; then
    DEPLOYMENT_COUNT=$(find hardhat/deployments -name "*.json" 2>/dev/null | wc -l)
    log_contract "Hardhat deployment records: $DEPLOYMENT_COUNT files"
else
    log_warning "No Hardhat deployment directory found"
fi

# Check for general deployment logs
if [ -d "deployments" ]; then
    LOG_COUNT=$(find deployments -name "*.txt" 2>/dev/null | wc -l)
    log_contract "Deployment logs: $LOG_COUNT files"
else
    log_warning "No deployment logs directory found"
fi

echo ""

# =============================================================================
# INTEGRATION TESTS
# =============================================================================

log_info "═══════════════════════════════════════════════════════════"
log_info "BASIC INTEGRATION TESTS"
log_info "═══════════════════════════════════════════════════════════"
echo ""

if command -v cast &> /dev/null && [ -n "$OINIO_TOKEN_ADDRESS" ]; then
    log_info "Testing OINIO Token transfer simulation..."
    
    # Simulate a transfer (doesn't execute, just tests the interface)
    if cast call "$OINIO_TOKEN_ADDRESS" "balanceOf(address)(uint256)" "0x0000000000000000000000000000000000000000" --rpc-url "$PI_RPC" &> /dev/null; then
        log_success "Token balanceOf function works"
    else
        log_warning "Token balanceOf function test failed"
    fi
fi

echo ""

# =============================================================================
# GENERATE HEALTH REPORT
# =============================================================================

log_info "Generating health report..."

TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
REPORT_FILE="deployments/health_check_${NETWORK}_$(date +%Y%m%d_%H%M%S).txt"

mkdir -p deployments

cat > "$REPORT_FILE" << EOF
DEPLOYMENT HEALTH CHECK REPORT
==============================
Generated: $TIMESTAMP
Network: $NETWORK

Contract Status:
----------------
OINIO Token:         ${OINIO_TOKEN_ADDRESS:-Not deployed}
OINIO Registry:      ${OINIO_REGISTRY_ADDRESS:-Not deployed}
W0G (0G):           ${W0G_ADDRESS:-Not deployed}
Factory (0G):       ${FACTORY_ADDRESS:-Not deployed}
Router (0G):        ${ROUTER_ADDRESS:-Not deployed}
Memorial (Pi):      ${MEMORIAL_CONTRACT_ID:-Not deployed}

Network RPCs:
-------------
Pi Network:  $PI_RPC
0G Network:  $ZERO_G_RPC

Failed Checks: $FAILED_CHECKS

Status: $([ $FAILED_CHECKS -eq 0 ] && echo "HEALTHY ✅" || echo "ISSUES DETECTED ⚠️")

Recommendations:
----------------
1. Review any failed checks above
2. Verify contracts on block explorers
3. Test contract interactions with frontend
4. Monitor gas usage and transaction success rates
5. Set up monitoring alerts for contract events

Block Explorer Links:
--------------------
0G Explorer:  https://scan.0g.ai/
Pi Explorer:  https://pi.blockscout.com/

EOF

log_success "Health report saved to $REPORT_FILE"

echo ""

# =============================================================================
# SUMMARY
# =============================================================================

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   HEALTH CHECK SUMMARY                                    ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

if [ $FAILED_CHECKS -eq 0 ]; then
    log_success "All contracts are healthy! ✨"
    echo ""
    log_info "Next steps:"
    echo "  1. Update frontend with contract addresses"
    echo "  2. Test contract interactions"
    echo "  3. Monitor events and logs"
    echo "  4. Set up alerting for critical functions"
    echo ""
    exit 0
else
    log_warning "Health check completed with $FAILED_CHECKS issues"
    echo ""
    log_info "Please review the issues above and take corrective action"
    echo ""
    exit 1
fi
