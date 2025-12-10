# Secrets Documentation

## Overview

This document lists all secrets required for deploying Pi Forge Quantum Genesis to Railway testnet and running GitHub Actions workflows. 

**⚠️ CRITICAL**: This file contains **NO ACTUAL SECRET VALUES**. All secrets must be:
- Added to GitHub repository secrets (Settings → Secrets and variables → Actions)
- Added to Railway project environment variables (Project → Settings → Variables)
- **NEVER** committed to git in plain text

## GitHub Actions Secrets

Configure these in: Repository → Settings → Secrets and variables → Actions → New repository secret

### Required Secrets

| Secret Name | Description | Required For | Example/Format |
|-------------|-------------|--------------|----------------|
| `RAILWAY_API_KEY` | Railway API token for deployments | Deploy workflow | `railway_***` (from Railway settings) |
| `RAILWAY_PROJECT_ID` | Railway project identifier | Deploy workflow | `project-id-here` |
| `GHCR_PAT` | GitHub Container Registry token (optional) | Build images | Use `GITHUB_TOKEN` instead |
| `SUPABASE_URL` | Supabase project URL (testnet) | Testing | `https://abc123.supabase.co` |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service role key (testnet) | Testing | `eyJ***` |
| `SUPABASE_KEY` | Supabase anon key (testnet) | Testing | `eyJ***` |
| `JWT_SECRET` | JWT signing secret | Testing/Deploy | Random 32+ char string |
| `PI_TESTNET_API_KEY` | Pi Network testnet API key | Testing | From Pi Developer Portal |
| `DISCORD_BOT_TOKEN` | Discord bot token for guardian alerts (optional) | Guardian bot | From Discord Developer Portal |
| `DISCORD_GUARDIAN_CHANNEL_ID` | Discord channel ID for alerts (optional) | Guardian bot | `1234567890` |

### Safety/Operational Secrets

| Secret Name | Description | Default | Notes |
|-------------|-------------|---------|-------|
| `GUARDIAN_KILL_SWITCH` | Emergency kill switch | `off` | Set to `on` to abort all deployments |
| `NFT_MINT_VALUE` | NFT mint value enforcement | `0` | MUST be `0` for testnet |
| `FORCE_DEPLOY_TO_MAINNET` | Mainnet deployment gate | (not set) | Requires 5/5 guardian approvals, NOT for this PR |

### Optional Secrets

| Secret Name | Description | Required For |
|-------------|-------------|--------------|
| `SLACK_WEBHOOK_URL` | Slack notifications | Deployment notifications |
| `SENTRY_DSN` | Error tracking | Error monitoring |
| `DATADOG_API_KEY` | Metrics and monitoring | Advanced monitoring |

## Railway Environment Variables

Configure these in: Railway Project → Service → Variables

### Guardian Coordinator Service

```bash
# REQUIRED
APP_ENVIRONMENT=testnet              # MUST be "testnet"
GUARDIAN_KILL_SWITCH=off             # "off" for normal operation
NFT_MINT_VALUE=0                     # MUST be "0"
GUARDIAN_ID=guardian-railway-001     # Unique guardian identifier
QUORUM_THRESHOLD=0.70                # Validation threshold (0.0-1.0)
ETHICAL_ENTROPY_MAX=0.05             # Maximum ethical entropy
REDIS_URL=${{Redis.REDIS_URL}}       # Internal Railway Redis reference
PORT=8080                            # Service port
LOG_LEVEL=INFO                       # Logging level

# OPTIONAL
DISCORD_BOT_TOKEN=<from-github-secrets>
DISCORD_GUARDIAN_CHANNEL_ID=<from-github-secrets>
```

### FastAPI Server Service

```bash
# REQUIRED
APP_ENVIRONMENT=testnet              # MUST be "testnet"
SUPABASE_URL=<your-testnet-url>      # From Supabase dashboard
SUPABASE_KEY=<your-testnet-anon-key> # From Supabase dashboard
JWT_SECRET=<secure-random-string>    # Same as GitHub secret
PI_NETWORK_MODE=testnet              # MUST be "testnet"
PI_TESTNET_API_KEY=<from-pi-portal>  # From Pi Developer Portal
PI_SANDBOX_MODE=true                 # Enable sandbox mode
NFT_MINT_VALUE=0                     # MUST be "0"
GUARDIAN_KILL_SWITCH=off             # "off" for normal operation
PORT=8000                            # Service port

# OPTIONAL
SUPABASE_SERVICE_ROLE_KEY=<service-role-key>  # For admin operations
CORS_ORIGINS=*                                 # Or specific domains
REDIS_URL=${{Redis.REDIS_URL}}                # If using Redis
```

### Flask Dashboard Service

```bash
# REQUIRED
APP_ENVIRONMENT=testnet              # MUST be "testnet"
FLASK_ENV=development                # or "production" for Railway
FLASK_SECRET_KEY=<secure-random>     # Flask session secret
PORT=5000                            # Service port

# OPTIONAL
FLASK_DEBUG=false                    # Set true for debug mode
LOG_LEVEL=INFO
```

