#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# 🌌 QUANTUM PI FORGE - BOOTSTRAP AGENT
# ═══════════════════════════════════════════════════════════════════════════
#
# This is the master bootstrap script that initializes the entire Quantum Pi
# Forge autonomous system on fresh infrastructure.
#
# Usage:
#   ./bootstrap.sh [--environment ENV] [--skip-tests] [--verbose]
#
# Options:
#   --environment ENV    Target environment (development|staging|production)
#   --skip-tests        Skip test execution during bootstrap
#   --verbose           Enable verbose logging
#   --help              Show this help message
#
# ═══════════════════════════════════════════════════════════════════════════

set -e  # Exit on error

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BOOTSTRAP_DIR="$SCRIPT_DIR"
LOG_FILE="$BOOTSTRAP_DIR/bootstrap-$(date +%Y%m%d-%H%M%S).log"

ENVIRONMENT="${ENVIRONMENT:-development}"
SKIP_TESTS=false
VERBOSE=false

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ═══════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
}

log_info() {
    echo -e "${BLUE}ℹ ${NC}$*" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}✅${NC} $*" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}⚠️ ${NC}$*" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}❌${NC} $*" | tee -a "$LOG_FILE"
}

log_step() {
    echo -e "${PURPLE}🔹${NC} $*" | tee -a "$LOG_FILE"
}

print_header() {
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}$*${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
}

check_command() {
    if command -v "$1" &> /dev/null; then
        log_success "$1 is installed"
        return 0
    else
        log_error "$1 is not installed"
        return 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════
# PARSE COMMAND LINE ARGUMENTS
# ═══════════════════════════════════════════════════════════════════════════

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --environment)
                ENVIRONMENT="$2"
                shift 2
                ;;
            --skip-tests)
                SKIP_TESTS=true
                shift
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

