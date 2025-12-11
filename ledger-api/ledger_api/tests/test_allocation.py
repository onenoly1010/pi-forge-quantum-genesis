"""
Tests for allocation engine
"""
import pytest
from decimal import Decimal
from sqlalchemy.orm import Session

from ledger_api.models.ledger_models import LedgerTransaction, LogicalAccount
from ledger_api.services.allocation import AllocationEngine, apply_allocations_for_transaction


def test_allocation_engine_creates_child_transactions(db: Session):
    """Test that allocation engine creates child transactions for COMPLETED EXTERNAL_DEPOSIT"""
    # Get an account to deposit to
    account = db.query(LogicalAccount).filter(
        LogicalAccount.account_name == "main_operating"
    ).first()
    
    # Create a COMPLETED EXTERNAL_DEPOSIT transaction
    parent_tx = LedgerTransaction(
        transaction_type="EXTERNAL_DEPOSIT",
        status="COMPLETED",
        amount=Decimal("100.00000000"),
        to_account_id=account.id,
        external_tx_hash="0xtest123",
        description="Test deposit",
        performed_by="test_user"
    )
    
    db.add(parent_tx)
    db.commit()
    db.refresh(parent_tx)
    
    # Record initial balance
    initial_balance = account.current_balance
    
    # Apply allocations
    engine = AllocationEngine(db)
    child_ids = engine.apply_allocations(parent_tx.id, performed_by="test_user")
    db.commit()
    
    # Verify child transactions were created
    assert len(child_ids) == 5, "Should create 5 child allocations"
    
    # Verify all children are INTERNAL_ALLOCATION type
    children = db.query(LedgerTransaction).filter(
        LedgerTransaction.id.in_(child_ids)
    ).all()
    
    for child in children:
        assert child.transaction_type == "INTERNAL_ALLOCATION"
        assert child.status == "COMPLETED"
        assert child.parent_transaction_id == parent_tx.id
    
    # Verify total allocation equals parent amount
    total_allocated = sum(child.amount for child in children)
    assert total_allocated == parent_tx.amount, "Total allocation should equal parent amount"
    
    # Verify percentages match the default rule (50, 20, 15, 10, 5)
    expected_allocations = {
        "main_operating": Decimal("50.00000000"),
        "reserve_fund": Decimal("20.00000000"),
        "rewards_pool": Decimal("15.00000000"),
        "development_fund": Decimal("10.00000000"),
        "marketing_fund": Decimal("5.00000000")
    }
    
    for child in children:
        target_account = db.query(LogicalAccount).filter(
            LogicalAccount.id == child.to_account_id
        ).first()
        assert child.amount == expected_allocations[target_account.account_name]


def test_allocation_engine_updates_balances(db: Session):
    """Test that allocation engine updates account balances correctly"""
    # Get accounts
    main_op = db.query(LogicalAccount).filter(
        LogicalAccount.account_name == "main_operating"
    ).first()
    
    reserve = db.query(LogicalAccount).filter(
        LogicalAccount.account_name == "reserve_fund"
    ).first()
    
    # Record initial balances
    initial_main_balance = main_op.current_balance
    initial_reserve_balance = reserve.current_balance
    
    # Create and apply deposit
    deposit_amount = Decimal("100.00000000")
    parent_tx = LedgerTransaction(
        transaction_type="EXTERNAL_DEPOSIT",
        status="COMPLETED",
        amount=deposit_amount,
        to_account_id=main_op.id,
        description="Test deposit for balance update",
        performed_by="test_user"
    )
    
    db.add(parent_tx)
    db.commit()
    db.refresh(parent_tx)
    
    # Apply allocations
    engine = AllocationEngine(db)
    engine.apply_allocations(parent_tx.id)
    db.commit()
    
    # Refresh accounts
    db.refresh(main_op)
    db.refresh(reserve)
    
    # Verify balances updated correctly
    # main_operating should receive 50% and then distribute
    # After allocation, it should have initial + deposit - allocations_from_it
    # But the deposit goes TO main_operating first, then allocations split it
    
    # Actually, based on the allocation logic:
    # - Parent deposit goes to main_operating: +100
    # - Allocations split FROM main_operating: -100 total
    # - main_operating gets 50% allocation back: +50
    # Net for main_operating: +100 - 100 + 50 = +50
    
    # reserve gets 20%: +20
    expected_reserve_balance = initial_reserve_balance + Decimal("20.00000000")
    assert reserve.current_balance == expected_reserve_balance


