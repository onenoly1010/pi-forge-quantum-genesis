"""Deterministic receipt layer — replay-safe, immutable tests."""

import pytest
from pydantic import ValidationError

from src.ledger.receipts import (
    Receipt,
    compute_receipt_hash,
    create_receipt,
    receipt_to_canonical_bytes,
)
from src.ledger.transaction import (
    SignedTransaction,
    create_unsigned_transaction,
    sign_transaction,
)
from src.security.wallet import generate_keypair


def _make_signed_tx(
    sender: str = "alice",
    nonce: int = 1,
    epoch: int = 0,
    action: str = "transfer",
    payload: dict | None = None,
) -> SignedTransaction:
    """Helper: create and sign a transaction for testing."""
    kp = generate_keypair()
    utx = create_unsigned_transaction(
        sender=sender,
        nonce=nonce,
        epoch=epoch,
        action=action,
        payload=payload or {"value": 10},
    )
    return sign_transaction(utx, kp.private_key)


# ======================================================================
# Test 1 — Deterministic receipt_hash Stability
# ======================================================================


class TestDeterministicReceiptHash:
    """Identical receipt payloads MUST produce identical receipt_hash."""

    def test_identical_receipts_same_hash(self) -> None:
        tx = _make_signed_tx()
        r1 = create_receipt(
            transaction=tx,
            reducer_version=1,
            policy_hash="policy123",
            state_root_before="root_a",
            state_root_after="root_b",
            execution_result={"status": "ok", "gas_used": 100},
        )
        r2 = create_receipt(
            transaction=tx,
            reducer_version=1,
            policy_hash="policy123",
            state_root_before="root_a",
            state_root_after="root_b",
            execution_result={"status": "ok", "gas_used": 100},
        )
        assert r1.receipt_hash == r2.receipt_hash

    def test_repeated_computation_same_hash(self) -> None:
        tx = _make_signed_tx()
        receipt = create_receipt(
            transaction=tx,
            reducer_version=2,
            policy_hash="p_hash",
            state_root_before="root_x",
            state_root_after="root_y",
            execution_result={"result": "success"},
        )
        hashes = [compute_receipt_hash({
            "tx_id": receipt.tx_id,
            "reducer_version": receipt.reducer_version,
            "policy_hash": receipt.policy_hash,
            "state_root_before": receipt.state_root_before,
            "state_root_after": receipt.state_root_after,
            "execution_result": dict(receipt.execution_result),
        }) for _ in range(100)]
        assert all(h == hashes[0] for h in hashes)

    def test_receipt_hash_matches_computed(self) -> None:
        tx = _make_signed_tx()
        receipt = create_receipt(
            transaction=tx,
            reducer_version=1,
            policy_hash="abc",
            state_root_before="s1",
            state_root_after="s2",
            execution_result={"ok": True},
        )
        payload = {
            "tx_id": receipt.tx_id,
            "reducer_version": receipt.reducer_version,
            "policy_hash": receipt.policy_hash,
            "state_root_before": receipt.state_root_before,
            "state_root_after": receipt.state_root_after,
            "execution_result": dict(receipt.execution_result),
        }
        assert receipt.receipt_hash == compute_receipt_hash(payload)


# ======================================================================
# Test 2 — Canonical Ordering Stability
# ======================================================================


class TestCanonicalOrderingStability:
    """Reordered execution_result dictionaries MUST hash identically."""

    def test_reordered_execution_result(self) -> None:
        tx = _make_signed_tx()
        r1 = create_receipt(
            transaction=tx,
            reducer_version=1,
            policy_hash="p1",
            state_root_before="a",
            state_root_after="b",
            execution_result={"b": 2, "a": 1},
        )
        r2 = create_receipt(
            transaction=tx,
            reducer_version=1,
            policy_hash="p1",
            state_root_before="a",
            state_root_after="b",
            execution_result={"a": 1, "b": 2},
        )
        assert r1.receipt_hash == r2.receipt_hash

    def test_reordered_nested_execution_result(self) -> None:
        tx = _make_signed_tx()
        r1 = create_receipt(
            transaction=tx,
            reducer_version=1,
            policy_hash="p1",
            state_root_before="a",
            state_root_after="b",
            execution_result={"nested": {"z": 26, "a": 1}, "top": True},
        )
        r2 = create_receipt(
            transaction=tx,
            reducer_version=1,
            policy_hash="p1",
            state_root_before="a",
            state_root_after="b",
            execution_result={"top": True, "nested": {"a": 1, "z": 26}},
        )
        assert r1.receipt_hash == r2.receipt_hash


