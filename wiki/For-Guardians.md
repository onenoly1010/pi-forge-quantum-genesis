# 🛡️ For Guardians - Guardian Team Responsibilities

**Last Updated**: December 2025

Welcome, Guardian! This guide covers your role in overseeing the Quantum Pi Forge autonomous AI platform.

---

## 🎯 Guardian Overview

### What is a Guardian?

Guardians are human overseers responsible for:
- **Critical decision approval** - Review autonomous AI decisions
- **System oversight** - Monitor platform health and operations
- **Incident response** - Coordinate emergency procedures
- **Safety enforcement** - Ensure ethical AI operation
- **Community stewardship** - Guide ecosystem evolution

### Current Guardian Team

**Lead Guardian**: @onenoly1010 (Kris Olofson)  
**AI Assistant**: @app/copilot  
**Guardian HQ**: [Issue #100](https://github.com/onenoly1010/pi-forge-quantum-genesis/issues/100)

**Future Roles**:
- Technical Guardian - System architecture
- Community Guardian - User support
- Economic Guardian - Tokenomics
- Compliance Guardian - Legal/regulatory

---

## 🔑 Core Responsibilities

### 1. Decision Oversight

Review and approve autonomous AI decisions based on confidence scores:

```
┌─────────────────────────────────────────────────┐
│ Confidence Score      │ Action                  │
├──────────────────────┼─────────────────────────┤
│ 0.9 - 1.0            │ Auto-approve (log only)  │
│ 0.8 - 0.9            │ Auto-approve (notify)    │
│ 0.6 - 0.8            │ Guardian review required │
│ 0.4 - 0.6            │ Detailed analysis needed │
│ 0.0 - 0.4            │ Reject or escalate       │
└─────────────────────────────────────────────────┘
```

**Your Role**: Review decisions with confidence < 0.8

### 2. System Monitoring

Monitor platform health:
- Daily health reports
- System metrics dashboards
- Error rate tracking
- Performance monitoring
- Security alerts

**Access**: [[Monitoring Observability]]

### 3. Incident Response

Lead emergency procedures:
- Respond to critical alerts within 1 hour
- Coordinate rollback procedures
- Lead post-incident reviews
- Update incident documentation
- Implement preventive measures

**Guide**: Emergency Procedures (below)

### 4. Policy & Governance

Guide ecosystem evolution:
- Update decision thresholds
- Refine autonomous rules
- Maintain documentation
- Approve major changes
- Enforce [[Genesis Declaration]] principles

### 5. Team Coordination

Work with AI agents and community:
- Triage with AI assistant
- Communicate with developers
- Support community members
- Report to stakeholders
- Onboard new guardians

---

## 🔐 Guardian Authority

### You Have Authority To:

✅ Approve or reject any autonomous decision  
✅ Override autonomous actions  
✅ Trigger emergency stops  
✅ Initiate rollbacks  
✅ Adjust system parameters  
✅ Grant temporary access for investigations  
✅ Enforce safety standards

### You Must Coordinate For:

⚠️ Major architectural changes  
⚠️ Smart contract deployments  
⚠️ Economic model adjustments  
⚠️ Policy changes affecting users  
⚠️ Genesis Declaration modifications

---

## 📋 Daily Operations

### Morning Routine (5-10 minutes)

#### 1. Check Guardian Dashboard

```bash
# Production
curl https://pi-forge-quantum-genesis.railway.app/api/guardian/dashboard | jq .
```

Review:
- System status (should be "healthy")
- Pending decisions count
- Recent autonomous actions
- Safety metrics (all > 0.7)
- Active alerts

#### 2. Review Health Report

- Check automated health reports (run every 6 hours)
- Verify all components green
- Note warnings or degraded services
- Review [[Monitoring Observability]]

#### 3. Review Pending Decisions

```bash
# Get decisions requiring approval
curl https://pi-forge-quantum-genesis.railway.app/api/autonomous/decision-history?requires_guardian=true&status=pending | jq .
```

For each decision:
1. Read decision details
2. Check confidence score
3. Review reasoning
4. Assess risk
5. Approve or schedule detailed review

#### 4. Check Overnight Activity

```bash
# Get last 12 hours of decisions
curl https://pi-forge-quantum-genesis.railway.app/api/autonomous/decision-history?limit=50&hours=12 | jq .
```

Look for:
- Unusual patterns
- High rejection rates
- Confidence score trends
- Failures or errors

### Throughout the Day

- Check email/alerts every 1-2 hours
- Review dashboard every 4 hours
- Respond to critical alerts within 1 hour
- Respond to high-priority within 4 hours

---

## 🚨 Emergency Procedures

### Critical Alert Response

**Within 1 hour**:

1. **Acknowledge alert**
   ```bash
   # Mark alert as acknowledged
   curl -X POST https://pi-forge-quantum-genesis.railway.app/api/guardian/alerts/{id}/acknowledge
   ```

2. **Assess severity**
   - System down?
   - Data breach?
   - Payment failure?
   - Security vulnerability?

3. **Take action**
   - Minor: Document and monitor
   - Major: Initiate incident response
   - Critical: Execute emergency stop

### Emergency Stop

**When to use**: Critical security issues, data integrity threats, systemic failures

```bash
# Trigger emergency stop
curl -X POST https://pi-forge-quantum-genesis.railway.app/api/guardian/emergency-stop \
  -H "Authorization: Bearer $GUARDIAN_TOKEN" \
  -d '{"reason": "Critical security vulnerability", "initiated_by": "guardian_username"}'
```

**This will**:
- Stop all autonomous operations
- Pause new user requests
- Alert all guardians
- Create incident report
- Preserve current state

### Rollback Procedure

**When to use**: Failed deployment, breaking changes, performance degradation

```bash
# Initiate rollback
curl -X POST https://pi-forge-quantum-genesis.railway.app/api/guardian/rollback \
  -H "Authorization: Bearer $GUARDIAN_TOKEN" \
  -d '{"target_version": "v1.2.3", "reason": "Performance degradation"}'
```

**Guide**: [[Deployment Guide]]

### Post-Incident Review

Within 24 hours of incident resolution:

1. **Document incident**
   - What happened
   - Timeline
   - Impact
   - Response actions

2. **Root cause analysis**
   - Why did it happen
   - Contributing factors
   - Similar past incidents

3. **Prevention measures**
   - What will prevent recurrence
   - System improvements
   - Process changes

4. **Update documentation**
   - [[Troubleshooting]]
   - [[Runbook Index]]
   - This guide

---

## 🎓 Decision Making

### Approval Framework

**Quick Approve** (< 5 minutes):
- Confidence >= 0.7
- Low/medium impact
- Easily reversible
- Routine operation
- Good historical performance

**Standard Review** (< 1 hour):
- Confidence 0.5-0.7
- Medium/high impact
- Some complexity
- Non-routine operation

**Deep Analysis** (< 4 hours):
- Confidence < 0.5
- High/critical impact
- Complex operation
- Novel scenario
- Unknown risks

**Escalate** (consult team):
- Confidence < 0.4
- Unclear requirements
- Policy implications
- Security concerns

### Decision Criteria

When reviewing decisions:

1. **Safety** - Security or stability risks?
2. **Impact** - Blast radius if wrong?
3. **Reversibility** - Can we roll back?
4. **Timing** - Right time for this?
5. **Context** - What else is happening?
6. **History** - Similar decisions before?

---

## 📊 Monitoring & Alerts

### Alert Channels

- **Slack** - Real-time notifications
- **Email** - Summary reports
- **Guardian Dashboard** - Visual overview
- **GitHub Issues** - Incident tracking

**Setup**: [[Monitoring Observability]]

### Alert Levels

**Critical** (1 hour response):
- System down
- Security breach
- Payment failures
- Data loss

**High** (4 hour response):
- Performance degradation
- High error rates
- Failed deployments
- Guardian approval needed

**Medium** (24 hour response):
- Warnings
- Unusual patterns
- Resource constraints
- Documentation needed

**Low** (review next check):
- Informational
- Routine events
- Success notifications
- Metrics updates

---

## 🤝 Communication

### Internal Communication

**With AI Agents**:
- Review decision logs
- Approve/reject via API
- Override when necessary
- Adjust thresholds

**With Developers**:
- GitHub issues
- Pull request reviews
- Slack/email
- Planning meetings

**With Other Guardians**:
- Guardian HQ (Issue #100)
- Shared dashboards
- Handoff notes
- Decision reviews

### External Communication

**With Community**:
- Transparent updates
- Incident reports (when appropriate)
- Policy changes
- Progress updates

**With Stakeholders**:
- Weekly summaries
- Incident reports
- Performance metrics
- Strategic updates

---

## 📚 Essential Documentation

### Must Read

- [[Genesis Declaration]] - Foundation
- [[Canon of Closure]] - Workflow
- [[Autonomous Agents]] - Agent system
- [[Monitoring Observability]] - Monitoring setup

### Reference Documents

- [[API Reference]] - API documentation
- [[Deployment Guide]] - Deployment procedures
- [[Runbook Index]] - Operational commands
- [[Troubleshooting]] - Common issues

### Guardian-Specific

- [[Guardian Playbook]] - Full playbook (docs/)
- [[Operational Team]] - Team structure (docs/)
- [[Identity Lock]] - Identity verification

---

## 🎯 Onboarding New Guardians

### Onboarding Process

1. **Review Canon** - Read all documentation
2. **Shadow** - Observe for 2 weeks
3. **Training** - Complete modules
4. **Demonstrate** - Show decision-making
5. **Credentials** - Receive access

### Training Checklist

- [ ] Read [[Genesis Declaration]]
- [ ] Understand [[Canon of Closure]]
- [ ] Review [[Guardian Playbook]]
- [ ] Complete decision-making scenarios
- [ ] Shadow lead guardian for 2 weeks
- [ ] Review past incidents
- [ ] Demonstrate emergency procedures
- [ ] Receive guardian credentials

---

## 🛠️ Tools & Access

### Required Tools

- **Guardian Dashboard** - https://pi-forge-quantum-genesis.railway.app/guardian
- **Grafana** - Metrics visualization
- **GitHub** - Issue tracking, PRs
- **Slack** - Real-time alerts
- **Email** - Summary reports

### Required Access

- Guardian API credentials
- Admin GitHub permissions
- Monitoring dashboards
- Alert management
- Deployment controls

---

## 📈 Performance Metrics

### Guardian Effectiveness

Track:
- Decision review time
- Approval accuracy
- Incident response time
- False positive rate
- Community satisfaction

### System Health

Monitor:
- Uptime percentage
- Error rates
- Performance metrics
- Security incidents
- User growth

---

## 🌟 Thank You!

Thank you for serving as a Guardian. Your oversight ensures Quantum Pi Forge operates ethically, safely, and transparently.

**You are the human conscience of the system.** 🛡️⚛️🔥

---

## See Also

- [[Home]] - Wiki home
- [[Genesis Declaration]] - Core principles
- [[Autonomous Agents]] - Agent system
- [[Monitoring Observability]] - Monitoring setup
- [[Operational Team]] - Team structure (docs/)
- [[Guardian Playbook]] - Full playbook (docs/)

---

[[Home]] | [[For Users]] | [[For Developers]] | [[Autonomous Agents]]

---

*The Guardian ensures the balance between autonomy and safety.* 🛡️✨
