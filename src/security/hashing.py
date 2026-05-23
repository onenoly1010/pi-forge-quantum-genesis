"""Deterministic constitutional hashing layer for 0G-aligned systems.

Provides canonical serialization and domain-separated hashing (SHA-256 / BLAKE3)
with strict rejection of non-deterministic or invalid values.
"""

import hashlib
import math
import unicodedata
from typing import Any, Dict, List, Union

import orjson
from blake3 import blake3

# ---------------------------------------------------------------------------
# Domain prefixes — used to enforce domain separation across hash contexts
# ---------------------------------------------------------------------------
DOMAIN_TX: bytes = b"TX:"
DOMAIN_STATE: bytes = b"STATE:"
DOMAIN_POLICY: bytes = b"POLICY:"
DOMAIN_RECEIPT: bytes = b"RECEIPT:"

# ---------------------------------------------------------------------------
# Internal validation helpers
# ---------------------------------------------------------------------------

# Recursive type for normalized JSON-compatible values.
_JsonValue = Union[None, bool, int, float, str, List["_JsonValue"], Dict[str, "_JsonValue"]]


def _check_value(value: Any) -> None:
    """Recursively validate *value* contains no NaN, Infinity, or unsupported types.

    Raises:
        ValueError: When *value* (or a descendant) is NaN or Infinity.
        TypeError: When *value* (or a descendant) is an unsupported runtime type.
    """
    if isinstance(value, bool):
        return
    if isinstance(value, (int, float)):
        if isinstance(value, float):
            if math.isnan(value):
                raise ValueError("NaN values are not allowed in canonical serialization")
            if math.isinf(value):
                raise ValueError("Infinity values are not allowed in canonical serialization")
        return
    if isinstance(value, str):
        _require_utf8(value)
        return
    if value is None:
        return
    if isinstance(value, (list, tuple)):
        for item in value:
            _check_value(item)
        return
    if isinstance(value, dict):
        for k, v in value.items():
            _check_value(k)
            _check_value(v)
        return
    raise TypeError(f"Unsupported type for canonical serialization: {type(value).__name__}")


def _require_utf8(text: str) -> None:
    """Raise ValueError when *text* cannot be encoded as UTF-8."""
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError(
            f"String cannot be encoded as UTF-8: {text!r}"
        ) from exc


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def normalize_value(value: Any) -> _JsonValue:
    """Recursively normalise *value* for deterministic canonical serialization.

    Steps performed:
    * Unicode NFC normalisation on every string.
    * Recursive dictionary-key Unicode NFC normalisation.
    * Recursive re-building of dictionaries / lists (tuples → lists).

    Raises:
        ValueError: When a NaN or Infinity float is encountered.
    """
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        if isinstance(value, float):
            if math.isnan(value):
                raise ValueError("NaN values are not allowed in canonical serialization")
            if math.isinf(value):
                raise ValueError("Infinity values are not allowed in canonical serialization")
        return value
    if value is None:
        return None
    if isinstance(value, (list, tuple)):
        return [normalize_value(item) for item in value]
    if isinstance(value, dict):
        return {
            unicodedata.normalize("NFC", k) if isinstance(k, str) else k: normalize_value(v)
            for k, v in value.items()
        }
    # Unsupported type — the caller will see this via orjson failure, but we
    # also raise here so the error is consistent regardless of backend.
    raise TypeError(f"Unsupported type for canonical serialization: {type(value).__name__}")


def canonical_serialize(obj: Any) -> bytes:
    """Serialize *obj* to canonical UTF-8 bytes.

    Rules:
    * UTF-8 only.
    * Unicode NFC normalised.
    * Dictionary keys recursively sorted.
    * List ordering preserved.
    * NaN / Infinity / -Infinity rejected.
    * Unsupported runtime objects rejected.
    * Deterministic compact separators (no whitespace).

    Returns:
        ``bytes`` — identical across platforms for the same input.
    """
    normalized = normalize_value(obj)
    try:
        return orjson.dumps(
            normalized,
            option=orjson.OPT_SORT_KEYS,
        )
    except TypeError as exc:
        # Wrap orjson-type errors (e.g. non-UTF-8 surrogates) into a
        # consistent ValueError so callers only need to catch one type.
        raise ValueError(str(exc)) from exc


def sha256_hex(data: bytes) -> str:
    """Return the lowercase hex SHA-256 digest of *data*."""
    return hashlib.sha256(data).hexdigest()


def blake3_hex(data: bytes) -> str:
    """Return the lowercase hex BLAKE3 digest of *data*."""
    return blake3(data).hexdigest()


# ---------------------------------------------------------------------------
# Domain-separated hash functions
# ---------------------------------------------------------------------------


def _domain_hash(domain: bytes, payload: Any) -> str:
    """Compute ``sha256(domain + canonical_serialize(payload))``."""
    serialized = canonical_serialize(payload)
    return sha256_hex(domain + serialized)


def hash_transaction(payload: Any) -> str:
    """Domain-separated hash of a **transaction** payload."""
    return _domain_hash(DOMAIN_TX, payload)


def hash_state(state: Any) -> str:
    """Domain-separated hash of a **state** payload."""
    return _domain_hash(DOMAIN_STATE, state)


def hash_policy(policy: Any) -> str:
    """Domain-separated hash of a **policy** payload."""
    return _domain_hash(DOMAIN_POLICY, policy)


def hash_receipt(receipt: Any) -> str:
    """Domain-separated hash of a **receipt** payload."""
    return _domain_hash(DOMAIN_RECEIPT, receipt)