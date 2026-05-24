"""
Quantum Pi Forge - Network Configuration
"""

ZERO_G_CONFIG = {
    "network": "mainnet",
    "chain_name": "0G Aristotle Mainnet",
    "chain_id": 16661,
    "rpc_url": "https://evmrpc.0g.ai",
    "explorer": "https://chainscan.0g.ai",
    "block_explorer": "https://chainscan.0g.ai",
    "native_token": {
        "name": "0G",
        "symbol": "A0GI",
        "decimals": 18,
    },
    "contracts": {
        "w0g": {
            "name": "Wrapped 0G",
            "symbol": "W0G",
            "address": "0x0000000000000000000000000000000000000000",
            "decimals": 18,
        },
        "factory": {
            "name": "0G Swap Factory",
            "address": "0x0000000000000000000000000000000000000000",
        },
        "router": {
            "name": "0G Swap Router",
            "address": "0x0000000000000000000000000000000000000000",
        },
    },
}

PI_NETWORK_CONFIG = {
    "network": "mainnet",
    "mode": "mainnet",
    "chain_name": "Pi Network",
    "chain_id": "pi-mainnet",
    "rpc_url": "",
    "explorer": "https://blockexplorer.minepi.com",
    "block_explorer": "https://blockexplorer.minepi.com",
    "native_token": {
        "name": "Pi",
        "symbol": "PI",
        "decimals": 7,
    },
    "contracts": {},
}

NETWORK_CONFIGS = {
    "zero_g": ZERO_G_CONFIG,
    "0g": ZERO_G_CONFIG,
    "pi_network": PI_NETWORK_CONFIG,
    "pi": PI_NETWORK_CONFIG,
}


def validate_zero_g_config():
    required = [
        "network",
        "chain_name",
        "chain_id",
        "rpc_url",
        "explorer",
        "block_explorer",
        "native_token",
        "contracts",
    ]

    for key in required:
        if key not in ZERO_G_CONFIG:
            return False

    token = ZERO_G_CONFIG["native_token"]
    if not isinstance(token, dict):
        return False

    for key in ["name", "symbol", "decimals"]:
        if key not in token:
            return False

    contracts = ZERO_G_CONFIG["contracts"]
    if not isinstance(contracts, dict):
        return False

    for key in ["w0g", "factory", "router"]:
        if key not in contracts:
            return False

    return True


def get_zero_g_explorer_url(value="", resource_type="tx"):
    base = ZERO_G_CONFIG["block_explorer"]

    if not value:
        return base

    return f"{base}/{resource_type}/{value}"


def get_network_config(network_name="zero_g"):
    return NETWORK_CONFIGS.get(network_name, {})


__all__ = [
    "ZERO_G_CONFIG",
    "PI_NETWORK_CONFIG",
    "NETWORK_CONFIGS",
    "validate_zero_g_config",
    "get_zero_g_explorer_url",
    "get_network_config",
]
