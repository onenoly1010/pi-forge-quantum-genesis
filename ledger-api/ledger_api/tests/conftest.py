"""
Pytest configuration and fixtures for Ledger API tests.
Sets up in-memory SQLite database for testing.
"""

import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Set test environment
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["GUARDIAN_JWT_SECRET"] = "test-secret-key-min-32-characters-long"
os.environ["NFT_MINT_VALUE"] = "0"
os.environ["APP_ENVIRONMENT"] = "testnet"

from ledger_api.db import Base, get_db
from ledger_api.main import app
from ledger_api.models.ledger_models import LogicalAccount, AllocationRule


@pytest.fixture(scope="function")
def test_engine():
    """Create a test database engine."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )
    return engine


@pytest.fixture(scope="function")
def test_db(test_engine):
    """Create test database session."""
    # Create tables
    Base.metadata.create_all(bind=test_engine)
    
    # Create session
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine
    )
    
    db = TestingSessionLocal()
    
    # Seed with default accounts
    seed_test_data(db)
    
    yield db
    
    db.close()
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(test_db):
    """Create test client with test database."""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def guardian_token():
    """Create a guardian JWT token for testing."""
    from ledger_api.utils.jwt_auth import create_guardian_token
    return create_guardian_token(user_id="test_guardian", role="guardian")


def seed_test_data(db):
    """Seed database with test data."""
    # Create logical accounts
    accounts = [
        LogicalAccount(
            account_name="Reserve Treasury",
            account_type="RESERVE",
            current_balance=0,
            allocation_percentage=40.0,
            is_active=True,
            meta_data={"description": "Reserve fund"}
        ),
        LogicalAccount(
            account_name="Development Fund",
            account_type="DEVELOPMENT",
            current_balance=0,
            allocation_percentage=25.0,
            is_active=True,
            meta_data={"description": "Development funding"}
        ),
        LogicalAccount(
            account_name="Community Rewards",
            account_type="COMMUNITY",
            current_balance=0,
            allocation_percentage=20.0,
            is_active=True,
            meta_data={"description": "Community rewards"}
        ),
        LogicalAccount(
            account_name="Operational Fund",
            account_type="OPERATIONAL",
            current_balance=0,
            allocation_percentage=15.0,
            is_active=True,
            meta_data={"description": "Operations"}
        )
    ]
    
    for account in accounts:
        db.add(account)
    
    db.flush()
    
    # Create default allocation rule
    default_rule = AllocationRule(
        rule_name="Default Deposit Allocation",
        trigger_transaction_type="EXTERNAL_DEPOSIT",
        purpose="Automatic allocation of incoming deposits",
        allocations=[
            {"account_id": 1, "percentage": 40.0},
            {"account_id": 2, "percentage": 25.0},
            {"account_id": 3, "percentage": 20.0},
            {"account_id": 4, "percentage": 15.0}
        ],
        is_active=True,
        priority=1,
        created_by="system"
    )
    
    db.add(default_rule)
    db.commit()
