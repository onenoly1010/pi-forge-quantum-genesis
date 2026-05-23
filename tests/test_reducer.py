"""Pure deterministic reducer — deterministic, replay-safe tests."""

import pytest

from src.ledger.reducer import reduce_state


# ======================================================================
# Basic action tests
# ======================================================================


class TestStateSet:
    """state.set adds or overwrites keys deterministically."""

    def test_adds_key(self) -> None:
        state = {"a": 1}
        result = reduce_state(state, "state.set", {"key": "b", "value": 2})
        assert result == {"a": 1, "b": 2}

    def test_overwrites_key(self) -> None:
        state = {"a": 1, "b": 2}
        result = reduce_state(state, "state.set", {"key": "b", "value": 99})
        assert result == {"a": 1, "b": 99}

    def test_sets_nested_value(self) -> None:
        state = {}
        result = reduce_state(state, "state.set", {"key": "config", "value": {"mode": "auto"}})
        assert result == {"config": {"mode": "auto"}}

    def test_sets_none_value(self) -> None:
        state = {"a": 1}
        result = reduce_state(state, "state.set", {"key": "b", "value": None})
        assert result == {"a": 1, "b": None}

    def test_sets_bool_value(self) -> None:
        state = {}
        result = reduce_state(state, "state.set", {"key": "active", "value": True})
        assert result == {"active": True}


class TestStateDelete:
    """state.delete removes keys deterministically."""

    def test_removes_key(self) -> None:
        state = {"a": 1, "b": 2}
        result = reduce_state(state, "state.delete", {"key": "b"})
        assert result == {"a": 1}

    def test_missing_key_is_noop(self) -> None:
        state = {"a": 1}
        result = reduce_state(state, "state.delete", {"key": "b"})
        assert result == {"a": 1}

    def test_delete_last_key(self) -> None:
        state = {"a": 1}
        result = reduce_state(state, "state.delete", {"key": "a"})
        assert result == {}


class TestCounterIncrement:
    """counter.increment initializes from 0 and adds deterministically."""

    def test_initializes_missing_key(self) -> None:
        state = {"a": 1}
        result = reduce_state(state, "counter.increment", {"key": "counter", "amount": 5})
        assert result == {"a": 1, "counter": 5}

    def test_adds_to_existing(self) -> None:
        state = {"counter": 10}
        result = reduce_state(state, "counter.increment", {"key": "counter", "amount": 3})
        assert result == {"counter": 13}

    def test_zero_amount(self) -> None:
        state = {"counter": 10}
        result = reduce_state(state, "counter.increment", {"key": "counter", "amount": 0})
        assert result == {"counter": 10}

    def test_multiple_increments(self) -> None:
        state: dict = {}
        state = reduce_state(state, "counter.increment", {"key": "c", "amount": 1})
        state = reduce_state(state, "counter.increment", {"key": "c", "amount": 2})
        state = reduce_state(state, "counter.increment", {"key": "c", "amount": 3})
        assert state == {"c": 6}


# ======================================================================
# No-mutation tests
# ======================================================================


class TestNoMutation:
    """Reducer MUST NOT mutate prior_state or payload."""

    def test_prior_state_not_mutated_state_set(self) -> None:
        original = {"a": 1, "b": 2}
        state = dict(original)
        _ = reduce_state(state, "state.set", {"key": "c", "value": 3})
        assert state == original

    def test_prior_state_not_mutated_state_delete(self) -> None:
        original = {"a": 1, "b": 2}
        state = dict(original)
        _ = reduce_state(state, "state.delete", {"key": "a"})
        assert state == original

    def test_prior_state_not_mutated_counter_increment(self) -> None:
        original = {"counter": 10}
        state = dict(original)
        _ = reduce_state(state, "counter.increment", {"key": "counter", "amount": 5})
        assert state == original

    def test_payload_not_mutated(self) -> None:
        state: dict = {}
        payload = {"key": "test", "value": 42}
        payload_copy = dict(payload)
        _ = reduce_state(state, "state.set", payload)
        assert payload == payload_copy


# ======================================================================
# Determinism tests
# ======================================================================


class TestDeterminism:
    """Repeated reductions with same inputs MUST produce identical outputs."""

    def test_state_set_deterministic(self) -> None:
        state = {"a": 1}
        results = [
            reduce_state(state, "state.set", {"key": "b", "value": 2})
            for _ in range(50)
        ]
        assert all(r == results[0] for r in results)

    def test_state_delete_deterministic(self) -> None:
        state = {"a": 1, "b": 2}
        results = [
            reduce_state(state, "state.delete", {"key": "a"})
            for _ in range(50)
        ]
        assert all(r == results[0] for r in results)

    def test_counter_increment_deterministic(self) -> None:
        state = {"counter": 10}
        results = [
            reduce_state(state, "counter.increment", {"key": "counter", "amount": 3})
            for _ in range(50)
        ]
        assert all(r == results[0] for r in results)

    def test_repeated_reduction_chain(self) -> None:
        """A chain of reductions with identical inputs must be replayable."""
        state: dict = {}
        state = reduce_state(state, "state.set", {"key": "counter", "value": 0})
        state = reduce_state(state, "counter.increment", {"key": "counter", "amount": 5})
        state = reduce_state(state, "state.set", {"key": "user", "value": "alice"})
        expected = dict(state)

        # Replay the exact same chain
        replay: dict = {}
        replay = reduce_state(replay, "state.set", {"key": "counter", "value": 0})
        replay = reduce_state(replay, "counter.increment", {"key": "counter", "amount": 5})
        replay = reduce_state(replay, "state.set", {"key": "user", "value": "alice"})
        assert replay == expected


