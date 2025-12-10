# 🌌 Quantum Pi Forge Bootstrap Agent

## Overview

The Bootstrap Agent is a comprehensive initialization system that sets up the entire Quantum Pi Forge autonomous infrastructure on fresh systems. It automates environment setup, dependency installation, validation, and deployment preparation, enabling rapid system initialization with minimal manual intervention.

## Features

✅ **Cross-Platform Support** - Works on Linux, macOS, and Windows
✅ **Automated Setup** - One command to initialize entire system
✅ **Comprehensive Validation** - Checks all requirements and dependencies
✅ **Environment Configuration** - Automated .env setup from templates
✅ **Service Health Checks** - Validates all three services (FastAPI, Flask, Gradio)
✅ **Deployment Preparation** - Generates deployment checklists and guides
✅ **Autonomous Handoff** - Sets up autonomous monitoring and operations
✅ **Detailed Reporting** - Complete logs and reports of bootstrap process

## Quick Start

### Linux/macOS

```bash
cd /path/to/pi-forge-quantum-genesis
./bootstrap/bootstrap.sh
```

### Windows (PowerShell)

```powershell
cd C:\path\to\pi-forge-quantum-genesis
.\bootstrap\bootstrap.ps1
```

## Prerequisites

### Required

- **Python 3.11+** - Programming language runtime
- **pip** - Python package manager
- **git** - Version control system

### Optional but Recommended

- **Docker** - For containerized deployment
- **Railway CLI** - For production deployment
- **curl** - For HTTP requests and health checks
- **Node.js 18+** - For frontend development

## Installation

The bootstrap scripts are included in the repository. No separate installation needed.

## Usage

### Basic Usage

```bash
# Linux/macOS
./bootstrap/bootstrap.sh

# Windows
.\bootstrap\bootstrap.ps1
```

### Advanced Options

#### Linux/macOS

```bash
# Specify environment
./bootstrap/bootstrap.sh --environment production

# Skip tests (faster bootstrap)
./bootstrap/bootstrap.sh --skip-tests

# Verbose output
./bootstrap/bootstrap.sh --verbose

# Show help
./bootstrap/bootstrap.sh --help
```

#### Windows

```powershell
# Specify environment
.\bootstrap\bootstrap.ps1 -Environment production

# Skip tests
.\bootstrap\bootstrap.ps1 -SkipTests

# Verbose output
.\bootstrap\bootstrap.ps1 -Verbose

# Show help
.\bootstrap\bootstrap.ps1 -Help
```

## What the Bootstrap Agent Does

### Step 1: System Requirements Check

- Verifies Python 3.11+ is installed
- Checks for pip, git
- Detects optional tools (Docker, Railway CLI, curl)
- Reports version information
- Validates minimum requirements met

### Step 2: Environment Setup

- Creates Python virtual environment (.venv)
- Activates virtual environment
- Upgrades pip, setuptools, wheel
- Installs all project dependencies from requirements.txt
- Creates .env file from template if not exists
- Validates environment variable configuration

### Step 3: Infrastructure Validation

- Checks all critical files exist:
  - server/main.py (FastAPI)
  - server/app.py (Flask)
  - server/canticle_interface.py (Gradio)
  - server/requirements.txt
  - Dockerfile
  - railway.toml
  - frontend/pi-forge-integration.js
- Validates Python imports work
- Tests module loading

### Step 4: Run Tests

- Installs pytest and testing dependencies
- Runs full test suite
- Reports test results
- Non-critical failures logged but don't block bootstrap

### Step 5: Service Initialization

- Performs health checks on all services
- Validates FastAPI module
- Validates Flask module
- Validates Gradio module
- Ensures all services can start

### Step 6: Deployment Preparation

- Validates deployment configuration
- Checks railway.toml
- Checks Dockerfile
- Tests Docker build (if Docker available)
- Generates deployment checklist

### Step 7: Autonomous Handoff Setup

- Validates AI Agent Handoff Runbook exists
- Creates autonomous operations guide
- Generates service management scripts
- Sets up monitoring infrastructure

### Step 8: Final Report

