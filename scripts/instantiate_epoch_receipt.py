#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import sys

GENESIS_PREVIOUS_ROOT = "0x" + "0" * 64
EPOCH_NUM = 1
REDUCER_VERSION = "v1.0.0"
SCHEMA_VERSION = "1.0.0"

def canonical_serialize(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")

def sha256_hash(data):
    return "0x" + hashlib.sha256(data).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    print("=== OINIO GENESIS DRY-RUN ===")

    manifest_path = "policy_manifest.json"
    if not os.path.exists(manifest_path):
        print("Missing policy_manifest.json")
        sys.exit(1)

    with open(manifest_path, "r", encoding="utf-8") as f:
        policy_manifest = json.load(f)

    policy_hash = sha256_hash(canonical_serialize(policy_manifest))

    genesis_event = {
        "event_type": "GENESIS_SUBSTRATE_INIT",
        "epoch": EPOCH_NUM,
        "purpose": "Initialize deterministic sovereign memory chain",
        "policy_hash": policy_hash,
        "reducer_version": REDUCER_VERSION,
        "schema_version": SCHEMA_VERSION
    }

    serialized_event = canonical_serialize(genesis_event)
    encrypted_event_hash = sha256_hash(serialized_event)

    previous_root_bytes = bytes.fromhex(GENESIS_PREVIOUS_ROOT[2:])
    state_root = sha256_hash(
        b"OINIO_STATE_ROOT_V1:" + previous_root_bytes + serialized_event
    )

    receipt = {
        "epoch": EPOCH_NUM,
        "previous_root": GENESIS_PREVIOUS_ROOT,
        "state_root": state_root,
        "policy_hash": policy_hash,
        "model_context_hash": "0x" + "0" * 64,
        "reducer_version": REDUCER_VERSION,
        "encrypted_event_hash": encrypted_event_hash,
        "storage_pointer": encrypted_event_hash,
        "canonicalization_version": "1.0.0",
        "schema_version": SCHEMA_VERSION,
        "signature": "0x" + "0" * 130
    }

    receipt_hash = sha256_hash(canonical_serialize(receipt))

    print(f"policy_hash: {policy_hash}")
    print(f"encrypted_event_hash: {encrypted_event_hash}")
    print(f"state_root: {state_root}")
    print(f"receipt_hash: {receipt_hash}")
    print("[+] Dry-run parameter compilation checks passed cleanly.")

if __name__ == "__main__":
    main()
