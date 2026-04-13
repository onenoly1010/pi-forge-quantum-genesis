# Deployment Guide

> **📌 Note**: This document is part of the deployment documentation suite.  
> For the complete deployment guide, see the **[Deployment Dashboard](docs/DEPLOYMENT_DASHBOARD.md)**.

## 📋 Repository Purpose

**This repository (`pi-forge-quantum-genesis`) is the Backend API** for the Quantum Pi Forge ecosystem.

### Primary Functions:
- ✅ **Backend API Services** — FastAPI/Flask/Gradio servers for Pi Network integration
- ✅ **Payment Processing** — Pi Network payment webhook handling
- ✅ **Quantum Operations** — Fractal generation, resonance calculations, artistic APIs
- ✅ **Coordination Hub** — Documentation and governance center
- ✅ **GitHub Agent Base** — Operational base for autonomous agents

### Architecture Context:
```
User → quantum-pi-forge-site (Frontend) 
     → pi-forge-quantum-genesis (Backend API - THIS REPO)
     → quantum-resonance-clean (Resonance Engine)
```

---

## 🚀 Current Deployments

### Backend API (Production)

**Railway Deployment** (Primary):
- **URL**: https://pi-forge-quantum-genesis.railway.app
- **Health Check**: `GET /health`
- **Status**: ✅ ACTIVE
- **Configuration**: See [railway.toml](./railway.toml)

```bash
# Test Railway deployment
curl https://pi-forge-quantum-genesis.railway.app/health
```

**Render Deployment** (Alternative):
- **URL**: https://pi-forge-quantum-genesis-1.onrender.com
- **Health Check**: `GET /health`
- **Status**: ✅ ACTIVE
- **Configuration**: See [render.yaml](./render.yaml)

```bash
# Test Render deployment
curl https://pi-forge-quantum-genesis-1.onrender.com/health
```

### API Endpoints

**Available Endpoints:**
- `/health` — Health check (lightweight)
- `/api/payments/*` — Pi Network payment processing
- `/api/pi-webhooks/*` — Pi Network webhook receiver
- `/api/pi-network/status` — Configuration status
- `/api/fractal/generate` — Quantum fractal generation
- `/sacred-trinity/*` — Sacred Trinity integration endpoints

---

## ⚙️ Deployment Configuration

### Railway Configuration

See [railway.toml](./railway.toml) for complete configuration.

**Key Settings:**
- **Docker Build**: Uses `Dockerfile` in root directory
- **Start Command**: `python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Health Check Path**: `/health`
- **Health Check Timeout**: 100 seconds
- **Restart Policy**: ON_FAILURE with 10 max retries

**Required Environment Variables:**
```bash
# Core Configuration
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
SECRET_KEY=your-secret-key

# Pi Network Integration
PI_NETWORK_MODE=mainnet
PI_NETWORK_APP_ID=your-app-id
PI_NETWORK_API_KEY=your-api-key
PI_NETWORK_WEBHOOK_SECRET=your-webhook-secret

