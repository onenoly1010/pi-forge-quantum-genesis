"""
Treasury status API endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from decimal import Decimal

from ledger_api.db import get_db
from ledger_api.models.ledger_models import LogicalAccount
from ledger_api.schemas.treasury import (
    TreasuryStatusResponse,
    AccountBalance
)

router = APIRouter(prefix="/api/v1/treasury", tags=["treasury"])


@router.get("/status", response_model=TreasuryStatusResponse)
def get_treasury_status(
    db: Session = Depends(get_db)
) -> TreasuryStatusResponse:
    """
    Get current treasury status showing all account balances.
    """
    # Get all active accounts
    accounts = db.query(LogicalAccount).filter(
        LogicalAccount.is_active == True
    ).order_by(LogicalAccount.account_type, LogicalAccount.account_name).all()

    # Calculate total balance
    total_balance = sum(account.current_balance for account in accounts)

    # Convert to response schema
    account_balances = [
        AccountBalance(
            account_name=account.account_name,
            account_type=account.account_type,
            current_balance=account.current_balance,
            is_active=account.is_active,
            updated_at=account.updated_at
        )
        for account in accounts
    ]

    return TreasuryStatusResponse(
        accounts=account_balances,
        total_balance=total_balance,
        active_account_count=len(accounts),
        timestamp=datetime.utcnow()
    )
