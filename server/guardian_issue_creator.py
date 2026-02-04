"""
Guardian Issue Creator Module

Automatically creates Guardian Decision Request issues for autonomous decisions
that require human oversight.
"""

import logging
import os
import subprocess
import tempfile
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)


class GuardianIssueCreator:
    """
    Creates GitHub issues for Guardian Decision Requests
    
    This class integrates with the autonomous decision system to automatically
    create properly formatted Guardian Decision Request issues when a decision
    requires human oversight.
    """
    
    def __init__(self, repo_owner: str = "onenoly1010", repo_name: str = "pi-forge-quantum-genesis"):
        """
        Initialize Guardian Issue Creator
        
        Args:
            repo_owner: GitHub repository owner
            repo_name: GitHub repository name
        """
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.repo_full_name = f"{repo_owner}/{repo_name}"
        logger.info(f"✅ Guardian Issue Creator initialized for repo: {self.repo_full_name}")
    
    def create_guardian_issue_from_decision(
        self,
        decision_data: Dict[str, Any],
        auto_create: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Create a Guardian Decision Request issue from decision data
        
        Args:
            decision_data: Decision data dictionary containing:
                - decision_id: Unique decision identifier
                - decision_type: Type of decision (deployment, scaling, etc.)
                - priority: Priority level (critical, high, medium, low)
                - confidence: Confidence score (0.0 to 1.0)
                - reasoning: Why the decision was made
                - metadata: Additional context
            auto_create: If True, automatically create the GitHub issue
            
        Returns:
            Dictionary with issue details if created, None otherwise
        """
        decision_id = decision_data.get("decision_id", "unknown")
        decision_type = decision_data.get("decision_type", "monitoring").title()
        priority = decision_data.get("metadata", {}).get("priority", "medium").title()
        confidence = decision_data.get("confidence", 0.0)
        reasoning = decision_data.get("reasoning", "Autonomous decision requires Guardian review")
        
        logger.info(
            f"🛡️ Creating Guardian issue for decision: {decision_id} "
            f"(type={decision_type}, priority={priority}, confidence={confidence:.2f})"
        )
        
        # Generate issue body
        issue_body = self._generate_issue_body(
            decision_id=decision_id,
            decision_type=decision_type,
            priority=priority,
            confidence=confidence,
            decision_data=decision_data
        )
        
        # Generate issue title
        issue_title = f"[GUARDIAN] {decision_type} - {decision_id}"
        
        result = {
            "decision_id": decision_id,
            "issue_title": issue_title,
            "issue_body": issue_body,
            "labels": ["guardian-decision", "needs-approval"],
            "assignees": [self.repo_owner],
            "created": False,
            "issue_number": None,
            "issue_url": None
        }
        
        if auto_create:
            # Try to create the issue using GitHub CLI
            try:
                issue_info = self._create_github_issue(
                    title=issue_title,
                    body=issue_body,
                    labels=["guardian-decision", "needs-approval"],
                    assignees=[self.repo_owner]
                )
                result.update(issue_info)
                result["created"] = True
                logger.info(f"✅ Guardian issue created: {result['issue_url']}")
            except Exception as e:
                logger.error(f"❌ Failed to create Guardian issue: {e}")
                logger.info("💡 Issue body generated but not created. Use manual creation.")
        else:
            logger.info("📝 Guardian issue body generated (auto_create=False)")
        
        return result
    
    def _generate_issue_body(
        self,
        decision_id: str,
        decision_type: str,
        priority: str,
        confidence: float,
        decision_data: Dict[str, Any]
    ) -> str:
        """Generate formatted issue body for Guardian Decision Request"""
        timestamp = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        
        # Extract data from decision
        metadata = decision_data.get("metadata", {})
        reasoning = decision_data.get("reasoning", "Autonomous decision reasoning")
        actions = decision_data.get("actions", [])
        
        # Determine action description
        if actions:
            action_description = "\n".join(f"- {action}" for action in actions)
        else:
            action_description = f"Execute autonomous {decision_type.lower()} decision"
        
        # Determine why Guardian approval is needed
        if confidence < 0.6:
            guardian_reason = f"Low confidence score ({confidence:.2f}) requires Guardian review"
        elif confidence < 0.8:
            guardian_reason = f"Moderate confidence score ({confidence:.2f}) requires Guardian approval"
        elif priority.lower() in ["critical", "high"]:
            guardian_reason = f"High-priority {decision_type.lower()} requires Guardian oversight"
        else:
            guardian_reason = "Decision flagged for Guardian review based on safety criteria"
        
        # Extract or set default values
        current_state = metadata.get("current_state", "System operating normally")
        proposed_change = metadata.get("proposed_change", f"Apply {decision_type.lower()} action")
        safety_impact = metadata.get("safety_impact", "Medium")
        blast_radius = metadata.get("blast_radius", f"{decision_type} impact limited to affected services")
        reversibility = "Yes" if metadata.get("reversible", True) else "No"
        data_risk = "Yes" if metadata.get("data_risk", False) else "No"
        requested_by = decision_data.get("source", "System")
        
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

{action_description}

**Why is Guardian approval needed?**

{guardian_reason}

**Autonomous Reasoning:**

{reasoning}

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

- Decision confidence: {confidence:.2%}
- Decision type: {decision_type}
- Priority level: {priority}
- Timestamp: {timestamp}

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
- [Guardian HQ - Issue #100](https://github.com/{self.repo_full_name}/issues/100)

---

### Decision Timeline

**Requested:** {timestamp}  
**Responded:** [Timestamp]  
**Executed:** [Timestamp]  
**Verified:** [Timestamp]

---

### Decision Data

<details>
<summary>Full Decision Data (JSON)</summary>

```json
{self._format_decision_data_json(decision_data)}
```

</details>

---

### Notes

[Any additional context, lessons learned, or notes for future reference]
"""
        return issue_body
    
    def _format_decision_data_json(self, decision_data: Dict[str, Any]) -> str:
        """Format decision data as pretty-printed JSON"""
        import json
        try:
            return json.dumps(decision_data, indent=2, default=str)
        except Exception as e:
            logger.warning(f"Failed to format decision data as JSON: {e}")
            return str(decision_data)
    
    def _create_github_issue(
        self,
        title: str,
        body: str,
        labels: list,
        assignees: list
    ) -> Dict[str, Any]:
        """
        Create GitHub issue using GitHub CLI
        
        Args:
            title: Issue title
            body: Issue body
            labels: List of labels
            assignees: List of assignees
            
        Returns:
            Dictionary with issue information
            
        Raises:
            RuntimeError: If issue creation fails
        """
        # Check if GitHub CLI is available
        try:
            subprocess.run(["gh", "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError(
                "GitHub CLI (gh) not found. Install from https://cli.github.com/ "
                "or set auto_create=False and create issues manually."
            )
        
        # Create temporary file for issue body
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(body)
            body_file = f.name
        
        try:
            # Build GitHub CLI command
            cmd = [
                "gh", "issue", "create",
                "--repo", self.repo_full_name,
                "--title", title,
                "--body-file", body_file,
                "--label", ",".join(labels),
                "--assignee", ",".join(assignees)
            ]
            
            # Execute command
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True
            )
            
            # Parse issue URL from output
            issue_url = result.stdout.strip()
            issue_number = issue_url.split('/')[-1] if issue_url else None
            
            return {
                "issue_number": issue_number,
                "issue_url": issue_url
            }
        
        finally:
            # Clean up temp file
            try:
                os.unlink(body_file)
            except Exception:
                pass
    
    def save_issue_body_to_file(
        self,
        decision_id: str,
        issue_body: str,
        output_dir: str = "/tmp"
    ) -> str:
        """
        Save issue body to a file
        
        Args:
            decision_id: Decision ID for filename
            issue_body: Issue body content
            output_dir: Directory to save file
            
        Returns:
            Path to saved file
        """
        output_path = Path(output_dir) / f"guardian-decision-{decision_id}.md"
        output_path.write_text(issue_body)
        logger.info(f"💾 Saved Guardian issue body to: {output_path}")
        return str(output_path)


# Global instance
_issue_creator: Optional[GuardianIssueCreator] = None


def get_guardian_issue_creator() -> GuardianIssueCreator:
    """Get or create global Guardian Issue Creator instance"""
    global _issue_creator
    if _issue_creator is None:
        _issue_creator = GuardianIssueCreator()
    return _issue_creator


def create_guardian_issue_for_decision(
    decision_data: Dict[str, Any],
    auto_create: bool = False
) -> Optional[Dict[str, Any]]:
    """
    Convenience function to create Guardian issue from decision data
    
    Args:
        decision_data: Decision data dictionary
        auto_create: If True, automatically create GitHub issue
        
    Returns:
        Dictionary with issue details if created, None otherwise
    """
    creator = get_guardian_issue_creator()
    return creator.create_guardian_issue_from_decision(decision_data, auto_create)
