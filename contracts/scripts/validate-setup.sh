#!/bin/bash
# Deployment Setup Validation Script
# Tests all deployment prerequisites and configurations

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTRACTS_DIR="$(dirname "$SCRIPT_DIR")"
ROOT_DIR="$(dirname "$CONTRACTS_DIR")"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   Deployment Setup Validation Script                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASSED=0
FAILED=0
WARNINGS=0

# Helper functions
pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSED++))
}

fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAILED++))
}

warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNINGS++))
}

# Test 1: Check directory structure
echo "═══════════════════════════════════════════════════════════"
echo "Test 1: Directory Structure"
echo "═══════════════════════════════════════════════════════════"

if [ -d "$CONTRACTS_DIR/hardhat" ]; then
    pass "Hardhat directory exists"
else
    fail "Hardhat directory not found"
fi

if [ -d "$CONTRACTS_DIR/0g-uniswap-v2" ]; then
    pass "0g-uniswap-v2 directory exists"
else
    fail "0g-uniswap-v2 directory not found"
fi

if [ -d "$CONTRACTS_DIR/oinio-memorial-bridge" ]; then
    pass "oinio-memorial-bridge directory exists"
else
    fail "oinio-memorial-bridge directory not found"
fi

echo ""

# Test 2: Check required files
echo "═══════════════════════════════════════════════════════════"
echo "Test 2: Required Files"
echo "═══════════════════════════════════════════════════════════"

files_to_check=(
    "$CONTRACTS_DIR/hardhat/hardhat.config.ts"
    "$CONTRACTS_DIR/hardhat/package.json"
    "$CONTRACTS_DIR/hardhat/scripts/deploy-inft.ts"
    "$CONTRACTS_DIR/hardhat/scripts/deploy-dex.ts"
    "$CONTRACTS_DIR/hardhat/scripts/check-balance.ts"
    "$CONTRACTS_DIR/script/Deploy.s.sol"
    "$CONTRACTS_DIR/0g-uniswap-v2/script/Deploy.s.sol"
    "$CONTRACTS_DIR/foundry.toml"
    "$CONTRACTS_DIR/DEPLOYMENT_GUIDE.md"
    "$CONTRACTS_DIR/SOROBAN_DEPLOYMENT.md"
    "$CONTRACTS_DIR/QUICK_REFERENCE.md"
)

for file in "${files_to_check[@]}"; do
    if [ -f "$file" ]; then
        pass "$(basename "$file") exists"
    else
        fail "$(basename "$file") not found at $file"
    fi
done

echo ""

# Test 3: Check environment configuration
echo "═══════════════════════════════════════════════════════════"
echo "Test 3: Environment Configuration"
echo "═══════════════════════════════════════════════════════════"

if [ -f "$CONTRACTS_DIR/.env.example" ]; then
    pass ".env.example exists"
else
    fail ".env.example not found"
fi

if [ -f "$CONTRACTS_DIR/.env" ]; then
    warn ".env exists (good for deployment, but ensure it's in .gitignore)"
    
    # Check if PRIVATE_KEY is set
    if grep -q "PRIVATE_KEY=0x" "$CONTRACTS_DIR/.env" 2>/dev/null; then
        if grep -q "PRIVATE_KEY=0x0000000000000000000000000000000000000000000000000000000000000000" "$CONTRACTS_DIR/.env"; then
            warn "PRIVATE_KEY is set to example value - update before deploying"
        else
            pass "PRIVATE_KEY is configured (not default value)"
        fi
    else
        warn ".env exists but PRIVATE_KEY may not be set"
    fi
else
    warn ".env not found (create from .env.example before deploying)"
fi

# Check .gitignore
if [ -f "$CONTRACTS_DIR/../.gitignore" ]; then
    if grep -q ".env" "$CONTRACTS_DIR/../.gitignore" 2>/dev/null; then
        pass ".env is in .gitignore"
    else
        fail ".env is NOT in .gitignore - this is a security risk!"
    fi
else
    warn ".gitignore not found"
fi

echo ""

# Test 4: Check Node.js and npm
echo "═══════════════════════════════════════════════════════════"
echo "Test 4: Node.js Environment"
echo "═══════════════════════════════════════════════════════════"

if command -v node >/dev/null 2>&1; then
    NODE_VERSION=$(node --version)
    pass "Node.js installed: $NODE_VERSION"
    
    # Check if version is 20+
    MAJOR_VERSION=$(echo "$NODE_VERSION" | sed 's/v//' | cut -d. -f1)
    if [ "$MAJOR_VERSION" -ge 20 ]; then
        pass "Node.js version is 20+ (recommended)"
    else
        warn "Node.js version is < 20 (20+ recommended)"
    fi
else
    fail "Node.js not found"
fi

