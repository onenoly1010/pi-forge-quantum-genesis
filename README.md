Pi Forge Quantum Genesis — Relaunch v2.0

## Overview

**🌟 [START HERE](./START_HERE.md)** — New to Quantum Pi Forge? Begin with the universal onboarding guide.

**🌊 [Constellation Status: LIVE](./CONSTELLATION_ACTIVATION.md)** — The Quantum Pi Forge is activated and operational as of December 22, 2025.

**📜 [Read the Genesis Declaration](./GENESIS.md)** — The foundational seal of the Quantum Pi Forge ecosystem, minted at Solstice 2025.

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

- **Production**: https://pi-forge-quantum-genesis.vercel.app
- **Backend API**: https://quantumpiforge.com
- **Documentation**: https://github.com/onenoly1010/pi-forge-quantum-genesis

**📊 Real-Time Status**: Check [CLEANUP_STATUS_DASHBOARD.md](./CLEANUP_STATUS_DASHBOARD.md) for live deployment health and monitoring data.

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
