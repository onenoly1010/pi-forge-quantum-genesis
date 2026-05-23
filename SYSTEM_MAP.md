# System Map

## High-Level Architecture Overview
Quantum Pi Forge is organized as a deterministic execution platform that converts validated inputs into canonical state transitions and auditable outputs. The system is structured into:
1. Input and orchestration surfaces
2. Deterministic execution and reduction pipeline
3. Canonical serialization and cryptographic integrity layers
4. Audit receipt and anchoring surfaces
5. Verification and replay control loops

## Deterministic Execution Flow
1. Inputs are accepted through controlled interfaces.
2. Inputs are normalized under canonical schemas.
3. Execution modules process data using deterministic rules.
4. Reducers produce finalized state transition candidates.
5. Canonical serializer emits stable byte-level representations.
6. Hashing layer generates integrity fingerprints.
7. Audit layer records receipts and verification metadata.
8. Anchoring layer persists verifiable references for external validation.
9. Replay validators confirm reproducibility against canonical records.

## Reducer Pipeline
- Reducers operate on normalized inputs only.
- Reduction order is stable and explicitly defined.
- State mutation is constrained to deterministic transition rules.
- Reducer outputs are treated as pre-serialization canonical candidates.

## Canonical Serialization Layer
- Serialization enforces deterministic field ordering and encoding.
- Canonical payloads are byte-stable across identical inputs.
- Serialization output is the sole source for downstream hashing.

## Hashing Layer
- Cryptographic hashing is applied to canonical serialized payloads.
- Hash outputs act as immutable integrity identifiers.
- Hash lineage is retained for verification, replay, and audit linkage.

## Audit Receipt Layer
- Each finalized transition produces an audit receipt.
- Receipts capture execution context, canonical hash, and verification markers.
- Receipts provide traceability for review, demos, and compliance checks.

## Anchoring Layer
- Anchoring references canonical hashes and receipts in durable records.
- Anchors support independent third-party verification of integrity claims.
- Anchor records are append-oriented to preserve historical continuity.

## Validator Role
Validators confirm:
- Input normalization compliance
- Reducer determinism
- Serialization stability
- Hash consistency
- Receipt completeness
- Anchor-reference integrity

Validators are verification actors, not state authors.

## Orchestration Role
Orchestration coordinates:
- Execution sequencing
- Dependency gating
- Validation checkpoints
- Artifact publication to public status and metrics surfaces

Orchestration enforces process discipline without changing deterministic core logic.

## Replay Verification Role
Replay verification re-executes historical inputs against canonical rules and compares:
- Canonical serialized outputs
- Hashes
- Receipts
- Anchor references

A replay match confirms deterministic reproducibility and audit confidence.