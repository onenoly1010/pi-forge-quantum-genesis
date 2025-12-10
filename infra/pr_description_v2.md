# INFRA-002: Fully Wired Testnet Deployment — Railway + GH Actions + Rollback

## 🎯 Overview

This PR adds a complete, production-ready testnet deployment infrastructure for Pi Forge Quantum Genesis with multi-layered safety controls, automated workflows, and comprehensive documentation.

## 🏗️ What's Included

### Infrastructure Configuration

- ✅ **Railway Multi-Service Configuration** (`infra/railway.toml`)
  - Guardian Coordinator service
  - FastAPI Server service
  - Flask Dashboard service
  - Gradio Interface service
  - Dockerfile-based builds
  - Health checks configured

- ✅ **Local Testnet Environment** (`infra/docker-compose.testnet.yml`)
  - All four application services
  - PostgreSQL database
  - Health checks and dependencies
  - Volume persistence
  - Network isolation

### GitHub Actions Workflows

- ✅ **Testnet Deployment Workflow** (`.github/workflows/deploy-testnet.yml`)
  - **Safety Gate Job**: Validates all deployment prerequisites
    - Confirmation phrase required: `CONFIRM-TESTNET-DEPLOY`
    - Environment must be `testnet`
    - `NFT_MINT_VALUE` must equal `0`
    - `GUARDIAN_KILL_SWITCH` must be `off`
    - `FORCE_DEPLOY_TO_MAINNET` must NOT exist
  - **Test & Build Job**: Runs tests and builds Docker images
  - **Deploy Job**: Deploys to Railway with environment variables
  - **Smoke Test Job**: Validates deployment health
  - **Mark Deployment Job**: Creates deployment record

- ✅ **Rollback Workflow** (`.github/workflows/rollback.yml`)
  - Manual rollback to specific deployment/commit
  - Confirmation required: `CONFIRM-ROLLBACK`
  - Reason documentation mandatory
  - Automatic team notification via GitHub issue
  - Per-service rollback support

### Testing & Validation

- ✅ **Smoke Test Script** (`scripts/smoke_test.sh`)
  - Health endpoint validation
  - JSON response verification
  - API documentation check
  - Environment configuration verification
  - Color-coded output
  - Retry logic for reliability

### Documentation

- ✅ **Infrastructure Guide** (`infra/README.md`)
  - Architecture overview
  - Quick start instructions
  - Safety controls documentation
  - Deployment workflow diagram
  - Monitoring guidance
  - Emergency procedures

- ✅ **Secrets Documentation** (`infra/SECRETS.md`)
  - Complete list of required secrets
  - Setup instructions with examples
  - Security best practices
  - Secret rotation procedures
  - Emergency revocation steps
  - Pre-deployment checklist

- ✅ **Railway Guide** (`infra/railway/README.md`)
  - Railway-specific setup
  - Service configuration
  - Deployment methods
  - Monitoring and logging
  - Troubleshooting guide
  - Cost management tips

## 🔒 Safety Controls

### Mandatory Enforcement

All deployments enforce these safety requirements:

1. **Environment Restriction**
   - Only `testnet` environment allowed
   - Deployment aborts if mainnet requested

2. **Zero-Value Transactions**
   - `NFT_MINT_VALUE` must be exactly `"0"`
   - Prevents any real Pi Network value transfers
   - Workflow validates before deployment

3. **Kill Switch Check**
   - `GUARDIAN_KILL_SWITCH` must be `"off"`
   - Provides emergency stop mechanism
   - Blocks all deployments when activated

4. **Mainnet Protection**
   - `FORCE_DEPLOY_TO_MAINNET` must NOT exist
   - Prevents accidental mainnet deployment
   - Mainnet requires separate PR with 5/5 guardian approval

5. **Manual Confirmation**
   - Explicit confirmation phrase required
   - Prevents accidental deployments
   - Documented in workflow inputs

## 📋 Required Secrets

Before deploying, configure these GitHub repository secrets:

### Railway Configuration
- `RAILWAY_TOKEN` - Railway API token
- `RAILWAY_PROJECT_ID` - Railway project identifier