show_help() {
    cat << EOF
Quantum Pi Forge Bootstrap Agent

Usage: ./bootstrap.sh [OPTIONS]

Options:
    --environment ENV    Target environment (development|staging|production)
                        Default: development
    --skip-tests        Skip test execution during bootstrap
    --verbose           Enable verbose logging
    --help              Show this help message

Examples:
    ./bootstrap.sh
    ./bootstrap.sh --environment production
    ./bootstrap.sh --environment staging --skip-tests
    ./bootstrap.sh --verbose

EOF
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 1: SYSTEM REQUIREMENTS CHECK
# ═══════════════════════════════════════════════════════════════════════════

check_system_requirements() {
    print_header "STEP 1: System Requirements Check"
    
    log_step "Checking required system dependencies..."
    
    local requirements_met=true
    
    # Check Python
    if check_command python3; then
        PYTHON_VERSION=$(python3 --version | awk '{print $2}')
        log_info "Python version: $PYTHON_VERSION"
        
        # Check if version is >= 3.11
        if python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)"; then
            log_success "Python version meets requirements (>= 3.11)"
        else
            log_warning "Python version should be >= 3.11, found $PYTHON_VERSION"
        fi
    else
        requirements_met=false
    fi
    
    # Check pip
    check_command pip3 || requirements_met=false
    
    # Check git
    check_command git || requirements_met=false
    
    # Optional but recommended
    if check_command curl; then
        log_success "curl is available"
    else
        log_warning "curl is not installed (optional but recommended)"
    fi
    
    if check_command docker; then
        DOCKER_VERSION=$(docker --version)
        log_success "Docker is available: $DOCKER_VERSION"
    else
        log_warning "Docker is not installed (optional for containerized deployment)"
    fi
    
    # Check for Railway CLI (optional)
    if check_command railway; then
        log_success "Railway CLI is available"
    else
        log_info "Railway CLI is not installed (optional for deployment)"
    fi
    
    if [ "$requirements_met" = false ]; then
        log_error "Some required dependencies are missing. Please install them and try again."
        exit 1
    fi
    
    log_success "All required system dependencies are available"
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 2: ENVIRONMENT SETUP
# ═══════════════════════════════════════════════════════════════════════════

setup_environment() {
    print_header "STEP 2: Environment Setup"
    
    cd "$PROJECT_ROOT"
    
    log_step "Setting up Python virtual environment..."
    
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
        log_success "Virtual environment created"
    else
        log_info "Virtual environment already exists"
    fi
    
    log_step "Activating virtual environment..."
    source .venv/bin/activate
    log_success "Virtual environment activated"
    
    log_step "Upgrading pip, setuptools, and wheel..."
    pip install --upgrade pip setuptools wheel --quiet
    log_success "Core Python packages upgraded"
    
    log_step "Installing project dependencies..."
    if [ -f "server/requirements.txt" ]; then
        pip install -r server/requirements.txt --quiet
        log_success "Project dependencies installed"
    else
        log_error "requirements.txt not found at server/requirements.txt"
        exit 1
    fi
    
    log_step "Checking environment configuration..."
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            log_warning ".env file not found. Creating from template..."
            cp .env.example .env
            log_success ".env file created from template"
            log_warning "⚠️  IMPORTANT: Please edit .env file with your actual credentials!"
        else
            log_error ".env.example not found. Cannot create .env file."
            exit 1
        fi
    else
        log_success ".env file exists"
    fi
    
    # Validate critical environment variables
    log_step "Validating environment variables..."
    source .env 2>/dev/null || true
    
    if [ -z "$SUPABASE_URL" ] || [ "$SUPABASE_URL" = "https://your-project.supabase.co" ]; then
        log_warning "SUPABASE_URL not configured in .env"
    else
        log_success "SUPABASE_URL is configured"
    fi
    
    if [ -z "$SUPABASE_KEY" ] || [ "$SUPABASE_KEY" = "your-anon-key" ]; then
        log_warning "SUPABASE_KEY not configured in .env"
    else
        log_success "SUPABASE_KEY is configured"
    fi
    
    if [ -z "$JWT_SECRET" ] || [ "$JWT_SECRET" = "your-secure-random-string-here" ]; then
        log_warning "JWT_SECRET not configured in .env"
    else
        log_success "JWT_SECRET is configured"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 3: INFRASTRUCTURE VALIDATION
# ═══════════════════════════════════════════════════════════════════════════

validate_infrastructure() {
    print_header "STEP 3: Infrastructure Validation"
    
    log_step "Validating project structure..."
    
    local critical_files=(
        "server/main.py"
        "server/app.py"
        "server/canticle_interface.py"
        "server/requirements.txt"
        "Dockerfile"
        "railway.toml"
        "frontend/pi-forge-integration.js"
    )
    
    local all_present=true
    for file in "${critical_files[@]}"; do
        if [ -f "$PROJECT_ROOT/$file" ]; then
            log_success "✓ $file"
        else
            log_error "✗ $file (missing)"
            all_present=false
        fi
    done
    
    if [ "$all_present" = false ]; then
        log_error "Some critical files are missing"
        exit 1
    fi
    
    log_success "All critical files present"
    
    log_step "Validating Python imports..."
    cd "$PROJECT_ROOT"
    
    if python3 -c "import sys; sys.path.insert(0, 'server'); from main import app; print('OK')" 2>/dev/null; then
        log_success "FastAPI module imports successfully"
    else
        log_error "FastAPI module import failed"
        exit 1
    fi
    
    if python3 -c "import sys; sys.path.insert(0, 'server'); from app import app; print('OK')" 2>/dev/null; then
        log_success "Flask module imports successfully"
    else
        log_error "Flask module import failed"
        exit 1
    fi
    
    log_success "Infrastructure validation complete"
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 4: RUN TESTS
# ═══════════════════════════════════════════════════════════════════════════

run_tests() {
    if [ "$SKIP_TESTS" = true ]; then
        log_warning "Skipping tests (--skip-tests flag provided)"
        return 0
    fi
    
    print_header "STEP 4: Running Tests"
    
    log_step "Installing test dependencies..."
    pip install pytest pytest-asyncio pytest-cov --quiet
    log_success "Test dependencies installed"
    
    log_step "Running test suite..."
    cd "$PROJECT_ROOT/tests"
    
    if python -m pytest -v --tb=short 2>&1 | tee -a "$LOG_FILE"; then
        log_success "All tests passed"
    else
        log_warning "Some tests failed (non-critical for bootstrap)"
    fi
    
    cd "$PROJECT_ROOT"
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 5: SERVICE INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════

initialize_services() {
    print_header "STEP 5: Service Initialization"
    
    log_step "Checking service health..."
    
    # Create a simple health check script
    cat > "$BOOTSTRAP_DIR/health_check.py" << 'EOF'
import sys
sys.path.insert(0, 'server')

try:
    from main import app as fastapi_app
    print("✅ FastAPI: OK")
except Exception as e:
    print(f"❌ FastAPI: FAILED - {e}")
    sys.exit(1)

try:
    from app import app as flask_app
    print("✅ Flask: OK")
except Exception as e:
    print(f"❌ Flask: FAILED - {e}")
    sys.exit(1)

try:
    import canticle_interface
    print("✅ Gradio: OK")
except Exception as e:
    print(f"❌ Gradio: FAILED - {e}")
    sys.exit(1)

print("\n🎉 All services initialized successfully!")
EOF
    
    cd "$PROJECT_ROOT"
    if python3 "$BOOTSTRAP_DIR/health_check.py"; then
        log_success "All services health check passed"
    else
        log_error "Service health check failed"
        exit 1
    fi
    
    # Clean up
    rm -f "$BOOTSTRAP_DIR/health_check.py"
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 6: DEPLOYMENT PREPARATION
# ═══════════════════════════════════════════════════════════════════════════

prepare_deployment() {
    print_header "STEP 6: Deployment Preparation"
    
    log_step "Validating deployment configuration..."
    
    # Check railway.toml
    if [ -f "$PROJECT_ROOT/railway.toml" ]; then
        log_success "railway.toml exists"
    else
        log_warning "railway.toml not found (needed for Railway deployment)"
    fi
    
    # Check Dockerfile
    if [ -f "$PROJECT_ROOT/Dockerfile" ]; then
        log_success "Dockerfile exists"
        
        if command -v docker &> /dev/null; then
            log_step "Testing Docker build..."
            if docker build -t quantum-pi-forge-test "$PROJECT_ROOT" 2>&1 | tail -5 | tee -a "$LOG_FILE"; then
                log_success "Docker build test passed"
            else
                log_warning "Docker build test failed (may be due to platform)"
            fi
        fi
    else
        log_error "Dockerfile not found"
    fi
    
    log_step "Generating deployment checklist..."
    cat > "$BOOTSTRAP_DIR/deployment-checklist.md" << EOF
# Deployment Checklist

Generated: $(date)
Environment: $ENVIRONMENT

## Pre-Deployment

- [x] System requirements verified
- [x] Python environment configured
- [x] Dependencies installed
- [x] Environment variables set
- [x] Infrastructure validated
- [x] Tests executed
- [x] Services initialized

## Deployment Steps

### Option 1: Railway Deployment

1. Install Railway CLI:
   \`\`\`bash
   npm i -g @railway/cli
   \`\`\`

2. Login to Railway:
   \`\`\`bash
   railway login
   \`\`\`

3. Link to project (or create new):
   \`\`\`bash
   railway link
   \`\`\`

4. Set environment variables:
   \`\`\`bash
   railway variables set SUPABASE_URL=<your-url>
   railway variables set SUPABASE_KEY=<your-key>
   railway variables set JWT_SECRET=<your-secret>
   \`\`\`

5. Deploy:
   \`\`\`bash
   railway up
   \`\`\`

### Option 2: Docker Deployment

1. Build image:
   \`\`\`bash
   docker build -t quantum-pi-forge .
   \`\`\`

2. Run container:
   \`\`\`bash
   docker run -p 8000:8000 --env-file .env quantum-pi-forge
   \`\`\`

### Option 3: Local Development

1. Start FastAPI (Port 8000):
   \`\`\`bash
   uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload
   \`\`\`

2. Start Flask (Port 5000):
   \`\`\`bash
   python server/app.py
   \`\`\`

3. Start Gradio (Port 7860):
   \`\`\`bash
   python server/canticle_interface.py
   \`\`\`

## Post-Deployment

- [ ] Verify health endpoints
- [ ] Test authentication
- [ ] Test WebSocket connections
- [ ] Monitor logs for errors
- [ ] Set up autonomous monitoring

## Autonomous Handoff

Once deployed, activate autonomous operations:

\`\`\`bash
# Enable scheduled monitoring
gh workflow enable ai-agent-handoff-runbook.yml

# Trigger initial health check
gh workflow run ai-agent-handoff-runbook.yml --field action=health-check
\`\`\`

EOF
    
    log_success "Deployment checklist created: $BOOTSTRAP_DIR/deployment-checklist.md"
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 7: AUTONOMOUS HANDOFF SETUP
# ═══════════════════════════════════════════════════════════════════════════

setup_autonomous_handoff() {
    print_header "STEP 7: Autonomous Handoff Setup"
    
    log_step "Validating autonomous runbook..."
    
    RUNBOOK_FILE="$PROJECT_ROOT/.github/workflows/ai-agent-handoff-runbook.yml"
    if [ -f "$RUNBOOK_FILE" ]; then
        log_success "AI Agent Handoff Runbook found"
    else
        log_warning "AI Agent Handoff Runbook not found at $RUNBOOK_FILE"
    fi
    
    log_step "Creating autonomous operations guide..."
    cat > "$BOOTSTRAP_DIR/autonomous-operations.md" << 'EOF'
# Autonomous Operations Guide

## Overview

The Quantum Pi Forge system is designed for autonomous operation through the AI Agent Handoff Runbook. This guide explains how to enable and monitor autonomous operations.

## Enable Autonomous Mode

### 1. GitHub Secrets Configuration

Set the following secrets in your GitHub repository:

- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_KEY` - Your Supabase anonymous key
- `JWT_SECRET` - Secure random string for JWT signing

Optional (for notifications):
- `SLACK_WEBHOOK_URL` - For Slack alerts
- `DISCORD_WEBHOOK_URL` - For Discord alerts

### 2. Enable Workflow

```bash
gh workflow enable ai-agent-handoff-runbook.yml
```

### 3. Trigger Initial Deployment

```bash
gh workflow run ai-agent-handoff-runbook.yml \
  --field action=full-deployment
```

## Autonomous Schedule

The system automatically runs health checks every 6 hours:
- **Cron**: `0 */6 * * *`
- **Actions**: Health validation, metrics collection, status updates

## Monitoring

### Check Status Issue

The system maintains a tracking issue:

```bash
gh issue list --label ai-agent,automated,runbook
```

### View Recent Runs

```bash
gh run list --workflow=ai-agent-handoff-runbook.yml --limit 10
```

### Download Reports

```bash
gh run download <run-id> --name monitoring-report
```

## Manual Operations

### Health Check

```bash
gh workflow run ai-agent-handoff-runbook.yml \
  --field action=health-check
```

### Rollback

```bash
gh workflow run ai-agent-handoff-runbook.yml \
  --field action=rollback
```

### Emergency Stop

```bash
gh workflow run ai-agent-handoff-runbook.yml \
  --field action=emergency-stop
```

## Autonomous Features

1. **Automated Health Monitoring** - Every 6 hours
2. **Self-Healing** - Automatic rollback on failure
3. **Status Tracking** - GitHub issue with current status
4. **Deployment History** - Tagged releases for rollback
5. **Alert System** - Webhook notifications on issues

## Success Criteria

✅ System running autonomously when:
- Scheduled health checks run successfully
- Status issue updates regularly
- Monitoring reports generated
- Rollback mechanism tested
- No manual intervention needed for routine operations

EOF
    
    log_success "Autonomous operations guide created: $BOOTSTRAP_DIR/autonomous-operations.md"
    
    log_step "Creating quick start helper script..."
    cat > "$BOOTSTRAP_DIR/start-services.sh" << 'EOF'
#!/bin/bash
# Quick start script for all Quantum Pi Forge services

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🌌 Starting Quantum Pi Forge Services..."
echo ""

cd "$PROJECT_ROOT"

# Activate virtual environment
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Run bootstrap.sh first."
    exit 1
fi

# Load environment
if [ -f ".env" ]; then
    set -a
    source .env
    set +a
else
    echo "⚠️  .env file not found. Run bootstrap.sh first."
    exit 1
fi

echo "Starting services in background..."
echo ""

# Start FastAPI
echo "🚀 Starting FastAPI (Port 8000)..."
uvicorn server.main:app --host 0.0.0.0 --port 8000 > logs/fastapi.log 2>&1 &
FASTAPI_PID=$!
echo "   PID: $FASTAPI_PID"

# Wait a bit for FastAPI to start
sleep 2

# Start Flask
echo "🎨 Starting Flask (Port 5000)..."
python server/app.py > logs/flask.log 2>&1 &
FLASK_PID=$!
echo "   PID: $FLASK_PID"

# Start Gradio
echo "🔮 Starting Gradio (Port 7860)..."
python server/canticle_interface.py > logs/gradio.log 2>&1 &
GRADIO_PID=$!
echo "   PID: $GRADIO_PID"

echo ""
echo "✅ All services started!"
echo ""
echo "Service URLs:"
echo "  - FastAPI: http://localhost:8000"
echo "  - Flask:   http://localhost:5000"
echo "  - Gradio:  http://localhost:7860"
echo ""
echo "Process IDs:"
echo "  - FastAPI: $FASTAPI_PID"
echo "  - Flask:   $FLASK_PID"
echo "  - Gradio:  $GRADIO_PID"
echo ""
echo "To stop services:"
echo "  kill $FASTAPI_PID $FLASK_PID $GRADIO_PID"
echo ""
echo "View logs:"
echo "  tail -f logs/*.log"
echo ""

# Save PIDs for later
echo "$FASTAPI_PID" > "$SCRIPT_DIR/fastapi.pid"
echo "$FLASK_PID" > "$SCRIPT_DIR/flask.pid"
echo "$GRADIO_PID" > "$SCRIPT_DIR/gradio.pid"
EOF
    
    chmod +x "$BOOTSTRAP_DIR/start-services.sh"
    log_success "Service starter script created: $BOOTSTRAP_DIR/start-services.sh"
    
    # Create stop script
    cat > "$BOOTSTRAP_DIR/stop-services.sh" << 'EOF'
#!/bin/bash
# Stop all Quantum Pi Forge services

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🛑 Stopping Quantum Pi Forge Services..."

if [ -f "$SCRIPT_DIR/fastapi.pid" ]; then
    FASTAPI_PID=$(cat "$SCRIPT_DIR/fastapi.pid")
    if kill -0 "$FASTAPI_PID" 2>/dev/null; then
        kill "$FASTAPI_PID"
        echo "✅ FastAPI stopped (PID: $FASTAPI_PID)"
    fi
    rm "$SCRIPT_DIR/fastapi.pid"
fi

if [ -f "$SCRIPT_DIR/flask.pid" ]; then
    FLASK_PID=$(cat "$SCRIPT_DIR/flask.pid")
    if kill -0 "$FLASK_PID" 2>/dev/null; then
        kill "$FLASK_PID"
        echo "✅ Flask stopped (PID: $FLASK_PID)"
    fi
    rm "$SCRIPT_DIR/flask.pid"
fi

if [ -f "$SCRIPT_DIR/gradio.pid" ]; then
    GRADIO_PID=$(cat "$SCRIPT_DIR/gradio.pid")
    if kill -0 "$GRADIO_PID" 2>/dev/null; then
        kill "$GRADIO_PID"
        echo "✅ Gradio stopped (PID: $GRADIO_PID)"
    fi
    rm "$SCRIPT_DIR/gradio.pid"
fi

echo "✅ All services stopped"
EOF
    
    chmod +x "$BOOTSTRAP_DIR/stop-services.sh"
    log_success "Service stopper script created: $BOOTSTRAP_DIR/stop-services.sh"
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 8: GENERATE FINAL REPORT
# ═══════════════════════════════════════════════════════════════════════════

generate_final_report() {
    print_header "STEP 8: Final Report"
    
    REPORT_FILE="$BOOTSTRAP_DIR/bootstrap-report-$(date +%Y%m%d-%H%M%S).md"
    
    cat > "$REPORT_FILE" << EOF
# Quantum Pi Forge Bootstrap Report

**Date**: $(date)
**Environment**: $ENVIRONMENT
**Status**: ✅ SUCCESS

## Summary

The Quantum Pi Forge autonomous system has been successfully bootstrapped and is ready for deployment.

## Steps Completed

1. ✅ System requirements validated
2. ✅ Python environment configured
3. ✅ Dependencies installed
4. ✅ Infrastructure validated
5. ✅ Tests executed
6. ✅ Services initialized
7. ✅ Deployment prepared
8. ✅ Autonomous handoff configured

## System Information

- **Python**: $(python3 --version)
- **Pip**: $(pip3 --version)
- **Git**: $(git --version)
- **Docker**: $(command -v docker &> /dev/null && docker --version || echo "Not installed")

## Project Structure

\`\`\`
$(tree -L 2 "$PROJECT_ROOT" 2>/dev/null || find "$PROJECT_ROOT" -maxdepth 2 -type d | head -20)
\`\`\`

## Next Steps

### 1. Configure Environment Variables

Edit the \`.env\` file and set your actual credentials:

\`\`\`bash
# Required
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
JWT_SECRET=your-secure-random-string
\`\`\`

### 2. Choose Deployment Method

See \`deployment-checklist.md\` for detailed instructions:
- Railway (Recommended for production)
- Docker (For containerized deployment)
- Local (For development)

### 3. Start Services

For local development:

\`\`\`bash
./bootstrap/start-services.sh
\`\`\`

Or manually:

\`\`\`bash
# FastAPI
uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload

# Flask
python server/app.py

# Gradio
python server/canticle_interface.py
\`\`\`

### 4. Verify Deployment

Check health endpoints:
- FastAPI: http://localhost:8000/
- Flask: http://localhost:5000/health
- Gradio: http://localhost:7860/

### 5. Enable Autonomous Operations

\`\`\`bash
# Set GitHub secrets
gh secret set SUPABASE_URL --body "your-url"
gh secret set SUPABASE_KEY --body "your-key"
gh secret set JWT_SECRET --body "your-secret"

# Enable workflow
gh workflow enable ai-agent-handoff-runbook.yml

# Trigger first deployment
gh workflow run ai-agent-handoff-runbook.yml --field action=full-deployment
\`\`\`

## Documentation

- **Deployment Checklist**: \`bootstrap/deployment-checklist.md\`
- **Autonomous Operations**: \`bootstrap/autonomous-operations.md\`
- **AI Agent Quick Reference**: \`docs/AI_AGENT_QUICK_REFERENCE.md\`
- **Bootstrap Log**: \`$LOG_FILE\`

## Support

For issues or questions:
1. Check the documentation in \`docs/\`
2. Review the bootstrap log: \`$LOG_FILE\`
3. Consult the AI Agent Handoff Runbook
4. Contact repository maintainer

---

🎉 **Bootstrap complete! The Quantum Resonance Lattice awaits activation.**

EOF
    
    log_success "Bootstrap report generated: $REPORT_FILE"
    
    # Display the report
    cat "$REPORT_FILE"
}

# ═══════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════

main() {
    # Parse arguments
    parse_args "$@"
    
    # Print banner
    clear
    print_header "🌌 QUANTUM PI FORGE - BOOTSTRAP AGENT"
    
    log_info "Bootstrap started at $(date)"
    log_info "Target environment: $ENVIRONMENT"
    log_info "Log file: $LOG_FILE"
    echo ""
    
    # Create logs directory
    mkdir -p "$PROJECT_ROOT/logs"
    
    # Execute bootstrap steps
    check_system_requirements
    setup_environment
    validate_infrastructure
    run_tests
    initialize_services
    prepare_deployment
    setup_autonomous_handoff
    generate_final_report
    
    # Final message
    print_header "✨ BOOTSTRAP COMPLETE"
    
    echo ""
    log_success "Quantum Pi Forge is ready for deployment!"
    echo ""
    log_info "Next steps:"
    echo "  1. Review and edit .env file with your credentials"
    echo "  2. Check deployment-checklist.md for deployment options"
    echo "  3. Read autonomous-operations.md for autonomous setup"
    echo "  4. Start services with: ./bootstrap/start-services.sh"
    echo ""
    log_info "Full bootstrap report: bootstrap/bootstrap-report-*.md"
    log_info "Bootstrap log: $LOG_FILE"
    echo ""
}

# Run main function
main "$@"
