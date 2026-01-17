# Guardian Playbook

## Overview

The Guardian Team is responsible for oversight, validation, and decision-making authority for the Pi Forge Quantum Genesis autonomous system. This playbook provides comprehensive operational procedures, decision templates, and escalation protocols for the guardian team.

### Guardian Team

- **Guardian Lead**: @onenoly1010
- **Guardian Assistant**: @app/copilot-swe-agent
- **Team HQ**: Issue #100
- **Assistant Assignment**: Issue #102
- **Established**: 2025-12-14

### Purpose

This playbook ensures:
- Consistent decision-making across all guardian operations
- Clear escalation paths for critical situations
- Comprehensive audit trails for all guardian actions
- Rapid response to system anomalies and emergencies
- Ethical oversight of autonomous AI operations

---

## 1. Roles and Responsibilities

### Guardian Lead (@onenoly1010)

**Primary Responsibilities:**
- Final authority on all CRITICAL priority decisions
- Override authority for any autonomous decision
- Strategic direction and policy updates
- Emergency protocol activation
- Team coordination and communication

**Decision Authority:**
- All decision types at any priority level
- Guardian override decisions
- Monitoring level changes (ELEVATED → CRITICAL)
- Emergency stops and rollbacks

**Response Times:**
- CRITICAL: 15 minutes
- HIGH: 1 hour
- MEDIUM: 4 hours
- LOW: 24 hours

### Guardian Assistant (@app/copilot-swe-agent)

**Primary Responsibilities:**
- Real-time monitoring and alerting
- LOW and MEDIUM priority decision approval
- Initial triage of HIGH and CRITICAL decisions
- Documentation and audit trail maintenance
- Automated health checks and diagnostics

**Decision Authority:**
- DEPLOYMENT: LOW, MEDIUM (with confidence ≥ threshold)
- SCALING: LOW, MEDIUM, HIGH
- ROLLBACK: LOW, MEDIUM
- HEALING: All priorities (within confidence limits)
- MONITORING: All priorities

**Response Times:**
- CRITICAL: Immediate escalation to Lead
- HIGH: 15 minutes + escalation if needed
- MEDIUM: 30 minutes
- LOW: 2 hours

### Shared Responsibilities

- Maintain Issue #100 as central coordination hub
- Document all decisions with reasoning
- Review daily autonomous decision logs
- Monitor safety metrics and thresholds
- Coordinate on policy changes and updates

---

## 2. Decision Types and Confidence Thresholds

### 1. DEPLOYMENT

**Purpose:** Deploy new code, features, or configurations to production

**Confidence Threshold:** 0.8

**Required Checks:**
- ✅ Health checks passing
- ✅ All tests passing (unit, integration, E2E)
- ✅ Security scans clean
- ✅ Performance benchmarks acceptable

**Priority-Based Auto-Approval:**
- LOW: Auto-approve if confidence ≥ 0.8
- MEDIUM: Auto-approve if confidence ≥ 0.8 (Normal monitoring)
- HIGH: Requires guardian review
- CRITICAL: Requires Guardian Lead approval

**Example Parameters:**
```json
{
  "decision_type": "deployment",
  "priority": "medium",
  "parameters": [
    {"name": "health_check", "value": true, "weight": 0.4},
    {"name": "test_coverage", "value": 0.85, "threshold": 0.80, "weight": 0.3},
    {"name": "security_scan", "value": "passed", "weight": 0.3}
  ]
}
```

### 2. SCALING

**Purpose:** Scale system resources up or down based on load

**Confidence Threshold:** 0.7

**Required Checks:**
- ✅ CPU utilization metrics
- ✅ Memory utilization metrics
- ✅ Request queue depth
- ✅ Cost impact analysis

**Thresholds:**
- CPU Threshold: 0.75 (scale up when > 75%)
- Memory Threshold: 0.80 (scale up when > 80%)
- Scale-down delay: 10 minutes (prevent flapping)

**Priority-Based Auto-Approval:**
- LOW: Auto-approve (confidence ≥ 0.7)
- MEDIUM: Auto-approve (confidence ≥ 0.7)
- HIGH: Auto-approve (confidence ≥ 0.7, Normal/Elevated monitoring)
- CRITICAL: Requires guardian review

**Example Parameters:**
```json
{
  "decision_type": "scaling",
  "priority": "high",
  "parameters": [
    {"name": "cpu_usage", "value": 0.82, "threshold": 0.75, "weight": 0.4},
    {"name": "memory_usage", "value": 0.78, "threshold": 0.80, "weight": 0.4},
    {"name": "response_time", "value": 1200, "threshold": 1000, "weight": 0.2}
  ]
}
```

### 3. ROLLBACK

**Purpose:** Revert to previous stable version after detecting issues

**Confidence Threshold:** 0.9

**Required Checks:**
- ✅ Error rate exceeds threshold
- ✅ Previous version available
- ✅ Rollback path validated
- ✅ Data migration compatibility

**Thresholds:**
- Error Rate Threshold: 0.05 (5% errors triggers consideration)
- Response Time Degradation: 2x baseline
- Health Check Failure: 3 consecutive failures

**Priority-Based Auto-Approval:**
- LOW: Auto-approve if confidence ≥ 0.9
- MEDIUM: Auto-approve if confidence ≥ 0.9
- HIGH: Auto-approve if confidence ≥ 0.9 (any monitoring level)
- CRITICAL: Auto-approve if confidence ≥ 0.9 (autonomous emergency rollback)

