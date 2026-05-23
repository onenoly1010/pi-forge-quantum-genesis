from __future__ import annotations

import os
from enum import Enum


class SystemMode(str, Enum):
    CONNECTED = "CONNECTED"
    AIRGAP = "AIRGAP"


class AirgapViolationError(RuntimeError):
    pass


def get_system_mode() -> SystemMode:
    raw = os.getenv("OINIO_SYSTEM_MODE", os.getenv("SYSTEM_MODE", "CONNECTED"))
    raw = raw.strip().upper()

    if raw == "AIRGAP":
        return SystemMode.AIRGAP
    return SystemMode.CONNECTED


def is_airgap() -> bool:
    return get_system_mode() == SystemMode.AIRGAP


def require_network_allowed(operation: str = "network operation") -> None:
    if is_airgap():
        raise AirgapViolationError(
            f"{operation} forbidden: OINIO_SYSTEM_MODE=AIRGAP"
        )
