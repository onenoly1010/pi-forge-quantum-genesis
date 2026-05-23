"""Deterministic receipt layer for 0G-aligned ledger systems.

Provides immutable receipt models with internally-derived receipt_hash,
canonical serialization, replay-safe determinism, and strict validation.
"""

from typing import Any, Dict

from pydantic import BaseModel, ConfigDict, Field, model_validator

from src.security.hashing import canonical_serialize, hash_receipt

# ---------------------------------------------------------------------------
# Receipt model — immutable, internally-derived receipt_hash
# ---------------------------------------------------------------------------


class Receipt(BaseModel, frozen=True):
    """A deterministic execution receipt with an internally-derived
    ``receipt_hash``.

    The ``receipt_hash`` is **never** user-supplied — it is always computed
    from the canonical serialisation of the receipt payload fields (excluding
    ``receipt_hash`` itself).  Attempting to set ``receipt_hash`` externally
    will be overridden.
    """

    tx_id: str = Field(..., min_length=1, description="Linked transaction ID (non-empty)")
    reducer_version: int = Field(..., ge=0, description="Reducer version (non-negative)")
    policy_hash: str = Field(..., min_length=1, description="Policy hash (non-empty)")
    state_root_before: str = Field(
        ..., min_length=1, description="State root before execution (non-empty)"
    )
    state_root_after: str = Field(
        ..., min_length=1, description="State root after execution (non-empty)"
    )
    execution_result: Dict[str, Any] = Field(
        default_factory=dict, description="Execution result payload (must be a dict)"
    )
    receipt_hash: str = Field(
        default="",
        description="Receipt hash — derived internally, never user-supplied",
    )

    model_config = ConfigDict(frozen=True, extra="forbid")

    @model_validator(mode="before")
    @classmethod
    def _compute_receipt_hash(cls, values: Any) -> Any:
        """Derive ``receipt_hash`` internally from the receipt payload.

        The ``receipt_hash`` field in the input is **ignored** — it is
        always recomputed from the canonical serialisation of the other
        receipt fields.
        """
        if isinstance(values, dict):
            # Validate execution_result is a dict
            exec_result = values.get("execution_result")
            if exec_result is not None and not isinstance(exec_result, dict):
                raise ValueError("execution_result must be a dictionary")

            # Build the receipt payload excluding receipt_hash
            payload: Dict[str, object] = {
                "tx_id": values.get("tx_id", ""),
                "reducer_version": values.get("reducer_version", 0),
                "policy_hash": values.get("policy_hash", ""),
                "state_root_before": values.get("state_root_before", ""),
                "state_root_after": values.get("state_root_after", ""),
                "execution_result": exec_result if exec_result is not None else {},
            }

            # Compute receipt_hash: sha256(b"RECEIPT:" + canonical_serialize(payload))
            receipt_hash = hash_receipt(payload)
            values["receipt_hash"] = receipt_hash
        return values


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def create_receipt(
    transaction: "SignedTransaction",  # type: ignore[name-defined]
    reducer_version: int,
    policy_hash: str,
    state_root_before: str,
    state_root_after: str,
    execution_result: Dict[str, object],
) -> "Receipt":
    """Create a fully-validated ``Receipt`` from a signed transaction and
    execution outputs.

    Args:
        transaction: The ``SignedTransaction`` to link this receipt to.
        reducer_version: Non-negative reducer version.
        policy_hash: Non-empty policy hash string.
        state_root_before: Non-empty state root before execution.
        state_root_after: Non-empty state root after execution.
        execution_result: Arbitrary JSON-compatible dict.

    Returns:
        A validated ``Receipt`` with internally-derived ``receipt_hash``.

    Raises:
        ValueError: If any validation constraint is violated.
    """
    return Receipt(
        tx_id=transaction.tx_id,
        reducer_version=reducer_version,
        policy_hash=policy_hash,
        state_root_before=state_root_before,
        state_root_after=state_root_after,
        execution_result=execution_result,
    )


def compute_receipt_hash(receipt_payload: Dict[str, object]) -> str:
    """Compute the deterministic ``receipt_hash`` for a receipt payload.

    The payload is a dictionary containing the receipt fields (excluding
    ``receipt_hash``).  The hash is computed as:

        receipt_hash = hash_receipt(canonical_serialize(payload))

    ``hash_receipt`` applies ``sha256(b"RECEIPT:" + canonical_serialize(...))``,
    providing domain separation at the receipt level.
    """
    return hash_receipt(receipt_payload)


def receipt_to_canonical_bytes(receipt: "Receipt") -> bytes:
    """Return the canonical serialisation bytes for *receipt*.

    The receipt is serialised deterministically — platform-independent,
    replay-stable, and suitable for storage or transmission.
    """
    return canonical_serialize(receipt.model_dump())