**Example Parameters:**
```json
{
  "decision_type": "rollback",
  "priority": "critical",
  "parameters": [
    {"name": "error_rate", "value": 0.08, "threshold": 0.05, "weight": 0.5},
    {"name": "health_check_failures", "value": 5, "threshold": 3, "weight": 0.3},
    {"name": "rollback_available", "value": true, "weight": 0.2}
  ]
}
```

### 4. HEALING

**Purpose:** Automatically repair degraded or failed system components

**Confidence Threshold:** 0.85

**Required Checks:**
- ✅ Failure detection confirmed
- ✅ Healing action available
- ✅ No recent healing attempts (avoid loops)
- ✅ System stability check

**Healing Actions:**
- Process restart
- Service restart
- Cache clearing
- Connection pool reset
- Memory cleanup

**Retry Configuration:**
- Max Retry Attempts: 3
- Retry Backoff: Exponential (1s, 2s, 4s)
- Cooldown Period: 5 minutes between healing attempts

**Priority-Based Auto-Approval:**
- LOW: Auto-approve if confidence ≥ 0.85
- MEDIUM: Auto-approve if confidence ≥ 0.85
- HIGH: Auto-approve if confidence ≥ 0.85
- CRITICAL: Auto-approve if confidence ≥ 0.85

**Example Parameters:**
```json
{
  "decision_type": "healing",
  "priority": "high",
  "parameters": [
    {"name": "process_health", "value": "unhealthy", "weight": 0.4},
    {"name": "healing_attempts", "value": 0, "threshold": 3, "weight": 0.3},
    {"name": "system_stability", "value": 0.88, "threshold": 0.85, "weight": 0.3}
  ]
}
```

### 5. MONITORING

**Purpose:** Adjust monitoring levels and alert configurations

**Confidence Threshold:** 0.6

**Required Checks:**
- ✅ Metrics trend analysis
- ✅ Alert threshold validation
- ✅ No alert fatigue indicators

**Monitoring Levels:**
- **NORMAL**: Standard operation, selective auto-approval
- **ELEVATED**: Increased scrutiny, restricted auto-approval
- **HIGH**: Strict oversight, minimal auto-approval
- **CRITICAL**: Maximum oversight, guardian approval required

**Priority-Based Auto-Approval:**
- LOW: Auto-approve if confidence ≥ 0.6
- MEDIUM: Auto-approve if confidence ≥ 0.6 (Normal monitoring)
- HIGH: Requires guardian review
- CRITICAL: Requires Guardian Lead approval

**Example Parameters:**
```json
{
  "decision_type": "monitoring",
  "priority": "medium",
  "parameters": [
    {"name": "alert_threshold", "value": 0.85, "weight": 0.5},
    {"name": "monitoring_level", "value": "elevated", "weight": 0.5}
  ]
}
```

### 6. GUARDIAN_OVERRIDE

**Purpose:** Manual guardian intervention to override autonomous decisions

**Confidence Threshold:** 0.95

**Required Checks:**
- ✅ Security validation
- ✅ Compliance check
- ✅ Impact assessment
- ✅ Audit trail creation

**Override Actions:**
- Approve: Accept the autonomous decision
- Reject: Deny the autonomous decision
- Modify: Alter parameters and re-evaluate

**Priority-Based Auto-Approval:**
- **NEVER auto-approved** - Always requires guardian review

**Example Parameters:**
```json
{
  "decision_type": "guardian_override",
  "priority": "critical",
  "parameters": [
    {"name": "original_decision_id", "value": "deploy_123456", "weight": 0.4},
    {"name": "override_action", "value": "reject", "weight": 0.3},
    {"name": "security_validated", "value": true, "weight": 0.3}
  ]
}
```

---

## 3. Escalation Procedures

### Escalation Matrix

| Scenario | Initial Handler | Escalation Path | Max Response Time |
|----------|----------------|-----------------|-------------------|
| LOW priority decision | Guardian Assistant | → Guardian Lead (if complex) | 2 hours |
| MEDIUM priority decision | Guardian Assistant | → Guardian Lead (if confidence < 0.8) | 30 minutes |
| HIGH priority decision | Guardian Assistant (triage) | → Guardian Lead (approval) | 15 minutes |
| CRITICAL priority decision | Guardian Lead | N/A (top level) | 15 minutes |
| Emergency incident | Guardian Assistant (immediate alert) | → Guardian Lead (simultaneous) | 5 minutes |
| Security breach | Guardian Lead (immediate) | External security team | Immediate |
| Data integrity issue | Guardian Lead | Database admin + Engineering | 10 minutes |
| Ethical violation | Guardian Lead | Ethics review board | 1 hour |

### Escalation Triggers

**Automatic Escalation:**
1. Confidence below threshold + HIGH/CRITICAL priority
2. Multiple consecutive decision failures (3+)
3. Safety metric below critical threshold
4. Security alert triggered
5. Autonomous system requests guardian intervention

**Manual Escalation:**
1. Guardian Assistant uncertainty on decision
2. Novel situation without precedent
3. Potential policy violation
4. Stakeholder request for review
5. Audit finding requiring attention

### Escalation Communication

