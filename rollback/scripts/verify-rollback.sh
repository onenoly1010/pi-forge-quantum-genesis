#!/bin/bash
# 🔍 QUANTUM RESONANCE LATTICE - ROLLBACK VERIFICATION SYSTEM
# Post-rollback health check and validation script

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROLLBACK_ROOT="$(dirname "$SCRIPT_DIR")"
PROJECT_ROOT="$(dirname "$ROLLBACK_ROOT")"

# Default values
QUICK_MODE=false
CHECK_ONLY=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --quick)
            QUICK_MODE=true
            shift
            ;;
        --check-only)
            CHECK_ONLY=true
            shift
            ;;
        *)
            shift
            ;;
    esac
done

# Print header
echo -e "${CYAN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║   🔍 ROLLBACK VERIFICATION SYSTEM                         ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Track overall status
OVERALL_STATUS=0

# Check git status
check_git_status() {
    echo -e "${CYAN}[1/6] Checking Git Status...${NC}"
    
    cd "$PROJECT_ROOT"
    
    local current_commit=$(git rev-parse HEAD)
    echo "   Current commit: $current_commit"
    
    local branch=$(git branch --show-current)
    echo "   Current branch: $branch"
    
    local uncommitted=$(git status --porcelain | wc -l)
    if [ "$uncommitted" -eq 0 ]; then
        echo -e "   ${GREEN}✓${NC} Working directory clean"
    else
        echo -e "   ${YELLOW}⚠${NC} Uncommitted changes: $uncommitted files"
    fi
    
    echo ""
}

# Check Python environment
check_python_environment() {
    echo -e "${CYAN}[2/6] Checking Python Environment...${NC}"
    
    if command -v python3 &> /dev/null; then
        local python_version=$(python3 --version)
        echo -e "   ${GREEN}✓${NC} Python: $python_version"
    else
        echo -e "   ${RED}✗${NC} Python not found"
        OVERALL_STATUS=1
    fi
    
    # Check virtual environment
    if [ -d "$PROJECT_ROOT/.venv" ]; then
        echo -e "   ${GREEN}✓${NC} Virtual environment exists"
    else
        echo -e "   ${YELLOW}⚠${NC} No virtual environment found"
    fi
    
    # Check required packages
    if [ -f "$PROJECT_ROOT/server/requirements.txt" ]; then
        local req_count=$(cat "$PROJECT_ROOT/server/requirements.txt" | grep -v '^#' | grep -v '^$' | wc -l)
        echo -e "   ${GREEN}✓${NC} Requirements file found ($req_count packages)"
    fi
    
    echo ""
}

# Check file integrity
check_file_integrity() {
    echo -e "${CYAN}[3/6] Checking Critical Files...${NC}"
    
    local critical_files=(
        "server/main.py"
        "server/app.py"
        "server/canticle_interface.py"
        "server/requirements.txt"
        "Dockerfile"
        "railway.toml"
    )
    
    for file in "${critical_files[@]}"; do
        if [ -f "$PROJECT_ROOT/$file" ]; then
            echo -e "   ${GREEN}✓${NC} $file"
        else
            echo -e "   ${RED}✗${NC} $file (MISSING)"
            OVERALL_STATUS=1
        fi
    done
    
    echo ""
}

# Check service ports (local development only)
check_service_ports() {
    if [ "$QUICK_MODE" = true ]; then
        return
    fi
    
    echo -e "${CYAN}[4/6] Checking Service Ports...${NC}"
    
    local ports=(8000 5000 7860)
    local port_names=("FastAPI" "Flask" "Gradio")
    
    for i in "${!ports[@]}"; do
        local port=${ports[$i]}
        local name=${port_names[$i]}
        
        if command -v lsof &> /dev/null; then
            if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
                echo -e "   ${GREEN}✓${NC} Port $port ($name): Active"
            else
                echo -e "   ${YELLOW}⚠${NC} Port $port ($name): Not listening"
            fi
        elif command -v netstat &> /dev/null; then
            if netstat -tuln | grep -q ":$port "; then
                echo -e "   ${GREEN}✓${NC} Port $port ($name): Active"
            else
                echo -e "   ${YELLOW}⚠${NC} Port $port ($name): Not listening"
            fi
        else
            echo -e "   ${YELLOW}⚠${NC} Cannot check ports (lsof/netstat not available)"
            break
        fi
    done
    
    echo ""
}

