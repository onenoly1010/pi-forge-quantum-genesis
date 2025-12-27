# 🚀 Deployment Guide - Railway, Vercel, GitHub Pages

**Last Updated**: December 2025

Complete deployment instructions for all Quantum Pi Forge services across multiple platforms.

---

## 🎯 Deployment Overview

### Platforms

- **Railway** - FastAPI backend (primary)
- **Vercel** - Frontend and serverless functions
- **GitHub Pages** - Static site hosting
- **Docker** - Containerized deployment

### Services

The [[Sacred Trinity]] services deploy to:
- **FastAPI** (Port 8000) → Railway
- **Flask** (Port 5000) → Railway or Vercel
- **Gradio** (Port 7860) → Railway or Spaces

---

## 🚂 Railway Deployment

### Prerequisites

- Railway account
- GitHub repository connected
- Environment variables ready

### Setup

**1. Create Project**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link project
railway link
```

**2. Configure Environment**

In Railway dashboard, add variables:
```bash
# Database
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
DATABASE_URL=postgresql://...

# Pi Network
PI_NETWORK_MODE=mainnet
PI_NETWORK_APP_ID=your-app-id
PI_NETWORK_API_KEY=your-api-key
PI_NETWORK_WEBHOOK_SECRET=your-secret

# Security
JWT_SECRET=your-jwt-secret
SECRET_KEY=your-secret-key
```

**3. Deploy**
```bash
# Via CLI
railway up

# Or connect GitHub for auto-deploy
# Push to main branch triggers deployment
```

### Health Check

```bash
curl https://your-app.railway.app/health
# Expected: "OK"
```

---

## ▲ Vercel Deployment

### Prerequisites

- Vercel account
- GitHub repository connected

### Setup

**1. Install Vercel CLI**
```bash
npm install -g vercel
```

**2. Configure `vercel.json`**

Already configured in repository:
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "public",
  "framework": null
}
```

**3. Deploy**
```bash
# Production
vercel --prod

# Preview
vercel
```

### Environment Variables

Add in Vercel dashboard:
```bash
PI_APP_SECRET=your-secret
# Other sensitive vars
```

---

## 📄 GitHub Pages Deployment

### Prerequisites

- GitHub repository
- Pages enabled in settings

### Setup

**1. Enable Pages**
- Go to repository settings
- Enable GitHub Pages
- Select branch: `gh-pages` or `main`
- Select folder: `/` or `/docs`

**2. Build & Deploy**
```bash
# Build static site
npm run build

# Deploy (if using gh-pages branch)
git checkout gh-pages
cp -r public/* .
git add .
git commit -m "Deploy site"
git push origin gh-pages
```

**3. Custom Domain** (Optional)
- Add `CNAME` file with domain
- Configure DNS A records

---

## 🐳 Docker Deployment

### Build Images

```bash
# FastAPI
docker build -f Dockerfile -t quantum-fastapi .

# Flask
docker build -f Dockerfile.flask -t quantum-flask .

# Gradio
docker build -f Dockerfile.gradio -t quantum-gradio .
```

### Run Containers

```bash
# Using docker-compose
docker-compose up -d

# Or individually
docker run -p 8000:8000 --env-file .env quantum-fastapi
docker run -p 5000:5000 --env-file .env quantum-flask
docker run -p 7860:7860 --env-file .env quantum-gradio
```

---

## 🔒 Security Configuration

### Secrets Management

**Never commit**:
- API keys
- Database passwords
- JWT secrets
- Webhook secrets

**Use**:
- Railway environment variables
- Vercel environment variables
- GitHub Secrets (for CI/CD)
- `.env` files (local only, gitignored)

### HTTPS/SSL

All platforms provide automatic HTTPS:
- **Railway**: Automatic SSL
- **Vercel**: Automatic SSL
- **GitHub Pages**: Automatic SSL (if custom domain)

---

## 📊 Monitoring

### Health Endpoints

Monitor deployment health:
```bash
# FastAPI
curl https://your-app.railway.app/health

# Check all services
curl https://your-app.railway.app/api/health
```

### Logs

**Railway**:
```bash
railway logs
railway logs --follow
```

**Vercel**:
```bash
vercel logs
vercel logs [deployment-url]
```

---

## 🔄 Continuous Deployment

### Auto-Deploy from GitHub

**Railway**:
1. Connect GitHub in dashboard
2. Select repository and branch
3. Auto-deploys on push to main

**Vercel**:
1. Import project from GitHub
2. Configure build settings
3. Auto-deploys on push to main

### Manual Deployment

```bash
# Railway
railway up

# Vercel
vercel --prod
```

---

## 🎯 Deployment Checklist

Before deploying to production:

- [ ] All environment variables configured
- [ ] Database migrations run
- [ ] Pi Network webhook configured
- [ ] Health endpoints responding
- [ ] HTTPS working
- [ ] Custom domain configured (if needed)
- [ ] Monitoring enabled
- [ ] Logs accessible
- [ ] Backup strategy in place
- [ ] Rollback plan documented

---

## 🆘 Troubleshooting

### Build Failures

Check:
- Build logs in platform dashboard
- Dependencies in `requirements.txt`
- Node version compatibility
- Environment variable presence

### Runtime Errors

Check:
- Application logs
- Database connectivity
- API key validity
- Network/firewall issues

### Performance Issues

Monitor:
- Response times
- Error rates
- Resource usage
- Database queries

**Full guide**: [[Troubleshooting]]

---

## 📚 Platform Documentation

- **Railway**: https://docs.railway.app
- **Vercel**: https://vercel.com/docs
- **GitHub Pages**: https://docs.github.com/pages
- **Docker**: https://docs.docker.com

---

## See Also

- [[Sacred Trinity]] - Service architecture
- [[Monitoring Observability]] - Monitoring setup
- [[Runbook Index]] - Operational commands
- [[Troubleshooting]] - Common issues

---

[[Home]] | [[Sacred Trinity]] | [[Monitoring Observability]]
