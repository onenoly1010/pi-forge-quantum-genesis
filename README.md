# 🌌 Pi Forge Quantum Genesis

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-red.svg)](https://flask.palletsprojects.com/)
[![Gradio](https://img.shields.io/badge/Gradio-5.31+-orange.svg)](https://gradio.app/)

> **Quantum Resonance Lattice** — Unifying ethical AI, finance resonance, and creative intelligence through autonomous multi-service architecture.

## 🚀 Quick Start (5 Minutes)

Get up and running with our automated bootstrap agent:

### Linux/macOS
```bash
git clone https://github.com/onenoly1010/pi-forge-quantum-genesis.git
cd pi-forge-quantum-genesis
chmod +x bootstrap/bootstrap.sh
./bootstrap/bootstrap.sh
```

### Windows (PowerShell)
```powershell
git clone https://github.com/onenoly1010/pi-forge-quantum-genesis.git
cd pi-forge-quantum-genesis
.\bootstrap\bootstrap.ps1
```

The bootstrap agent will:
- ✅ Validate system requirements
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Configure environment
- ✅ Run health checks
- ✅ Generate deployment guides
- ✅ Create service management scripts

**See [Quick Start Guide](bootstrap/QUICKSTART.md) for details.**

## 📚 Overview

Pi Forge Quantum Genesis is a **multi-application autonomous system** featuring three distinct services forming a "Quantum Resonance Lattice":

### The Three Services

1. **🚀 FastAPI Quantum Conduit** (Port 8000)
   - Production API server with async/await
   - Supabase authentication & WebSocket
   - Pi Network payment integration
   - Health monitoring endpoints

2. **🎨 Flask Glyph Weaver** (Port 5000)
   - Quantum resonance visualization dashboard
   - SVG procedural generation (4-phase cascade)
   - Template rendering engine
   - Legacy route support

3. **🔮 Gradio Truth Mirror** (Port 7860)
   - Ethical AI audit interface
   - Interactive model evaluation
   - Standalone ethics portal
   - Gradio component UI

### Key Features

- **Autonomous Operations** - Self-monitoring and self-healing via GitHub Actions
- **Multi-Service Architecture** - Three specialized services, one deployment
- **Production Ready** - Health checks, logging, error handling, security
- **Bootstrap Agent** - One-command setup on fresh infrastructure
- **Cross-Platform** - Works on Linux, macOS, and Windows
- **Docker Support** - Full containerization with Docker Compose
- **Railway Deployment** - Zero-config deployment to Railway
- **Comprehensive Testing** - Full test suite with pytest

## 🛠️ Architecture

### Service Communication

```
┌─────────────────────────────────────────────────────────┐
│                  Quantum Resonance Lattice               │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   FastAPI    │  │    Flask     │  │   Gradio     │  │
│  │   Port 8000  │  │  Port 5000   │  │  Port 7860   │  │
│  │              │  │              │  │              │  │
│  │ • Auth/API   │  │ • Dashboard  │  │ • Ethics UI  │  │
│  │ • WebSocket  │  │ • SVG Viz    │  │ • Auditing   │  │
│  │ • Pi Network │  │ • Templates  │  │ • Evaluation │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│         │                 │                  │          │
│         └─────────────────┴──────────────────┘          │
│                      │                                   │
│              Shared JWT Auth                            │
│              Supabase Backend                           │
│              Common Configuration                        │
└─────────────────────────────────────────────────────────┘
```

### Technology Stack

- **Backend**: Python 3.11+, FastAPI, Flask, Gradio
- **Database**: Supabase (PostgreSQL)
- **Authentication**: JWT, Supabase Auth
- **WebSocket**: Native WebSocket support
- **Frontend**: JavaScript, SVG visualization
- **Deployment**: Railway, Docker, systemd
- **CI/CD**: GitHub Actions with autonomous monitoring
- **Testing**: pytest, pytest-asyncio

## 📖 Documentation

### Getting Started
- **[Quick Start Guide](bootstrap/QUICKSTART.md)** - Get running in 5 minutes
- **[Bootstrap README](bootstrap/README.md)** - Bootstrap agent documentation
- **[Deployment Guide](bootstrap/DEPLOYMENT_GUIDE.md)** - Production deployment
- **[Autonomous Operations](bootstrap/docs/AUTONOMOUS_OPERATIONS.md)** - AI agent setup

### Development
- **[Copilot Instructions](.github/copilot-instructions.md)** - Development conventions
- **[AI Agent Quick Reference](docs/AI_AGENT_QUICK_REFERENCE.md)** - Agent commands
- **[Docker Development Guide](docs/DOCKER_DEVELOPMENT_GUIDE.md)** - Docker setup

### Deployment
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Railway deployment notes
- **[Railway Template](bootstrap/templates/railway.toml.template)** - Railway config
- **[Docker Compose Template](bootstrap/templates/docker-compose.yml.template)** - Multi-service setup

## 🔧 Development

### Prerequisites

- Python 3.11+
- pip (Python package manager)
- git
- (Optional) Docker for containerized development

### Local Setup

1. **Run Bootstrap**
   ```bash
   ./bootstrap/bootstrap.sh  # Linux/macOS
   .\bootstrap\bootstrap.ps1  # Windows
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Start Services**
   ```bash
   ./bootstrap/start-services.sh  # Linux/macOS
   .\bootstrap\start-services.ps1  # Windows
   ```

4. **Verify**
   - FastAPI: http://localhost:8000
   - Flask: http://localhost:5000
   - Gradio: http://localhost:7860

### Manual Setup (Alternative)

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
.\.venv\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install -r server/requirements.txt

# Run services individually
uvicorn server.main:app --reload  # FastAPI
python server/app.py              # Flask
python server/canticle_interface.py  # Gradio
```

### Running Tests

```bash
cd tests
pytest -v
```

## 🚀 Deployment

### Railway (Recommended)

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway link
railway up
```

See [Deployment Guide](bootstrap/DEPLOYMENT_GUIDE.md) for detailed instructions.

### Docker

```bash
# Build and run
docker build -t quantum-pi-forge .
docker run -p 8000:8000 --env-file .env quantum-pi-forge

# Or use Docker Compose
cp bootstrap/templates/docker-compose.yml.template docker-compose.yml
docker-compose up -d
```

### Manual Deployment

See [Deployment Guide](bootstrap/DEPLOYMENT_GUIDE.md) for systemd service setup, Nginx configuration, and SSL setup.

## 🤖 Autonomous Operations

Enable self-monitoring and self-healing:

```bash
# Set GitHub secrets
gh secret set SUPABASE_URL --body "your-url"
gh secret set SUPABASE_KEY --body "your-key"
gh secret set JWT_SECRET --body "$(openssl rand -hex 32)"

# Enable autonomous runbook
gh workflow enable ai-agent-handoff-runbook.yml

# Trigger initial deployment
gh workflow run ai-agent-handoff-runbook.yml --field action=full-deployment
```

**Features**:
- 🔄 Scheduled health checks every 6 hours
- 🛡️ Automatic rollback on failures
- 📊 GitHub issue status tracking
- 🚨 Webhook notifications (Slack, Discord)
- 📈 Performance metrics collection

See [Autonomous Operations Guide](bootstrap/docs/AUTONOMOUS_OPERATIONS.md) for details.

## 🔐 Environment Configuration

Required environment variables:

```env
# Supabase (Required)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key

# JWT Authentication (Required)
JWT_SECRET=your-secure-random-string

# Optional
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
```

Generate secure secrets:
```bash
openssl rand -hex 32  # JWT_SECRET
```

## 📁 Project Structure

```
pi-forge-quantum-genesis/
├── bootstrap/              # Bootstrap agent and scripts
│   ├── bootstrap.sh       # Linux/macOS bootstrap
│   ├── bootstrap.ps1      # Windows bootstrap
│   ├── QUICKSTART.md      # Quick start guide
│   ├── README.md          # Bootstrap documentation
│   ├── DEPLOYMENT_GUIDE.md # Deployment guide
│   ├── docs/              # Additional documentation
│   │   └── AUTONOMOUS_OPERATIONS.md
│   ├── scripts/           # Service management scripts
│   └── templates/         # Configuration templates
├── server/                # Backend services
│   ├── main.py           # FastAPI application
│   ├── app.py            # Flask application
│   ├── canticle_interface.py  # Gradio application
│   └── requirements.txt  # Python dependencies
├── frontend/              # Frontend assets
├── tests/                 # Test suite
├── docs/                  # Documentation
├── .github/              # GitHub workflows
│   └── workflows/
│       └── ai-agent-handoff-runbook.yml
├── Dockerfile            # Production container
├── railway.toml          # Railway deployment
└── .env.example          # Environment template
```

## 🧪 Testing

```bash
# Run all tests
cd tests
pytest -v

# Run with coverage
pytest --cov=../server --cov-report=term

# Run specific test file
pytest test_health_endpoints.py -v
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

See [LICENSE](LICENSE) file for details.

## 🙏 Credits

**© 2025 Pi Forge Collective — Quantum Genesis Initiative**

**Lead Developer**: Kris Olofson (onenoly1010)

### Built With

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Flask](https://flask.palletsprojects.com/) - Micro web framework
- [Gradio](https://gradio.app/) - ML interface builder
- [Supabase](https://supabase.com/) - Open source Firebase alternative
- [Railway](https://railway.app/) - Infrastructure platform

## 📞 Support

- **Documentation**: See `bootstrap/` and `docs/` directories
- **Issues**: [GitHub Issues](https://github.com/onenoly1010/pi-forge-quantum-genesis/issues)
- **Discussions**: [GitHub Discussions](https://github.com/onenoly1010/pi-forge-quantum-genesis/discussions)

---

**🌌 Welcome to the Quantum Resonance Lattice!**

*The Cyber Samarai serves as the quantum guardian maintaining sub-5-nanosecond coherence between all layers.*