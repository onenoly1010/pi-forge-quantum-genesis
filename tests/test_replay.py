"""Deterministic replay layer — pure, replay-safe tests."""

import pytest

from src.ledger.executor import execute_batch
from src.ledger.replay import (
    REASON_EXECUTION_ERROR,
    REASON_FINAL_STATE_ROOT_MISMATCH,
    REASON_RECEIPT_HASHES_MISMATCH,
    REASON_VALID,
    ReplayResult,
    replay_batch,
)
from nacl.signing import SigningKey

from src.ledger.transaction import (
    SignedTransaction,
    create_unsigned_transaction,
    sign_transaction,
)
from src.snapshots.state_root import derive_state_root
from src.security.wallet import KeyPair, derive_address, generate_keypair


def _make_signed_tx(
    kp=None,
    sender: str | None = None,
    nonce: int = 1,
    epoch: int = 0,
    action: str = "state.set",
    payload: dict | None = None,
) -> SignedTransaction:
    """Helper: create and sign a transaction."""
    if kp is None:
        kp = generate_keypair()
    elif isinstance(kp, (bytes, bytearray)):
        signing_key = SigningKey(bytes(kp))
        kp = KeyPair(private_key=bytes(kp), public_key=bytes(signing_key.verify_key))
    elif not hasattr(kp, "private_key") or not hasattr(kp, "public_key"):
        raise TypeError("kp must be a KeyPair or a 32-byte private key seed")

    sender_addr = sender if sender else derive_address(kp.public_key)
    utx = create_unsigned_transaction(
        sender=sender_addr,
        nonce=nonce,
        epoch=epoch,
        action=action,
        payload=payload or {"key": "x", "value": 1},
    )
    return sign_transaction(utx, kp.private_key)


def _valid_replay_params():
    """Return (state, txs, pks, nonces, rv, ph)."""
    kp = generate_keypair()
    sender = derive_address(kp.public_key)
    tx1 = _make_signed_tx(kp=kp, sender=sender, nonce=1, action="state.set",
                          payload={"key": "a", "value": 1})
    tx2 = _make_signed_tx(kp=kp, sender=sender, nonce=2, action="counter.increment",
                          payload={"key": "c", "amount": 5})
    initial_state: dict = {}
    pks = {sender: kp.public_key}
    nonces = {sender: 0}
    return initial_state, [tx1, tx2], pks, nonces, 1, "policy_abc"


# ======================================================================
# Test 1 — Valid Replay Passes
# ======================================================================


class TestValidReplayPasses:
    """A valid replay MUST pass without expectations."""

    def test_valid_replay_no_expectations(self) -> None:
        state, txs, pks, nonces, rv, ph = _valid_replay_params()
        result = replay_batch(state, txs, pks, nonces, rv, ph)
        assert result.is_valid is True
        assert result.reason == REASON_VALID

    def test_valid_replay_with_correct_root(self) -> None:
        state, txs, pks, nonces, rv, ph = _valid_replay_params()
        expected_root = execute_batch(state, txs, pks, nonces, rv, ph).final_state_root
        result = replay_batch(state, txs, pks, nonces, rv, ph,
                              expected_final_state_root=expected_root)
        assert result.is_valid is True
        assert result.reason == REASON_VALID

    def test_valid_replay_with_correct_receipt_hashes(self) -> None:
        state, txs, pks, nonces, rv, ph = _valid_replay_params()
        batch_result = execute_batch(state, txs, pks, nonces, rv, ph)
        expected_hashes = tuple(r.receipt_hash for r in batch_result.receipts)
        result = replay_batch(state, txs, pks, nonces, rv, ph,
                              expected_receipt_hashes=expected_hashes)
        assert result.is_valid is True
        assert result.reason == REASON_VALID

    def test_valid_replay_with_both_expectations(self) -> None:
        state, txs, pks, nonces, rv, ph = _valid_replay_params()
        batch_result = execute_batch(state, txs, pks, nonces, rv, ph)
        result = replay_batch(
            state, txs, pks, nonces, rv, ph,
            expected_final_state_root=batch_result.final_state_root,
            expected_receipt_hashes=tuple(r.receipt_hash for r in batch_result.receipts),
        )
        assert result.is_valid is True
        assert result.reason == REASON_VALID


# ======================================================================
# Test 2 — Replay Returns Deterministic Final Root
# ======================================================================


