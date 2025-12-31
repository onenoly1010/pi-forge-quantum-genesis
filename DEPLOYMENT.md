# 🚀 Infrastructure — Simple Truth

## What Actually Runs

The Quantum Pi Forge operates with **3 core services**:

### 1. Railway (Backend API)
- **Service**: FastAPI Quantum Conduit
- **URL**: https://pi-forge-quantum-genesis.railway.app
- **Health Check**: `/health`
- **Configuration**: `railway.toml` + `Dockerfile`
- **Purpose**: Core backend logic, API endpoints

### 2. Supabase (Database)
- **Service**: PostgreSQL + Authentication
- **Access**: Private (environment variables)
- **Purpose**: Data persistence, user auth, real-time features

### 3. GitHub Pages (Public Portal)
- **Service**: Static site hosting
- **URL**: https://onenoly1010.github.io/quantum-pi-forge-site/
- **Repository**: `quantum-pi-forge-site`
- **Purpose**: Public-facing manifesto and documentation

---

## This Repository's Role

**⚠️ Important: This is a COORDINATION HUB, not a deployable application.**

**What this repo provides:**
- ✅ Governance center
- ✅ Documentation hub
- ✅ Multi-repo coordination
- ✅ GitHub Agent operations base
- ✅ Canon of Autonomy preservation

**What this repo does NOT provide:**
- ❌ Deployable frontend application
- ❌ Production web service
- ❌ User-facing interface

---

## Railway Deployment (Backend)

The backend runs on Railway using Docker containerization.

### Configuration
- **Dockerfile**: `Dockerfile` (multi-stage Python 3.11 build)
- **Config**: `railway.toml`
- **Start Command**: `python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Health Check**: `/health` endpoint (100s timeout)

### Environment Variables
Required in Railway dashboard:
- `SUPABASE_URL` — Supabase project URL
- `SUPABASE_KEY` — Supabase anon/public key
- `SECRET_KEY` — Application secret (generate random string)
- `PI_APP_SECRET` — Pi Network app secret

Optional:
- `GUARDIAN_SLACK_WEBHOOK_URL` — Slack alerts
- `MAILGUN_DOMAIN`, `MAILGUN_API_KEY` — Email alerts
- `SENDGRID_API_KEY`, `SENDGRID_FROM` — SendGrid emails
- `OPENAI_API_KEY` — AI features
- `ANTHROPIC_API_KEY` — AI features
- `SENTRY_DSN` — Error tracking

### Auto-Deploy
- Configured to deploy from `main` branch
- Docker builds automatically on push
- Health checks ensure deployment success

---

## Vercel (Optional Documentation)

This repo includes minimal Vercel configuration for:
- ✅ Build verification in CI/CD
- ✅ Optional static documentation hosting
- ✅ Development preview environments

**This is NOT a production deployment.**

### Configuration
- **File**: `vercel.json`
- **Build Command**: `npm run build`
- **Output**: Static documentation pages

### If You Want to Disconnect

If this repo was accidentally connected to Vercel:

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Find `pi-forge-quantum-genesis` project
3. Settings → General → Delete Project
4. Confirm deletion

The repository continues to function normally without Vercel.

---

## Health Monitoring

### Endpoints
- **Railway Health**: https://pi-forge-quantum-genesis.railway.app/health
- **Public Site**: https://onenoly1010.github.io/quantum-pi-forge-site/

### Automated Checks
- GitHub Actions workflows monitor deployments
- Health check failures trigger alerts
- See `.github/workflows/scheduled-monitoring.yml`

### Manual Verification
```bash
# Check Railway backend
curl https://pi-forge-quantum-genesis.railway.app/health

# Should return: {"status": "healthy", ...}
```

---

## Deployment Checklist

When deploying changes:

1. ✅ Test locally first
2. ✅ Verify environment variables
3. ✅ Push to branch, create PR
4. ✅ Review in GitHub Actions
5. ✅ Merge to `main` triggers deploy
6. ✅ Verify health endpoint
7. ✅ Check monitoring alerts

---

## Guardrails (Not Bureaucracy)

**Failures teach once, then become permanent guardrails:**

- Stale branches auto-deleted after 90 days (see workflows)
- Health monitoring prevents repeat failures
- Canon alignment checked on all changes
- Deployment failures trigger immediate alerts

**Philosophy:** Make best NOW, not later.

---

*Last Updated: Solstice 2025*  
*Status: ACTIVE / SIMPLIFIED*

**I AM.** 🏛️⚛️🔥
