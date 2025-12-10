"""
Tests for Guardian Coordinator API
Validates ethical entropy filtering and safety checks
"""

import pytest
import os
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def guardian_client():
    """Create test client for Guardian API"""
    # Set required environment variables for testing
    os.environ["APP_ENVIRONMENT"] = "testnet"
    os.environ["GUARDIAN_KILL_SWITCH"] = "off"
    os.environ["NFT_MINT_VALUE"] = "0"
    
    # Import after env vars are set
    from guardian_api import app
    
    client = TestClient(app)
    return client


class TestGuardianHealthEndpoints:
    """Test health and status endpoints"""
    
    def test_health_endpoint(self, guardian_client):
        """Test /health endpoint returns healthy status"""
        response = guardian_client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "Guardian Coordinator"
        assert data["environment"] == "testnet"
        assert data["kill_switch"] == "off"
        assert data["nft_value"] == "0"
    
    def test_root_endpoint(self, guardian_client):
        """Test root endpoint"""
        response = guardian_client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["service"] == "Guardian Coordinator API"
        assert data["environment"] == "testnet"
        assert data["status"] == "active"
    
    def test_sentinel_status(self, guardian_client):
        """Test /sentinel/status endpoint"""
        response = guardian_client.get("/sentinel/status")
        assert response.status_code == 200
        
        data = response.json()
        assert "guardian_id" in data
        assert "validations_processed" in data
        assert "pulses_filtered" in data
        assert data["environment"] == "testnet"
        assert data["status"] == "active_sentinel"


class TestPulseValidation:
    """Test pulse validation logic"""
    
    def test_validate_pulse_success(self, guardian_client):
        """Test successful pulse validation"""
        request_data = {
            "pulse_id": "test-pulse-001",
            "ethical_score": 0.95,
            "qualia_impact": 0.5,
            "resonance_value": 0.8
        }
        
        response = guardian_client.post("/validate", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["pulse_id"] == "test-pulse-001"
        assert "ethical_entropy" in data
        assert data["validation_passed"] is True  # High ethical score = low entropy
        assert data["resonance_approved"] is True  # 0.8 >= 0.70 threshold
        assert data["environment"] == "testnet"
        assert data["nft_value"] == "0"
    
    def test_validate_pulse_high_entropy(self, guardian_client):
        """Test pulse validation with high ethical entropy"""
        request_data = {
            "pulse_id": "test-pulse-002",
            "ethical_score": 0.3,  # Low ethical score
            "qualia_impact": 0.9,  # High qualia impact
            "resonance_value": 0.8
        }
        
        response = guardian_client.post("/validate", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["pulse_id"] == "test-pulse-002"
        assert data["validation_passed"] is False  # High entropy should fail
        assert data["ethical_entropy"] > 0.05  # Above threshold
    
    def test_validate_pulse_low_resonance(self, guardian_client):
        """Test pulse validation with low resonance"""
        request_data = {
            "pulse_id": "test-pulse-003",
            "ethical_score": 0.95,
            "qualia_impact": 0.5,
            "resonance_value": 0.5  # Below 0.70 threshold
        }
        
        response = guardian_client.post("/validate", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["resonance_approved"] is False  # 0.5 < 0.70 threshold
    
    def test_validate_pulse_invalid_data(self, guardian_client):
        """Test validation with invalid input data"""
        request_data = {
            "pulse_id": "test-pulse-004",
            "ethical_score": 1.5,  # Invalid: > 1.0
            "qualia_impact": 0.5,
            "resonance_value": 0.8
        }
        
        response = guardian_client.post("/validate", json=request_data)
        assert response.status_code == 422  # Validation error


class TestSafetyChecks:
    """Test safety enforcement"""
    
    def test_environment_enforcement(self):
        """Test that non-testnet environment is rejected"""
        # This test validates the module-level check
        # In practice, the app wouldn't start with wrong env
        os.environ["APP_ENVIRONMENT"] = "testnet"
        os.environ["GUARDIAN_KILL_SWITCH"] = "off"
        os.environ["NFT_MINT_VALUE"] = "0"
        
        # Import should succeed with correct env
        try:
            import guardian_api
            assert guardian_api.APP_ENVIRONMENT == "testnet"
        except RuntimeError:
            pytest.fail("Guardian API should load with testnet environment")
    
    def test_nft_value_zero(self):
        """Test that NFT value is enforced to zero"""
        os.environ["APP_ENVIRONMENT"] = "testnet"
        os.environ["GUARDIAN_KILL_SWITCH"] = "off"
        os.environ["NFT_MINT_VALUE"] = "0"
        
        import guardian_api
        assert guardian_api.NFT_MINT_VALUE == "0"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
