# 🤖 Autonomous Agent Handoff Guide

## Overview

This guide is designed for autonomous AI agents managing the Quantum Resonance Lattice deployment. It provides clear decision trees, automation patterns, and safety guardrails for emergency rollback operations.

---

## Agent Operating Principles

### Prime Directives

1. **Preserve User Data**: Never sacrifice data integrity for speed
2. **Minimize Downtime**: Fastest safe recovery is always preferred
3. **Transparent Operations**: Log all decisions and actions
4. **Human Escalation**: Know when to request human intervention
5. **Verification**: Always verify restoration after rollback

### Autonomy Levels

| Level | Description | Agent Authority |
|-------|-------------|-----------------|
| **L1** | Monitoring Only | Read logs, report issues |
| **L2** | Diagnostic | Run health checks, identify problems |
| **L3** | Automated Recovery | Execute rollback with confirmation |
| **L4** | Full Autonomy | Execute rollback without human approval |

**Current Recommended Level**: L3 (requires confirmation for production)

---

## Decision Tree: Rollback or Not?

```
Issue Detected
    │
    ├─ Is service completely down?
    │   └─ YES → IMMEDIATE ROLLBACK (Level: Fast)
    │
    ├─ Are 5xx errors > 10% of requests?
    │   └─ YES → ROLLBACK (Level: Fast)
    │
    ├─ Is authentication system broken?
    │   └─ YES → IMMEDIATE ROLLBACK (Level: Fast)
    │
    ├─ Is payment processing broken?
    │   └─ YES → ROLLBACK (Level: Fast)
    │
    ├─ Did database migration fail?
    │   └─ YES → ROLLBACK (Level: Full)
    │
    ├─ Is issue affecting <5% of users?
    │   ├─ YES → Monitor for 15 minutes
    │   │   ├─ Improving? → Continue monitoring
    │   │   └─ Worsening? → ROLLBACK (Level: Fast)
    │   └─ NO → Continue evaluation
    │
    ├─ Can hotfix be deployed in <15 minutes?
    │   ├─ YES → Attempt hotfix
    │   │   ├─ Success? → No rollback needed
    │   │   └─ Failed? → ROLLBACK (Level: Fast)
    │   └─ NO → ROLLBACK (Level: Fast)
    │
    └─ Is this a UI-only issue?
        ├─ YES → Monitor, no immediate rollback
        └─ NO → Evaluate severity
```

---

## Automated Rollback Workflow

### Phase 1: Detection (1-2 minutes)

```bash
# Agent monitoring loop
while true; do
    # Check service health
    ./rollback/scripts/verify-rollback.sh --check-only
    
    # If failures detected:
    if [ $? -ne 0 ]; then
        log_incident "Service degradation detected"
        trigger_evaluation
        break
    fi
    
    sleep 60  # Check every minute
done
```

### Phase 2: Evaluation (1-2 minutes)

```python
# Pseudo-code for agent evaluation
def evaluate_rollback_necessity():
    """
    Determine if rollback is needed and at what level.
    Returns: ("rollback_needed", "rollback_level", "confidence")
    """
    
    # Collect metrics
    metrics = {
        "service_availability": check_service_availability(),
        "error_rate": get_error_rate_last_5min(),
        "response_time": get_avg_response_time(),
        "recent_deployment": was_deployed_in_last_hour(),
        "database_issues": check_database_connectivity(),
    }
    
    # Critical issues - immediate rollback
    if metrics["service_availability"] < 50:
        return (True, "fast", 0.99)
    
    if metrics["error_rate"] > 0.10:  # >10% errors
        return (True, "fast", 0.95)
    
    if metrics["database_issues"] and metrics["recent_deployment"]:
        return (True, "full", 0.90)
    
    # Warning level - monitor or consider rollback
    if metrics["error_rate"] > 0.05:  # 5-10% errors
        return (True, "fast", 0.70)
    
    # No rollback needed
    return (False, None, 0.95)
```

### Phase 3: Backup (2-3 minutes)

```bash
# Always backup before rollback
./rollback/scripts/backup-current-state.sh

# Verify backup successful
if [ ! -f "rollback/backups/state-*/MANIFEST.txt" ]; then
    log_error "Backup failed - aborting rollback"
    escalate_to_human
    exit 1
fi
```

### Phase 4: Execution (5-10 minutes)

