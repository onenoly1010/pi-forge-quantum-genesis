"""
Test suite for Guardian Coordinator flows.
Tests multisig quorum logic and API endpoints.
"""

import pytest
from datetime import datetime
from fastapi.testclient import TestClient

# Import models
from src.models.approval import Vote, VoteChoice, ProposalCreate, ProposalAction
from src.models.guardian import GuardianCreate

# Import utilities
from src.utils.multisig import (
    verify_quorum,
    calculate_approval_percentage,
    check_duplicate_vote,
    get_quorum_status,
    validate_vote_eligibility
)

# Import API
from src.api.main import app

client = TestClient(app)


# =============================================================================
# MULTISIG UTILITY TESTS
# =============================================================================

class TestMultisigVerifyQuorum:
    """Test quorum verification logic."""
    
    def test_verify_quorum_met(self):
        """Test when quorum is met."""
        votes = [
            Vote(guardian_id="g1", vote=VoteChoice.APPROVE),
            Vote(guardian_id="g2", vote=VoteChoice.APPROVE),
            Vote(guardian_id="g3", vote=VoteChoice.APPROVE),
        ]
        
        approve_count, required, met = verify_quorum(votes, required_quorum=3)
        
        assert approve_count == 3
        assert required == 3
        assert met is True
    
    def test_verify_quorum_not_met(self):
        """Test when quorum is not met."""
        votes = [
            Vote(guardian_id="g1", vote=VoteChoice.APPROVE),
            Vote(guardian_id="g2", vote=VoteChoice.REJECT),
        ]
        
        approve_count, required, met = verify_quorum(votes, required_quorum=3)
        
        assert approve_count == 1
        assert required == 3
        assert met is False
    
    def test_verify_quorum_with_abstentions(self):
        """Test quorum with abstentions."""
        votes = [
            Vote(guardian_id="g1", vote=VoteChoice.APPROVE),
            Vote(guardian_id="g2", vote=VoteChoice.APPROVE),
            Vote(guardian_id="g3", vote=VoteChoice.ABSTAIN),
        ]
        
        approve_count, required, met = verify_quorum(votes, required_quorum=2)
        
        assert approve_count == 2
        assert met is True
    
    def test_verify_quorum_empty_votes(self):
        """Test quorum with no votes."""
        votes = []
        
        approve_count, required, met = verify_quorum(votes, required_quorum=3)
        
        assert approve_count == 0
        assert met is False
    
    def test_verify_quorum_invalid_requirement(self):
        """Test with invalid quorum requirement."""
        votes = [Vote(guardian_id="g1", vote=VoteChoice.APPROVE)]
        
        with pytest.raises(ValueError, match="must be at least 1"):
            verify_quorum(votes, required_quorum=0)
    
    def test_verify_quorum_dict_format(self):
        """Test quorum verification with dict votes."""
        votes = [
            {'guardian_id': 'g1', 'vote': 'approve'},
            {'guardian_id': 'g2', 'vote': 'approve'},
        ]
        
        approve_count, required, met = verify_quorum(votes, required_quorum=2)
        
        assert approve_count == 2
        assert met is True


class TestApprovalPercentage:
    """Test approval percentage calculation."""
    
    def test_100_percent_approval(self):
        """Test 100% approval."""
        votes = [
            Vote(guardian_id="g1", vote=VoteChoice.APPROVE),
            Vote(guardian_id="g2", vote=VoteChoice.APPROVE),
        ]
        
        percentage = calculate_approval_percentage(votes)
        assert percentage == 100.0
    
    def test_50_percent_approval(self):
        """Test 50% approval."""
        votes = [
            Vote(guardian_id="g1", vote=VoteChoice.APPROVE),
            Vote(guardian_id="g2", vote=VoteChoice.REJECT),
        ]
        
        percentage = calculate_approval_percentage(votes)
        assert percentage == 50.0
    
    def test_approval_with_abstentions(self):
        """Test approval percentage excludes abstentions."""
        votes = [
            Vote(guardian_id="g1", vote=VoteChoice.APPROVE),
            Vote(guardian_id="g2", vote=VoteChoice.ABSTAIN),
        ]
        
        percentage = calculate_approval_percentage(votes)
        assert percentage == 100.0  # Only counting approve/reject
    
    def test_no_votes(self):
        """Test with no votes."""
        percentage = calculate_approval_percentage([])
        assert percentage == 0.0


class TestDuplicateVote:
    """Test duplicate vote checking."""
    
    def test_no_duplicate(self):
        """Test when guardian hasn't voted."""
        votes = [
            Vote(guardian_id="g1", vote=VoteChoice.APPROVE),
        ]
        
        assert check_duplicate_vote(votes, "g2") is False
    
    def test_has_duplicate(self):
        """Test when guardian has already voted."""
        votes = [
            Vote(guardian_id="g1", vote=VoteChoice.APPROVE),
            Vote(guardian_id="g2", vote=VoteChoice.REJECT),
        ]
        
        assert check_duplicate_vote(votes, "g1") is True


class TestQuorumStatus:
    """Test comprehensive quorum status."""
    
    def test_quorum_status_complete(self):
        """Test full quorum status information."""
        votes = [
            Vote(guardian_id="g1", vote=VoteChoice.APPROVE),
            Vote(guardian_id="g2", vote=VoteChoice.APPROVE),
            Vote(guardian_id="g3", vote=VoteChoice.REJECT),
            Vote(guardian_id="g4", vote=VoteChoice.ABSTAIN),
        ]
        
        status = get_quorum_status(votes, required_quorum=2)
        
        assert status['votes_approve'] == 2
        assert status['votes_reject'] == 1
        assert status['votes_abstain'] == 1
        assert status['total_votes'] == 4
        assert status['quorum_required'] == 2
        assert status['quorum_met'] is True
        assert status['can_execute'] is True
        assert status['votes_needed'] == 0