class TestDeterministicFinalRoot:
    """Replay MUST return a deterministic final state root."""

    def test_repeated_replay_same_root(self) -> None:
        state, txs, pks, nonces, rv, ph = _valid_replay_params()
        results = [replay_batch(state, txs, pks, nonces, rv, ph) for _ in range(50)]
        assert all(r.final_state_root == results[0].final_state_root for r in results)

    def test_root_matches_executed(self) -> None:
        state, txs, pks, nonces, rv, ph = _valid_replay_params()
        batch_result = execute_batch(state, txs, pks, nonces, rv, ph)
        result = replay_batch(state, txs, pks, nonces, rv, ph)
        assert result.final_state_root == batch_result.final_state_root


# ======================================================================
# Test 3 — Replay Returns Deterministic Receipt Hashes
# ======================================================================


class TestDeterministicReceiptHashes:
    """Replay MUST return deterministic receipt hashes."""

    def test_repeated_replay_same_hashes(self) -> None:
        state, txs, pks, nonces, rv, ph = _valid_replay_params()
        results = [replay_batch(state, txs, pks, nonces, rv, ph) for _ in range(50)]
        assert all(r.receipt_hashes == results[0].receipt_hashes for r in results)


# ======================================================================
# Test 4 — Final State Root Mismatch Fails
# ======================================================================


class TestFinalStateRootMismatch:
    """Wrong expected root MUST fail with correct reason."""

    def test_wrong_root(self) -> None:
        state, txs, pks, nonces, rv, ph = _valid_replay_params()
        wrong_root = "0" * 64
        result = replay_batch(state, txs, pks, nonces, rv, ph,
                              expected_final_state_root=wrong_root)
        assert result.is_valid is False
        assert result.reason == REASON_FINAL_STATE_ROOT_MISMATCH

    def test_reason_string_exact(self) -> None:
        state, txs, pks, nonces, rv, ph = _valid_replay_params()
        result = replay_batch(state, txs, pks, nonces, rv, ph,
                              expected_final_state_root="x" * 64)
        assert result.reason == "final_state_root_mismatch"


# ======================================================================
# Test 5 — Receipt Hashes Mismatch Fails
# ======================================================================


class TestReceiptHashesMismatch:
    """Wrong expected receipt hashes MUST fail with correct reason."""

    def test_wrong_hashes(self) -> None:
        state, txs, pks, nonces, rv, ph = _valid_replay_params()
        result = replay_batch(state, txs, pks, nonces, rv, ph,
                              expected_receipt_hashes=("x" * 64,))
        assert result.is_valid is False
        assert result.reason == REASON_RECEIPT_HASHES_MISMATCH

    def test_empty_hashes_when_expected(self) -> None:
        state, txs, pks, nonces, rv, ph = _valid_replay_params()
        # There are 2 receipts, but we expect 0
        result = replay_batch(state, txs, pks, nonces, rv, ph,
                              expected_receipt_hashes=())
        assert result.is_valid is False
        assert result.reason == REASON_RECEIPT_HASHES_MISMATCH

    def test_reason_string_exact(self) -> None:
        state, txs, pks, nonces, rv, ph = _valid_replay_params()
        result = replay_batch(state, txs, pks, nonces, rv, ph,
                              expected_receipt_hashes=("bad",))
        assert result.reason == "receipt_hashes_mismatch"


# ======================================================================
# Test 6 — Repeated Replay Produces Identical Result
# ======================================================================


class TestRepeatedReplayDeterministic:
    """Repeated replay MUST produce identical results."""

    def test_repeated_50_times(self) -> None:
        state, txs, pks, nonces, rv, ph = _valid_replay_params()
        batch_result = execute_batch(state, txs, pks, nonces, rv, ph)
        expected_root = batch_result.final_state_root
        expected_hashes = tuple(r.receipt_hash for r in batch_result.receipts)

        results = [
            replay_batch(state, txs, pks, nonces, rv, ph,
                         expected_final_state_root=expected_root,
                         expected_receipt_hashes=expected_hashes)
            for _ in range(50)
        ]
        assert all(
            r.is_valid == results[0].is_valid
            and r.reason == results[0].reason
            and r.final_state_root == results[0].final_state_root
            and r.receipt_hashes == results[0].receipt_hashes
            for r in results
        )


# ======================================================================
# Test 7 — Replay Preserves Accepted Tx IDs
# ======================================================================


