# Infrastructure Documentation

## Overview

This directory contains all infrastructure-as-code for deploying Pi Forge Quantum Genesis to Railway in an isolated testnet environment.

## Directory Structure

```
infra/
├── railway.toml                  # Railway deployment manifest
├── docker-compose.testnet.yml    # Local testnet orchestration
├── SECRETS.md                    # Secret documentation (no values)
├── railway/
│   └── README.md                 # Railway deployment guide
└── README.md                     # This file
```

## Quick Start

### Local Development (Testnet Staging)

```bash
# 1. Copy environment template
cp .env.testnet.example .env.testnet

# 2. Edit .env.testnet with your testnet credentials
# NEVER commit this file!

# 3. Start all services
docker-compose -f infra/docker-compose.testnet.yml up

# 4. Access services:
#    - Guardian Coordinator: http://localhost:8080/health
#    - FastAPI Server: http://localhost:8000/health
#    - Flask Dashboard: http://localhost:5000/health
#    - Gradio Interface: http://localhost:7860/
```

### Railway Deployment

See [infra/railway/README.md](railway/README.md) for comprehensive Railway deployment guide.

**Quick Deploy:**

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login and link project
railway login
railway link

# 3. Set environment variables via Railway UI
# See infra/SECRETS.md for required variables

# 4. Deploy
railway up
```

## Services

### 1. Guardian Coordinator (Port 8080)

**Purpose**: Ethical entropy filtering and validation consensus

**Key Features**:
- FastAPI-based validation API
- Module-level safety enforcement (APP_ENVIRONMENT=testnet)
- Redis stream processing for pulse validation
- Quorum-based consensus with configurable thresholds
- Zero-value enforcement (NFT_MINT_VALUE=0)

**Endpoints**:
- `GET /health` - Health check
- `GET /` - Service info
- `GET /sentinel/status` - Validation statistics
- `POST /validate` - Validate quantum pulse

**Docker**: `guardian-coordinator/docker/Dockerfile.guardian`

### 2. FastAPI Server (Port 8000)

**Purpose**: Primary production API with Supabase auth & WebSocket

**Key Features**:
- User authentication and registration
- WebSocket support for real-time updates
- Pi Network payment integration (testnet only)
- Supabase database integration

**Dockerfile**: `Dockerfile` (root)

### 3. Flask Dashboard (Port 5000)

**Purpose**: Quantum resonance visualization and template serving

**Key Features**:
- SVG-based visualization rendering
- Procedural art generation
- Template serving for HTML pages

**Dockerfile**: `Dockerfile.flask`

### 4. Gradio Interface (Port 7860)

**Purpose**: Ethical AI audit tool and interactive interface

**Key Features**:
- Interactive web UI for ethical audits
- Model evaluation capabilities
- Standalone operation mode

**Dockerfile**: `Dockerfile.gradio`

## Safety Features

### Mandatory Environment Variables

All services **MUST** have these set:

```bash
APP_ENVIRONMENT=testnet          # MUST be "testnet"
GUARDIAN_KILL_SWITCH=off         # "off" for normal operation
NFT_MINT_VALUE=0                 # MUST be "0" for testnet
```

### Safety Enforcement Layers

1. **Module-level checks**: Guardian coordinator validates environment at import time
2. **GitHub Actions gates**: Workflow aborts if environment != testnet
3. **Railway variables**: Environment variables validated before deployment
4. **Kill switch**: Emergency abort via GUARDIAN_KILL_SWITCH=on
5. **Mainnet gate**: FORCE_DEPLOY_TO_MAINNET prevents accidental mainnet deploys

### What Happens on Safety Violation?

- **Wrong APP_ENVIRONMENT**: Application refuses to start, exits with error
- **NFT_MINT_VALUE != 0**: Deployment aborted in CI, application refuses to start
- **GUARDIAN_KILL_SWITCH=on**: All deployments blocked, services refuse to start
- **FORCE_DEPLOY_TO_MAINNET set**: Workflow aborts (testnet workflows only)

## GitHub Actions Workflows

### deploy-testnet.yml

**Triggers**:
- Push to `main` branch
- Manual workflow dispatch

**Jobs**:
1. **safety-gate**: Pre-deployment validation
2. **tests**: Run pytest for all services
3. **build-images**: Build and push Docker images to GHCR
4. **deploy**: Deploy to Railway with health checks
5. **smoke-tests**: Post-deployment validation

**Safety Checks**:
- APP_ENVIRONMENT == "testnet"
- NFT_MINT_VALUE == "0" or unset
- GUARDIAN_KILL_SWITCH != "on"
- FORCE_DEPLOY_TO_MAINNET != "true"

### rollback.yml

**Trigger**: Manual workflow dispatch only

**Inputs**:
- `service`: Which service to rollback (or "all")
- `deployment_id`: Railway deployment ID (optional)
- `image_tag`: Docker image tag (optional)
- `confirmation`: Must type "ROLLBACK" exactly
- `reason`: Audit trail description

**Jobs**:
1. **validate-rollback**: Validate inputs and confirmation
2. **execute-rollback**: Perform Railway rollback
3. **post-rollback-validation**: Verify services are healthy

## Environment Variables

See [SECRETS.md](SECRETS.md) for comprehensive list of all required environment variables and secrets.

### Critical Variables

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `APP_ENVIRONMENT` | ✅ | testnet | Environment identifier |
| `GUARDIAN_KILL_SWITCH` | ✅ | off | Emergency abort |
| `NFT_MINT_VALUE` | ✅ | 0 | Zero-value enforcement |
| `SUPABASE_URL` | ✅ | - | Supabase project URL |
| `SUPABASE_KEY` | ✅ | - | Supabase anon key |
| `JWT_SECRET` | ✅ | - | JWT signing secret |
| `PI_TESTNET_API_KEY` | ✅ | - | Pi Network testnet key |
| `RAILWAY_API_KEY` | CI only | - | Railway API token |
| `RAILWAY_PROJECT_ID` | CI only | - | Railway project ID |

## Architecture Diagrams

### Service Communication Flow

```
┌─────────────────┐
│   GitHub Push   │
└────────┬────────┘
         │
         v
