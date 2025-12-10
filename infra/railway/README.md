# Railway Deployment Guide

Complete guide for deploying Pi Forge Quantum Genesis to Railway testnet environment.

## 🚂 Overview

Railway provides the hosting infrastructure for Pi Forge Quantum Genesis testnet. This guide covers setup, deployment, and management.

## 📋 Prerequisites

- Railway account (https://railway.app)
- Railway CLI installed (`npm install -g @railway/cli`)
- GitHub repository access
- Railway project created

## 🏗️ Initial Setup

### 1. Create Railway Project

```bash
# Login to Railway
railway login

# Create new project
railway init

# Link to existing project
railway link <project-id>
```

### 2. Configure Services

The project requires four services:

1. **guardian-coordinator** - Safety monitoring and oversight
2. **fastapi-server** - Main API server
3. **flask-dashboard** - Visualization dashboard
4. **gradio-interface** - Ethical AI interface

### 3. Set Up Environment Variables

For each service, configure the following:

```bash
# Set environment for a service
railway variables set \
  APP_ENVIRONMENT=testnet \
  NFT_MINT_VALUE=0 \
  SUPABASE_URL=<testnet-url> \
  SUPABASE_KEY=<testnet-key> \
  JWT_SECRET=<jwt-secret> \
  GUARDIAN_KILL_SWITCH=off \
  --service <service-name> \
  --environment testnet
```

## 🚀 Deployment Methods

### Method 1: GitHub Actions (Recommended)

The GitHub Actions workflow handles deployment automatically:

1. Navigate to repository Actions tab
2. Select "Deploy to Testnet (Railway)"
3. Click "Run workflow"
4. Select environment: `testnet`
5. Enter confirmation: `CONFIRM-TESTNET-DEPLOY`
6. Monitor workflow progress

### Method 2: Railway CLI

```bash
# Deploy all services
railway up --environment testnet

# Deploy specific service
railway up --service guardian-coordinator --environment testnet
railway up --service fastapi-server --environment testnet
railway up --service flask-dashboard --environment testnet
railway up --service gradio-interface --environment testnet
```

### Method 3: Railway Dashboard

1. Navigate to Railway dashboard
2. Select your project
3. Click on each service
4. Click "Deploy" button
5. Monitor deployment logs

## 🔧 Configuration

### Railway Project Structure

```
pi-forge-quantum-genesis/
├── guardian-coordinator (Service)
│   ├── Build: Dockerfile
│   ├── Start: uvicorn guardian_coordinator.main:app
│   └── Port: 8000
├── fastapi-server (Service)
│   ├── Build: Dockerfile
│   ├── Start: uvicorn main:app
│   └── Port: 8000
├── flask-dashboard (Service)
│   ├── Build: Dockerfile.flask
│   ├── Start: python app.py
│   └── Port: 5000
└── gradio-interface (Service)
    ├── Build: Dockerfile.gradio
    ├── Start: python app.py
    └── Port: 7860
```

### Health Checks

Configure health checks for each service:

| Service | Path | Timeout | Interval |
|---------|------|---------|----------|
| guardian-coordinator | `/health` | 60s | 30s |
| fastapi-server | `/` | 30s | 30s |
| flask-dashboard | `/` | 30s | 30s |
| gradio-interface | `/` | 30s | 30s |

## 📊 Monitoring

### View Logs

```bash
# View logs for all services
railway logs --environment testnet

# View logs for specific service
railway logs --service fastapi-server --environment testnet

# Follow logs in real-time
railway logs --follow --environment testnet
```

### Check Service Status

```bash
# Get service status
railway status --environment testnet

# Get service domains
railway domain --environment testnet
```

### Metrics Dashboard

Access Railway metrics dashboard:
1. Open Railway dashboard
2. Select your project
3. Click "Metrics" tab
4. View CPU, memory, and network metrics

## 🔄 Updates and Rollbacks

### Deploy Update

```bash
# Deploy latest changes
railway up --environment testnet

# Deploy specific commit
railway up --ref <commit-sha> --environment testnet
```

### Rollback Deployment

```bash
# List deployments
railway deployments --environment testnet

# Rollback to specific deployment
railway rollback --deployment <deployment-id> --environment testnet

# Rollback specific service
railway rollback \
  --service fastapi-server \
  --deployment <deployment-id> \
  --environment testnet
```

## 🛠️ Troubleshooting

### Build Failures

```bash
# Check build logs
railway logs --service <service-name> --environment testnet

# Common issues:
# - Missing dependencies: Update requirements.txt
# - Dockerfile errors: Validate Dockerfile syntax
# - Build timeout: Increase build timeout in Railway settings
```

### Runtime Errors

```bash
# Check runtime logs
railway logs --follow --service <service-name> --environment testnet

# Common issues:
# - Missing environment variables: Check Railway variables
# - Port binding errors: Verify PORT environment variable
# - Database connection: Check Supabase configuration
```

### Service Unreachable

```bash
# Verify service is running
railway status --environment testnet

# Check service domain
railway domain --environment testnet

# Restart service
railway restart --service <service-name> --environment testnet
```

## 🔐 Security

### Environment Isolation

- **Testnet environment**: Completely isolated from mainnet
- **Separate credentials**: Different API keys, database instances
- **Access control**: Limited to testnet-specific resources

### Secret Management

```bash
# Add secret via CLI
railway variables set SECRET_NAME=value --environment testnet

# Remove secret
railway variables delete SECRET_NAME --environment testnet

# List all variables (values hidden)
railway variables --environment testnet
```

### Access Control

1. Navigate to Railway dashboard
2. Go to Project Settings
3. Click "Members" tab
4. Invite team members with appropriate roles
5. Enable 2FA for all members

## 📈 Scaling

### Vertical Scaling

```bash
# Railway automatically scales within plan limits
# Upgrade plan if needed for more resources
```

### Horizontal Scaling

Railway supports multiple replicas per service:
1. Navigate to service settings
2. Adjust "Replicas" setting
3. Save and redeploy

## 💰 Cost Management

### Monitor Usage

```bash
# View current usage
railway usage --environment testnet
```

### Optimize Costs

- Use appropriate service sizes
- Implement proper health checks to avoid restarts
- Monitor resource usage and adjust as needed
- Clean up unused environments and services

## 🔗 Custom Domains

### Add Custom Domain

```bash
# Add domain via CLI
railway domain add testnet.yourdomain.com --environment testnet

# Or via dashboard:
# 1. Go to service settings
# 2. Click "Domains" tab
# 3. Add custom domain
# 4. Configure DNS records
```

## 📚 Best Practices

### Deployment

1. **Test locally first**: Use docker-compose.testnet.yml
2. **Use staging**: Deploy to testnet before production
3. **Monitor deployments**: Watch logs during deployment
4. **Verify health**: Run smoke tests post-deployment

### Configuration

1. **Environment variables**: Never hardcode secrets
2. **Separate environments**: Testnet vs. production isolation
3. **Health checks**: Configure appropriate timeouts
4. **Logging**: Enable detailed logging for troubleshooting

### Maintenance

1. **Regular updates**: Keep dependencies updated
2. **Monitor metrics**: Review CPU, memory, network usage
3. **Log rotation**: Railway handles automatically
4. **Backup strategy**: Regular database backups via Supabase

## 🚨 Emergency Procedures

### Service Down

```bash
# Quick restart
railway restart --service <service-name> --environment testnet

# Force redeploy
railway up --force --service <service-name> --environment testnet
```

### Complete Outage

```bash
# Restart all services
railway restart --environment testnet

# If restart fails, rollback to last known good deployment
railway rollback --deployment <last-good-deployment-id> --environment testnet
```

### Database Issues

1. Check Supabase dashboard
2. Verify connection strings
3. Check Railway environment variables
4. Review service logs for connection errors

## 📞 Support

### Railway Support

- Documentation: https://docs.railway.app
- Discord: https://discord.gg/railway
- GitHub: https://github.com/railwayapp/railway

### Project-Specific Support

- Check infra/README.md for general guidance
- Review infra/SECRETS.md for configuration
- Check GitHub Issues for known problems
- Contact repository administrators

## 🔄 Migration Guide

### From Local to Railway

1. Test with docker-compose locally
2. Configure Railway services
3. Set environment variables
4. Deploy via GitHub Actions
5. Run smoke tests
6. Monitor for issues

### Between Railway Environments

```bash
# Export variables from source
railway variables --environment source > vars.txt

# Import to target (after manual review and editing)
railway variables set $(cat vars.txt) --environment target
```

---

**⚠️ IMPORTANT NOTES**

- Always deploy to testnet first
- Never use production credentials in testnet
- Monitor costs and resource usage
- Keep Railway CLI updated
- Review Railway changelog for breaking changes
- Maintain service health checks
- Test rollback procedures regularly

For questions or issues, refer to Railway documentation or contact repository administrators.