def test_allocation_engine_is_idempotent(db: Session):
    """Test that allocation engine is idempotent - calling twice doesn't create duplicates"""
    # Get an account
    account = db.query(LogicalAccount).filter(
        LogicalAccount.account_name == "main_operating"
    ).first()
    
    # Create deposit
    parent_tx = LedgerTransaction(
        transaction_type="EXTERNAL_DEPOSIT",
        status="COMPLETED",
        amount=Decimal("100.00000000"),
        to_account_id=account.id,
        description="Idempotency test",
        performed_by="test_user"
    )
    
    db.add(parent_tx)
    db.commit()
    db.refresh(parent_tx)
    
    # Apply allocations first time
    engine = AllocationEngine(db)
    child_ids_1 = engine.apply_allocations(parent_tx.id)
    db.commit()
    
    # Apply allocations second time
    child_ids_2 = engine.apply_allocations(parent_tx.id)
    db.commit()
    
    # Should return the same children
    assert set(child_ids_1) == set(child_ids_2)
    assert len(child_ids_1) == 5
    
    # Verify no duplicate children in database
    all_children = db.query(LedgerTransaction).filter(
        LedgerTransaction.parent_transaction_id == parent_tx.id
    ).all()
    
    assert len(all_children) == 5, "Should have exactly 5 children, not duplicates"


def test_allocation_engine_rejects_non_external_deposit(db: Session):
    """Test that allocation engine rejects non-EXTERNAL_DEPOSIT transactions"""
    account = db.query(LogicalAccount).filter(
        LogicalAccount.account_name == "main_operating"
    ).first()
    
    # Create a PAYMENT transaction (not EXTERNAL_DEPOSIT)
    tx = LedgerTransaction(
        transaction_type="PAYMENT",
        status="COMPLETED",
        amount=Decimal("100.00000000"),
        from_account_id=account.id,
        to_account_id=account.id,
        description="Payment transaction",
        performed_by="test_user"
    )
    
    db.add(tx)
    db.commit()
    db.refresh(tx)
    
    # Try to apply allocations - should raise error
    engine = AllocationEngine(db)
    
    with pytest.raises(ValueError, match="must be EXTERNAL_DEPOSIT"):
        engine.apply_allocations(tx.id)


def test_allocation_engine_rejects_non_completed_status(db: Session):
    """Test that allocation engine rejects non-COMPLETED transactions"""
    account = db.query(LogicalAccount).filter(
        LogicalAccount.account_name == "main_operating"
    ).first()
    
    # Create a PENDING EXTERNAL_DEPOSIT
    tx = LedgerTransaction(
        transaction_type="EXTERNAL_DEPOSIT",
        status="PENDING",  # Not COMPLETED
        amount=Decimal("100.00000000"),
        to_account_id=account.id,
        description="Pending deposit",
        performed_by="test_user"
    )
    
    db.add(tx)
    db.commit()
    db.refresh(tx)
    
    # Try to apply allocations - should raise error
    engine = AllocationEngine(db)
    
    with pytest.raises(ValueError, match="must be COMPLETED"):
        engine.apply_allocations(tx.id)


def test_apply_allocations_for_transaction_convenience_function(db: Session):
    """Test the convenience function for applying allocations"""
    account = db.query(LogicalAccount).filter(
        LogicalAccount.account_name == "main_operating"
    ).first()
    
    parent_tx = LedgerTransaction(
        transaction_type="EXTERNAL_DEPOSIT",
        status="COMPLETED",
        amount=Decimal("100.00000000"),
        to_account_id=account.id,
        description="Convenience function test",
        performed_by="test_user"
    )
    
    db.add(parent_tx)
    db.commit()
    db.refresh(parent_tx)
    
    # Use convenience function
    child_ids = apply_allocations_for_transaction(
        db=db,
        transaction_id=parent_tx.id,
        performed_by="test_user"
    )
    db.commit()
    
    # Verify it worked
    assert len(child_ids) == 5
    
    children = db.query(LedgerTransaction).filter(
        LedgerTransaction.id.in_(child_ids)
    ).all()
    
    assert all(child.parent_transaction_id == parent_tx.id for child in children)
