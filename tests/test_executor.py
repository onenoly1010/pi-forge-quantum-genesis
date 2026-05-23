"""Deterministic executor layer — pure, replay-safe batch execution tests."""

import pytest

from src.ledger.executor import ExecutionBatchResult, execute_batch
from src.ledger.transaction import (
    SignedTransaction,
    create_unsigned_transaction,
    sign_transaction,
)
from src.snapshots.state_root import derive_state_root
from src.security.wallet import derive_address, generate_keypair


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
    sender_addr = sender if sender else derive_address(kp.public_key)
    utx = create_unsigned_transaction(
        sender=sender_addr,
        nonce=nonce,
        epoch=epoch,
        action=action,
        payload=payload or {"key": "x", "value": 1},
    )
    return sign_transaction(utx, kp.private_key)


# ======================================================================
# Helper: valid batch fixture
# ======================================================================


def _valid_batch_params():
    """Return (prior_state, transactions, pks, nonces, reducer_ver, policy_hash)."""
    kp = generate_keypair()
    sender = derive_address(kp.public_key)
    tx1 = _make_signed_tx(kp=kp, sender=sender, nonce=1, action="state.set",
                          payload={"key": "a", "value": 1})
    tx2 = _make_signed_tx(kp=kp, sender=sender, nonce=2, action="counter.increment",
                          payload={"key": "counter", "amount": 5})
    prior_state: dict = {}
    pks = {sender: kp.public_key}
    nonces = {sender: 0}
    return prior_state, [tx1, tx2], pks, nonces, 1, "policy_abc"


# ======================================================================
# Test 1 — Valid Batch Updates State
# ======================================================================


class TestValidBatchUpdatesState:
    """Valid batch MUST update state and produce correct results."""

    def test_state_updated(self) -> None:
        prior_state, txs, pks, nonces, rv, ph = _valid_batch_params()
        result = execute_batch(prior_state, txs, pks, nonces, rv, ph)
        assert "a" in result.final_state
        assert result.final_state["a"] == 1
        assert "counter" in result.final_state
        assert result.final_state["counter"] == 5

    def test_accepted_ids_correct(self) -> None:
        prior_state, txs, pks, nonces, rv, ph = _valid_batch_params()
        result = execute_batch(prior_state, txs, pks, nonces, rv, ph)
        assert len(result.accepted_tx_ids) == 2
        assert result.accepted_tx_ids[0] == txs[0].tx_id
        assert result.accepted_tx_ids[1] == txs[1].tx_id


# ======================================================================
# Test 2 — Receipt Generated For Valid Transaction
# ======================================================================


class TestReceiptGenerated:
    """Receipt MUST be generated for each valid transaction."""

    def test_two_receipts(self) -> None:
        prior_state, txs, pks, nonces, rv, ph = _valid_batch_params()
        result = execute_batch(prior_state, txs, pks, nonces, rv, ph)
        assert len(result.receipts) == 2
        assert result.receipts[0].tx_id == txs[0].tx_id
        assert result.receipts[1].tx_id == txs[1].tx_id

    def test_receipt_execution_result(self) -> None:
        prior_state, txs, pks, nonces, rv, ph = _valid_batch_params()
        result = execute_batch(prior_state, txs, pks, nonces, rv, ph)
        for receipt in result.receipts:
            assert receipt.execution_result["status"] == "accepted"
            assert receipt.execution_result["action"] in ("state.set", "counter.increment")


# ======================================================================
# Test 3 — State Roots Progress Deterministically
# ======================================================================


class TestStateRootsProgress:
    """State roots MUST progress deterministically through the batch."""

    def test_initial_root_matches_prior(self) -> None:
        prior_state, txs, pks, nonces, rv, ph = _valid_batch_params()
        result = execute_batch(prior_state, txs, pks, nonces, rv, ph)
        assert result.initial_state_root == derive_state_root(prior_state)

    def test_final_root_matches_final_state(self) -> None:
        prior_state, txs, pks, nonces, rv, ph = _valid_batch_params()
        result = execute_batch(prior_state, txs, pks, nonces, rv, ph)
        assert result.final_state_root == derive_state_root(result.final_state)

    def test_roots_differ(self) -> None:
        prior_state, txs, pks, nonces, rv, ph = _valid_batch_params()
        result = execute_batch(prior_state, txs, pks, nonces, rv, ph)
        assert result.initial_state_root != result.final_state_root


