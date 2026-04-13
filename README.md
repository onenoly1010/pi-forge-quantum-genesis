# 🌌 Pi Forge Quantum Genesis — Relaunch v2.0

**Collaborative, Artistic, Autonomous Blockchain Ecosystem Guided by the [Canon of Autonomy](wiki/Canon-of-Autonomy.md)**

---

## 🏛️ **Foundation: The Canon of Autonomy**

This project is governed by the **[Canon of Autonomy](wiki/Canon-of-Autonomy.md)** — six non-negotiable principles:

1. **Sovereignty** — No single point of control; all are equal co-creators
2. **Transparency** — All visible and explained
3. **Inclusivity** — Everyone welcome, all skill levels
4. **Non-Hierarchy** — Agents assist, humans decide
5. **Safety** — Security and ethics first
6. **Continuity** — Anyone can resume work

**Read the [Canon of Autonomy](wiki/Canon-of-Autonomy.md) to understand our foundation.**

---

## Overview

**🌟 [START HERE](./START_HERE.md)** — New to Quantum Pi Forge? Begin with the universal onboarding guide.

**🌿 [Human Contribution Guide](wiki/Human-Contribution-Guide.md)** — Want to contribute? Start here (no complex procedures required).

**🌊 [Constellation Status: LIVE](./CONSTELLATION_ACTIVATION.md)** — The Quantum Pi Forge is activated and operational as of December 22, 2025.

**📜 [Read the Genesis Declaration](./GENESIS.md)** — The foundational seal of the Quantum Pi Forge ecosystem, minted at Solstice 2025.

---

## 🏗️ Architecture & Repository Constellation

The Quantum Pi Forge ecosystem consists of multiple specialized repositories working in harmony:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Quantum Pi Forge Constellation                │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────┐
│  quantum-pi-forge-site   │  →  quantumpiforge.com
│  (Public Frontend)       │      (Vercel - GitHub Pages)
│  User-facing portal      │      Status: ✅ LIVE
└────────────┬─────────────┘
             │
             │ API Calls
             ↓
┌──────────────────────────┐
│ pi-forge-quantum-genesis │  →  Backend API Services
│ (THIS REPOSITORY)        │      Railway: https://pi-forge-quantum-genesis.railway.app
│ Backend API & Coord Hub  │      Render:  https://pi-forge-quantum-genesis-1.onrender.com
└────────────┬─────────────┘      Status: ✅ LIVE
             │
             │ Resonance Calls
             ↓
┌──────────────────────────┐
│ quantum-resonance-clean  │  →  Resonance Engine
│ (Resonance Engine)       │      https://your-project.workers.dev
│ Harmonic Ledger Backend  │      Status: ✅ LIVE
└──────────────────────────┘
```

### This Repository's Purpose

**`pi-forge-quantum-genesis`** serves as:
- ✅ **Backend API** — FastAPI services for Pi Network integration, payments, and quantum operations
- ✅ **Coordination Hub** — Documentation, governance, and multi-repo coordination
- ✅ **GitHub Agent Base** — Operational center for autonomous agents
- ✅ **Canon Preservation** — Home of the Canon of Autonomy principles

---

## 🚀 Deployment Options

### Vercel (Recommended for Frontend)

**Quick Deploy to Vercel:**
1. Click the button below or follow the [Vercel Deployment Guide](./VERCEL_DEPLOYMENT_GUIDE.md)
2. Configure environment variables (see below)
3. Deploy automatically via GitHub integration

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/onenoly1010/pi-forge-quantum-genesis)

**Features:**
- ✅ Mobile-optimized PWA with offline support
- ✅ Global CDN with Edge Network
- ✅ Automatic HTTPS and SSL
- ✅ One-click deployment
- ✅ Preview deployments on PRs
- ✅ Built-in analytics

**Setup:**
```bash
# Automated setup
./scripts/vercel-setup.sh

# Or manual deployment
npm install -g vercel
vercel login
vercel --prod
```

### Railway (Backend Services)

For backend Python services (FastAPI, Flask, Gradio), see [Production Deployment Guide](./docs/PRODUCTION_DEPLOYMENT.md)

---

## Quickstart Guide

### 1️⃣ Setup Environment

**For Frontend Development:**
```bash
# Install Node.js dependencies
npm install

# Build static assets
npm run build

# Serve locally (optional)
npx serve public -p 3000
```

**For Backend Development:**
```bash
# Setup Python environment
python3 -m venv venv
source venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
pip install -r server/requirements.txt
```

### 2️⃣ Environment Variables

Create a `.env` file (see `.env.example`):

```bash
# Required for Pi Network integration
PI_APP_SECRET=your-pi-network-app-secret

# Optional for monitoring
GUARDIAN_SLACK_WEBHOOK_URL=your-slack-webhook-url
SENDGRID_API_KEY=your-sendgrid-api-key
```

### 3️⃣ Launch the Application

**Frontend (Vercel/Static):**
```bash
npm run build
npx serve public
```

**Backend (Local Development):**
```bash
# FastAPI server
cd server
uvicorn main:app --reload --port 8000

# Flask dashboard
python app.py

