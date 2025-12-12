# Autonomous Operations Guide

## Overview

Once the Quantum Pi Forge system is bootstrapped and deployed, it can operate autonomously through the AI Agent Handoff Runbook. This guide explains how to enable, monitor, and maintain autonomous operations.

## Autonomous Architecture

The system uses GitHub Actions workflows to provide:

1. **Scheduled Health Monitoring** - Automatic health checks every 6 hours
2. **Self-Healing** - Automatic rollback on deployment failures
3. **Status Tracking** - Continuous status updates via GitHub Issues
4. **Deployment Automation** - Automated CI/CD pipeline with safety gates
5. **Alert System** - Webhook notifications for critical events

## Initial Setup

### 1. Configure GitHub Secrets

Set the following secrets in your GitHub repository settings:

```bash
# Navigate to: Settings → Secrets and variables → Actions → New repository secret

# Required secrets
SUPABASE_URL        # Your Supabase project URL
SUPABASE_KEY        # Your Supabase anonymous key
JWT_SECRET          # Secure random string for JWT signing

# Optional (for notifications)
SLACK_WEBHOOK_URL   # For Slack alerts
DISCORD_WEBHOOK_URL # For Discord alerts
```

Using GitHub CLI:

```bash
# Set secrets via CLI
gh secret set SUPABASE_URL --body "https://your-project.supabase.co"
gh secret set SUPABASE_KEY --body "your-anon-key"
gh secret set JWT_SECRET --body "$(openssl rand -hex 32)"

# Optional notification secrets
gh secret set SLACK_WEBHOOK_URL --body "https://hooks.slack.com/services/..."
gh secret set DISCORD_WEBHOOK_URL --body "https://discord.com/api/webhooks/..."
```

### 2. Enable the AI Agent Handoff Runbook

```bash
# Enable the workflow
gh workflow enable ai-agent-handoff-runbook.yml

# Verify it's enabled
gh workflow list
```

### 3. Trigger Initial Deployment

```bash
# Trigger full deployment
gh workflow run ai-agent-handoff-runbook.yml \
  --field action=full-deployment

# Monitor the run
gh run watch
```

## Autonomous Schedule

The system automatically performs health checks on a schedule:

- **Frequency**: Every 6 hours
- **Cron Schedule**: `0 */6 * * *`
- **Actions Performed**:
  - Module import validation
  - Critical file verification
  - File size checks
  - Health status reporting
  - Metrics collection
  - Status issue updates

## Monitoring Autonomous Operations

### Check System Status

The system maintains a tracking issue with current status:

```bash
# Find the status issue
gh issue list --label ai-agent,automated,runbook

# View the status issue
gh issue view <issue-number>
```

The status issue shows:

- ✅ Overall system health
- 📊 Recent deployment information
- 🔄 Rollback status
- 📈 Performance metrics
- 🚀 Service status (FastAPI, Flask, Gradio)

### View Recent Workflow Runs

```bash
# List recent runs
gh run list --workflow=ai-agent-handoff-runbook.yml --limit 10

# View specific run
gh run view <run-id>

# Watch live run
gh run watch <run-id>

# View logs
gh run view <run-id> --log
```

### Download Reports

The system generates detailed reports as artifacts:

```bash
# Download all artifacts from a run
gh run download <run-id>

# Download specific artifact
gh run download <run-id> --name monitoring-report
gh run download <run-id> --name deployment-record
gh run download <run-id> --name safety-gate-report
```

## Manual Operations

### Health Check

Trigger a manual health check:

```bash
gh workflow run ai-agent-handoff-runbook.yml \
  --field action=health-check
```

### Full Deployment

Deploy the latest code to production:

```bash
gh workflow run ai-agent-handoff-runbook.yml \
  --field action=full-deployment
```

### Component Update

Update a specific component:

```bash
# Update FastAPI only
gh workflow run ai-agent-handoff-runbook.yml \
  --field action=update-component \
  --field target_component=fastapi

# Update Flask only
gh workflow run ai-agent-handoff-runbook.yml \
  --field action=update-component \
  --field target_component=flask

# Update all components
gh workflow run ai-agent-handoff-runbook.yml \
  --field action=update-component \
  --field target_component=all
```

### Rollback

Roll back to a previous deployment:

```bash
# Automatic rollback to last known good
gh workflow run ai-agent-handoff-runbook.yml \
  --field action=rollback

# Rollback to specific version
gh workflow run ai-agent-handoff-runbook.yml \
  --field action=rollback \
  --field rollback_version="deploy-20241210-120000-abc1234"

# List available rollback tags
git tag -l "deploy-*" --sort=-version:refname | head -10
```

