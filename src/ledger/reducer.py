"""Pure deterministic reducer for 0G-aligned ledger systems.

Provides a single pure function ``reduce_state`` that applies deterministic
actions (``state.set``, ``state.delete``, ``counter.increment``) to a state
dictionary without mutating inputs.
"""

import copy
from typing import Any, Dict


def reduce_state(
    prior_state: Dict[str, object],
    action: str,
    payload: Dict[str, object],
) -> Dict[str, object]:
    """Apply a deterministic *action* to *prior_state*, returning a new state.

    This function is:
    * pure — no side-effects, no mutation of inputs, no I/O
    * deterministic — identical inputs produce identical outputs
    * replay-safe — cross-platform stable

    Args:
        prior_state: The current state dictionary (must be a dict).
        action: The action name (``state.set``, ``state.delete``, or
            ``counter.increment``).
        payload: Action-specific parameters (must be a dict).

    Returns:
        A new state dictionary representing the result of applying *action*.

    Raises:
        TypeError: If *prior_state* or *payload* is not a dict.
        ValueError: If *action* is empty, unsupported, or payload validation
            fails (missing/empty keys, negative amounts, invalid types).
    """
    # --- Input type validation ---
    if not isinstance(prior_state, dict):
        raise TypeError("prior_state must be a dict")
    if not isinstance(payload, dict):
        raise TypeError("payload must be a dict")

    # --- Action validation ---
    if not action:
        raise ValueError("action must not be empty")
    if action not in _ACTION_DISPATCH:
        raise ValueError(f"unsupported action: {action!r}")

    # --- Dispatch ---
    # Deep-copy to guarantee no mutation of prior_state
    new_state = copy.deepcopy(prior_state)
    return _ACTION_DISPATCH[action](new_state, payload)


# ---------------------------------------------------------------------------
# Dispatch table
# ---------------------------------------------------------------------------

_ACTION_DISPATCH: Dict[str, Any] = {}


def _register(action: str) -> Any:
    """Decorator to register an action handler."""
    def decorator(func: Any) -> Any:
        _ACTION_DISPATCH[action] = func
        return func
    return decorator


# ---------------------------------------------------------------------------
# Action handlers
# ---------------------------------------------------------------------------


@_register("state.set")
def _state_set(state: Dict[str, object], payload: Dict[str, object]) -> Dict[str, object]:
    """Set ``state[key] = value``.

    Payload: ``{"key": "...", "value": ...}``
    """
    key = payload.get("key")
    if key is None:
        raise ValueError("state.set: missing 'key' in payload")
    if not isinstance(key, str) or not key:
        raise ValueError("state.set: key must be a non-empty string")

    if "value" not in payload:
        raise ValueError("state.set: missing 'value' in payload")

    value = payload["value"]
    state[str(key)] = value
    return state


@_register("state.delete")
def _state_delete(state: Dict[str, object], payload: Dict[str, object]) -> Dict[str, object]:
    """Remove *key* from state if present.

    Payload: ``{"key": "..."}``

    Deleting an absent key is a deterministic no-op.
    """
    key = payload.get("key")
    if key is None:
        raise ValueError("state.delete: missing 'key' in payload")
    if not isinstance(key, str) or not key:
        raise ValueError("state.delete: key must be a non-empty string")

    state.pop(str(key), None)
    return state


@_register("counter.increment")
def _counter_increment(state: Dict[str, object], payload: Dict[str, object]) -> Dict[str, object]:
    """Increment a counter in state.

    Payload: ``{"key": "...", "amount": <int>}``

    If *key* does not exist in state, it is initialised to 0 first.
    """
    key = payload.get("key")
    if key is None:
        raise ValueError("counter.increment: missing 'key' in payload")
    if not isinstance(key, str) or not key:
        raise ValueError("counter.increment: key must be a non-empty string")

    amount = payload.get("amount")
    if amount is None:
        raise ValueError("counter.increment: missing 'amount' in payload")
    if not isinstance(amount, int) or isinstance(amount, bool):
        raise ValueError("counter.increment: amount must be an integer")
    if amount < 0:
        raise ValueError("counter.increment: amount must be non-negative")

    str_key = str(key)
    current = state.get(str_key, 0)
    if not isinstance(current, int) or isinstance(current, bool):
        raise ValueError(
            f"counter.increment: current value for key {key!r} must be an integer, "
            f"got {type(current).__name__}"
        )
    state[str_key] = current + amount
    return state