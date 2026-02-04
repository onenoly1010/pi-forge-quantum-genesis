"""
Tests for Guardian Issue Creator

Tests the functionality of creating Guardian Decision Request issues
from autonomous decision data.
"""

import pytest
import json
from server.guardian_issue_creator import (
    GuardianIssueCreator,
    create_guardian_issue_for_decision,
    get_guardian_issue_creator
)


class TestGuardianIssueCreator:
    """Test suite for GuardianIssueCreator class"""
    
    def test_initialization(self):
        """Test GuardianIssueCreator initialization"""
        creator = GuardianIssueCreator()
        assert creator.repo_owner == "onenoly1010"
        assert creator.repo_name == "pi-forge-quantum-genesis"
        assert creator.repo_full_name == "onenoly1010/pi-forge-quantum-genesis"
    
    def test_initialization_custom_repo(self):
        """Test GuardianIssueCreator with custom repository"""
        creator = GuardianIssueCreator(repo_owner="testuser", repo_name="testrepo")
        assert creator.repo_owner == "testuser"
        assert creator.repo_name == "testrepo"
        assert creator.repo_full_name == "testuser/testrepo"
    
    def test_generate_issue_body_deployment(self):
        """Test issue body generation for deployment decision"""
        creator = GuardianIssueCreator()
        
        decision_data = {
            "decision_id": "deployment_1234567890",
            "decision_type": "deployment",
            "confidence": 0.75,
            "reasoning": "All tests passed, ready for deployment",
            "actions": ["Deploy version 2.1.0", "Run smoke tests"],
            "metadata": {
                "priority": "high",
                "current_state": "Version 2.0.9 running",
                "proposed_change": "Deploy version 2.1.0",
                "safety_impact": "Low",
                "reversible": True,
                "data_risk": False
            },
            "source": "autonomous_agent"
        }
        
        issue_body = creator._generate_issue_body(
            decision_id="deployment_1234567890",
            decision_type="Deployment",
            priority="High",
            confidence=0.75,
            decision_data=decision_data
        )
        
        # Verify key elements are present
        assert "deployment_1234567890" in issue_body
        assert "Deployment" in issue_body
        assert "High" in issue_body
        assert "0.75" in issue_body
        assert "All tests passed" in issue_body
        assert "Deploy version 2.1.0" in issue_body
        assert "Guardian Decision Request" in issue_body
    
    def test_generate_issue_body_rollback(self):
        """Test issue body generation for rollback decision"""
        creator = GuardianIssueCreator()
        
        decision_data = {
            "decision_id": "rollback_9876543210",
            "decision_type": "rollback",
            "confidence": 0.60,
            "reasoning": "Critical bug detected in production",
            "actions": ["Rollback to version 2.0.9"],
            "metadata": {
                "priority": "critical",
                "current_state": "Version 2.1.0 with critical bug",
                "proposed_change": "Revert to version 2.0.9",
                "safety_impact": "High",
                "reversible": True,
                "data_risk": False
            },
            "source": "autonomous_agent"
        }
        
        issue_body = creator._generate_issue_body(
            decision_id="rollback_9876543210",
            decision_type="Rollback",
            priority="Critical",
            confidence=0.60,
            decision_data=decision_data
        )
        
        # Verify key elements
        assert "rollback_9876543210" in issue_body
        assert "Rollback" in issue_body
        assert "Critical" in issue_body
        assert "0.60" in issue_body
        assert "Critical bug" in issue_body
    
    def test_generate_issue_body_scaling(self):
        """Test issue body generation for scaling decision"""
        creator = GuardianIssueCreator()
        
        decision_data = {
            "decision_id": "scaling_5555555555",
            "decision_type": "scaling",
            "confidence": 0.85,
            "reasoning": "High CPU usage detected",
            "actions": ["Scale up to 6 instances"],
            "metadata": {
                "priority": "medium",
                "current_state": "3 instances at 85% CPU",
                "proposed_change": "Add 3 instances",
                "safety_impact": "Low",
                "reversible": True,
                "data_risk": False
            },
            "source": "autonomous_agent"
        }
        
        issue_body = creator._generate_issue_body(
            decision_id="scaling_5555555555",
            decision_type="Scaling",
            priority="Medium",
            confidence=0.85,
            decision_data=decision_data
        )
        
        # Verify key elements
        assert "scaling_5555555555" in issue_body
        assert "Scaling" in issue_body
        assert "Medium" in issue_body
        assert "0.85" in issue_body
    
    def test_create_guardian_issue_no_auto_create(self):
        """Test creating Guardian issue without auto-creation"""
        creator = GuardianIssueCreator()
        
        decision_data = {
            "decision_id": "test_1111111111",
            "decision_type": "deployment",
            "confidence": 0.70,
            "reasoning": "Test deployment",
            "actions": ["Test action"],
            "metadata": {"priority": "low"},
            "source": "test"
        }
        
        result = creator.create_guardian_issue_from_decision(
            decision_data,
            auto_create=False
        )
        
        # Verify result structure
        assert result is not None
        assert result["decision_id"] == "test_1111111111"
        assert result["issue_title"] == "[GUARDIAN] Deployment - test_1111111111"
        assert result["issue_body"] is not None
        assert "test_1111111111" in result["issue_body"]
        assert result["labels"] == ["guardian-decision", "needs-approval"]
        assert result["assignees"] == ["onenoly1010"]
        assert result["created"] is False
        assert result["issue_number"] is None
        assert result["issue_url"] is None
    
    def test_format_decision_data_json(self):
        """Test JSON formatting of decision data"""
        creator = GuardianIssueCreator()
        
        decision_data = {
            "decision_id": "test_123",
            "confidence": 0.8,
            "metadata": {
                "key1": "value1",
                "key2": 42
            }
        }
        
        json_str = creator._format_decision_data_json(decision_data)
        
        # Verify it's valid JSON
        parsed = json.loads(json_str)
        assert parsed["decision_id"] == "test_123"
        assert parsed["confidence"] == 0.8
        assert parsed["metadata"]["key1"] == "value1"
        assert parsed["metadata"]["key2"] == 42
    
    def test_save_issue_body_to_file(self, tmp_path):
        """Test saving issue body to file"""
        creator = GuardianIssueCreator()
        
        decision_id = "test_save_123"
        issue_body = "Test issue body content"
        
        file_path = creator.save_issue_body_to_file(
            decision_id,
            issue_body,
            output_dir=str(tmp_path)
        )
        
        # Verify file was created
        assert file_path is not None
        with open(file_path, 'r') as f:
            content = f.read()
        
        assert content == issue_body
        assert f"guardian-decision-{decision_id}.md" in file_path
    
    def test_issue_body_contains_required_sections(self):
        """Test that issue body contains all required sections"""
        creator = GuardianIssueCreator()
        
        decision_data = {
            "decision_id": "complete_test",
            "decision_type": "deployment",
            "confidence": 0.75,
            "reasoning": "Complete test",
            "actions": ["Action 1"],
            "metadata": {"priority": "high"},
            "source": "test"
        }
        
        issue_body = creator._generate_issue_body(
            "complete_test",
            "Deployment",
            "High",
            0.75,
            decision_data
        )
        
        # Check for required sections
        required_sections = [
            "Guardian Decision Request",
            "Decision Information",
            "Decision Summary",
            "Context & Analysis",
            "Risk Assessment",
            "Decision Criteria Review",
            "Guardian Response",
            "Reference Links",
            "Decision Timeline"
        ]
        
        for section in required_sections:
            assert section in issue_body, f"Missing section: {section}"
    
    def test_confidence_score_reasoning(self):
        """Test that confidence scores generate appropriate reasoning"""
        creator = GuardianIssueCreator()
        
        # Test low confidence
        decision_data_low = {
            "decision_id": "low_conf",
            "decision_type": "deployment",
            "confidence": 0.55,
            "reasoning": "Test",
            "actions": [],
            "metadata": {"priority": "medium"},
            "source": "test"
        }
        
        body_low = creator._generate_issue_body(
            "low_conf", "Deployment", "Medium", 0.55, decision_data_low
        )
        assert "Low confidence" in body_low or "0.55" in body_low
        
        # Test moderate confidence
        decision_data_mod = {
            "decision_id": "mod_conf",
            "decision_type": "deployment",
            "confidence": 0.70,
            "reasoning": "Test",
            "actions": [],
            "metadata": {"priority": "medium"},
            "source": "test"
        }
        
        body_mod = creator._generate_issue_body(
            "mod_conf", "Deployment", "Medium", 0.70, decision_data_mod
        )
        assert "Moderate confidence" in body_mod or "0.70" in body_mod