if command -v npm >/dev/null 2>&1; then
    NPM_VERSION=$(npm --version)
    pass "npm installed: $NPM_VERSION"
else
    fail "npm not found"
fi

# Check if Hardhat dependencies are installed
if [ -d "$CONTRACTS_DIR/hardhat/node_modules" ]; then
    pass "Hardhat dependencies installed"
else
    warn "Hardhat dependencies not installed - run 'cd contracts/hardhat && npm install'"
fi

echo ""

# Test 5: Check Foundry
echo "═══════════════════════════════════════════════════════════"
echo "Test 5: Foundry Environment"
echo "═══════════════════════════════════════════════════════════"

if command -v forge >/dev/null 2>&1; then
    FORGE_VERSION=$(forge --version | head -n 1)
    pass "Forge installed: $FORGE_VERSION"
else
    fail "Forge not found - install from https://book.getfoundry.sh/"
fi

if command -v cast >/dev/null 2>&1; then
    pass "Cast installed"
else
    fail "Cast not found"
fi

# Check if contracts compile
echo ""
echo "Checking Forge compilation..."
cd "$CONTRACTS_DIR"
if forge build >/dev/null 2>&1; then
    pass "Contracts compile successfully with Forge"
else
    fail "Forge compilation failed - run 'forge build' to see errors"
fi

echo ""

# Test 6: Check Soroban (optional)
echo "═══════════════════════════════════════════════════════════"
echo "Test 6: Soroban Environment (Optional)"
echo "═══════════════════════════════════════════════════════════"

if command -v soroban >/dev/null 2>&1; then
    SOROBAN_VERSION=$(soroban --version)
    pass "Soroban CLI installed: $SOROBAN_VERSION"
else
    warn "Soroban CLI not found (only needed for Pi Network Stellar contracts)"
fi

if command -v cargo >/dev/null 2>&1; then
    CARGO_VERSION=$(cargo --version)
    pass "Cargo installed: $CARGO_VERSION"
else
    warn "Cargo not found (only needed for Soroban contracts)"
fi

echo ""

# Test 7: Check TypeScript compilation
echo "═══════════════════════════════════════════════════════════"
echo "Test 7: TypeScript Configuration"
echo "═══════════════════════════════════════════════════════════"

if command -v tsc >/dev/null 2>&1; then
    pass "TypeScript compiler installed"
else
    warn "TypeScript compiler not found globally"
fi

if [ -f "$CONTRACTS_DIR/hardhat/tsconfig.json" ]; then
    pass "Hardhat tsconfig.json exists"
else
    fail "Hardhat tsconfig.json not found"
fi

echo ""

# Test 8: Check documentation
echo "═══════════════════════════════════════════════════════════"
echo "Test 8: Documentation Completeness"
echo "═══════════════════════════════════════════════════════════"

docs=(
    "DEPLOYMENT_GUIDE.md:Comprehensive deployment guide"
    "SOROBAN_DEPLOYMENT.md:Soroban deployment guide"
    "QUICK_REFERENCE.md:Quick reference guide"
    "hardhat/README.md:Hardhat documentation"
    "README.md:Main contracts README"
)

for doc in "${docs[@]}"; do
    filename="${doc%%:*}"
    description="${doc##*:}"
    if [ -f "$CONTRACTS_DIR/$filename" ]; then
        pass "$description exists"
    else
        fail "$description not found"
    fi
done

echo ""

# Test 9: Validate script files
echo "═══════════════════════════════════════════════════════════"
echo "Test 9: Script Validation"
echo "═══════════════════════════════════════════════════════════"

# Check if scripts are executable
scripts_to_check=(
    "$CONTRACTS_DIR/oinio-memorial-bridge/build.sh"
    "$CONTRACTS_DIR/oinio-memorial-bridge/deploy.sh"
)

for script in "${scripts_to_check[@]}"; do
    if [ -f "$script" ]; then
        if [ -x "$script" ]; then
            pass "$(basename "$script") is executable"
        else
            warn "$(basename "$script") is not executable - run 'chmod +x $script'"
        fi
    fi
done

echo ""

# Summary
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    VALIDATION SUMMARY                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}Passed:${NC}   $PASSED"
echo -e "${YELLOW}Warnings:${NC} $WARNINGS"
echo -e "${RED}Failed:${NC}   $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All critical checks passed!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Configure .env file (copy from .env.example)"
    echo "2. Install Hardhat dependencies: cd contracts/hardhat && npm install"
    echo "3. Review documentation: contracts/QUICK_REFERENCE.md"
    echo "4. Run deployment: npm run deploy:inft:0g (or other deploy command)"
    exit 0
else
    echo -e "${RED}❌ Some checks failed!${NC}"
    echo ""
    echo "Please fix the issues above before deploying."
    echo "See contracts/DEPLOYMENT_GUIDE.md for detailed setup instructions."
    exit 1
fi
