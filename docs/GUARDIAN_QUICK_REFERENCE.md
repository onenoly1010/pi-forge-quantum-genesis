# 🛡️ Guardian Quick Reference

**One-Page Cheat Sheet for Guardian Operations**

## 👥 Guardian Team

| Role | Contact | Authority |
|------|---------|-----------|
| **Guardian Lead** | @onenoly1010 | All decisions, final authority |
| **Guardian Assistant** | @app/copilot-swe-agent | LOW/MEDIUM decisions, triage |
| **Team HQ** | Issue #100 | Central coordination |
| **Assistant Assignment** | Issue #102 | Task tracking |

---

## ⚡ Response Times

| Priority | Assistant | Lead | Escalation |
|----------|-----------|------|------------|
| **CRITICAL** | Immediate → Lead | 15 min | Immediate |
| **HIGH** | 15 min | 1 hour | If confidence < threshold |
| **MEDIUM** | 30 min | 4 hours | If complex |
| **LOW** | 2 hours | 24 hours | Optional |

---

## 🎯 Decision Types & Thresholds

| Type | Confidence | Max Auto-Approve | Key Checks |
|------|------------|------------------|------------|
| **DEPLOYMENT** | 0.8 | MEDIUM | health, tests, security |
| **SCALING** | 0.7 | HIGH | CPU, memory, cost |
| **ROLLBACK** | 0.9 | CRITICAL | error rate, availability |
| **HEALING** | 0.85 | HIGH | process health, retries |
| **MONITORING** | 0.6 | MEDIUM | metrics, trends |
| **GUARDIAN_OVERRIDE** | 0.95 | **NEVER** | all checks |

---

## 🚨 Emergency Actions

### Immediate Commands

```bash
# Emergency Stop (Critical breach/runaway process)
gh workflow run "ai-agent-handoff-runbook.yml" --field action=emergency-stop

# Fast Rollback (5-10 min)
gh workflow run "ai-agent-handoff-runbook.yml" --field action=rollback

# Health Check
gh workflow run "ai-agent-handoff-runbook.yml" --field action=health-check
```

### Emergency Escalation

```
@onenoly1010 🚨 URGENT: [Brief issue]
Priority: CRITICAL
Type: [type]
Action needed: [specific action]
Issue: #100
```

---

## 📊 Monitoring Levels

| Level | Trigger | Auto-Approval | Action |
|-------|---------|---------------|--------|
| **NORMAL** | Standard ops | Most decisions | Standard monitoring |
| **ELEVATED** | 1 metric low | Restricted | Increase checks |
| **HIGH** | Multiple metrics low | Minimal | Guardian review |
| **CRITICAL** | Critical incident | Healing only | Lead approval |

---

## 🔍 Safety Metrics

| Metric | Threshold | Alert At |
|--------|-----------|----------|
| Transaction Safety | 0.95 | < 0.95 |
| Ethical Compliance | 0.90 | < 0.90 |
| Security Score | 0.90 | < 0.90 |
| System Stability | 0.85 | < 0.85 |

**Alert Levels:**
- < Threshold: ELEVATED
- < (Threshold - 0.10): HIGH
- < (Threshold - 0.20): CRITICAL

---

## 📋 Quick Decision Checklist

### ✅ Approve If:
- [ ] Confidence ≥ threshold
- [ ] Priority within auto-approve limit
- [ ] All required checks passing
- [ ] No recent similar failures
- [ ] Monitoring level allows

### ❌ Reject If:
- [ ] Confidence < threshold
- [ ] Security concerns
- [ ] Missing required checks
- [ ] Budget exceeded (scaling)
- [ ] Risk too high

### 🔄 Escalate If:
- [ ] Uncertainty about decision
- [ ] Novel situation
- [ ] Priority above authority
- [ ] Policy violation suspected
- [ ] Multiple concurrent issues

---

## 🛠️ Common CLI Commands

### Workflow Management
```bash
# List recent runs
gh run list --workflow=ai-agent-handoff-runbook.yml --limit 10

# Watch live
gh run watch <run-id>

# View logs
gh run view <run-id> --log

# Re-run failed
gh run rerun <run-id> --failed
```

### Issue Management
```bash
# View Team HQ
gh issue view 100

# List guardian issues
gh issue list --label guardian

# Comment on issue
gh issue comment 100 --body "Decision: [details]"
```

### Monitoring
```bash
# Check recent deployments
git tag -l "deploy-*" --sort=-version:refname | head -5

# Service health
curl https://[service]/health
```

---

## 🔄 Decision Response Template

```markdown
## Decision: [TYPE] - [APPROVED/REJECTED/MODIFIED]

**ID:** [decision_id]
**Priority:** [priority]
**Confidence:** [X.XX]

### Reasoning
[Brief reasoning]

### Action
- [ ] ✅ APPROVED / ❌ REJECTED / 🔄 MODIFIED

**Guardian:** @[username]
**Time:** [timestamp]
```