- Generates comprehensive bootstrap report
- Lists all completed steps
- Provides next steps guidance
- Includes troubleshooting information
- Saves complete log of bootstrap process

## Generated Files and Scripts

After running the bootstrap agent, you'll have:

### Documentation

- `bootstrap/bootstrap-report-YYYYMMDD-HHMMSS.md` - Complete bootstrap report
- `bootstrap/deployment-checklist.md` - Step-by-step deployment guide
- `bootstrap/autonomous-operations.md` - Autonomous system setup guide

### Scripts

- `bootstrap/start-services.sh` (Linux/macOS) - Start all services
- `bootstrap/stop-services.sh` (Linux/macOS) - Stop all services
- `bootstrap/start-services.ps1` (Windows) - Start all services
- `bootstrap/stop-services.ps1` (Windows) - Stop all services

### Logs

- `bootstrap/bootstrap-YYYYMMDD-HHMMSS.log` - Detailed bootstrap log
- `logs/` - Directory for service logs

## Post-Bootstrap Steps

### 1. Configure Environment Variables

Edit the `.env` file with your actual credentials:

```bash
# Linux/macOS
nano .env

# Windows
notepad .env
```

Required variables:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
JWT_SECRET=your-secure-random-string
```

### 2. Start Services

#### Linux/macOS

```bash
# All services
./bootstrap/start-services.sh

# Or individually
uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload  # FastAPI
python server/app.py                                         # Flask
python server/canticle_interface.py                          # Gradio
```

#### Windows

```powershell
# All services
.\bootstrap\start-services.ps1

# Or individually
uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload  # FastAPI
python server\app.py                                         # Flask
python server\canticle_interface.py                          # Gradio
```

### 3. Verify Services

Check health endpoints:

```bash
# FastAPI
curl http://localhost:8000/

# Flask
curl http://localhost:5000/health

# Gradio (open in browser)
# http://localhost:7860/
```

### 4. Deploy to Production

See `bootstrap/deployment-checklist.md` for:
- Railway deployment
- Docker deployment
- Manual deployment

### 5. Enable Autonomous Operations

See `bootstrap/autonomous-operations.md` for:
- GitHub Actions setup
- Autonomous monitoring
- Automatic rollbacks
- Status tracking

## Service Management

### Starting Services

```bash
# Linux/macOS
./bootstrap/start-services.sh

# Windows
.\bootstrap\start-services.ps1
```

Services will start in background and log to `logs/` directory.

### Stopping Services

```bash
# Linux/macOS
./bootstrap/stop-services.sh

# Windows
.\bootstrap\stop-services.ps1
```

### Checking Service Status

```bash
# Check if services are running
ps aux | grep -E "uvicorn|flask|gradio"  # Linux/macOS
Get-Process | Where-Object {$_.Name -match "python"}  # Windows

