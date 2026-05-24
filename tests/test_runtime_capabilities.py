import pytest

from server.security.capabilities import (
    CapabilityBlockedError,
    SystemMode,
    get_system_mode,
    network_allowed,
    require_network_capability,
)


def test_default_mode_connected(monkeypatch):
    monkeypatch.delenv("QPF_SYSTEM_MODE", raising=False)

    assert get_system_mode() == SystemMode.CONNECTED
    assert network_allowed() is True


def test_airgap_blocks_network(monkeypatch):
    monkeypatch.setenv("QPF_SYSTEM_MODE", "AIRGAP")

    assert get_system_mode() == SystemMode.AIRGAP
    assert network_allowed() is False

    with pytest.raises(CapabilityBlockedError):
        require_network_capability("aiohttp.ClientSession")


def test_unknown_mode_fails_open_to_connected(monkeypatch):
    monkeypatch.setenv("QPF_SYSTEM_MODE", "bad-value")

    assert get_system_mode() == SystemMode.CONNECTED
    assert network_allowed() is True
