#!/bin/bash

# =============================================================================
# PRE-DEPLOYMENT SAFETY CHECKS
# =============================================================================
# Comprehensive validation of environment, network, and deployment readiness
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[!]${NC} $1"; }
log_error() { echo -e "${RED}[✗]${NC} $1"; }

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
echo "║   PRE-DEPLOYMENT SAFETY CHECKS                            ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
log_info "Network: $NETWORK"
echo ""

# =============================================================================
# CHECK 1: ENVIRONMENT CONFIGURATION
# =============================================================================

log_info "Check 1: Environment Configuration"
echo "─────────────────────────────────────"

# Check .env file exists
if [ ! -f ".env" ]; then
    log_error ".env file not found"
    ((FAILED_CHECKS++))
else
    log_success ".env file exists"
    source .env
fi

# Check PRIVATE_KEY
if [ -z "$PRIVATE_KEY" ]; then
    log_error "PRIVATE_KEY not set in .env"
    ((FAILED_CHECKS++))
else
    # Validate format (should be 66 chars: 0x + 64 hex characters)
    if [[ $PRIVATE_KEY =~ ^0x[0-9a-fA-F]{64}$ ]]; then
        log_success "PRIVATE_KEY is properly formatted"
    else
        log_warning "PRIVATE_KEY format may be incorrect (expected: 0x followed by 64 hex chars = 66 total chars)"
    fi
fi

# Check RPC URLs
if [ "$NETWORK" = "mainnet" ]; then
    if [ -z "$RPC_URL_MAINNET" ] && [ -z "$PI_MAINNET_RPC" ] && [ -z "$ZERO_G_RPC" ]; then
        log_error "No mainnet RPC URLs configured"
        ((FAILED_CHECKS++))
    else
        log_success "Mainnet RPC URLs configured"
    fi
else
    if [ -z "$RPC_URL_TESTNET" ] && [ -z "$PI_TESTNET_RPC" ]; then
        log_error "No testnet RPC URLs configured"
        ((FAILED_CHECKS++))
    else
        log_success "Testnet RPC URLs configured"
    fi
fi

echo ""

# =============================================================================
# CHECK 2: REQUIRED TOOLS
# =============================================================================

log_info "Check 2: Required Tools Installation"
echo "─────────────────────────────────────"

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    log_success "Node.js installed: $NODE_VERSION"
else
    log_error "Node.js not found"
    ((FAILED_CHECKS++))
fi

# Check npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    log_success "npm installed: $NPM_VERSION"
else
    log_error "npm not found"
    ((FAILED_CHECKS++))
fi

# Check Forge (Foundry)
if command -v forge &> /dev/null; then
    FORGE_VERSION=$(forge --version | head -n 1)
    log_success "Forge installed: $FORGE_VERSION"
else
    log_warning "Forge not found (required for DEX deployment)"
fi

# Check Cast (Foundry)
if command -v cast &> /dev/null; then
    log_success "Cast installed"
else
    log_warning "Cast not found (useful for contract interaction)"
fi

# Check Soroban CLI
if command -v soroban &> /dev/null; then
    SOROBAN_VERSION=$(soroban --version)
    log_success "Soroban CLI installed: $SOROBAN_VERSION"
else
    log_warning "Soroban CLI not found (required for Memorial contract)"
fi

echo ""

# =============================================================================
# CHECK 3: NETWORK CONNECTIVITY
# =============================================================================

log_info "Check 3: Network Connectivity"
echo "─────────────────────────────────────"

