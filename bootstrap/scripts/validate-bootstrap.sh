#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# Bootstrap Agent Validation Script
# ═══════════════════════════════════════════════════════════════════════════
#
# This script validates that the bootstrap agent is properly configured
# without running the full bootstrap process.
#
# Usage: ./validate-bootstrap.sh
#
# ═══════════════════════════════════════════════════════════════════════════

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "═══════════════════════════════════════════════════════════════"
echo "Bootstrap Agent Validation"
echo "═══════════════════════════════════════════════════════════════"
echo ""

ERRORS=0
WARNINGS=0

# Check bootstrap scripts exist and are executable
echo "Checking bootstrap scripts..."
if [ -f "$PROJECT_ROOT/bootstrap/bootstrap.sh" ]; then
    echo -e "${GREEN}✓${NC} bootstrap.sh exists"
    
    if [ -x "$PROJECT_ROOT/bootstrap/bootstrap.sh" ]; then
        echo -e "${GREEN}✓${NC} bootstrap.sh is executable"
    else
        echo -e "${RED}✗${NC} bootstrap.sh is not executable"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo -e "${RED}✗${NC} bootstrap.sh not found"
    ERRORS=$((ERRORS + 1))
fi

if [ -f "$PROJECT_ROOT/bootstrap/bootstrap.ps1" ]; then
    echo -e "${GREEN}✓${NC} bootstrap.ps1 exists"
else
    echo -e "${RED}✗${NC} bootstrap.ps1 not found"
    ERRORS=$((ERRORS + 1))
fi

echo ""

# Check documentation
echo "Checking documentation..."
DOCS=(
    "bootstrap/README.md"
    "bootstrap/QUICKSTART.md"
    "bootstrap/DEPLOYMENT_GUIDE.md"
    "bootstrap/docs/AUTONOMOUS_OPERATIONS.md"
)

for doc in "${DOCS[@]}"; do
    if [ -f "$PROJECT_ROOT/$doc" ]; then
        echo -e "${GREEN}✓${NC} $doc exists"
    else
        echo -e "${RED}✗${NC} $doc not found"
        ERRORS=$((ERRORS + 1))
    fi
done

echo ""

# Check templates
echo "Checking templates..."
TEMPLATES=(
    "bootstrap/templates/railway.toml.template"
    "bootstrap/templates/docker-compose.yml.template"
)

for template in "${TEMPLATES[@]}"; do
    if [ -f "$PROJECT_ROOT/$template" ]; then
        echo -e "${GREEN}✓${NC} $template exists"
    else
        echo -e "${RED}✗${NC} $template not found"
        ERRORS=$((ERRORS + 1))
    fi
done

echo ""

# Check critical project files
echo "Checking critical project files..."
CRITICAL_FILES=(
    "server/main.py"
    "server/app.py"
    "server/canticle_interface.py"
    "server/requirements.txt"
    "Dockerfile"
    "railway.toml"
    ".env.example"
)

for file in "${CRITICAL_FILES[@]}"; do
    if [ -f "$PROJECT_ROOT/$file" ]; then
        echo -e "${GREEN}✓${NC} $file exists"
    else
        echo -e "${RED}✗${NC} $file not found"
        ERRORS=$((ERRORS + 1))
    fi
done

echo ""

# Check .env.example has required variables
echo "Checking .env.example configuration..."
ENV_EXAMPLE="$PROJECT_ROOT/.env.example"
if [ -f "$ENV_EXAMPLE" ]; then
    REQUIRED_VARS=("SUPABASE_URL" "SUPABASE_KEY" "JWT_SECRET")
    
    for var in "${REQUIRED_VARS[@]}"; do
        if grep -q "^$var=" "$ENV_EXAMPLE"; then
            echo -e "${GREEN}✓${NC} $var found in .env.example"
        else
            echo -e "${RED}✗${NC} $var not found in .env.example"
            ERRORS=$((ERRORS + 1))
        fi
    done
else
    echo -e "${RED}✗${NC} .env.example not found"
    ERRORS=$((ERRORS + 1))
fi

echo ""

# Check .gitignore
echo "Checking .gitignore configuration..."
GITIGNORE="$PROJECT_ROOT/.gitignore"
if [ -f "$GITIGNORE" ]; then
    IGNORE_PATTERNS=("bootstrap/bootstrap-*.log" "logs/")
    
    for pattern in "${IGNORE_PATTERNS[@]}"; do
        if grep -q "$pattern" "$GITIGNORE"; then
            echo -e "${GREEN}✓${NC} $pattern in .gitignore"
        else
            echo -e "${YELLOW}⚠${NC} $pattern not in .gitignore"
            WARNINGS=$((WARNINGS + 1))
        fi
    done
else
    echo -e "${RED}✗${NC} .gitignore not found"
    ERRORS=$((ERRORS + 1))
fi

echo ""

# Check Python version
echo "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} Python installed: $PYTHON_VERSION"
    
    if python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)"; then
        echo -e "${GREEN}✓${NC} Python version >= 3.11"
    else
        echo -e "${YELLOW}⚠${NC} Python version < 3.11 (recommended: 3.11+)"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo -e "${RED}✗${NC} Python3 not found"
    ERRORS=$((ERRORS + 1))
fi

echo ""

# Check bootstrap script syntax
echo "Checking bootstrap.sh syntax..."
if bash -n "$PROJECT_ROOT/bootstrap/bootstrap.sh" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} bootstrap.sh syntax is valid"
else
    echo -e "${RED}✗${NC} bootstrap.sh has syntax errors"
    ERRORS=$((ERRORS + 1))
fi

echo ""

# Check README updated
echo "Checking README.md..."
README="$PROJECT_ROOT/README.md"
if [ -f "$README" ]; then
    if grep -q "bootstrap" "$README"; then
        echo -e "${GREEN}✓${NC} README mentions bootstrap"
    else
        echo -e "${YELLOW}⚠${NC} README doesn't mention bootstrap"
        WARNINGS=$((WARNINGS + 1))
    fi
    
    if grep -q "Quick Start" "$README"; then
        echo -e "${GREEN}✓${NC} README has Quick Start section"
    else
        echo -e "${YELLOW}⚠${NC} README missing Quick Start section"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo -e "${RED}✗${NC} README.md not found"
    ERRORS=$((ERRORS + 1))
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "Validation Complete"
echo "═══════════════════════════════════════════════════════════════"
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    echo ""
    echo "Bootstrap agent is ready to use:"
    echo "  Linux/macOS: ./bootstrap/bootstrap.sh"
    echo "  Windows:     .\\bootstrap\\bootstrap.ps1"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠ Validation passed with $WARNINGS warning(s)${NC}"
    echo "Bootstrap agent should work, but review warnings above."
    exit 0
else
    echo -e "${RED}✗ Validation failed with $ERRORS error(s) and $WARNINGS warning(s)${NC}"
    echo "Fix errors before using bootstrap agent."
    exit 1
fi
