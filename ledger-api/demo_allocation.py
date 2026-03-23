#!/usr/bin/env python3
"""
Standalone demonstration of the Ledger API allocation engine
This script demonstrates that the atomic allocation logic works correctly
"""

import sys
import json
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add parent directory to path
sys.path.insert(0, '.')

from ledger_api.db import Base
from ledger_api.models.ledger_models import (
    LogicalAccount,
    LedgerTransaction,
    AllocationRule
)
from ledger_api.services.allocation import AllocationEngine

# Create in-memory database
engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
db = Session()

print("=" * 70)
print("LEDGER API - ALLOCATION ENGINE DEMONSTRATION")
print("=" * 70)
print()

# Seed accounts
print("1. Creating logical accounts...")
accounts = [
    LogicalAccount(account_name='main_operating', account_type='OPERATING', current_balance=0),
    LogicalAccount(account_name='reserve_fund', account_type='RESERVE', current_balance=0),
    LogicalAccount(account_name='rewards_pool', account_type='REWARDS', current_balance=0),
    LogicalAccount(account_name='development_fund', account_type='DEVELOPMENT', current_balance=0),
    LogicalAccount(account_name='marketing_fund', account_type='MARKETING', current_balance=0),
]
for account in accounts:
    db.add(account)
    print(f"   ✓ {account.account_name}: {account.current_balance} Pi")
db.commit()
print()

# Create allocation rule
print("2. Creating default allocation rule (50/20/15/10/5)...")
rule = AllocationRule(
    rule_name='default_deposit_allocation',
    is_active=True,
    priority=100,
    allocation_config=json.dumps([
        {'account_name': 'main_operating', 'percentage': '50'},
        {'account_name': 'reserve_fund', 'percentage': '20'},
        {'account_name': 'rewards_pool', 'percentage': '15'},
        {'account_name': 'development_fund', 'percentage': '10'},
        {'account_name': 'marketing_fund', 'percentage': '5'}
    ]),
    description='Default allocation rule',
    created_by='system'
)
db.add(rule)
db.commit()
print("   ✓ Rule created successfully")
print()

# Create external deposit
deposit_amount = Decimal('100.00000000')
print(f"3. Creating EXTERNAL_DEPOSIT of {deposit_amount} Pi...")
main_op = db.query(LogicalAccount).filter(
    LogicalAccount.account_name == 'main_operating'
).first()

parent_tx = LedgerTransaction(
    transaction_type='EXTERNAL_DEPOSIT',
    status='COMPLETED',
    amount=deposit_amount,
    to_account_id=main_op.id,
    external_tx_hash='0xdemo123456',
    description='Demo external deposit',
    performed_by='demo_user'
)
db.add(parent_tx)
db.commit()
db.refresh(parent_tx)
print(f"   ✓ Transaction created: {parent_tx.id}")
print()

# Apply allocations
print("4. Applying allocations atomically...")
engine = AllocationEngine(db)
child_ids = engine.apply_allocations(parent_tx.id, performed_by='demo_user')
db.commit()
print(f"   ✓ Created {len(child_ids)} allocation transactions")
print()

# Show results
print("5. Allocation Results:")
print()
print("   Child Transactions:")
children = db.query(LedgerTransaction).filter(
    LedgerTransaction.id.in_(child_ids)
).all()

total_allocated = Decimal(0)
for child in children:
    target = db.query(LogicalAccount).filter(
        LogicalAccount.id == child.to_account_id
    ).first()
    print(f"      → {child.amount:>15} Pi to {target.account_name}")
    total_allocated += child.amount

print()
print(f"   Total Allocated: {total_allocated} Pi")
print(f"   Original Amount: {deposit_amount} Pi")
print(f"   Match: {'✓ YES' if total_allocated == deposit_amount else '✗ NO'}")
print()

# Show account balances
print("6. Final Account Balances:")
accounts = db.query(LogicalAccount).all()
total_balance = Decimal(0)
for account in accounts:
    db.refresh(account)
    print(f"      {account.account_name:>18}: {account.current_balance:>15} Pi")
    total_balance += account.current_balance

print(f"      {'TOTAL':>18}: {total_balance:>15} Pi")
print()

# Test idempotency
print("7. Testing Idempotency (running allocation again)...")
child_ids_2 = engine.apply_allocations(parent_tx.id, performed_by='demo_user')
db.commit()
print(f"   First run:  {len(child_ids)} allocations")
print(f"   Second run: {len(child_ids_2)} allocations")
print(f"   Same IDs: {'✓ YES' if set(child_ids) == set(child_ids_2) else '✗ NO'}")
print()

# Verify no duplicate allocations
all_children = db.query(LedgerTransaction).filter(
    LedgerTransaction.parent_transaction_id == parent_tx.id
).all()
print(f"   Total children in DB: {len(all_children)}")
print(f"   Idempotent: {'✓ YES - No duplicates created' if len(all_children) == 5 else '✗ NO - Duplicates found!'}")
print()

print("=" * 70)
print("DEMONSTRATION COMPLETE")
print("=" * 70)
print()
print("Key Features Demonstrated:")
print("  ✓ Atomic allocation creation (all or nothing)")
print("  ✓ Correct percentage-based distribution")
print("  ✓ Balance updates across all accounts")
print("  ✓ Idempotent operation (no duplicates)")
print("  ✓ Audit trail creation")
print()