┌─────────────────────────────────────────────────────┐
│          GitHub Actions CI/CD Pipeline              │
│  ┌──────────┐  ┌───────┐  ┌───────┐  ┌──────────┐ │
│  │  Safety  │→ │ Tests │→ │ Build │→ │  Deploy  │ │
│  │   Gate   │  │       │  │       │  │          │ │
│  └──────────┘  └───────┘  └───────┘  └──────────┘ │
└────────────────────────┬────────────────────────────┘
                         │
                         v
              ┌──────────────────────┐
              │   Railway Platform   │
              └──────────────────────┘
                         │
         ┌───────────────┼───────────────┬──────────┐
         v               v               v          v
┌─────────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│  Guardian   │  │ FastAPI  │  │  Flask   │  │  Gradio  │
│ Coordinator │  │  Server  │  │Dashboard │  │Interface │
│   :8080     │  │  :8000   │  │  :5000   │  │  :7860   │
└──────┬──────┘  └────┬─────┘  └────┬─────┘  └──────────┘
       │              │              │
       └──────────────┼──────────────┘
                      │
                      v
              ┌───────────────┐
              │  Redis Cache  │
              │    :6379      │
              └───────────────┘
```

### Deployment Pipeline

```
┌──────────┐
│   Code   │
│  Commit  │
└─────┬────┘
      │
      v
┌─────────────────┐       ┌──────────────┐
│  Safety Gate    │──X───→│   Abort if   │
│  - APP_ENV      │       │   - Not      │
│  - Kill Switch  │       │     testnet  │
│  - NFT Value    │       │   - Kill ON  │
│  - Secrets      │       │   - NFT != 0 │
└────────┬────────┘       └──────────────┘
         │
         ✓ Pass
         │
         v
┌─────────────────┐       ┌──────────────┐
│  Run Tests      │──X───→│  Abort if    │
│  - Guardian     │       │  tests fail  │
│  - FastAPI      │       │              │
│  - Flask        │       └──────────────┘
└────────┬────────┘
         │
         ✓ Pass
         │
         v
┌─────────────────┐       ┌──────────────┐
│ Build Images    │──────→│   Push to    │
│  - 4 services   │       │     GHCR     │
│  - Multi-stage  │       │              │
└────────┬────────┘       └──────────────┘
         │
         ✓ Complete
         │
         v
