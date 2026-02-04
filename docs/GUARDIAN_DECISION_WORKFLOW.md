# 🛡️ Guardian Decision Request Workflow

## Overview

The Guardian Decision Request system provides a structured process for requesting human oversight on autonomous system decisions. This document explains how to create, process, and respond to Guardian Decision Requests.

## Table of Contents

1. [When to Create a Guardian Decision Request](#when-to-create-a-guardian-decision-request)
2. [Creating Guardian Decision Requests](#creating-guardian-decision-requests)
3. [Processing Guardian Decision Requests](#processing-guardian-decision-requests)
4. [Guardian Response Protocol](#guardian-response-protocol)
5. [Integration with Autonomous Systems](#integration-with-autonomous-systems)
6. [Examples](#examples)
7. [Troubleshooting](#troubleshooting)

---

## When to Create a Guardian Decision Request

Guardian Decision Requests should be created when:

### Automatic Triggers

- **Low Confidence**: Decision confidence score < 0.8
- **High Priority**: Critical or high-priority decisions
- **High Impact**: Decisions affecting multiple services or users
- **Data Risk**: Decisions that may impact data integrity
- **Security Concerns**: Decisions with security implications
- **Policy Questions**: Decisions requiring policy interpretation

### Manual Triggers

- **Novel Situations**: Scenarios not covered by existing rules
- **Complex Decisions**: Multi-faceted decisions requiring judgment
- **Strategic Changes**: Changes affecting system architecture or economics
- **Emergency Overrides**: When human judgment supersedes automation

---

## Creating Guardian Decision Requests

### Method 1: Using the CLI Script (Recommended)

The `create_guardian_decision.py` script provides an easy way to create Guardian Decision Requests:

```bash
# Basic usage
python scripts/create_guardian_decision.py \
  --decision-id deployment_1234567890 \
  --decision-type Deployment \
  --priority High \
  --confidence 0.75 \
  --action "Deploy version 2.1.0 to production" \
  --reason "Confidence below threshold, requires Guardian review"

# With full options
python scripts/create_guardian_decision.py \
  --decision-id scaling_1234567890 \
  --decision-type Scaling \
  --priority Critical \
  --confidence 0.65 \
  --action "Scale up web servers from 2 to 8 instances" \
  --reason "Sudden traffic spike, requires immediate scaling" \
  --current-state "2 instances at 95% CPU, response time degrading" \
  --proposed-change "Add 6 instances to handle increased load" \
  --safety-impact High \
  --blast-radius "Affects main web service, 100% of users" \
  --reversibility Yes \
  --data-risk No \
  --requested-by System \
  --output /tmp/guardian-decision.md \
  --show-gh-command

# Then create the issue
gh issue create \
  --title "[GUARDIAN] Scaling - scaling_1234567890" \
  --body-file /tmp/guardian-decision.md \
  --label "guardian-decision,needs-approval" \
  --assignee onenoly1010
```

### Method 2: Using the Python API

```python
from server.guardian_issue_creator import create_guardian_issue_for_decision

# Create from decision data
decision_data = {
    "decision_id": "deployment_1234567890",
    "decision_type": "deployment",
    "confidence": 0.75,
    "reasoning": "All tests passed, ready for deployment",
    "actions": ["Deploy version 2.1.0", "Run smoke tests", "Monitor for 1 hour"],
    "metadata": {
        "priority": "high",
        "current_state": "Version 2.0.9 running smoothly",
        "proposed_change": "Deploy version 2.1.0 with new features",
        "safety_impact": "Low",
        "reversible": True,
        "data_risk": False
    },
    "source": "autonomous_agent"
}

# Create issue body (without creating actual GitHub issue)
result = create_guardian_issue_for_decision(decision_data, auto_create=False)
print(f"Issue body: {result['issue_body']}")

# Or auto-create GitHub issue (requires GitHub CLI)
result = create_guardian_issue_for_decision(decision_data, auto_create=True)
if result['created']:
    print(f"✅ Issue created: {result['issue_url']}")
```

### Method 3: Manual GitHub Issue Creation

1. Go to: https://github.com/onenoly1010/pi-forge-quantum-genesis/issues/new/choose
2. Select "Guardian Decision" template
3. Fill in the template fields
4. Submit the issue

---

## Processing Guardian Decision Requests

### Guardian Review Process

1. **Receive Notification**
   - Email notification for new Guardian Decision Request
   - Check Guardian HQ (Issue #100) for pending requests
   - Review dashboard: `curl https://pi-forge-quantum-genesis.railway.app/api/guardian/dashboard`

2. **Initial Assessment** (< 5 minutes)
   - Read decision summary
   - Check confidence score and priority
   - Review risk assessment
   - Identify decision type

3. **Detailed Review** (time varies by priority)
   - **Critical**: < 1 hour
   - **High**: < 4 hours
   - **Medium**: < 24 hours
   - **Low**: < 72 hours

4. **Decision Criteria Evaluation**
   - Review safety checklist
   - Assess impact
   - Verify approval criteria
   - Check for conflicts or dependencies

5. **Make Decision**
   - **Approve**: Decision meets all criteria
   - **Reject**: Decision does not meet criteria or has issues
   - **Need More Info**: Additional context required
   - **Escalate**: Requires team discussion or stakeholder input

6. **Document Response**
   - Add Guardian comments to issue
   - Specify conditions (if conditional approval)
   - Define follow-up actions
   - Update decision timeline

7. **Execute or Block**
   - If approved: Record approval and allow execution
   - If rejected: Block execution and document reasoning
   - If escalated: Wait for team decision

---

## Guardian Response Protocol

### Approval Response Template

```markdown
### Guardian Response

**Decision:** Approve

**Guardian Comments:**

Reviewed deployment decision #deployment_1234567890. Decision meets all approval criteria:

✅ All safety checks passed
✅ Tests completed successfully (127/127 passing)
✅ Security scan clean (0 vulnerabilities)
✅ Rollback plan documented and tested
✅ Impact assessment shows low risk
✅ Monitoring alerts configured

**Conditions:**

- Monitor closely for first 2 hours post-deployment
- Have on-call engineer available
- Rollback immediately if error rate exceeds 1%

**Follow-up Actions:**

- Record approval in system: `python scripts/record_guardian_approval.py record deployment_1234567890 --guardian onenoly1010 --reasoning "Approved - all criteria met"`
- Execute deployment
- Monitor metrics dashboard
- Update issue when deployment completes

**Timeline Update:**

- Responded: 2026-02-04T13:45:00Z
- Expected Execution: 2026-02-04T14:00:00Z
```

### Rejection Response Template

```markdown
### Guardian Response

**Decision:** Reject

**Guardian Comments:**

Reviewed deployment decision #deployment_1234567890. Decision REJECTED due to the following concerns:

❌ Security scan identified 3 high-severity vulnerabilities
❌ Rollback plan incomplete (missing database migration rollback)
❌ Confidence score too low (0.62) for production deployment

**Required Actions Before Approval:**

1. Fix security vulnerabilities: CVE-2024-12345, CVE-2024-12346, CVE-2024-12347
2. Complete rollback documentation including database migration rollback procedure
3. Improve test coverage for new features (currently 65%, need 80%+)
4. Re-run autonomous decision after fixes

**Follow-up Actions:**

- Create tasks for required fixes
- Re-evaluate when fixes are complete
- Run new autonomous decision evaluation

**Timeline Update:**

- Responded: 2026-02-04T13:45:00Z
- Expected Re-evaluation: 2026-02-04T16:00:00Z (after fixes)
```

### Escalation Response Template

```markdown
### Guardian Response

**Decision:** Escalate

**Guardian Comments:**

Reviewed scaling decision #scaling_1234567890. This decision requires team discussion and stakeholder input due to:

⚠️ Significant cost implications ($500/month increase)
⚠️ Architectural implications (need to evaluate alternative approaches)
⚠️ Policy question: Should we implement auto-scaling for this tier?

**Questions for Team:**

1. Budget approval for $500/month increase?
2. Should we implement auto-scaling instead of manual scaling?
3. What's the long-term scaling strategy for this service?

**Recommended Next Steps:**

1. Schedule team meeting to discuss scaling strategy
2. Evaluate cost-benefit of auto-scaling implementation
3. Get budget approval from stakeholders
4. Document scaling policy for this service tier

**Follow-up Actions:**

- @team Review and provide input
- Schedule team meeting within 24 hours
- Document decision in escalation notes

**Timeline Update:**

- Responded: 2026-02-04T13:45:00Z
- Team Meeting: 2026-02-05T10:00:00Z
- Expected Resolution: 2026-02-05T15:00:00Z
```

---

## Integration with Autonomous Systems

### Autonomous Decision System Integration

The Guardian Decision Request system integrates with the autonomous decision system to automatically create requests when needed.

```python
# In autonomous_decision.py
from server.guardian_issue_creator import create_guardian_issue_for_decision

class AIDecisionMatrix:
    def make_decision(self, context: DecisionContext) -> DecisionResult:
        # ... decision logic ...
        
        result = DecisionResult(
            decision_id=decision_id,
            decision_type=context.decision_type,
            approved=auto_approved,
            confidence=confidence,
            reasoning=reasoning,
            actions=actions,
            requires_guardian=requires_guardian,
            metadata=metadata
        )
        
        # If Guardian approval required, create issue
        if requires_guardian:
            decision_data = {
                "decision_id": result.decision_id,
                "decision_type": result.decision_type.value,
                "confidence": result.confidence,
                "reasoning": result.reasoning,
                "actions": result.actions,
                "metadata": result.metadata,
                "source": context.source
            }
            
            # Create Guardian Decision Request
            issue_result = create_guardian_issue_for_decision(
                decision_data,
                auto_create=True  # Set False for testing
            )
            
            if issue_result and issue_result.get('created'):
                logger.info(
                    f"🛡️ Guardian Decision Request created: {issue_result['issue_url']}"
                )
        
        return result
```

### API Integration

```python
# In main.py
from server.guardian_issue_creator import get_guardian_issue_creator

@app.post("/api/autonomous/request-guardian-decision")
async def request_guardian_decision(decision_data: dict):
    """Create Guardian Decision Request from API call"""
    creator = get_guardian_issue_creator()
    result = creator.create_guardian_issue_from_decision(
        decision_data,
        auto_create=True
    )
    
    return {
        "success": result.get('created', False),
        "decision_id": result.get('decision_id'),
        "issue_url": result.get('issue_url'),
        "issue_number": result.get('issue_number')
    }
```

---

## Examples

### Example 1: Deployment Decision Request

```bash
python scripts/create_guardian_decision.py \
  --decision-id deployment_1707142800 \
  --decision-type Deployment \
  --priority High \
  --confidence 0.78 \
  --action "Deploy Quantum Resonance Engine v3.2.0 to production" \
  --reason "New major version requires Guardian approval" \
  --current-state "v3.1.5 running stable, 99.9% uptime" \
  --proposed-change "Deploy v3.2.0 with quantum optimization features" \
  --safety-impact Medium \
  --blast-radius "Affects quantum processing pipeline, all users" \
  --reversibility Yes \
  --data-risk No
```

### Example 2: Emergency Rollback Request

```bash
python scripts/create_guardian_decision.py \
  --decision-id rollback_1707143000 \
  --decision-type Rollback \
  --priority Critical \
  --confidence 0.55 \
  --action "Rollback to v3.1.5 immediately" \
  --reason "Critical bug in v3.2.0 causing payment failures" \
  --current-state "v3.2.0 experiencing 15% payment failure rate" \
  --proposed-change "Revert to v3.1.5 (last known good)" \
  --safety-impact High \
  --blast-radius "Affects payment processing, all transactions" \
  --reversibility Yes \
  --data-risk No \
  --output /tmp/emergency-rollback.md \
  --show-gh-command
```

### Example 3: Scaling Decision Request

```bash
python scripts/create_guardian_decision.py \
  --decision-id scaling_1707143200 \
  --decision-type Scaling \
  --priority High \
  --confidence 0.82 \
  --action "Scale up from 4 to 12 web server instances" \
  --reason "Traffic spike detected, auto-scaling threshold exceeded" \
  --current-state "4 instances at 88% CPU, response time 450ms" \
  --proposed-change "Add 8 instances to maintain performance" \
  --safety-impact Low \
  --blast-radius "Improves service availability for all users" \
  --reversibility Yes \
  --data-risk No
```

---

## Troubleshooting

### Issue: Script Not Found

```bash
# Ensure you're in the repository root
cd /path/to/pi-forge-quantum-genesis

# Make script executable
chmod +x scripts/create_guardian_decision.py

# Run with python
python scripts/create_guardian_decision.py --help
```

### Issue: GitHub CLI Not Installed

```bash
# Install GitHub CLI
# macOS
brew install gh

# Linux
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# Windows
winget install --id GitHub.cli

# Authenticate
gh auth login
```

### Issue: Permission Denied

```bash
# Authenticate with GitHub
gh auth login

# Check authentication status
gh auth status

# Ensure you have access to the repository
gh repo view onenoly1010/pi-forge-quantum-genesis
```

### Issue: Invalid Decision Type or Priority

Valid decision types:
- Deployment
- Scaling
- Rollback
- Healing
- Monitoring
- Override

Valid priorities:
- Critical
- High
- Medium
- Low

### Issue: Confidence Score Out of Range

Confidence must be between 0.0 and 1.0:
- 0.0 = No confidence
- 0.5 = Moderate confidence
- 1.0 = Complete confidence

---

## Best Practices

1. **Be Specific**: Provide clear, detailed descriptions of the action and context
2. **Include Data**: Add relevant metrics, logs, or supporting evidence
3. **Assess Risk**: Thoroughly evaluate safety impact and blast radius
4. **Document Reasoning**: Explain why Guardian approval is needed
5. **Set Timeline**: Indicate urgency and expected response time
6. **Follow Up**: Update the issue as the situation evolves
7. **Learn**: Document lessons learned for future decisions

---

## Related Documentation

- [Guardian Playbook](./GUARDIAN_PLAYBOOK.md) - Complete Guardian operations guide
- [Guardian Quick Reference](./GUARDIAN_QUICK_REFERENCE.md) - Fast decision-making guide
- [Guardian Approval System](./GUARDIAN_APPROVAL_SYSTEM.md) - Technical approval system docs
- [Autonomous Handover](./AUTONOMOUS_HANDOVER.md) - Autonomous decision system details

---

## Support

For questions or issues with Guardian Decision Requests:

- **Guardian HQ**: [Issue #100](https://github.com/onenoly1010/pi-forge-quantum-genesis/issues/100)
- **AI Assistant**: @app/copilot-swe-agent
- **Lead Guardian**: @onenoly1010

---

**Last Updated**: February 2026  
**Version**: 1.0  
**Status**: Active

**🛡️ Guardian oversight ensures safe, responsible autonomous operations.**