```bash
# Execute rollback based on determined level
case $ROLLBACK_LEVEL in
    "fast")
        ./rollback/scripts/emergency-rollback.sh --fast --auto-confirm
        ;;
    "full")
        ./rollback/scripts/emergency-rollback.sh --full --auto-confirm
        ;;
    *)
        log_error "Invalid rollback level: $ROLLBACK_LEVEL"
        exit 1
        ;;
esac

# Capture exit code
ROLLBACK_EXIT_CODE=$?
```

### Phase 5: Verification (3-5 minutes)

```bash
# Verify rollback success
./rollback/scripts/verify-rollback.sh

if [ $? -eq 0 ]; then
    log_success "Rollback verification passed"
    notify_success
else
    log_error "Rollback verification failed"
    escalate_to_human
fi
```

### Phase 6: Documentation (1-2 minutes)

```bash
# Auto-generate incident report
cat > "rollback/logs/incident-$(date +%Y%m%d-%H%M%S).md" << EOF
# Automated Rollback Incident

**Timestamp**: $(date -Iseconds)
**Trigger**: Automated monitoring
**Rollback Level**: $ROLLBACK_LEVEL
**Duration**: $DURATION_MINUTES minutes
**Status**: $([ $ROLLBACK_EXIT_CODE -eq 0 ] && echo "Success" || echo "Failed")

## Detection Metrics
- Service Availability: $SERVICE_AVAILABILITY%
- Error Rate: $ERROR_RATE%
- Response Time: ${RESPONSE_TIME}ms
- Recent Deployment: $([ $RECENT_DEPLOY -eq 1 ] && echo "Yes" || echo "No")

## Rollback Details
- Previous Commit: $PREVIOUS_COMMIT
- Target Commit: $TARGET_COMMIT
- Services Affected: FastAPI, Flask, Gradio
- Data Loss: None

## Verification Results
$(cat rollback/logs/rollback-*.log | tail -20)

## Next Actions
- [ ] Human review of incident
- [ ] Root cause analysis
- [ ] Update deployment checklist
EOF
```

---

## Agent API Reference

### Core Functions

#### `check_service_health()`
```python
def check_service_health():
    """
    Check health of all services.
    Returns: dict with service status
    """
    endpoints = {
        "fastapi": "http://localhost:8000/",
        "flask": "http://localhost:5000/health",
        "gradio": "http://localhost:7860/"
    }
    
    status = {}
    for service, url in endpoints.items():
        try:
            response = requests.get(url, timeout=5)
            status[service] = response.status_code == 200
        except:
            status[service] = False
    
    return status
```

#### `execute_rollback(level, auto_confirm=True)`
```python
def execute_rollback(level="fast", auto_confirm=True):
    """
    Execute rollback at specified level.
    
    Args:
        level: "fast", "full", or "manual"
        auto_confirm: Skip confirmation prompts
    
    Returns: (success, log_path, backup_path)
    """
    import subprocess
    
    cmd = [
        "./rollback/scripts/emergency-rollback.sh",
        f"--{level}"
    ]
    
    if auto_confirm:
        cmd.append("--auto-confirm")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    return (
        result.returncode == 0,
        find_latest_log(),
        find_latest_backup()
    )
```

#### `verify_rollback_success()`
```python
def verify_rollback_success():
    """
    Verify rollback completed successfully.
    Returns: (success, details)
    """
    import subprocess
    
    result = subprocess.run(
        ["./rollback/scripts/verify-rollback.sh"],
        capture_output=True,
        text=True
    )
    
    return (
        result.returncode == 0,
        result.stdout
    )
```

---

## Safety Guardrails

### Mandatory Checks

Before executing rollback, agent MUST verify:

```python
# Safety checklist
safety_checks = {
    "backup_created": check_backup_exists(),
    "target_commit_valid": verify_commit_exists(target_commit),
    "no_data_loss_risk": verify_no_pending_transactions(),
    "rollback_script_exists": os.path.exists("rollback/scripts/emergency-rollback.sh"),
    "sufficient_disk_space": get_disk_space() > 1_000_000_000,  # 1GB
}

if not all(safety_checks.values()):
    escalate_to_human("Safety checks failed", safety_checks)
    abort_rollback()
```

### Rate Limiting

Prevent rollback loops:

