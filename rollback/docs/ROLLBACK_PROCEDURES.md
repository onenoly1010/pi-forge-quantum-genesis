# 📋 Rollback Procedures - Detailed Guide

## Table of Contents

1. [Pre-Rollback Assessment](#pre-rollback-assessment)
2. [Fast Rollback Procedure](#fast-rollback-procedure)
3. [Full Rollback Procedure](#full-rollback-procedure)
4. [Manual Rollback Procedure](#manual-rollback-procedure)
5. [Post-Rollback Verification](#post-rollback-verification)
6. [Incident Documentation](#incident-documentation)

---

## Pre-Rollback Assessment

### Step 1: Confirm the Issue

Before initiating a rollback, verify:

- [ ] The issue is production-critical (affects user experience)
- [ ] The issue is not a temporary network/infrastructure problem
- [ ] The issue occurred after a recent deployment
- [ ] A simple hotfix is not feasible within 15 minutes

### Step 2: Identify Scope

Determine what broke:

- **Service completely down?** → Fast rollback recommended
- **Database issues?** → Full rollback may be needed
- **Partial functionality broken?** → Consider hotfix first
- **Security vulnerability?** → Immediate rollback required

### Step 3: Communicate

1. Notify team members of the issue
2. Document symptoms and error messages
3. Note the time the issue was first detected
4. Determine estimated user impact

### Step 4: Identify Target State

Find the last known good commit:

```bash
# Check recent commits
git log --oneline -10

# Check known good commits registry
cat rollback/config/known-good-commits.json

# Check Railway deployment history
# Visit: https://railway.app/dashboard
```

---

## Fast Rollback Procedure

**Duration**: 5-10 minutes  
**Database Changes**: None  
**Risk Level**: Low  

### When to Use

- Recent deployment broke critical functionality
- Need immediate service restoration
- No database schema changes in recent deployment
- Code-level issues only

### Execution Steps

#### Linux/Railway (Production)

```bash
# 1. Navigate to project root
cd /path/to/pi-forge-quantum-genesis

# 2. Execute fast rollback
./rollback/scripts/emergency-rollback.sh --fast

# 3. Confirm when prompted
# Type: yes

# 4. Wait for completion (5-10 minutes)
```

#### Windows (Development)

```powershell
# 1. Navigate to project root
cd C:\path\to\pi-forge-quantum-genesis

# 2. Execute fast rollback
.\rollback\scripts\emergency-rollback.ps1 -Fast

# 3. Confirm when prompted
# Type: yes

# 4. Wait for completion (5-10 minutes)
```

### What Happens

1. **Backup**: Current state saved to `rollback/backups/`
2. **Git Reset**: Code reverted to target commit
3. **Cache Clear**: Python cache and temporary files removed
4. **Service Restart**: All services restarted (automatic in Railway)
5. **Verification**: Basic health checks executed

### Expected Output

```
╔════════════════════════════════════════════════════════════╗
║   🔄 QUANTUM RESONANCE LATTICE EMERGENCY ROLLBACK         ║
║   Sacred Trinity Production Recovery System               ║
╚════════════════════════════════════════════════════════════╝

[INFO] Emergency Rollback System initiated at 2025-12-10 17:39:00
[INFO] Rollback level: fast
⚠️  WARNING: This will rollback the production system!
Rollback Level: fast
Target Commit: 0bf9c64

Are you sure you want to proceed? (yes/no): yes

[INFO] Creating backup of current state...
[SUCCESS] Backup created at: /path/to/rollback/backups/state-20251210-173900
[INFO] Using known good commit: 0bf9c64
[INFO] 🚀 Initiating FAST ROLLBACK procedure...
[INFO] Stashing uncommitted changes...
[INFO] Reverting code to commit: 0bf9c64
[INFO] Cleaning untracked files...
[INFO] Clearing Python cache...
[SUCCESS] ✅ Fast rollback complete!
[INFO] Running post-rollback verification...

╔════════════════════════════════════════════════════════════╗
║   ✅ ROLLBACK COMPLETE                                     ║
╚════════════════════════════════════════════════════════════╝
```

---

## Full Rollback Procedure

**Duration**: 15-30 minutes  
**Database Changes**: Yes (migrations rolled back)  
**Risk Level**: Medium  

### When to Use

- Database schema changes caused issues
- Environment configuration changes broke services
- Fast rollback didn't fully resolve the issue
- Need comprehensive restoration

### Execution Steps

#### Linux/Railway (Production)

```bash
# 1. Execute full rollback
./rollback/scripts/emergency-rollback.sh --full

# 2. Confirm database rollback when prompted
```

#### Windows (Development)

```powershell
# 1. Execute full rollback
.\rollback\scripts\emergency-rollback.ps1 -Full

# 2. Confirm database rollback when prompted
```

### What Happens

Everything in Fast Rollback, PLUS:

1. **Database Migrations**: Reverted to previous schema version
2. **Environment Config**: Previous `.env` settings restored
3. **Extended Verification**: Database integrity checks
4. **Detailed Logging**: Comprehensive rollback report generated

### Database Rollback Details

**Note**: Database migration rollback is currently a placeholder. When migrations are implemented:

```bash
# Alembic-based rollback (future)
alembic downgrade -1  # Rollback one migration
alembic downgrade <revision>  # Rollback to specific version
```

---

## Manual Rollback Procedure

**Duration**: 30-60 minutes  
**Database Changes**: As needed (guided)  
**Risk Level**: Low (requires human approval at each step)  

### When to Use

- Automated rollback failed
- Complex deployment with multiple interdependent changes
- Data integrity concerns require careful review
- Need to rollback only specific components

### Execution Steps

```bash
# Linux/Railway
./rollback/scripts/emergency-rollback.sh --manual

# Windows
.\rollback\scripts\emergency-rollback.ps1 -Manual
```

### Interactive Prompts

You will be prompted at each step:

1. **Code Rollback**: Confirm git reset to target commit
2. **Database Rollback**: Confirm database migration rollback
3. **Service Verification**: Confirm running health checks
4. **Data Validation**: Manual inspection of critical data

Type `yes` to proceed with each step, or `no` to skip.

### Manual Intervention Points

During manual rollback, you can:

- Inspect database state before rolling back
- Verify specific data records
- Test individual services before full restart
- Create custom database backups
- Selectively restore configuration files

---

## Post-Rollback Verification

After rollback completes, verify system health:

### Automated Verification

```bash
# Linux/Railway
./rollback/scripts/verify-rollback.sh

# Windows
.\rollback\scripts\verify-rollback.ps1
```

### Manual Verification Checklist

#### Service Health

- [ ] FastAPI responds at `/` endpoint
- [ ] Flask responds at `/health` endpoint
- [ ] Gradio interface loads successfully
- [ ] WebSocket connections work
- [ ] No error logs in console

#### Authentication

- [ ] User registration works
- [ ] User login works
- [ ] JWT tokens generated correctly
- [ ] Protected endpoints require auth

#### Core Features

- [ ] Dashboard visualization renders
- [ ] Payment processing functional (sandbox mode)
- [ ] Audit interface accessible
- [ ] Real-time streaming works

#### Data Integrity

- [ ] Recent user data intact
- [ ] Transaction records preserved
- [ ] Audit logs complete
- [ ] No orphaned records

### Production Testing

```bash
# Test FastAPI health
curl https://your-app.railway.app/

# Test Flask health
curl https://your-app.railway.app/health

# Expected response: 200 OK with JSON health data
```

---

## Incident Documentation

After rollback, document the incident:

### Create Incident Report

```bash
# Create new incident file
nano rollback/logs/incident-$(date +%Y%m%d).md
```

### Incident Report Template

```markdown
# Rollback Incident Report

**Date**: 2025-12-10  
**Time**: 17:39 UTC  
**Severity**: Critical / High / Medium / Low  
**Rollback Type**: Fast / Full / Manual  

## Issue Description

[Describe what went wrong]

## Symptoms

- Error messages observed
- Services affected
- User impact
- Time of first detection

## Root Cause

[Describe what caused the issue]

## Rollback Details

- **Target Commit**: [commit hash]
- **Previous Commit**: [commit hash]
- **Duration**: [X minutes]
- **Data Loss**: Yes / No
- **User Impact Duration**: [X minutes]

## Verification Results

- [ ] All services healthy
- [ ] Authentication working
- [ ] Core features functional
- [ ] Data integrity confirmed

## Preventive Measures

[How to prevent this in the future]

## Action Items

- [ ] Update deployment checklist
- [ ] Add new test coverage
- [ ] Improve monitoring
- [ ] Update documentation

## Timeline

- **17:30** - Deployment initiated
- **17:35** - Issue detected
- **17:36** - Rollback decision made
- **17:37** - Rollback initiated
- **17:42** - Rollback complete
- **17:45** - Verification complete
- **17:50** - All systems normal

## Lessons Learned

[Key takeaways from this incident]
```

### Update Known Good Commits

After verifying the rollback target is stable:

```bash
# Edit known good commits
nano rollback/config/known-good-commits.json

# Add the verified commit to the list
# Commit and push the update
git add rollback/config/known-good-commits.json
git commit -m "Update known good commits after rollback verification"
git push
```

---

## Emergency Contacts

If rollback fails or you need assistance:

1. **Repository Owner**: @onenoly1010 (Kris Olofson)
2. **GitHub Issues**: https://github.com/onenoly1010/pi-forge-quantum-genesis/issues
3. **Railway Support**: https://railway.app/help

---

## Additional Resources

- **Main Rollback Documentation**: `rollback/README.md`
- **Service Dependencies**: `rollback/docs/SERVICE_DEPENDENCIES.md`
- **Troubleshooting Guide**: `rollback/docs/TROUBLESHOOTING.md`
- **Production Deployment**: `docs/PRODUCTION_DEPLOYMENT.md`

---

© 2025 Pi Forge Collective — Quantum Genesis Initiative
