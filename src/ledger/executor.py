"""Deterministic executor layer for 0G-aligned ledger systems.

Provides ``execute_batch`` for pure, replay-safe batch transaction execution
with validation gates, state reduction, receipt generation, and nonce tracking.
"""

import copy
from typing import Any, Dict, List, Tuple

from pydantic import BaseModel, ConfigDict, Field

from src.ledger.receipts import Receipt, create_receipt
from src.ledger.reducer import reduce_state
from src.ledger.transaction import SignedTransaction
from src.ledger.validator import validate_transaction
from src.snapshots.state_root import derive_state_root

# ---------------------------------------------------------------------------
# Execution batch result model
# ---------------------------------------------------------------------------


class ExecutionBatchResult(BaseModel, frozen=True):
    """Immutable result of a deterministic batch execution.

    Attributes:
        initial_state_root: State root before any transactions were applied.
        final_state_root: State root after all transactions were applied.
        final_state: The final state dictionary after execution.
        receipts: Tuple of ``Receipt`` objects for accepted transactions.
        accepted_tx_ids: Tuple of transaction IDs that were accepted.
        rejected_tx_ids: Tuple of transaction IDs that were rejected.
    """

    initial_state_root: str = Field(
        description="State root before batch execution"
    )
    final_state_root: str = Field(
        description="State root after batch execution"
    )
    final_state: Dict[str, Any] = Field(
        description="Final state after all reductions"
    )
    receipts: Tuple[Receipt, ...] = Field(
        default_factory=tuple, description="Receipts for accepted transactions"
    )
    accepted_tx_ids: Tuple[str, ...] = Field(
        default_factory=tuple, description="Accepted transaction IDs"
    )
    rejected_tx_ids: Tuple[str, ...] = Field(
        default_factory=tuple, description="Rejected transaction IDs"
    )

    model_config = ConfigDict(frozen=True)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def execute_batch(
    prior_state: Dict[str, object],
    ordered_transactions: List[SignedTransaction],
    public_keys_by_sender: Dict[str, bytes],
    current_nonces_by_sender: Dict[str, int],
    reducer_version: int,
    policy_hash: str,
) -> ExecutionBatchResult:
    """Deterministically execute a batch of ordered transactions.

    For each transaction:
    1. Look up the sender's public key (reject if missing).
    2. Look up the sender's current nonce (default to 0 if missing).
    3. Validate the transaction via ``validate_transaction``.
    4. If valid: reduce state using ``transaction.action`` and
       ``transaction.payload``, derive state roots, generate a receipt,
       and advance the nonce for subsequent transactions in the batch.
    5. If invalid: reject without mutating state or generating a receipt.

    Args:
        prior_state: The initial state dictionary.
        ordered_transactions: Ordered list of ``SignedTransaction`` objects.
        public_keys_by_sender: Mapping from sender address (str) to 32-byte
            Ed25519 public key (bytes).
        current_nonces_by_sender: Mapping from sender address (str) to current
            nonce (int).  Missing senders default to 0.
        reducer_version: Non-negative reducer version for receipts.
        policy_hash: Non-empty policy hash string for receipts.

    Returns:
        An immutable ``ExecutionBatchResult`` with final state, roots, and
        receipts.  All fields are deterministic and replay-safe.
    """
    state: Dict[str, object] = copy.deepcopy(prior_state)
    nonces: Dict[str, int] = dict(current_nonces_by_sender)
    accepted_tx_ids: List[str] = []
    rejected_tx_ids: List[str] = []
    receipts_list: List[Receipt] = []

    initial_state_root = derive_state_root(prior_state)

    for tx in ordered_transactions:
        sender = tx.sender

        # --- Step 1: Look up public key (reject if missing) ---
        public_key = public_keys_by_sender.get(sender)
        if public_key is None:
            rejected_tx_ids.append(tx.tx_id)
            continue

        # --- Step 2: Look up current nonce (default 0) ---
        current_nonce = nonces.get(sender, 0)

        # --- Step 3: Validate transaction ---
        validation_result = validate_transaction(tx, public_key, current_nonce)
        if not validation_result.is_valid:
            rejected_tx_ids.append(tx.tx_id)
            continue

        # --- Step 4: Derive state root before reduction ---
        state_root_before = derive_state_root(state)

        # --- Step 5: Apply reducer ---
        try:
            state = reduce_state(state, tx.action, dict(tx.payload))
        except (ValueError, TypeError):
            rejected_tx_ids.append(tx.tx_id)
            continue

        # --- Step 6: Derive state root after reduction ---
        state_root_after = derive_state_root(state)

        # --- Step 7: Generate receipt ---
        try:
            receipt = create_receipt(
                transaction=tx,
                reducer_version=reducer_version,
                policy_hash=policy_hash,
                state_root_before=state_root_before,
                state_root_after=state_root_after,
                execution_result={
                    "status": "accepted",
                    "action": tx.action,
                },
            )
        except Exception:
            rejected_tx_ids.append(tx.tx_id)
            continue

        # --- Step 8: Accept transaction, advance nonce ---
        accepted_tx_ids.append(tx.tx_id)
        receipts_list.append(receipt)
        nonces[sender] = current_nonce + 1

    final_state_root = derive_state_root(state)

    return ExecutionBatchResult(
        initial_state_root=initial_state_root,
        final_state_root=final_state_root,
        final_state=state,
        receipts=tuple(receipts_list),
        accepted_tx_ids=tuple(accepted_tx_ids),
        rejected_tx_ids=tuple(rejected_tx_ids),
    )