# ======================================================================
# Test 3 — Immutable Receipt Enforcement
# ======================================================================


class TestImmutableReceiptEnforcement:
    """Mutation attempts MUST fail."""

    def test_tx_id_frozen(self) -> None:
        tx = _make_signed_tx()
        receipt = create_receipt(
            transaction=tx,
            reducer_version=1,
            policy_hash="p",
            state_root_before="a",
            state_root_after="b",
            execution_result={},
        )
        with pytest.raises(Exception):
            receipt.tx_id = "different"  # type: ignore

    def test_receipt_hash_frozen(self) -> None:
        tx = _make_signed_tx()
        receipt = create_receipt(
            transaction=tx,
            reducer_version=1,
            policy_hash="p",
            state_root_before="a",
            state_root_after="b",
            execution_result={},
        )
        with pytest.raises(Exception):
            receipt.receipt_hash = "different"  # type: ignore

    def test_execution_result_frozen(self) -> None:
        tx = _make_signed_tx()
        receipt = create_receipt(
            transaction=tx,
            reducer_version=1,
            policy_hash="p",
            state_root_before="a",
            state_root_after="b",
            execution_result={},
        )
        with pytest.raises(Exception):
            receipt.execution_result = {"x": 1}  # type: ignore

    def test_state_root_after_frozen(self) -> None:
        tx = _make_signed_tx()
        receipt = create_receipt(
            transaction=tx,
            reducer_version=1,
            policy_hash="p",
            state_root_before="a",
            state_root_after="b",
            execution_result={},
        )
        with pytest.raises(Exception):
            receipt.state_root_after = "c"  # type: ignore


# ======================================================================
# Test 4 — receipt_hash Internal Derivation
# ======================================================================


class TestReceiptHashInternalDerivation:
    """External receipt_hash injection MUST fail (overridden)."""

    def test_receipt_hash_ignored_on_construction(self) -> None:
        tx = _make_signed_tx()
        # Construct a receipt where we know the correct hash
        correct_receipt = create_receipt(
            transaction=tx,
            reducer_version=1,
            policy_hash="p",
            state_root_before="a",
            state_root_after="b",
            execution_result={"k": "v"},
        )
        # Try to inject a different receipt_hash
        injected = Receipt(
            receipt_hash="injected_hash",
            tx_id=tx.tx_id,
            reducer_version=1,
            policy_hash="p",
            state_root_before="a",
            state_root_after="b",
            execution_result={"k": "v"},
        )
        assert injected.receipt_hash != "injected_hash"
        assert injected.receipt_hash == correct_receipt.receipt_hash

    def test_receipt_hash_always_computed_from_fields(self) -> None:
        tx = _make_signed_tx()
        r1 = create_receipt(
            transaction=tx,
            reducer_version=1,
            policy_hash="p",
            state_root_before="a",
            state_root_after="b",
            execution_result={"k": "v"},
        )
        r2 = create_receipt(
            transaction=tx,
            reducer_version=1,
            policy_hash="p",
            state_root_before="a",
            state_root_after="b",
            execution_result={"k": "v"},
        )
        assert r1.receipt_hash == r2.receipt_hash

    def test_different_fields_different_hash(self) -> None:
        tx = _make_signed_tx()
        r1 = create_receipt(
            transaction=tx,
            reducer_version=1,
            policy_hash="p1",
            state_root_before="a",
            state_root_after="b",
            execution_result={},
        )
        r2 = create_receipt(
            transaction=tx,
            reducer_version=1,
            policy_hash="p2",
            state_root_before="a",
            state_root_after="b",
            execution_result={},
        )
        assert r1.receipt_hash != r2.receipt_hash