# Function to test RPC endpoint
test_rpc() {
    local RPC_URL=$1
    local NETWORK_NAME=$2
    
    if [ -z "$RPC_URL" ]; then
        log_warning "$NETWORK_NAME RPC URL not configured"
        return 1
    fi
    
    log_info "Testing $NETWORK_NAME: $RPC_URL"
    
    # Try to get chain ID
    RESPONSE=$(curl -s -X POST "$RPC_URL" \
        -H "Content-Type: application/json" \
        -d '{"jsonrpc":"2.0","method":"eth_chainId","params":[],"id":1}' \
        --max-time 10 || echo "")
    
    if echo "$RESPONSE" | grep -q "result"; then
        CHAIN_ID=$(echo "$RESPONSE" | grep -o '"result":"[^"]*"' | cut -d'"' -f4)
        CHAIN_ID_DEC=$((CHAIN_ID))
        log_success "$NETWORK_NAME connected (Chain ID: $CHAIN_ID_DEC)"
        return 0
    else
        log_error "$NETWORK_NAME connection failed"
        ((FAILED_CHECKS++))
        return 1
    fi
}

# Test configured networks
if [ "$NETWORK" = "mainnet" ]; then
    # Test Pi Network Mainnet
    if [ -n "$PI_MAINNET_RPC" ]; then
        test_rpc "$PI_MAINNET_RPC" "Pi Network Mainnet"
    fi
    
    # Test 0G Network
    if [ -n "$ZERO_G_RPC" ]; then
        test_rpc "$ZERO_G_RPC" "0G Aristotle Mainnet"
    fi
else
    # Test Pi Network Testnet
    if [ -n "$PI_TESTNET_RPC" ]; then
        test_rpc "$PI_TESTNET_RPC" "Pi Network Testnet"
    fi
fi

echo ""

# =============================================================================
# CHECK 4: WALLET BALANCES
# =============================================================================

log_info "Check 4: Wallet Balances"
echo "─────────────────────────────────────"

# Function to check balance
check_balance() {
    local RPC_URL=$1
    local NETWORK_NAME=$2
    local MIN_BALANCE_ETH=$3
    
    if [ -z "$RPC_URL" ] || [ -z "$PRIVATE_KEY" ]; then
        log_warning "Cannot check $NETWORK_NAME balance (missing configuration)"
        return 1
    fi
    
    # Derive address from private key using cast (if available)
    if command -v cast &> /dev/null; then
        DEPLOYER_ADDRESS=$(cast wallet address "$PRIVATE_KEY" 2>/dev/null || echo "")
        
        if [ -n "$DEPLOYER_ADDRESS" ]; then
            log_info "Deployer address: $DEPLOYER_ADDRESS"
            
            # Get balance
            BALANCE_HEX=$(curl -s -X POST "$RPC_URL" \
                -H "Content-Type: application/json" \
                -d "{\"jsonrpc\":\"2.0\",\"method\":\"eth_getBalance\",\"params\":[\"$DEPLOYER_ADDRESS\",\"latest\"],\"id\":1}" \
                --max-time 10 | grep -o '"result":"[^"]*"' | cut -d'"' -f4)
            
            if [ -n "$BALANCE_HEX" ]; then
                # Convert to decimal
                BALANCE_WEI=$(printf "%d" $BALANCE_HEX 2>/dev/null || echo "0")
                BALANCE_ETH=$(echo "scale=4; $BALANCE_WEI / 1000000000000000000" | bc)
                
                log_info "$NETWORK_NAME balance: $BALANCE_ETH ETH"
                
                # Check minimum balance
                if (( $(echo "$BALANCE_ETH < $MIN_BALANCE_ETH" | bc -l) )); then
                    log_error "Insufficient balance (minimum: $MIN_BALANCE_ETH ETH)"
                    ((FAILED_CHECKS++))
                    return 1
                else
                    log_success "Balance sufficient (minimum: $MIN_BALANCE_ETH ETH)"
                    return 0
                fi
            else
                log_warning "Could not retrieve balance"
                return 1
            fi
        else
            log_warning "Could not derive address from private key"
            return 1
        fi
    else
        log_warning "Cast not available, skipping balance check"
        return 1
    fi
}

# Check balances for target networks
if [ "$NETWORK" = "mainnet" ]; then
    if [ -n "$PI_MAINNET_RPC" ]; then
        check_balance "$PI_MAINNET_RPC" "Pi Network Mainnet" "0.1"
        echo ""
    fi
    
    if [ -n "$ZERO_G_RPC" ]; then
        check_balance "$ZERO_G_RPC" "0G Aristotle Mainnet" "0.5"
        echo ""
    fi
