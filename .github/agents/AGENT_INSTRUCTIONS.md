# 🎯 Coding Agent Instructions - Quick Reference

**Fast Reference Guide for Task Execution**

This document provides quick-reference instructions for coding agents. For comprehensive onboarding, see [ONBOARDING.md](./ONBOARDING.md).

---

## 🚦 Before You Start

### Prerequisites Checklist

- [ ] Read [ONBOARDING.md](./ONBOARDING.md) completely
- [ ] Understand OINIO principles
- [ ] Know the Sacred Trinity architecture
- [ ] Set up local development environment
- [ ] Verified all services run locally

**⚠️ If any box is unchecked, complete onboarding first!**

---

## 🎯 Task Execution Process

### Step 1: Understand the Task

1. Read the issue or task description thoroughly
2. Identify which service(s) are affected:
   - FastAPI (`server/main.py`) - Port 8000
   - Flask (`server/app.py`) - Port 5000
   - Gradio (`server/canticle_interface.py`) - Port 7860
3. Check for dependencies or related issues
4. Verify alignment with OINIO principles

### Step 2: Plan Your Approach

1. Identify minimal changes needed
2. List files to modify
3. Plan testing strategy
4. Consider deployment impact
5. Check for breaking changes

### Step 3: Implement Changes

```bash
# 1. Create feature branch
git checkout -b feature/your-feature-name

# 2. Make your changes
# Edit files as needed

# 3. Format code
black .

# 4. Lint code
flake8 .

# 5. Run tests
pytest -v

# 6. Test locally
# Start affected service(s) and verify manually
```

### Step 4: Quality Assurance

```bash
# Run comprehensive tests
pytest --cov=server --cov-report=html

# Check coverage (must be >80%)
open htmlcov/index.html

# Verify all services still work
# FastAPI
curl http://localhost:8000/api/health

# Flask
curl http://localhost:5000/

# Manual testing of changed functionality
```

### Step 5: Documentation

1. Update docstrings for modified functions
2. Update API documentation if endpoints changed
3. Update README if setup process changed
4. Add comments for complex logic
5. Update CHANGELOG if applicable

### Step 6: Commit & Push

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: brief description of change

Detailed explanation of what changed and why.
Relates to issue #123"

# Push to remote
git push origin feature/your-feature-name

# Create pull request via GitHub UI
```

---

## 📋 Common Task Patterns

### Adding a New API Endpoint

**File:** `server/main.py`

```python
@app.get("/api/new-endpoint")
async def new_endpoint():
    """Brief description of endpoint."""
    try:
        # Implementation
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Error in new_endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

**Don't forget:**
- Add to API documentation
- Write unit tests
- Add authentication if needed
- Update OpenAPI schema

### Adding a New Flask Route

**File:** `server/app.py`

```python
@app.route('/new-route')
def new_route():
    """Brief description of route."""
    try:
        # Implementation
        return render_template('template.html', data=data)
    except Exception as e:
        logger.error(f"Error in new_route: {e}")
        return render_template('error.html', error=str(e)), 500
```

**Don't forget:**
- Create template if needed
- Add route to navigation
- Write integration tests
- Update Flask documentation

### Modifying Database Schema

**File:** `server/integrations/supabase_client.py`

```python
# 1. Update schema in Supabase dashboard
# 2. Update client code
def new_table_operation():
    """Description of operation."""
    try:
        result = supabase.table('table_name').select('*').execute()
        return result.data
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise
```

**Don't forget:**
- Document schema changes
- Update data models
- Write migration script if needed
- Test with sample data

### Adding Environment Variables

**Files:** `.env.example`, `server/config.py`

```python
# 1. Add to .env.example
NEW_CONFIG_VAR=default_value

# 2. Add to config.py
import os

NEW_CONFIG_VAR = os.getenv('NEW_CONFIG_VAR', 'default_value')

# 3. Update documentation
# Add description to README.md
```

**Don't forget:**
- Document the variable purpose
- Provide example value
- Update deployment configs
- Test with and without the variable

---

## 🧪 Testing Guidelines

### Writing Unit Tests

**File:** `tests/test_*.py`

```python
import pytest
from server.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_endpoint_success():
    """Test successful endpoint call."""
    response = client.get("/api/endpoint")
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_endpoint_error():
    """Test error handling."""
    response = client.get("/api/endpoint?invalid=param")
    assert response.status_code == 400
```

