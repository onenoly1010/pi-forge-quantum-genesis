"""Canonical transaction layer — deterministic, replay-safe tests."""

import pytest
from pydantic import ValidationError

from src.ledger.transaction import (
    SignedTransaction,
    UnsignedTransaction,
    compute_transaction_id,
    create_unsigned_transaction,
    sign_transaction,
    transaction_to_signable_bytes,
    verify_transaction_signature,
)
from src.security.wallet import generate_keypair


# ======================================================================
# Test 1 — Deterministic tx_id Stability
# ======================================================================


class TestDeterministicTxId:
    """Identical unsigned payloads MUST generate identical tx_ids."""

    def test_identical_payloads_same_tx_id(self) -> None:
        utx1 = create_unsigned_transaction(
            sender="alice", nonce=1, epoch=2, action="transfer", payload={"amount": 100}
        )
        utx2 = create_unsigned_transaction(
            sender="alice", nonce=1, epoch=2, action="transfer", payload={"amount": 100}
        )
        tx_id1 = compute_transaction_id(utx1)
        tx_id2 = compute_transaction_id(utx2)
        assert tx_id1 == tx_id2

    def test_repeated_computation_same_tx_id(self) -> None:
        utx = create_unsigned_transaction(
            sender="bob", nonce=0, epoch=1, action="stake", payload={"value": 50}
        )
        ids = [compute_transaction_id(utx) for _ in range(100)]
        assert all(i == ids[0] for i in ids)

    def test_signed_tx_internal_tx_id_matches_unsigned(self) -> None:
        kp = generate_keypair()
        utx = create_unsigned_transaction(
            sender="charlie", nonce=5, epoch=3, action="vote", payload={"proposal": "p1"}
        )
        expected_id = compute_transaction_id(utx)
        stx = sign_transaction(utx, kp.private_key)
        assert stx.tx_id == expected_id


# ======================================================================
# Test 2 — Canonical Ordering Stability
# ======================================================================


class TestCanonicalOrderingStability:
    """Reordered payload dictionaries MUST generate same tx_id."""

    def test_reordered_payload_keys(self) -> None:
        utx1 = create_unsigned_transaction(
            sender="alice",
            nonce=1,
            epoch=0,
            action="transfer",
            payload={"b": 2, "a": 1},
        )
        utx2 = create_unsigned_transaction(
            sender="alice",
            nonce=1,
            epoch=0,
            action="transfer",
            payload={"a": 1, "b": 2},
        )
        assert compute_transaction_id(utx1) == compute_transaction_id(utx2)

    def test_reordered_nested_payload(self) -> None:
        utx1 = create_unsigned_transaction(
            sender="alice",
            nonce=1,
            epoch=0,
            action="test",
            payload={"nested": {"z": 26, "a": 1}, "top": True},
        )
        utx2 = create_unsigned_transaction(
            sender="alice",
            nonce=1,
            epoch=0,
            action="test",
            payload={"top": True, "nested": {"a": 1, "z": 26}},
        )
        assert compute_transaction_id(utx1) == compute_transaction_id(utx2)


# ======================================================================
# Test 3 — Signature Verification Success
# ======================================================================


class TestSignatureVerificationSuccess:
    """Valid signed transaction MUST verify True."""

    def test_valid_signature_verifies(self) -> None:
        kp = generate_keypair()
        utx = create_unsigned_transaction(
            sender="alice", nonce=1, epoch=0, action="transfer", payload={"value": 10}
        )
        stx = sign_transaction(utx, kp.private_key)
        assert verify_transaction_signature(stx, kp.public_key) is True

    def test_empty_payload_verifies(self) -> None:
        kp = generate_keypair()
        utx = create_unsigned_transaction(
            sender="bob", nonce=0, epoch=0, action="ping", payload={}
        )
        stx = sign_transaction(utx, kp.private_key)
        assert verify_transaction_signature(stx, kp.public_key) is True

    def test_multiple_transactions_all_verify(self) -> None:
        kp = generate_keypair()
        for i in range(10):
            utx = create_unsigned_transaction(
                sender="carol",
                nonce=i,
                epoch=0,
                action="tx",
                payload={"seq": i},
            )
            stx = sign_transaction(utx, kp.private_key)
            assert verify_transaction_signature(stx, kp.public_key) is True


# ======================================================================
# Test 4 — Signature Verification Failure
# ======================================================================


