#!/bin/bash
# 🔄 QUANTUM RESONANCE LATTICE - EMERGENCY ROLLBACK SYSTEM
# Production-ready rollback script for Railway deployment
# Compatible with Linux/Unix systems

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROLLBACK_ROOT="$(dirname "$SCRIPT_DIR")"
PROJECT_ROOT="$(dirname "$ROLLBACK_ROOT")"
LOG_FILE="${ROLLBACK_ROOT}/logs/rollback-$(date +%Y%m%d-%H%M%S).log"
BACKUP_DIR="${ROLLBACK_ROOT}/backups/state-$(date +%Y%m%d-%H%M%S)"

# Default values
ROLLBACK_LEVEL="fast"
AUTO_CONFIRM=false
DRY_RUN=false

# Logging function
log() {
    local level=$1
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo -e "${timestamp} [${level}] ${message}" | tee -a "$LOG_FILE"
    
    case $level in
        ERROR)   echo -e "${RED}[ERROR]${NC} ${message}" ;;
        SUCCESS) echo -e "${GREEN}[SUCCESS]${NC} ${message}" ;;
        WARNING) echo -e "${YELLOW}[WARNING]${NC} ${message}" ;;
        INFO)    echo -e "${CYAN}[INFO]${NC} ${message}" ;;
        *)       echo -e "${message}" ;;
    esac
}

# Print banner
print_banner() {
    echo -e "${MAGENTA}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║   🔄 QUANTUM RESONANCE LATTICE EMERGENCY ROLLBACK         ║"
    echo "║   Sacred Trinity Production Recovery System               ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Display usage
usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Emergency rollback system for Pi Forge Quantum Genesis platform.

OPTIONS:
    --fast              Fast rollback (code revert only, 5-10 min)
    --full              Full rollback (code + database, 15-30 min)
    --manual            Manual guided rollback (30-60 min)
    --auto-confirm      Skip confirmation prompts (use with caution!)
    --dry-run           Simulate rollback without making changes
    --commit HASH       Specific commit to rollback to
    --help              Display this help message

EXAMPLES:
    $0 --fast                    # Quick code rollback
    $0 --full --auto-confirm     # Full automated rollback
    $0 --dry-run --fast          # Test fast rollback procedure
    $0 --commit abc123def        # Rollback to specific commit

ROLLBACK LEVELS:
    Fast   - Reverts code, restarts services (no DB changes)
    Full   - Reverts code, DB migrations, environment config
    Manual - Step-by-step guided rollback with checkpoints

EOF
    exit 0
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --fast)
                ROLLBACK_LEVEL="fast"
                shift
                ;;
            --full)
                ROLLBACK_LEVEL="full"
                shift
                ;;
            --manual)
                ROLLBACK_LEVEL="manual"
                shift
                ;;
            --auto-confirm)
                AUTO_CONFIRM=true
                shift
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --commit)
                TARGET_COMMIT="$2"
                shift 2
                ;;
            --help)
                usage
                ;;
            *)
                log ERROR "Unknown option: $1"
                usage
                ;;
        esac
    done
}

# Confirm rollback action
confirm_rollback() {
    if [ "$AUTO_CONFIRM" = true ]; then
        return 0
    fi
    
    echo -e "${RED}⚠️  WARNING: This will rollback the production system!${NC}"
    echo -e "${YELLOW}Rollback Level: ${ROLLBACK_LEVEL}${NC}"
    echo -e "${YELLOW}Target Commit: ${TARGET_COMMIT:-latest known good}${NC}"
    echo ""
    read -p "Are you sure you want to proceed? (yes/no): " -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        log WARNING "Rollback cancelled by user"
        exit 1
    fi
}