# ======================================================================
# Test 4 — Invalid Signature Rejects Transaction
# ======================================================================


class TestInvalidSignatureRejects:
    """Invalid signature MUST reject transaction without mutating state."""

    def test_rejected(self) -> None:
        kp = generate_keypair()
        kp_other = generate_keypair()
        sender = derive_address(kp.public_key)
        tx = _make_signed_tx(kp=kp_other, sender=sender, nonce=1, action="state.set",
                             payload={"key": "a", "value": 1})
        prior_state: dict = {}
        pks = {sender: kp.public_key}  # kp.public_key, signed by kp_other
        result = execute_batch(prior_state, [tx], pks, {sender: 0}, 1, "p")
        assert len(result.rejected_tx_ids) == 1
        assert len(result.accepted_tx_ids) == 0
        assert len(result.receipts) == 0
        assert result.final_state == prior_state


# ======================================================================
# Test 5 — Missing Public Key Rejects Transaction
# ======================================================================


class TestMissingPublicKeyRejects:
    """Missing public key MUST reject transaction without mutating state."""

    def test_rejected(self) -> None:
        kp = generate_keypair()
        sender = derive_address(kp.public_key)
        tx = _make_signed_tx(kp=kp, sender=sender, nonce=1)
        prior_state: dict = {}
        # Empty public_keys_by_sender
        result = execute_batch(prior_state, [tx], {}, {sender: 0}, 1, "p")
        assert len(result.rejected_tx_ids) == 1
        assert len(result.accepted_tx_ids) == 0
        assert result.final_state == prior_state


# ======================================================================
# Test 6 — Nonce Mismatch Rejects Transaction
# ======================================================================


class TestNonceMismatchRejects:
    """Nonce mismatch MUST reject transaction without mutating state."""

    def test_rejected_wrong_nonce(self) -> None:
        kp = generate_keypair()
        sender = derive_address(kp.public_key)
        # Transaction has nonce=1, but current nonce is 5 → expected 6
        tx = _make_signed_tx(kp=kp, sender=sender, nonce=1)
        prior_state: dict = {}
        pks = {sender: kp.public_key}
        result = execute_batch(prior_state, [tx], pks, {sender: 5}, 1, "p")
        assert len(result.rejected_tx_ids) == 1
        assert len(result.accepted_tx_ids) == 0
        assert result.final_state == prior_state


# ======================================================================
# Test 7 — Rejected Transaction Does Not Mutate State
# ======================================================================


class TestRejectedNoStateMutation:
    """Rejected transaction MUST NOT mutate state."""

    def test_invalid_signature_no_mutation(self) -> None:
        kp = generate_keypair()
        kp_other = generate_keypair()
        sender = derive_address(kp.public_key)
        tx = _make_signed_tx(kp=kp_other, sender=sender, nonce=1)
        prior_state = {"existing": 42}
        pks = {sender: kp.public_key}
        result = execute_batch(prior_state, [tx], pks, {sender: 0}, 1, "p")
        assert result.final_state == {"existing": 42}

    def test_missing_pk_no_mutation(self) -> None:
        kp = generate_keypair()
        sender = derive_address(kp.public_key)
        tx = _make_signed_tx(kp=kp, sender=sender, nonce=1)
        prior_state = {"existing": 42}
        result = execute_batch(prior_state, [tx], {}, {sender: 0}, 1, "p")
        assert result.final_state == {"existing": 42}

    def test_nonce_mismatch_no_mutation(self) -> None:
        kp = generate_keypair()
        sender = derive_address(kp.public_key)
        tx = _make_signed_tx(kp=kp, sender=sender, nonce=1)
        prior_state = {"existing": 42}
        pks = {sender: kp.public_key}
        result = execute_batch(prior_state, [tx], pks, {sender: 5}, 1, "p")
        assert result.final_state == {"existing": 42}