class TestConvenienceFunctions:
    """Test convenience functions"""
    
    def test_get_guardian_issue_creator(self):
        """Test getting global instance"""
        creator1 = get_guardian_issue_creator()
        creator2 = get_guardian_issue_creator()
        
        # Should return same instance
        assert creator1 is creator2
    
    def test_create_guardian_issue_for_decision(self):
        """Test convenience function"""
        decision_data = {
            "decision_id": "conv_test",
            "decision_type": "deployment",
            "confidence": 0.75,
            "reasoning": "Convenience test",
            "actions": ["Test action"],
            "metadata": {"priority": "low"},
            "source": "test"
        }
        
        result = create_guardian_issue_for_decision(
            decision_data,
            auto_create=False
        )
        
        assert result is not None
        assert result["decision_id"] == "conv_test"
        assert result["created"] is False


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_missing_metadata(self):
        """Test handling of missing metadata"""
        creator = GuardianIssueCreator()
        
        decision_data = {
            "decision_id": "no_meta",
            "decision_type": "deployment",
            "confidence": 0.75,
            "reasoning": "No metadata",
            "actions": []
            # No metadata field
        }
        
        result = creator.create_guardian_issue_from_decision(
            decision_data,
            auto_create=False
        )
        
        # Should handle gracefully with defaults
        assert result is not None
        assert "no_meta" in result["issue_body"]
    
    def test_missing_actions(self):
        """Test handling of missing actions"""
        creator = GuardianIssueCreator()
        
        decision_data = {
            "decision_id": "no_actions",
            "decision_type": "deployment",
            "confidence": 0.75,
            "reasoning": "No actions",
            "metadata": {"priority": "low"}
            # No actions field
        }
        
        result = creator.create_guardian_issue_from_decision(
            decision_data,
            auto_create=False
        )
        
        # Should handle gracefully
        assert result is not None
        assert "autonomous deployment decision" in result["issue_body"].lower()
    
    def test_format_invalid_json_data(self):
        """Test handling of non-serializable data"""
        creator = GuardianIssueCreator()
        
        # Object that can't be JSON serialized
        class NonSerializable:
            pass
        
        decision_data = {
            "decision_id": "invalid_json",
            "obj": NonSerializable()
        }
        
        # Should handle gracefully and convert to string
        json_str = creator._format_decision_data_json(decision_data)
        assert json_str is not None
        assert "invalid_json" in json_str


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
