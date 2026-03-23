# 🛡️ Guardian Decision Request System

## Quick Overview

The Guardian Decision Request system provides structured human oversight for autonomous AI decisions in the Pi Forge Quantum Genesis platform. When the autonomous system encounters a decision that requires human judgment, it creates a Guardian Decision Request issue for review and approval.

## 🎯 Key Features

- **Structured Decision Templates**: Standardized format for decision requests
- **Automated Issue Creation**: CLI tool and Python API for creating requests
- **Risk Assessment Framework**: Built-in safety and impact evaluation
- **Integration Ready**: Works seamlessly with autonomous decision system
- **GitHub-Native**: Uses GitHub Issues for tracking and collaboration

## 🚀 Quick Start

### Create Your First Guardian Decision Request

```bash
# Example: Deployment decision
python scripts/create_guardian_decision.py \
  --decision-id deployment_$(date +%s) \
  --decision-type Deployment \
  --priority High \
  --confidence 0.75 \
  --action "Deploy version 2.1.0 to production" \
  --reason "Confidence below threshold, requires Guardian review" \
  --output /tmp/guardian-decision.md
```

### View the Generated Request

```bash
cat /tmp/guardian-decision.md
```

### Create GitHub Issue (if you have GitHub CLI)

```bash
gh issue create \
  --title "[GUARDIAN] Deployment - deployment_$(date +%s)" \
  --body-file /tmp/guardian-decision.md \
  --label "guardian-decision,needs-approval" \
  --assignee onenoly1010
```

## 📋 Decision Types

The system supports six types of decisions:

| Type | Description | Typical Confidence Threshold |
|------|-------------|------------------------------|
| **Deployment** | Code deployments to production | 0.80 |
| **Scaling** | Resource scaling (up or down) | 0.85 |
| **Rollback** | Reverting to previous version | 0.70 |
| **Healing** | Self-healing actions | 0.75 |
| **Monitoring** | Monitoring configuration changes | 0.85 |
| **Override** | Manual override of autonomous decisions | N/A (always requires Guardian) |

## 🎨 Usage Examples

### Example 1: Emergency Rollback

```bash
python scripts/create_guardian_decision.py \
  --decision-id rollback_emergency_$(date +%s) \
  --decision-type Rollback \
  --priority Critical \
  --confidence 0.60 \
  --action "Rollback to version 2.0.9 immediately" \
  --reason "Critical bug causing 15% payment failures" \
  --current-state "v2.1.0 experiencing payment failures" \
  --proposed-change "Revert to last known good version 2.0.9" \
  --safety-impact High \
  --blast-radius "Affects payment processing, all transactions" \
  --reversibility Yes \
  --data-risk No
```

### Example 2: Scaling Decision

```bash
python scripts/create_guardian_decision.py \
  --decision-id scaling_$(date +%s) \
  --decision-type Scaling \
  --priority High \
  --confidence 0.82 \
  --action "Scale up from 4 to 12 web server instances" \
  --reason "Sustained high CPU usage above 85%" \
  --current-state "4 instances at 88% CPU, 450ms response time" \
  --proposed-change "Add 8 instances to handle increased load" \
  --safety-impact Low \
  --blast-radius "Improves availability for all users" \
  --reversibility Yes
```

### Example 3: Routine Deployment

```bash
python scripts/create_guardian_decision.py \
  --decision-id deployment_$(date +%s) \
  --decision-type Deployment \
  --priority Medium \
  --confidence 0.88 \
  --action "Deploy minor version update 2.1.3" \
  --reason "Routine deployment following standard process" \
  --current-state "v2.1.2 running stable" \
  --proposed-change "Deploy v2.1.3 with bug fixes" \
  --safety-impact Low
```

## 🔧 Python API Usage

### Using the Guardian Issue Creator

```python
from server.guardian_issue_creator import create_guardian_issue_for_decision

# Prepare decision data
decision_data = {
    "decision_id": "deployment_1707142800",
    "decision_type": "deployment",
    "confidence": 0.75,
    "reasoning": "All tests passed, ready for production deployment",
    "actions": [
        "Deploy version 2.1.0",
        "Run smoke tests",
        "Monitor for 1 hour"
    ],
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

# Create issue (auto_create=False for testing)
result = create_guardian_issue_for_decision(
    decision_data,
    auto_create=False
)

print(f"Decision ID: {result['decision_id']}")
print(f"Issue Title: {result['issue_title']}")
print(f"Issue Body:\n{result['issue_body']}")

# To actually create the GitHub issue, set auto_create=True
# (requires GitHub CLI to be installed and authenticated)
```

### Integration with Autonomous Decision System

```python
from server.autonomous_decision import AIDecisionMatrix, DecisionContext
from server.guardian_issue_creator import create_guardian_issue_for_decision

# In your autonomous decision logic
matrix = AIDecisionMatrix()
context = DecisionContext(
    decision_type=DecisionType.DEPLOYMENT,
    priority=DecisionPriority.HIGH,
    parameters=[...],
    metadata={...}
)

result = matrix.make_decision(context)

# If Guardian approval required
if result.requires_guardian:
    decision_data = {
        "decision_id": result.decision_id,
        "decision_type": result.decision_type.value,
        "confidence": result.confidence,
        "reasoning": result.reasoning,
        "actions": result.actions,
        "metadata": result.metadata
    }
    
    # Create Guardian Decision Request
    issue = create_guardian_issue_for_decision(
        decision_data,
        auto_create=True  # Auto-create if GH CLI available
    )
    
    if issue and issue.get('created'):
        print(f"✅ Guardian approval requested: {issue['issue_url']}")
```

