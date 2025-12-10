# Railway Deployment Guide

## Overview

This guide covers deploying the Pi Forge Quantum Genesis stack to Railway in an isolated testnet environment.

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **Railway CLI**: Install via `npm install -g @railway/cli` or `brew install railway`
3. **GitHub Repository**: Ensure repository is connected to Railway
4. **Testnet Credentials**: Have all testnet API keys and secrets ready (see `infra/SECRETS.md`)

## Initial Setup

### 1. Create Railway Project

```bash
# Login to Railway
railway login

# Create new project (or link existing)
railway init

# Link to your GitHub repository
railway link
```

### 2. Configure Environment Variables

**CRITICAL**: All environment variables must be set via Railway UI or CLI. **NEVER** commit secrets to git.

Navigate to Railway Project → Settings → Variables, and add the following for each service:

#### Global Environment Variables (All Services)

```bash
APP_ENVIRONMENT=testnet
GUARDIAN_KILL_SWITCH=off
NFT_MINT_VALUE=0
LOG_LEVEL=INFO
```

#### Guardian Coordinator Service

```bash
GUARDIAN_ID=guardian-railway-001
QUORUM_THRESHOLD=0.70
ETHICAL_ENTROPY_MAX=0.05
REDIS_URL=${{Redis.REDIS_URL}}  # Railway internal service reference
PORT=8080
```

#### FastAPI Server Service

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-testnet-anon-key
JWT_SECRET=your-secure-random-jwt-secret
PI_NETWORK_MODE=testnet
PI_TESTNET_API_KEY=your-pi-testnet-api-key
PI_SANDBOX_MODE=true
PORT=8000
```

#### Flask Dashboard Service

```bash
FLASK_ENV=development
FLASK_SECRET_KEY=your-flask-secret-key
PORT=5000
```

#### Gradio Interface Service

```bash
GRADIO_SERVER_NAME=0.0.0.0
GRADIO_SERVER_PORT=7860
PORT=7860
```

### 3. Add Redis Service

Railway supports adding Redis as a service:

1. Go to Railway Project → New → Database → Redis
2. Note the internal URL (automatically available as `${{Redis.REDIS_URL}}`)
3. Reference in other services using the variable syntax

## Deployment Methods

### Method 1: Automatic Deployment (GitHub Actions)

The repository includes a GitHub Actions workflow that automatically deploys on push to `main`:

```bash
# Merge your changes to main
git checkout main
git merge your-feature-branch
git push origin main

# GitHub Actions will automatically:
# 1. Run tests
# 2. Build Docker images
# 3. Push to GHCR
# 4. Deploy to Railway testnet
```

See `.github/workflows/deploy-testnet.yml` for workflow details.

### Method 2: Manual Deployment (Railway CLI)

For one-off deploys or testing:

```bash
# Deploy all services
railway up

# Deploy specific service
railway up --service guardian-coordinator

# Check deployment status
railway status

# View logs
railway logs --service fastapi-server

# Open service in browser
railway open
```

### Method 3: Railway UI

1. Navigate to your Railway project
2. Click on service (e.g., `guardian-coordinator`)
3. Go to "Deployments" tab
4. Click "Deploy" → "Deploy Latest Commit"

## Health Checks

After deployment, verify all services are healthy:

```bash
# Guardian Coordinator
curl https://your-guardian.railway.app/health

# FastAPI Server
curl https://your-fastapi.railway.app/health

# Flask Dashboard
curl https://your-flask.railway.app/health

# Gradio Interface
curl https://your-gradio.railway.app/
```

Expected response for Guardian:
```json
{
  "status": "healthy",
  "service": "Guardian Coordinator",
  "environment": "testnet",
  "kill_switch": "off",
  "nft_value": "0"
}
```

## Rollback Procedures

### Using Railway UI

1. Navigate to Service → Deployments
2. Find the last known good deployment
3. Click "⋯" menu → "Rollback to this deployment"

### Using Railway CLI

```bash
# List recent deployments
railway deployment list --service guardian-coordinator

