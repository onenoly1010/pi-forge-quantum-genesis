# 🚀 Quantum Pi Forge - Quick Start Guide

Get your Quantum Resonance Lattice up and running in minutes!

## ⚡ 5-Minute Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/onenoly1010/pi-forge-quantum-genesis.git
cd pi-forge-quantum-genesis
```

### Step 2: Run Bootstrap

#### Linux/macOS
```bash
chmod +x bootstrap/bootstrap.sh
./bootstrap/bootstrap.sh
```

#### Windows (PowerShell)
```powershell
.\bootstrap\bootstrap.ps1
```

### Step 3: Configure Environment

Edit `.env` with your credentials:

```bash
# Linux/macOS
nano .env

# Windows
notepad .env
```

Required:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
JWT_SECRET=your-secure-random-string
```

### Step 4: Start Services

#### Linux/macOS
```bash
./bootstrap/start-services.sh
```

#### Windows
```powershell
.\bootstrap\start-services.ps1
```

### Step 5: Verify

Open in browser:
- FastAPI: http://localhost:8000
- Flask: http://localhost:5000
- Gradio: http://localhost:7860

## 🎯 What You Get

### Three Quantum Services

1. **FastAPI Quantum Conduit** (Port 8000)
   - Production API server
   - WebSocket support
   - Supabase authentication
   - Pi Network integration

2. **Flask Glyph Weaver** (Port 5000)
   - Resonance visualization dashboard
   - SVG procedural generation
   - Template serving

3. **Gradio Truth Mirror** (Port 7860)
   - Ethical AI audit interface
   - Model evaluation
   - Interactive exploration

### Development Tools

- ✅ Virtual environment configured
- ✅ All dependencies installed
- ✅ Tests ready to run
- ✅ Health checks automated
- ✅ Service management scripts
- ✅ Complete documentation

## 📚 Next Steps

### Deploy to Production

See [Deployment Guide](DEPLOYMENT_GUIDE.md) for:
- Railway deployment
- Docker deployment
- Environment configuration

### Enable Autonomous Operations

See [Autonomous Operations](docs/AUTONOMOUS_OPERATIONS.md) for:
- GitHub Actions setup
- Scheduled monitoring
- Automatic rollbacks
- Status tracking

### Explore Documentation

- `bootstrap/README.md` - Bootstrap system details
- `bootstrap/deployment-checklist.md` - Deployment steps
- `docs/AI_AGENT_QUICK_REFERENCE.md` - Agent commands
- `.github/copilot-instructions.md` - Development guide

## 🔧 Common Tasks

### Run Tests

```bash
cd tests
pytest -v
```

### Check Service Health

```bash
# FastAPI
curl http://localhost:8000/

# Flask
curl http://localhost:5000/health
```

### View Logs

```bash
# Linux/macOS
tail -f logs/*.log

# Windows
Get-Content logs\*.log -Wait
```

### Stop Services

```bash
# Linux/macOS
./bootstrap/stop-services.sh

# Windows
.\bootstrap\stop-services.ps1
```

## 🆘 Troubleshooting

### Bootstrap Fails

```bash
# Check system requirements
python3 --version  # Should be 3.11+
pip --version
git --version

# Try verbose mode
./bootstrap/bootstrap.sh --verbose
```

### Services Won't Start

```bash
# Verify virtual environment
source .venv/bin/activate  # Linux/macOS
.\.venv\Scripts\Activate.ps1  # Windows

# Check .env configuration
cat .env

# Reinstall dependencies
pip install -r server/requirements.txt
```

### Port Already in Use

```bash
# Find process using port (Linux/macOS)
lsof -i :8000

# Find process using port (Windows)
netstat -ano | findstr :8000

# Kill process if needed
kill <PID>  # Linux/macOS
Stop-Process -Id <PID>  # Windows
```

## 🌟 Features

### Multi-Application Architecture

All three services share:
- Common JWT authentication
- Shared environment configuration
- Integrated deployment
- Unified monitoring

### Production Ready

- Health check endpoints
- Graceful error handling
- Comprehensive logging
- Security best practices
- Docker containerization
- Railway deployment config

### Autonomous Operations

- Scheduled health monitoring (every 6 hours)
- Automatic rollback on failures
- GitHub issue status tracking
- Webhook notifications
- CI/CD pipeline automation

## 📊 Project Structure

```
pi-forge-quantum-genesis/
├── bootstrap/              # Bootstrap agent and scripts
│   ├── bootstrap.sh       # Linux/macOS bootstrap
│   ├── bootstrap.ps1      # Windows bootstrap
│   ├── start-services.sh  # Service starter (Linux/macOS)
│   ├── stop-services.sh   # Service stopper (Linux/macOS)
│   ├── start-services.ps1 # Service starter (Windows)
│   ├── stop-services.ps1  # Service stopper (Windows)
│   └── docs/              # Bootstrap documentation
├── server/                 # Backend services
│   ├── main.py            # FastAPI application
│   ├── app.py             # Flask application
│   ├── canticle_interface.py  # Gradio application
│   └── requirements.txt   # Python dependencies
├── frontend/               # Frontend assets
│   └── pi-forge-integration.js
├── tests/                  # Test suite
├── docs/                   # Documentation
├── .github/                # GitHub workflows
│   └── workflows/
│       └── ai-agent-handoff-runbook.yml
├── Dockerfile             # Production container
├── railway.toml           # Railway deployment
└── .env.example           # Environment template
```

## 🔐 Security Notes

1. **Never commit .env** - Contains sensitive credentials
2. **Use strong secrets** - Generate with `openssl rand -hex 32`
3. **Rotate keys regularly** - Update credentials periodically
4. **Enable HTTPS** - Use SSL/TLS in production
5. **Review permissions** - Follow least privilege principle

## 🚀 Deployment Options

### Railway (Recommended)

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway link
railway up
```

### Docker

```bash
# Build and run
docker build -t quantum-pi-forge .
docker run -p 8000:8000 --env-file .env quantum-pi-forge
```

### Manual

```bash
# Production server
uvicorn server.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📖 Learn More

- [Full Documentation](../README.md)
- [Bootstrap Guide](README.md)
- [Deployment Checklist](deployment-checklist.md)
- [Autonomous Operations](docs/AUTONOMOUS_OPERATIONS.md)
- [AI Agent Reference](../docs/AI_AGENT_QUICK_REFERENCE.md)

## 🎉 Success!

You now have a fully functional Quantum Pi Forge system!

**What's happening:**
- ✅ Three services running in harmony
- ✅ Authentication ready
- ✅ WebSocket connections active
- ✅ Health monitoring enabled
- ✅ Ready for development or deployment

**Ready for the next level?**
- Deploy to production
- Enable autonomous operations
- Integrate with Pi Network
- Build amazing applications

---

**Need help?** Check the documentation or open an issue!

**🌌 Welcome to the Quantum Resonance Lattice!**
