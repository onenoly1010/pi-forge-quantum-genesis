"""
Reconciliation API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ledger_api.db import get_db
from ledger_api.schemas.treasury import (
    ReconciliationRequest,
    ReconciliationResponse
)
from ledger_api.services.reconciliation import perform_reconciliation

router = APIRouter(prefix="/api/v1/treasury", tags=["reconciliation"])


@router.post("/reconcile", response_model=ReconciliationResponse, status_code=201)
def reconcile_treasury(
    request: ReconciliationRequest,
    db: Session = Depends(get_db)
) -> ReconciliationResponse:
    """
    Perform reconciliation between external wallet balance and internal accounts.
    
    Compares the provided external wallet balance with the sum of all internal
    account balances and creates a reconciliation log entry.
    """
    try:
        reconciliation = perform_reconciliation(
            db=db,
            external_wallet_balance=request.external_wallet_balance,
            external_source=request.external_source,
            performed_by=request.performed_by
        )

        db.commit()
        db.refresh(reconciliation)

        return reconciliation

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
