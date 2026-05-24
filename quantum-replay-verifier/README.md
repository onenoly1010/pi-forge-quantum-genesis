# quantum-replay-verifier

Zero-dependency deterministic replay verifier for signed identity transaction batches.

## Run

./verify.sh

## Runtime

- Node.js >= 20
- No npm install
- No dependencies
- No network access
- No environment variables
- No wall-clock time

## What this proves

Independent machines reproduce identical state roots from identical signed transaction batches.

Mutated payloads are rejected deterministically.