### Emergency Stop

Immediately halt all deployments:

```bash
gh workflow run ai-agent-handoff-runbook.yml \
  --field action=emergency-stop
```

## Workflow Jobs

The autonomous runbook consists of 6 jobs:

### 1. Safety Gate (🛡️)

**Purpose**: Validates deployment safety before proceeding

**Checks**:
- Critical files exist
- No breaking changes in recent commits
- Environment health
- Scheduled vs. triggered runs

**Outputs**:
- `deployment_approved` - Whether deployment can proceed
- `skip_deployment` - Whether to skip deployment (scheduled runs)
- Safety gate report artifact

### 2. CI Pipeline (🔧)

**Purpose**: Build, lint, and test the application

**Steps**:
- Lint with flake8 (critical errors)
- Run unit tests with coverage
- Build application (validate imports)
- Create deployment package

**Outputs**:
- `build_success` - Whether build succeeded
- `test_coverage` - Test coverage level
- Deployment package artifact

### 3. Deployment (🚀)

**Purpose**: Deploy to production environment

**Steps**:
- Download deployment package
- Create deployment tag
- Deploy to Railway (or configured platform)
- Wait for stabilization
- Record deployment metadata

**Outputs**:
- `deployment_url` - Production URL
- `deployment_id` - Unique deployment ID
- Deployment record artifact

### 4. Monitoring (📊)

**Purpose**: Verify deployment health

**Checks**:
- FastAPI module import
- Flask module import
- Critical file presence
- File size validation
- Performance metrics

**Outputs**:
- `health_status` - Current health (healthy/degraded/warning)
- Monitoring report artifact

### 5. Rollback (🔄)

**Purpose**: Automatic recovery on failure

**Triggers**:
- Deployment failure
- Health status degraded
- Manual rollback request

**Actions**:
- Find last successful deployment
- Execute rollback
- Send rollback alert
- Generate rollback report

### 6. Communication (📢)

**Purpose**: Update status and send notifications

**Actions**:
- Collect all job statuses
- Update/create tracking issue
- Send webhook notifications (if configured)
- Generate final summary

## Status Indicators

The system uses emoji indicators for status:

| Emoji | Status | Meaning |
|-------|--------|---------|
| 🟢 | success | All systems operational |
| 🔴 | failed | Critical failure detected |
| 🟡 | blocked | Safety gate prevented deployment |
| 🔄 | rolled_back | System recovered via rollback |
| ⏭️ | skipped | Job not needed for this run |
| ⚠️ | warning | Non-critical issues detected |

## Autonomous Features in Detail

### Scheduled Monitoring

**Cron**: `0 */6 * * *` (every 6 hours)

**Actions**:
1. Validate module imports
2. Check critical files
3. Collect metrics
4. Update status issue
5. No deployment (monitoring only)

### Self-Healing

**Triggers**:
- Deployment failure
- Health degradation
- Service unavailability

**Response**:
1. Detect failure condition
2. Identify last successful deployment
3. Execute automatic rollback
4. Send alert notifications
5. Update status issue
6. Generate rollback report

### Safety Gates

**Pre-Deployment Checks**:
- ✅ Critical files present
- ✅ No breaking changes
- ✅ Environment healthy
- ✅ Dependencies satisfied

**During Deployment**:
- ✅ Build succeeds
- ✅ Tests pass
- ✅ Linting passes

**Post-Deployment**:
- ✅ Health checks pass
- ✅ Services responding
- ✅ No errors in logs

### Deployment Tagging

Each deployment creates a Git tag:

**Format**: `deploy-YYYYMMDD-HHMMSS-<commit-hash>`

**Example**: `deploy-20241210-143000-abc1234`

**Usage**:
```bash
# List deployment tags
git tag -l "deploy-*" --sort=-version:refname

# Rollback to specific tag
gh workflow run ai-agent-handoff-runbook.yml \
  --field action=rollback \
  --field rollback_version="deploy-20241210-143000-abc1234"
```

## Notification Setup

### Slack Integration

1. Create a Slack webhook:
   - Go to https://api.slack.com/apps
   - Create an app
   - Enable Incoming Webhooks
   - Create webhook for your channel

2. Set the secret:
   ```bash
   gh secret set SLACK_WEBHOOK_URL --body "https://hooks.slack.com/services/..."
   ```

### Discord Integration

1. Create a Discord webhook:
   - Open Discord server settings
   - Go to Integrations → Webhooks
   - Create webhook
   - Copy webhook URL