┌─────────────────┐       ┌──────────────┐
│ Deploy Railway  │──────→│  Health      │
│  - CLI deploy   │       │  Checks      │
│  - Set vars     │       │   - /health  │
└────────┬────────┘       └──────┬───────┘
         │                       │
         │    ✓ Healthy          │
         └───────────────────────┘
                   │
                   v
         ┌─────────────────┐
         │  Smoke Tests    │
         │   - Endpoints   │
         │   - Validation  │
         └────────┬────────┘
                  │
                  ✓ Pass
                  │
                  v
         ┌─────────────────┐
         │   Deployment    │
         │    Complete     │
         └─────────────────┘
```

## Testing

### Run All Tests Locally

```bash
# Guardian coordinator
cd guardian-coordinator
pytest tests/ -v

# Main repository tests
cd ..
pytest tests/test_health_endpoints.py -v

# Validate infrastructure YAML
python3 -c "import yaml; yaml.safe_load(open('infra/railway.toml'))"
python3 -c "import yaml; yaml.safe_load(open('infra/docker-compose.testnet.yml'))"
```

### Manual Service Testing

```bash
# Test guardian coordinator
cd guardian-coordinator
APP_ENVIRONMENT=testnet \
GUARDIAN_KILL_SWITCH=off \
NFT_MINT_VALUE=0 \
python guardian_api.py

# In another terminal
curl http://localhost:8080/health
curl -X POST http://localhost:8080/validate \
  -H "Content-Type: application/json" \
  -d '{
    "pulse_id": "test-001",
    "ethical_score": 0.95,
    "qualia_impact": 0.5,
    "resonance_value": 0.8
  }'
```

## Troubleshooting

### Services Won't Start

**Check environment variables**:
```bash
# Verify all required vars are set
railway variables --service guardian-coordinator
```

**Check logs**:
```bash
railway logs --service guardian-coordinator --tail 100
```

**Verify safety settings**:
```bash
# Must output "testnet"
railway run echo $APP_ENVIRONMENT

# Must output "0"
railway run echo $NFT_MINT_VALUE

# Must output "off"
railway run echo $GUARDIAN_KILL_SWITCH
```

### Deployment Fails Safety Checks

1. Review GitHub Actions logs
2. Verify secrets are set correctly in GitHub repository settings
3. Check Railway environment variables match requirements
4. Ensure no `FORCE_DEPLOY_TO_MAINNET` secret is set

### Rollback Needed

Use manual rollback workflow:

```bash
# Via GitHub UI
Actions → Rollback → Run workflow
  - Service: guardian-coordinator
  - Confirmation: ROLLBACK
  - Reason: Describe issue

# Via gh CLI
gh workflow run rollback.yml \
  -f service=guardian-coordinator \
  -f confirmation=ROLLBACK \
  -f reason="Deployment issue detected"
```

## Security Best Practices

### ✅ DO

- Always use testnet environment for this deployment
- Rotate secrets quarterly
- Review Railway logs regularly
- Test locally before deploying
- Use `.env.testnet` for local testing (gitignored)
- Set explicit GITHUB_TOKEN permissions in workflows
- Enable 2FA on all accounts (Railway, GitHub, Supabase)

### ❌ DON'T

- Commit secrets to git
- Use mainnet credentials in testnet
- Set NFT_MINT_VALUE to non-zero
- Disable kill switch without good reason
- Share API keys via insecure channels
- Use production Supabase project for testnet
- Mix testnet and mainnet environment variables

## Maintenance

### Updating Dependencies

```bash
# Guardian coordinator
cd guardian-coordinator
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt

# Main application
pip install --upgrade -r server/requirements.txt
pip freeze > server/requirements.txt
```

### Rotating Secrets

1. Generate new secret
2. Update in Railway UI
3. Update in GitHub Secrets
4. Deploy to activate new secret
5. Document rotation in `SECRETS.md` audit log

### Monitoring

Railway provides built-in metrics:
- CPU usage
- Memory usage
- Network I/O
- Request counts
- Error rates

Access via: Railway Project → Service → Metrics tab

## Support

- **Railway**: https://railway.app/help
- **GitHub Actions**: https://docs.github.com/en/actions
- **Guardian Coordinator**: See `guardian-coordinator/tests/`
- **Repository Issues**: https://github.com/onenoly1010/pi-forge-quantum-genesis/issues

## Version History

- **v1.0.0** (Current): Initial testnet deployment infrastructure
  - Guardian coordinator service
  - Railway deployment manifests
  - GitHub Actions CI/CD
  - Safety enforcement layers
  - Comprehensive testing

## License

See repository root LICENSE file.
