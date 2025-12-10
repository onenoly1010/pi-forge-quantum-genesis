# Required Secrets Documentation

This document lists all required GitHub repository secrets and Railway environment variables for testnet deployment.

## 🔐 GitHub Repository Secrets

Configure these secrets in: `Settings → Secrets and variables → Actions → Repository secrets`

### Railway Configuration

| Secret Name | Description | Example/Format | Required |
|-------------|-------------|----------------|----------|
| `RAILWAY_TOKEN` | Railway API authentication token | `railway_***` | ✅ Yes |
| `RAILWAY_PROJECT_ID` | Railway project ID | `proj_abc123` | ✅ Yes |

### Testnet Supabase Configuration

| Secret Name | Description | Example/Format | Required |
|-------------|-------------|----------------|----------|
| `TESTNET_SUPABASE_URL` | Testnet Supabase project URL | `https://xxx.supabase.co` | ✅ Yes |
| `TESTNET_SUPABASE_KEY` | Testnet Supabase anonymous key | `eyJhbGc...` | ✅ Yes |
| `TESTNET_JWT_SECRET` | JWT signing secret for testnet | Random 64-char string | ✅ Yes |

### Deployment Configuration

| Secret Name | Description | Example/Format | Required |
|-------------|-------------|----------------|----------|
| `TESTNET_BASE_URL` | Base URL for testnet deployment | `https://testnet.railway.app` | ✅ Yes |
| `NFT_MINT_VALUE` | **MUST BE "0" for testnet** | `0` | ✅ Yes |
| `GUARDIAN_KILL_SWITCH` | Emergency deployment kill switch | `off` or `on` | ✅ Yes |

### ⚠️ Forbidden Secrets

These secrets **MUST NOT** exist in repository:

- ❌ `FORCE_DEPLOY_TO_MAINNET` - Mainnet deployment requires separate PR
- ❌ `MAINNET_SUPABASE_URL` - Must not be in repository secrets
- ❌ `MAINNET_SUPABASE_KEY` - Must not be in repository secrets
- ❌ Production API keys or tokens

## 🚂 Railway Environment Variables

Configure these in Railway dashboard per service:

### All Services (Common)

```bash
APP_ENVIRONMENT=testnet
NFT_MINT_VALUE=0
SUPABASE_URL=${TESTNET_SUPABASE_URL}
SUPABASE_KEY=${TESTNET_SUPABASE_KEY}
JWT_SECRET=${TESTNET_JWT_SECRET}
GUARDIAN_KILL_SWITCH=off
```

### Service-Specific Variables

#### Guardian Coordinator
```bash
SERVICE_NAME=guardian-coordinator
HEALTH_CHECK_INTERVAL=30
LOG_LEVEL=INFO
```

#### FastAPI Server
```bash
SERVICE_NAME=fastapi-server
CORS_ORIGINS=*
WS_HEARTBEAT_INTERVAL=30
```

#### Flask Dashboard
```bash
SERVICE_NAME=flask-dashboard
FLASK_ENV=production
FLASK_DEBUG=0
```

#### Gradio Interface
```bash
SERVICE_NAME=gradio-interface
GRADIO_SERVER_NAME=0.0.0.0
GRADIO_SERVER_PORT=7860
```

## 🔧 Setup Instructions

### 1. Generate Secrets

