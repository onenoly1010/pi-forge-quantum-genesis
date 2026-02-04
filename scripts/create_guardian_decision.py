#!/usr/bin/env python3
"""
Create Guardian Decision Request Issues

This script creates GitHub issues using the Guardian Decision template
for requesting human oversight on autonomous system decisions.

Usage:
    python scripts/create_guardian_decision.py \
        --decision-id deployment_1234567890 \
        --decision-type deployment \
        --priority high \
        --confidence 0.75 \
        --action "Deploy version 2.1.0 to production" \
        --reason "Confidence below threshold, requires Guardian review"
"""

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from typing import Dict, Any, Optional


class GuardianDecisionIssueCreator:
    """Helper class to create Guardian Decision issues"""
    
    DECISION_TYPES = ["Deployment", "Scaling", "Rollback", "Healing", "Monitoring", "Override"]
    PRIORITIES = ["Critical", "High", "Medium", "Low"]
    
    def __init__(self):
        self.template_path = ".github/ISSUE_TEMPLATE/guardian-decision-template.md"
    
    def create_issue_body(
        self,
        decision_id: str,
        decision_type: str,
        priority: str,
        confidence: float,
        action: str,
        reason: str,
        current_state: Optional[str] = None,
        proposed_change: Optional[str] = None,
        safety_impact: str = "Medium",
        blast_radius: Optional[str] = None,
        reversibility: str = "Yes",
        data_risk: str = "No",
        requested_by: str = "System"
    ) -> str:
        """
        Create issue body with Guardian Decision template filled in
        
        Args:
            decision_id: Unique decision identifier
            decision_type: Type of decision (Deployment, Scaling, etc.)
            priority: Priority level (Critical, High, Medium, Low)
            confidence: Confidence score (0.0 to 1.0)
            action: Description of the action being requested
            reason: Why Guardian approval is needed
            current_state: Current system state
            proposed_change: Details of proposed change
            safety_impact: Safety impact level
            blast_radius: Description of impact scope
            reversibility: Whether change is reversible
            data_risk: Whether there's data integrity risk
            requested_by: Who requested the decision
            
        Returns:
            Formatted issue body as markdown string
        """
        timestamp = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        
        # Set defaults for optional fields
        if not current_state:
            current_state = "[System state that led to this decision request]"
        if not proposed_change:
            proposed_change = f"Execute {action}"
        if not blast_radius:
            blast_radius = "Impact assessment pending"
        
        issue_body = f"""## 🛡️ Guardian Decision Request

### Decision Information

**Decision ID:** {decision_id}  
**Decision Type:** {decision_type}  
**Priority:** {priority}  
**Confidence Score:** {confidence:.2f}  
**Requested By:** {requested_by}  
**Timestamp:** {timestamp}

---

### Decision Summary

**What action is being requested?**

{action}

**Why is Guardian approval needed?**

{reason}

---

### Context & Analysis

**Current State:**

{current_state}

**Proposed Change:**

{proposed_change}

**Risk Assessment:**

- **Safety Impact:** {safety_impact}
- **Blast Radius:** {blast_radius}
- **Reversibility:** {reversibility}
- **Data Risk:** {data_risk}

**Supporting Data:**

- Relevant metrics: [To be filled in]
- Recent history: [To be filled in]
- Dependencies: [To be filled in]

---

### Decision Criteria Review

**Safety Checklist:**

- [ ] No security risks identified
- [ ] No stability concerns
- [ ] Data integrity preserved
- [ ] Rollback plan exists (if applicable)

**Impact Assessment:**

- [ ] Impact scope documented
- [ ] User impact assessed
- [ ] Financial impact calculated
- [ ] Recovery plan defined

**Approval Criteria:**

- [ ] Tests passed (if deployment)
- [ ] Metrics justify action (if scaling)
- [ ] Root cause known (if rollback/healing)
- [ ] Cost acceptable
- [ ] No active incidents

---

### Guardian Response

**Decision:** [Approve | Reject | Escalate | Need More Info]

**Guardian Comments:**

[Guardian's reasoning, additional context, or concerns]

**Conditions (if conditional approval):**

[Any specific conditions or requirements for execution]

**Follow-up Actions:**

[What should happen next, monitoring requirements, etc.]

---

### Reference Links

- [Guardian Playbook](../../docs/GUARDIAN_PLAYBOOK.md)
- [Guardian Quick Reference](../../docs/GUARDIAN_QUICK_REFERENCE.md)
- [Guardian HQ - Issue #100](https://github.com/onenoly1010/pi-forge-quantum-genesis/issues/100)

---

### Decision Timeline

**Requested:** {timestamp}  
**Responded:** [Timestamp]  
**Executed:** [Timestamp]  
**Verified:** [Timestamp]

---

### Notes

[Any additional context, lessons learned, or notes for future reference]
"""
        return issue_body
    
    def validate_inputs(
        self,
        decision_type: str,
        priority: str,
        confidence: float
    ) -> bool:
        """Validate input parameters"""
        if decision_type not in self.DECISION_TYPES:
            print(f"❌ Error: Invalid decision type '{decision_type}'")
            print(f"   Valid types: {', '.join(self.DECISION_TYPES)}")
            return False
        
        if priority not in self.PRIORITIES:
            print(f"❌ Error: Invalid priority '{priority}'")
            print(f"   Valid priorities: {', '.join(self.PRIORITIES)}")
            return False
        
        if not (0.0 <= confidence <= 1.0):
            print(f"❌ Error: Confidence must be between 0.0 and 1.0, got {confidence}")
            return False
        
        return True
    
    def print_issue_body(self, body: str):
        """Print the issue body to stdout"""
        print("\n" + "="*80)
        print("GUARDIAN DECISION REQUEST ISSUE BODY")
        print("="*80 + "\n")
        print(body)
        print("\n" + "="*80)
    
    def save_to_file(self, body: str, filename: str):
        """Save issue body to a file"""
        with open(filename, 'w') as f:
            f.write(body)
        print(f"✅ Issue body saved to: {filename}")
    
    def get_github_cli_command(
        self,
        decision_id: str,
        decision_type: str,
        body_file: str
    ) -> str:
        """Generate GitHub CLI command to create the issue"""
        title = f"[GUARDIAN] {decision_type} - {decision_id}"
        labels = "guardian-decision,needs-approval"
        assignees = "onenoly1010"
        
        cmd = f"""gh issue create \\
  --title "{title}" \\
  --body-file {body_file} \\
  --label "{labels}" \\
  --assignee {assignees}"""
        
        return cmd