---

## 📈 Scaling Quick Reference

### Scale UP Triggers
- CPU > 75% for 5+ min
- Memory > 80% for 5+ min
- Response time > 2x baseline
- Queue depth growing

### Scale DOWN Triggers
- CPU < 40% for 10+ min
- Memory < 50% for 10+ min
- Low traffic period
- Cost optimization

**Cooldown:** 10 minutes between scaling actions

---

## ⏮️ Rollback Quick Reference

### Automatic Rollback Triggers
- Error rate > 5%
- 3+ consecutive health check failures
- Response time > 2x baseline
- Service unavailable

### Rollback Commands
```bash
# Latest
gh workflow run "ai-agent-handoff-runbook.yml" --field action=rollback

# Specific version
gh workflow run "ai-agent-handoff-runbook.yml" \
  --field action=rollback \
  --field rollback_version="deploy-YYYYMMDD-HHMMSS-hash"
```

---

## 🏥 Healing Quick Reference

### Auto-Healing Actions
1. **Process Restart** (most common)
2. **Service Restart** (if process restart fails)
3. **Cache Clear** (for cache issues)
4. **Connection Reset** (for network issues)
5. **Memory Cleanup** (for memory leaks)

### Healing Limits
- **Max Attempts:** 3
- **Cooldown:** 5 minutes
- **Escalate After:** 3 failures

---

## 📞 Escalation Matrix

| Scenario | Handler | Escalate To | Time |
|----------|---------|-------------|------|
| LOW decision | Assistant | Lead (if complex) | 2h |
| MEDIUM decision | Assistant | Lead (if conf < 0.8) | 30m |
| HIGH decision | Lead | N/A | 15m |
| CRITICAL decision | Lead | N/A | 15m |
| Emergency | Both | External if needed | 5m |
| Security | Lead | Security team | Immediate |

---

## 🗓️ Daily Tasks

### Guardian Assistant
- [ ] Review autonomous decisions in Issue #100
- [ ] Check safety metrics
- [ ] Verify auto-approved decisions
- [ ] Monitor system health
- [ ] Update status summary

### Guardian Lead
- [ ] Review assistant summary
- [ ] Approve pending HIGH decisions
- [ ] Check for anomalies
- [ ] Review escalations

---

## 📚 Key Resources

**Documentation:**
- Full Playbook: `docs/GUARDIAN_PLAYBOOK.md`
- Autonomous Handover: `docs/AUTONOMOUS_HANDOVER.md`
- AI Agent Reference: `docs/AI_AGENT_QUICK_REFERENCE.md`

**Templates:**
- Decision Template: `.github/ISSUE_TEMPLATE/guardian-decision-template.md`

**API Endpoints:**
- Decision: `POST /api/autonomous/decision`
- History: `GET /api/autonomous/decision-history`
- Override: `POST /api/guardian/override`
- Monitoring: `GET /api/monitoring/status`

---

## 🎯 Priority Decision Matrix

| Priority | Can Approve | Must Escalate | Response |
|----------|-------------|---------------|----------|
| **LOW** | Assistant | Never | 2 hours |
| **MEDIUM** | Assistant | If conf < 0.8 | 30 min |
| **HIGH** | Lead | To Lead (from Asst) | 15 min |
| **CRITICAL** | Lead only | External if needed | 15 min |

---

## 🚦 Status Indicators

| Icon | Status | Meaning |
|------|--------|---------|
| 🟢 | success | All systems go |
| 🟡 | warning | Attention needed |
| 🔴 | failed | Critical issue |
| 🔄 | rolled_back | System recovered |
| ⏭️ | skipped | Not applicable |
| 🚨 | emergency | Urgent action |

---

## 💡 Quick Tips

1. **When in doubt, escalate** - Better safe than sorry
2. **Document everything** - All decisions go to Issue #100
3. **Watch confidence scores** - Low confidence = more scrutiny
4. **Monitor after actions** - Verify success for 30+ min
5. **Know your limits** - Stick to your authority level
6. **Use templates** - Ensures complete documentation
7. **Check recent history** - Learn from similar decisions

---

## 🆘 Emergency Contact

**Critical Issues:**
1. Post to Issue #100 with 🚨
2. @mention @onenoly1010
3. Use CRITICAL priority
4. Include brief context
5. Suggest immediate action

**Template:**
```
@onenoly1010 🚨 CRITICAL

[One-line issue description]

Required: [specific action]
Timeline: [urgency]

Details in Issue #100
```

---

**Version:** 1.0.0 | **Updated:** 2025-12-14  
**Team HQ:** Issue #100 | **Full Playbook:** `docs/GUARDIAN_PLAYBOOK.md`  
**Guardian Lead:** @onenoly1010 | **Assistant:** @app/copilot-swe-agent
