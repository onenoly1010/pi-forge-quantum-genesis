from __future__ import annotations

import os
from enum import Enum


class SystemMode(str, Enum):
    NORMAL = "NORMAL"
    AIRGAP = "AIRGAP"


def get_system_mode() -> SystemMode:
    raw = os.getenv("OINIO_SYSTEM_MODE", "NORMAL").strip().upper()
    if raw == "AIRGAP":
        return SystemMode.AIRGAP
    return SystemMode.NORMAL


def is_airgap() -> bool:
    return get_system_mode() == SystemMode.AIRGAP


def require_network_allowed() -> None:
    if is_airgap():
        raise RuntimeError("network access forbidden: OINIO_SYSTEM_MODE=AIRGAP")
