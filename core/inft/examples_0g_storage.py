"""
Example usage of 0G Storage Integration for iNFT Memory

This demonstrates how to use the 0G Storage integration for persisting
and restoring AI/agent memory in a decentralized, encrypted manner.
"""

import asyncio
import os
import sqlite3
import sys
from pathlib import Path

# Add server directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "server"))

from integrations.zero_g_storage import (
    ZeroGStorageClient,
    generate_encryption_key,
    sync_to_0g_storage,
    load_from_0g_storage,
)


async def example_basic_usage():
    """Example: Basic sync and load using convenience functions"""
    print("=" * 60)
    print("Example 1: Basic Sync and Load")
    print("=" * 60)
    
    # Setup (normally from environment variables)
    inft_id = "inft_example_001"
    
    # Create a sample database
    db_path = f"/tmp/inft_{inft_id}.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agent_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER,
            event_type TEXT,
            content TEXT,
            metadata TEXT
        )
    """)
    
    cursor.execute(
        "INSERT INTO agent_memory (timestamp, event_type, content, metadata) VALUES (?, ?, ?, ?)",
        (1234567890, "decision", "Chose option A", '{"confidence": 0.95}')
    )
    
    conn.commit()
    conn.close()
    
    print(f"✓ Created sample database: {db_path}")
    
    # Note: In production, set these environment variables:
    # ZERO_G_RPC, ZERO_G_STORAGE_CONTRACT, ZERO_G_PRIVATE_KEY, INFT_ENCRYPTION_PASSWORD
    
    print(f"\nTo sync in production:")
    print(f"  metadata = await sync_to_0g_storage('{inft_id}')")
    print(f"  # Uploads encrypted DB to 0G Storage and updates on-chain pointer")
    
    print(f"\nTo restore in production:")
    print(f"  restored_path = await load_from_0g_storage('{inft_id}')")
    print(f"  # Downloads from 0G Storage, verifies checksum, decrypts")
    
    # Clean up
    os.remove(db_path)
    print("\n✓ Example complete")


async def example_advanced_client():
    """Example: Advanced usage with explicit client configuration"""
    print("\n" + "=" * 60)
    print("Example 2: Advanced Client Configuration")
    print("=" * 60)
    
    # Generate encryption key from password
    password = "my_secure_password_123"
    encryption_key = generate_encryption_key(password)
    
    print(f"✓ Generated encryption key from password")
    
    # Create client with explicit configuration
    client = ZeroGStorageClient(
        rpc_url="https://evmrpc.0g.ai",
        storage_contract_address="0x1234567890123456789012345678901234567890",
        private_key=None,  # In production, provide actual private key
        encryption_key=encryption_key
    )
    
    print(f"✓ Created ZeroGStorageClient")
    
    # Create a sample database
    inft_id = "inft_example_002"
    db_path = f"/tmp/inft_{inft_id}.db"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE memory (id INTEGER PRIMARY KEY, data TEXT)")
    cursor.execute("INSERT INTO memory (data) VALUES (?)", ("test memory",))
    conn.commit()
    conn.close()
    
    print(f"✓ Created database: {db_path}")
    
    # Sync to 0G Storage
    print(f"\nSyncing to 0G Storage...")
    metadata = await client.sync_to_0g_storage(
        inft_id=inft_id,
        db_path=db_path,
        encrypt=True
    )
    
    print(f"✓ Synced successfully!")
    print(f"  - iNFT ID: {metadata.inft_id}")
    print(f"  - Storage Hash: {metadata.file_hash}")
    print(f"  - Checksum: {metadata.checksum}")
    print(f"  - Size: {metadata.size_bytes} bytes")
    print(f"  - Encryption: {metadata.encryption_key_id}")
    
    # Clean up
    os.remove(db_path)
    print("\n✓ Example complete")


async def example_event_logs():
    """Example: Incremental event logging with auto-batching"""
    print("\n" + "=" * 60)
    print("Example 3: Event Logging with Auto-Batching")
    print("=" * 60)
    
    client = ZeroGStorageClient(
        rpc_url="https://evmrpc.0g.ai",
        storage_contract_address="0x1234567890123456789012345678901234567890",
        encryption_key=generate_encryption_key("password")
    )
    
    inft_id = "inft_example_003"
    
    print(f"Appending events to log for {inft_id}...")
    
    # Append events
    for i in range(5):
        event = {
            "action": f"agent_action_{i}",
            "data": {
                "timestamp": 1234567890 + i,
                "confidence": 0.9 + (i * 0.01),
                "result": f"result_{i}"
            }
        }
        
        storage_hash = await client.append_event_log(
            inft_id=inft_id,
            event=event,
            auto_batch=True,
            batch_size=10  # Will upload after 10 events
        )
        
        if storage_hash:
            print(f"  ✓ Batch uploaded: {storage_hash}")
        else:
            print(f"  · Event {i+1} appended (batch not full)")
    
    # Clean up
    log_path = f"/tmp/inft_{inft_id}_events.jsonl"
    if os.path.exists(log_path):
        os.remove(log_path)
    
    print("\n✓ Example complete")


async def example_encryption_key_rotation():
    """Example: Rotating encryption keys"""
    print("\n" + "=" * 60)
    print("Example 4: Encryption Key Rotation")
    print("=" * 60)
    
    # Original client with old key
    old_password = "old_password_123"
    old_key = generate_encryption_key(old_password)
    
    old_client = ZeroGStorageClient(
        rpc_url="https://evmrpc.0g.ai",
        storage_contract_address="0x1234567890123456789012345678901234567890",
        encryption_key=old_key
    )
    
    print(f"✓ Created client with old encryption key")
    
    # Create and encrypt a database with old key
    inft_id = "inft_example_004"
    db_path = f"/tmp/inft_{inft_id}.db"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE data (id INTEGER PRIMARY KEY, value TEXT)")
    cursor.execute("INSERT INTO data (value) VALUES (?)", ("sensitive data",))
    conn.commit()
    conn.close()
    
    # Sync with old key
    await old_client.sync_to_0g_storage(inft_id, db_path, encrypt=True)
    print(f"✓ Synced with old key")
    
    # Rotate to new key
    new_password = "new_password_456"
    new_key = generate_encryption_key(new_password)
    
    new_client = ZeroGStorageClient(
        rpc_url="https://evmrpc.0g.ai",
        storage_contract_address="0x1234567890123456789012345678901234567890",
        encryption_key=new_key
    )
    
    print(f"✓ Created client with new encryption key")
    
    # Re-encrypt: load with old key, sync with new key
    # (In production, you'd download from 0G Storage first)
    await new_client.sync_to_0g_storage(inft_id, db_path, encrypt=True)
    print(f"✓ Re-encrypted with new key")
    
    # Clean up
    os.remove(db_path)
    print("\n✓ Example complete")


async def example_checksum_validation():
    """Example: Integrity validation with checksums"""
    print("\n" + "=" * 60)
    print("Example 5: Checksum Validation")
    print("=" * 60)
    
    client = ZeroGStorageClient(
        rpc_url="https://evmrpc.0g.ai",
        storage_contract_address="0x1234567890123456789012345678901234567890",
        encryption_key=generate_encryption_key("password")
    )
    
    # Create database
    inft_id = "inft_example_005"
    db_path = f"/tmp/inft_{inft_id}.db"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, data TEXT)")
    cursor.execute("INSERT INTO test (data) VALUES (?)", ("test data",))
    conn.commit()
    conn.close()
    
    # Calculate checksum
    checksum = client.calculate_file_checksum(db_path)
    print(f"✓ Original checksum: {checksum}")
    
    # Sync to storage
    metadata = await client.sync_to_0g_storage(inft_id, db_path, encrypt=False)
    print(f"✓ Uploaded checksum: {metadata.checksum}")
    
    # Verify checksums match
    assert checksum == metadata.checksum, "Checksum mismatch!"
    print(f"✓ Checksums verified!")
    
    # Clean up
    os.remove(db_path)
    print("\n✓ Example complete")


async def main():
    """Run all examples"""
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║     0G Storage Integration Examples for iNFT Memory       ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    await example_basic_usage()
    await example_advanced_client()
    await example_event_logs()
    await example_encryption_key_rotation()
    await example_checksum_validation()
    
    print("\n" + "=" * 60)
    print("All examples completed successfully! 🎉")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Set up environment variables (see core/inft/0G_STORAGE_INTEGRATION.md)")
    print("2. Deploy storage registry contract to 0G Network")
    print("3. Integrate with actual 0G Storage SDK")
    print("4. Test with real iNFT agents")
    print()


if __name__ == "__main__":
    asyncio.run(main())
