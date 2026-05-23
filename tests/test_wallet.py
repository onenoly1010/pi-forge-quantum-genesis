"""Deterministic wallet layer — Ed25519, BLAKE3 address derivation, replay-safe tests."""

import pytest

from src.security.wallet import (
    KeyPair,
    WalletIdentity,
    derive_address,
    export_private_key,
    export_public_key,
    generate_keypair,
    import_private_key,
    import_public_key,
    sign_message,
    verify_signature,
)


# ======================================================================
# Test 1 — Deterministic Address Derivation
# ======================================================================


class TestDeterministicAddressDerivation:
    """Same public key MUST always derive the same address."""

    def test_repeated_derivation(self) -> None:
        kp = generate_keypair()
        addr1 = derive_address(kp.public_key)
        addr2 = derive_address(kp.public_key)
        assert addr1 == addr2

    def test_repeated_derivation_100_times(self) -> None:
        kp = generate_keypair()
        addresses = [derive_address(kp.public_key) for _ in range(100)]
        assert all(a == addresses[0] for a in addresses)

    def test_address_is_lowercase_hex(self) -> None:
        kp = generate_keypair()
        addr = derive_address(kp.public_key)
        assert addr == addr.lower()
        # Verify it's valid hex
        int(addr, 16)

    def test_address_length(self) -> None:
        kp = generate_keypair()
        addr = derive_address(kp.public_key)
        assert len(addr) == 40

    def test_derivation_is_pure(self) -> None:
        """Two calls with identical bytes produce identical address."""
        kp = generate_keypair()
        pk_bytes = bytes(kp.public_key)
        a1 = derive_address(pk_bytes)
        a2 = derive_address(bytes(pk_bytes))
        assert a1 == a2


# ======================================================================
# Test 2 — Unique Address Generation
# ======================================================================


class TestUniqueAddressGeneration:
    """Different keypairs MUST derive different addresses."""

    def test_two_different_keypairs(self) -> None:
        kp1 = generate_keypair()
        kp2 = generate_keypair()
        addr1 = derive_address(kp1.public_key)
        addr2 = derive_address(kp2.public_key)
        assert addr1 != addr2

    def test_multiple_keypairs_unique(self) -> None:
        addresses = set()
        for _ in range(50):
            kp = generate_keypair()
            addr = derive_address(kp.public_key)
            assert addr not in addresses, "All generated addresses must be unique"
            addresses.add(addr)

    def test_all_derived_addresses_unique_length(self) -> None:
        addresses = {derive_address(generate_keypair().public_key) for _ in range(20)}
        assert len(addresses) == 20


# ======================================================================
# Test 3 — Signature Verification Success
# ======================================================================


class TestSignatureVerificationSuccess:
    """Valid signature MUST verify True."""

    def test_valid_signature_verifies(self) -> None:
        kp = generate_keypair()
        message = b"test message"
        sig = sign_message(kp.private_key, message)
        assert verify_signature(kp.public_key, message, sig) is True

    def test_different_messages_all_valid(self) -> None:
        kp = generate_keypair()
        messages = [b"msg1", b"msg2", b"a" * 1000, b"", b"\x00\x01\x02"]
        for msg in messages:
            sig = sign_message(kp.private_key, msg)
            assert verify_signature(kp.public_key, msg, sig) is True

    def test_empty_message(self) -> None:
        kp = generate_keypair()
        sig = sign_message(kp.private_key, b"")
        assert verify_signature(kp.public_key, b"", sig) is True

    def test_binary_message(self) -> None:
        kp = generate_keypair()
        msg = bytes(range(256))
        sig = sign_message(kp.private_key, msg)
        assert verify_signature(kp.public_key, msg, sig) is True


# ======================================================================
# Test 4 — Signature Verification Failure
# ======================================================================


class TestSignatureVerificationFailure:
    """Modified message MUST fail verification."""

    def test_modified_message(self) -> None:
        kp = generate_keypair()
        message = b"original message"
        sig = sign_message(kp.private_key, message)
        assert verify_signature(kp.public_key, b"tampered message", sig) is False

    def test_single_byte_tamper(self) -> None:
        kp = generate_keypair()
        message = b"original message"
        sig = sign_message(kp.private_key, message)
        tampered = bytearray(message)
        tampered[0] ^= 1
        assert verify_signature(kp.public_key, bytes(tampered), sig) is False

    def test_wrong_public_key(self) -> None:
        kp1 = generate_keypair()
        kp2 = generate_keypair()
        message = b"test"
        sig = sign_message(kp1.private_key, message)
        assert verify_signature(kp2.public_key, message, sig) is False


