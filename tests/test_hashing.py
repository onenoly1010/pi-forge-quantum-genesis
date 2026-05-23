"""Constitutional hashing layer — deterministic, replay-safe tests."""

import math
import sys
import unicodedata

import pytest

from src.security.hashing import (
    blake3_hex,
    canonical_serialize,
    hash_policy,
    hash_receipt,
    hash_state,
    hash_transaction,
    normalize_value,
    sha256_hex,
)

# ======================================================================
# Test 1 — Canonical Dictionary Equivalence
# ======================================================================


class TestCanonicalDictionaryEquivalence:
    """Dictionaries differing only by key ordering MUST hash identically."""

    def test_key_order_independence(self) -> None:
        a = {"a": 1, "b": 2}
        b = {"b": 2, "a": 1}
        assert canonical_serialize(a) == canonical_serialize(b)

    def test_sha256_key_order_independence(self) -> None:
        a = {"a": 1, "b": 2}
        b = {"b": 2, "a": 1}
        assert sha256_hex(canonical_serialize(a)) == sha256_hex(canonical_serialize(b))

    def test_blake3_key_order_independence(self) -> None:
        a = {"a": 1, "b": 2}
        b = {"b": 2, "a": 1}
        ser_a = canonical_serialize(a)
        ser_b = canonical_serialize(b)
        assert blake3_hex(ser_a) == blake3_hex(ser_b)


# ======================================================================
# Test 2 — Nested Dictionary Stability
# ======================================================================


class TestNestedDictionaryStability:
    """Deeply nested dictionaries with reordered keys MUST serialize identically."""

    def test_nested_reorder(self) -> None:
        a = {"level1": {"level2": {"a": 1, "b": 2}, "x": 10}, "y": 20}
        b = {"y": 20, "level1": {"x": 10, "level2": {"b": 2, "a": 1}}}
        assert canonical_serialize(a) == canonical_serialize(b)

    def test_triple_nested_reorder(self) -> None:
        a = {"l1": {"l2": {"l3": {"c": 3, "a": 1, "b": 2}}}}
        b = {"l1": {"l2": {"l3": {"b": 2, "c": 3, "a": 1}}}}
        assert canonical_serialize(a) == canonical_serialize(b)

    def test_mixed_nested_types(self) -> None:
        a = {"items": [{"id": 2, "val": "b"}, {"id": 1, "val": "a"}], "meta": {"ver": 1}}
        b = {"meta": {"ver": 1}, "items": [{"val": "b", "id": 2}, {"val": "a", "id": 1}]}
        assert canonical_serialize(a) == canonical_serialize(b)


# ======================================================================
# Test 3 — Unicode NFC Equivalence
# ======================================================================


class TestUnicodeNfcEquivalence:
    """Unicode strings that are canonically equivalent under NFC MUST hash identically."""

    def test_nfc_nfd_equivalence(self) -> None:
        composed = unicodedata.normalize("NFC", "é")  # U+00E9
        decomposed = unicodedata.normalize("NFD", "é")  # e + U+0301
        assert composed != decomposed, "Precondition: strings differ before normalization"
        ser_composed = canonical_serialize(composed)
        ser_decomposed = canonical_serialize(decomposed)
        assert ser_composed == ser_decomposed

    def test_nfc_accent_variants(self) -> None:
        nfc = unicodedata.normalize("NFC", "café")
        nfd = unicodedata.normalize("NFD", "café")
        assert canonical_serialize(nfc) == canonical_serialize(nfd)

    def test_nfc_multi_codepoint(self) -> None:
        nfc = unicodedata.normalize("NFC", "Naïve 🧑‍💻")
        nfd = unicodedata.normalize("NFD", "Naïve 🧑‍💻")
        assert canonical_serialize(nfc) == canonical_serialize(nfd)

    def test_nfc_dictionary_keys(self) -> None:
        nfc_key = unicodedata.normalize("NFC", "résumé")
        nfd_key = unicodedata.normalize("NFD", "résumé")
        a = {nfc_key: 1}
        b = {nfd_key: 1}
        assert canonical_serialize(a) == canonical_serialize(b)


# ======================================================================
# Test 4 — NaN Rejection
# ======================================================================