### Testnet Environment
- `TESTNET_SUPABASE_URL` - Testnet Supabase project URL
- `TESTNET_SUPABASE_KEY` - Testnet Supabase anonymous key
- `TESTNET_JWT_SECRET` - JWT signing secret (64 chars)
- `TESTNET_BASE_URL` - Deployed testnet base URL

### Deployment Safety
- `NFT_MINT_VALUE` - **MUST BE "0"**
- `GUARDIAN_KILL_SWITCH` - Set to "off" (or "on" to block deployments)

See [infra/SECRETS.md](infra/SECRETS.md) for detailed setup instructions.

## 🚀 Deployment Instructions

### Option 1: GitHub Actions UI (Recommended)

1. **Configure Secrets** (one-time setup)
   ```bash
   gh secret set RAILWAY_TOKEN --body "<your-token>"
   gh secret set RAILWAY_PROJECT_ID --body "<your-project-id>"
   gh secret set TESTNET_SUPABASE_URL --body "<testnet-url>"
   gh secret set TESTNET_SUPABASE_KEY --body "<testnet-key>"
   gh secret set TESTNET_JWT_SECRET --body "$(openssl rand -hex 32)"
   gh secret set TESTNET_BASE_URL --body "<testnet-url>"
   gh secret set NFT_MINT_VALUE --body "0"
   gh secret set GUARDIAN_KILL_SWITCH --body "off"
   ```

2. **Run Deployment Workflow**
   - Navigate to **Actions** → **Deploy to Testnet (Railway)**
   - Click **Run workflow**
   - Select branch: `infra/testnet-deploy-v2`
   - Environment: `testnet`
   - Confirmation: `CONFIRM-TESTNET-DEPLOY`
   - Click **Run workflow**

3. **Monitor Deployment**
   - Watch workflow progress in Actions tab
   - Review job outputs for any issues
   - Check smoke test results

4. **Verify Deployment**
   ```bash
   # Run smoke tests
   TESTNET_URL="<your-testnet-url>" ./scripts/smoke_test.sh
   ```

### Option 2: GitHub CLI

```bash
# Deploy via CLI
gh workflow run deploy-testnet.yml \
  --ref infra/testnet-deploy-v2 \
  -f requested_environment=testnet \
  -f confirm_safety="CONFIRM-TESTNET-DEPLOY"

# Monitor workflow
gh run watch

# Run smoke tests
TESTNET_URL="<your-testnet-url>" ./scripts/smoke_test.sh
```

### Option 3: Local Testing First

```bash
# Test locally with docker-compose
cd infra
export TESTNET_SUPABASE_URL="<your-url>"
export TESTNET_SUPABASE_KEY="<your-key>"
export TESTNET_JWT_SECRET="<your-secret>"
export NFT_MINT_VALUE=0
export GUARDIAN_KILL_SWITCH=off

docker-compose -f docker-compose.testnet.yml up

# Run smoke tests against local
TESTNET_URL="http://localhost:8000" ../scripts/smoke_test.sh
```

## 🔄 Rollback Procedure

If issues occur after deployment:

### Via GitHub Actions UI

1. Navigate to **Actions** → **Rollback Testnet Deployment**
2. Click **Run workflow**
3. Enter target deployment ID or commit SHA
4. Confirmation: `CONFIRM-ROLLBACK`
5. Reason: Brief description of why
6. Click **Run workflow**

### Via GitHub CLI

```bash
gh workflow run rollback.yml \
  -f target_deployment="<commit-sha-or-deployment-id>" \
  -f confirm_rollback="CONFIRM-ROLLBACK" \
  -f reason="Brief description of issue"
```

## 🧪 Testing

### Pre-Deployment Testing

```bash
# Run unit tests
pytest tests/ -v

# Test docker-compose configuration
cd infra
docker-compose -f docker-compose.testnet.yml config

# Build images locally
docker-compose -f docker-compose.testnet.yml build
```

### Post-Deployment Validation