### Gradio Interface Service

```bash
# REQUIRED
APP_ENVIRONMENT=testnet              # MUST be "testnet"
GRADIO_SERVER_NAME=0.0.0.0          # Bind to all interfaces
GRADIO_SERVER_PORT=7860             # Gradio default port
PORT=7860                            # Service port

# OPTIONAL
GRADIO_ANALYTICS_ENABLED=false      # Disable analytics
LOG_LEVEL=INFO
```

### Redis Service (Railway Add-on)

Redis is automatically provisioned by Railway. Other services reference it using:

```bash
REDIS_URL=${{Redis.REDIS_URL}}
```

## How to Generate Secrets

### JWT_SECRET

```bash
# Linux/Mac
openssl rand -base64 32

# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

### Supabase Credentials

1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Create new project (or use existing testnet project)
3. Navigate to Settings → API
4. Copy:
   - Project URL (e.g., `https://abc123.supabase.co`)
   - `anon` `public` key
   - `service_role` `secret` key

### Pi Network Testnet API Key

1. Go to [Pi Developer Portal](https://developers.minepi.com)
2. Create new app or select existing testnet app
3. Navigate to App Settings → API Keys
4. Generate testnet API key
5. **NEVER** use mainnet keys for testnet deployments

### Railway API Key

1. Go to [Railway Dashboard](https://railway.app)
2. Click profile → Account Settings → Tokens
3. Generate new token
4. Copy token (starts with `railway_`)
5. Add to GitHub secrets as `RAILWAY_API_KEY`

### Railway Project ID

```bash
# Via Railway CLI
railway status

# Or from Railway URL
# https://railway.app/project/<PROJECT_ID>
```

### Discord Bot (Optional)

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create new application
3. Navigate to Bot → Reset Token
4. Copy token
5. Add bot to your server
6. Get channel ID: Enable Developer Mode → Right-click channel → Copy ID

## Security Best Practices

### ✅ DO

- Store all secrets in Railway UI or GitHub Secrets
- Use different secrets for testnet vs. mainnet (if/when mainnet is approved)
- Rotate secrets regularly (quarterly recommended)
- Use strong, randomly generated values (32+ characters)
- Enable 2FA on Railway, GitHub, and Supabase accounts
- Audit secret access logs periodically
- Use Railway's internal service references (`${{service.VAR}}`)

### ❌ DON'T

- Commit secrets to git (check with `git log -p | grep -i secret`)
- Share secrets via Slack, Discord, or email
- Use production/mainnet secrets for testnet
- Reuse secrets across different environments
- Store secrets in `.env` files that are committed
- Log secrets in application logs
- Expose secrets in error messages

## Environment Variable Precedence

Railway environment variables follow this precedence (highest to lowest):

1. Service-specific variables (set in service settings)
2. Environment-specific variables (e.g., `production` environment)
3. Global project variables
4. Railway-provided variables (e.g., `${{Redis.REDIS_URL}}`)

## Validation Checklist

Before deploying, verify:

- [ ] All required secrets are set in GitHub Actions
- [ ] All required environment variables are set in Railway for each service
- [ ] `APP_ENVIRONMENT=testnet` for **all** services
- [ ] `NFT_MINT_VALUE=0` for **all** services using Pi Network
- [ ] `GUARDIAN_KILL_SWITCH=off` (or `on` if intentionally paused)
- [ ] Supabase URLs and keys are for **testnet** project
- [ ] Pi Network API key is for **testnet** app
- [ ] No secrets are committed to git (`git log -p | grep -E "sk-|eyJ"`)

## Secrets Audit Log

Maintain a log of secret rotations:

```
YYYY-MM-DD | Secret Name           | Rotated By | Reason
-----------|----------------------|------------|------------------
2024-01-15 | JWT_SECRET           | Admin      | Quarterly rotation
2024-02-01 | RAILWAY_API_KEY      | Admin      | Team member departure
2024-03-10 | SUPABASE_SERVICE_KEY | Admin      | Security audit
```

## Support

For issues with secrets:

1. **Railway**: https://railway.app/help
2. **GitHub**: https://docs.github.com/en/actions/security-guides/encrypted-secrets
3. **Supabase**: https://supabase.com/docs/guides/api
4. **Pi Network**: https://developers.minepi.com/support

## Emergency Procedures

### If a Secret is Compromised

1. **Immediately rotate** the compromised secret in the source (Railway, Supabase, etc.)
2. **Update** the secret in GitHub Actions and Railway
3. **Redeploy** all affected services
4. **Audit logs** for unauthorized access
5. **Document** the incident in the audit log above

### If GUARDIAN_KILL_SWITCH is Activated

1. All deployments will abort
2. Existing services continue running
3. To resume: Set `GUARDIAN_KILL_SWITCH=off` in Railway and GitHub Secrets
4. Redeploy or restart services as needed

## Notes

- This document should be reviewed quarterly
- Update when adding new services or integrations
- Keep in sync with actual deployment configurations
- Version control this file (without actual values)
