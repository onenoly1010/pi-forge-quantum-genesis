"""Deterministic state root derivation — pure, replay-safe tests."""

import pytest

from src.snapshots.state_root import derive_state_root


# ======================================================================
# Test 1 — Identical State Produces Identical Root
# ======================================================================


class TestIdenticalStateIdenticalRoot:
    """Identical state inputs MUST produce identical state roots."""

    def test_identical_dict_state(self) -> None:
        state = {"balance": 100, "nonce": 1}
        root1 = derive_state_root(state)
        root2 = derive_state_root(state)
        assert root1 == root2

    def test_repeated_derivation_100_times(self) -> None:
        state = {"a": 1, "b": [2, 3, 4], "c": {"nested": True}}
        roots = [derive_state_root(state) for _ in range(100)]
        assert all(r == roots[0] for r in roots)


# ======================================================================
# Test 2 — Reordered Dictionaries Produce Identical Root
# ======================================================================


class TestReorderedDictionariesIdenticalRoot:
    """Dictionaries differing only by key ordering MUST produce identical roots."""

    def test_reordered_top_level_keys(self) -> None:
        root1 = derive_state_root({"b": 2, "a": 1})
        root2 = derive_state_root({"a": 1, "b": 2})
        assert root1 == root2

    def test_reordered_keys_different_insertion(self) -> None:
        root1 = derive_state_root({"z": 26, "m": 13, "a": 1})
        root2 = derive_state_root({"a": 1, "m": 13, "z": 26})
        assert root1 == root2


# ======================================================================
# Test 3 — Nested Reordered Dictionaries Produce Identical Root
# ======================================================================


class TestNestedReorderedDictionariesIdenticalRoot:
    """Deeply nested dictionaries with reordered keys MUST produce identical roots."""

    def test_nested_reorder(self) -> None:
        root1 = derive_state_root(
            {"level1": {"level2": {"a": 1, "b": 2}, "x": 10}, "y": 20}
        )
        root2 = derive_state_root(
            {"y": 20, "level1": {"x": 10, "level2": {"b": 2, "a": 1}}}
        )
        assert root1 == root2

    def test_triple_nested_reorder(self) -> None:
        root1 = derive_state_root({"l1": {"l2": {"l3": {"c": 3, "a": 1, "b": 2}}}})
        root2 = derive_state_root({"l1": {"l2": {"l3": {"b": 2, "c": 3, "a": 1}}}})
        assert root1 == root2


# ======================================================================
# Test 4 — Different State Produces Different Root
# ======================================================================


class TestDifferentStateDifferentRoot:
    """Different state inputs MUST produce different state roots."""

    def test_different_values(self) -> None:
        root1 = derive_state_root({"balance": 100})
        root2 = derive_state_root({"balance": 200})
        assert root1 != root2

    def test_different_keys(self) -> None:
        root1 = derive_state_root({"alice": 100})
        root2 = derive_state_root({"bob": 100})
        assert root1 != root2

    def test_different_nested_structure(self) -> None:
        root1 = derive_state_root({"data": {"inner": 1}})
        root2 = derive_state_root({"data": {"inner": 2}})
        assert root1 != root2


# ======================================================================
# Test 5 — List Ordering Affects Root
# ======================================================================


class TestListOrderingAffectsRoot:
    """Different list orderings MUST produce different state roots."""

    def test_reordered_list(self) -> None:
        root1 = derive_state_root([1, 2, 3])
        root2 = derive_state_root([3, 2, 1])
        assert root1 != root2

    def test_reordered_list_in_dict(self) -> None:
        root1 = derive_state_root({"items": [1, 2, 3]})
        root2 = derive_state_root({"items": [3, 2, 1]})
        assert root1 != root2

    def test_partially_reordered_list(self) -> None:
        root1 = derive_state_root({"data": ["a", "b", "c"]})
        root2 = derive_state_root({"data": ["a", "c", "b"]})
        assert root1 != root2


# ======================================================================
# Test 6 — Input State Is Not Mutated
# ======================================================================


class TestInputStateNotMutated:
    """``derive_state_root`` MUST NOT mutate its input."""

    def test_dict_not_mutated(self) -> None:
        original = {"balance": 100, "nested": {"a": 1}}
        state = dict(original)
        _ = derive_state_root(state)
        assert state == original

    def test_list_not_mutated(self) -> None:
        original = [1, 2, 3]
        state = list(original)
        _ = derive_state_root(state)
        assert state == original

    def test_nested_dict_not_mutated(self) -> None:
        original = {"level1": {"level2": {"a": 1, "b": 2}, "x": 10}, "y": 20}
        state = {"level1": dict(original["level1"]), "y": original["y"]}
        state["level1"]["level2"] = dict(original["level1"]["level2"])
        _ = derive_state_root(state)
        assert state == original


# ======================================================================
# Test 7 — NaN Is Rejected
# ======================================================================


class TestNaNRejection:
    """NaN values MUST be rejected with an exception."""

    def test_nan_at_top_level(self) -> None:
        with pytest.raises(ValueError, match="NaN"):
            derive_state_root(float("nan"))

    def test_nan_in_dict(self) -> None:
        with pytest.raises(ValueError, match="NaN"):
            derive_state_root({"value": float("nan")})

    def test_nan_in_nested_dict(self) -> None:
        with pytest.raises(ValueError, match="NaN"):
            derive_state_root({"nested": {"value": float("nan")}})

    def test_nan_in_list(self) -> None:
        with pytest.raises(ValueError, match="NaN"):
            derive_state_root([1, float("nan"), 3])