# Optional Services
SENTRY_DSN=your-sentry-dsn
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
```

**Deployment Steps:**
1. Connect Railway to GitHub repository
2. Configure environment variables in Railway dashboard
3. Railway automatically detects `railway.toml` and deploys
4. Monitor deployment at https://railway.app/dashboard

---

### Render Configuration

See [render.yaml](./render.yaml) for complete configuration.

**Key Settings:**
- **Service Type**: Web Service
- **Runtime**: Docker
- **Dockerfile Path**: `./Dockerfile`
- **Plan**: Free tier
- **Region**: Oregon
- **Health Check Path**: `/health`

**Required Environment Variables:**
Same as Railway configuration (see above).

**Deployment Steps:**
1. Connect Render to GitHub repository
2. Render automatically detects `render.yaml`
3. Configure environment variables in Render dashboard
4. Deploy and monitor at https://dashboard.render.com

---

## 🔧 Vercel Deployment (Optional Documentation Hosting)

**Note**: Vercel deployment is OPTIONAL and used primarily for:
- Static documentation hosting
- Development preview environments  
- Build verification in CI/CD

**This is NOT the primary production deployment method for the backend API.**

### When to Use Vercel for This Repo

✅ **Use Vercel if you want to**:
- Host static documentation pages
- Preview changes to HTML interfaces
- Test build processes

❌ **Do NOT use Vercel for**:
- Production backend API (use Railway or Render instead)
- Main application deployment
- Backend services requiring Python runtime

### Frontend Deployment

**For the main public-facing frontend**, use the separate repository:
- **Repository**: [quantum-pi-forge-site](https://github.com/onenoly1010/quantum-pi-forge-site)
- **URL**: https://quantumpiforge.com
- **Deployment**: Vercel/GitHub Pages

---

## 🔍 Health Checks & Monitoring

### Health Check Endpoints

**Primary Health Check:**
```bash
# Railway
curl https://pi-forge-quantum-genesis.railway.app/health

# Render
curl https://pi-forge-quantum-genesis-1.onrender.com/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "pi-forge-quantum-genesis",
  "timestamp": "2026-02-07T20:00:00Z"
}
```

### Monitoring

- **GitHub Actions**: Automated health checks run every 6 hours
- **Dashboard**: See [CLEANUP_STATUS_DASHBOARD.md](./CLEANUP_STATUS_DASHBOARD.md)
- **Service Status**: See [DEPLOYMENT_CONSOLIDATION.md](./DEPLOYMENT_CONSOLIDATION.md)

---

## 📚 Related Documentation

- **[DEPLOYMENT_CONSOLIDATION.md](./DEPLOYMENT_CONSOLIDATION.md)** — Complete deployment reference
- **[docs/DEPLOYMENT_DASHBOARD.md](./docs/DEPLOYMENT_DASHBOARD.md)** — Deployment operations dashboard
- **[docs/PRODUCTION_DEPLOYMENT.md](./docs/PRODUCTION_DEPLOYMENT.md)** — Production deployment guide
- **[README.md](./README.md)** — Repository overview and quickstart

---

## 🔧 Local Development

### Build Configuration (Vercel Optional)

If using Vercel for documentation hosting:

- **Framework**: None (static site with custom build)
- **Build Command**: `npm run build`
- **Output Directory**: `.vercel/output/static` (Vercel Build Output API v3)
- **Node.js Version**: 20.x

The build process:
1. Creates `.vercel/output/static` directory
2. Generates `config.json` with routing rules
3. Copies static HTML files
4. Copies static JavaScript files

### Backend Local Development

**Start Backend Services:**
```bash
# FastAPI server (Port 8000)
cd server
uvicorn main:app --reload --port 8000

# Flask dashboard (Port 5000)
python app.py

# Gradio interface (Port 7860)
python canticle_interface.py
```

### Local Testing

```bash
# Install dependencies
npm install
pip install -r server/requirements.txt

# Build static assets (if needed)
npm run build

# Test backend locally
cd server
pytest tests/

# Test health endpoint
curl http://localhost:8000/health
```

---

## 🎯 Quick Reference

### Service URLs
- **Railway Backend**: https://pi-forge-quantum-genesis.railway.app
- **Render Backend**: https://pi-forge-quantum-genesis-1.onrender.com
- **Public Frontend**: https://quantumpiforge.com
- **Resonance Engine**: https://your-project.workers.dev

### Configuration Files
- `railway.toml` — Railway deployment configuration
- `render.yaml` — Render deployment configuration
- `vercel.json` — Vercel configuration (optional)
- `Dockerfile` — Docker containerization
- `server/requirements.txt` — Python dependencies

### Key Endpoints
- `GET /health` — Health check
- `POST /api/payments/initiate` — Pi Network payment
- `POST /api/pi-webhooks/payment` — Payment webhook
- `GET /api/pi-network/status` — Pi Network status