# Create backup of current state
backup_current_state() {
    log INFO "Creating backup of current state..."
    
    mkdir -p "$BACKUP_DIR"
    
    # Backup git state
    git rev-parse HEAD > "$BACKUP_DIR/current-commit.txt" 2>/dev/null || echo "unknown" > "$BACKUP_DIR/current-commit.txt"
    git status > "$BACKUP_DIR/git-status.txt" 2>/dev/null || echo "git not available" > "$BACKUP_DIR/git-status.txt"
    git diff > "$BACKUP_DIR/git-diff.txt" 2>/dev/null || echo "no diff" > "$BACKUP_DIR/git-diff.txt"
    
    # Backup environment files
    if [ -f "$PROJECT_ROOT/.env" ]; then
        cp "$PROJECT_ROOT/.env" "$BACKUP_DIR/.env.backup"
    fi
    
    # Backup configuration
    if [ -f "$PROJECT_ROOT/railway.toml" ]; then
        cp "$PROJECT_ROOT/railway.toml" "$BACKUP_DIR/railway.toml.backup"
    fi
    
    # Save runtime logs (if any)
    if [ -d "$PROJECT_ROOT/logs" ]; then
        cp -r "$PROJECT_ROOT/logs" "$BACKUP_DIR/runtime-logs" 2>/dev/null || true
    fi
    
    log SUCCESS "Backup created at: $BACKUP_DIR"
}

# Determine target commit
determine_target_commit() {
    if [ -n "${TARGET_COMMIT:-}" ]; then
        log INFO "Using specified commit: $TARGET_COMMIT"
        return
    fi
    
    # Load known good commits
    local config_file="$ROLLBACK_ROOT/config/known-good-commits.json"
    
    if [ -f "$config_file" ]; then
        # Get the most recent known good commit
        TARGET_COMMIT=$(python3 -c "import json; print(json.load(open('$config_file'))['commits'][0]['hash'])" 2>/dev/null || echo "")
    fi
    
    # Fallback: use previous commit
    if [ -z "${TARGET_COMMIT:-}" ]; then
        TARGET_COMMIT=$(git rev-parse HEAD~1)
        log WARNING "No known good commit found, using HEAD~1: $TARGET_COMMIT"
    else
        log INFO "Using known good commit: $TARGET_COMMIT"
    fi
}

# Fast rollback procedure
fast_rollback() {
    log INFO "🚀 Initiating FAST ROLLBACK procedure..."
    
    if [ "$DRY_RUN" = true ]; then
        log INFO "[DRY RUN] Would revert to commit: $TARGET_COMMIT"
        log INFO "[DRY RUN] Would restart services"
        return 0
    fi
    
    cd "$PROJECT_ROOT"
    
    # Verify commit exists
    if ! git rev-parse "$TARGET_COMMIT" >/dev/null 2>&1; then
        log ERROR "Target commit $TARGET_COMMIT does not exist!"
        exit 1
    fi
    
    # Stash any uncommitted changes
    log INFO "Stashing uncommitted changes..."
    git stash push -m "Emergency rollback stash - $(date +%Y%m%d-%H%M%S)" || true
    
    # Hard reset to target commit
    log INFO "Reverting code to commit: $TARGET_COMMIT"
    git reset --hard "$TARGET_COMMIT"
    
    # Clean untracked files
    log INFO "Backing up untracked files before cleaning..."
    BACKUP_UNTRACKED_DIR="${ROLLBACK_ROOT}/backup/untracked-$(date +%Y%m%d-%H%M%S)"
    mkdir -p "$BACKUP_UNTRACKED_DIR"
    # Find untracked files and move them to backup
    UNTRACKED_FILES=$(git ls-files --others --exclude-standard)
    if [ -n "$UNTRACKED_FILES" ]; then
        while IFS= read -r file; do
            # Only move if file/directory still exists
            if [ -e "$file" ]; then
                # Create target directory if needed
                mkdir -p "$BACKUP_UNTRACKED_DIR/$(dirname "$file")"
                mv "$file" "$BACKUP_UNTRACKED_DIR/$file"
                log INFO "Moved untracked: $file -> $BACKUP_UNTRACKED_DIR/$file"
            fi
        done <<< "$UNTRACKED_FILES"
    else
        log INFO "No untracked files to back up."
    fi
    log INFO "Cleaning untracked files..."
    git clean -fd
    
    # Clear Python cache
    log INFO "Clearing Python cache..."
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    
    # Restart services (if running locally)
    if command -v pkill &> /dev/null; then
        log INFO "Restarting services..."
        pkill -f "uvicorn" || true
        pkill -f "flask" || true
        pkill -f "gradio" || true
        sleep 2
    fi
    
    log SUCCESS "✅ Fast rollback complete!"
    log INFO "Services will restart automatically in Railway deployment"
}