class TestSignatureVerificationFailure:
    """Modified payload MUST fail verification."""

    def test_different_sender_fails(self) -> None:
        kp = generate_keypair()
        utx = create_unsigned_transaction(
            sender="alice", nonce=1, epoch=0, action="transfer", payload={"value": 10}
        )
        stx = sign_transaction(utx, kp.private_key)
        # Construct a tampered SignedTransaction
        tampered = SignedTransaction(
            sender="bob",
            nonce=stx.nonce,
            epoch=stx.epoch,
            action=stx.action,
            payload=dict(stx.payload),
            signature=stx.signature,
        )
        assert verify_transaction_signature(tampered, kp.public_key) is False

    def test_different_nonce_fails(self) -> None:
        kp = generate_keypair()
        utx = create_unsigned_transaction(
            sender="alice", nonce=1, epoch=0, action="transfer", payload={"value": 10}
        )
        stx = sign_transaction(utx, kp.private_key)
        tampered = SignedTransaction(
            sender=stx.sender,
            nonce=999,
            epoch=stx.epoch,
            action=stx.action,
            payload=dict(stx.payload),
            signature=stx.signature,
        )
        assert verify_transaction_signature(tampered, kp.public_key) is False

    def test_different_payload_fails(self) -> None:
        kp = generate_keypair()
        utx = create_unsigned_transaction(
            sender="alice", nonce=1, epoch=0, action="transfer", payload={"value": 10}
        )
        stx = sign_transaction(utx, kp.private_key)
        tampered = SignedTransaction(
            sender=stx.sender,
            nonce=stx.nonce,
            epoch=stx.epoch,
            action=stx.action,
            payload={"value": 999},
            signature=stx.signature,
        )
        assert verify_transaction_signature(tampered, kp.public_key) is False

    def test_wrong_public_key_fails(self) -> None:
        kp1 = generate_keypair()
        kp2 = generate_keypair()
        utx = create_unsigned_transaction(
            sender="alice", nonce=1, epoch=0, action="transfer", payload={"value": 10}
        )
        stx = sign_transaction(utx, kp1.private_key)
        assert verify_transaction_signature(stx, kp2.public_key) is False


# ======================================================================
# Test 5 — tx_id Internal Derivation
# ======================================================================


class TestTxIdInternalDerivation:
    """Attempting external tx_id injection MUST fail (overridden)."""

    def test_tx_id_ignored_on_construction(self) -> None:
        """Any tx_id passed to SignedTransaction is overridden."""
        kp = generate_keypair()
        utx = create_unsigned_transaction(
            sender="alice", nonce=1, epoch=0, action="transfer", payload={"value": 10}
        )
        stx = sign_transaction(utx, kp.private_key)
        correct_id = stx.tx_id

        # Try to inject a different tx_id
        injected = SignedTransaction(
            tx_id="injected_id",
            sender="alice",
            nonce=1,
            epoch=0,
            action="transfer",
            payload={"value": 10},
            signature=stx.signature,
        )
        assert injected.tx_id != "injected_id"
        assert injected.tx_id == correct_id

    def test_tx_id_always_computed_from_fields(self) -> None:
        """tx_id is deterministic based on unsigned fields only."""
        kp = generate_keypair()
        stx1 = sign_transaction(
            create_unsigned_transaction(
                sender="alice", nonce=1, epoch=0, action="transfer", payload={"value": 10}
            ),
            kp.private_key,
        )
        stx2 = sign_transaction(
            create_unsigned_transaction(
                sender="alice", nonce=1, epoch=0, action="transfer", payload={"value": 10}
            ),
            kp.private_key,
        )
        # Same fields → same tx_id regardless of signature
        assert stx1.tx_id == stx2.tx_id

    def test_tx_id_differs_for_different_payloads(self) -> None:
        stx1 = create_unsigned_transaction(
            sender="a", nonce=0, epoch=0, action="x", payload={"v": 1}
        )
        stx2 = create_unsigned_transaction(
            sender="a", nonce=0, epoch=0, action="x", payload={"v": 2}
        )
        assert compute_transaction_id(stx1) != compute_transaction_id(stx2)


# ======================================================================
# Test 6 — Immutable Transaction Enforcement
# ======================================================================