# Rollback to specific deployment
railway deployment rollback <deployment-id>
```

### Using GitHub Actions Workflow

Trigger the manual rollback workflow:

```bash
# Via GitHub UI: Actions → Rollback → Run workflow
# Or via gh CLI:
gh workflow run rollback.yml \
  -f service=guardian-coordinator \
  -f deployment_id=<deployment-id> \
  -f confirmation=true
```

## Monitoring

### View Logs

```bash
# Real-time logs for specific service
railway logs --service guardian-coordinator --follow

# Last 100 lines
railway logs --service fastapi-server --tail 100

# Filter by timestamp
railway logs --since 1h
```

### Metrics

Railway provides built-in metrics:
- CPU usage
- Memory usage
- Network traffic
- Request counts

Access via: Project → Service → Metrics

## Troubleshooting

### Service Won't Start

1. **Check environment variables**: Ensure all required secrets are set
2. **View build logs**: `railway logs --build`
3. **Verify Dockerfile**: Test locally with `docker build -f <dockerfile> .`
4. **Check health endpoint**: Ensure `/health` returns 200

### Environment Variable Issues

```bash
# List all environment variables for a service
railway variables --service guardian-coordinator

# Set variable via CLI
railway variables set APP_ENVIRONMENT=testnet --service guardian-coordinator

# Delete variable
railway variables delete OLD_VARIABLE --service guardian-coordinator
```

### Connection Issues Between Services

Railway services can reference each other using internal URLs:

```bash
# Redis URL (automatic)
REDIS_URL=${{Redis.REDIS_URL}}

# Custom service reference
GUARDIAN_URL=${{guardian-coordinator.RAILWAY_PRIVATE_DOMAIN}}
```

### Deployment Fails Safety Checks

If deployment is blocked by safety checks:

1. **Verify APP_ENVIRONMENT=testnet**: Must be exactly "testnet"
2. **Check GUARDIAN_KILL_SWITCH**: Must be "off"
3. **Verify NFT_MINT_VALUE=0**: Must be exactly "0" (string)
4. **Review workflow logs**: `gh run view <run-id>`

## Safety Reminders

⚠️ **CRITICAL SAFETY RULES**:

1. ✅ **DO**: Always deploy to testnet environment first
2. ✅ **DO**: Verify NFT_MINT_VALUE=0 before any deployment
3. ✅ **DO**: Check GUARDIAN_KILL_SWITCH is "off" for normal operations
4. ❌ **DON'T**: Set APP_ENVIRONMENT to anything other than "testnet"
5. ❌ **DON'T**: Commit secrets to git (use Railway UI or GitHub Secrets)
6. ❌ **DON'T**: Set FORCE_DEPLOY_TO_MAINNET without 5/5 guardian approvals

## Advanced Configuration

### Custom Domains

1. Railway Project → Service → Settings → Domains
2. Add custom domain
3. Configure DNS CNAME record
4. Railway automatically provisions SSL certificate

### Auto-scaling

Railway supports horizontal scaling:

```bash
# Via railway.toml
[deploy]
numReplicas = 3

# Or via UI: Service → Settings → Replicas
```

### Resource Limits

Configure CPU and memory limits in `railway.toml`:

```toml
[deploy.resources]
cpu = "2000m"  # 2 vCPUs
memory = "2Gi"  # 2 GB RAM
```

## Support

- **Railway Documentation**: https://docs.railway.app
- **Railway Discord**: https://discord.gg/railway
- **Repository Issues**: https://github.com/onenoly1010/pi-forge-quantum-genesis/issues
- **Secrets Documentation**: See `infra/SECRETS.md`

## Next Steps

1. ✅ Set up all environment variables in Railway
2. ✅ Test deployment with `railway up`
3. ✅ Verify health checks for all services
4. ✅ Configure GitHub Actions secrets for automated deployments
5. ✅ Set up monitoring and alerts
6. ✅ Document your Railway project ID for team members
