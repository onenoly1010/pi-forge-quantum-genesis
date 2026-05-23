"""Deterministic state root derivation for 0G-aligned ledger systems.

Provides a single pure function ``derive_state_root`` that computes a
replay-stable, domain-separated state root from any canonically-serialisable
object.
"""

from typing import Any

from src.security.hashing import hash_state


def derive_state_root(state: object) -> str:
    """Derive a deterministic, replay-stable state root from *state*.

    The state root is computed as:

        state_root = hash_state(state)

    ``hash_state`` applies ``sha256(b"STATE:" + canonical_serialize(state))``,
    providing domain separation and deterministic canonical serialisation.

    This function is:
    * pure — no side-effects, no mutation of *state*
    * deterministic — identical inputs produce identical outputs
    * replay-safe — cross-platform stable

    Args:
        state: Any JSON-compatible object (dict, list, str, int, float, bool, None).

    Returns:
        A lowercase hex string (SHA-256 digest, 64 characters).

    Raises:
        ValueError: If *state* contains NaN or Infinity values.
        TypeError: If *state* contains unsupported runtime object types.
    """
    return hash_state(state)