class TestNaNRejection:
    """Serialization MUST raise for NaN values."""

    def test_nan_top_level(self) -> None:
        with pytest.raises(ValueError, match="NaN"):
            canonical_serialize(float("nan"))

    def test_nan_in_list(self) -> None:
        with pytest.raises(ValueError, match="NaN"):
            canonical_serialize([1, float("nan"), 3])

    def test_nan_in_dict_value(self) -> None:
        with pytest.raises(ValueError, match="NaN"):
            canonical_serialize({"x": float("nan")})

    def test_nan_in_nested_dict(self) -> None:
        with pytest.raises(ValueError, match="NaN"):
            canonical_serialize({"a": {"b": float("nan")}})


# ======================================================================
# Test 5 — Infinity Rejection
# ======================================================================


class TestInfinityRejection:
    """Serialization MUST raise for positive and negative infinity."""

    def test_pos_inf_top_level(self) -> None:
        with pytest.raises(ValueError, match="Infinity"):
            canonical_serialize(float("inf"))

    def test_neg_inf_top_level(self) -> None:
        with pytest.raises(ValueError, match="Infinity"):
            canonical_serialize(float("-inf"))

    def test_pos_inf_in_list(self) -> None:
        with pytest.raises(ValueError, match="Infinity"):
            canonical_serialize([1, float("inf"), 2])

    def test_neg_inf_in_dict(self) -> None:
        with pytest.raises(ValueError, match="Infinity"):
            canonical_serialize({"x": float("-inf")})


# ======================================================================
# Test 6 — SHA256 Reproducibility
# ======================================================================


class TestSha256Reproducibility:
    """Repeated SHA-256 hashing MUST produce identical outputs."""

    def test_repeated_calls_same_output(self) -> None:
        data = b"deterministic test data"
        results = [sha256_hex(data) for _ in range(100)]
        assert all(r == results[0] for r in results)

    def test_serialization_then_hash_repeatable(self) -> None:
        obj = {"key": "value", "nested": {"a": 1, "b": 2}}
        ser = canonical_serialize(obj)
        h1 = sha256_hex(ser)
        h2 = sha256_hex(ser)
        assert h1 == h2

    def test_roundtrip_stability(self) -> None:
        obj = {"data": [1, 2, 3], "meta": {"version": 1}}
        hashes = [sha256_hex(canonical_serialize(obj)) for _ in range(50)]
        assert all(h == hashes[0] for h in hashes)


# ======================================================================
# Test 7 — Blake3 Reproducibility
# ======================================================================


class TestBlake3Reproducibility:
    """Repeated BLAKE3 hashing MUST produce identical outputs."""

    def test_repeated_calls_same_output(self) -> None:
        data = b"deterministic blake3 test"
        results = [blake3_hex(data) for _ in range(100)]
        assert all(r == results[0] for r in results)

    def test_serialization_then_blake3_repeatable(self) -> None:
        obj = {"key": "value", "nested": {"a": 1, "b": 2}}
        ser = canonical_serialize(obj)
        h1 = blake3_hex(ser)
        h2 = blake3_hex(ser)
        assert h1 == h2

    def test_blake3_empty_bytes(self) -> None:
        h1 = blake3_hex(b"")
        h2 = blake3_hex(b"")
        assert h1 == h2


# ======================================================================
# Test 8 — Domain Separation
# ======================================================================


class TestDomainSeparation:
    """Domain-separated hash functions MUST produce different outputs for the same payload."""

    def test_tx_vs_state(self) -> None:
        payload = {"a": 1, "b": 2}
        assert hash_transaction(payload) != hash_state(payload)

    def test_tx_vs_policy(self) -> None:
        payload = {"a": 1, "b": 2}
        assert hash_transaction(payload) != hash_policy(payload)

    def test_tx_vs_receipt(self) -> None:
        payload = {"a": 1, "b": 2}
        assert hash_transaction(payload) != hash_receipt(payload)

    def test_state_vs_policy(self) -> None:
        payload = {"a": 1, "b": 2}
        assert hash_state(payload) != hash_policy(payload)

    def test_state_vs_receipt(self) -> None:
        payload = {"a": 1, "b": 2}
        assert hash_state(payload) != hash_receipt(payload)

    def test_policy_vs_receipt(self) -> None:
        payload = {"a": 1, "b": 2}
        assert hash_policy(payload) != hash_receipt(payload)

    def test_all_four_domains_distinct(self) -> None:
        payload = {"x": 42}
        digests = {
            hash_transaction(payload),
            hash_state(payload),
            hash_policy(payload),
            hash_receipt(payload),
        }
        assert len(digests) == 4, "All four domain hashes must be distinct"

    def test_domain_separation_identical_payload_nested(self) -> None:
        payload = {"nested": {"deep": [1, 2, 3], "key": "val"}, "top": True}
        assert hash_transaction(payload) != hash_state(payload)
        assert hash_state(payload) != hash_policy(payload)
        assert hash_policy(payload) != hash_receipt(payload)


