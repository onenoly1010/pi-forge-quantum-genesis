# Guardian Documentation

Welcome to the Guardian Team documentation for Pi Forge Quantum Genesis autonomous operations.

## 📚 Documentation Index

### Core Documentation

1. **[Guardian Playbook](GUARDIAN_PLAYBOOK.md)** - Complete operational guide (1,419 lines)
   - Full 9-section operational manual
   - Comprehensive decision-making procedures
   - Templates for all decision types
   - Emergency protocols and escalation procedures

2. **[Guardian Quick Reference](GUARDIAN_QUICK_REFERENCE.md)** - One-page cheat sheet (344 lines)
   - Fast lookup for response times and thresholds
   - Quick CLI commands
   - Emergency action procedures
   - Decision matrices

3. **[Guardian Decision Template](../.github/ISSUE_TEMPLATE/guardian-decision-template.md)** - Structured decision template (200 lines)
   - Use this template for all guardian decisions
   - Includes checkboxes, reasoning fields, and audit trail
   - Ensures comprehensive decision documentation

4. **[Issue #100 Update Instructions](ISSUE_100_UPDATE.md)** - Content for Guardian Team HQ
   - Instructions for adding Guardian Resources section to Issue #100
   - Links and quick reference material

### Supporting Documentation

- **[Autonomous Handover](AUTONOMOUS_HANDOVER.md)** - AI-driven decision system documentation
- **[AI Agent Quick Reference](AI_AGENT_QUICK_REFERENCE.md)** - AI agent operational commands

## 👥 Guardian Team

| Role | GitHub Handle | Responsibilities |
|------|---------------|------------------|
| **Guardian Lead** | @onenoly1010 | Final authority, critical decisions, strategic direction |
| **Guardian Assistant** | @app/copilot-swe-agent | Monitoring, triage, routine decisions |

**Team HQ:** Issue #100  
**Assistant Assignment:** Issue #102  
**Established:** 2025-12-14

## 🚀 Quick Start

### For New Guardians

1. Read the [Guardian Playbook](GUARDIAN_PLAYBOOK.md) - Focus on sections 1-3 first
2. Review the [Quick Reference](GUARDIAN_QUICK_REFERENCE.md) - Keep this handy
3. Familiarize yourself with the [Decision Template](../.github/ISSUE_TEMPLATE/guardian-decision-template.md)
4. Bookmark Issue #100 (Team HQ)

### For Emergency Response

1. Go to [Quick Reference - Emergency Actions](GUARDIAN_QUICK_REFERENCE.md#emergency-actions)
2. Follow the appropriate emergency protocol from [Playbook Section 4](GUARDIAN_PLAYBOOK.md#4-emergency-protocols)
3. Document all actions in Issue #100

### For Making Decisions

1. Review the request and gather context
2. Check the appropriate decision type in [Playbook Section 2](GUARDIAN_PLAYBOOK.md#2-decision-types-and-confidence-thresholds)
3. Use the relevant template from [Playbook Section 5](GUARDIAN_PLAYBOOK.md#5-decision-templates)
4. Document using the [Decision Template](../.github/ISSUE_TEMPLATE/guardian-decision-template.md)
5. Post to Issue #100

## 🎯 Decision Types

| Decision Type | Confidence Threshold | Description |
|---------------|---------------------|-------------|
| **DEPLOYMENT** | 0.8 | Deploy code, features, or configurations |
| **SCALING** | 0.7 | Scale resources up or down |
| **ROLLBACK** | 0.9 | Revert to previous stable version |
| **HEALING** | 0.85 | Automated system repairs |
| **MONITORING** | 0.6 | Adjust monitoring levels and alerts |
| **GUARDIAN_OVERRIDE** | 0.95 | Manual guardian intervention |

## ⚡ Priority Levels

| Priority | Response Time (Assistant) | Response Time (Lead) |
|----------|--------------------------|---------------------|
| **CRITICAL** | Immediate → Lead | 15 minutes |
| **HIGH** | 15 minutes | 1 hour |
| **MEDIUM** | 30 minutes | 4 hours |
| **LOW** | 2 hours | 24 hours |

## 📊 Key Thresholds

### Safety Metrics
- Transaction Safety: 0.95
- Ethical Compliance: 0.90
- Security Score: 0.90
- System Stability: 0.85

### Resource Thresholds
- CPU Scale Up: 75%
- Memory Scale Up: 80%
- Error Rate Rollback: 5%
- Max Healing Retries: 3

## 🔗 Quick Links

### Daily Operations
- [Daily Tasks](GUARDIAN_QUICK_REFERENCE.md#-daily-tasks)
- [Monitoring Guidelines](GUARDIAN_PLAYBOOK.md#6-monitoring-guidelines)
- [Common Scenarios](GUARDIAN_PLAYBOOK.md#7-common-scenarios)

### Emergency Procedures
- [Emergency Stop](GUARDIAN_PLAYBOOK.md#emergency-stop)
- [Emergency Rollback](GUARDIAN_PLAYBOOK.md#emergency-rollback)
- [Service Degradation Response](GUARDIAN_PLAYBOOK.md#service-degradation-response)

### Decision Making
- [Escalation Procedures](GUARDIAN_PLAYBOOK.md#3-escalation-procedures)
- [Decision Templates](GUARDIAN_PLAYBOOK.md#5-decision-templates)
- [Decision Checklist](GUARDIAN_QUICK_REFERENCE.md#-quick-decision-checklist)

### Tools & Commands
- [CLI Tools](GUARDIAN_PLAYBOOK.md#8-cli-tools-and-commands)
- [Quick Commands](GUARDIAN_QUICK_REFERENCE.md#-common-cli-commands)
- [API Endpoints](GUARDIAN_PLAYBOOK.md#api-endpoints)

### Audit & Compliance
- [Audit Procedures](GUARDIAN_PLAYBOOK.md#9-audit-procedures)
- [Weekly Reports](GUARDIAN_PLAYBOOK.md#weekly-audit-review)
- [Incident Post-Mortems](GUARDIAN_PLAYBOOK.md#incident-post-mortems)

## 🛠️ Essential Commands

### Emergency Actions
```bash
# Emergency Stop
gh workflow run "ai-agent-handoff-runbook.yml" --field action=emergency-stop

# Fast Rollback
gh workflow run "ai-agent-handoff-runbook.yml" --field action=rollback

# Health Check
gh workflow run "ai-agent-handoff-runbook.yml" --field action=health-check
```

### Monitoring
```bash
# View Team HQ
gh issue view 100

# Check recent workflow runs
gh run list --workflow=ai-agent-handoff-runbook.yml --limit 10

# Watch live run
gh run watch <run-id>
```

## 📋 Daily Checklist

### Guardian Assistant (Daily)
- [ ] Review autonomous decisions in Issue #100
- [ ] Check safety metrics dashboard
- [ ] Verify all auto-approved decisions
- [ ] Monitor system health trends
- [ ] Update status in Issue #100

### Guardian Lead (Daily)
- [ ] Review Guardian Assistant summary
- [ ] Approve pending HIGH priority decisions
- [ ] Check for pattern anomalies
- [ ] Review escalations and overrides

## 🆘 Emergency Contact

**For Critical Issues:**
1. Post to Issue #100 with 🚨
2. @mention @onenoly1010
3. Use CRITICAL priority
4. Include brief context
5. Suggest immediate action

**Emergency Format:**
```
@onenoly1010 🚨 CRITICAL

[One-line issue description]

Required: [specific action]
Timeline: [urgency]

Details in Issue #100
```

## 📈 Success Metrics

Track these metrics weekly:
- Total decisions by type
- Auto-approval rate
- Average confidence scores
- Guardian override count
- Escalations count
- Incident response times

## 🔄 Document Updates

**Update Frequency:**
- Minor updates: As needed
- Major updates: After significant incidents or quarterly review
- Version bumps: With any decision rule changes

**Update Process:**
1. Propose changes in Issue #100
2. Guardian Lead review and approval
3. Update document with version increment
4. Notify team of changes

## 📞 Support Resources

**Primary Communication:** Issue #100 (Guardian Team HQ)

**External Resources:**
- Railway Dashboard: Monitor deployments
- Supabase Dashboard: Database operations
- GitHub Actions: Workflow runs

**Runbooks:**
- Production Deployment: `PRODUCTION_DEPLOYMENT.md`
- Rollback Validation: `ROLLBACK_VALIDATION.md`
- AI Agent Operations: `AI_AGENT_HANDOFF_RUNBOOK.md`

## 🎓 Training Resources

### For Guardian Assistant Role
1. Study [Autonomous Handover](AUTONOMOUS_HANDOVER.md)
2. Practice with LOW priority decisions
3. Shadow Guardian Lead on MEDIUM decisions
4. Review [Common Scenarios](GUARDIAN_PLAYBOOK.md#7-common-scenarios)

### For Guardian Lead Role
1. Master all sections of the [Playbook](GUARDIAN_PLAYBOOK.md)
2. Review incident post-mortems
3. Understand system architecture
4. Practice emergency procedures

## 📝 Version History

- **v1.0.0** (2025-12-14): Initial guardian documentation suite
  - Guardian Playbook created
  - Quick Reference guide created
  - Decision template created
  - Issue #100 update instructions created

## 🤝 Contributing

All guardian team members are encouraged to suggest improvements:
1. Identify issue or improvement
2. Post to Issue #100 with `#playbook-update` tag
3. Discuss with team
4. Guardian Lead approves changes
5. Update documentation
6. Notify team of changes

---

**Guardian Documentation Version:** 1.0.0  
**Last Updated:** 2025-12-14  
**Maintained by:** Guardian Team (@onenoly1010, @app/copilot-swe-agent)  
**Team HQ:** Issue #100

---

*For comprehensive details, always refer to the full [Guardian Playbook](GUARDIAN_PLAYBOOK.md)*
