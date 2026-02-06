#!/bin/bash

# =============================================================================
# COMPREHENSIVE DEPLOYMENT ORCHESTRATION SCRIPT
# =============================================================================
# This script orchestrates deployment of all contracts across multiple chains
# Supports: Hardhat (iNFT), Forge (DEX, OINIO), Soroban (Memorial)
# =============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   DEPLOYMENT ORCHESTRATION SCRIPT                         ║"
echo "║   Multi-Chain, Multi-Tool Deployment System               ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Navigate to contracts directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTRACTS_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$CONTRACTS_DIR"

# =============================================================================
# PARSE COMMAND LINE ARGUMENTS
# =============================================================================

DEPLOY_TARGET="all"
NETWORK="mainnet"
SKIP_CHECKS=false
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --target)
            DEPLOY_TARGET="$2"
            shift 2
            ;;
        --network)
            NETWORK="$2"
            shift 2
            ;;
        --skip-checks)
            SKIP_CHECKS=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --help)
            echo "Usage: ./deploy-all.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --target <TARGET>    Deployment target: all, inft, dex, memorial"
            echo "  --network <NETWORK>  Network: mainnet, testnet"
            echo "  --skip-checks        Skip pre-deployment checks"
            echo "  --dry-run            Show deployment plan without executing"
            echo "  --help               Show this help message"
            echo ""
            echo "Examples:"
            echo "  ./deploy-all.sh --target inft --network testnet"
            echo "  ./deploy-all.sh --target dex --network mainnet"
            echo "  ./deploy-all.sh --dry-run"
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

log_info "Deployment Configuration:"
echo "  Target: $DEPLOY_TARGET"
echo "  Network: $NETWORK"
echo "  Skip Checks: $SKIP_CHECKS"
echo "  Dry Run: $DRY_RUN"
echo ""

# =============================================================================
# LOAD AND VALIDATE ENVIRONMENT
# =============================================================================

log_info "Loading environment configuration..."

if [ ! -f ".env" ]; then
    log_error ".env file not found!"
    log_info "Please create .env from .env.example and configure it"
    exit 1
fi

source .env

# Validate required variables
if [ -z "$PRIVATE_KEY" ]; then
    log_error "PRIVATE_KEY not set in .env"
    exit 1
fi

log_success "Environment loaded"
echo ""

# =============================================================================
# PRE-DEPLOYMENT CHECKS
# =============================================================================

if [ "$SKIP_CHECKS" = false ] && [ "$DRY_RUN" = false ]; then
    log_info "Running pre-deployment checks..."
    
    if [ -f "scripts/pre-deploy-check.sh" ]; then
        bash scripts/pre-deploy-check.sh --network "$NETWORK"
        if [ $? -ne 0 ]; then
            log_error "Pre-deployment checks failed!"
            exit 1
        fi
    else
        log_warning "Pre-deployment check script not found, skipping..."
    fi
    
    log_success "Pre-deployment checks passed"
    echo ""
fi

# =============================================================================
# DEPLOYMENT FUNCTIONS
# =============================================================================

deploy_inft_pi() {
    log_info "Deploying iNFT contracts to Pi Network ($NETWORK)..."
    
    if [ "$DRY_RUN" = true ]; then
        log_info "[DRY RUN] Would deploy OINIO Token and Model Registry to Pi Network"
        return 0
    fi
    
    # Method 1: Using Hardhat
    if [ "$NETWORK" = "mainnet" ]; then
        log_info "Using Hardhat for deployment..."
        cd hardhat
        npm run deploy:pi:inft
        cd ..
    else
        log_info "Using Hardhat for testnet deployment..."
        cd hardhat
        npm run deploy:pi:testnet:inft
        cd ..
    fi
    
    log_success "iNFT deployment completed"
}

deploy_inft_0g() {
    log_info "Deploying iNFT contracts to 0G Network..."
    
    if [ "$DRY_RUN" = true ]; then
        log_info "[DRY RUN] Would deploy OINIO Token and Model Registry to 0G"
        return 0
    fi
    
    cd hardhat
    npm run deploy:0g:inft
    cd ..
    
    log_success "iNFT deployment to 0G completed"
}

deploy_inft_forge() {
    log_info "Deploying iNFT contracts using Forge..."
    
    if [ "$DRY_RUN" = true ]; then
        log_info "[DRY RUN] Would deploy via Forge script"
        return 0
    fi
    
    local RPC_URL=""
    if [ "$NETWORK" = "mainnet" ]; then
        RPC_URL="${RPC_URL_MAINNET}"
    else
        RPC_URL="${RPC_URL_TESTNET}"
    fi
    
    log_info "Deploying via Forge to $RPC_URL..."
    forge script script/Deploy.s.sol \
        --rpc-url "$RPC_URL" \
        --private-key "$PRIVATE_KEY" \
        --broadcast \
        --verify \
        --slow
    
    log_success "Forge deployment completed"
}

