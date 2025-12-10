# 🔧 Rollback Troubleshooting Guide

## Common Issues and Solutions

This guide covers common problems encountered during rollback operations and their solutions.

---

## Table of Contents

1. [Rollback Script Failures](#rollback-script-failures)
2. [Git Issues](#git-issues)
3. [Service Startup Failures](#service-startup-failures)
4. [Database Issues](#database-issues)
5. [Environment Configuration](#environment-configuration)
6. [Port Conflicts](#port-conflicts)
7. [Permission Issues](#permission-issues)
8. [Railway Deployment Issues](#railway-deployment-issues)

---

## Rollback Script Failures

### Issue: Script Won't Execute (Permission Denied)

**Symptoms**:
```bash
bash: ./rollback/scripts/emergency-rollback.sh: Permission denied
```

**Solution**:
```bash
# Make scripts executable
chmod +x rollback/scripts/*.sh

# Then run again
./rollback/scripts/emergency-rollback.sh --fast
```

---

### Issue: Script Fails with "Command Not Found"

**Symptoms**:
```bash
./rollback/scripts/emergency-rollback.sh: line 42: python3: command not found
```

**Solution**:
```bash
# Check if python3 is installed
which python3

# If not installed (Linux):
sudo apt-get install python3

# If not in PATH, use full path
/usr/bin/python3 --version

# Or create symlink
sudo ln -s /usr/bin/python3.11 /usr/bin/python3
```

---

### Issue: Rollback Fails with "Git Not Available"

**Symptoms**:
```
[ERROR] Git not available - cannot perform rollback
```

**Solution**:
```bash
# Verify git installation
git --version

# If not installed (Linux):
sudo apt-get install git

# Configure git (if needed)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## Git Issues

### Issue: Uncommitted Changes Block Rollback

**Symptoms**:
```
error: Your local changes to the following files would be overwritten by checkout
```

**Solution**:

**Option 1**: Let rollback script handle it (recommended)
```bash
# Script automatically stashes changes
./rollback/scripts/emergency-rollback.sh --fast
```

**Option 2**: Manual stash
```bash
# Stash changes manually
git stash push -m "Pre-rollback stash"

# Then run rollback
./rollback/scripts/emergency-rollback.sh --fast

# Later, recover stashed changes if needed
git stash pop
```

**Option 3**: Discard changes
```bash
# WARNING: This permanently deletes uncommitted changes
git reset --hard HEAD
git clean -fd

# Then run rollback
./rollback/scripts/emergency-rollback.sh --fast
```

---

### Issue: Target Commit Not Found

**Symptoms**:
```
[ERROR] Target commit abc123def does not exist!
```

**Solution**:
```bash
# Check available commits
git log --oneline -20

# Use a different commit
./rollback/scripts/emergency-rollback.sh --fast --commit <valid-hash>

# Or let script use default (HEAD~1)
./rollback/scripts/emergency-rollback.sh --fast
```

---

### Issue: Detached HEAD State

**Symptoms**:
```
You are in 'detached HEAD' state.
```

**Solution**:
```bash
# This is normal after rollback
# To continue development, checkout your branch
git checkout main

# Or create new branch from current state
git checkout -b rollback-recovery
```

---

## Service Startup Failures

### Issue: FastAPI Won't Start After Rollback

**Symptoms**:
```
ERROR: Could not import module "server.main"
ModuleNotFoundError: No module named 'fastapi'
```

**Solution**:
```bash
# Reinstall dependencies
source .venv/bin/activate  # Linux
# or
.\.venv\Scripts\Activate.ps1  # Windows

pip install -r server/requirements.txt

# Then restart
uvicorn server.main:app --host 0.0.0.0 --port 8000
```

---

### Issue: Import Errors After Rollback

**Symptoms**:
```
ModuleNotFoundError: No module named 'tracing_system'
```

**Solution**:
```bash
# Clear Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete

# Verify file exists
ls -la server/tracing_system.py

# If missing, git status to check
git status

# Reset if needed
git reset --hard <target-commit>
```

---

### Issue: Service Crashes on Startup

**Symptoms**:
```
[ERROR] Service exited with code 1
Traceback (most recent call last):
  ...
```

**Solution**:
```bash
# Check Python syntax
python3 -m py_compile server/main.py
python3 -m py_compile server/app.py

# Check for missing dependencies
pip install -r server/requirements.txt --upgrade

# Run in verbose mode to see errors
python3 -m uvicorn server.main:app --log-level debug
```

---

## Database Issues

### Issue: Supabase Connection Fails

**Symptoms**:
```
[ERROR] Could not connect to Supabase
```

**Solution**:
```bash
# 1. Verify environment variables
echo $SUPABASE_URL
echo $SUPABASE_KEY

# 2. Check .env file exists
cat .env | grep SUPABASE

# 3. Test connection manually
python3 -c "
import os
from supabase import create_client
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
client = create_client(url, key)
print('✓ Connection successful')
"

# 4. Check Supabase status
# Visit: https://status.supabase.com
```

---

### Issue: Database Schema Mismatch

**Symptoms**:
```
[ERROR] Table 'payments' does not exist
```

**Solution**:
```bash
# This usually means database rollback is needed

# Option 1: Check Supabase dashboard
# Visit: https://app.supabase.com
# Go to Table Editor and verify tables exist

# Option 2: Run database migrations forward
# (If migrations are implemented)
alembic upgrade head

# Option 3: Manual table creation
# Use Supabase SQL Editor to create missing tables
```

---

## Environment Configuration

### Issue: Missing Environment Variables

**Symptoms**:
```
KeyError: 'SUPABASE_URL'
```

**Solution**:

**Development (Local)**:
```bash
# 1. Copy example file
cp .env.example .env

# 2. Edit with your values
nano .env

# 3. Load environment (if needed)
source .env  # Linux
# or
$env:SUPABASE_URL="value"  # PowerShell
```

**Production (Railway)**:
```bash
# 1. Check Railway dashboard
# Visit: https://railway.app/dashboard

# 2. Go to your project → Variables

# 3. Add missing variables:
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-key-here

# 4. Redeploy service
```

---

### Issue: Environment Variables Not Loading

**Symptoms**:
```
os.getenv('SUPABASE_URL') returns None
```

**Solution**:
```python
# Add debug logging to check
import os
print("Environment:", os.environ)

# For Railway, variables should be automatically available
# For local, ensure using python-dotenv:

from dotenv import load_dotenv
load_dotenv()

# Verify
import os
print(os.getenv('SUPABASE_URL'))
```

---

## Port Conflicts

### Issue: Port Already in Use

**Symptoms**:
```
ERROR: [Errno 98] Address already in use
OSError: [WinError 10048] Only one usage of socket address
```

**Solution**:

**Linux**:
```bash
# Find process using port
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or kill all Python processes
pkill -f python3

# Then restart service
uvicorn server.main:app --port 8000
```

**Windows**:
```powershell
# Find process using port
Get-NetTCPConnection -LocalPort 8000

# Kill the process
Stop-Process -Id <PID> -Force

# Or use emergency script
.\scripts\emergency.ps1 -KillAll

# Then restart service
python -m uvicorn server.main:app --port 8000
```

---

## Permission Issues

### Issue: Cannot Write to Rollback Directories

**Symptoms**:
```
[ERROR] Permission denied: 'rollback/logs/rollback.log'
```

**Solution**:
```bash
# Fix permissions on rollback directory
chmod -R u+w rollback/

# Ensure directories exist
mkdir -p rollback/logs rollback/backups

# If on Linux, check ownership
ls -la rollback/
chown -R $USER:$USER rollback/
```

---

### Issue: Git Reset Fails Due to Permissions

**Symptoms**:
```
error: unable to unlink old 'server/main.py': Permission denied
```

**Solution**:

**Windows**:
```powershell
# Close any editors or processes using the files
# Check what's using files
Get-Process | Where-Object {$_.MainWindowTitle -like "*main.py*"}

# Force close
Stop-Process -Name "python" -Force
Stop-Process -Name "Code" -Force  # VS Code

# Then retry
git reset --hard <commit>
```

**Linux**:
```bash
# Check what's using files
lsof | grep main.py

# Force close processes
pkill -f python3

# Retry
git reset --hard <commit>
```

---

## Railway Deployment Issues

### Issue: Railway Deployment Fails After Rollback

**Symptoms**:
```
Build failed: dockerfile build failed
```

**Solution**:
```bash
# 1. Verify Dockerfile is valid
docker build -t test .

# 2. Check railway.toml is correct
cat railway.toml

# 3. Push changes
git push

# 4. Manually trigger redeploy in Railway dashboard
# Visit: https://railway.app/dashboard
# Click: Deployments → Redeploy
```

---

### Issue: Railway Environment Variables Missing After Rollback

**Symptoms**:
```
Deployed successfully but service crashes with missing env vars
```

**Solution**:
```bash
# Railway environment variables persist across deploys
# Check they're still set:

# 1. Visit Railway dashboard
# 2. Go to Variables tab
# 3. Verify all required variables present:
#    - SUPABASE_URL
#    - SUPABASE_KEY
#    - (others as needed)

# 4. If missing, re-add them and redeploy
```

---

### Issue: Railway Detects Wrong Start Command

**Symptoms**:
```
Railway starts wrong service or fails to start
```

**Solution**:
```bash
# Ensure railway.toml has correct start command
cat railway.toml

# Should contain:
# [deploy]
# startCommand = "cd server && uvicorn main:app --host 0.0.0.0 --port $PORT"

# If wrong, fix and commit:
git add railway.toml
git commit -m "Fix Railway start command"
git push
```

---

## Emergency Recovery

### When All Else Fails

If rollback completely fails:

1. **Manual Git Reset**:
```bash
# Nuclear option - reset everything
git fetch origin
git reset --hard origin/main
git clean -fdx  # WARNING: Deletes everything not in git
```

2. **Fresh Clone**:
```bash
# Start completely fresh
cd ..
mv pi-forge-quantum-genesis pi-forge-quantum-genesis.backup
git clone https://github.com/onenoly1010/pi-forge-quantum-genesis.git
cd pi-forge-quantum-genesis
```

3. **Railway Redeploy from Known Good Commit**:
```bash
# In Railway dashboard:
# 1. Go to Deployments
# 2. Find last known good deployment
# 3. Click "Redeploy"
```

4. **Database Restore from Backup**:
```bash
# In Supabase dashboard:
# 1. Go to Database → Backups
# 2. Select recent backup
# 3. Click "Restore"
```

---

## Getting Help

If issues persist:

1. **Check Logs**:
```bash
# Rollback logs
cat rollback/logs/rollback-*.log

# Service logs (if running locally)
journalctl -u your-service  # Linux systemd
```

2. **Create GitHub Issue**:
   - Include error messages
   - Include rollback log file
   - Describe what you tried
   - https://github.com/onenoly1010/pi-forge-quantum-genesis/issues

3. **Contact Repository Owner**:
   - @onenoly1010 (Kris Olofson)

---

© 2025 Pi Forge Collective — Quantum Genesis Initiative