```bash
# Run smoke tests
TESTNET_URL="<testnet-url>" ./scripts/smoke_test.sh

# Manual health checks
curl https://<testnet-url>/
curl https://<testnet-url>/health
curl https://<testnet-url>/docs
```

## 📊 Monitoring

### Health Endpoints

- **FastAPI**: `GET /` and `GET /health`
- **Flask Dashboard**: `GET /` and `GET /health`
- **Gradio Interface**: `GET /`
- **Guardian Coordinator**: `GET /health`

### Railway Monitoring

```bash
# View deployment logs
railway logs --environment testnet --follow

# Check service status
railway status --environment testnet

# View metrics
# Use Railway dashboard for CPU, memory, network graphs
```

## 🔍 Files Changed

```
infra/
├── railway.toml                          # New: Railway service config
├── docker-compose.testnet.yml            # New: Local testnet compose
├── README.md                             # New: Infrastructure docs
├── SECRETS.md                            # New: Secrets documentation
├── railway/
│   └── README.md                         # New: Railway-specific guide
└── pr_description_v2.md                  # New: This PR description

.github/workflows/
├── deploy-testnet.yml                    # New: Deployment workflow
└── rollback.yml                          # New: Rollback workflow

scripts/
└── smoke_test.sh                         # New: Smoke test script
```

## ✅ Pre-Merge Checklist

- [x] All files added with correct content
- [x] No secrets or tokens committed to repository
- [x] Workflows include all safety gates
- [x] Documentation is comprehensive
- [x] Smoke test script is executable
- [x] Docker compose configuration validated
- [x] Railway configuration reviewed
- [x] Placeholder values used for all secrets
- [x] Safety constraints documented
- [x] Rollback procedure tested (dry-run)

## 🚨 Important Notes

### Testnet-Only Deployment

⚠️ This infrastructure is **STRICTLY FOR TESTNET ONLY**. Mainnet deployment requires:

1. Separate PR with `infra/mainnet-*` prefix
2. Comprehensive security audit
3. Guardian review and 5/5 approval
4. Production readiness checklist
5. Separate Railway project and credentials
6. Additional safety controls and monitoring

### No Secrets Committed

✅ This PR contains **NO SECRETS**. All sensitive values use:
- Placeholder references like `<your-token>`
- GitHub Secrets references like `${{ secrets.RAILWAY_TOKEN }}`
- Environment variable templates like `${TESTNET_SUPABASE_URL}`

### Safety First

All workflows enforce:
- ✅ Testnet environment only
- ✅ Zero-value transactions (`NFT_MINT_VALUE=0`)
- ✅ Guardian kill switch check
- ✅ No mainnet access
- ✅ Manual confirmation required
- ✅ Comprehensive validation

## 📚 Next Steps After Merge

1. **Configure Repository Secrets**
   - Follow instructions in `infra/SECRETS.md`
   - Use `gh secret set` or GitHub Settings UI

2. **Set Up Railway Project**
   - Create Railway project
   - Configure services per `infra/railway/README.md`
   - Set environment variables

3. **Test Deployment Workflow**
   - Run deployment to testnet
   - Validate all safety gates
   - Verify smoke tests pass

4. **Monitor and Iterate**
   - Watch Railway metrics
   - Review logs for issues
   - Refine configuration as needed

## 🤝 Review Guidelines

### For Reviewers

Please verify:
- [ ] No secrets or tokens in any files
- [ ] All safety gates present in workflows
- [ ] Documentation is accurate and complete
- [ ] Rollback procedure is clear
- [ ] Smoke tests are comprehensive
- [ ] Railway configuration matches services
- [ ] Docker compose is properly structured
- [ ] File permissions are correct (smoke_test.sh executable)

### Approval Requirements

This PR requires approval from:
- [ ] Repository administrator
- [ ] DevOps/Infrastructure team member
- [ ] Security reviewer (for workflow safety gates)

---

## 🙏 Acknowledgments

This infrastructure builds upon:
- Railway platform for hosting
- GitHub Actions for CI/CD
- Docker for containerization
- Guardian coordinator for safety oversight

**Ready for testnet deployment! 🚀**