# ======================================================================
# Test 8 — Batch Preserves Transaction Order
# ======================================================================


class TestPreservesOrder:
    """Batch execution MUST preserve transaction order."""

    def test_order_preserved(self) -> None:
        kp = generate_keypair()
        sender = derive_address(kp.public_key)
        tx1 = _make_signed_tx(kp=kp, sender=sender, nonce=1, action="state.set",
                              payload={"key": "a", "value": 1})
        tx2 = _make_signed_tx(kp=kp, sender=sender, nonce=2, action="state.set",
                              payload={"key": "b", "value": 2})
        prior_state = {}
        pks = {sender: kp.public_key}
        result = execute_batch(prior_state, [tx1, tx2], pks, {sender: 0}, 1, "p")
        assert result.accepted_tx_ids == (tx1.tx_id, tx2.tx_id)
        assert result.final_state == {"a": 1, "b": 2}


# ======================================================================
# Test 9 — Multiple Valid Transactions Update Nonce Sequence
# ======================================================================


class TestNonceSequence:
    """Multiple valid transactions from same sender MUST advance nonce."""

    def test_nonce_advances(self) -> None:
        kp = generate_keypair()
        sender = derive_address(kp.public_key)
        tx1 = _make_signed_tx(kp=kp, sender=sender, nonce=1, action="counter.increment",
                              payload={"key": "c", "amount": 1})
        tx2 = _make_signed_tx(kp=kp, sender=sender, nonce=2, action="counter.increment",
                              payload={"key": "c", "amount": 2})
        tx3 = _make_signed_tx(kp=kp, sender=sender, nonce=3, action="counter.increment",
                              payload={"key": "c", "amount": 3})
        prior_state = {}
        pks = {sender: kp.public_key}
        result = execute_batch(prior_state, [tx1, tx2, tx3], pks, {sender: 0}, 1, "p")
        assert len(result.accepted_tx_ids) == 3
        assert result.final_state == {"c": 6}
        assert len(result.receipts) == 3

    def test_nonce_gap_rejected(self) -> None:
        kp = generate_keypair()
        sender = derive_address(kp.public_key)
        tx1 = _make_signed_tx(kp=kp, sender=sender, nonce=1, action="state.set",
                              payload={"key": "a", "value": 1})
        tx2 = _make_signed_tx(kp=kp, sender=sender, nonce=3, action="state.set",
                              payload={"key": "b", "value": 2})
        prior_state = {}
        pks = {sender: kp.public_key}
        result = execute_batch(prior_state, [tx1, tx2], pks, {sender: 0}, 1, "p")
        assert len(result.accepted_tx_ids) == 1  # only tx1 accepted
        assert len(result.rejected_tx_ids) == 1  # tx2 rejected (expected nonce 2, got 3)
        assert result.final_state == {"a": 1}


# ======================================================================
# Test 10 — Prior State Is Not Mutated
# ======================================================================


class TestPriorStateNotMutated:
    """``execute_batch`` MUST NOT mutate prior_state."""

    def test_prior_state_unchanged(self) -> None:
        prior_state_orig = {"existing": 42}
        prior_state = dict(prior_state_orig)
        kp = generate_keypair()
        sender = derive_address(kp.public_key)
        tx = _make_signed_tx(kp=kp, sender=sender, nonce=1)
        pks = {sender: kp.public_key}
        _ = execute_batch(prior_state, [tx], pks, {sender: 0}, 1, "p")
        assert prior_state == prior_state_orig


# ======================================================================
# Test 11 — Ordered Transactions Is Not Mutated
# ======================================================================


