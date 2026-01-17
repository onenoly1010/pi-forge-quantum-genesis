---
name: Guardian Decision
about: Template for guardian decision responses on autonomous system actions
title: '[DECISION] [TYPE] - [Brief Description]'
labels: guardian, decision, autonomous
assignees: onenoly1010
---

## Guardian Decision Response

**Decision ID:** `[auto-generated or manual ID]`  
**Original Request:** [Link to issue/PR/decision request]  
**Priority:** [CRITICAL / HIGH / MEDIUM / LOW]  
**Decision Type:** [DEPLOYMENT / SCALING / ROLLBACK / HEALING / MONITORING / GUARDIAN_OVERRIDE]  
**Requested By:** [Source/User]  
**Request Timestamp:** [ISO 8601 timestamp]

---

## Decision Summary

### Context
<!-- Brief description of what decision is being made and why -->



### Parameters
<!-- Key parameters and values that inform this decision -->

| Parameter | Value | Threshold | Weight | Status |
|-----------|-------|-----------|--------|--------|
| [param1] | [value] | [threshold] | [0.0-1.0] | ✅/⚠️/❌ |
| [param2] | [value] | [threshold] | [0.0-1.0] | ✅/⚠️/❌ |
| [param3] | [value] | [threshold] | [0.0-1.0] | ✅/⚠️/❌ |

### Risk Assessment
- **Confidence Score:** [0.00 - 1.00]
- **Risk Level:** [LOW / MEDIUM / HIGH / CRITICAL]
- **Impact:** [Brief description of potential impact]
- **Blast Radius:** [Services/users affected]

---

## Guardian Decision

**Confidence Threshold Required:** [0.X based on decision type]  
**Calculated Confidence:** [X.XX]  
**Auto-Approval Eligible:** [YES / NO]  
**Monitoring Level:** [NORMAL / ELEVATED / HIGH / CRITICAL]

### Decision

Choose one:

- [ ] ✅ **APPROVED** - Proceed with the requested action
- [ ] ❌ **REJECTED** - Do not proceed with the requested action
- [ ] 🔄 **MODIFIED** - Proceed with modifications

### Reasoning

<!-- Detailed explanation of why this decision was made -->
<!-- Include analysis of parameters, context, and any relevant considerations -->



### Modifications (if applicable)

<!-- If decision is MODIFIED, describe what changes are required -->
<!-- Delete this section if APPROVED or REJECTED -->



### Required Actions

<!-- Checklist of actions that must be taken to execute this decision -->

- [ ] [Action 1]
- [ ] [Action 2]
- [ ] [Action 3]

---

## Execution Plan

### Pre-Execution Checks
<!-- What must be verified before executing this decision -->

- [ ] All required checks passing
- [ ] No conflicting operations in progress
- [ ] Rollback plan confirmed (if applicable)
- [ ] Monitoring in place

### Execution Steps
<!-- How this decision will be executed -->

1. [Step 1]
2. [Step 2]
3. [Step 3]

### Success Criteria
<!-- How to determine if execution was successful -->

- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

### Monitoring Plan
- **Duration:** [e.g., 30 minutes, 2 hours]
- **Key Metrics:** [Metrics to watch]
- **Alert Thresholds:** [When to escalate or rollback]

---

## Audit Trail

### Timeline

| Time | Event | Actor |
|------|-------|-------|
| [timestamp] | Decision requested | [source] |
| [timestamp] | Evaluation started | [guardian] |
| [timestamp] | Decision made | [guardian] |
| [timestamp] | Execution started | [system/guardian] |
| [timestamp] | Execution completed | [system/guardian] |
| [timestamp] | Verification completed | [guardian] |

### Execution Result

<!-- To be filled after execution -->

**Status:** [SUCCESS / FAILED / PARTIALLY_SUCCESSFUL]  
**Completion Time:** [timestamp]  
**Outcome:** [Brief description of what happened]

### Metrics Impact

<!-- Key metrics before and after execution -->

| Metric | Before | After | Change | Status |
|--------|--------|-------|--------|--------|
| [metric1] | [value] | [value] | [±X%] | ✅/⚠️/❌ |
| [metric2] | [value] | [value] | [±X%] | ✅/⚠️/❌ |

---

## Escalation & Follow-up

### Escalation Status
- [ ] No escalation needed
- [ ] Escalated to Guardian Lead
- [ ] Escalated to external team: [team name]

### Follow-up Actions

<!-- Any additional actions required after execution -->

- [ ] [Follow-up action 1]
- [ ] [Follow-up action 2]

### Lessons Learned

<!-- What can be learned from this decision and its outcome -->
<!-- Any suggested improvements to processes or playbooks -->



---

## Guardian Sign-off

**Guardian:** @[username]  
**Role:** [Guardian Lead / Guardian Assistant]  
**Decision Timestamp:** [ISO 8601 timestamp]  
**Signature:** [GitHub handle or digital signature]

---

## Related Documentation

<!-- Links to related issues, PRs, documentation -->

- Team HQ: Issue #100
- Related Issue: [link if applicable]
- Related PR: [link if applicable]
- Incident Report: [link if applicable]
- Documentation: [relevant playbook sections]

---

## Notes

<!-- Any additional context, observations, or notes -->



---

**Template Version:** 1.0.0  
**Last Updated:** 2025-12-14  
**Maintained by:** Guardian Team (@onenoly1010, @app/copilot-swe-agent)