class TestPreservesAcceptedTxIds:
    """Replay MUST preserve accepted transaction IDs."""

    def test_accepted_ids_match_executor(self) -> None:
        state, txs, pks, nonces, rv, ph = _valid_replay_params()
        batch_result = execute_batch(state, txs, pks, nonces, rv, ph)
        result = replay_batch(state, txs, pks, nonces, rv, ph)
        assert result.accepted_tx_ids == batch_result.accepted_tx_ids
        assert len(result.accepted_tx_ids) == 2


# ======================================================================
# Test 8 — Replay Preserves Rejected Tx IDs
# ======================================================================


class TestPreservesRejectedTxIds:
    """Replay MUST preserve rejected transaction IDs."""

    def test_rejected_ids_match_executor(self) -> None:
        kp = generate_keypair()
        kp_other = generate_keypair()
        sender = derive_address(kp.public_key)

        tx_valid = _make_signed_tx(kp=kp, sender=sender, nonce=1, action="state.set",
                                   payload={"key": "a", "value": 1})
        tx_invalid = _make_signed_tx(kp=kp_other, sender=sender, nonce=2,
                                     action="state.set", payload={"key": "b", "value": 2})

        state: dict = {}
        pks = {sender: kp.public_key}
        batch_result = execute_batch(state, [tx_valid, tx_invalid], pks, {sender: 0}, 1, "p")
        result = replay_batch(state, [tx_valid, tx_invalid], pks, {sender: 0}, 1, "p")
        assert result.rejected_tx_ids == batch_result.rejected_tx_ids
        assert len(result.rejected_tx_ids) == 1
        assert result.accepted_tx_ids == batch_result.accepted_tx_ids
        assert len(result.accepted_tx_ids) == 1


# ======================================================================
# Test 9 — Replay Does Not Mutate Initial State
# ======================================================================


class TestNoMutateInitialState:
    """Replay MUST NOT mutate initial_state."""

    def test_state_unchanged(self) -> None:
        state, txs, pks, nonces, rv, ph = _valid_replay_params()
        state_copy = dict(state)
        _ = replay_batch(state, txs, pks, nonces, rv, ph)
        assert state == state_copy


# ======================================================================
# Test 10 — Replay Does Not Mutate Transactions
# ======================================================================


class TestNoMutateTransactions:
    """Replay MUST NOT mutate ordered_transactions."""

    def test_tx_list_unchanged(self) -> None:
        state, txs, pks, nonces, rv, ph = _valid_replay_params()
        original_ids = [t.tx_id for t in txs]
        _ = replay_batch(state, txs, pks, nonces, rv, ph)
        assert [t.tx_id for t in txs] == original_ids


# ======================================================================
# Test 11 — Replay Does Not Mutate Public Key Map
# ======================================================================


class TestNoMutatePublicKeyMap:
    """Replay MUST NOT mutate public_keys_by_sender."""

    def test_pks_unchanged(self) -> None:
        state, txs, pks, nonces, rv, ph = _valid_replay_params()
        pks_copy = dict(pks)
        _ = replay_batch(state, txs, pks, nonces, rv, ph)
        assert pks == pks_copy


# ======================================================================
# Test 12 — Replay Does Not Mutate Nonce Map
# ======================================================================


class TestNoMutateNonceMap:
    """Replay MUST NOT mutate initial_nonces_by_sender."""

    def test_nonces_unchanged(self) -> None:
        state, txs, pks, nonces, rv, ph = _valid_replay_params()
        nonces_copy = dict(nonces)
        _ = replay_batch(state, txs, pks, nonces, rv, ph)
        assert nonces == nonces_copy


# ======================================================================
# Test 13 — Empty Batch Replay Is Valid
# ======================================================================


class TestEmptyBatchReplay:
    """An empty batch replay MUST be valid."""

    def test_empty_batch_valid(self) -> None:
        result = replay_batch({"a": 1}, [], {}, {}, 1, "p")
        assert result.is_valid is True
        assert result.reason == REASON_VALID
        assert len(result.accepted_tx_ids) == 0
        assert len(result.rejected_tx_ids) == 0
        assert len(result.receipt_hashes) == 0

    def test_empty_batch_with_correct_root(self) -> None:
        root = derive_state_root({"a": 1})
        result = replay_batch({"a": 1}, [], {}, {}, 1, "p",
                              expected_final_state_root=root)
        assert result.is_valid is True

    def test_empty_batch_with_wrong_root(self) -> None:
        result = replay_batch({"a": 1}, [], {}, {}, 1, "p",
                              expected_final_state_root="x" * 64)
        assert result.is_valid is False
        assert result.reason == REASON_FINAL_STATE_ROOT_MISMATCH