# ======================================================================
# Test 5 — Replay Stability
# ======================================================================


class TestReplayStability:
    """Repeated receipt generation MUST produce identical hashes."""

    def test_repeated_create_same_params(self) -> None:
        tx = _make_signed_tx()
        receipts = [
            create_receipt(
                transaction=tx,
                reducer_version=1,
                policy_hash="p",
                state_root_before="a",
                state_root_after="b",
                execution_result={"x": 1},
            )
            for _ in range(50)
        ]
        assert all(r.receipt_hash == receipts[0].receipt_hash for r in receipts)

    def test_repeated_canonical_bytes(self) -> None:
        tx = _make_signed_tx()
        receipt = create_receipt(
            transaction=tx,
            reducer_version=1,
            policy_hash="p",
            state_root_before="a",
            state_root_after="b",
            execution_result={"x": 1},
        )
        serialized = receipt_to_canonical_bytes(receipt)
        results = [receipt_to_canonical_bytes(receipt) for _ in range(100)]
        assert all(r == serialized for r in results)


# ======================================================================
# Test 6 — Canonical Byte Stability
# ======================================================================


class TestCanonicalByteStability:
    """Repeated canonical serialization MUST produce identical bytes."""

    def test_repeated_serialize_same_receipt(self) -> None:
        tx = _make_signed_tx()
        receipt = create_receipt(
            transaction=tx,
            reducer_version=1,
            policy_hash="p",
            state_root_before="a",
            state_root_after="b",
            execution_result={"k": "v"},
        )
        results = [receipt_to_canonical_bytes(receipt) for _ in range(100)]
        assert all(r == results[0] for r in results)

    def test_serialize_identical_receipts(self) -> None:
        tx = _make_signed_tx()
        r1 = create_receipt(
            transaction=tx,
            reducer_version=1,
            policy_hash="p",
            state_root_before="a",
            state_root_after="b",
            execution_result={"k": "v"},
        )
        r2 = create_receipt(
            transaction=tx,
            reducer_version=1,
            policy_hash="p",
            state_root_before="a",
            state_root_after="b",
            execution_result={"k": "v"},
        )
        assert receipt_to_canonical_bytes(r1) == receipt_to_canonical_bytes(r2)


# ======================================================================
# Test 7 — Invalid reducer_version Rejection
# ======================================================================


class TestInvalidReducerVersionRejection:
    """Negative reducer_version MUST fail validation."""

    def test_negative_reducer_version_direct(self) -> None:
        tx = _make_signed_tx()
        with pytest.raises(ValidationError):
            Receipt(
                tx_id=tx.tx_id,
                reducer_version=-1,
                policy_hash="p",
                state_root_before="a",
                state_root_after="b",
                execution_result={},
            )

    def test_negative_reducer_version_create(self) -> None:
        tx = _make_signed_tx()
        with pytest.raises(ValidationError):
            create_receipt(
                transaction=tx,
                reducer_version=-1,
                policy_hash="p",
                state_root_before="a",
                state_root_after="b",
                execution_result={},
            )


# ======================================================================
# Test 8 — Empty tx_id Rejection
# ======================================================================


class TestEmptyTxIdRejection:
    """Empty tx_id MUST fail validation."""

    def test_empty_tx_id_direct(self) -> None:
        with pytest.raises(ValidationError):
            Receipt(
                tx_id="",
                reducer_version=0,
                policy_hash="p",
                state_root_before="a",
                state_root_after="b",
                execution_result={},
            )

    def test_empty_tx_id_create(self) -> None:
        # Create a transaction with a tx_id, then override via Receipt directly
        with pytest.raises(ValidationError):
            Receipt(
                tx_id="",
                reducer_version=0,
                policy_hash="p",
                state_root_before="a",
                state_root_after="b",
                execution_result={},
            )


# ======================================================================
# Test 9 — Empty policy_hash Rejection
# ======================================================================


