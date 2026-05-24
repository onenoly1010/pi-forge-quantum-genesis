# Manual Replay Helper

This repository includes a local helper script for replaying signed transactions through the ledger replay layer.

## Purpose

The file `run_manual_replay.py` demonstrates how to:

- generate an Ed25519 key pair using the repo wallet utilities
- create and sign a sample transaction
- execute `src.ledger.replay.replay_batch`
- print the final replay result and root hash

## Run it

Activate the project Python environment, then run:

```bash
source .venv/bin/activate
python run_manual_replay.py
```

## What it does

The helper builds a sample transaction and performs a replay of the batch using the same local ledger logic used in unit tests.

The output includes:

- `is_valid` — whether the replay matched expectations
- `final_state_root` — deterministic final state root computed by replay
- `reason` — failure reason when the replay is invalid

## Customization

You can customize the example by importing the helper from Python:

```python
from run_manual_replay import build_manual_replay_example
from src.ledger.replay import replay_batch

initial_state, ordered_transactions, public_keys_by_sender, initial_nonces_by_sender, reducer_version, policy_hash = build_manual_replay_example(
    action="state.set",
    payload={"key": "x", "value": 42},
)

result = replay_batch(
    initial_state=initial_state,
    ordered_transactions=ordered_transactions,
    public_keys_by_sender=public_keys_by_sender,
    initial_nonces_by_sender=initial_nonces_by_sender,
    reducer_version=reducer_version,
    policy_hash=policy_hash,
)

print(result)
```

## Important note

The helper uses a `KeyPair` object returned by `src.security.wallet.generate_keypair()`.
If you reuse `_make_signed_tx()` from `tests/test_replay.py`, make sure to pass a `KeyPair`-like object with `.private_key` and `.public_key` attributes, not raw bytes.