```bash
# Generate JWT secret (64 characters)
openssl rand -hex 32

# Or using Python
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 2. Configure GitHub Secrets

```bash
# Using GitHub CLI
gh secret set RAILWAY_TOKEN --body "<your-railway-token>"
gh secret set RAILWAY_PROJECT_ID --body "<your-project-id>"
gh secret set TESTNET_SUPABASE_URL --body "<your-testnet-url>"
gh secret set TESTNET_SUPABASE_KEY --body "<your-testnet-key>"
gh secret set TESTNET_JWT_SECRET --body "<generated-jwt-secret>"
gh secret set TESTNET_BASE_URL --body "<your-testnet-url>"
gh secret set NFT_MINT_VALUE --body "0"
gh secret set GUARDIAN_KILL_SWITCH --body "off"
```

### 3. Configure Railway Environment

1. Navigate to Railway dashboard → Your project
2. Select each service
3. Go to Variables tab
4. Add environment variables listed above
5. Deploy changes

## 🔍 Verification

### Check GitHub Secrets

```bash
# List all configured secrets
gh secret list
```

Expected output should include all required secrets listed above.

### Verify Railway Configuration

```bash
# Using Railway CLI
railway login
railway link <project-id>
railway vars --environment testnet
```

### Test Secret Access

The deployment workflow includes automatic validation:
- ✅ Checks `NFT_MINT_VALUE == "0"`
- ✅ Checks `GUARDIAN_KILL_SWITCH != "on"`
- ✅ Verifies forbidden secrets don't exist
- ✅ Validates required secrets are present

## 🛡️ Security Best Practices

### Testnet Secrets

1. **Isolation**: Use completely separate credentials from mainnet
2. **Rotation**: Rotate testnet secrets monthly
3. **Access Control**: Limit who can view/modify secrets
4. **Audit**: Review secret access logs regularly

### Secret Rotation Procedure

```bash
# 1. Generate new secret
NEW_SECRET=$(openssl rand -hex 32)

# 2. Update GitHub secret
gh secret set TESTNET_JWT_SECRET --body "$NEW_SECRET"

# 3. Update Railway environment
railway vars set JWT_SECRET="$NEW_SECRET" --environment testnet

# 4. Trigger redeployment
gh workflow run deploy-testnet.yml \
  -f requested_environment=testnet \
  -f confirm_safety="CONFIRM-TESTNET-DEPLOY"
```

### Emergency Secret Revocation

If a secret is compromised:

```bash
# 1. Activate kill switch
gh secret set GUARDIAN_KILL_SWITCH --body "on"

# 2. Revoke compromised credentials at source
# - Revoke Railway token in Railway dashboard
# - Reset Supabase keys in Supabase dashboard
# - Regenerate JWT secret

# 3. Update with new credentials
gh secret set RAILWAY_TOKEN --body "<new-token>"
# ... update other secrets

# 4. Deactivate kill switch
gh secret set GUARDIAN_KILL_SWITCH --body "off"
```

## 📋 Pre-Deployment Checklist

Before running deployment workflow:

- [ ] `RAILWAY_TOKEN` configured and valid
- [ ] `RAILWAY_PROJECT_ID` matches target project
- [ ] `TESTNET_SUPABASE_URL` points to testnet instance
- [ ] `TESTNET_SUPABASE_KEY` is valid testnet key
- [ ] `TESTNET_JWT_SECRET` generated and unique
- [ ] `TESTNET_BASE_URL` configured correctly
- [ ] `NFT_MINT_VALUE` is exactly `"0"`
- [ ] `GUARDIAN_KILL_SWITCH` is `"off"`
- [ ] No forbidden secrets exist
- [ ] Railway environment variables configured
- [ ] Secrets tested with smoke tests

## 🚨 Troubleshooting

### Deployment Fails with "Secret not found"

```bash
# List configured secrets
gh secret list

# Add missing secret
gh secret set <SECRET_NAME> --body "<value>"
```

### NFT_MINT_VALUE Validation Fails

```bash
# Check current value
gh secret list | grep NFT_MINT_VALUE

# Set to required value
gh secret set NFT_MINT_VALUE --body "0"
```

### Kill Switch Activated

```bash
# Check current status
gh secret list | grep GUARDIAN_KILL_SWITCH

# Deactivate (only if safe to deploy)
gh secret set GUARDIAN_KILL_SWITCH --body "off"
```

## 📞 Support

For secret-related issues:

1. Review this documentation
2. Check deployment workflow logs
3. Verify Railway environment configuration
4. Contact repository administrators
5. Review guardian coordinator logs

---

**⚠️ CRITICAL SECURITY NOTICE**

- **NEVER** commit secrets to version control
- **NEVER** share secrets via chat, email, or insecure channels
- **ALWAYS** use GitHub Secrets or Railway environment variables
- **ALWAYS** use testnet credentials for testnet deployments
- **ALWAYS** rotate secrets if compromise suspected

Violation of security practices may result in immediate kill switch activation and security audit.