class TestEmptyPolicyHashRejection:
    """Empty policy_hash MUST fail validation."""

    def test_empty_policy_hash_direct(self) -> None:
        tx = _make_signed_tx()
        with pytest.raises(ValidationError):
            Receipt(
                tx_id=tx.tx_id,
                reducer_version=0,
                policy_hash="",
                state_root_before="a",
                state_root_after="b",
                execution_result={},
            )

    def test_empty_policy_hash_create(self) -> None:
        tx = _make_signed_tx()
        with pytest.raises(ValidationError):
            create_receipt(
                transaction=tx,
                reducer_version=0,
                policy_hash="",
                state_root_before="a",
                state_root_after="b",
                execution_result={},
            )


# ======================================================================
# Test 10 — Empty state roots Rejection
# ======================================================================


class TestEmptyStateRootsRejection:
    """Empty state_root_before/state_root_after MUST fail validation."""

    def test_empty_state_root_before(self) -> None:
        tx = _make_signed_tx()
        with pytest.raises(ValidationError):
            Receipt(
                tx_id=tx.tx_id,
                reducer_version=0,
                policy_hash="p",
                state_root_before="",
                state_root_after="b",
                execution_result={},
            )

    def test_empty_state_root_after(self) -> None:
        tx = _make_signed_tx()
        with pytest.raises(ValidationError):
            Receipt(
                tx_id=tx.tx_id,
                reducer_version=0,
                policy_hash="p",
                state_root_before="a",
                state_root_after="",
                execution_result={},
            )

    def test_both_state_roots_empty(self) -> None:
        tx = _make_signed_tx()
        with pytest.raises(ValidationError):
            Receipt(
                tx_id=tx.tx_id,
                reducer_version=0,
                policy_hash="p",
                state_root_before="",
                state_root_after="",
                execution_result={},
            )


# ======================================================================
# Test 11 — Invalid execution_result Rejection
# ======================================================================


class TestInvalidExecutionResultRejection:
    """Non-dict execution_result MUST fail validation."""

    def test_execution_result_string(self) -> None:
        tx = _make_signed_tx()
        with pytest.raises(ValidationError):
            Receipt(
                tx_id=tx.tx_id,
                reducer_version=0,
                policy_hash="p",
                state_root_before="a",
                state_root_after="b",
                execution_result="not-a-dict",  # type: ignore
            )

    def test_execution_result_list(self) -> None:
        tx = _make_signed_tx()
        with pytest.raises(ValidationError):
            Receipt(
                tx_id=tx.tx_id,
                reducer_version=0,
                policy_hash="p",
                state_root_before="a",
                state_root_after="b",
                execution_result=[1, 2, 3],  # type: ignore
            )

    def test_execution_result_none_rejected(self) -> None:
        tx = _make_signed_tx()
        with pytest.raises(ValidationError):
            Receipt(
                tx_id=tx.tx_id,
                reducer_version=0,
                policy_hash="p",
                state_root_before="a",
                state_root_after="b",
                execution_result=None,  # type: ignore
            )


# ======================================================================
# Test 12 — receipt_hash Determinism Across Copies
# ======================================================================


class TestReceiptHashDeterminismAcrossCopies:
    """Copied identical receipt payloads MUST preserve exact receipt_hash."""

    def test_copy_identical_payload(self) -> None:
        tx = _make_signed_tx()
        original = create_receipt(
            transaction=tx,
            reducer_version=1,
            policy_hash="p",
            state_root_before="a",
            state_root_after="b",
            execution_result={"data": 42},
        )
        # Reconstruct with same data
        duplicate = create_receipt(
            transaction=tx,
            reducer_version=1,
            policy_hash="p",
            state_root_before="a",
            state_root_after="b",
            execution_result={"data": 42},
        )
        assert original.receipt_hash == duplicate.receipt_hash

    def test_model_dump_preserves_hash(self) -> None:
        tx = _make_signed_tx()
        receipt = create_receipt(
            transaction=tx,
            reducer_version=1,
            policy_hash="p",
            state_root_before="a",
            state_root_after="b",
            execution_result={"data": 42},
        )
        # model_dump() includes receipt_hash
        dumped = receipt.model_dump()
        assert isinstance(dumped, dict)
        assert "receipt_hash" in dumped
        assert dumped["receipt_hash"] == receipt.receipt_hash