def main():
    parser = argparse.ArgumentParser(
        description="Create Guardian Decision Request Issue",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create deployment decision request
  python scripts/create_guardian_decision.py \\
    --decision-id deployment_1234567890 \\
    --decision-type Deployment \\
    --priority High \\
    --confidence 0.75 \\
    --action "Deploy version 2.1.0 to production" \\
    --reason "Confidence below threshold, requires review"

  # Create scaling decision request
  python scripts/create_guardian_decision.py \\
    --decision-id scaling_1234567890 \\
    --decision-type Scaling \\
    --priority Medium \\
    --confidence 0.82 \\
    --action "Scale up web servers from 2 to 4 instances" \\
    --reason "High CPU usage sustained above 80%"

  # Save to file and get GitHub CLI command
  python scripts/create_guardian_decision.py \\
    --decision-id rollback_1234567890 \\
    --decision-type Rollback \\
    --priority Critical \\
    --confidence 0.60 \\
    --action "Rollback to version 2.0.9" \\
    --reason "Critical bug in production" \\
    --output /tmp/guardian-decision.md \\
    --show-gh-command
"""
    )
    
    # Required arguments
    parser.add_argument(
        "--decision-id",
        required=True,
        help="Unique decision identifier (e.g., deployment_1234567890)"
    )
    parser.add_argument(
        "--decision-type",
        required=True,
        choices=GuardianDecisionIssueCreator.DECISION_TYPES,
        help="Type of decision"
    )
    parser.add_argument(
        "--priority",
        required=True,
        choices=GuardianDecisionIssueCreator.PRIORITIES,
        help="Priority level"
    )
    parser.add_argument(
        "--confidence",
        required=True,
        type=float,
        help="Confidence score (0.0 to 1.0)"
    )
    parser.add_argument(
        "--action",
        required=True,
        help="Clear description of the action being requested"
    )
    parser.add_argument(
        "--reason",
        required=True,
        help="Why Guardian approval is needed"
    )
    
    # Optional arguments
    parser.add_argument(
        "--current-state",
        help="Current system state description"
    )
    parser.add_argument(
        "--proposed-change",
        help="Details of proposed change"
    )
    parser.add_argument(
        "--safety-impact",
        choices=["Low", "Medium", "High"],
        default="Medium",
        help="Safety impact level"
    )
    parser.add_argument(
        "--blast-radius",
        help="Description of potential impact scope"
    )
    parser.add_argument(
        "--reversibility",
        choices=["Yes", "No"],
        default="Yes",
        help="Whether change is easily reversible"
    )
    parser.add_argument(
        "--data-risk",
        choices=["Yes", "No"],
        default="No",
        help="Whether there's risk to data integrity"
    )
    parser.add_argument(
        "--requested-by",
        default="System",
        help="Who requested this decision (System or User)"
    )
    
    # Output options
    parser.add_argument(
        "--output",
        help="Save issue body to file instead of printing"
    )
    parser.add_argument(
        "--show-gh-command",
        action="store_true",
        help="Show GitHub CLI command to create the issue"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON instead of markdown"
    )
    
    args = parser.parse_args()
    
    # Create issue creator
    creator = GuardianDecisionIssueCreator()
    
    # Validate inputs
    if not creator.validate_inputs(args.decision_type, args.priority, args.confidence):
        sys.exit(1)
    
    # Create issue body
    issue_body = creator.create_issue_body(
        decision_id=args.decision_id,
        decision_type=args.decision_type,
        priority=args.priority,
        confidence=args.confidence,
        action=args.action,
        reason=args.reason,
        current_state=args.current_state,
        proposed_change=args.proposed_change,
        safety_impact=args.safety_impact,
        blast_radius=args.blast_radius,
        reversibility=args.reversibility,
        data_risk=args.data_risk,
        requested_by=args.requested_by
    )
    
    # Output based on options
    if args.json:
        # Output as JSON
        data = {
            "decision_id": args.decision_id,
            "decision_type": args.decision_type,
            "priority": args.priority,
            "confidence": args.confidence,
            "action": args.action,
            "reason": args.reason,
            "body": issue_body,
            "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        }
        print(json.dumps(data, indent=2))
    elif args.output:
        # Save to file
        creator.save_to_file(issue_body, args.output)
        
        if args.show_gh_command:
            print("\n" + "="*80)
            print("GITHUB CLI COMMAND")
            print("="*80 + "\n")
            print(creator.get_github_cli_command(
                args.decision_id,
                args.decision_type,
                args.output
            ))
            print("\n" + "="*80)
    else:
        # Print to stdout
        creator.print_issue_body(issue_body)
        
        if args.show_gh_command:
            # Save to temp file for GitHub CLI command
            temp_file = f"/tmp/guardian-decision-{args.decision_id}.md"
            creator.save_to_file(issue_body, temp_file)
            print("\n" + "="*80)
            print("GITHUB CLI COMMAND")
            print("="*80 + "\n")
            print(creator.get_github_cli_command(
                args.decision_id,
                args.decision_type,
                temp_file
            ))
            print("\n" + "="*80)
    
    print(f"\n✅ Guardian Decision Request created successfully!")
    print(f"   Decision ID: {args.decision_id}")
    print(f"   Type: {args.decision_type}")
    print(f"   Priority: {args.priority}")
    print(f"   Confidence: {args.confidence:.2f}")


if __name__ == "__main__":
    main()
