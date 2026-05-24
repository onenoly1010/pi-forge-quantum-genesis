"""
Runtime capability gates for Quantum Pi Forge.

Default mode is CONNECTED to preserve existing behavior.
Set QPF_SYSTEM_MODE=AIRGAP to block outbound network client creation.
"""

from enum import Enum
import os


class SystemMode(str, Enum):
    CONNECTED = "CONNECTED"
    AIRGAP = "AIRGAP"


class CapabilityBlockedError(RuntimeError):
    pass


def get_system_mode() -> SystemMode:
    raw = os.getenv("QPF_SYSTEM_MODE", SystemMode.CONNECTED.value).upper()

    try:
        return SystemMode(raw)
    except ValueError:
        return SystemMode.CONNECTED


def network_allowed() -> bool:
    return get_system_mode() == SystemMode.CONNECTED


def require_network_capability(surface: str = "network") -> None:
    if not network_allowed():
        raise CapabilityBlockedError(
            f"Network capability blocked in AIRGAP mode: {surface}"
        )