**Urgent (CRITICAL/HIGH):**
```
@onenoly1010 🚨 URGENT: Guardian decision required

Priority: CRITICAL
Decision Type: [deployment/scaling/rollback/healing/monitoring]
Issue: [Brief description]
Confidence: [X.XX]
Auto-decision: [Would approve/reject]
Reason for escalation: [Specific reason]

Context: [Detailed context]
Recommendation: [Assistant's recommendation]

Decision Link: Issue #100 Comment [link]
```

**Standard (MEDIUM/LOW):**
```
@onenoly1010 Guardian review requested

Priority: MEDIUM
Decision Type: [type]
Confidence: [X.XX]
Reason: [Brief reason]

See Issue #100 for details.
```

---

## 4. Emergency Protocols

### Emergency Stop

**When to Execute:**
- Critical security breach detected
- Runaway autonomous process
- Data corruption in progress
- Ethical violation in progress
- Guardian Lead directive

**Procedure:**
1. Execute emergency stop command:
   ```bash
   gh workflow run "ai-agent-handoff-runbook.yml" --field action=emergency-stop
   ```
2. Post to Issue #100: "🚨 EMERGENCY STOP EXECUTED - [reason]"
3. Notify Guardian Lead immediately
4. Document incident in audit trail
5. Conduct post-incident review

**Recovery:**
1. Identify root cause
2. Implement fix
3. Test in isolated environment
4. Guardian Lead approval for restart
5. Gradual service restoration

### Emergency Rollback

**When to Execute:**
- Production deployment causing critical issues
- Error rate > 5%
- Service unavailability
- Data integrity concerns
- Performance degradation > 2x baseline

**Fast Rollback (5-10 minutes):**
```bash
# Automatic rollback to last known good
gh workflow run "ai-agent-handoff-runbook.yml" --field action=rollback
```

**Targeted Rollback (specific version):**
```bash
gh workflow run "ai-agent-handoff-runbook.yml" \
  --field action=rollback \
  --field rollback_version="deploy-20241214-120000-abc1234"
```

**Post-Rollback:**
1. Verify system stability (30 min observation)
2. Analyze failure root cause
3. Document in Issue #100
4. Create incident report
5. Update deployment procedures if needed

### Service Degradation Response

**Detection:**
- Automated health checks failing
- Response time > 2x baseline
- Error rate increasing
- User complaints

**Response Levels:**

**Level 1 - Minor Degradation:**
- Guardian Assistant monitors
- Enable verbose logging
- Increase health check frequency
- Document in Issue #100

**Level 2 - Moderate Degradation:**
- Alert Guardian Lead
- Initiate healing procedures
- Consider scaling up resources
- Prepare rollback plan

**Level 3 - Severe Degradation:**
- Immediate Guardian Lead notification
- Execute healing + scaling
- Prepare for emergency rollback
- Activate incident response

**Level 4 - Critical Failure:**
- Emergency Stop or Rollback
- Full guardian team mobilization
- External stakeholder notification
- Incident commander activation (Guardian Lead)

### Communication During Emergencies

**Internal (Guardian Team):**
- Post all updates to Issue #100
- Use @mentions for urgent notifications
- Include timestamps on all communications
- Document all actions taken

**External (Stakeholders):**
- Guardian Lead decides on external communication
- Use established communication channels
- Be transparent about impact and ETA
- Provide regular updates every 30 minutes during active incident

---

## 5. Decision Templates

### Template 1: Deployment Decision

```markdown
## 🚀 Deployment Decision

**Decision ID:** `deploy_[timestamp]`  
**Priority:** [CRITICAL/HIGH/MEDIUM/LOW]  
**Requested by:** [source]  
**Timestamp:** [ISO 8601 timestamp]

### Deployment Details
- **Component:** [fastapi/flask/gradio/all]
- **Version:** [version or commit SHA]
- **Environment:** [production/testnet]
- **Estimated Impact:** [description]

### Pre-Deployment Checks
- [ ] Health checks passing
- [ ] All tests passing (coverage: ___%)
- [ ] Security scans clean
- [ ] Performance benchmarks acceptable
- [ ] Database migrations ready (if applicable)
- [ ] Rollback plan confirmed

### Risk Assessment
- **Confidence Score:** [0.00 - 1.00]
- **Risk Level:** [LOW/MEDIUM/HIGH/CRITICAL]
- **Blast Radius:** [services/users affected]

### Parameters
| Parameter | Value | Threshold | Weight | Status |
|-----------|-------|-----------|--------|--------|
| health_check | [value] | - | 0.4 | ✅/❌ |
| test_coverage | [value] | 0.80 | 0.3 | ✅/❌ |
| security_scan | [value] | - | 0.3 | ✅/❌ |

### Decision

**Confidence Threshold Required:** 0.8  
**Calculated Confidence:** [X.XX]  
**Auto-Approval Eligible:** [YES/NO]  

#### Guardian Decision:
- [ ] ✅ **APPROVED** - Proceed with deployment
- [ ] ❌ **REJECTED** - Do not deploy
- [ ] 🔄 **MODIFIED** - Deploy with modifications

**Reasoning:**
[Detailed reasoning for the decision]

**Modifications (if applicable):**
[Any modifications to the deployment plan]

**Guardian:** [Guardian Lead/Assistant]  
**Decision Timestamp:** [timestamp]  

### Monitoring Plan
- **Duration:** [e.g., 2 hours]
- **Key Metrics:** [list metrics to watch]
- **Rollback Trigger:** [conditions that trigger rollback]

### Audit Trail
- Requested: [timestamp] by [source]
- Evaluated: [timestamp] by [guardian]
- Decided: [timestamp] - [APPROVED/REJECTED/MODIFIED]
- Result: [timestamp] - [SUCCESS/FAILED/ROLLED_BACK]
```