### Running Specific Tests

```bash
# Single test file
pytest tests/test_main.py -v

# Single test function
pytest tests/test_main.py::test_health_endpoint -v

# Tests matching pattern
pytest -k "health" -v

# With coverage
pytest --cov=server tests/test_main.py
```

---

## 🔍 Debugging Tips

### Local Debugging

```bash
# Run with verbose logging
LOGLEVEL=DEBUG uvicorn server.main:app --reload

# Run with Python debugger
python -m pdb server/main.py

# Check service health
curl -v http://localhost:8000/api/health

# View logs
docker-compose logs -f
```

### Common Issues

**Issue:** Port already in use
```bash
# Find process on port (Linux/Mac)
lsof -i :8000

# Kill process
kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Issue:** Module not found
```bash
# Reinstall dependencies
pip install -r server/requirements.txt

# Verify virtual environment
which python  # Should show .venv path
```

**Issue:** Database connection failed
```bash
# Test Supabase connection
python -c "import os; from supabase import create_client; client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY')); print('✅ Connected')"

# Check environment variables
cat .env | grep SUPABASE
```

---

## 🚀 Deployment Checklist

### Pre-Deployment

- [ ] All tests pass locally
- [ ] Code is formatted (black .)
- [ ] No linting errors (flake8 .)
- [ ] Coverage >80%
- [ ] Documentation updated
- [ ] Environment variables documented
- [ ] Manual testing complete
- [ ] No secrets in code

### Deployment

```bash
# 1. Merge to main branch
git checkout main
git merge feature/your-feature

# 2. Push to trigger deployment
git push origin main

# 3. Monitor deployment
# Railway: https://railway.app/project/<project-id>
# Check logs for errors

# 4. Verify production
curl https://pi-forge-quantum-genesis.railway.app/health
```

### Post-Deployment

- [ ] Health check passes
- [ ] API docs accessible
- [ ] No errors in logs
- [ ] Monitor for 15 minutes
- [ ] Update deployment status
- [ ] Notify team if needed

---

## 🛡️ Security Checklist

### Code Security

- [ ] No hardcoded secrets
- [ ] All inputs validated
- [ ] SQL injection prevented (use parameterized queries)
- [ ] XSS prevented (sanitize outputs)
- [ ] CSRF protection enabled
- [ ] Authentication on protected routes
- [ ] Rate limiting implemented
- [ ] Error messages don't expose internals

### Data Security

- [ ] User data encrypted
- [ ] Passwords hashed
- [ ] Sensitive data logged carefully
- [ ] Access controls implemented
- [ ] GDPR compliance maintained

---

## 📝 Code Style Quick Reference

### Python Style

```python
# Good
def calculate_resonance(frequency: float, amplitude: float) -> dict:
    """Calculate quantum resonance values.
    
    Args:
        frequency: Resonance frequency in Hz
        amplitude: Wave amplitude in arbitrary units
        
    Returns:
        Dictionary with resonance data
    """
    try:
        result = frequency * amplitude
        return {"resonance": result, "status": "calculated"}
    except Exception as e:
        logger.error(f"Resonance calculation failed: {e}")
        raise

# Bad
def calc(f,a):  # No types, no docstring
    return f*a  # No error handling
```

### Import Order

```python
# 1. Standard library
import os
import sys
from datetime import datetime

# 2. Third-party
from fastapi import FastAPI, HTTPException
from supabase import create_client

# 3. Local
from server.config import Config
from server.integrations.pi_network import PiNetworkClient
```

### Error Handling

```python
# Good - Specific exceptions, logging, user-friendly messages
try:
    result = process_payment(amount)
except ValueError as e:
    logger.warning(f"Invalid payment amount: {e}")
    raise HTTPException(status_code=400, detail="Invalid amount")
except Exception as e:
    logger.error(f"Payment processing failed: {e}")
    raise HTTPException(status_code=500, detail="Payment failed")

# Bad - Bare except, no logging
try:
    result = process_payment(amount)
except:
    return {"error": "something went wrong"}
