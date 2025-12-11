"""
Pytest configuration and fixtures for ledger API tests
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from ledger_api.db import Base, get_db
from ledger_api.main import app
# Import all models to register them with Base before creating tables
from ledger_api.models.ledger_models import (
    LogicalAccount, 
    LedgerTransaction,
    AllocationRule,
    AuditLog,
    ReconciliationLog
)
import json


# Use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test"""
    # Import here to avoid circular dependencies
    import ledger_api.db as db_module
    
    # Save original engine
    original_engine = db_module.engine
    
    # Replace with test engine
    db_module.engine = engine
    db_module.SessionLocal = TestingSessionLocal
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    db = TestingSessionLocal()
    
    # Seed with default accounts
    seed_default_accounts(db)
    seed_default_allocation_rule(db)
    
    yield db
    
    # Cleanup
    db.close()
    Base.metadata.drop_all(bind=engine)
    
    # Restore original engine
    db_module.engine = original_engine


@pytest.fixture(scope="function")
def client(db):
    """Create a test client with database dependency override"""
    import os
    
    # Set testing flag to skip lifespan database checks
    os.environ["TESTING"] = "true"
    
    def override_get_db():
        try:
            yield db
        finally:
            pass  # Don't close here, let the db fixture handle it
    
    # Override the get_db dependency BEFORE creating TestClient
    app.dependency_overrides[get_db] = override_get_db
    
    # Create client with raise_server_exceptions=False to get proper error responses
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client
    
    # Clear overrides and testing flag
    app.dependency_overrides.clear()
    if "TESTING" in os.environ:
        del os.environ["TESTING"]


def seed_default_accounts(db):
    """Seed default logical accounts for testing"""
    accounts = [
        LogicalAccount(
            account_name="main_operating",
            account_type="OPERATING",
            description="Primary operating account",
            current_balance=0
        ),
        LogicalAccount(
            account_name="reserve_fund",
            account_type="RESERVE",
            description="Reserve fund",
            current_balance=0
        ),
        LogicalAccount(
            account_name="rewards_pool",
            account_type="REWARDS",
            description="Rewards pool",
            current_balance=0
        ),
        LogicalAccount(
            account_name="development_fund",
            account_type="DEVELOPMENT",
            description="Development fund",
            current_balance=0
        ),
        LogicalAccount(
            account_name="marketing_fund",
            account_type="MARKETING",
            description="Marketing fund",
            current_balance=0
        ),
    ]
    
    for account in accounts:
        db.add(account)
    
    db.commit()


def seed_default_allocation_rule(db):
    """Seed default allocation rule for testing"""
    rule = AllocationRule(
        rule_name="default_deposit_allocation",
        is_active=True,
        priority=100,
        allocation_config=json.dumps([
            {"account_name": "main_operating", "percentage": "50"},
            {"account_name": "reserve_fund", "percentage": "20"},
            {"account_name": "rewards_pool", "percentage": "15"},
            {"account_name": "development_fund", "percentage": "10"},
            {"account_name": "marketing_fund", "percentage": "5"}
        ]),
        description="Default allocation rule",
        created_by="test_system"
    )
    
    db.add(rule)
    db.commit()


@pytest.fixture
def guardian_token():
    """Generate a valid guardian JWT token for testing"""
    from ledger_api.utils.jwt_auth import create_jwt_token
    import os
    
    # Set a test JWT secret if not already set
    if not os.getenv("GUARDIAN_JWT_SECRET"):
        os.environ["GUARDIAN_JWT_SECRET"] = "test-secret-key-at-least-32-characters-long-for-testing"
    
    return create_jwt_token(sub="test_guardian", role="guardian")