# ======================================================================
# Test 13 — receipt_hash Changes On State Transition Change
# ======================================================================


class TestReceiptHashChangesOnStateChange:
    """Changing state_root_after MUST change receipt_hash."""

    def test_different_state_root_after(self) -> None:
        tx = _make_signed_tx()
        r1 = create_receipt(
            transaction=tx,
            reducer_version=1,
            policy_hash="p",
            state_root_before="a",
            state_root_after="b",
            execution_result={},
        )
        r2 = create_receipt(
            transaction=tx,
            reducer_version=1,
            policy_hash="p",
            state_root_before="a",
            state_root_after="c",
            execution_result={},
        )
        assert r1.receipt_hash != r2.receipt_hash

    def test_different_state_root_before(self) -> None:
        tx = _make_signed_tx()
        r1 = create_receipt(
            transaction=tx,
            reducer_version=1,
            policy_hash="p",
            state_root_before="a",
            state_root_after="b",
            execution_result={},
        )
        r2 = create_receipt(
            transaction=tx,
            reducer_version=1,
            policy_hash="p",
            state_root_before="x",
            state_root_after="b",
            execution_result={},
        )
        assert r1.receipt_hash != r2.receipt_hash


# ======================================================================
# Test 14 — receipt_hash Changes On Policy Change
# ======================================================================


class TestReceiptHashChangesOnPolicyChange:
    """Changing policy_hash MUST change receipt_hash."""

    def test_different_policy_hash(self) -> None:
        tx = _make_signed_tx()
        r1 = create_receipt(
            transaction=tx,
            reducer_version=1,
            policy_hash="policy_a",
            state_root_before="a",
            state_root_after="b",
            execution_result={},
        )
        r2 = create_receipt(
            transaction=tx,
            reducer_version=1,
            policy_hash="policy_b",
            state_root_before="a",
            state_root_after="b",
            execution_result={},
        )
        assert r1.receipt_hash != r2.receipt_hash


# ======================================================================
# Test 15 — tx_id Link Integrity
# ======================================================================


class TestTxIdLinkIntegrity:
    """Receipt tx_id MUST exactly match source transaction tx_id."""

    def test_receipt_tx_id_matches_transaction(self) -> None:
        tx = _make_signed_tx()
        receipt = create_receipt(
            transaction=tx,
            reducer_version=1,
            policy_hash="p",
            state_root_before="a",
            state_root_after="b",
            execution_result={},
        )
        assert receipt.tx_id == tx.tx_id

    def test_multiple_receipts_link_correctly(self) -> None:
        tx1 = _make_signed_tx(sender="alice", nonce=1)
        tx2 = _make_signed_tx(sender="bob", nonce=2)

        r1 = create_receipt(
            transaction=tx1,
            reducer_version=1,
            policy_hash="p1",
            state_root_before="a",
            state_root_after="b",
            execution_result={},
        )
        r2 = create_receipt(
            transaction=tx2,
            reducer_version=1,
            policy_hash="p1",
            state_root_before="a",
            state_root_after="b",
            execution_result={},
        )
        assert r1.tx_id == tx1.tx_id
        assert r2.tx_id == tx2.tx_id
        assert r1.tx_id != r2.tx_id

    def test_different_transactions_different_hashes(self) -> None:
        tx1 = _make_signed_tx(sender="carol", nonce=1)
        tx2 = _make_signed_tx(sender="carol", nonce=2)

        r1 = create_receipt(
            transaction=tx1,
            reducer_version=1,
            policy_hash="p",
            state_root_before="a",
            state_root_after="b",
            execution_result={},
        )
        r2 = create_receipt(
            transaction=tx2,
            reducer_version=1,
            policy_hash="p",
            state_root_before="a",
            state_root_after="b",
            execution_result={},
        )
        assert r1.tx_id != r2.tx_id
        # Different tx_ids, same other fields → different receipt_hashes
        assert r1.receipt_hash != r2.receipt_hash