# Check configuration
check_configuration() {
    echo -e "${CYAN}[5/6] Checking Configuration...${NC}"
    
    # Check environment file
    if [ -f "$PROJECT_ROOT/.env" ]; then
        echo -e "   ${GREEN}✓${NC} .env file exists"
        
        # Check for required variables (without exposing values)
        if grep -q "SUPABASE_URL" "$PROJECT_ROOT/.env" 2>/dev/null; then
            echo -e "   ${GREEN}✓${NC} SUPABASE_URL configured"
        else
            echo -e "   ${YELLOW}⚠${NC} SUPABASE_URL not found"
        fi
        
        if grep -q "SUPABASE_KEY" "$PROJECT_ROOT/.env" 2>/dev/null; then
            echo -e "   ${GREEN}✓${NC} SUPABASE_KEY configured"
        else
            echo -e "   ${YELLOW}⚠${NC} SUPABASE_KEY not found"
        fi
    else
        echo -e "   ${YELLOW}⚠${NC} .env file not found (expected for Railway deployment)"
    fi
    
    # Check Railway config
    if [ -f "$PROJECT_ROOT/railway.toml" ]; then
        echo -e "   ${GREEN}✓${NC} railway.toml exists"
    else
        echo -e "   ${RED}✗${NC} railway.toml missing"
        OVERALL_STATUS=1
    fi
    
    echo ""
}

# Run basic Python syntax checks
check_python_syntax() {
    if [ "$QUICK_MODE" = true ] || [ "$CHECK_ONLY" = true ]; then
        return
    fi
    
    echo -e "${CYAN}[6/6] Checking Python Syntax...${NC}"
    
    local python_files=(
        "server/main.py"
        "server/app.py"
        "server/canticle_interface.py"
    )
    
    for file in "${python_files[@]}"; do
        if [ -f "$PROJECT_ROOT/$file" ]; then
            if python3 -m py_compile "$PROJECT_ROOT/$file" 2>/dev/null; then
                echo -e "   ${GREEN}✓${NC} $file (syntax valid)"
            else
                echo -e "   ${RED}✗${NC} $file (SYNTAX ERROR)"
                OVERALL_STATUS=1
            fi
        fi
    done
    
    echo ""
}

# Test HTTP endpoints (if services are running)
test_endpoints() {
    if [ "$QUICK_MODE" = true ] || [ "$CHECK_ONLY" = true ]; then
        return
    fi
    
    echo -e "${CYAN}[OPTIONAL] Testing HTTP Endpoints...${NC}"
    
    # Only test if curl is available
    if ! command -v curl &> /dev/null; then
        echo -e "   ${YELLOW}⚠${NC} curl not available - skipping endpoint tests"
        return
    fi
    
    # Test FastAPI
    if curl -sf http://localhost:8000/ >/dev/null 2>&1; then
        echo -e "   ${GREEN}✓${NC} FastAPI endpoint responding"
    else
        echo -e "   ${YELLOW}⚠${NC} FastAPI not responding (may not be running)"
    fi
    
    # Test Flask
    if curl -sf http://localhost:5000/health >/dev/null 2>&1; then
        echo -e "   ${GREEN}✓${NC} Flask endpoint responding"
    else
        echo -e "   ${YELLOW}⚠${NC} Flask not responding (may not be running)"
    fi
    
    echo ""
}

# Main verification
main() {
    check_git_status
    check_python_environment
    check_file_integrity
    check_service_ports
    check_configuration
    check_python_syntax
    
    # Optional endpoint tests
    test_endpoints
    
    # Final summary
    echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
    
    if [ $OVERALL_STATUS -eq 0 ]; then
        echo -e "${GREEN}✅ VERIFICATION PASSED${NC}"
        echo -e "${GREEN}All critical checks completed successfully${NC}"
    else
        echo -e "${RED}❌ VERIFICATION FAILED${NC}"
        echo -e "${RED}Some critical checks failed - review output above${NC}"
    fi
    
    echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
    
    exit $OVERALL_STATUS
}

# Execute main
main