## 📖 CLI Reference

### Required Arguments

- `--decision-id`: Unique identifier (e.g., `deployment_1234567890`)
- `--decision-type`: Type of decision (Deployment, Scaling, Rollback, Healing, Monitoring, Override)
- `--priority`: Priority level (Critical, High, Medium, Low)
- `--confidence`: Confidence score from 0.0 to 1.0
- `--action`: Clear description of the requested action
- `--reason`: Why Guardian approval is needed

### Optional Arguments

- `--current-state`: Description of current system state
- `--proposed-change`: Details of what will change
- `--safety-impact`: Low, Medium, or High
- `--blast-radius`: Scope of potential impact
- `--reversibility`: Yes or No
- `--data-risk`: Yes or No
- `--requested-by`: System or User (default: System)

### Output Options

- `--output FILE`: Save to file instead of stdout
- `--show-gh-command`: Display GitHub CLI command to create issue
- `--json`: Output as JSON format

## 🎓 Decision Criteria

### When Guardian Approval is Required

Guardian approval is automatically required when:

1. **Low Confidence** (< 0.8): Decision confidence below threshold
2. **High Priority**: Critical or high-priority changes
3. **High Impact**: Changes affecting multiple services
4. **Data Risk**: Potential data integrity concerns
5. **Security Impact**: Security-related changes
6. **Novel Situations**: Scenarios not covered by rules
7. **Policy Questions**: Requires policy interpretation

### Guardian Response Options

When reviewing a Guardian Decision Request, the Guardian can:

1. **Approve**: Decision meets all criteria, proceed
2. **Reject**: Decision has issues, block execution
3. **Need More Info**: Additional context required
4. **Escalate**: Requires team discussion

## 🔗 Integration Points

### With Approval System

```bash
# After Guardian approves, record approval
python scripts/record_guardian_approval.py record deployment_1234567890 \
  --guardian onenoly1010 \
  --reasoning "Approved - all criteria met"
```

### With Monitoring System

```python
from server.guardian_monitor import get_guardian_monitor

monitor = get_guardian_monitor()

# Validate decision before creating request
validation = monitor.validate_decision(
    decision_id="deployment_123",
    decision_data={...}
)

if validation.status == "pending":
    # Create Guardian Decision Request
    create_guardian_issue_for_decision(...)
```

## 📚 Documentation

- **[Guardian Playbook](./docs/GUARDIAN_PLAYBOOK.md)**: Complete operations guide
- **[Guardian Quick Reference](./docs/GUARDIAN_QUICK_REFERENCE.md)**: Fast decision-making guide
- **[Guardian Decision Workflow](./docs/GUARDIAN_DECISION_WORKFLOW.md)**: Detailed workflow documentation
- **[Guardian Approval System](./docs/GUARDIAN_APPROVAL_SYSTEM.md)**: Technical approval system docs

## 🛠️ Files & Components

### Core Files

- `scripts/create_guardian_decision.py`: CLI tool for creating requests
- `server/guardian_issue_creator.py`: Python API for issue creation
- `.github/ISSUE_TEMPLATE/guardian-decision-template.md`: GitHub issue template
- `tests/test_guardian_issue_creator.py`: Test suite

### Related Systems

- `server/guardian_approvals.py`: Approval recording system
- `server/guardian_monitor.py`: Monitoring and validation
- `server/autonomous_decision.py`: Autonomous decision engine

## 🚨 Troubleshooting

### GitHub CLI Not Found

```bash
# Install GitHub CLI
# macOS: brew install gh
# Linux: See https://cli.github.com/
# Windows: winget install --id GitHub.cli

# Authenticate
gh auth login
```

### Permission Denied

```bash
# Ensure script is executable
chmod +x scripts/create_guardian_decision.py

# Run with python explicitly
python scripts/create_guardian_decision.py [args]
```

### Invalid Arguments

Check that:
- Decision type is one of: Deployment, Scaling, Rollback, Healing, Monitoring, Override
- Priority is one of: Critical, High, Medium, Low
- Confidence is between 0.0 and 1.0

## 🤝 Contributing

To contribute improvements to the Guardian Decision system:

1. Test changes with various decision types
2. Run test suite: `python -m pytest tests/test_guardian_issue_creator.py`
3. Update documentation as needed
4. Submit PR with clear description

## 📞 Support

- **Guardian HQ**: [Issue #100](https://github.com/onenoly1010/pi-forge-quantum-genesis/issues/100)
- **AI Assistant**: @app/copilot-swe-agent
- **Lead Guardian**: @onenoly1010

## 📝 License

Part of the Pi Forge Quantum Genesis project.

---

**Last Updated**: February 2026  
**Version**: 1.0.0

**🛡️ Guardian oversight ensures safe, responsible autonomous operations.**