2. Set the secret:
   ```bash
   gh secret set DISCORD_WEBHOOK_URL --body "https://discord.com/api/webhooks/..."
   ```

### Notification Triggers

Notifications are sent when:
- ❌ Deployment fails
- 🔄 Rollback executes
- ⚠️ Health status degrades
- 🚨 Emergency stop triggered

## Best Practices

### 1. Regular Monitoring

```bash
# Check status weekly
gh issue view $(gh issue list --label ai-agent --json number --jq '.[0].number')

# Review recent runs
gh run list --workflow=ai-agent-handoff-runbook.yml --limit 5
```

### 2. Before Risky Changes

```bash
# Note current deployment tag
git tag -l "deploy-*" --sort=-version:refname | head -1

# Run health check first
gh workflow run ai-agent-handoff-runbook.yml --field action=health-check
```

### 3. After Deployment

```bash
# Wait for monitoring to complete
sleep 120

# Check deployment status
gh run view $(gh run list --limit 1 --json databaseId --jq '.[0].databaseId')
```

### 4. On Failures

```bash
# Download artifacts for analysis
gh run download <run-id>

# Check rollback status
cat rollback-report.md

# Review logs
cat workflow-summary.md
```

### 5. Maintenance Windows

```bash
# Disable scheduled monitoring during maintenance
gh workflow disable ai-agent-handoff-runbook.yml

# Perform maintenance
# ...

# Re-enable afterward
gh workflow enable ai-agent-handoff-runbook.yml
```

## Troubleshooting Autonomous Operations

### Workflow Not Running

**Check**:
```bash
# Verify workflow is enabled
gh workflow list

# Check recent runs
gh run list --workflow=ai-agent-handoff-runbook.yml
```

**Solution**:
```bash
# Enable workflow
gh workflow enable ai-agent-handoff-runbook.yml
```

### Health Checks Failing

**Check**:
```bash
# Download monitoring report
gh run download <run-id> --name monitoring-report
cat monitoring-report.md
```

**Common Issues**:
- Module import failures → Check dependencies
- Missing files → Verify repository structure
- Size violations → Optimize large files

### Rollback Not Working

**Check**:
```bash
# Verify rollback tags exist
git tag -l "deploy-*" --sort=-version:refname

# Download rollback report
gh run download <run-id> --name rollback-report
```

**Solution**:
```bash
# Manual rollback if needed
git checkout <deployment-tag>
# Then redeploy
```

### Status Issue Not Updating

**Check**:
```bash
# Verify issue exists
gh issue list --label ai-agent,automated,runbook

# Check workflow permissions
gh workflow view ai-agent-handoff-runbook.yml
```

**Solution**:
```bash
# Create issue manually if needed
gh issue create \
  --title "🤖 AI Agent Autonomous Runbook Status" \
  --label ai-agent,automated,runbook \
  --body "Tracking issue for autonomous operations"
```

## Success Criteria

✅ **System is fully autonomous when**:

1. Scheduled health checks run successfully every 6 hours
2. Status issue updates automatically
3. Monitoring reports generated consistently
4. Rollback mechanism tested and working
5. No manual intervention needed for routine operations
6. Alerts configured and received
7. Deployment tags created automatically
8. CI/CD pipeline runs without errors

## Advanced Configuration

### Custom Monitoring Frequency

Edit `.github/workflows/ai-agent-handoff-runbook.yml`:

```yaml
schedule:
  # Change from every 6 hours to every 3 hours
  - cron: '0 */3 * * *'
```

### Custom Safety Gates

Add custom checks to the safety gate job:

```yaml
- name: Custom Safety Check
  run: |
    # Your custom validation logic
    echo "Running custom safety check..."
```

### Custom Notifications

Add custom notification endpoints:

```yaml
- name: Custom Notification
  run: |
    curl -X POST "${{ secrets.CUSTOM_WEBHOOK_URL }}" \
      -d '{"status": "${{ needs.deployment.result }}"}'
```

## Summary

The Autonomous Operations system provides:

- ✅ **Zero-touch monitoring** - Automatic health checks
- ✅ **Self-healing** - Automatic recovery from failures
- ✅ **Continuous tracking** - Real-time status updates
- ✅ **Proactive alerts** - Notifications on issues
- ✅ **Historical data** - Deployment records and metrics
- ✅ **Easy management** - Simple CLI commands
- ✅ **Production-ready** - Battle-tested workflows

---

**🤖 Your Quantum Resonance Lattice now operates autonomously!**