```python
# Check recent rollback history
def can_execute_rollback():
    """
    Prevent too-frequent rollbacks.
    Returns: (allowed, reason)
    """
    recent_rollbacks = count_rollbacks_last_24h()
    
    if recent_rollbacks >= 3:
        return (False, "Too many rollbacks in 24h - human review required")
    
    last_rollback_time = get_last_rollback_time()
    if last_rollback_time and (time.time() - last_rollback_time) < 300:
        return (False, "Last rollback was <5 min ago - waiting")
    
    return (True, "OK")
```

### Human Escalation Triggers

Agent MUST escalate to human when:

1. **Rollback fails** after execution
2. **Verification fails** after rollback
3. **Multiple rollbacks** in short period (>3 in 24h)
4. **Database issues detected** (requires full rollback)
5. **Safety checks fail**
6. **Unknown error patterns** encountered

```python
def escalate_to_human(reason, context=None):
    """
    Alert humans that intervention is needed.
    """
    message = f"""
    🚨 HUMAN INTERVENTION REQUIRED
    
    Reason: {reason}
    Timestamp: {datetime.now().isoformat()}
    Current Status: {get_system_status()}
    
    Context:
    {json.dumps(context, indent=2)}
    
    Actions Taken:
    - Rollback halted
    - Current state backed up
    - Logs captured
    
    Next Steps:
    1. Review logs: {get_latest_log_path()}
    2. Check system status: ./rollback/scripts/verify-rollback.sh
    3. Decide: Manual intervention or retry rollback
    """
    
    # Send notification (implementation depends on system)
    send_alert(message)
    log_escalation(reason, context)
    
    # Wait for human response
    wait_for_human_input()
```

---

## Monitoring Integration

### Continuous Health Monitoring

```python
# Agent monitoring loop
class RollbackAgent:
    def __init__(self):
        self.monitoring = True
        self.check_interval = 60  # seconds
        self.escalation_threshold = 3  # consecutive failures
        self.consecutive_failures = 0
    
    def monitor_loop(self):
        while self.monitoring:
            health = check_service_health()
            
            if not health["overall_healthy"]:
                self.consecutive_failures += 1
                log_warning(f"Health check failed ({self.consecutive_failures}/{self.escalation_threshold})")
                
                if self.consecutive_failures >= self.escalation_threshold:
                    self.initiate_rollback_evaluation()
            else:
                self.consecutive_failures = 0
            
            time.sleep(self.check_interval)
    
    def initiate_rollback_evaluation(self):
        """Evaluate if rollback is needed"""
        should_rollback, level, confidence = evaluate_rollback_necessity()
        
        if should_rollback and confidence > 0.90:
            log_info(f"Initiating {level} rollback (confidence: {confidence})")
            self.execute_rollback(level)
        elif should_rollback and confidence > 0.70:
            log_warning(f"Rollback recommended but confidence low ({confidence})")
            escalate_to_human("Low confidence rollback decision", {
                "level": level,
                "confidence": confidence
            })
        else:
            log_info("No rollback needed")
```

---

## Logging Standards

### Log Levels

```python
# Use consistent log levels
LOG_LEVELS = {
    "DEBUG": "Detailed debugging information",
    "INFO": "Normal operational messages",
    "WARNING": "Warning - requires attention but not critical",
    "ERROR": "Error - operation failed",
    "CRITICAL": "Critical - immediate action required"
}
```

### Log Format

```python
# Standard log entry format
def log_entry(level, message, context=None):
    """
    Create standardized log entry.
    """
    entry = {
        "timestamp": datetime.now().isoformat(),
        "level": level,
        "agent": "rollback_agent",
        "message": message,
        "context": context or {}
    }
    
    # Write to log file
    with open("rollback/logs/agent.log", "a") as f:
        f.write(json.dumps(entry) + "\n")
    
    # Also write to console
    print(f"[{entry['timestamp']}] [{level}] {message}")
```

---

## Testing Rollback Automation

### Dry Run Mode

Always test in dry-run mode first:

```bash
# Test rollback automation without making changes
./rollback/scripts/emergency-rollback.sh --fast --dry-run

# Verify script behavior
# Check logs
cat rollback/logs/rollback-*.log
```

### Simulation Environment

Create test scenarios:

```python
# Simulate service failure
def simulate_service_failure(service="fastapi"):
    """
    Simulate service failure for testing.
    """
    # Kill service process
    subprocess.run(["pkill", "-f", service])
    
    # Wait for agent to detect
    time.sleep(120)  # 2 minutes
    
    # Verify agent initiated rollback
    assert rollback_was_initiated()
    
    # Verify service restored
    assert service_is_healthy(service)
```

---

## Continuous Improvement

### Agent Learning

After each rollback:

1. **Analyze Decision Accuracy**
   - Was rollback necessary?
   - Was correct level chosen?
   - Could hotfix have worked?

2. **Update Thresholds**
   - Adjust error rate thresholds
   - Tune response time limits
   - Refine confidence scores

3. **Document Patterns**
   - Record common failure modes
   - Update decision tree
   - Improve detection logic

---

## Example: Complete Autonomous Rollback

```python
#!/usr/bin/env python3
"""
Complete autonomous rollback agent example.
"""
import subprocess
import time
import json
from datetime import datetime

class AutonomousRollbackAgent:
    def __init__(self):
        self.config = self.load_config()
        self.monitoring = True
    
    def load_config(self):
        with open("rollback/config/rollback-config.json") as f:
            return json.load(f)
    
    def run(self):
        """Main agent loop"""
        print("🤖 Autonomous Rollback Agent starting...")
        
        while self.monitoring:
            try:
                # Check system health
                health = self.check_health()
                
                if not health["healthy"]:
                    self.handle_unhealthy_state(health)
                
                # Sleep until next check
                time.sleep(self.config["monitoring"]["check_interval_seconds"])
                
            except KeyboardInterrupt:
                print("\n🛑 Agent shutting down...")
                break
            except Exception as e:
                print(f"❌ Agent error: {e}")
                time.sleep(60)
    
    def check_health(self):
        """Check system health"""
        result = subprocess.run(
            ["./rollback/scripts/verify-rollback.sh", "--check-only"],
            capture_output=True
        )
        
        return {
            "healthy": result.returncode == 0,
            "details": result.stdout.decode()
        }
    
    def handle_unhealthy_state(self, health):
        """Handle unhealthy system state"""
        print(f"⚠️  Unhealthy state detected")
        
        # Evaluate rollback necessity
        should_rollback, level = self.evaluate_rollback()
        
        if should_rollback:
            print(f"🔄 Initiating {level} rollback...")
            success = self.execute_rollback(level)
            
            if success:
                print("✅ Rollback completed successfully")
            else:
                print("❌ Rollback failed - escalating to human")
                self.escalate_to_human("Rollback execution failed")
    
    def evaluate_rollback(self):
        """Evaluate if rollback is needed"""
        # Simple evaluation logic
        # In production, use more sophisticated analysis
        return (True, "fast")
    
    def execute_rollback(self, level):
        """Execute rollback"""
        result = subprocess.run([
            "./rollback/scripts/emergency-rollback.sh",
            f"--{level}",
            "--auto-confirm"
        ])
        
        return result.returncode == 0
    
    def escalate_to_human(self, reason):
        """Escalate to human operator"""
        message = f"""
        🚨 ESCALATION REQUIRED
        Reason: {reason}
        Time: {datetime.now().isoformat()}
        """
        print(message)
        # In production: send alert via webhook, email, etc.

if __name__ == "__main__":
    agent = AutonomousRollbackAgent()
    agent.run()
```

---

## Security Considerations

### Credentials Management

```python
# Never log sensitive data
def safe_log(message, context=None):
    """Log with sensitive data redaction"""
    if context:
        # Redact sensitive keys
        sensitive_keys = ["password", "token", "key", "secret"]
        safe_context = {
            k: "***REDACTED***" if any(s in k.lower() for s in sensitive_keys) else v
            for k, v in context.items()
        }
    else:
        safe_context = {}
    
    log_entry("INFO", message, safe_context)
```

### Audit Trail

```python
# Maintain complete audit trail
def log_rollback_decision(decision, reasoning):
    """Log rollback decision for audit"""
    audit_entry = {
        "timestamp": datetime.now().isoformat(),
        "decision": decision,
        "reasoning": reasoning,
        "agent_version": "1.0.0",
        "metrics_used": get_current_metrics()
    }
    
    with open("rollback/logs/audit-trail.jsonl", "a") as f:
        f.write(json.dumps(audit_entry) + "\n")
```

---

© 2025 Pi Forge Collective — Quantum Genesis Initiative