class TestOrderedTransactionsNotMutated:
    """``execute_batch`` MUST NOT mutate ordered_transactions."""

    def test_tx_list_unchanged(self) -> None:
        prior_state, txs, pks, nonces, rv, ph = _valid_batch_params()
        original_tx_ids = [t.tx_id for t in txs]
        _ = execute_batch(prior_state, txs, pks, nonces, rv, ph)
        assert [t.tx_id for t in txs] == original_tx_ids


# ======================================================================
# Test 12 — Public Keys By Sender Is Not Mutated
# ======================================================================


class TestPublicKeysNotMutated:
    """``execute_batch`` MUST NOT mutate public_keys_by_sender."""

    def test_pks_unchanged(self) -> None:
        kp = generate_keypair()
        sender = derive_address(kp.public_key)
        tx = _make_signed_tx(kp=kp, sender=sender, nonce=1)
        pks_orig = {sender: kp.public_key}
        pks = dict(pks_orig)
        _ = execute_batch({}, [tx], pks, {sender: 0}, 1, "p")
        assert pks == pks_orig


# ======================================================================
# Test 13 — Current Nonces By Sender Is Not Mutated
# ======================================================================


class TestNoncesNotMutated:
    """``execute_batch`` MUST NOT mutate current_nonces_by_sender."""

    def test_nonces_unchanged(self) -> None:
        kp = generate_keypair()
        sender = derive_address(kp.public_key)
        tx = _make_signed_tx(kp=kp, sender=sender, nonce=1)
        nonces_orig = {sender: 0}
        nonces = dict(nonces_orig)
        pks = {sender: kp.public_key}
        _ = execute_batch({}, [tx], pks, nonces, 1, "p")
        assert nonces == nonces_orig


# ======================================================================
# Test 14 — Repeated Execution Produces Identical Result
# ======================================================================


class TestRepeatedExecutionDeterministic:
    """Repeated execution of same batch MUST produce identical results."""

    def test_repeated_50_times(self) -> None:
        prior_state, txs, pks, nonces, rv, ph = _valid_batch_params()
        results = [
            execute_batch(prior_state, txs, pks, nonces, rv, ph)
            for _ in range(50)
        ]
        assert all(
            r.initial_state_root == results[0].initial_state_root
            and r.final_state_root == results[0].final_state_root
            and r.final_state == results[0].final_state
            and r.accepted_tx_ids == results[0].accepted_tx_ids
            and r.rejected_tx_ids == results[0].rejected_tx_ids
            and len(r.receipts) == len(results[0].receipts)
            for r in results
        )


# ======================================================================
# Test 15 — Reducer Error Rejects Without Halting
# ======================================================================


class TestReducerErrorRejects:
    """Reducer error MUST reject transaction without halting the batch."""

    def test_invalid_action_rejected(self) -> None:
        kp = generate_keypair()
        sender = derive_address(kp.public_key)
        # Validly signed but with unsupported action
        utx = create_unsigned_transaction(
            sender=sender, nonce=1, epoch=0, action="invalid.action", payload={}
        )
        tx = sign_transaction(utx, kp.private_key)

        # Second valid tx — nonce=1 (same as tx1 because nonce didn't advance after rejection)
        tx2 = _make_signed_tx(kp=kp, sender=sender, nonce=1, action="state.set",
                              payload={"key": "a", "value": 1})

        prior_state = {}
        pks = {sender: kp.public_key}
        result = execute_batch(prior_state, [tx, tx2], pks, {sender: 0}, 1, "p")
        assert len(result.rejected_tx_ids) == 1  # only invalid.action rejected
        assert len(result.accepted_tx_ids) == 1  # tx2 accepted (nonce=1 matches 0+1)
        assert result.final_state == {"a": 1}


# ======================================================================
# Test 16 — Final State Root Equals derive_state_root(final_state)
# ======================================================================


class TestFinalStateRootCorrect:
    """Final state root MUST equal derive_state_root(final_state)."""

    def test_final_root_matches(self) -> None:
        prior_state, txs, pks, nonces, rv, ph = _valid_batch_params()
        result = execute_batch(prior_state, txs, pks, nonces, rv, ph)
        assert result.final_state_root == derive_state_root(result.final_state)


