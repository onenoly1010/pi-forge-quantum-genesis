#!/bin/bash
# 💾 QUANTUM RESONANCE LATTICE - STATE BACKUP SYSTEM
# Creates comprehensive backup of current deployment state

set -euo pipefail

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROLLBACK_ROOT="$(dirname "$SCRIPT_DIR")"
PROJECT_ROOT="$(dirname "$ROLLBACK_ROOT")"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_DIR="${ROLLBACK_ROOT}/backups/state-${TIMESTAMP}"

echo -e "${CYAN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║   💾 CREATING DEPLOYMENT STATE BACKUP                     ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Create backup directory
mkdir -p "$BACKUP_DIR"

echo -e "${CYAN}Backup location: $BACKUP_DIR${NC}"
echo ""

# 1. Git state
echo -e "${CYAN}[1/7] Backing up Git state...${NC}"
cd "$PROJECT_ROOT"

git rev-parse HEAD > "$BACKUP_DIR/commit-hash.txt" 2>/dev/null || echo "unknown" > "$BACKUP_DIR/commit-hash.txt"
git branch --show-current > "$BACKUP_DIR/branch-name.txt" 2>/dev/null || echo "unknown" > "$BACKUP_DIR/branch-name.txt"
git log -1 --pretty=format:"%H%n%an%n%ae%n%ai%n%s" > "$BACKUP_DIR/commit-info.txt" 2>/dev/null || true
git status > "$BACKUP_DIR/git-status.txt" 2>/dev/null || true
git diff > "$BACKUP_DIR/git-diff.txt" 2>/dev/null || true

echo -e "${GREEN}✓${NC} Git state backed up"

# 2. Configuration files
echo -e "${CYAN}[2/7] Backing up configuration files...${NC}"

[ -f "$PROJECT_ROOT/.env" ] && cp "$PROJECT_ROOT/.env" "$BACKUP_DIR/.env.backup"
[ -f "$PROJECT_ROOT/railway.toml" ] && cp "$PROJECT_ROOT/railway.toml" "$BACKUP_DIR/railway.toml.backup"
[ -f "$PROJECT_ROOT/Dockerfile" ] && cp "$PROJECT_ROOT/Dockerfile" "$BACKUP_DIR/Dockerfile.backup"
[ -f "$PROJECT_ROOT/server/requirements.txt" ] && cp "$PROJECT_ROOT/server/requirements.txt" "$BACKUP_DIR/requirements.txt.backup"

echo -e "${GREEN}✓${NC} Configuration files backed up"

# 3. Python environment info
echo -e "${CYAN}[3/7] Backing up Python environment info...${NC}"

python3 --version > "$BACKUP_DIR/python-version.txt" 2>&1 || echo "python3 not available" > "$BACKUP_DIR/python-version.txt"

if command -v pip3 &> /dev/null; then
    pip3 list --format=freeze > "$BACKUP_DIR/installed-packages.txt" 2>&1 || true
fi

echo -e "${GREEN}✓${NC} Python environment info backed up"

# 4. Service status (if running)
echo -e "${CYAN}[4/7] Capturing service status...${NC}"

if command -v lsof &> /dev/null; then
    lsof -Pi :8000 -sTCP:LISTEN > "$BACKUP_DIR/port-8000-status.txt" 2>&1 || echo "Not listening" > "$BACKUP_DIR/port-8000-status.txt"
    lsof -Pi :5000 -sTCP:LISTEN > "$BACKUP_DIR/port-5000-status.txt" 2>&1 || echo "Not listening" > "$BACKUP_DIR/port-5000-status.txt"
    lsof -Pi :7860 -sTCP:LISTEN > "$BACKUP_DIR/port-7860-status.txt" 2>&1 || echo "Not listening" > "$BACKUP_DIR/port-7860-status.txt"
fi

echo -e "${GREEN}✓${NC} Service status captured"

# 5. System information
echo -e "${CYAN}[5/7] Capturing system information...${NC}"

uname -a > "$BACKUP_DIR/system-info.txt" 2>&1 || true
df -h > "$BACKUP_DIR/disk-usage.txt" 2>&1 || true
free -h > "$BACKUP_DIR/memory-usage.txt" 2>&1 || true

echo -e "${GREEN}✓${NC} System information captured"

# 6. Logs (if available)
echo -e "${CYAN}[6/7] Backing up logs...${NC}"

if [ -d "$PROJECT_ROOT/logs" ]; then
    cp -r "$PROJECT_ROOT/logs" "$BACKUP_DIR/runtime-logs" 2>/dev/null || true
    echo -e "${GREEN}✓${NC} Runtime logs backed up"
else
    echo -e "${YELLOW}⚠${NC} No logs directory found"
fi

# 7. Create backup manifest
echo -e "${CYAN}[7/7] Creating backup manifest...${NC}"

cat > "$BACKUP_DIR/MANIFEST.txt" << EOF
QUANTUM RESONANCE LATTICE - STATE BACKUP
=========================================

Backup Timestamp: $(date '+%Y-%m-%d %H:%M:%S %Z')
Backup Location: $BACKUP_DIR

GIT INFORMATION:
- Commit Hash: $(cat "$BACKUP_DIR/commit-hash.txt")
- Branch: $(cat "$BACKUP_DIR/branch-name.txt")

CONFIGURATION FILES:
$(ls -1 "$BACKUP_DIR" | grep -E '\.(backup|txt)$' || echo "None")

BACKUP CONTENTS:
$(ls -lh "$BACKUP_DIR")

To restore from this backup:
1. Review MANIFEST.txt and commit-info.txt
2. Execute: git reset --hard $(cat "$BACKUP_DIR/commit-hash.txt")
3. Restore configuration files from .backup files
4. Restart services

=========================================
EOF

echo -e "${GREEN}✓${NC} Backup manifest created"

# Summary
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   ✅ BACKUP COMPLETE                                       ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}Backup Details:${NC}"
echo -e "  Location: ${YELLOW}$BACKUP_DIR${NC}"
echo -e "  Commit: ${YELLOW}$(cat "$BACKUP_DIR/commit-hash.txt")${NC}"
echo -e "  Branch: ${YELLOW}$(cat "$BACKUP_DIR/branch-name.txt")${NC}"
echo ""
echo -e "${CYAN}View backup manifest: cat $BACKUP_DIR/MANIFEST.txt${NC}"
echo ""