deploy_dex_0g() {
    log_info "Deploying DEX contracts to 0G Network..."
    
    if [ "$DRY_RUN" = true ]; then
        log_info "[DRY RUN] Would deploy W0G, Factory, and Router to 0G"
        return 0
    fi
    
    cd 0g-uniswap-v2
    
    # Check if setup is complete
    if [ ! -f ".env" ]; then
        log_warning "0G DEX .env not found, copying from example..."
        cp .env.example .env
        log_error "Please configure 0g-uniswap-v2/.env and run again"
        exit 1
    fi
    
    log_info "Running 0G DEX deployment script..."
    bash scripts/deploy.sh
    
    cd ..
    log_success "DEX deployment completed"
}

deploy_memorial_pi() {
    log_info "Deploying Memorial Bridge to Pi Network via Soroban..."
    
    if [ "$DRY_RUN" = true ]; then
        log_info "[DRY RUN] Would deploy Memorial contract via Soroban"
        return 0
    fi
    
    cd oinio-memorial-bridge
    
    # Check if built
    if [ ! -f "target/wasm32-unknown-unknown/release/oinio_memorial_bridge.wasm" ]; then
        log_info "Building Memorial contract..."
        bash build.sh
    fi
    
    log_info "Deploying Memorial contract..."
    bash deploy.sh
    
    cd ..
    log_success "Memorial deployment completed"
}

# =============================================================================
# MAIN DEPLOYMENT LOGIC
# =============================================================================

log_info "Starting deployment process..."
echo ""

case $DEPLOY_TARGET in
    all)
        log_info "Deploying ALL contracts to specified networks..."
        echo ""
        
        # Deploy iNFT contracts
        if [ "$NETWORK" = "mainnet" ]; then
            deploy_inft_pi
            echo ""
            deploy_inft_0g
        else
            deploy_inft_pi
        fi
        echo ""
        
        # Deploy DEX (0G only)
        if [ "$NETWORK" = "mainnet" ]; then
            deploy_dex_0g
            echo ""
        fi
        
        # Deploy Memorial (Pi Network only)
        if [ "$NETWORK" = "mainnet" ]; then
            deploy_memorial_pi
            echo ""
        fi
        ;;
        
    inft)
        log_info "Deploying iNFT contracts only..."
        echo ""
        
        if [ "$NETWORK" = "mainnet" ]; then
            deploy_inft_pi
            echo ""
            deploy_inft_0g
        else
            deploy_inft_pi
        fi
        ;;
        
    dex)
        log_info "Deploying DEX contracts to 0G..."
        echo ""
        deploy_dex_0g
        ;;
        
    memorial)
        log_info "Deploying Memorial Bridge to Pi Network..."
        echo ""
        deploy_memorial_pi
        ;;
        
    *)
        log_error "Unknown target: $DEPLOY_TARGET"
        log_info "Valid targets: all, inft, dex, memorial"
        exit 1
        ;;
esac

# =============================================================================
# POST-DEPLOYMENT ACTIONS
# =============================================================================

if [ "$DRY_RUN" = false ]; then
    log_info "Running post-deployment verification..."
    echo ""
    
    if [ -f "scripts/post-deploy-check.sh" ]; then
        bash scripts/post-deploy-check.sh --network "$NETWORK"
    else
        log_warning "Post-deployment check script not found, skipping..."
    fi
    
    # Save deployment summary
    log_info "Generating deployment summary..."
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    SUMMARY_FILE="deployments/deployment_${NETWORK}_${TIMESTAMP}.txt"
    
    mkdir -p deployments
    
    cat > "$SUMMARY_FILE" << EOF
Deployment Summary
==================
Timestamp: $(date)
Network: $NETWORK
Target: $DEPLOY_TARGET

Deployment Details:
- Review deployment logs above for contract addresses
- Check hardhat/deployments/ for detailed JSON files
- Update .env.launch with deployed addresses

Next Steps:
1. Verify contracts on block explorers
2. Update frontend configuration
3. Run health checks
4. Test contract interactions

EOF
    
    log_success "Deployment summary saved to $SUMMARY_FILE"
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   DEPLOYMENT COMPLETE                                     ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

if [ "$DRY_RUN" = true ]; then
    log_info "This was a dry run. No actual deployments were made."
else
    log_success "All deployments completed successfully!"
    log_info "Review deployment logs and summaries above"
    echo ""
    log_info "Next steps:"
    echo "  1. Run: npm run verify:contracts"
    echo "  2. Run: npm run health:check"
    echo "  3. Update frontend with new addresses"
fi

echo ""