# ======================================================================
# Test 17 — Initial State Root Equals derive_state_root(prior_state)
# ======================================================================


class TestInitialStateRootCorrect:
    """Initial state root MUST equal derive_state_root(prior_state)."""

    def test_initial_root_matches(self) -> None:
        prior_state, txs, pks, nonces, rv, ph = _valid_batch_params()
        result = execute_batch(prior_state, txs, pks, nonces, rv, ph)
        assert result.initial_state_root == derive_state_root(prior_state)


# ======================================================================
# Test 18 — Result Model Is Immutable
# ======================================================================


class TestResultModelImmutable:
    """ExecutionBatchResult MUST be immutable."""

    def test_fields_frozen(self) -> None:
        result = ExecutionBatchResult(
            initial_state_root="a",
            final_state_root="b",
            final_state={},
            receipts=(),
            accepted_tx_ids=(),
            rejected_tx_ids=(),
        )
        with pytest.raises(Exception):
            result.final_state = {"x": 1}  # type: ignore

    def test_tuples_immutable(self) -> None:
        result = ExecutionBatchResult(
            initial_state_root="a",
            final_state_root="b",
            final_state={},
            receipts=(),
            accepted_tx_ids=("abc",),
            rejected_tx_ids=(),
        )
        with pytest.raises(Exception):
            result.accepted_tx_ids = ("xyz",)  # type: ignore


# ======================================================================
# Additional edge cases
# ======================================================================


class TestExecutorEdgeCases:
    """Additional edge cases for batch execution."""

    def test_empty_batch(self) -> None:
        result = execute_batch({"a": 1}, [], {}, {}, 1, "p")
        assert result.initial_state_root == derive_state_root({"a": 1})
        assert result.final_state_root == derive_state_root({"a": 1})
        assert result.final_state == {"a": 1}
        assert len(result.receipts) == 0
        assert len(result.accepted_tx_ids) == 0
        assert len(result.rejected_tx_ids) == 0

    def test_multi_sender_batch(self) -> None:
        kp1 = generate_keypair()
        kp2 = generate_keypair()
        s1 = derive_address(kp1.public_key)
        s2 = derive_address(kp2.public_key)

        tx1 = _make_signed_tx(kp=kp1, sender=s1, nonce=1, action="state.set",
                              payload={"key": "from_alice", "value": 100})
        tx2 = _make_signed_tx(kp=kp2, sender=s2, nonce=1, action="state.set",
                              payload={"key": "from_bob", "value": 200})

        prior_state = {}
        pks = {s1: kp1.public_key, s2: kp2.public_key}
        nonces = {s1: 0, s2: 0}
        result = execute_batch(prior_state, [tx1, tx2], pks, nonces, 1, "p")
        assert len(result.accepted_tx_ids) == 2
        assert result.final_state == {"from_alice": 100, "from_bob": 200}

    def test_some_rejected_some_accepted(self) -> None:
        kp = generate_keypair()
        kp_other = generate_keypair()
        sender = derive_address(kp.public_key)

        tx_valid = _make_signed_tx(kp=kp, sender=sender, nonce=1, action="state.set",
                                   payload={"key": "a", "value": 1})
        tx_invalid_sig = _make_signed_tx(kp=kp_other, sender=sender, nonce=2,
                                         action="state.set", payload={"key": "b", "value": 2})
        tx_valid2 = _make_signed_tx(kp=kp, sender=sender, nonce=2,
                                    action="counter.increment", payload={"key": "c", "amount": 1})

        prior_state = {}
        pks = {sender: kp.public_key}
        result = execute_batch(prior_state, [tx_valid, tx_invalid_sig, tx_valid2],
                               pks, {sender: 0}, 1, "p")

        assert len(result.accepted_tx_ids) == 2  # tx_valid and tx_valid2
        assert len(result.rejected_tx_ids) == 1  # tx_invalid_sig
        assert result.final_state == {"a": 1, "c": 1}