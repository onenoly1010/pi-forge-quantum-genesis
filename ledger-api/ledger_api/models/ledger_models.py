"""
SQLAlchemy models for Ledger API
Maps to the SQL schema with SQLite-compatible types
"""
from sqlalchemy import (
    Column, String, Numeric, Boolean, DateTime, Text, 
    ForeignKey, CheckConstraint, Index, Integer
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from ledger_api.db import Base


# Helper for UUID - uses string for SQLite compatibility
def get_uuid_column():
    """Returns UUID column compatible with both PostgreSQL and SQLite"""
    try:
        # Try PostgreSQL UUID type
        from sqlalchemy.dialects.postgresql import UUID as PG_UUID
        return Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    except ImportError:
        # Fallback to String for SQLite
        return Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))


class LogicalAccount(Base):
    """
    Logical Accounts - Internal wallet subdivisions
    """
    __tablename__ = "logical_accounts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_name = Column(String(100), nullable=False, unique=True, index=True)
    account_type = Column(String(50), nullable=False, index=True)
    current_balance = Column(Numeric(20, 8), nullable=False, default=0)
    description = Column(Text)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    transactions_to = relationship("LedgerTransaction", foreign_keys="LedgerTransaction.to_account_id", back_populates="to_account")
    transactions_from = relationship("LedgerTransaction", foreign_keys="LedgerTransaction.from_account_id", back_populates="from_account")

    __table_args__ = (
        CheckConstraint("account_type IN ('OPERATING', 'RESERVE', 'REWARDS', 'DEVELOPMENT', 'MARKETING', 'CUSTOM')", name="valid_account_type"),
        CheckConstraint("current_balance >= 0", name="non_negative_balance"),
    )


class LedgerTransaction(Base):
    """
    Ledger Transactions - All financial movements
    """
    __tablename__ = "ledger_transactions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    transaction_type = Column(String(50), nullable=False, index=True)
    status = Column(String(30), nullable=False, index=True)
    amount = Column(Numeric(20, 8), nullable=False)
    
    # Account relationships
    from_account_id = Column(String(36), ForeignKey("logical_accounts.id"), index=True)
    to_account_id = Column(String(36), ForeignKey("logical_accounts.id"), index=True)
    
    # Parent/child hierarchy
    parent_transaction_id = Column(String(36), ForeignKey("ledger_transactions.id"), index=True)
    
    # External identifiers
    external_tx_hash = Column(String(255), index=True)
    pi_payment_id = Column(String(255), index=True)
    
    # Metadata
    description = Column(Text)
    tx_metadata = Column(Text)  # JSON string for SQLite compatibility (renamed to avoid SQLAlchemy conflict)
    
    # User context
    performed_by = Column(String(255))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    completed_at = Column(DateTime(timezone=True))

    # Relationships
    from_account = relationship("LogicalAccount", foreign_keys=[from_account_id], back_populates="transactions_from")
    to_account = relationship("LogicalAccount", foreign_keys=[to_account_id], back_populates="transactions_to")
    parent_transaction = relationship("LedgerTransaction", remote_side=[id], foreign_keys=[parent_transaction_id])
    
    __table_args__ = (
        CheckConstraint("transaction_type IN ('EXTERNAL_DEPOSIT', 'EXTERNAL_WITHDRAWAL', 'INTERNAL_ALLOCATION', 'PAYMENT', 'REFUND', 'FEE', 'NFT_MINT', 'REWARD')", name="valid_transaction_type"),
        CheckConstraint("status IN ('PENDING', 'COMPLETED', 'FAILED', 'CANCELLED', 'REFUNDED')", name="valid_status"),
        CheckConstraint("amount >= 0", name="non_negative_amount"),
    )


class AllocationRule(Base):
    """
    Allocation Rules - Defines how external deposits are split
    """
    __tablename__ = "allocation_rules"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    rule_name = Column(String(100), nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, default=True)
    priority = Column(Integer, nullable=False, default=100)
    
    # Allocation configuration (stored as JSON string for SQLite)
    allocation_config = Column(Text, nullable=False)  # JSON string
    
    # Conditions
    min_amount = Column(Numeric(20, 8))
    max_amount = Column(Numeric(20, 8))
    
    # Metadata
    description = Column(Text)
    created_by = Column(String(255))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        Index('idx_allocation_rules_active', 'is_active', 'priority'),
    )


class AuditLog(Base):
    """
    Audit Log - Immutable record of administrative changes
    """
    __tablename__ = "audit_log"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(String(36), nullable=False, index=True)
    action = Column(String(30), nullable=False)
    
    # Change tracking (JSON strings for SQLite)
    old_value = Column(Text)  # JSON string
    new_value = Column(Text)  # JSON string
    
    # Actor
    performed_by = Column(String(255), nullable=False, index=True)
    
    # Context
    ip_address = Column(String(45))
    user_agent = Column(Text)
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    __table_args__ = (
        CheckConstraint("entity_type IN ('ledger_transaction', 'allocation_rule', 'logical_account', 'reconciliation')", name="valid_entity_type"),
        CheckConstraint("action IN ('CREATE', 'UPDATE', 'DELETE', 'EXECUTE')", name="valid_action"),
        Index('idx_audit_log_entity', 'entity_type', 'entity_id'),
    )


class ReconciliationLog(Base):
    """
    Reconciliation Log - External vs internal balance tracking
    """
    __tablename__ = "reconciliation_log"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # External state
    external_wallet_balance = Column(Numeric(20, 8), nullable=False)
    external_source = Column(String(100))
    
    # Internal state
    internal_total_balance = Column(Numeric(20, 8), nullable=False)
    
    # Comparison
    discrepancy = Column(Numeric(20, 8), nullable=False)
    discrepancy_percentage = Column(Numeric(10, 4))
    
    # Status
    status = Column(String(30), nullable=False, index=True)
    
    # Resolution
    resolution_notes = Column(Text)
    resolved_at = Column(DateTime(timezone=True))
    resolved_by = Column(String(255))
    
    # Context
    performed_by = Column(String(255), nullable=False)
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    __table_args__ = (
        CheckConstraint("status IN ('BALANCED', 'MINOR_DISCREPANCY', 'MAJOR_DISCREPANCY', 'CRITICAL')", name="valid_status"),
    )