# ======================================================================
# Test 9 — Deterministic Byte Stability
# ======================================================================


class TestDeterministicByteStability:
    """Repeated canonical serialization MUST produce byte-identical outputs."""

    def test_repeated_serialize_same_object(self) -> None:
        obj = {"z": 26, "a": 1, "nested": {"y": 25, "b": 2}}
        results = [canonical_serialize(obj) for _ in range(100)]
        assert all(r == results[0] for r in results)

    def test_serialize_none(self) -> None:
        ser = canonical_serialize(None)
        assert ser == b"null"

    def test_serialize_bool(self) -> None:
        assert canonical_serialize(True) == b"true"
        assert canonical_serialize(False) == b"false"

    def test_serialize_int_list(self) -> None:
        obj = [3, 1, 2]
        ser1 = canonical_serialize(obj)
        ser2 = canonical_serialize([3, 1, 2])
        assert ser1 == ser2

    def test_serialize_mixed_nested(self) -> None:
        obj = {"list": [{"b": 2, "a": 1}, {"d": 4, "c": 3}], "flag": True, "name": "test"}
        ser1 = canonical_serialize(obj)
        ser2 = canonical_serialize(obj)
        assert ser1 == ser2


# ======================================================================
# Additional edge-case tests
# ======================================================================


class TestNormalizeValue:
    """Normalize_value must handle all JSON-compatible types."""

    def test_string_normalization(self) -> None:
        nfd = unicodedata.normalize("NFD", "é")
        result = normalize_value(nfd)
        assert result == "é"
        assert unicodedata.is_normalized("NFC", result)

    def test_integer_passthrough(self) -> None:
        assert normalize_value(42) == 42

    def test_float_passthrough(self) -> None:
        assert normalize_value(3.14) == 3.14

    def test_bool_passthrough(self) -> None:
        assert normalize_value(True) is True
        assert normalize_value(False) is False

    def test_none_passthrough(self) -> None:
        assert normalize_value(None) is None

    def test_list_recursion(self) -> None:
        nfd_str = unicodedata.normalize("NFD", "é")
        result = normalize_value([nfd_str, {"key": nfd_str}])
        assert result == ["é", {"key": "é"}]

    def test_tuple_conversion_to_list(self) -> None:
        result = normalize_value((1, 2, 3))
        assert result == [1, 2, 3]

    def test_nan_rejection(self) -> None:
        with pytest.raises(ValueError, match="NaN"):
            normalize_value(float("nan"))

    def test_inf_rejection(self) -> None:
        with pytest.raises(ValueError, match="Infinity"):
            normalize_value(float("inf"))


class TestUnsupportedTypes:
    """Unsupported runtime objects MUST raise TypeError."""

    def test_custom_object(self) -> None:
        class Custom:
            pass

        with pytest.raises(TypeError, match="Unsupported type"):
            canonical_serialize(Custom())

    def test_custom_in_list(self) -> None:
        class Custom:
            pass

        with pytest.raises(TypeError, match="Unsupported type"):
            canonical_serialize([1, Custom()])

    def test_custom_in_dict_value(self) -> None:
        class Custom:
            pass

        with pytest.raises(TypeError, match="Unsupported type"):
            canonical_serialize({"x": Custom()})

    def test_set_types(self) -> None:
        with pytest.raises(TypeError, match="Unsupported type"):
            canonical_serialize({1, 2, 3})


class TestUnicodeEdgeCases:
    """Edge cases for Unicode handling."""

    def test_surrogate_rejection(self) -> None:
        # Lone surrogate — invalid UTF-8
        with pytest.raises(ValueError):
            canonical_serialize("\ud800")

    def test_empty_string(self) -> None:
        ser = canonical_serialize("")
        assert ser == b'""'

    def test_unicode_snowman(self) -> None:
        ser = canonical_serialize("☃")
        # orjson emits UTF-8-encoded bytes, not ASCII escapes
        assert ser == b'"\xe2\x98\x83"'

    def test_mixed_script_unicode(self) -> None:
        text = "Hello, 世界! 🎉"
        ser1 = canonical_serialize(text)
        ser2 = canonical_serialize(text)
        assert ser1 == ser2