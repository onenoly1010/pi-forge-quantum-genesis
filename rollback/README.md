# 🔄 Quantum Resonance Lattice - Emergency Rollback System

## Overview

The Emergency Rollback System provides comprehensive procedures and automated scripts for quickly reverting the Pi Forge Quantum Genesis platform to a known stable state in case of deployment failures, critical bugs, or system instability.

## 🎯 Quick Start

### Immediate Emergency Rollback (Railway Production)

```bash
# Linux/Railway Production
./rollback/scripts/emergency-rollback.sh --fast

# Windows Development
.\rollback\scripts\emergency-rollback.ps1 -Fast
```

### Full Controlled Rollback

```bash
# Linux/Railway Production
./rollback/scripts/emergency-rollback.sh --full

# Windows Development
.\rollback\scripts\emergency-rollback.ps1 -Full
```

## 📁 Directory Structure

```
rollback/
├── README.md                          # This file - Main documentation
├── scripts/                           # Executable rollback scripts
│   ├── emergency-rollback.sh          # Main Linux/Railway rollback script
│   ├── emergency-rollback.ps1         # Main Windows rollback script
│   ├── rollback-fastapi.sh            # FastAPI service rollback
│   ├── rollback-flask.sh              # Flask service rollback
│   ├── rollback-gradio.sh             # Gradio service rollback
│   ├── rollback-database.sh           # Database state rollback
│   ├── verify-rollback.sh             # Post-rollback verification
│   └── backup-current-state.sh        # Create deployment snapshot
├── docs/                              # Detailed documentation
│   ├── ROLLBACK_PROCEDURES.md         # Step-by-step rollback guide
│   ├── SERVICE_DEPENDENCIES.md        # Service dependency map
│   ├── TROUBLESHOOTING.md             # Common issues and solutions
│   └── AUTONOMOUS_HANDOFF.md          # Autonomous agent handoff guide
├── config/                            # Rollback configuration
│   ├── rollback-config.json           # Main configuration
│   ├── known-good-commits.json        # Verified stable commits
│   └── service-endpoints.json         # Service health check endpoints
├── logs/                              # Rollback execution logs
│   └── .gitkeep                       # Keep directory in git
└── backups/                           # State backups
    └── .gitkeep                       # Keep directory in git
```

## 🚨 When to Use Emergency Rollback

### Critical Situations (Use Immediately)

- ❌ **Production service completely down** (HTTP 5xx errors)
- ❌ **Database connection failures** affecting all users
- ❌ **Authentication system broken** (no users can login)
- ❌ **Payment processing failures** (Pi Network integration broken)
- ❌ **WebSocket streaming failures** (real-time features dead)
- ❌ **Security vulnerability detected** in deployed code

### Non-Critical Situations (Investigate First)

- ⚠️ Performance degradation (but service functional)
- ⚠️ Single feature not working (core functionality intact)
- ⚠️ UI rendering issues (but API functional)
- ⚠️ Individual user reports (not widespread)

## 🛠️ Rollback Levels

### Level 1: Fast Rollback (5-10 minutes)

**What it does:**
- Reverts git repository to last known good commit
- Restarts all services with previous codebase
- Maintains database state (no data loss)
- Clears application caches

**When to use:**
- Recent deployment broke critical functionality
- Need to restore service immediately
- Database changes are minimal or non-breaking

**Command:**
```bash
./rollback/scripts/emergency-rollback.sh --fast
```

### Level 2: Full Rollback (15-30 minutes)

**What it does:**
- Everything in Fast Rollback, PLUS:
- Rolls back database migrations
- Restores previous environment configuration
- Validates all service health checks
- Creates detailed rollback report

**When to use:**
- Database schema changes caused issues
- Environment variable changes broke services
- Need comprehensive system restoration
- Fast rollback didn't fully resolve issues

**Command:**
```bash
./rollback/scripts/emergency-rollback.sh --full
```

### Level 3: Manual Rollback (30-60 minutes)

**What it does:**
- Guided manual intervention with checklist
- Custom database restoration procedures
- Service-by-service rollback with validation
- Detailed incident documentation

**When to use:**
- Automated rollback failed
- Complex multi-service deployment
- Data integrity concerns
- Requires human judgment

**Command:**
```bash
./rollback/scripts/emergency-rollback.sh --manual
```

## 📋 Pre-Rollback Checklist

