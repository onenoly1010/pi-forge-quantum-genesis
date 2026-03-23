"""
Pi Forge Quantum Genesis - iNFT Storage Module

This module provides the memory layer for intelligent NFTs (iNFTs) with:
- Decentralized storage via 0G Storage integration
- Memory continuity across sessions
- Encrypted context management
- Auditable state transitions
- Oracle query tracking
- Financial allocation management
"""

__version__ = "1.0.0"

from .models import (
    INFTState,
    EventLog,
    StateTransition,
    UserContext,
    MemoryContinuity,
    OracleQuery,
    LedgerAllocation
)

from .services.sync import sync_to_0g_storage, log_event_to_0g
from .services.logic_gates import should_transition_phase, calculate_consciousness_score

__all__ = [
    "INFTState",
    "EventLog",
    "StateTransition",
    "UserContext",
    "MemoryContinuity",
    "OracleQuery",
    "LedgerAllocation",
    "sync_to_0g_storage",
    "log_event_to_0g",
    "should_transition_phase",
    "calculate_consciousness_score",
]