### Template 2: Scaling Decision

```markdown
## 📊 Scaling Decision

**Decision ID:** `scale_[timestamp]`  
**Priority:** [CRITICAL/HIGH/MEDIUM/LOW]  
**Requested by:** [source]  
**Timestamp:** [ISO 8601 timestamp]

### Scaling Details
- **Action:** [SCALE_UP/SCALE_DOWN]
- **Component:** [service name]
- **Current:** [current scale]
- **Target:** [target scale]
- **Reason:** [load/schedule/manual]

### Resource Metrics
| Metric | Current | Threshold | Status |
|--------|---------|-----------|--------|
| CPU Usage | [X]% | 75% | ✅/⚠️/❌ |
| Memory Usage | [X]% | 80% | ✅/⚠️/❌ |
| Response Time | [X]ms | [X]ms | ✅/⚠️/❌ |
| Request Queue | [X] | [X] | ✅/⚠️/❌ |

### Cost Impact
- **Current Cost:** $[X]/hour
- **Projected Cost:** $[X]/hour
- **Cost Delta:** +$[X]/hour ([X]% increase)
- **Budget Status:** [WITHIN/APPROACHING/EXCEEDS]

### Decision

**Confidence Threshold Required:** 0.7  
**Calculated Confidence:** [X.XX]  
**Auto-Approval Eligible:** [YES/NO]

#### Guardian Decision:
- [ ] ✅ **APPROVED** - Proceed with scaling
- [ ] ❌ **REJECTED** - Do not scale
- [ ] 🔄 **MODIFIED** - Scale with modifications

**Reasoning:**
[Detailed reasoning for the decision]

**Modifications (if applicable):**
[Any modifications to the scaling plan]

**Guardian:** [Guardian Lead/Assistant]  
**Decision Timestamp:** [timestamp]

### Monitoring Plan
- **Observation Period:** [duration]
- **Success Criteria:** [metrics to validate scaling success]
- **Rollback Plan:** [how to revert if needed]

### Audit Trail
- Requested: [timestamp] by [source]
- Evaluated: [timestamp] by [guardian]
- Decided: [timestamp] - [APPROVED/REJECTED/MODIFIED]
- Executed: [timestamp]
- Result: [SUCCESS/FAILED]
```

### Template 3: Rollback Decision

```markdown
## ⏮️ Rollback Decision

**Decision ID:** `rollback_[timestamp]`  
**Priority:** [CRITICAL/HIGH/MEDIUM/LOW]  
**Requested by:** [source]  
**Timestamp:** [ISO 8601 timestamp]

### Rollback Details
- **Target Deployment:** [deployment ID to rollback]
- **Deployed At:** [timestamp]
- **Rollback To:** [version/commit to restore]
- **Reason:** [error_rate/performance/security/other]

### Incident Metrics
| Metric | Current | Baseline | Status |
|--------|---------|----------|--------|
| Error Rate | [X]% | [X]% | ❌ |
| Response Time | [X]ms | [X]ms | ⚠️ |
| Health Status | [status] | healthy | ❌ |
| User Impact | [X] users | 0 | ❌ |

### Rollback Impact
- **Services Affected:** [list]
- **Data Migration:** [REQUIRED/NOT_REQUIRED]
- **Downtime Estimate:** [duration]
- **User Impact:** [description]

### Decision

**Confidence Threshold Required:** 0.9  
**Calculated Confidence:** [X.XX]  
**Auto-Approval Eligible:** [YES/NO]

#### Guardian Decision:
- [ ] ✅ **APPROVED** - Proceed with rollback
- [ ] ❌ **REJECTED** - Do not rollback
- [ ] 🔄 **MODIFIED** - Rollback with modifications

**Reasoning:**
[Detailed reasoning for the decision]

**Modifications (if applicable):**
[Any modifications to the rollback plan]

**Guardian:** [Guardian Lead/Assistant]  
**Decision Timestamp:** [timestamp]

### Post-Rollback Actions
- [ ] Verify system stability (30 min)
- [ ] Analyze root cause
- [ ] Create incident report
- [ ] Update deployment procedures
- [ ] Schedule fix deployment

### Audit Trail
- Incident Detected: [timestamp]
- Rollback Requested: [timestamp] by [source]
- Evaluated: [timestamp] by [guardian]
- Decided: [timestamp] - [APPROVED/REJECTED/MODIFIED]
- Executed: [timestamp]
- Verified: [timestamp] - [SUCCESS/FAILED]
- Root Cause: [identified/pending]
```

### Template 4: Healing Decision