# ======================================================================
# Test 5 — Invalid Signature Rejection
# ======================================================================


class TestInvalidSignatureRejection:
    """Malformed signatures MUST safely return False."""

    def test_empty_signature(self) -> None:
        kp = generate_keypair()
        assert verify_signature(kp.public_key, b"msg", "") is False

    def test_short_signature(self) -> None:
        kp = generate_keypair()
        assert verify_signature(kp.public_key, b"msg", "abcd") is False

    def test_garbage_hex(self) -> None:
        kp = generate_keypair()
        assert verify_signature(kp.public_key, b"msg", "zzzz") is False

    def test_non_hex_string(self) -> None:
        kp = generate_keypair()
        assert verify_signature(kp.public_key, b"msg", "not-hex-str!") is False

    def test_none_signature(self) -> None:
        kp = generate_keypair()
        # noinspection PyTypeChecker
        assert verify_signature(kp.public_key, b"msg", None) is False  # type: ignore

    def test_long_invalid_hex(self) -> None:
        kp = generate_keypair()
        # Valid hex but wrong length for Ed25519 (64 hex chars = 32 bytes, not 64)
        assert verify_signature(kp.public_key, b"msg", "ab" * 32) is False


# ======================================================================
# Test 6 — Export/Import Round Trip
# ======================================================================


class TestExportImportRoundTrip:
    """Exported/imported keys MUST preserve exact bytes."""

    def test_private_key_roundtrip(self) -> None:
        kp = generate_keypair()
        exported = export_private_key(kp.private_key)
        imported = import_private_key(exported)
        assert imported == kp.private_key

    def test_public_key_roundtrip(self) -> None:
        kp = generate_keypair()
        exported = export_public_key(kp.public_key)
        imported = import_public_key(exported)
        assert imported == kp.public_key

    def test_exported_private_key_length(self) -> None:
        kp = generate_keypair()
        exported = export_private_key(kp.private_key)
        assert len(exported) == 64  # 32 bytes → 64 hex chars

    def test_exported_public_key_length(self) -> None:
        kp = generate_keypair()
        exported = export_public_key(kp.public_key)
        assert len(exported) == 64  # 32 bytes → 64 hex chars

    def test_sign_after_import(self) -> None:
        kp = generate_keypair()
        exported = export_private_key(kp.private_key)
        imported = import_private_key(exported)
        message = b"round-trip test"
        sig1 = sign_message(kp.private_key, message)
        sig2 = sign_message(imported, message)
        assert sig1 == sig2
        assert verify_signature(kp.public_key, message, sig1) is True

    def test_verify_after_import_public(self) -> None:
        kp = generate_keypair()
        exported_pub = export_public_key(kp.public_key)
        imported_pub = import_public_key(exported_pub)
        message = b"verify after import"
        sig = sign_message(kp.private_key, message)
        assert verify_signature(imported_pub, message, sig) is True


# ======================================================================
# Test 7 — Hex Encoding Stability
# ======================================================================


class TestHexEncodingStability:
    """Repeated exports MUST produce identical lowercase hex."""

    def test_repeated_private_key_export(self) -> None:
        kp = generate_keypair()
        results = [export_private_key(kp.private_key) for _ in range(50)]
        assert all(r == results[0] for r in results)

    def test_repeated_public_key_export(self) -> None:
        kp = generate_keypair()
        results = [export_public_key(kp.public_key) for _ in range(50)]
        assert all(r == results[0] for r in results)

    def test_export_is_lowercase(self) -> None:
        kp = generate_keypair()
        assert export_private_key(kp.private_key) == export_private_key(kp.private_key).lower()
        assert export_public_key(kp.public_key) == export_public_key(kp.public_key).lower()

    def test_export_no_prefix(self) -> None:
        kp = generate_keypair()
        priv = export_private_key(kp.private_key)
        pub = export_public_key(kp.public_key)
        assert not priv.startswith("0x")
        assert not pub.startswith("0x")


# ======================================================================
# Test 8 — Immutable Model Enforcement
# ======================================================================


