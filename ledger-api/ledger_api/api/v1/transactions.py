"""
Transaction API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
import json
import logging

from ledger_api.db import get_db
from ledger_api.models.ledger_models import LedgerTransaction
from ledger_api.schemas.transaction import (
    TransactionCreate,
    TransactionResponse,
    TransactionListResponse,
    AllocationResult
)
from ledger_api.services.allocation import apply_allocations_for_transaction
from ledger_api.services.audit import create_audit_log

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/transactions", tags=["transactions"])


@router.post("", response_model=TransactionResponse, status_code=201)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
) -> TransactionResponse:
    """
    Create a new transaction.
    
    If the transaction is a COMPLETED EXTERNAL_DEPOSIT, the allocation engine
    will automatically run to split the funds according to allocation rules.
    """
    # Convert metadata dict to JSON string for storage
    metadata_json = json.dumps(transaction.metadata) if transaction.metadata else None

    # Create the transaction
    db_transaction = LedgerTransaction(
        transaction_type=transaction.transaction_type,
        status=transaction.status,
        amount=transaction.amount,
        from_account_id=transaction.from_account_id,
        to_account_id=transaction.to_account_id,
        parent_transaction_id=transaction.parent_transaction_id,
        external_tx_hash=transaction.external_tx_hash,
        pi_payment_id=transaction.pi_payment_id,
        description=transaction.description,
        tx_metadata=metadata_json,
        performed_by=transaction.performed_by
    )

    # Set completed_at if status is COMPLETED
    if transaction.status == "COMPLETED":
        db_transaction.completed_at = datetime.utcnow()

    try:
        db.add(db_transaction)
        db.flush()

        # Create audit log
        create_audit_log(
            db=db,
            entity_type="ledger_transaction",
            entity_id=db_transaction.id,
            action="CREATE",
            old_value=None,
            new_value={
                "transaction_type": transaction.transaction_type,
                "status": transaction.status,
                "amount": str(transaction.amount)
            },
            performed_by=transaction.performed_by or "system"
        )

        # Apply allocations if this is a COMPLETED EXTERNAL_DEPOSIT
        if (transaction.transaction_type == "EXTERNAL_DEPOSIT" and 
            transaction.status == "COMPLETED"):
            try:
                child_ids = apply_allocations_for_transaction(
                    db=db,
                    transaction_id=db_transaction.id,
                    performed_by=transaction.performed_by
                )
                logger.info(f"Applied allocations for transaction {db_transaction.id}: {len(child_ids)} children created")
            except Exception as e:
                logger.error(f"Failed to apply allocations: {e}")
                # Rollback the entire transaction including the parent
                db.rollback()
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to apply allocations: {str(e)}"
                )

        # Commit the transaction
        db.commit()
        db.refresh(db_transaction)

        # Parse tx_metadata back to dict for response
        if db_transaction.tx_metadata:
            db_transaction.metadata = json.loads(db_transaction.tx_metadata)
        else:
            db_transaction.metadata = None

        return db_transaction

    except Exception as e:
        db.rollback()
        logger.error(f"Error creating transaction: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=TransactionListResponse)
def list_transactions(
    transaction_type: Optional[str] = Query(None, description="Filter by transaction type"),
    status: Optional[str] = Query(None, description="Filter by status"),
    from_account_id: Optional[str] = Query(None, description="Filter by source account"),
    to_account_id: Optional[str] = Query(None, description="Filter by destination account"),
    parent_transaction_id: Optional[str] = Query(None, description="Filter by parent transaction"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Page size"),
    db: Session = Depends(get_db)
) -> TransactionListResponse:
    """
    List transactions with optional filters.
    """
    # Build query
    query = db.query(LedgerTransaction)

    # Apply filters
    if transaction_type:
        query = query.filter(LedgerTransaction.transaction_type == transaction_type)
    
    if status:
        query = query.filter(LedgerTransaction.status == status)
    
    if from_account_id:
        query = query.filter(LedgerTransaction.from_account_id == from_account_id)
    
    if to_account_id:
        query = query.filter(LedgerTransaction.to_account_id == to_account_id)
    
    if parent_transaction_id:
        query = query.filter(LedgerTransaction.parent_transaction_id == parent_transaction_id)

    # Get total count
    total = query.count()

    # Apply pagination
    offset = (page - 1) * page_size
    transactions = query.order_by(LedgerTransaction.created_at.desc()).offset(offset).limit(page_size).all()

    # Parse metadata for each transaction
    for tx in transactions:
        if tx.tx_metadata:
            try:
                tx.metadata = json.loads(tx.tx_metadata)
            except json.JSONDecodeError:
                tx.metadata = {}
        else:
            tx.metadata = None

    return TransactionListResponse(
        transactions=transactions,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
    transaction_id: str,
    db: Session = Depends(get_db)
) -> TransactionResponse:
    """
    Get a specific transaction by ID.
    """
    transaction = db.query(LedgerTransaction).filter(
        LedgerTransaction.id == transaction_id
    ).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # Parse metadata
    if transaction.tx_metadata:
        try:
            transaction.metadata = json.loads(transaction.tx_metadata)
        except json.JSONDecodeError:
            transaction.metadata = {}
    else:
        transaction.metadata = None

    return transaction


@router.get("/{transaction_id}/allocations", response_model=AllocationResult)
def get_transaction_allocations(
    transaction_id: str,
    db: Session = Depends(get_db)
) -> AllocationResult:
    """
    Get allocation results for a transaction.
    Returns child transactions created by the allocation engine.
    """
    # Get parent transaction
    parent_tx = db.query(LedgerTransaction).filter(
        LedgerTransaction.id == transaction_id
    ).first()

    if not parent_tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # Get child allocations
    children = db.query(LedgerTransaction).filter(
        LedgerTransaction.parent_transaction_id == transaction_id,
        LedgerTransaction.transaction_type == "INTERNAL_ALLOCATION"
    ).all()

    total_allocated = sum(child.amount for child in children)
    
    return AllocationResult(
        parent_transaction_id=transaction_id,
        child_transaction_ids=[child.id for child in children],
        total_allocated=total_allocated,
        allocation_count=len(children)
    )