```

---

## 🌀 Canon of Closure - Quick Steps

Every task follows these 10 steps:

1. **🧹 Lint** - `black . && flake8 .`
2. **🏠 Host** - `source .venv/bin/activate`
3. **🧪 Test** - `pytest -v`
4. **📊 Pre-aggregate** - `docker-compose up -d`
5. **📦 Release** - `git tag -a v1.0.0 -m "Release"`
6. **🚀 Deploy** - `git push origin main`
7. **🔄 Rollback** - `./deploy.sh production --rollback` (if needed)
8. **📡 Monitor** - Check logs & metrics
9. **📈 Visualize** - Review dashboards
10. **🚨 Alert** - Verify alerts work

**The circle never ends. Each completion is a new beginning.**

---

## 🤖 Agent Handoff Template

When handing off to another agent:

```markdown
## Handoff to [Agent Name]

### Summary
- ✅ Completed: [List completed items]
- ⏳ In Progress: [List in-progress items]
- ❌ Blocked: [List blockers]

### Next Steps
1. [Clear action item]
2. [Clear action item]
3. [Clear action item]

### Files Modified
- `path/to/file1.py` - [Description of changes]
- `path/to/file2.py` - [Description of changes]

### Canon Alignment
- Sovereignty: [How changes maintain autonomy]
- Transparency: [How changes are documented]
- Safety: [How changes maintain security]

### Continuity Notes
[Any context needed for someone else to continue]

### Related Issues
- #123 - [Brief description]
- #456 - [Brief description]
```

---

## 📚 Essential Links

### Documentation
- [ONBOARDING.md](./ONBOARDING.md) - Full onboarding guide
- [GENESIS.md](../../GENESIS.md) - Foundational principles
- [README.md](../../README.md) - Technical overview
- [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md) - System architecture
- [docs/API.md](../../docs/API.md) - API reference
- [docs/DEV_REFERENCE.md](../../docs/DEV_REFERENCE.md) - Command reference
- [docs/CANON_OF_CLOSURE.md](../../docs/CANON_OF_CLOSURE.md) - Development methodology

### Live Services
- Production API: https://pi-forge-quantum-genesis.railway.app
- API Docs: https://pi-forge-quantum-genesis.railway.app/docs
- Health Check: https://pi-forge-quantum-genesis.railway.app/health
- Public Site: https://onenoly1010.github.io/quantum-pi-forge-site/

### Development
- Repository: https://github.com/onenoly1010/pi-forge-quantum-genesis
- Issues: https://github.com/onenoly1010/pi-forge-quantum-genesis/issues
- Pull Requests: https://github.com/onenoly1010/pi-forge-quantum-genesis/pulls

---

## 🆘 Need Help?

### When to Escalate

Escalate to the GitHub Agent when:
- Canon alignment is unclear
- Breaking changes are needed
- Cross-repository coordination required
- Security concerns arise
- Architecture decisions needed

### How to Escalate

1. Comment on the issue with `@github-agent`
2. Clearly describe the question or blocker
3. Provide context and attempted solutions
4. Wait for response before proceeding

---

## ✅ Pre-Commit Checklist

Before every commit:

- [ ] Code formatted (`black .`)
- [ ] No linting errors (`flake8 .`)
- [ ] All tests pass (`pytest -v`)
- [ ] Coverage >80% (`pytest --cov=server`)
- [ ] Documentation updated
- [ ] No secrets in code
- [ ] Manual testing complete
- [ ] Commit message descriptive

---

## 🎉 Quick Start Commands

```bash
# One-time setup
git clone https://github.com/onenoly1010/pi-forge-quantum-genesis.git
cd pi-forge-quantum-genesis
python -m venv .venv
source .venv/bin/activate
pip install -r server/requirements.txt
cp .env.example .env

# Daily workflow
source .venv/bin/activate                    # Activate environment
git pull origin main                         # Get latest
git checkout -b feature/my-feature          # Create branch
# ... make changes ...
black . && flake8 .                         # Format & lint
pytest -v                                    # Test
git add . && git commit -m "feat: ..."     # Commit
git push origin feature/my-feature          # Push

# Before committing
black .                                      # Format
flake8 .                                     # Lint
pytest --cov=server                         # Test with coverage
uvicorn server.main:app --reload            # Test locally
```

---

**Keep this guide handy. Refer to it before, during, and after every task.**

**Remember:** Follow the Canon, maintain quality, align with OINIO principles.

**Powered by OINIO | Where Consciousness Meets Code** 🌌

*Version 1.0 | Last Updated: 2026-02-04*
