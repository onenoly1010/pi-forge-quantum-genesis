# Replay Verifier Baseline

Status: PASS

The embedded zero-dependency quantum replay verifier was executed successfully from the parent repository.

Verified result:

- CONSENSUS VERIFIED
- MUTATION REJECTED

Baseline tag:

- v0.1.0-sovereign-baseline

State root reproduced:

- 0xb8d60b87536eec6173948b607bb4252a854c6310d724ce67f1929a4c755dd7cd

Determinism proof:

- Fixture generation uses deterministic key material.
- Running the verifier twice produced identical fixture hashes.
- Running the verifier twice produced identical output logs.
- Mutated input was rejected.

Purpose:

This confirms that the replay verifier exists as a runnable reference implementation inside the main repository, uses stable local path resolution, reproduces the expected deterministic state root, verifies receipt-chain integrity, and rejects mutated input.
