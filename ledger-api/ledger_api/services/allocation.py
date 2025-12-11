"""
Allocation Engine - Atomic and Idempotent Allocation Logic
Handles automatic splitting of EXTERNAL_DEPOSIT transactions
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from decimal import Decimal
from typing import List, Optional, Dict, Any
import json
import logging

from ledger_api.models.ledger_models import (
    LedgerTransaction, 
    AllocationRule, 
    LogicalAccount
)
from ledger_api.services.audit import create_audit_log

logger = logging.getLogger(__name__)


class AllocationEngine:
    """
    Atomic allocation engine for splitting external deposits
    """

    def __init__(self, db: Session):
        self.db = db

    def apply_allocations(
        self, 
        parent_transaction_id: str,
        performed_by: Optional[str] = None
    ) -> List[str]:
        """
        Apply allocation rules to a COMPLETED EXTERNAL_DEPOSIT transaction.
        
        This method is:
        - Atomic: All allocations happen in one DB transaction or none
        - Idempotent: Can be called multiple times without creating duplicates
        
        Args:
            parent_transaction_id: ID of the parent EXTERNAL_DEPOSIT transaction
            performed_by: User performing the allocation
            
        Returns:
            List of created child transaction IDs
            
        Raises:
            ValueError: If transaction is not eligible for allocation
        """
        # Get the parent transaction
        parent_tx = self.db.query(LedgerTransaction).filter(
            LedgerTransaction.id == parent_transaction_id
        ).first()

        if not parent_tx:
            raise ValueError(f"Transaction {parent_transaction_id} not found")

        # Validate transaction is eligible for allocation
        if parent_tx.transaction_type != "EXTERNAL_DEPOSIT":
            raise ValueError(f"Transaction type must be EXTERNAL_DEPOSIT, got {parent_tx.transaction_type}")
        
        if parent_tx.status != "COMPLETED":
            raise ValueError(f"Transaction status must be COMPLETED, got {parent_tx.status}")

        # Check for idempotency - if allocations already exist, return them
        existing_allocations = self.db.query(LedgerTransaction).filter(
            and_(
                LedgerTransaction.parent_transaction_id == parent_transaction_id,
                LedgerTransaction.transaction_type == "INTERNAL_ALLOCATION"
            )
        ).all()

        if existing_allocations:
            logger.info(f"Allocations already exist for transaction {parent_transaction_id}, returning existing")
            return [alloc.id for alloc in existing_allocations]

        # IMPORTANT: First, credit the parent deposit to the target account
        # This is the initial deposit that arrives
        target_account = self.db.query(LogicalAccount).filter(
            LogicalAccount.id == parent_tx.to_account_id
        ).first()
        
        if not target_account:
            raise ValueError(f"Target account {parent_tx.to_account_id} not found")
        
        # Add the deposit to the target account
        target_account.current_balance += parent_tx.amount
        self.db.flush()
        
        logger.info(f"Credited {parent_tx.amount} to {target_account.account_name}")

        # Get applicable allocation rule
        allocation_rule = self._get_applicable_rule(parent_tx.amount)
        
        if not allocation_rule:
            logger.warning(f"No applicable allocation rule found for amount {parent_tx.amount}")
            return []

        # Parse allocation config
        try:
            config = json.loads(allocation_rule.allocation_config)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse allocation config: {e}")
            raise ValueError(f"Invalid allocation config: {e}")

        # Create child allocations
        child_transaction_ids = []
        total_allocated = Decimal(0)

        for allocation in config:
            account_name = allocation.get('account_name')
            percentage = Decimal(str(allocation.get('percentage', 0)))

            # Get the target account
            target_account = self.db.query(LogicalAccount).filter(
                LogicalAccount.account_name == account_name,
                LogicalAccount.is_active == True
            ).first()

            if not target_account:
                logger.error(f"Target account {account_name} not found or inactive")
                # Rollback will happen at transaction level
                raise ValueError(f"Target account {account_name} not found or inactive")

            # Calculate allocation amount
            allocation_amount = (parent_tx.amount * percentage / 100).quantize(Decimal('0.00000001'))

            # Create child transaction
            child_tx = LedgerTransaction(
                transaction_type="INTERNAL_ALLOCATION",
                status="COMPLETED",
                amount=allocation_amount,
                from_account_id=parent_tx.to_account_id,  # From parent's destination
                to_account_id=target_account.id,
                parent_transaction_id=parent_transaction_id,
                description=f"Auto-allocation: {percentage}% to {account_name}",
                tx_metadata=json.dumps({
                    "allocation_rule_id": allocation_rule.id,
                    "allocation_rule_name": allocation_rule.rule_name,
                    "percentage": str(percentage)
                }),
                performed_by=performed_by or "allocation_engine"
            )

            self.db.add(child_tx)
            self.db.flush()  # Get the ID without committing

            # Update account balances
            # Deduct from source account (parent's to_account)
            source_account = self.db.query(LogicalAccount).filter(
                LogicalAccount.id == parent_tx.to_account_id
            ).first()
            
            if source_account:
                source_account.current_balance -= allocation_amount

            # Add to target account
            target_account.current_balance += allocation_amount

            child_transaction_ids.append(child_tx.id)
            total_allocated += allocation_amount

            logger.info(f"Created allocation: {allocation_amount} to {account_name}")

        # Create audit log entry
        create_audit_log(
            db=self.db,
            entity_type="ledger_transaction",
            entity_id=parent_transaction_id,
            action="EXECUTE",
            old_value=None,
            new_value={
                "allocation_rule_id": allocation_rule.id,
                "child_transactions": child_transaction_ids,
                "total_allocated": str(total_allocated)
            },
            performed_by=performed_by or "allocation_engine"
        )

        logger.info(f"Successfully created {len(child_transaction_ids)} allocations totaling {total_allocated}")

        return child_transaction_ids

    def _get_applicable_rule(self, amount: Decimal) -> Optional[AllocationRule]:
        """
        Get the most applicable allocation rule for the given amount.
        
        Rules are selected based on:
        1. Amount range (min_amount <= amount <= max_amount)
        2. Active status
        3. Priority (lower number = higher priority)
        
        Args:
            amount: Transaction amount
            
        Returns:
            Most applicable AllocationRule or None
        """
        # Query for active rules
        query = self.db.query(AllocationRule).filter(
            AllocationRule.is_active == True
        )

        # Filter by amount range
        rules = query.all()
        applicable_rules = []

        for rule in rules:
            # Check min_amount
            if rule.min_amount is not None and amount < rule.min_amount:
                continue
            
            # Check max_amount
            if rule.max_amount is not None and amount > rule.max_amount:
                continue

            applicable_rules.append(rule)

        if not applicable_rules:
            return None

        # Sort by priority (lower = higher priority)
        applicable_rules.sort(key=lambda r: r.priority)

        return applicable_rules[0]


def apply_allocations_for_transaction(
    db: Session,
    transaction_id: str,
    performed_by: Optional[str] = None
) -> List[str]:
    """
    Convenience function to apply allocations for a transaction.
    
    Args:
        db: Database session
        transaction_id: ID of the EXTERNAL_DEPOSIT transaction
        performed_by: User performing the allocation
        
    Returns:
        List of created child transaction IDs
    """
    engine = AllocationEngine(db)
    return engine.apply_allocations(transaction_id, performed_by)
