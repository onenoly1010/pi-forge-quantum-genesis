from __future__ import annotations

from src.ledger.replay import replay_batch
from src.security.wallet import derive_address, generate_keypair
from tests.test_replay import _make_signed_tx
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
return verify_signature(public_key, signable, transaction.signature)(.venv) kris@quantum-pi-forge:~/forge/Quantum-pi-forge$ python - <<'PY'

def build_manual_replay_example(
    action: str = "state.set",
    payload: dict | None = None,
    nonce: int = 1,
    epoch: int = 0,
    reducer_version: int = 1,
    policy_hash: str = "genesis_hash_001",
) -> tuple[dict, list, dict, dict, int, str]:
    """Build a reusable example payload for `replay_batch`."""
    kp = generate_keypair()
    sender = derive_address(kp.public_key)
    tx = _make_signed_tx(
        kp=kp,
        sender=sender,
        nonce=nonce,
        epoch=epoch,
        action=action,
        payload=payload or {"system": "online"},
    )

    initial_state: dict = {}
    public_keys = {sender: kp.public_key}
    initial_nonces = {sender: 0}

    return initial_state, [tx], public_keys, initial_nonces, reducer_version, policy_hash


def run_manual_replay_example() -> None:
    """Execute the example replay and print the result."""
    (
        initial_state,
        ordered_transactions,
        public_keys_by_sender,
        initial_nonces_by_sender,
        reducer_version,
        policy_hash,
    ) = build_manual_replay_example()

    result = replay_batch(
        initial_state=initial_state,
        ordered_transactions=ordered_transactions,
        public_keys_by_sender=public_keys_by_sender,
        initial_nonces_by_sender=initial_nonces_by_sender,
        reducer_version=reducer_version,
        policy_hash=policy_hash,
    )

    print("\n--- REPLAY RESULTS ---")
    print(f"Valid:       {result.is_valid}")
    print(f"Final Root:  {result.final_state_root}")
    if not result.is_valid:
        print(f"Reason:      {result.reason}")


if __name__ == "__main__":
    run_manual_replay_example()
