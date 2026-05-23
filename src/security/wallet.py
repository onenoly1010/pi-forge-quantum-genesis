"""Deterministic wallet layer using Ed25519 (NaCl) for 0G-aligned systems.

Provides key generation, deterministic address derivation via BLAKE3,
Ed25519 detached signing/verification, and immutable data models.
Entropy is strictly confined to ``generate_keypair()`` only.
"""

import os

from blake3 import blake3
from nacl.exceptions import BadSignatureError
from nacl.signing import SigningKey, VerifyKey
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Data models — immutable, fully typed
# ---------------------------------------------------------------------------


class KeyPair(BaseModel, frozen=True):
    """Immutable key pair holding raw bytes for private and public keys."""

    private_key: bytes = Field(description="Ed25519 private key seed (32 bytes)")
    public_key: bytes = Field(description="Ed25519 public key (32 bytes)")

    model_config = {"frozen": True}


class WalletIdentity(BaseModel, frozen=True):
    """Immutable wallet identity derived from a key pair."""

    address: str = Field(description="0G-compatible address (lowercase hex, 40 chars)")
    public_key: str = Field(description="Hex-encoded public key")
    private_key: str = Field(description="Hex-encoded private key (seed)")

    model_config = {"frozen": True}


# ---------------------------------------------------------------------------
# Key generation (entropy permitted only here)
# ---------------------------------------------------------------------------


def generate_keypair() -> KeyPair:
    """Generate a new Ed25519 key pair using cryptographic entropy.

    Entropy is sourced from ``os.urandom(32)`` and is the **only** location
    in this module where non-determinism is permitted.
    """
    seed = os.urandom(32)
    signing_key = SigningKey(seed)
    return KeyPair(private_key=seed, public_key=bytes(signing_key.verify_key))


# ---------------------------------------------------------------------------
# Address derivation (deterministic — no entropy)
# ---------------------------------------------------------------------------


def derive_address(public_key: bytes) -> str:
    """Derive a deterministic 40-char lowercase hex address from *public_key*.

    Derivation: ``address = blake3(public_key).hexdigest()[:40]``

    This is a **pure function** — no randomness, no timestamps, no state.
    """
    return blake3(public_key).hexdigest()[:40]


# ---------------------------------------------------------------------------
# Signing & verification
# ---------------------------------------------------------------------------


def sign_message(private_key: bytes, message: bytes) -> str:
    """Sign *message* with *private_key* (32-byte seed), returning a
    lowercase hex-encoded detached Ed25519 signature.

    Ed25519 uses deterministic nonces (RFC 8032), so signing the same
    message with the same key always produces the identical signature.
    """
    signing_key = _ensure_signing_key(private_key)
    signature = signing_key.sign(message).signature
    return signature.hex()


def verify_signature(public_key: bytes, message: bytes, signature_hex: str) -> bool:
    """Verify a hex-encoded detached Ed25519 signature.

    Returns ``True`` for valid signatures, ``False`` for invalid or
    malformed input. Never raises an uncaught exception.
    """
    try:
        signature = bytes.fromhex(signature_hex)
    except (ValueError, AttributeError, TypeError):
        return False
    try:
        verify_key = VerifyKey(public_key)
        verify_key.verify(message, signature)
        return True
    except BadSignatureError:
        return False
    except Exception:  # Catch any unexpected crypto errors safely
        return False


# ---------------------------------------------------------------------------
# Export / import (deterministic hex round-trip)
# ---------------------------------------------------------------------------


def export_private_key(private_key: bytes) -> str:
    """Export a 32-byte Ed25519 private key seed as lowercase hex.

    No prefix. Byte-perfect round-trip with ``import_private_key``.
    """
    return private_key.hex()


def export_public_key(public_key: bytes) -> str:
    """Export a 32-byte Ed25519 public key as lowercase hex.

    No prefix. Byte-perfect round-trip with ``import_public_key``.
    """
    return public_key.hex()


def import_private_key(private_key_hex: str) -> bytes:
    """Import a lowercase hex-encoded Ed25519 private key seed."""
    return bytes.fromhex(private_key_hex)


def import_public_key(public_key_hex: str) -> bytes:
    """Import a lowercase hex-encoded Ed25519 public key."""
    return bytes.fromhex(public_key_hex)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_EDIT = "Ed25519 private key must be exactly 32 bytes (seed)"


def _ensure_signing_key(private_key: bytes) -> SigningKey:
    """Validate *private_key* is a valid Ed25519 seed and return a SigningKey."""
    if len(private_key) != 32:
        raise ValueError(_EDIT)
    return SigningKey(private_key)