class TestImmutableModelEnforcement:
    """Attempting to mutate Pydantic models MUST fail."""

    def test_keypair_frozen(self) -> None:
        kp = generate_keypair()
        with pytest.raises(Exception):
            kp.private_key = b"\x00" * 32  # type: ignore

    def test_keypair_cannot_set_public_key(self) -> None:
        kp = generate_keypair()
        with pytest.raises(Exception):
            kp.public_key = b"\x00" * 32  # type: ignore

    def test_wallet_identity_frozen(self) -> None:
        kp = generate_keypair()
        addr = derive_address(kp.public_key)
        identity = WalletIdentity(
            address=addr,
            public_key=export_public_key(kp.public_key),
            private_key=export_private_key(kp.private_key),
        )
        with pytest.raises(Exception):
            identity.address = "different"  # type: ignore

    def test_wallet_identity_cannot_set_pubkey(self) -> None:
        kp = generate_keypair()
        identity = WalletIdentity(
            address=derive_address(kp.public_key),
            public_key=export_public_key(kp.public_key),
            private_key=export_private_key(kp.private_key),
        )
        with pytest.raises(Exception):
            identity.public_key = "different"  # type: ignore

    def test_wallet_identity_cannot_set_privkey(self) -> None:
        kp = generate_keypair()
        identity = WalletIdentity(
            address=derive_address(kp.public_key),
            public_key=export_public_key(kp.public_key),
            private_key=export_private_key(kp.private_key),
        )
        with pytest.raises(Exception):
            identity.private_key = "different"  # type: ignore


# ======================================================================
# Test 9 — Replay-Stable Signing
# ======================================================================


class TestReplayStableSigning:
    """Signing same message with same key MUST produce identical signature."""

    def test_repeated_signing_same_message(self) -> None:
        kp = generate_keypair()
        message = b"deterministic message"
        sigs = [sign_message(kp.private_key, message) for _ in range(50)]
        assert all(s == sigs[0] for s in sigs)

    def test_repeated_signing_across_process_base(self) -> None:
        """Sign with exported-then-imported key — should match."""
        kp = generate_keypair()
        message = b"test"
        priv_hex = export_private_key(kp.private_key)
        imported_sk = import_private_key(priv_hex)
        sig1 = sign_message(kp.private_key, message)
        sig2 = sign_message(imported_sk, message)
        assert sig1 == sig2

    def test_signature_deterministic_different_calls(self) -> None:
        kp = generate_keypair()
        message = b"deterministic"
        # Generate 3 times in sequence
        sig1 = sign_message(kp.private_key, message)
        sig2 = sign_message(kp.private_key, message)
        sig3 = sign_message(kp.private_key, message)
        assert sig1 == sig2 == sig3

    def test_signature_hex_length(self) -> None:
        kp = generate_keypair()
        sig = sign_message(kp.private_key, b"test")
        # Ed25519 signatures are 64 bytes → 128 hex characters
        assert len(sig) == 128


# ======================================================================
# Test 10 — No Hidden Randomness
# ======================================================================


class TestNoHiddenRandomness:
    """Address derivation and verification MUST remain deterministic."""

    def test_address_pure_function(self) -> None:
        """Same bytes in → same address out, every time."""
        pk_bytes = bytes(range(32))
        a1 = derive_address(pk_bytes)
        a2 = derive_address(pk_bytes)
        a3 = derive_address(bytes(range(32)))
        assert a1 == a2 == a3

    def test_sign_verify_deterministic_roundtrip(self) -> None:
        kp = generate_keypair()
        message = b"deterministic"
        sig = sign_message(kp.private_key, message)
        # Verify many times — must be stable
        for _ in range(50):
            assert verify_signature(kp.public_key, message, sig) is True

    def test_keypair_only_random_function(self) -> None:
        """Ensure that only generate_keypair uses randomness."""
        kp = generate_keypair()
        # derive_address is pure
        addr = derive_address(kp.public_key)
        # Run it again — must match
        assert addr == derive_address(kp.public_key)
        # Export/import are pure
        priv_hex = export_private_key(kp.private_key)
        pub_hex = export_public_key(kp.public_key)
        assert import_private_key(priv_hex) == kp.private_key
        assert import_public_key(pub_hex) == kp.public_key

    def test_no_random_function_outside_keygen(self) -> None:
        """Call all deterministic functions and verify no side-effects on outputs."""
        kp = generate_keypair()
        addr = derive_address(kp.public_key)
        sig = sign_message(kp.private_key, b"test")

        # Repeated calls must be identical
        assert addr == derive_address(kp.public_key)
        assert sig == sign_message(kp.private_key, b"test")

        # verify must be consistent
        assert verify_signature(kp.public_key, b"test", sig) is True
        assert verify_signature(kp.public_key, b"test", sig) is True

        # Export must be consistent
        assert export_private_key(kp.private_key) == export_private_key(kp.private_key)
        assert export_public_key(kp.public_key) == export_public_key(kp.public_key)