class TestVoteEligibility:
    """Test vote eligibility validation."""
    
    def test_eligible_active_guardian(self):
        """Test eligible active guardian."""
        votes = []
        eligible, reason = validate_vote_eligibility("g1", votes, "active")
        
        assert eligible is True
        assert reason == "Eligible to vote"
    
    def test_ineligible_inactive_guardian(self):
        """Test ineligible inactive guardian."""
        votes = []
        eligible, reason = validate_vote_eligibility("g1", votes, "inactive")
        
        assert eligible is False
        assert "inactive" in reason.lower()
    
    def test_ineligible_duplicate_vote(self):
        """Test ineligible due to duplicate vote."""
        votes = [Vote(guardian_id="g1", vote=VoteChoice.APPROVE)]
        eligible, reason = validate_vote_eligibility("g1", votes, "active")
        
        assert eligible is False
        assert "already voted" in reason.lower()


# =============================================================================
# API ENDPOINT TESTS
# =============================================================================

class TestHealthEndpoints:
    """Test API health endpoints."""
    
    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data['service'] == "Hephaestus Guardian Coordinator"
    
    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == "healthy"


class TestProposalEndpoints:
    """Test proposal management endpoints."""
    
    def test_create_proposal(self):
        """Test creating a new proposal."""
        proposal_data = {
            "action": "deploy_contract",
            "description": "Deploy Guardian NFT contract for testing",
            "params": {"contract": "GuardianNFT"},
            "proposer": "test_guardian"
        }
        
        response = client.post("/api/guardian/proposal", json=proposal_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data['action'] == "deploy_contract"
        assert data['proposer'] == "test_guardian"
        assert data['status'] == "pending"
        assert data['votes_approve'] == 0
    
    def test_list_proposals(self):
        """Test listing proposals."""
        response = client.get("/api/guardian/proposals")
        assert response.status_code == 200
        
        data = response.json()
        assert 'proposals' in data
        assert 'total' in data
        assert isinstance(data['proposals'], list)
    
    def test_get_proposal(self):
        """Test getting specific proposal."""
        # First create a proposal
        proposal_data = {
            "action": "custom",
            "description": "Test proposal for retrieval",
            "params": {},
            "proposer": "test_guardian"
        }
        
        create_response = client.post("/api/guardian/proposal", json=proposal_data)
        proposal_id = create_response.json()['proposal_id']
        
        # Then retrieve it
        response = client.get(f"/api/guardian/proposals/{proposal_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data['proposal_id'] == proposal_id
    
    def test_get_nonexistent_proposal(self):
        """Test getting non-existent proposal."""
        response = client.get("/api/guardian/proposals/nonexistent")
        assert response.status_code == 404


class TestVotingEndpoints:
    """Test voting endpoints."""
    
    def test_submit_vote(self):
        """Test submitting a vote."""
        # Create proposal
        proposal_data = {
            "action": "custom",
            "description": "Test proposal for voting",
            "params": {},
            "proposer": "test_guardian"
        }
        
        create_response = client.post("/api/guardian/proposal", json=proposal_data)
        proposal_id = create_response.json()['proposal_id']
        
        # Submit vote
        vote_data = {
            "guardian_id": "guardian_1",
            "vote": "approve",
            "comment": "Looks good!"
        }
        
        response = client.post(f"/api/guardian/vote/{proposal_id}", json=vote_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data['vote_accepted'] is True
        assert data['votes_approve'] == 1
    
    def test_submit_duplicate_vote(self):
        """Test submitting duplicate vote."""
        # Create proposal
        proposal_data = {
            "action": "custom",
            "description": "Test proposal for duplicate vote",
            "params": {},
            "proposer": "test_guardian"
        }
        
        create_response = client.post("/api/guardian/proposal", json=proposal_data)
        proposal_id = create_response.json()['proposal_id']
        
        # Submit first vote
        vote_data = {
            "guardian_id": "guardian_2",
            "vote": "approve"
        }
        
        client.post(f"/api/guardian/vote/{proposal_id}", json=vote_data)
        
        # Submit duplicate vote
        response = client.post(f"/api/guardian/vote/{proposal_id}", json=vote_data)
        assert response.status_code == 400
    
    def test_auto_execute_on_quorum(self):
        """Test proposal auto-executes when quorum is reached."""
        # Create proposal with low quorum
        proposal_data = {
            "action": "custom",
            "description": "Test auto-execution",
            "params": {},
            "proposer": "test_guardian",
            "quorum_required": 2
        }
        
        create_response = client.post("/api/guardian/proposal", json=proposal_data)
        proposal_id = create_response.json()['proposal_id']
        
        # Submit votes to reach quorum
        for i in range(1, 3):
            vote_data = {
                "guardian_id": f"guardian_{i}",
                "vote": "approve"
            }
            response = client.post(f"/api/guardian/vote/{proposal_id}", json=vote_data)
        
        # Last vote should trigger execution
        data = response.json()
        assert data['quorum_met'] is True
        assert data['executed'] is True


class TestGuardianEndpoints:
    """Test guardian management endpoints."""
    
    def test_register_guardian(self):
        """Test registering a new guardian."""
        guardian_data = {
            "guardian_id": "new_guardian_test",
            "display_name": "Test Guardian",
            "status": "active",
            "role": "guardian"
        }
        
        response = client.post("/api/guardian/register", json=guardian_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data['guardian_id'] == "new_guardian_test"
    
    def test_list_guardians(self):
        """Test listing guardians."""
        response = client.get("/api/guardian/list")
        assert response.status_code == 200
        
        data = response.json()
        assert 'guardians' in data
        assert 'total' in data


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