# ======================================================================
# Test 8 — Infinity Is Rejected
# ======================================================================


class TestInfinityRejection:
    """Infinity values MUST be rejected with an exception."""

    def test_pos_inf_at_top_level(self) -> None:
        with pytest.raises(ValueError, match="Infinity"):
            derive_state_root(float("inf"))

    def test_neg_inf_at_top_level(self) -> None:
        with pytest.raises(ValueError, match="Infinity"):
            derive_state_root(float("-inf"))

    def test_pos_inf_in_dict(self) -> None:
        with pytest.raises(ValueError, match="Infinity"):
            derive_state_root({"value": float("inf")})

    def test_neg_inf_in_nested_dict(self) -> None:
        with pytest.raises(ValueError, match="Infinity"):
            derive_state_root({"nested": {"value": float("-inf")}})


# ======================================================================
# Test 9 — Unsupported Object Is Rejected
# ======================================================================


class TestUnsupportedObjectRejection:
    """Unsupported runtime object types MUST be rejected."""

    def test_custom_object(self) -> None:
        class Custom:
            pass

        with pytest.raises((ValueError, TypeError)):
            derive_state_root(Custom())

    def test_set(self) -> None:
        with pytest.raises((ValueError, TypeError)):
            derive_state_root({1, 2, 3})

    def test_custom_in_dict(self) -> None:
        class Custom:
            pass

        with pytest.raises((ValueError, TypeError)):
            derive_state_root({"obj": Custom()})


# ======================================================================
# Test 10 — Repeated Derivation Is Byte-Stable
# ======================================================================


class TestRepeatedDerivationByteStable:
    """Repeated derivation of the same state MUST produce identical roots."""

    def test_repeated_same_state(self) -> None:
        state = {"a": 1, "b": [2, 3, {"nested": True}], "c": "hello"}
        roots = [derive_state_root(state) for _ in range(100)]
        assert all(r == roots[0] for r in roots)

    def test_root_is_hex(self) -> None:
        root = derive_state_root({"test": True})
        assert isinstance(root, str)
        assert len(root) == 64
        int(root, 16)  # verify valid hex

    def test_root_is_lowercase(self) -> None:
        root = derive_state_root({"test": True})
        assert root == root.lower()


# ======================================================================
# Test 11 — Empty Dict Is Valid
# ======================================================================


class TestEmptyDictValid:
    """An empty dictionary MUST be a valid state input."""

    def test_empty_dict(self) -> None:
        root = derive_state_root({})
        assert isinstance(root, str)
        assert len(root) == 64

    def test_empty_dict_repeatable(self) -> None:
        root1 = derive_state_root({})
        root2 = derive_state_root({})
        assert root1 == root2

    def test_nested_empty_dict(self) -> None:
        root = derive_state_root({"nested": {}})
        assert isinstance(root, str)
        assert len(root) == 64


# ======================================================================
# Test 12 — Empty List Is Valid
# ======================================================================


class TestEmptyListValid:
    """An empty list MUST be a valid state input."""

    def test_empty_list(self) -> None:
        root = derive_state_root([])
        assert isinstance(root, str)
        assert len(root) == 64

    def test_empty_list_repeatable(self) -> None:
        root1 = derive_state_root([])
        root2 = derive_state_root([])
        assert root1 == root2

    def test_list_with_empty_list(self) -> None:
        root = derive_state_root({"items": []})
        assert isinstance(root, str)
        assert len(root) == 64


# ======================================================================
# Additional edge cases
# ======================================================================


class TestStateRootEdgeCases:
    """Additional edge cases for state root derivation."""

    def test_none_state(self) -> None:
        root = derive_state_root(None)
        assert isinstance(root, str)
        assert len(root) == 64

    def test_bool_state(self) -> None:
        root1 = derive_state_root(True)
        root2 = derive_state_root(True)
        assert root1 == root2

    def test_int_state(self) -> None:
        root1 = derive_state_root(42)
        root2 = derive_state_root(42)
        assert root1 == root2

    def test_string_state(self) -> None:
        root1 = derive_state_root("hello")
        root2 = derive_state_root("hello")
        assert root1 == root2

    def test_unicode_state(self) -> None:
        root1 = derive_state_root("café")
        nfd = "cafe\u0301"
        root2 = derive_state_root(nfd)
        assert root1 == root2  # NFC normalization

    def test_mixed_nested_state(self) -> None:
        state = {
            "users": [
                {"name": "alice", "balance": 100},
                {"name": "bob", "balance": 200},
            ],
            "config": {"version": 1, "active": True},
        }
        root = derive_state_root(state)
        assert isinstance(root, str)
        assert len(root) == 64

    def test_domain_separated_from_other_hashes(self) -> None:
        """State roots should differ from transaction hashes for same data."""
        from src.security.hashing import hash_transaction

        state = {"a": 1}
        state_root = derive_state_root(state)
        tx_hash = hash_transaction(state)
        assert state_root != tx_hash