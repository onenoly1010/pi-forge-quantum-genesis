"""Canonical transaction layer for 0G-aligned deterministic ledger systems.

Provides immutable Pydantic models for transaction payloads, unsigned and
signed transactions, with deterministic tx_id derivation, Ed25519 signing,
and replay-safe verification.
"""

from typing import Any, Dict

from pydantic import BaseModel, ConfigDict, Field, model_validator

from src.security.hashing import canonical_serialize, hash_transaction
from src.security.wallet import verify_signature

# ---------------------------------------------------------------------------
# Data models — immutable, fully typed, replay-safe
# ---------------------------------------------------------------------------


class TransactionPayload(BaseModel, frozen=True):
    """Arbitrary payload container for transaction data.

    The payload is stored as a JSON-compatible dictionary and serialized
    via ``canonical_serialize`` for deterministic hashing and signing.
    """

    data: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(frozen=True)


class UnsignedTransaction(BaseModel, frozen=True):
    """An unsigned transaction with no signature attached.

    Fields are immutable.  Validation rejects negative nonces/epochs and
    empty sender/action strings.
    """

    sender: str = Field(..., min_length=1, description="Sender address (lowercase hex)")
    nonce: int = Field(..., ge=0, description="Nonce — must be non-negative")
    epoch: int = Field(..., ge=0, description="Epoch — must be non-negative")
    action: str = Field(..., min_length=1, description="Transaction action type")
    payload: Dict[str, Any] = Field(
        default_factory=dict, description="Arbitrary JSON-compatible payload"
    )

    model_config = ConfigDict(frozen=True, extra="forbid")

    @model_validator(mode="before")
    @classmethod
    def _validate_payload_is_dict(cls, values: Any) -> Any:
        """Ensure payload is a dict.  Non-dict payloads are rejected."""
        if isinstance(values, dict):
            payload = values.get("payload", {})
            if payload is not None and not isinstance(payload, dict):
                raise ValueError("payload must be a dictionary")
        return values


class SignedTransaction(BaseModel, frozen=True):
    """A fully signed transaction with an internally-derived tx_id.

    The ``tx_id`` is **never** user-supplied — it is always computed from
    the canonically-serialised unsigned payload via ``hash_transaction``.
    Attempting to set ``tx_id`` externally will be overridden.
    """

    tx_id: str = Field(
        default="",
        description="Transaction ID — derived internally, never user-supplied",
    )
    sender: str = Field(..., min_length=1)
    nonce: int = Field(..., ge=0)
    epoch: int = Field(..., ge=0)
    action: str = Field(..., min_length=1)
    payload: Dict[str, Any] = Field(default_factory=dict)
    signature: str = Field(default="", description="Hex-encoded Ed25519 detached signature")

    model_config = ConfigDict(frozen=True, extra="forbid")

    @model_validator(mode="before")
    @classmethod
    def _compute_tx_id(cls, values: Any) -> Any:
        """Derive ``tx_id`` internally from the unsigned payload.

        The ``tx_id`` field in the input is **ignored** — it is always
        recomputed from the canonical serialisation of the unsigned
        transaction fields.
        """
        if isinstance(values, dict):
            # Build the unsigned payload dict (exclude tx_id and signature)
            unsigned = {
                "sender": values.get("sender", ""),
                "nonce": values.get("nonce", 0),
                "epoch": values.get("epoch", 0),
                "action": values.get("action", ""),
                "payload": values.get("payload", {}),
            }
            # Validate payload is a dict
            payload = values.get("payload")
            if payload is not None and not isinstance(payload, dict):
                raise ValueError("payload must be a dictionary")
            # Compute tx_id from canonical serialization + domain hash
            tx_id = compute_transaction_id(
                UnsignedTransaction(**unsigned)  # type: ignore[arg-type]
            )
            values["tx_id"] = tx_id
        return values


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def create_unsigned_transaction(
    sender: str,
    nonce: int,
    epoch: int,
    action: str,
    payload: Dict[str, object],
) -> UnsignedTransaction:
    """Create an ``UnsignedTransaction`` with validation.

    Args:
        sender: Sender address (lowercase hex, non-empty).
        nonce: Nonce (must be >= 0).
        epoch: Epoch (must be >= 0).
        action: Action type (non-empty).
        payload: Arbitrary JSON-compatible payload (must be a dict).

    Returns:
        A validated ``UnsignedTransaction``.

    Raises:
        ValueError: If any validation constraint is violated.
    """
    return UnsignedTransaction(
        sender=sender, nonce=nonce, epoch=epoch, action=action, payload=payload
    )


def transaction_to_signable_bytes(transaction: UnsignedTransaction) -> bytes:
    """Return the canonical bytes to be signed for *transaction*.

    The signable bytes are the canonical serialisation of the unsigned
    transaction — deterministic, platform-independent, and replay-stable.
    """
    model_dict = transaction.model_dump()
    return canonical_serialize(model_dict)


def compute_transaction_id(transaction: UnsignedTransaction) -> str:
    """Compute the deterministic ``tx_id`` for an ``UnsignedTransaction``.

    Derivation:
        tx_id = hash_transaction(canonical_serialize(unsigned_payload))

    ``hash_transaction`` applies ``sha256(b"TX:" + canonical_serialize(...))``,
    providing domain separation at the transaction level.
    """
    signable = transaction_to_signable_bytes(transaction)
    # hash_transaction accepts Any and internally canonical-serializes,
    # but we already have canonical bytes.  We feed the unsigned dict.
    return hash_transaction(transaction.model_dump())


def sign_transaction(
    transaction: UnsignedTransaction,
    private_key: bytes,
) -> SignedTransaction:
    """Sign an ``UnsignedTransaction``, returning a ``SignedTransaction``.

    The signature is an Ed25519 detached signature over the canonical
    serialisation bytes.  The ``tx_id`` is internally derived.

    Args:
        transaction: The unsigned transaction to sign.
        private_key: 32-byte Ed25519 private key seed.

    Returns:
        A ``SignedTransaction`` including the internally-derived ``tx_id``
        and the hex-encoded signature.
    """
    from src.security.wallet import sign_message as _sign_message

    signable = transaction_to_signable_bytes(transaction)
    signature = _sign_message(private_key, signable)

    model_dict = transaction.model_dump()
    return SignedTransaction(**model_dict, signature=signature)  # type: ignore[arg-type]


def verify_transaction_signature(
    transaction: SignedTransaction,
    public_key: bytes,
) -> bool:
    """Verify the Ed25519 signature on a ``SignedTransaction``.

    The verification reconstructs the unsigned canonical bytes from the
    signed transaction (excluding signature) and checks the detached
    signature against the provided *public_key*.

    Args:
        transaction: The signed transaction to verify.
        public_key: 32-byte Ed25519 public key.

    Returns:
        ``True`` if the signature is valid, ``False`` otherwise.
    """
    unsigned = UnsignedTransaction(
        sender=transaction.sender,
        nonce=transaction.nonce,
        epoch=transaction.epoch,
        action=transaction.action,
        payload=dict(transaction.payload),
    )
    signable = transaction_to_signable_bytes(unsigned)
    return verify_signature(public_key, signable, transaction.signature)