```markdown
## 🏥 Healing Decision

**Decision ID:** `heal_[timestamp]`  
**Priority:** [CRITICAL/HIGH/MEDIUM/LOW]  
**Requested by:** [source]  
**Timestamp:** [ISO 8601 timestamp]

### Healing Details
- **Component:** [service/process name]
- **Issue Detected:** [description]
- **Healing Action:** [restart/reset/cleanup/other]
- **Previous Attempts:** [count]

### Diagnostics
| Check | Status | Details |
|-------|--------|---------|
| Process Health | ✅/❌ | [details] |
| Memory Usage | ✅/⚠️/❌ | [X]% |
| CPU Usage | ✅/⚠️/❌ | [X]% |
| Disk Space | ✅/⚠️/❌ | [X]% free |
| Network Connectivity | ✅/❌ | [details] |

### Healing Configuration
- **Max Retry Attempts:** 3
- **Current Attempt:** [X]
- **Cooldown Period:** 5 minutes
- **Last Attempt:** [timestamp or N/A]

### Decision

**Confidence Threshold Required:** 0.85  
**Calculated Confidence:** [X.XX]  
**Auto-Approval Eligible:** [YES/NO]

#### Guardian Decision:
- [ ] ✅ **APPROVED** - Proceed with healing
- [ ] ❌ **REJECTED** - Do not heal (escalate)
- [ ] 🔄 **MODIFIED** - Heal with modifications

**Reasoning:**
[Detailed reasoning for the decision]

**Modifications (if applicable):**
[Any modifications to the healing plan]

**Guardian:** [Guardian Lead/Assistant]  
**Decision Timestamp:** [timestamp]

### Success Criteria
- [ ] Process running
- [ ] Health checks passing
- [ ] Metrics within normal range
- [ ] No errors in logs (5 min)

### Escalation Plan
If healing fails after 3 attempts:
1. Escalate to Guardian Lead
2. Consider service restart
3. Evaluate need for rollback
4. Initiate incident response

### Audit Trail
- Issue Detected: [timestamp]
- Healing Requested: [timestamp] by [source]
- Evaluated: [timestamp] by [guardian]
- Decided: [timestamp] - [APPROVED/REJECTED/MODIFIED]
- Executed: [timestamp]
- Result: [SUCCESS/FAILED]
- Retry Count: [X]
```

### Template 5: Monitoring Decision

```markdown
## 📡 Monitoring Decision

**Decision ID:** `monitor_[timestamp]`  
**Priority:** [CRITICAL/HIGH/MEDIUM/LOW]  
**Requested by:** [source]  
**Timestamp:** [ISO 8601 timestamp]

### Monitoring Change
- **Action:** [INCREASE_LEVEL/DECREASE_LEVEL/UPDATE_THRESHOLDS]
- **Current Level:** [NORMAL/ELEVATED/HIGH/CRITICAL]
- **Target Level:** [NORMAL/ELEVATED/HIGH/CRITICAL]
- **Reason:** [description]

### Current Monitoring State
| Metric | Status | Threshold | Value |
|--------|--------|-----------|-------|
| System Health | ✅/⚠️/❌ | 0.85 | [X.XX] |
| Error Rate | ✅/⚠️/❌ | 0.05 | [X.XX] |
| Response Time | ✅/⚠️/❌ | [X]ms | [X]ms |
| Security Score | ✅/⚠️/❌ | 0.90 | [X.XX] |

### Impact of Change
- **Monitoring Frequency:** [current] → [new]
- **Auto-Approval Rules:** [changes]
- **Alert Thresholds:** [changes]
- **Guardian Oversight:** [changes]

### Decision

**Confidence Threshold Required:** 0.6  
**Calculated Confidence:** [X.XX]  
**Auto-Approval Eligible:** [YES/NO]

#### Guardian Decision:
- [ ] ✅ **APPROVED** - Proceed with monitoring change
- [ ] ❌ **REJECTED** - Do not change monitoring
- [ ] 🔄 **MODIFIED** - Change with modifications

**Reasoning:**
[Detailed reasoning for the decision]

**Modifications (if applicable):**
[Any modifications to the monitoring plan]

**Guardian:** [Guardian Lead/Assistant]  
**Decision Timestamp:** [timestamp]

### Monitoring Plan
- **Review Period:** [duration]
- **Success Criteria:** [how to measure effectiveness]
- **Reversion Plan:** [when/how to revert if needed]

### Audit Trail
- Requested: [timestamp] by [source]
- Evaluated: [timestamp] by [guardian]
- Decided: [timestamp] - [APPROVED/REJECTED/MODIFIED]
- Implemented: [timestamp]
- Review Date: [timestamp]
```

---

## 6. Monitoring Guidelines

### Daily Monitoring Tasks