else
    if [ -n "$PI_TESTNET_RPC" ]; then
        check_balance "$PI_TESTNET_RPC" "Pi Network Testnet" "0.1"
        echo ""
    fi
fi

# =============================================================================
# CHECK 5: CONTRACT COMPILATION
# =============================================================================

log_info "Check 5: Contract Compilation Status"
echo "─────────────────────────────────────"

# Check Hardhat contracts
if [ -d "hardhat" ]; then
    log_info "Checking Hardhat compilation..."
    cd hardhat
    
    if [ -d "artifacts" ]; then
        log_success "Hardhat artifacts exist"
    else
        log_warning "Hardhat contracts not compiled, attempting compilation..."
        npm run compile 2>&1 | grep -q "Compiled" && log_success "Compilation successful" || log_error "Compilation failed"
    fi
    
    cd ..
fi

# Check Forge contracts
if [ -d "src" ]; then
    log_info "Checking Forge compilation..."
    
    if [ -d "out" ]; then
        log_success "Forge artifacts exist"
    else
        log_warning "Forge contracts not compiled, attempting compilation..."
        forge build &> /dev/null && log_success "Compilation successful" || log_error "Compilation failed"
    fi
fi

# Check Soroban contracts
if [ -d "oinio-memorial-bridge" ]; then
    log_info "Checking Soroban contract build..."
    
    if [ -f "oinio-memorial-bridge/target/wasm32-unknown-unknown/release/oinio_memorial_bridge.wasm" ]; then
        log_success "Soroban contract built"
    else
        log_warning "Soroban contract not built (run ./oinio-memorial-bridge/build.sh)"
    fi
fi

echo ""

# =============================================================================
# CHECK 6: GIT STATUS
# =============================================================================

log_info "Check 6: Git Repository Status"
echo "─────────────────────────────────────"

if git rev-parse --git-dir > /dev/null 2>&1; then
    # Check for uncommitted changes
    if [ -n "$(git status --porcelain)" ]; then
        log_warning "Uncommitted changes detected"
        log_info "Consider committing changes before deployment"
    else
        log_success "Working directory is clean"
    fi
    
    # Get current branch
    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
    log_info "Current branch: $CURRENT_BRANCH"
else
    log_warning "Not a git repository"
fi

echo ""

# =============================================================================
# CHECK 7: SECURITY CHECKS
# =============================================================================

log_info "Check 7: Security Checks"
echo "─────────────────────────────────────"

# Check if .env is in .gitignore
if [ -f "../.gitignore" ]; then
    if grep -q "^\.env$" ../.gitignore || grep -q "^\.env" ../.gitignore; then
        log_success ".env is in .gitignore"
    else
        log_error ".env is NOT in .gitignore - SECURITY RISK!"
        ((FAILED_CHECKS++))
    fi
else
    log_warning ".gitignore not found"
fi

# Check for hardcoded keys in source code
log_info "Scanning for potential hardcoded secrets..."
HARDCODED_KEY_PATTERN="0x[0-9a-fA-F]{64}"
if grep -r -E "$HARDCODED_KEY_PATTERN" src/ hardhat/scripts/ 2>/dev/null | grep -v "0x0000000000000000000000000000000000000000000000000000000000000000" | grep -q .; then
    log_error "Potential hardcoded private keys found in source code!"
    ((FAILED_CHECKS++))
else
    log_success "No hardcoded private keys detected"
fi

echo ""

# =============================================================================
# SUMMARY
# =============================================================================

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   PRE-DEPLOYMENT CHECK SUMMARY                            ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

if [ $FAILED_CHECKS -eq 0 ]; then
    log_success "All critical checks passed! ✨"
    echo ""
    log_info "You are ready to deploy to $NETWORK"
    echo ""
    exit 0
else
    log_error "Failed checks: $FAILED_CHECKS"
    echo ""
    log_error "Please fix the issues above before deploying"
    echo ""
    exit 1
fi