# Gradio interface
python canticle_interface.py
```

---

## 📱 Mobile PWA Features

- **Installable**: Add to home screen on iOS/Android
- **Offline Support**: Service worker caching for offline access
- **Push Notifications**: Real-time updates (when enabled)
- **Responsive Design**: Optimized for all screen sizes
- **App-like Experience**: Full-screen mode, custom splash screen

---

## Module Summary

**New to Quantum Pi Forge?**

👉 **[START_HERE.md](./START_HERE.md)** — Your universal onboarding entry point

This comprehensive guide will help you:
1. Understand the constellation structure
2. Navigate the documentation
3. Find the right resources for your interests
4. Engage with the agent system
5. Make your first contribution

You are welcome here.

---

## 🤖 Autonomous Deployment

This repository includes complete autonomous deployment capabilities:

- **GitHub Actions CI/CD**: Automated testing and deployment
- **Health Monitoring**: Continuous deployment verification
- **Auto-Scaling**: Vercel Edge Network handles traffic spikes
- **Rollback Support**: One-click rollback to previous versions
- **Agent Oversight**: See [Autonomous Deployment Handoff](./AUTONOMOUS_DEPLOYMENT_HANDOFF.md)

### 🛡️ Guardian Decision System

Human-in-the-loop oversight for critical autonomous decisions:

- **Decision Requests**: Structured process for requesting Guardian approval
- **CLI Tool**: `scripts/create_guardian_decision.py` for creating decision requests
- **Python API**: Programmatic integration with autonomous systems
- **Documentation**: See [Guardian Decision README](./GUARDIAN_DECISION_README.md)

**Quick Example:**
```bash
python scripts/create_guardian_decision.py \
  --decision-id deployment_$(date +%s) \
  --decision-type Deployment \
  --priority High \
  --confidence 0.75 \
  --action "Deploy version X.Y.Z" \
  --reason "Requires Guardian review"
```

**Guardian Resources:**
- [Guardian Playbook](./docs/GUARDIAN_PLAYBOOK.md) - Complete operations guide
- [Guardian Quick Reference](./docs/GUARDIAN_QUICK_REFERENCE.md) - Fast decision-making
- [Guardian Decision Workflow](./docs/GUARDIAN_DECISION_WORKFLOW.md) - Process documentation
- [Example Guardian Decision](./docs/GUARDIAN_DECISION_EXAMPLE.md) - Sample approved request

### 📊 Live Deployment Health Dashboard

Real-time deployment status and health metrics are automatically tracked and updated:

- **📈 [CLEANUP_STATUS_DASHBOARD.md](./CLEANUP_STATUS_DASHBOARD.md)** — Live deployment health tracking
- **Auto-Updated**: Dashboard refreshes every 6 hours via GitHub Actions
- **Health Checks**: Monitors Public Site, Backend API, and Resonance Engine
- **Repository Metrics**: Tracks issues, PRs, commits, and workflow status

**What's Monitored:**
- Service availability and response times for all production deployments
- Repository activity metrics (commits, issues, pull requests)
- Automated cleanup workflow status (branch cleanup, stale PR management)
- Next scheduled update timestamps

The dashboard is maintained by the [`deployment-health-dashboard.yml`](.github/workflows/deployment-health-dashboard.yml) workflow, ensuring you always have current deployment status without manual intervention.

---

## 📚 Documentation

**📋 For complete deployment information, see [DEPLOYMENT_CONSOLIDATION.md](./DEPLOYMENT_CONSOLIDATION.md)**

**📖 Full Documentation Index**: [docs/index.md](./docs/index.md) — Complete navigation to all documentation resources

### Recent Major Updates

- **Feb 8, 2026**: [Comprehensive repository cleanup documentation](./docs/COMMIT_DD5AEBBC_SUMMARY.md) added (3,200+ lines)
  - Branch cleanup analysis and safeguards
  - Repository maintenance best practices
  - Deployment configuration improvements
  - Workflow fixes and dependency updates

### Vercel Configuration Note

---

## 🔧 Development

**Build Commands:**
```bash
npm run build        # Build for production
npm run typecheck    # TypeScript type checking
npm test             # Run test suite
```

**Testing:**
```bash
# Test Vercel build
pytest tests/test_vercel_build.py -v

# Verify deployment
./scripts/verify-vercel-deployment.sh https://your-deployment-url
```

---

## 🌐 Live Deployments

### Production Services

**Public Frontend:**
- **URL**: https://quantumpiforge.com
- **Repository**: [quantum-pi-forge-site](https://github.com/onenoly1010/quantum-pi-forge-site)
- **Status**: ✅ LIVE on Vercel/GitHub Pages

**Backend API (This Repository):**
- **Railway**: https://pi-forge-quantum-genesis.railway.app
- **Render**: https://pi-forge-quantum-genesis-1.onrender.com
- **Health Check**: `GET /health`
- **Status**: ✅ LIVE

**Resonance Engine:**
- **URL**: https://your-project.workers.dev
- **Repository**: [quantum-resonance-clean](https://github.com/onenoly1010/quantum-resonance-clean)
- **Status**: ✅ LIVE on Vercel

**📊 Real-Time Status**: Check [CLEANUP_STATUS_DASHBOARD.md](./CLEANUP_STATUS_DASHBOARD.md) for live deployment health and monitoring data.

### Quick Health Checks

```bash
# Backend API (Railway)
curl https://pi-forge-quantum-genesis.railway.app/health

# Backend API (Render)
curl https://pi-forge-quantum-genesis-1.onrender.com/health

# Resonance Engine
curl https://your-project.workers.dev/

# Public Site
curl -I https://quantumpiforge.com
```

---

## Notes

- ✅ Compatible with Vercel, Railway, Hugging Face Spaces, and Netlify
- ✅ Designed to sync with Pi Network wallet integration
- ✅ Mobile-first responsive design with PWA support
- ✅ Maintain directory integrity to avoid path conflicts
- ✅ Full autonomous deployment support for AI agents

---

## Credits

© 2025 Pi Forge Collective — Quantum Genesis Initiative  
**Lead**: Kris Olofson (onenoly1010)

**Built with**: FastAPI • Flask • Gradio • Vercel • Pi Network • Ethical AI

---

## License

MIT License - See [LICENSE](./LICENSE) for details
