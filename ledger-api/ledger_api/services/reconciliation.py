"""
Reconciliation service for comparing external and internal balances
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal
from typing import Optional
import logging

from ledger_api.models.ledger_models import (
    ReconciliationLog,
    LogicalAccount
)
from ledger_api.services.audit import create_audit_log

logger = logging.getLogger(__name__)


def calculate_internal_total_balance(db: Session) -> Decimal:
    """
    Calculate total internal balance across all active accounts.
    
    Args:
        db: Database session
        
    Returns:
        Total balance as Decimal
    """
    result = db.query(
        func.sum(LogicalAccount.current_balance)
    ).filter(
        LogicalAccount.is_active == True
    ).scalar()

    return Decimal(str(result)) if result else Decimal(0)


def perform_reconciliation(
    db: Session,
    external_wallet_balance: Decimal,
    external_source: Optional[str],
    performed_by: str
) -> ReconciliationLog:
    """
    Perform reconciliation between external wallet and internal accounts.
    
    Args:
        db: Database session
        external_wallet_balance: Balance from external wallet
        external_source: Source of external balance (e.g., "Pi Network Wallet")
        performed_by: User performing reconciliation
        
    Returns:
        ReconciliationLog entry
    """
    # Calculate internal total
    internal_total = calculate_internal_total_balance(db)

    # Calculate discrepancy
    discrepancy = external_wallet_balance - internal_total

    # Calculate percentage discrepancy
    if external_wallet_balance != 0:
        discrepancy_percentage = (abs(discrepancy) / external_wallet_balance * 100).quantize(Decimal('0.0001'))
    else:
        discrepancy_percentage = Decimal(0) if internal_total == 0 else Decimal(100)

    # Determine status based on discrepancy
    abs_discrepancy = abs(discrepancy)
    if abs_discrepancy == 0:
        status = "BALANCED"
    elif discrepancy_percentage < Decimal('0.1'):  # Less than 0.1%
        status = "MINOR_DISCREPANCY"
    elif discrepancy_percentage < Decimal('5'):  # Less than 5%
        status = "MAJOR_DISCREPANCY"
    else:
        status = "CRITICAL"

    # Create reconciliation log
    reconciliation = ReconciliationLog(
        external_wallet_balance=external_wallet_balance,
        external_source=external_source,
        internal_total_balance=internal_total,
        discrepancy=discrepancy,
        discrepancy_percentage=discrepancy_percentage,
        status=status,
        performed_by=performed_by
    )

    db.add(reconciliation)
    db.flush()

    # Create audit log
    create_audit_log(
        db=db,
        entity_type="reconciliation",
        entity_id=reconciliation.id,
        action="CREATE",
        old_value=None,
        new_value={
            "external_wallet_balance": str(external_wallet_balance),
            "internal_total_balance": str(internal_total),
            "discrepancy": str(discrepancy),
            "status": status
        },
        performed_by=performed_by
    )

    logger.info(
        f"Reconciliation performed: External={external_wallet_balance}, "
        f"Internal={internal_total}, Discrepancy={discrepancy}, Status={status}"
    )

    return reconciliation


def get_latest_reconciliation(db: Session) -> Optional[ReconciliationLog]:
    """
    Get the most recent reconciliation record.
    
    Args:
        db: Database session
        
    Returns:
        Latest ReconciliationLog or None
    """
    return db.query(ReconciliationLog).order_by(
        ReconciliationLog.created_at.desc()
    ).first()


def get_reconciliation_history(
    db: Session,
    limit: int = 50,
    status: Optional[str] = None
) -> list:
    """
    Get reconciliation history with optional status filter.
    
    Args:
        db: Database session
        limit: Maximum number of records to return
        status: Optional status filter
        
    Returns:
        List of ReconciliationLog entries
    """
    query = db.query(ReconciliationLog)

    if status:
        query = query.filter(ReconciliationLog.status == status)

    query = query.order_by(ReconciliationLog.created_at.desc())
    query = query.limit(limit)

    return query.all()
