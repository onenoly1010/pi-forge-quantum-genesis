#!/usr/bin/env python3
"""
Tests for the POST /api/analyze endpoint
"""

import pytest
from fastapi.testclient import TestClient
import sys
sys.path.insert(0, 'server')
from main import app

client = TestClient(app)


class TestAnalyzeEndpoint:
    """Test suite for the /api/analyze security analysis endpoint"""

    def test_approved_transaction(self):
        """Test that a normal transaction is approved"""
        response = client.post(
            "/api/analyze",
            json={"user": "john_doe", "amount": 500.0}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "APPROVED"
        assert "approved" in data["message"].lower()

    def test_blocked_high_amount(self):
        """Test that high amount transactions are blocked"""
        response = client.post(
            "/api/analyze",
            json={"user": "john_doe", "amount": 15000.0}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "BLOCKED"
        assert "exceeds maximum" in data["message"].lower() or "blocked" in data["message"].lower()

    def test_blocked_anonymous_user(self):
        """Test that anonymous users are blocked"""
        response = client.post(
            "/api/analyze",
            json={"user": "anonymous", "amount": 100.0}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "BLOCKED"
        assert "anonymous" in data["message"].lower()

    def test_blocked_guest_user(self):
        """Test that guest users are blocked"""
        response = client.post(
            "/api/analyze",
            json={"user": "guest", "amount": 100.0}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "BLOCKED"

    def test_blocked_empty_user(self):
        """Test that empty username is blocked"""
        response = client.post(
            "/api/analyze",
            json={"user": "", "amount": 100.0}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "BLOCKED"

    def test_warning_medium_amount(self):
        """Test that medium amount transactions get a warning"""
        response = client.post(
            "/api/analyze",
            json={"user": "john_doe", "amount": 5000.0}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "WARNING"
        assert "review" in data["message"].lower() or "warning" in data["message"].lower()

    def test_approved_at_threshold_boundary(self):
        """Test that amount exactly at medium threshold is approved"""
        response = client.post(
            "/api/analyze",
            json={"user": "john_doe", "amount": 1000.0}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "APPROVED"

    def test_warning_just_above_medium_threshold(self):
        """Test that amount just above medium threshold gets warning"""
        response = client.post(
            "/api/analyze",
            json={"user": "john_doe", "amount": 1000.01}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "WARNING"

    def test_blocked_at_high_threshold(self):
        """Test that amount just above high threshold is blocked"""
        response = client.post(
            "/api/analyze",
            json={"user": "john_doe", "amount": 10000.01}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "BLOCKED"

    def test_user_case_insensitive(self):
        """Test that anonymous user check is case insensitive"""
        response = client.post(
            "/api/analyze",
            json={"user": "ANONYMOUS", "amount": 100.0}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "BLOCKED"

    def test_user_with_whitespace(self):
        """Test that user with whitespace around anonymous is blocked"""
        response = client.post(
            "/api/analyze",
            json={"user": "  anonymous  ", "amount": 100.0}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "BLOCKED"

    def test_invalid_request_missing_user(self):
        """Test that request without user field returns validation error"""
        response = client.post(
            "/api/analyze",
            json={"amount": 100.0}
        )
        assert response.status_code == 422  # Validation error

    def test_invalid_request_missing_amount(self):
        """Test that request without amount field returns validation error"""
        response = client.post(
            "/api/analyze",
            json={"user": "john_doe"}
        )
        assert response.status_code == 422  # Validation error

    def test_response_contains_required_fields(self):
        """Test that response always contains status and message fields"""
        response = client.post(
            "/api/analyze",
            json={"user": "john_doe", "amount": 100.0}
        )
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "message" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