class TestImmutableTransactionEnforcement:
    """Mutation attempts MUST raise exception."""

    def test_unsigned_transaction_frozen(self) -> None:
        utx = create_unsigned_transaction(
            sender="alice", nonce=1, epoch=0, action="transfer", payload={}
        )
        with pytest.raises(Exception):
            utx.sender = "bob"  # type: ignore

    def test_signed_transaction_frozen(self) -> None:
        kp = generate_keypair()
        utx = create_unsigned_transaction(
            sender="alice", nonce=1, epoch=0, action="transfer", payload={}
        )
        stx = sign_transaction(utx, kp.private_key)
        with pytest.raises(Exception):
            stx.sender = "bob"  # type: ignore

    def test_signed_transaction_tx_id_frozen(self) -> None:
        kp = generate_keypair()
        utx = create_unsigned_transaction(
            sender="alice", nonce=1, epoch=0, action="transfer", payload={}
        )
        stx = sign_transaction(utx, kp.private_key)
        with pytest.raises(Exception):
            stx.tx_id = "different"  # type: ignore

    def test_signed_transaction_signature_frozen(self) -> None:
        kp = generate_keypair()
        utx = create_unsigned_transaction(
            sender="alice", nonce=1, epoch=0, action="transfer", payload={}
        )
        stx = sign_transaction(utx, kp.private_key)
        with pytest.raises(Exception):
            stx.signature = "different"  # type: ignore


# ======================================================================
# Test 7 — Replay-Stable Signing
# ======================================================================


class TestReplayStableSigning:
    """Signing same transaction with same key MUST produce identical signature."""

    def test_repeated_signing_same_tx(self) -> None:
        kp = generate_keypair()
        utx = create_unsigned_transaction(
            sender="alice", nonce=1, epoch=0, action="transfer", payload={"value": 10}
        )
        sigs = [sign_transaction(utx, kp.private_key).signature for _ in range(50)]
        assert all(s == sigs[0] for s in sigs)

    def test_sign_identical_unsigned_different_instances(self) -> None:
        kp = generate_keypair()
        utx1 = create_unsigned_transaction(
            sender="alice", nonce=1, epoch=0, action="transfer", payload={"value": 10}
        )
        utx2 = create_unsigned_transaction(
            sender="alice", nonce=1, epoch=0, action="transfer", payload={"value": 10}
        )
        stx1 = sign_transaction(utx1, kp.private_key)
        stx2 = sign_transaction(utx2, kp.private_key)
        assert stx1.signature == stx2.signature

    def test_sign_after_export_import_key(self) -> None:
        kp = generate_keypair()
        utx = create_unsigned_transaction(
            sender="alice", nonce=1, epoch=0, action="transfer", payload={"value": 10}
        )
        from src.security.wallet import export_private_key, import_private_key

        priv_hex = export_private_key(kp.private_key)
        imported_sk = import_private_key(priv_hex)
        stx1 = sign_transaction(utx, kp.private_key)
        stx2 = sign_transaction(utx, imported_sk)
        assert stx1.signature == stx2.signature


# ======================================================================
# Test 8 — Signature Excluded From tx_id
# ======================================================================


class TestSignatureExcludedFromTxId:
    """Changing signature MUST NOT alter tx_id."""

    def test_different_signatures_same_tx_id(self) -> None:
        kp1 = generate_keypair()
        kp2 = generate_keypair()
        utx = create_unsigned_transaction(
            sender="alice", nonce=1, epoch=0, action="transfer", payload={"value": 10}
        )
        stx1 = sign_transaction(utx, kp1.private_key)
        stx2 = sign_transaction(utx, kp2.private_key)
        # Different keys produce different signatures but same tx_id
        assert stx1.signature != stx2.signature
        assert stx1.tx_id == stx2.tx_id

    def test_tx_id_matches_unsigned_id(self) -> None:
        kp = generate_keypair()
        utx = create_unsigned_transaction(
            sender="alice", nonce=1, epoch=0, action="transfer", payload={"value": 10}
        )
        unsigned_id = compute_transaction_id(utx)
        stx = sign_transaction(utx, kp.private_key)
        assert stx.tx_id == unsigned_id

    def test_manually_changed_signature_same_tx_id(self) -> None:
        kp = generate_keypair()
        utx = create_unsigned_transaction(
            sender="alice", nonce=1, epoch=0, action="transfer", payload={"value": 10}
        )
        stx = sign_transaction(utx, kp.private_key)
        original_tx_id = stx.tx_id
        # Construct with same unsigned fields but different signature
        stx2 = SignedTransaction(
            sender=stx.sender,
            nonce=stx.nonce,
            epoch=stx.epoch,
            action=stx.action,
            payload=dict(stx.payload),
            signature="ff" * 64,
        )
        assert stx2.tx_id == original_tx_id


