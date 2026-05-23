"""Deterministic validator layer for 0G-aligned ledger systems.

Provides ``validate_transaction`` and the ``ValidationResult`` model for
pure, replay-safe transaction validation without side-effects.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from src.ledger.transaction import (
    SignedTransaction,
    UnsignedTransaction,
    compute_transaction_id,
    transaction_to_signable_bytes,
)
from src.security.wallet import derive_address, verify_signature

# ---------------------------------------------------------------------------
# Failure reason constants — exact strings required by specification
# ---------------------------------------------------------------------------

REASON_VALID: str = "valid"
REASON_INVALID_TRANSACTION_TYPE: str = "invalid_transaction_type"
REASON_INVALID_CURRENT_NONCE: str = "invalid_current_nonce"
REASON_TX_ID_MISMATCH: str = "tx_id_mismatch"
REASON_INVALID_SIGNATURE: str = "invalid_signature"
REASON_NONCE_MISMATCH: str = "nonce_mismatch"
REASON_SENDER_MISMATCH: str = "sender_mismatch"
REASON_SERIALIZATION_ERROR: str = "serialization_error"


# ---------------------------------------------------------------------------
# Validation result model
# ---------------------------------------------------------------------------


class ValidationResult(BaseModel, frozen=True):
    """Immutable result of a deterministic transaction validation.

    Attributes:
        is_valid: ``True`` if all checks pass, ``False`` otherwise.
        reason: Exact deterministic reason string.
        tx_id: The transaction ID of the validated transaction.
    """

    is_valid: bool = Field(default=False)
    reason: str = Field(default=REASON_VALID)
    tx_id: str = Field(default="")

    model_config = ConfigDict(frozen=True)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def validate_transaction(
    transaction: "SignedTransaction",
    public_key: bytes,
    current_nonce: int,
) -> "ValidationResult":
    """Deterministically validate a ``SignedTransaction``.

    Performs the following checks in order:
    1. Transaction object type
    2. Non-negative ``current_nonce``
    3. Nonce rule: ``transaction.nonce == current_nonce + 1``
    4. Sender / public-key binding: ``derive_address(public_key) == sender``
    5. ``tx_id`` recomputation from unsigned fields
    6. Ed25519 signature verification

    Args:
        transaction: The signed transaction to validate.
        public_key: 32-byte Ed25519 public key of the purported sender.
        current_nonce: The current nonce of the sender's account.

    Returns:
        A ``ValidationResult`` with ``is_valid``, ``reason``, and ``tx_id``.
        All fields are deterministic and replay-safe.
    """
    # --- Check 1: Transaction object type ---
    if not isinstance(transaction, SignedTransaction):
        return ValidationResult(
            is_valid=False,
            reason=REASON_INVALID_TRANSACTION_TYPE,
            tx_id="",
        )

    tx_id = transaction.tx_id

    # --- Check 2: Non-negative current_nonce ---
    if not isinstance(current_nonce, int) or isinstance(current_nonce, bool) or current_nonce < 0:
        return ValidationResult(
            is_valid=False,
            reason=REASON_INVALID_CURRENT_NONCE,
            tx_id=tx_id,
        )

    # --- Check 3: Nonce correctness ---
    if transaction.nonce != current_nonce + 1:
        return ValidationResult(
            is_valid=False,
            reason=REASON_NONCE_MISMATCH,
            tx_id=tx_id,
        )

    # --- Check 4: Sender / public-key binding ---
    derived_address = derive_address(public_key)
    if transaction.sender != derived_address:
        return ValidationResult(
            is_valid=False,
            reason=REASON_SENDER_MISMATCH,
            tx_id=tx_id,
        )

    # --- Check 5: tx_id recomputation ---
    try:
        unsigned = UnsignedTransaction(
            sender=transaction.sender,
            nonce=transaction.nonce,
            epoch=transaction.epoch,
            action=transaction.action,
            payload=dict(transaction.payload),
        )
        expected_tx_id = compute_transaction_id(unsigned)
    except Exception:
        return ValidationResult(
            is_valid=False,
            reason=REASON_SERIALIZATION_ERROR,
            tx_id=tx_id,
        )

    if tx_id != expected_tx_id:
        return ValidationResult(
            is_valid=False,
            reason=REASON_TX_ID_MISMATCH,
            tx_id=tx_id,
        )

    # --- Check 6: Signature verification ---
    try:
        signable = transaction_to_signable_bytes(unsigned)
    except Exception:
        return ValidationResult(
            is_valid=False,
            reason=REASON_SERIALIZATION_ERROR,
            tx_id=tx_id,
        )

    if not verify_signature(public_key, signable, transaction.signature):
        return ValidationResult(
            is_valid=False,
            reason=REASON_INVALID_SIGNATURE,
            tx_id=tx_id,
        )

    # --- All checks passed ---
    return ValidationResult(
        is_valid=True,
        reason=REASON_VALID,
        tx_id=tx_id,
    )