# Check logs
tail -f logs/*.log  # Linux/macOS
Get-Content logs\*.log -Wait  # Windows
```

## Troubleshooting

### Bootstrap Fails at System Requirements

**Problem**: Required dependencies not installed

**Solution**:
```bash
# Install Python 3.11+
# Ubuntu/Debian
sudo apt update && sudo apt install python3.11 python3-pip git

# macOS (Homebrew)
brew install python@3.11 git

# Windows
# Download Python from python.org
# Install Git from git-scm.com
```

### Virtual Environment Creation Fails

**Problem**: Permission issues or disk space

**Solution**:
```bash
# Check disk space
df -h  # Linux/macOS
Get-PSDrive  # Windows

# Check permissions
ls -la  # Linux/macOS
Get-Acl .  # Windows

# Retry with sudo (Linux only)
sudo ./bootstrap/bootstrap.sh
```

### Dependency Installation Fails

**Problem**: Network issues or package conflicts

**Solution**:
```bash
# Clear pip cache
pip cache purge

# Retry with verbose output
./bootstrap/bootstrap.sh --verbose

# Install dependencies manually
pip install -r server/requirements.txt --verbose
```

### Module Import Fails

**Problem**: Python path issues

**Solution**:
```bash
# Ensure virtual environment is activated
source .venv/bin/activate  # Linux/macOS
.\.venv\Scripts\Activate.ps1  # Windows

# Verify Python path
python -c "import sys; print(sys.path)"

# Reinstall dependencies
pip install -r server/requirements.txt --force-reinstall
```

### Tests Fail

**Problem**: Environment not configured or test issues

**Solution**:
```bash
# Skip tests during bootstrap
./bootstrap/bootstrap.sh --skip-tests

# Run tests manually later
cd tests
pytest -v
```

### Docker Build Fails

**Problem**: Docker not installed or permissions

**Solution**:
```bash
# Install Docker
# See: https://docs.docker.com/get-docker/

# Add user to docker group (Linux)
sudo usermod -aG docker $USER
newgrp docker

# Test Docker
docker run hello-world
```

## Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `SUPABASE_URL` | Supabase project URL | `https://abc123.supabase.co` |
| `SUPABASE_KEY` | Supabase anonymous key | `eyJhbGc...` |
| `JWT_SECRET` | JWT signing secret | `your-random-string` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Deployment environment | `development` |
| `DEBUG` | Debug mode | `true` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `FASTAPI_PORT` | FastAPI port | `8000` |
| `FLASK_PORT` | Flask port | `5000` |
| `GRADIO_PORT` | Gradio port | `7860` |

## Advanced Configuration

### Custom Python Version

```bash
# Use specific Python version
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r server/requirements.txt
```

### Custom Virtual Environment Location

```bash
# Create venv in custom location
python -m venv /path/to/custom/venv
source /path/to/custom/venv/bin/activate
```

### Docker-Only Bootstrap

```bash
# Skip local setup, use Docker
docker build -t quantum-pi-forge .
docker run -p 8000:8000 --env-file .env quantum-pi-forge
```

## CI/CD Integration

The bootstrap agent can be integrated into CI/CD pipelines:

### GitHub Actions

```yaml
- name: Bootstrap System
  run: |
    chmod +x bootstrap/bootstrap.sh
    ./bootstrap/bootstrap.sh --skip-tests
```

### GitLab CI

```yaml
bootstrap:
  script:
    - chmod +x bootstrap/bootstrap.sh
    - ./bootstrap/bootstrap.sh --skip-tests
```

### Jenkins

```groovy
stage('Bootstrap') {
    steps {
        sh 'chmod +x bootstrap/bootstrap.sh'
        sh './bootstrap/bootstrap.sh --skip-tests'
    }
}
```

## Security Considerations

1. **Never commit .env file** - Contains sensitive credentials
2. **Use strong JWT_SECRET** - Generate with: `openssl rand -hex 32`
3. **Rotate credentials regularly** - Update Supabase keys periodically
4. **Limit permissions** - Use least privilege principle
5. **Enable HTTPS** - Use SSL/TLS in production
6. **Validate inputs** - Bootstrap validates all inputs

## Performance

### Bootstrap Time

- **Minimal**: ~2-3 minutes (skip tests)
- **Standard**: ~5-7 minutes (with tests)
- **Full**: ~10-15 minutes (with Docker build)

### Resource Requirements

- **Disk Space**: ~500 MB (dependencies + virtual environment)
- **RAM**: ~2 GB (during dependency installation)
- **Network**: ~100 MB (downloading packages)

## Support

### Getting Help

1. Check the bootstrap log: `bootstrap/bootstrap-YYYYMMDD-HHMMSS.log`
2. Review the documentation in `docs/`
3. Consult the deployment checklist
4. Check GitHub Issues
5. Contact repository maintainer

### Reporting Issues

When reporting bootstrap issues, include:

1. Operating system and version
2. Python version
3. Complete bootstrap log
4. Error messages
5. Steps to reproduce

## Contributing

To improve the bootstrap agent:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on multiple platforms
5. Submit a pull request

## License

See the main repository LICENSE file.

## Changelog

### Version 1.0.0 (2024-12-10)

- Initial release
- Cross-platform support (Linux, macOS, Windows)
- Automated environment setup
- Comprehensive validation
- Service health checks
- Deployment preparation
- Autonomous handoff setup
- Complete documentation

---

**🎉 Bootstrap your Quantum Resonance Lattice with confidence!**