# ======================================================================
# Test 9 — Invalid Nonce Rejection
# ======================================================================


class TestInvalidNonceRejection:
    """Negative nonce MUST raise validation error."""

    def test_negative_nonce_unsigned(self) -> None:
        with pytest.raises(ValidationError):
            create_unsigned_transaction(
                sender="alice", nonce=-1, epoch=0, action="transfer", payload={}
            )

    def test_negative_nonce_direct_model(self) -> None:
        with pytest.raises(ValidationError):
            UnsignedTransaction(sender="bob", nonce=-5, epoch=0, action="test", payload={})

    def test_negative_nonce_signed_model(self) -> None:
        with pytest.raises(ValidationError):
            SignedTransaction(
                sender="alice", nonce=-1, epoch=0, action="transfer", payload={}
            )


# ======================================================================
# Test 10 — Invalid Epoch Rejection
# ======================================================================


class TestInvalidEpochRejection:
    """Negative epoch MUST raise validation error."""

    def test_negative_epoch_unsigned(self) -> None:
        with pytest.raises(ValidationError):
            create_unsigned_transaction(
                sender="alice", nonce=0, epoch=-1, action="transfer", payload={}
            )

    def test_negative_epoch_direct_model(self) -> None:
        with pytest.raises(ValidationError):
            UnsignedTransaction(sender="bob", nonce=0, epoch=-5, action="test", payload={})

    def test_negative_epoch_signed_model(self) -> None:
        with pytest.raises(ValidationError):
            SignedTransaction(
                sender="alice", nonce=0, epoch=-1, action="transfer", payload={}
            )


# ======================================================================
# Test 11 — Empty Sender Rejection
# ======================================================================


class TestEmptySenderRejection:
    """Empty sender MUST fail validation."""

    def test_empty_sender_unsigned(self) -> None:
        with pytest.raises(ValidationError):
            create_unsigned_transaction(
                sender="", nonce=0, epoch=0, action="transfer", payload={}
            )

    def test_empty_sender_direct_model(self) -> None:
        with pytest.raises(ValidationError):
            UnsignedTransaction(sender="", nonce=0, epoch=0, action="test", payload={})

    def test_empty_sender_signed_model(self) -> None:
        with pytest.raises(ValidationError):
            SignedTransaction(sender="", nonce=0, epoch=0, action="transfer", payload={})


# ======================================================================
# Test 12 — Empty Action Rejection
# ======================================================================


class TestEmptyActionRejection:
    """Empty action MUST fail validation."""

    def test_empty_action_unsigned(self) -> None:
        with pytest.raises(ValidationError):
            create_unsigned_transaction(
                sender="alice", nonce=0, epoch=0, action="", payload={}
            )

    def test_empty_action_direct_model(self) -> None:
        with pytest.raises(ValidationError):
            UnsignedTransaction(sender="bob", nonce=0, epoch=0, action="", payload={})

    def test_empty_action_signed_model(self) -> None:
        with pytest.raises(ValidationError):
            SignedTransaction(sender="alice", nonce=0, epoch=0, action="", payload={})


# ======================================================================
# Test 13 — Deterministic Signable Bytes
# ======================================================================


class TestDeterministicSignableBytes:
    """Repeated signable-byte generation MUST produce identical bytes."""

    def test_repeated_signable_bytes(self) -> None:
        utx = create_unsigned_transaction(
            sender="alice", nonce=1, epoch=2, action="transfer", payload={"amount": 100}
        )
        results = [transaction_to_signable_bytes(utx) for _ in range(100)]
        assert all(r == results[0] for r in results)

    def test_signable_bytes_equivalent_unsigned(self) -> None:
        """Identical unsigned tx data must produce same signable bytes."""
        utx1 = create_unsigned_transaction(
            sender="alice", nonce=1, epoch=2, action="transfer", payload={"amount": 100}
        )
        utx2 = create_unsigned_transaction(
            sender="alice", nonce=1, epoch=2, action="transfer", payload={"amount": 100}
        )
        assert transaction_to_signable_bytes(utx1) == transaction_to_signable_bytes(utx2)

    def test_signable_bytes_reordered_payload(self) -> None:
        """Reordered payload keys must produce same signable bytes."""
        utx1 = create_unsigned_transaction(
            sender="alice",
            nonce=0,
            epoch=0,
            action="test",
            payload={"b": 2, "a": 1},
        )
        utx2 = create_unsigned_transaction(
            sender="alice",
            nonce=0,
            epoch=0,
            action="test",
            payload={"a": 1, "b": 2},
        )
        assert transaction_to_signable_bytes(utx1) == transaction_to_signable_bytes(utx2)


