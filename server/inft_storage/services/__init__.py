"""
iNFT Storage Services

Provides core services for iNFT memory management including:
- 0G Storage synchronization
- Logic gates for consciousness evolution
- Memory health monitoring
"""

from .sync import (
    ZeroGStorageClient,
    sync_to_0g_storage,
    log_event_to_0g,
    restore_from_0g_storage
)

from .logic_gates import (
    calculate_consciousness_score,
    should_transition_phase,
    evaluate_interaction_complexity,
    check_memory_health
)

__all__ = [
    # Sync services
    "ZeroGStorageClient",
    "sync_to_0g_storage",
    "log_event_to_0g",
    "restore_from_0g_storage",
    
    # Logic gate services
    "calculate_consciousness_score",
    "should_transition_phase",
    "evaluate_interaction_complexity",
    "check_memory_health"
]
