"""Deterministic replay layer for 0G-aligned ledger systems.

Provides ``replay_batch`` for pure, replay-safe batch re-execution with
expected state root and receipt hash verification.
"""

from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, ConfigDict, Field

from src.ledger.executor import execute_batch
from src.ledger.transaction import SignedTransaction

# ---------------------------------------------------------------------------
# Failure reason constants
# ---------------------------------------------------------------------------

REASON_VALID: str = "valid"
REASON_FINAL_STATE_ROOT_MISMATCH: str = "final_state_root_mismatch"
REASON_RECEIPT_HASHES_MISMATCH: str = "receipt_hashes_mismatch"
REASON_EXECUTION_ERROR: str = "execution_error"


# ---------------------------------------------------------------------------
# Replay result model
# ---------------------------------------------------------------------------


class ReplayResult(BaseModel, frozen=True):
    """Immutable result of a deterministic batch replay.

    Attributes:
        is_valid: ``True`` if replay matches all expectations, ``False``
            otherwise.
        reason: Exact deterministic reason string.
        initial_state_root: State root before any transactions.
        final_state_root: State root after all transactions.
        receipt_hashes: Tuple of ``receipt_hash`` values from all receipts
            generated during replay.
        accepted_tx_ids: Tuple of transaction IDs that were accepted.
        rejected_tx_ids: Tuple of transaction IDs that were rejected.
    """

    is_valid: bool = Field(default=False)
    reason: str = Field(default=REASON_VALID)
    initial_state_root: str = Field(default="")
    final_state_root: str = Field(default="")
    receipt_hashes: Tuple[str, ...] = Field(default_factory=tuple)
    accepted_tx_ids: Tuple[str, ...] = Field(default_factory=tuple)
    rejected_tx_ids: Tuple[str, ...] = Field(default_factory=tuple)

    model_config = ConfigDict(frozen=True)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def replay_batch(
    initial_state: Dict[str, object],
    ordered_transactions: List[SignedTransaction],
    public_keys_by_sender: Dict[str, bytes],
    initial_nonces_by_sender: Dict[str, int],
    reducer_version: int,
    policy_hash: str,
    expected_final_state_root: Optional[str] = None,
    expected_receipt_hashes: Optional[Tuple[str, ...]] = None,
) -> ReplayResult:
    """Deterministically re-execute a batch of transactions, optionally
    verifying against expected state roots and receipt hashes.

    This function delegates to ``execute_batch`` and then compares the
    computed results against any provided expectations.

    Args:
        initial_state: The initial state dictionary.
        ordered_transactions: Ordered list of ``SignedTransaction`` objects.
        public_keys_by_sender: Mapping from sender address to public key.
        initial_nonces_by_sender: Mapping from sender address to initial
            nonce.
        reducer_version: Non-negative reducer version for receipts.
        policy_hash: Non-empty policy hash for receipts.
        expected_final_state_root: If provided, the replay will verify that
            the computed final state root matches this value.
        expected_receipt_hashes: If provided, the replay will verify that
            the computed receipt hash sequence matches this tuple.

    Returns:
        An immutable ``ReplayResult`` with verification outcome.
    """
    # --- Step 1: Execute batch ---
    try:
        batch_result = execute_batch(
            prior_state=initial_state,
            ordered_transactions=ordered_transactions,
            public_keys_by_sender=public_keys_by_sender,
            current_nonces_by_sender=initial_nonces_by_sender,
            reducer_version=reducer_version,
            policy_hash=policy_hash,
        )
    except Exception:
        return ReplayResult(
            is_valid=False,
            reason=REASON_EXECUTION_ERROR,
        )

    computed_final_state_root = batch_result.final_state_root
    computed_receipt_hashes = tuple(r.receipt_hash for r in batch_result.receipts)

    # --- Step 2: Verify expected final state root ---
    if expected_final_state_root is not None:
        if computed_final_state_root != expected_final_state_root:
            return ReplayResult(
                is_valid=False,
                reason=REASON_FINAL_STATE_ROOT_MISMATCH,
                initial_state_root=batch_result.initial_state_root,
                final_state_root=computed_final_state_root,
                receipt_hashes=computed_receipt_hashes,
                accepted_tx_ids=batch_result.accepted_tx_ids,
                rejected_tx_ids=batch_result.rejected_tx_ids,
            )

    # --- Step 3: Verify expected receipt hashes ---
    if expected_receipt_hashes is not None:
        if computed_receipt_hashes != expected_receipt_hashes:
            return ReplayResult(
                is_valid=False,
                reason=REASON_RECEIPT_HASHES_MISMATCH,
                initial_state_root=batch_result.initial_state_root,
                final_state_root=computed_final_state_root,
                receipt_hashes=computed_receipt_hashes,
                accepted_tx_ids=batch_result.accepted_tx_ids,
                rejected_tx_ids=batch_result.rejected_tx_ids,
            )

    # --- All checks passed ---
    return ReplayResult(
        is_valid=True,
        reason=REASON_VALID,
        initial_state_root=batch_result.initial_state_root,
        final_state_root=computed_final_state_root,
        receipt_hashes=computed_receipt_hashes,
        accepted_tx_ids=batch_result.accepted_tx_ids,
        rejected_tx_ids=batch_result.rejected_tx_ids,
    )