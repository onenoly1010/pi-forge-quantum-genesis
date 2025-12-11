"""
Tests for transaction API endpoints
"""
import pytest
from decimal import Decimal
from fastapi.testclient import TestClient

from ledger_api.models.ledger_models import LogicalAccount


def test_create_simple_transaction(client: TestClient, db):
    """Test creating a simple PENDING transaction"""
    # Get an account
    account = db.query(LogicalAccount).filter(
        LogicalAccount.account_name == "main_operating"
    ).first()
    
    # Create transaction payload
    payload = {
        "transaction_type": "PAYMENT",
        "status": "PENDING",
        "amount": "50.00000000",
        "from_account_id": account.id,
        "to_account_id": account.id,
        "description": "Test payment",
        "performed_by": "test_user"
    }
    
    # Make request
    response = client.post("/api/v1/transactions", json=payload)
    
    # Verify response
    assert response.status_code == 201
    data = response.json()
    assert data["transaction_type"] == "PAYMENT"
    assert data["status"] == "PENDING"
    assert data["amount"] == "50.00000000"


def test_create_completed_external_deposit_triggers_allocations(client: TestClient, db):
    """Test that COMPLETED EXTERNAL_DEPOSIT automatically triggers allocations"""
    # Get an account
    account = db.query(LogicalAccount).filter(
        LogicalAccount.account_name == "main_operating"
    ).first()
    
    # Create COMPLETED EXTERNAL_DEPOSIT
    payload = {
        "transaction_type": "EXTERNAL_DEPOSIT",
        "status": "COMPLETED",
        "amount": "100.00000000",
        "to_account_id": account.id,
        "external_tx_hash": "0xabc123",
        "description": "External deposit with auto-allocation",
        "performed_by": "test_user"
    }
    
    # Make request
    response = client.post("/api/v1/transactions", json=payload)
    
    # Verify transaction created
    assert response.status_code == 201
    data = response.json()
    parent_id = data["id"]
    
    # Check allocations were created
    allocations_response = client.get(f"/api/v1/transactions/{parent_id}/allocations")
    assert allocations_response.status_code == 200
    
    allocations_data = allocations_response.json()
    assert allocations_data["allocation_count"] == 5
    assert allocations_data["total_allocated"] == "100.00000000"
    assert len(allocations_data["child_transaction_ids"]) == 5


def test_list_transactions(client: TestClient, db):
    """Test listing transactions with filters"""
    # Get an account
    account = db.query(LogicalAccount).filter(
        LogicalAccount.account_name == "main_operating"
    ).first()
    
    # Create some transactions
    for i in range(3):
        payload = {
            "transaction_type": "PAYMENT",
            "status": "COMPLETED",
            "amount": f"{i+1}.00000000",
            "from_account_id": account.id,
            "to_account_id": account.id,
            "description": f"Test payment {i}",
            "performed_by": "test_user"
        }
        client.post("/api/v1/transactions", json=payload)
    
    # List all transactions
    response = client.get("/api/v1/transactions")
    assert response.status_code == 200
    
    data = response.json()
    assert data["total"] >= 3
    assert len(data["transactions"]) >= 3


def test_list_transactions_with_filters(client: TestClient, db):
    """Test listing transactions with type filter"""
    account = db.query(LogicalAccount).filter(
        LogicalAccount.account_name == "main_operating"
    ).first()
    
    # Create PAYMENT
    client.post("/api/v1/transactions", json={
        "transaction_type": "PAYMENT",
        "status": "COMPLETED",
        "amount": "10.00000000",
        "from_account_id": account.id,
        "to_account_id": account.id,
        "performed_by": "test_user"
    })
    
    # Create REFUND
    client.post("/api/v1/transactions", json={
        "transaction_type": "REFUND",
        "status": "COMPLETED",
        "amount": "5.00000000",
        "from_account_id": account.id,
        "to_account_id": account.id,
        "performed_by": "test_user"
    })
    
    # Filter by PAYMENT
    response = client.get("/api/v1/transactions?transaction_type=PAYMENT")
    assert response.status_code == 200
    
    data = response.json()
    assert all(tx["transaction_type"] == "PAYMENT" for tx in data["transactions"])


def test_get_transaction_by_id(client: TestClient, db):
    """Test getting a specific transaction"""
    account = db.query(LogicalAccount).filter(
        LogicalAccount.account_name == "main_operating"
    ).first()
    
    # Create transaction
    create_response = client.post("/api/v1/transactions", json={
        "transaction_type": "PAYMENT",
        "status": "COMPLETED",
        "amount": "25.00000000",
        "from_account_id": account.id,
        "to_account_id": account.id,
        "description": "Get by ID test",
        "performed_by": "test_user"
    })
    
    tx_id = create_response.json()["id"]
    
    # Get transaction by ID
    response = client.get(f"/api/v1/transactions/{tx_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == tx_id
    assert data["description"] == "Get by ID test"


def test_get_nonexistent_transaction(client: TestClient):
    """Test getting a transaction that doesn't exist"""
    response = client.get("/api/v1/transactions/nonexistent-id")
    assert response.status_code == 404


def test_transaction_validation_negative_amount(client: TestClient, db):
    """Test that negative amounts are rejected"""
    account = db.query(LogicalAccount).filter(
        LogicalAccount.account_name == "main_operating"
    ).first()
    
    # Try to create transaction with negative amount
    payload = {
        "transaction_type": "PAYMENT",
        "status": "PENDING",
        "amount": "-10.00000000",  # Negative
        "from_account_id": account.id,
        "to_account_id": account.id,
        "performed_by": "test_user"
    }
    
    response = client.post("/api/v1/transactions", json=payload)
    assert response.status_code == 422  # Validation error


def test_transaction_validation_invalid_type(client: TestClient, db):
    """Test that invalid transaction types are rejected"""
    account = db.query(LogicalAccount).filter(
        LogicalAccount.account_name == "main_operating"
    ).first()
    
    payload = {
        "transaction_type": "INVALID_TYPE",
        "status": "PENDING",
        "amount": "10.00000000",
        "from_account_id": account.id,
        "to_account_id": account.id,
        "performed_by": "test_user"
    }
    
    response = client.post("/api/v1/transactions", json=payload)
    assert response.status_code == 422  # Validation error


def test_pagination(client: TestClient, db):
    """Test transaction list pagination"""
    account = db.query(LogicalAccount).filter(
        LogicalAccount.account_name == "main_operating"
    ).first()
    
    # Create 10 transactions
    for i in range(10):
        client.post("/api/v1/transactions", json={
            "transaction_type": "PAYMENT",
            "status": "COMPLETED",
            "amount": f"{i+1}.00000000",
            "from_account_id": account.id,
            "to_account_id": account.id,
            "performed_by": "test_user"
        })
    
    # Get first page (5 items)
    response = client.get("/api/v1/transactions?page=1&page_size=5")
    assert response.status_code == 200
    
    data = response.json()
    assert data["page"] == 1
    assert data["page_size"] == 5
    assert len(data["transactions"]) == 5
    assert data["total"] >= 10
    
    # Get second page
    response = client.get("/api/v1/transactions?page=2&page_size=5")
    assert response.status_code == 200
    
    data = response.json()
    assert data["page"] == 2
    assert len(data["transactions"]) == 5