Before executing rollback, verify:

1. **Confirm Issue Severity**
   - [ ] Production services are affected
   - [ ] Issue cannot be hotfixed quickly
   - [ ] Rollback is safer than forward fix

2. **Identify Target State**
   - [ ] Know which commit/version to roll back to
   - [ ] Verify target version is in `known-good-commits.json`
   - [ ] Check Railway deployment history

3. **Communicate Status**
   - [ ] Notify team of rollback initiation
   - [ ] Update status page (if applicable)
   - [ ] Document incident in logs

4. **Backup Current State**
   - [ ] Run `backup-current-state.sh` first
   - [ ] Capture current environment variables
   - [ ] Document error messages/symptoms

## 🔍 Post-Rollback Verification

After rollback completes:

1. **Service Health Checks**
   ```bash
   ./rollback/scripts/verify-rollback.sh
   ```

2. **Manual Verification**
   - [ ] FastAPI: `https://your-app.railway.app/`
   - [ ] Flask Dashboard: `https://your-app.railway.app/health`
   - [ ] Gradio Interface: `https://your-app.railway.app:7860`
   - [ ] WebSocket: Test real-time streaming
   - [ ] Authentication: Test login/register
   - [ ] Pi Network: Test payment flow (sandbox mode)

3. **Data Integrity**
   - [ ] Verify recent transactions preserved
   - [ ] Check user data intact
   - [ ] Validate audit logs

## 🎓 Autonomous Agent Handoff

For autonomous AI agents managing deployments:

### Rollback Decision Tree

```
Is service completely down?
├─ YES → Execute Fast Rollback immediately
└─ NO → Is critical functionality broken?
    ├─ YES → Evaluate rollback necessity
    │   ├─ Can be hotfixed in <15 min? → Attempt hotfix
    │   └─ Otherwise → Execute Fast Rollback
    └─ NO → Continue monitoring, no rollback needed
```

### Agent Execution Pattern

```bash
# 1. Assess situation
./rollback/scripts/verify-rollback.sh --check-only

# 2. Backup current state
./rollback/scripts/backup-current-state.sh

# 3. Execute rollback
./rollback/scripts/emergency-rollback.sh --fast --auto-confirm

# 4. Verify restoration
./rollback/scripts/verify-rollback.sh

# 5. Document incident
echo "Rollback executed at $(date): [REASON]" >> rollback/logs/rollback-history.log
```

## 🔗 Related Documentation

- **Deployment Guide**: `docs/PRODUCTION_DEPLOYMENT.md`
- **Sacred Trinity Tracing**: `docs/SACRED_TRINITY_TRACING.md`
- **Server Status Report**: `docs/SERVER_STATUS_REPORT.md`
- **Docker Development**: `docs/DOCKER_DEVELOPMENT_GUIDE.md`

## 📞 Emergency Contacts

When rollback fails or manual intervention needed:

1. **Repository Owner**: @onenoly1010 (Kris Olofson)
2. **GitHub Issues**: https://github.com/onenoly1010/pi-forge-quantum-genesis/issues
3. **Railway Dashboard**: https://railway.app/dashboard

## ⚙️ Configuration

Edit `rollback/config/rollback-config.json` to customize:

- Known good commit hashes
- Service health check endpoints
- Rollback timeout values
- Notification webhooks

## 🧪 Testing Rollback Scripts

**IMPORTANT**: Test rollback procedures in development environment first!

```bash
# Create test branch
git checkout -b test-rollback

# Simulate failure
# (make breaking changes)

# Test rollback
./rollback/scripts/emergency-rollback.sh --fast --dry-run

# Verify functionality restored
./rollback/scripts/verify-rollback.sh
```

## 📊 Rollback Success Metrics

Track rollback effectiveness:

- **Mean Time to Rollback (MTTR)**: Target <10 minutes
- **Rollback Success Rate**: Target >95%
- **Data Loss Events**: Target 0
- **False Positive Rollbacks**: Minimize unnecessary rollbacks

## 🚀 Continuous Improvement

After each rollback incident:

1. Document root cause in `rollback/logs/`
2. Update `known-good-commits.json` if needed
3. Review and improve rollback procedures
4. Update this documentation with lessons learned

---

## License

© 2025 Pi Forge Collective — Quantum Genesis Initiative  
Licensed under the project's main license terms