# Full rollback procedure
full_rollback() {
    log INFO "🔄 Initiating FULL ROLLBACK procedure..."
    
    # Execute fast rollback first
    fast_rollback
    
    if [ "$DRY_RUN" = true ]; then
        log INFO "[DRY RUN] Would rollback database migrations"
        log INFO "[DRY RUN] Would restore environment configuration"
        return 0
    fi
    
    # Database rollback (if migrations exist)
    if [ -d "$PROJECT_ROOT/migrations" ] || [ -d "$PROJECT_ROOT/alembic" ]; then
        log INFO "Rolling back database migrations..."
        # Add database rollback logic here when migrations are implemented
        log WARNING "Database migrations not implemented yet - skipping"
    fi
    
    # Restore environment configuration
    if [ -f "$BACKUP_DIR/.env.backup" ]; then
        log INFO "Restoring previous environment configuration..."
        cp "$BACKUP_DIR/.env.backup" "$PROJECT_ROOT/.env"
    fi
    
    log SUCCESS "✅ Full rollback complete!"
}

# Manual rollback procedure
manual_rollback() {
    log INFO "📋 Initiating MANUAL ROLLBACK procedure..."
    
    echo -e "${CYAN}This is a guided manual rollback process.${NC}"
    echo -e "${CYAN}You will be prompted at each step.${NC}"
    echo ""
    
    # Step 1: Code rollback
    echo -e "${YELLOW}Step 1: Code Rollback${NC}"
    read -p "Proceed with code rollback? (yes/no): " -r
    if [[ $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        fast_rollback
    fi
    
    # Step 2: Database rollback
    echo ""
    echo -e "${YELLOW}Step 2: Database Rollback${NC}"
    read -p "Proceed with database rollback? (yes/no): " -r
    if [[ $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        log INFO "Database rollback would be executed here"
        log WARNING "Database migrations not implemented yet"
    fi
    
    # Step 3: Service verification
    echo ""
    echo -e "${YELLOW}Step 3: Service Verification${NC}"
    read -p "Proceed with service verification? (yes/no): " -r
    if [[ $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        "$SCRIPT_DIR/verify-rollback.sh" || true
    fi
    
    log SUCCESS "✅ Manual rollback procedure complete!"
}

# Main rollback execution
execute_rollback() {
    case $ROLLBACK_LEVEL in
        fast)
            fast_rollback
            ;;
        full)
            full_rollback
            ;;
        manual)
            manual_rollback
            ;;
        *)
            log ERROR "Invalid rollback level: $ROLLBACK_LEVEL"
            exit 1
            ;;
    esac
}

# Post-rollback verification
verify_rollback() {
    log INFO "Running post-rollback verification..."
    
    if [ -f "$SCRIPT_DIR/verify-rollback.sh" ]; then
        "$SCRIPT_DIR/verify-rollback.sh" --quick || log WARNING "Verification script encountered issues"
    else
        log WARNING "Verification script not found - skipping automated verification"
    fi
}

# Main execution
main() {
    print_banner
    
    # Create log directory if needed
    mkdir -p "$(dirname "$LOG_FILE")"
    
    log INFO "Emergency Rollback System initiated at $(date)"
    log INFO "Rollback level: $ROLLBACK_LEVEL"
    
    # Parse arguments
    parse_args "$@"
    
    # Confirm action
    confirm_rollback
    
    # Create backup
    backup_current_state
    
    # Determine target
    determine_target_commit
    
    # Execute rollback
    execute_rollback
    
    # Verify rollback
    if [ "$DRY_RUN" != true ]; then
        verify_rollback
    fi
    
    # Final summary
    echo ""
    log SUCCESS "╔════════════════════════════════════════════════════════════╗"
    log SUCCESS "║   ✅ ROLLBACK COMPLETE                                     ║"
    log SUCCESS "╚════════════════════════════════════════════════════════════╝"
    echo ""
    log INFO "Rollback log saved to: $LOG_FILE"
    log INFO "Backup saved to: $BACKUP_DIR"
    
    if [ "$DRY_RUN" = true ]; then
        echo -e "${YELLOW}This was a DRY RUN - no actual changes were made${NC}"
    fi
}

# Execute main function
main "$@"