# ======================================================================
# Test 14 — Malformed Signature Handling
# ======================================================================


class TestMalformedSignatureHandling:
    """Malformed signature MUST safely return False."""

    def test_empty_signature(self) -> None:
        kp = generate_keypair()
        utx = create_unsigned_transaction(
            sender="alice", nonce=1, epoch=0, action="transfer", payload={}
        )
        stx = sign_transaction(utx, kp.private_key)
        # Create a version with empty signature
        bad = SignedTransaction(
            sender=stx.sender,
            nonce=stx.nonce,
            epoch=stx.epoch,
            action=stx.action,
            payload=dict(stx.payload),
            signature="",
        )
        assert verify_transaction_signature(bad, kp.public_key) is False

    def test_short_signature(self) -> None:
        kp = generate_keypair()
        utx = create_unsigned_transaction(
            sender="alice", nonce=1, epoch=0, action="transfer", payload={}
        )
        stx = sign_transaction(utx, kp.private_key)
        bad = SignedTransaction(
            sender=stx.sender,
            nonce=stx.nonce,
            epoch=stx.epoch,
            action=stx.action,
            payload=dict(stx.payload),
            signature="abcd",
        )
        assert verify_transaction_signature(bad, kp.public_key) is False

    def test_garbage_signature(self) -> None:
        kp = generate_keypair()
        utx = create_unsigned_transaction(
            sender="alice", nonce=1, epoch=0, action="transfer", payload={}
        )
        stx = sign_transaction(utx, kp.private_key)
        bad = SignedTransaction(
            sender=stx.sender,
            nonce=stx.nonce,
            epoch=stx.epoch,
            action=stx.action,
            payload=dict(stx.payload),
            signature="zzzz",
        )
        assert verify_transaction_signature(bad, kp.public_key) is False

    def test_signature_wrong_length(self) -> None:
        kp = generate_keypair()
        utx = create_unsigned_transaction(
            sender="alice", nonce=1, epoch=0, action="transfer", payload={}
        )
        stx = sign_transaction(utx, kp.private_key)
        # 64 hex chars = 32 bytes (wrong for Ed25519 which needs 64 bytes = 128 hex chars)
        bad = SignedTransaction(
            sender=stx.sender,
            nonce=stx.nonce,
            epoch=stx.epoch,
            action=stx.action,
            payload=dict(stx.payload),
            signature="ab" * 32,
        )
        assert verify_transaction_signature(bad, kp.public_key) is False


# ======================================================================
# Additional edge-case tests
# ======================================================================


class TestTransactionEdgeCases:
    """Additional edge cases for the transaction layer."""

    def test_signed_with_empty_payload(self) -> None:
        kp = generate_keypair()
        utx = create_unsigned_transaction(
            sender="alice", nonce=0, epoch=0, action="ping", payload={}
        )
        stx = sign_transaction(utx, kp.private_key)
        assert verify_transaction_signature(stx, kp.public_key) is True

    def test_signed_with_nested_payload(self) -> None:
        kp = generate_keypair()
        utx = create_unsigned_transaction(
            sender="bob",
            nonce=1,
            epoch=2,
            action="complex",
            payload={"items": [{"id": 1, "val": "a"}, {"id": 2, "val": "b"}], "meta": {"ver": 1}},
        )
        stx = sign_transaction(utx, kp.private_key)
        assert verify_transaction_signature(stx, kp.public_key) is True

    def test_non_dict_payload_rejected(self) -> None:
        with pytest.raises(ValidationError):
            UnsignedTransaction(
                sender="alice", nonce=0, epoch=0, action="test", payload="not-a-dict"  # type: ignore
            )

    def test_non_dict_payload_signed_rejected(self) -> None:
        with pytest.raises(ValidationError):
            SignedTransaction(
                sender="alice",
                nonce=0,
                epoch=0,
                action="test",
                payload="not-a-dict",  # type: ignore
            )

    def test_zero_nonce_and_epoch_allowed(self) -> None:
        utx = create_unsigned_transaction(
            sender="alice", nonce=0, epoch=0, action="genesis", payload={}
        )
        assert utx.nonce == 0
        assert utx.epoch == 0