# ======================================================================
# Validation rejection tests
# ======================================================================


class TestValidationRejection:
    """Invalid inputs MUST raise appropriate exceptions."""

    def test_unsupported_action(self) -> None:
        with pytest.raises(ValueError, match="unsupported action"):
            reduce_state({}, "unknown.action", {})

    def test_empty_action(self) -> None:
        with pytest.raises(ValueError, match="action must not be empty"):
            reduce_state({}, "", {})

    def test_non_dict_prior_state(self) -> None:
        with pytest.raises(TypeError, match="prior_state must be a dict"):
            reduce_state("not-a-dict", "state.set", {"key": "a", "value": 1})  # type: ignore

    def test_non_dict_payload(self) -> None:
        with pytest.raises(TypeError, match="payload must be a dict"):
            reduce_state({}, "state.set", "not-a-dict")  # type: ignore

    def test_state_set_empty_key(self) -> None:
        with pytest.raises(ValueError, match="key must be a non-empty string"):
            reduce_state({}, "state.set", {"key": "", "value": 1})

    def test_state_set_missing_key(self) -> None:
        with pytest.raises(ValueError, match="missing 'key'"):
            reduce_state({}, "state.set", {"value": 1})

    def test_state_set_missing_value(self) -> None:
        with pytest.raises(ValueError, match="missing 'value'"):
            reduce_state({}, "state.set", {"key": "a"})

    def test_state_delete_empty_key(self) -> None:
        with pytest.raises(ValueError, match="key must be a non-empty string"):
            reduce_state({}, "state.delete", {"key": ""})

    def test_state_delete_missing_key(self) -> None:
        with pytest.raises(ValueError, match="missing 'key'"):
            reduce_state({}, "state.delete", {})

    def test_counter_increment_empty_key(self) -> None:
        with pytest.raises(ValueError, match="key must be a non-empty string"):
            reduce_state({}, "counter.increment", {"key": "", "amount": 1})

    def test_counter_increment_missing_key(self) -> None:
        with pytest.raises(ValueError, match="missing 'key'"):
            reduce_state({}, "counter.increment", {"amount": 1})

    def test_counter_increment_missing_amount(self) -> None:
        with pytest.raises(ValueError, match="missing 'amount'"):
            reduce_state({}, "counter.increment", {"key": "c"})

    def test_counter_increment_negative_amount(self) -> None:
        with pytest.raises(ValueError, match="amount must be non-negative"):
            reduce_state({}, "counter.increment", {"key": "c", "amount": -1})

    def test_counter_increment_float_amount(self) -> None:
        with pytest.raises(ValueError, match="amount must be an integer"):
            reduce_state({}, "counter.increment", {"key": "c", "amount": 1.5})  # type: ignore

    def test_counter_increment_non_integer_current(self) -> None:
        with pytest.raises(ValueError, match="must be an integer"):
            reduce_state(
                {"counter": "not-an-int"},
                "counter.increment",
                {"key": "counter", "amount": 1},
            )

    def test_counter_increment_bool_amount(self) -> None:
        with pytest.raises(ValueError, match="amount must be an integer"):
            reduce_state({}, "counter.increment", {"key": "c", "amount": True})  # type: ignore


# ======================================================================
# Return value type tests
# ======================================================================


class TestReturnValue:
    """Reducer MUST always return a new dict."""

    def test_returns_new_dict_state_set(self) -> None:
        state = {"a": 1}
        result = reduce_state(state, "state.set", {"key": "b", "value": 2})
        assert isinstance(result, dict)
        assert result is not state

    def test_returns_new_dict_counter_increment(self) -> None:
        state = {"counter": 10}
        result = reduce_state(state, "counter.increment", {"key": "counter", "amount": 1})
        assert isinstance(result, dict)
        assert result is not state

    def test_returns_new_dict_state_delete(self) -> None:
        state = {"a": 1}
        result = reduce_state(state, "state.delete", {"key": "a"})
        assert isinstance(result, dict)
        assert result is not state

    def test_results_are_independent(self) -> None:
        state = {"a": 1}
        r1 = reduce_state(state, "state.set", {"key": "b", "value": 2})
        r2 = reduce_state(state, "state.set", {"key": "c", "value": 3})
        assert r1 == {"a": 1, "b": 2}
        assert r2 == {"a": 1, "c": 3}