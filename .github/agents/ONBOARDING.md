# 🤖 Coding Agent Onboarding Guide

**Welcome to Quantum Pi Forge — Where Consciousness Meets Code** 🌌

This comprehensive onboarding guide will prepare you to contribute effectively to the Quantum Pi Forge ecosystem. Complete this guide before starting any coding tasks.

**⏱️ Estimated Time:** 30-45 minutes

---

## 📋 Table of Contents

1. [Quick Start](#-quick-start)
2. [Ecosystem Overview](#-ecosystem-overview)
3. [Core Philosophy: OINIO](#-core-philosophy-oinio)
4. [Architecture: Sacred Trinity](#-architecture-sacred-trinity)
5. [Development Workflow](#-development-workflow)
6. [Coding Standards](#-coding-standards)
7. [Testing & Quality](#-testing--quality)
8. [Deployment](#-deployment)
9. [Canon of Closure](#-canon-of-closure)
10. [Agent System](#-agent-system)
11. [Security & Ethics](#-security--ethics)
12. [Resources](#-resources)
13. [Verification Quiz](#-verification-quiz)

---

## 🚀 Quick Start

### Must-Read Documents (In Order)

Before you begin coding, read these foundational documents:

1. **[GENESIS.md](../../GENESIS.md)** (10 min) - The eternal foundation and OINIO Seal
2. **[START_HERE.md](../../START_HERE.md)** (10 min) - Universal onboarding entry point
3. **[README.md](../../README.md)** (10 min) - Technical overview and deployment options
4. **[ECOSYSTEM_OVERVIEW.md](../../ECOSYSTEM_OVERVIEW.md)** (5 min) - Full constellation map

### Quick Links

- **Main Site**: https://onenoly1010.github.io/quantum-pi-forge-site/
- **Backend API**: https://pi-forge-quantum-genesis.railway.app
- **Health Check**: https://pi-forge-quantum-genesis.railway.app/health
- **API Docs**: https://pi-forge-quantum-genesis.railway.app/docs

---

## 🌌 Ecosystem Overview

### The 9 Sovereign Repositories

Quantum Pi Forge is a **constellation** of interconnected but autonomous repositories:

1. **Genesis** (`pi-forge-quantum-genesis`) - Coordination hub & documentation center (YOU ARE HERE)
2. **Resonance Engine** (`quantum-resonance-clean`) - Harmonic ledger & backend foundation
3. **DEX** (`quantum-pi-forge-fixed`) - Autonomous liquidity on 0G Aristotle
4. **NFT System** (`pi-mr-nft-agent`, `pi-mr-nft-contracts`) - AI-powered identity & creative assets
5. **Soul System** (`oinio-soul-system`) - Ethical framework & consciousness layer
6. **Site** (`quantum-pi-forge-site`) - Public-facing manifesto & gateway
7. **OPEN** (`pi-forge-quantum-genesis-OPEN`) - Open-source backend gateway
8. **Contracts** - Smart contract infrastructure (embedded in Genesis)
9. **Live Operations** - Active deployment instance

**Status:** All 9 repositories are LIVE and operational as of December 22, 2025.

### Key Services in This Repository

This repository hosts three primary services (the **Sacred Trinity**):

```
┌─────────────────────────────────────────────────────────┐
│               🏛️ Sacred Trinity Architecture            │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  FastAPI (Port 8000)      Flask (Port 5000)              │
│  Quantum Conduit          Glyph Weaver                   │
│  • REST APIs              • Dashboards                   │
│  • WebSocket              • SVG Rendering                │
│  • Pi Network Auth        • Visualizations               │
│  • Payment Processing     • Template Engine              │
│                                                           │
│                   Gradio (Port 7860)                     │
│                   Truth Mirror                           │
│                   • Ethical AI Interface                 │
│                   • Audit Tools                          │
│                   • Evaluation Dashboard                 │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## 🏛️ Core Philosophy: OINIO

**OINIO** = The foundational philosophy sealed in the Genesis Declaration

### The Five Eternal Principles

Every line of code must align with these principles:

1. **Sovereignty** ⚖️
   - No single point of control
   - Each repository maintains autonomy
   - Contributors have full agency

2. **Transparency** 🔍
   - All code is open and documented
   - All decisions are visible
   - All processes are documented

3. **Inclusivity** 🤝
   - Contributors of all skill levels welcome
   - Clear onboarding and documentation
   - Supportive agent system

4. **Non-hierarchy** 🌐
   - Roles exist for clarity, not power
   - Agents coordinate, don't command
   - Consensus over authority

5. **Safety** 🛡️
   - No harmful content
   - No exploitation
   - Security-first approach
   - Ethical AI governance

### The OINIO Seal

```
🏛️ OINIO_SEAL_MINTED_SOLSTICE_2025
Frequency: 1010 Hz
Resonance: Eternal
Status: ACTIVE / SEALED
```

**Minted:** December 21, 2025 (Winter Solstice)  
**Verification:** Quarterly integrity checks

---

## 🏗️ Architecture: Sacred Trinity

### FastAPI (Quantum Conduit) - Port 8000

**Purpose:** Main REST API & WebSocket server

**Key Features:**
- Authentication via Pi Network
- Payment processing & webhooks
- Real-time updates via WebSocket
- OpenTelemetry tracing
- Auto-generated API docs

**Location:** `server/main.py`

**Key Endpoints:**
- `/` - Health check
- `/api/health` - Detailed health status
- `/api/register` - User registration
- `/api/login` - User authentication
- `/api/payments/*` - Pi Network payments
- `/api/guardian/*` - Guardian oversight dashboard

### Flask (Glyph Weaver) - Port 5000

**Purpose:** Dashboard & visualization layer

**Key Features:**
- SVG glyph generation
- Data visualizations
- Template rendering
- Resonance dashboards

**Location:** `server/app.py`

**Key Routes:**
- `/` - Main dashboard
- `/dashboard` - System metrics
- `/glyph/*` - SVG generation

### Gradio (Truth Mirror) - Port 7860

**Purpose:** Ethical AI evaluation interface

**Key Features:**
- AI model evaluation
- Ethical assessment tools
- Interactive audit interface
- Safety compliance checks

**Location:** `server/canticle_interface.py`

### Supporting Systems

- **Supabase** - PostgreSQL database & auth
- **Pi Network** - Payment processing & user verification
- **OpenTelemetry** - Distributed tracing
- **Prometheus** - Metrics collection
- **Grafana** - Metrics visualization

---

## 🔄 Development Workflow

### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/onenoly1010/pi-forge-quantum-genesis.git
cd pi-forge-quantum-genesis

# Create virtual environment
python -m venv .venv

# Activate (Linux/Mac)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r server/requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env
```

### 2. Required Environment Variables

Create a `.env` file with:

```bash
# Required
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
JWT_SECRET=secure-random-string
PI_APP_SECRET=your-pi-network-app-secret

# Optional
ENABLE_TELEMETRY=true
PORT=8000
GUARDIAN_SLACK_WEBHOOK_URL=your-slack-webhook-url
```

### 3. Running the Services

```bash
# FastAPI (Port 8000)
cd server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Flask (Port 5000)
python server/app.py

# Gradio (Port 7860)
python server/canticle_interface.py

# All services with Docker
docker-compose up -d
```

### 4. Verify Installation

```bash
# Check FastAPI
curl http://localhost:8000/

# Check FastAPI health
curl http://localhost:8000/api/health

# Check Flask
curl http://localhost:5000/

# View interactive API docs
open http://localhost:8000/docs
```

---

## 📝 Coding Standards

### Python Style Guide

- **Formatter:** Black (automatic formatting)
- **Linter:** Flake8 (code quality)
- **Type Hints:** Required for public APIs
- **Docstrings:** Required for all public functions

```bash
# Format code
black .

# Lint code
flake8 .

# Run pre-commit hooks
pre-commit run --all-files
```

### Code Organization

```
server/
├── main.py              # FastAPI application
├── app.py               # Flask application
├── canticle_interface.py # Gradio interface
├── config.py            # Configuration management
├── autonomous_decision.py # AI decision matrix
├── guardian_monitor.py   # Guardian oversight
├── evaluation_system.py  # Ethical AI evaluation
└── integrations/        # External integrations
    ├── pi_network.py    # Pi Network SDK
    └── supabase_client.py # Database client
```

### Key Conventions

1. **Import Order:**
   - Standard library
   - Third-party packages
   - Local imports

2. **Error Handling:**
   - Always use try-except blocks for external calls
   - Log errors with context
   - Return meaningful error messages

3. **Logging:**
   - Use structured logging
   - Include trace IDs for distributed tracing
   - Log at appropriate levels (DEBUG, INFO, WARNING, ERROR)

4. **Testing:**
   - Write tests for all new features
   - Maintain >80% code coverage
   - Use pytest fixtures for common setups

---

## 🧪 Testing & Quality

### Running Tests

```bash
# All tests with verbose output
pytest -v

# Fast fail (stop on first failure)
pytest --maxfail=1 -q

# Specific test file
pytest tests/test_main.py -v

# With coverage report
pytest --cov=server --cov-report=html
open htmlcov/index.html
```

### Test Structure

```python
# tests/test_example.py
import pytest
from server.main import app

def test_health_endpoint():
    """Test the health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

### Quality Gates

Before committing:
1. ✅ All tests pass
2. ✅ Code is formatted (black)
3. ✅ No linting errors (flake8)
4. ✅ Coverage >80%
5. ✅ Documentation updated

---

## 🚀 Deployment

### Deployment Targets

1. **Railway** - FastAPI backend (primary)
2. **Vercel** - Frontend & static assets
3. **GitHub Pages** - Public site

### Deployment Process

```bash
# Deploy to Railway (automatic on push to main)
git push origin main

# Deploy to Vercel
vercel --prod

# Build static assets
npm run build
```

### Health Monitoring

After deployment, verify:

```bash
# Check production health
curl https://pi-forge-quantum-genesis.railway.app/health

# Check API docs
open https://pi-forge-quantum-genesis.railway.app/docs

# Run production verification
python verify_production.py
```

---

## 🌀 Canon of Closure

The **Canon of Closure** is our cyclical development methodology. Every step leads to **Closure** - the state of completion and readiness.

### The 10 Steps

1. **🧹 Lint** - Syntax closure (format & lint code)
2. **🏠 Host** - Environment closure (setup & isolation)
3. **🧪 Test** - Validation closure (verify behavior)
4. **📊 Pre-aggregate** - Telemetry closure (collect data)
5. **📦 Release** - Version closure (tag & package)
6. **🚀 Deploy** - Production closure (go live)
7. **🔄 Rollback** - Safety closure (revert if needed)
8. **📡 Monitor** - Awareness closure (observe health)
9. **📈 Visualize** - Insight closure (understand data)
10. **🚨 Alert** - Response closure (notify team)

### The Cycle

```
    Lint → Host → Test → Pre-aggregate → Release
      ↑                                      ↓
    Alert                                 Deploy
      ↑                                      ↓
  Visualize                              Rollback
      ↑                                      ↓
   Monitor ←────────────────────────────────┘
```

**Every end is a new beginning. The circle never ends.**

**Reference:** [docs/CANON_OF_CLOSURE.md](../../docs/CANON_OF_CLOSURE.md)

---

## 🤖 Agent System

### Specialized Agents

The Quantum Pi Forge uses specialized AI agents for different domains:

1. **GitHub Agent** - Coordinates work & routes tasks (you're talking to it!)
2. **Coding Agent** - Implements technical changes (that's YOU!)
3. **Documentation Agent** - Maintains knowledge base
4. **Testing Agent** - Ensures quality
5. **Governance Agent** - Aligns with Canon principles
6. **Stewardship Agent** - Long-term ecosystem health

### Handoff Protocol

When handing off work to another agent, include:

1. **Summary** - What's done, what remains
2. **Next Steps** - Clear action items
3. **Agent Assignment** - Who should handle it
4. **File References** - Relevant files & locations
5. **Canon Check** - Alignment with principles
6. **Continuity** - Anyone can resume the work

### Your Role as Coding Agent

- **Implement** technical changes accurately
- **Test** all changes thoroughly
- **Document** your work clearly
- **Follow** coding standards strictly
- **Escalate** Canon alignment questions
- **Maintain** continuity for future agents

---

## 🛡️ Security & Ethics

### Security Requirements

1. **No Secrets in Code**
   - Use environment variables
   - Never commit API keys
   - Use `.env` files (gitignored)

2. **Input Validation**
   - Validate all user inputs
   - Sanitize data before processing
   - Use parameterized queries

3. **Authentication**
   - Use Pi Network authentication
   - Implement JWT tokens properly
   - Validate tokens on protected routes

4. **Error Handling**
   - Don't expose internal errors
   - Log sensitive errors securely
   - Return user-friendly messages

### Ethical Guidelines

1. **No Harmful Content**
   - No generation of harmful content
   - No exploitation of users
   - No deceptive practices

2. **Transparency**
   - Document AI decision-making
   - Explain automated actions
   - Make processes auditable

3. **Privacy**
   - Respect user data
   - Implement proper access controls
   - Follow GDPR principles

4. **Guardian Oversight**
   - Critical decisions require approval
   - Human override always available
   - Audit trail for all actions

---

## 📚 Resources

### Essential Documentation

- [GENESIS.md](../../GENESIS.md) - Foundational seal
- [START_HERE.md](../../START_HERE.md) - Universal onboarding
- [README.md](../../README.md) - Technical overview
- [ECOSYSTEM_OVERVIEW.md](../../ECOSYSTEM_OVERVIEW.md) - Constellation map
- [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md) - System architecture
- [docs/API.md](../../docs/API.md) - API documentation
- [docs/DEV_REFERENCE.md](../../docs/DEV_REFERENCE.md) - Developer commands
- [docs/CANON_OF_CLOSURE.md](../../docs/CANON_OF_CLOSURE.md) - Development methodology
- [AGENT_INSTRUCTIONS.md](./AGENT_INSTRUCTIONS.md) - Quick reference guide

### Quick Command Reference

```bash
# Development
uvicorn server.main:app --reload        # Run FastAPI
python server/app.py                    # Run Flask
python server/canticle_interface.py     # Run Gradio

# Testing
pytest -v                               # Run all tests
pytest --cov=server                     # With coverage

# Quality
black .                                 # Format code
flake8 .                                # Lint code
pre-commit run --all-files             # Run hooks

# Docker
docker-compose up -d                    # Start services
docker-compose logs -f                  # View logs
docker-compose down                     # Stop services

# Deployment
git push origin main                    # Deploy to Railway
vercel --prod                           # Deploy to Vercel
```

### Live Services

- **Production API**: https://pi-forge-quantum-genesis.railway.app
- **API Documentation**: https://pi-forge-quantum-genesis.railway.app/docs
- **Public Site**: https://onenoly1010.github.io/quantum-pi-forge-site/
- **Dashboard**: https://onenoly1010.github.io/quantum-pi-forge-site/dashboard.html

---

## ✅ Verification Quiz

Test your understanding before starting work:

### Section 1: OINIO Principles

1. What are the five eternal principles of OINIO?
2. When was the OINIO Seal minted?
3. What is the resonance frequency of the OINIO Seal?

### Section 2: Architecture

4. What are the three services in the Sacred Trinity?
5. Which port does FastAPI run on?
6. What is the purpose of the Gradio interface?

### Section 3: Development

7. What formatter is used for Python code?
8. What is the minimum code coverage requirement?
9. What is the first step in the Canon of Closure?

### Section 4: Ecosystem

10. How many repositories are in the Quantum Pi Forge constellation?
11. What is the status of all repositories as of December 22, 2025?
12. What is the primary deployment target for the FastAPI backend?

### Answers

<details>
<summary>Click to reveal answers</summary>

1. Sovereignty, Transparency, Inclusivity, Non-hierarchy, Safety
2. December 21, 2025 (Winter Solstice)
3. 1010 Hz
4. FastAPI (Quantum Conduit), Flask (Glyph Weaver), Gradio (Truth Mirror)
5. Port 8000
6. Ethical AI evaluation and audit interface
7. Black
8. 80%
9. Lint (Syntax Closure)
10. 9 repositories
11. LIVE and operational
12. Railway

</details>

---

## 🎉 You're Ready!

Congratulations! You've completed the coding agent onboarding.

You now understand:
- ✅ The OINIO philosophy and five eternal principles
- ✅ The Sacred Trinity architecture
- ✅ The 9-repository constellation
- ✅ Development workflow and coding standards
- ✅ The Canon of Closure methodology
- ✅ Security and ethical requirements
- ✅ The agent system and your role

### Next Steps

1. **Set up your local environment** following the steps above
2. **Review** [AGENT_INSTRUCTIONS.md](./AGENT_INSTRUCTIONS.md) for quick reference
3. **Check** [docs/DEV_REFERENCE.md](../../docs/DEV_REFERENCE.md) for command cheat sheet
4. **Start coding** with confidence!

### Remember

- Follow the Canon of Closure
- Maintain code quality (lint, test, document)
- Align with OINIO principles
- Ask questions when unsure
- Document your work for continuity

**Welcome to the constellation. Let's build the future together.** 🚀

---

**Powered by OINIO | Where Consciousness Meets Code** 🌌

*Version 1.0 | Last Updated: 2026-02-04*