**Guardian Assistant (Daily):**
1. Review autonomous decision log (Issue #100)
2. Check safety metrics dashboard
3. Verify all auto-approved decisions
4. Monitor system health trends
5. Update status in Issue #100

**Guardian Lead (Daily):**
1. Review Guardian Assistant summary
2. Approve pending HIGH priority decisions
3. Check for pattern anomalies
4. Review escalations and overrides

### Weekly Monitoring Tasks

**Guardian Team (Weekly):**
1. Review decision patterns and trends
2. Analyze auto-approval success rate
3. Review and update confidence thresholds
4. Conduct audit log review
5. Update playbook if needed

### Safety Metrics Monitoring

**Critical Metrics (Continuous):**
- **Transaction Safety:** Threshold 0.95
- **Ethical Compliance:** Threshold 0.90
- **Security Score:** Threshold 0.90
- **System Stability:** Threshold 0.85

**Alert Conditions:**
- Any metric below threshold: ELEVATED monitoring
- Any metric < (threshold - 0.10): HIGH monitoring
- Any metric < (threshold - 0.20): CRITICAL monitoring

### Monitoring Level Management

**NORMAL → ELEVATED:**
- Trigger: Single safety metric below threshold
- Action: Guardian Assistant increases monitoring frequency
- Auto-approval: Slightly restricted
- Duration: Until metric recovers + 1 hour

**ELEVATED → HIGH:**
- Trigger: Multiple metrics below threshold OR single metric critically low
- Action: Guardian Assistant escalates to Lead
- Auto-approval: Significantly restricted
- Duration: Until all metrics recover + 2 hours

**HIGH → CRITICAL:**
- Trigger: Critical incident OR Guardian Lead directive
- Action: Maximum oversight, Guardian Lead approval required
- Auto-approval: Minimal (healing only)
- Duration: Until Guardian Lead downgrades

**Downgrading Monitoring Levels:**
- Must maintain healthy metrics for minimum duration
- Guardian approval required (Lead for CRITICAL→HIGH, Assistant for others)
- Gradual reduction (CRITICAL→HIGH→ELEVATED→NORMAL)
- Document reasoning in Issue #100

### Health Check Procedures

**Automated Health Checks (Every 5 minutes):**
- Service availability (HTTP 200 responses)
- Response time < 2000ms
- Error rate < 5%
- Memory usage < 80%
- CPU usage < 75%

**Manual Health Checks (Daily):**
```bash
# Run comprehensive health check
gh workflow run "ai-agent-handoff-runbook.yml" --field action=health-check

# Check specific component
curl https://[service-url]/health
```

**Health Check Failures:**
1. First failure: Log and monitor
2. Second consecutive failure: Alert Guardian Assistant
3. Third consecutive failure: Initiate healing
4. Fourth consecutive failure: Escalate to Guardian Lead

---

## 7. Common Scenarios

### Scenario 1: High Traffic Spike

**Detection:**
- CPU usage > 75% for 5+ minutes
- Response time increasing
- Request queue growing

**Guardian Assistant Action:**
1. Evaluate scaling decision (auto-generated)
2. Check confidence score (threshold: 0.7)
3. If confidence ≥ 0.7 and priority ≤ HIGH: Approve
4. Monitor scaling execution
5. Verify metrics improve within 10 minutes

**Escalation:**
- If metrics don't improve: Scale more or escalate
- If cost exceeds budget: Escalate to Guardian Lead

### Scenario 2: Deployment Failure

**Detection:**
- Health checks failing post-deployment
- Error rate spiking
- Automated rollback triggered

**Guardian Assistant Action:**
1. Verify rollback execution
2. Confirm system restoration
3. Document failure in Issue #100
4. Review deployment logs
5. Create incident report

**Guardian Lead Action:**
1. Review incident report
2. Approve root cause analysis
3. Approve deployment procedure updates
4. Authorize retry when ready

### Scenario 3: Security Alert

**Detection:**
- Security scan fails
- Unusual access patterns detected
- Vulnerability disclosed

**Immediate Actions:**
1. Alert Guardian Lead (CRITICAL priority)
2. Increase monitoring to CRITICAL level
3. Review recent decisions and deployments
4. Prepare emergency stop if needed

**Guardian Lead Actions:**
1. Assess security impact
2. Decide: Continue (with mitigations), Rollback, or Emergency Stop
3. Coordinate with security team
4. Implement fixes
5. Conduct security review

### Scenario 4: Autonomous Decision Disagreement

**Detection:**
- Guardian Assistant disagrees with auto-decision
- Edge case outside standard rules
- Novel situation

**Guardian Assistant Action:**
1. Document concerns in Issue #100
2. Escalate to Guardian Lead with recommendation
3. Provide analysis and context
4. Suggest decision approach

**Guardian Lead Action:**
1. Review context and recommendation
2. Make final decision
3. Document reasoning
4. Update playbook if precedent-setting

### Scenario 5: System Performance Degradation

**Detection:**
- Response time gradually increasing
- Memory leaks suspected
- CPU usage creeping up

**Guardian Assistant Action:**
1. Enable verbose monitoring
2. Analyze trends over time
3. Initiate healing if clear issue identified
4. Document in Issue #100

**If Healing Fails:**
1. Escalate to Guardian Lead
2. Consider service restart
3. Evaluate need for rollback
4. Plan maintenance window if needed

### Scenario 6: Confidence Score Below Threshold

**Detection:**
- Autonomous decision confidence < required threshold
- System requests guardian review

**Guardian Assistant Action:**
1. Review decision parameters
2. Analyze why confidence is low
3. Check for missing data or unclear context
4. Make informed decision or escalate

**Decision Approach:**
- If LOW/MEDIUM priority and clear reasoning: Approve/Reject
- If HIGH priority or uncertainty: Escalate to Guardian Lead
- Always document reasoning

### Scenario 7: Multiple Concurrent Issues

**Detection:**
- Multiple alerts firing
- System instability
- Cascading failures

**Guardian Assistant Action:**
1. Immediately alert Guardian Lead
2. Prioritize issues by severity
3. Focus on stabilization first
4. Document all actions in real-time

**Guardian Lead Action:**
1. Activate incident commander role
2. Assess need for emergency stop
3. Prioritize: Security → Stability → Performance
4. Coordinate recovery actions
5. Conduct post-incident review

---

## 8. CLI Tools and Commands

### GitHub CLI Workflows

**Health Check:**
```bash
gh workflow run "ai-agent-handoff-runbook.yml" --field action=health-check
```

**Full Deployment:**
```bash
gh workflow run "ai-agent-handoff-runbook.yml" --field action=full-deployment
```

**Rollback (Latest):**
```bash
gh workflow run "ai-agent-handoff-runbook.yml" --field action=rollback
```

**Rollback (Specific Version):**
```bash
gh workflow run "ai-agent-handoff-runbook.yml" \
  --field action=rollback \
  --field rollback_version="deploy-20241214-120000-abc1234"
```

**Emergency Stop:**
```bash
gh workflow run "ai-agent-handoff-runbook.yml" --field action=emergency-stop
```

**Update Component:**
```bash
gh workflow run "ai-agent-handoff-runbook.yml" \
  --field action=update-component \
  --field target_component=fastapi
```

### Monitoring Commands

**View Recent Runs:**
```bash
gh run list --workflow=ai-agent-handoff-runbook.yml --limit 10
```

**Watch Live Run:**
```bash
gh run watch <run-id>
```

**View Logs:**
```bash
gh run view <run-id> --log
```

**View Failed Jobs:**
```bash
gh run view <run-id> --log-failed
```

**Check Issue Status:**
```bash
gh issue view 100
```

**Download Artifacts:**
```bash
gh run download <run-id>
```

### API Endpoints

**Make Autonomous Decision:**
```bash
curl -X POST http://localhost:8000/api/autonomous/decision \
  -H "Content-Type: application/json" \
  -d '{
    "decision_type": "deployment",
    "priority": "medium",
    "parameters": [
      {"name": "health_check", "value": true, "weight": 0.4}
    ]
  }'
```

**Get Decision History:**
```bash
curl "http://localhost:8000/api/autonomous/decision-history?limit=10"
```

**Get Autonomous Metrics:**
```bash
curl "http://localhost:8000/api/autonomous/metrics"
```

**Guardian Override:**
```bash
curl -X POST http://localhost:8000/api/guardian/override \
  -H "Content-Type: application/json" \
  -d '{
    "original_decision_id": "deploy_123456",
    "action": "approve",
    "reasoning": "Manual verification complete",
    "guardian_id": "onenoly1010"
  }'
```

**Update Monitoring Level:**
```bash
curl -X POST http://localhost:8000/api/guardian/update-monitoring-level \
  -H "Content-Type: application/json" \
  -d '{
    "level": "elevated",
    "reason": "Increased traffic detected"
  }'
```

**Get Monitoring Status:**
```bash
curl "http://localhost:8000/api/monitoring/status"
```

---

## 9. Audit Procedures

### Decision Audit Trail

**Every Decision Must Include:**
1. Decision ID (unique identifier)
2. Decision type and priority
3. Timestamp (ISO 8601 format)
4. Parameters and confidence score
5. Guardian who made the decision
6. Reasoning for the decision
7. Outcome (approved/rejected/modified)
8. Execution result (success/failed)

**Audit Log Location:**
- Primary: Issue #100 comments
- Secondary: System logs (`/var/log/guardian/`)
- Tertiary: Vercel metrics endpoint

### Weekly Audit Review

**Guardian Assistant (Every Monday):**
1. Compile last 7 days of decisions
2. Generate statistics report:
   - Total decisions by type
   - Auto-approval rate
   - Average confidence scores
   - Guardian override count
   - Escalations count
3. Identify trends and anomalies
4. Post summary to Issue #100

**Report Template:**
```markdown
## 📊 Weekly Guardian Audit Report

**Period:** [Start Date] to [End Date]  
**Generated:** [Timestamp]

### Decision Summary
- **Total Decisions:** [X]
  - Deployment: [X] ([X]% auto-approved)
  - Scaling: [X] ([X]% auto-approved)
  - Rollback: [X] ([X]% auto-approved)
  - Healing: [X] ([X]% auto-approved)
  - Monitoring: [X] ([X]% auto-approved)
  - Guardian Override: [X]

### Confidence Scores
- **Average Overall:** [X.XX]
- **By Type:**
  - Deployment: [X.XX]
  - Scaling: [X.XX]
  - Rollback: [X.XX]
  - Healing: [X.XX]
  - Monitoring: [X.XX]

### Guardian Activity
- **Assistant Decisions:** [X]
- **Lead Decisions:** [X]
- **Escalations:** [X]
- **Overrides:** [X]

### Incidents
- **Total Incidents:** [X]
- **Emergency Rollbacks:** [X]
- **Emergency Stops:** [X]
- **Unresolved Issues:** [X]

### Trends & Anomalies
[Description of any notable patterns or concerns]

### Recommendations
[Any suggested playbook updates or process improvements]

---
*Generated by Guardian Assistant*
```

### Monthly Audit Review

**Guardian Lead (First Monday of Month):**
1. Review all weekly reports
2. Analyze month-over-month trends
3. Evaluate playbook effectiveness
4. Update confidence thresholds if needed
5. Approve process improvements
6. Conduct compliance review

### Compliance Verification

**Quarterly (Guardian Lead):**
1. Verify all decisions have audit trails
2. Check adherence to response times
3. Review escalation procedures
4. Validate safety metric thresholds
5. Conduct security audit
6. Generate compliance report

### Incident Post-Mortems

**After Every Critical Incident:**
1. **Timeline:** Document complete sequence of events
2. **Root Cause:** Identify underlying cause
3. **Response Analysis:** Evaluate guardian response
4. **Lessons Learned:** What went well, what didn't
5. **Action Items:** Concrete improvements
6. **Playbook Updates:** Incorporate learnings

**Post-Mortem Template:**
```markdown
## Incident Post-Mortem: [Incident ID]

**Date:** [Date]  
**Duration:** [X] hours  
**Severity:** [CRITICAL/HIGH/MEDIUM/LOW]  
**Impact:** [Description]

### Timeline
- [HH:MM] - [Event]
- [HH:MM] - [Event]
- ...

### Root Cause
[Detailed analysis of underlying cause]

### What Went Well
- [Item]
- [Item]

### What Went Wrong
- [Item]
- [Item]

### Action Items
- [ ] [Action item with owner and due date]
- [ ] [Action item with owner and due date]

### Playbook Updates Required
- [ ] [Update description]
- [ ] [Update description]

**Conducted by:** [Guardian Lead]  
**Reviewed by:** [Guardian Team]  
**Date:** [Date]
```

---

## 10. Contacts and Resources

### Guardian Team

- **Guardian Lead:** @onenoly1010
  - GitHub: [@onenoly1010](https://github.com/onenoly1010)
  - Responsible for: Final decisions, critical approvals, strategic direction

- **Guardian Assistant:** @app/copilot-swe-agent
  - Responsible for: Monitoring, triage, routine decisions, documentation

### Communication Channels

- **Primary:** Issue #100 (Team HQ)
- **Assistant Assignment:** Issue #102
- **Emergency:** @mention @onenoly1010 in Issue #100

### Key Resources

**Documentation:**
- [Guardian Playbook](/docs/GUARDIAN_PLAYBOOK.md) (this document)
- [Guardian Quick Reference](/docs/GUARDIAN_QUICK_REFERENCE.md)
- [Autonomous Handover Documentation](/docs/AUTONOMOUS_HANDOVER.md)
- [AI Agent Quick Reference](/docs/AI_AGENT_QUICK_REFERENCE.md)

**Issue Templates:**
- [Guardian Decision Template](/.github/ISSUE_TEMPLATE/guardian-decision-template.md)

**System Documentation:**
- [Deployment Guide](/docs/PRODUCTION_DEPLOYMENT.md)
- [Rollback Validation](/docs/ROLLBACK_VALIDATION.md)
- [Pi Network Integration](/docs/PI_NETWORK_INTEGRATION.md)

**Operational Workflows:**
- AI Agent Handoff Runbook: `.github/workflows/ai-agent-handoff-runbook.yml`
- Deployment Workflow: `.github/workflows/deploy-testnet.yml`

### External Contacts

**For Escalation Beyond Guardian Team:**
- **Security Issues:** [Security team contact or process]
- **Infrastructure Issues:** Railway support
- **Database Issues:** Supabase support
- **Compliance Questions:** [Compliance team or process]

### Support Resources

**Monitoring Dashboards:**
- Production Dashboard: `frontend/production_dashboard.html`
- Resonance Dashboard: `frontend/resonance_dashboard.html`

**Log Locations:**
- Guardian Decisions: Issue #100
- System Logs: Railway logs via CLI
- Autonomous Decisions: `/api/autonomous/decision-history`
- Monitoring Data: `/api/monitoring/latest-data`

**Runbooks:**
- Deployment: `docs/PRODUCTION_DEPLOYMENT.md`
- Rollback: `docs/ROLLBACK_VALIDATION.md`
- AI Agent Operations: `docs/AI_AGENT_HANDOFF_RUNBOOK.md`

---

## Appendix

### Version History

- **v1.0.0** (2025-12-14): Initial Guardian Playbook creation
  - Comprehensive 9-section operational guide
  - Decision templates for all 5 decision types
  - Escalation procedures and emergency protocols
  - Monitoring guidelines and audit procedures

### Playbook Maintenance

**Update Frequency:**
- **Minor updates:** As needed (typos, clarifications)
- **Major updates:** After significant incidents or quarterly review
- **Version bump:** With any decision rule changes

**Update Process:**
1. Propose changes in Issue #100
2. Guardian Lead review and approval
3. Update document with version increment
4. Notify team of changes
5. Update training materials if needed

### Glossary

- **Auto-Approval:** Autonomous system approval without guardian intervention
- **Confidence Score:** 0.0-1.0 score indicating decision certainty
- **Confidence Threshold:** Minimum confidence required for auto-approval
- **Escalation:** Transferring decision to higher authority
- **Guardian Override:** Manual guardian intervention in autonomous decision
- **Monitoring Level:** System oversight intensity (NORMAL/ELEVATED/HIGH/CRITICAL)
- **Priority:** Decision urgency (CRITICAL/HIGH/MEDIUM/LOW)
- **Safety Metric:** Key performance indicator for system health

### Changelog

All significant changes to this playbook are documented in Issue #100 with the tag `#playbook-update`.

---

**Guardian Playbook Version:** 1.0.0  
**Last Updated:** 2025-12-14  
**Maintained by:** Guardian Team (@onenoly1010, @app/copilot-swe-agent)  
**Team HQ:** Issue #100