# ======================================================================
# Test 14 — ReplayResult Is Immutable
# ======================================================================


class TestReplayResultImmutable:
    """ReplayResult MUST be immutable."""

    def test_fields_frozen(self) -> None:
        result = ReplayResult(
            is_valid=True,
            reason="valid",
            initial_state_root="a",
            final_state_root="b",
            receipt_hashes=(),
            accepted_tx_ids=(),
            rejected_tx_ids=(),
        )
        with pytest.raises(Exception):
            result.is_valid = False  # type: ignore

    def test_tuples_frozen(self) -> None:
        result = ReplayResult(
            is_valid=True,
            reason="valid",
            initial_state_root="a",
            final_state_root="b",
            receipt_hashes=("abc",),
            accepted_tx_ids=("def",),
            rejected_tx_ids=(),
        )
        with pytest.raises(Exception):
            result.accepted_tx_ids = ("xyz",)  # type: ignore


# ======================================================================
# Test 15 — Exact Reason Strings Are Enforced
# ======================================================================


class TestExactReasonStrings:
    """Each failure condition MUST return its exact reason string."""

    def test_valid_reason(self) -> None:
        state, txs, pks, nonces, rv, ph = _valid_replay_params()
        result = replay_batch(state, txs, pks, nonces, rv, ph)
        assert result.reason == "valid"
        assert result.reason == REASON_VALID

    def test_final_state_root_mismatch_reason(self) -> None:
        state, txs, pks, nonces, rv, ph = _valid_replay_params()
        result = replay_batch(state, txs, pks, nonces, rv, ph,
                              expected_final_state_root="x" * 64)
        assert result.reason == "final_state_root_mismatch"
        assert result.reason == REASON_FINAL_STATE_ROOT_MISMATCH

    def test_receipt_hashes_mismatch_reason(self) -> None:
        state, txs, pks, nonces, rv, ph = _valid_replay_params()
        result = replay_batch(state, txs, pks, nonces, rv, ph,
                              expected_receipt_hashes=("bad",))
        assert result.reason == "receipt_hashes_mismatch"
        assert result.reason == REASON_RECEIPT_HASHES_MISMATCH


# ======================================================================
# Additional edge cases
# ======================================================================


class TestReplayEdgeCases:
    """Additional edge cases for replay."""

    def test_multi_sender_replay(self) -> None:
        kp1 = generate_keypair()
        kp2 = generate_keypair()
        s1 = derive_address(kp1.public_key)
        s2 = derive_address(kp2.public_key)

        tx1 = _make_signed_tx(kp=kp1, sender=s1, nonce=1, action="state.set",
                              payload={"key": "a", "value": 1})
        tx2 = _make_signed_tx(kp=kp2, sender=s2, nonce=1, action="state.set",
                              payload={"key": "b", "value": 2})

        state: dict = {}
        pks = {s1: kp1.public_key, s2: kp2.public_key}
        nonces = {s1: 0, s2: 0}

        batch_result = execute_batch(state, [tx1, tx2], pks, nonces, 1, "p")
        result = replay_batch(state, [tx1, tx2], pks, nonces, 1, "p",
                              expected_final_state_root=batch_result.final_state_root,
                              expected_receipt_hashes=tuple(
                                  r.receipt_hash for r in batch_result.receipts
                              ))
        assert result.is_valid is True
        assert result.reason == REASON_VALID
        assert len(result.accepted_tx_ids) == 2

    def test_replay_with_rejected_tx(self) -> None:
        kp = generate_keypair()
        kp_other = generate_keypair()
        sender = derive_address(kp.public_key)

        tx_valid = _make_signed_tx(kp=kp, sender=sender, nonce=1, action="state.set",
                                   payload={"key": "a", "value": 1})
        tx_invalid = _make_signed_tx(kp=kp_other, sender=sender, nonce=2,
                                     action="state.set", payload={"key": "b", "value": 2})

        state: dict = {}
        pks = {sender: kp.public_key}

        batch_result = execute_batch(state, [tx_valid, tx_invalid], pks, {sender: 0}, 1, "p")
        result = replay_batch(state, [tx_valid, tx_invalid], pks, {sender: 0}, 1, "p",
                              expected_final_state_root=batch_result.final_state_root,
                              expected_receipt_hashes=tuple(
                                  r.receipt_hash for r in batch_result.receipts
                              ))
        assert result.is_valid is True
        assert len(result.accepted_tx_ids) == 1
        assert len(result.rejected_tx_ids) == 1