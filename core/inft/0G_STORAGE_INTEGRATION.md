# 0G Storage Integration for iNFT Memory Persistence

This guide provides comprehensive documentation for integrating 0G Storage with intelligent NFTs (iNFTs) to enable sovereign AI/agent memory persistence, synchronization, and restoration.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Python Integration](#python-integration)
- [TypeScript Integration](#typescript-integration)
- [Security Best Practices](#security-best-practices)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)

## Overview

The 0G Storage integration provides:

- **Encrypted Upload/Download**: Secure transfer of SQLite databases containing AI/agent memory
- **On-Chain Anchoring**: Smart contract pointers for verifiable storage locations
- **Incremental Logs**: Append-only event logs with auto-batching
- **Chain-of-Custody**: Cryptographic validation of storage update sequences
- **Key Rotation**: Support for periodic encryption key updates

## Architecture

```
┌─────────────────┐
│   iNFT Agent    │
│  (AI Memory)    │
└────────┬────────┘
         │
         │ sync/load
         ▼
┌─────────────────┐      ┌─────────────────┐
│  Storage Client │─────▶│   0G Storage    │
│  (Python/TS)    │      │    Network      │
└────────┬────────┘      └─────────────────┘
         │
         │ update pointer
         ▼
┌─────────────────┐
│  Smart Contract │
│ (On-Chain Link) │
└─────────────────┘
```

### Data Flow

1. **Sync to Storage**:
   - Validate SQLite database integrity
   - Encrypt database with Fernet/AES-256-GCM
   - Upload to 0G Storage (content-addressed)
   - Update on-chain pointer with storage hash and checksum

2. **Load from Storage**:
   - Query on-chain pointer for storage hash
   - Download from 0G Storage
   - Verify checksum integrity
   - Decrypt database
   - Validate database integrity

## Python Integration

### Installation

Add required dependencies to your `requirements.txt`:

```txt
web3>=6.0.0
cryptography>=41.0.0
```

### Quick Start

```python
import asyncio
from server.integrations.zero_g_storage import (
    sync_to_0g_storage,
    load_from_0g_storage,
    ZeroGStorageClient,
    generate_encryption_key
)

# Set environment variables
# ZERO_G_RPC=https://evmrpc.0g.ai
# ZERO_G_STORAGE_CONTRACT=0x...
# ZERO_G_PRIVATE_KEY=0x...
# INFT_ENCRYPTION_PASSWORD=your_secure_password

async def main():
    inft_id = "inft_12345"
    
    # Sync database to 0G Storage
    metadata = await sync_to_0g_storage(
        inft_id=inft_id,
        db_path=f"/data/inft_{inft_id}.db"
    )
    print(f"Uploaded: {metadata.file_hash}")
    
    # Load database from 0G Storage
    restored_path = await load_from_0g_storage(
        inft_id=inft_id,
        output_dir="/tmp"
    )
    print(f"Restored to: {restored_path}")

asyncio.run(main())
```

### Advanced Usage

#### Manual Client Configuration

```python
from server.integrations.zero_g_storage import (
    ZeroGStorageClient,
    generate_encryption_key
)

# Generate encryption key from password
password = "your_secure_password"
encryption_key = generate_encryption_key(password)

# Create client with explicit configuration
client = ZeroGStorageClient(
    rpc_url="https://evmrpc.0g.ai",
    storage_contract_address="0x...",
    private_key="0x...",
    encryption_key=encryption_key
)

# Sync with custom options
metadata = await client.sync_to_0g_storage(
    inft_id="inft_12345",
    db_path="/data/my_db.db",
    encrypt=True
)
```

#### Incremental Event Logs

```python
# Append events with auto-batching
event = {
    "action": "decision_made",
    "data": {"choice": "option_a", "confidence": 0.95}
}

storage_hash = await client.append_event_log(
    inft_id="inft_12345",
    event=event,
    auto_batch=True,
    batch_size=100  # Upload after 100 events
)

if storage_hash:
    print(f"Batch uploaded: {storage_hash}")
```

#### Chain-of-Custody Validation

```python
# Validate sequential updates
storage_hashes = [
    "0xabc...",
    "0xdef...",
    "0x123..."
]

is_valid = client.validate_chain_of_custody(
    inft_id="inft_12345",
    storage_hashes=storage_hashes
)
```

## TypeScript Integration

### Installation

Add required dependencies:

```bash
npm install ethers
```

### Quick Start

```typescript
import {
  syncTo0gStorage,
  loadFrom0gStorage,
  ZeroGStorageClient,
  generateEncryptionKey
} from './core/inft/zero-g-storage';

// Set environment variables
// ZERO_G_RPC=https://evmrpc.0g.ai
// ZERO_G_STORAGE_CONTRACT=0x...
// ZERO_G_PRIVATE_KEY=0x...
// INFT_ENCRYPTION_PASSWORD=your_secure_password

async function main() {
  const inftId = 'inft_12345';
  
  // Sync database to 0G Storage
  const metadata = await syncTo0gStorage(
    inftId,
    `/data/inft_${inftId}.db`
  );
  console.log(`Uploaded: ${metadata.fileHash}`);
  
  // Load database from 0G Storage
  const restoredPath = await loadFrom0gStorage(
    inftId,
    '/tmp'
  );
  console.log(`Restored to: ${restoredPath}`);
}

main().catch(console.error);
```

### Advanced Usage

#### Manual Client Configuration

```typescript
import {
  ZeroGStorageClient,
  generateEncryptionKey,
  ZeroGStorageConfig
} from './core/inft/zero-g-storage';

// Generate encryption key from password
const password = 'your_secure_password';
const encryptionKey = generateEncryptionKey(password);

// Create client with explicit configuration
const config: ZeroGStorageConfig = {
  rpcUrl: 'https://evmrpc.0g.ai',
  storageContractAddress: '0x...',
  privateKey: '0x...',
  encryptionKey
};

const client = new ZeroGStorageClient(config);

// Sync with custom options
const metadata = await client.syncTo0gStorage(
  'inft_12345',
  '/data/my_db.db',
  true  // encrypt
);
```

#### Incremental Event Logs

```typescript
// Append events with auto-batching
const event = {
  action: 'decision_made',
  data: { choice: 'option_a', confidence: 0.95 }
};

const storageHash = await client.appendEventLog(
  'inft_12345',
  event,
  true,  // autoBatch
  100    // batchSize
);

if (storageHash) {
  console.log(`Batch uploaded: ${storageHash}`);
}
```

## Security Best Practices

### 1. Key Management

#### Key Generation

```python
# Python
from server.integrations.zero_g_storage import generate_encryption_key

# Generate from strong password + salt
password = "use_a_strong_password_from_secure_source"
salt = os.urandom(16)  # Store this securely!
key = generate_encryption_key(password, salt)
```

```typescript
// TypeScript
import { generateEncryptionKey } from './core/inft/zero-g-storage';
import * as crypto from 'crypto';

// Generate from strong password + salt
const password = 'use_a_strong_password_from_secure_source';
const salt = crypto.randomBytes(16);  // Store this securely!
const key = generateEncryptionKey(password, salt);
```

#### Key Storage

**DO NOT** hardcode encryption keys. Use:
- Environment variables (for development)
- Hardware security modules (HSM) for production
- Key management services (AWS KMS, Azure Key Vault, etc.)
- Encrypted configuration files with restricted access

#### Key Rotation

```python
# Python - Rotate encryption key
new_password = "new_strong_password"
new_key = generate_encryption_key(new_password)
client.rotate_encryption_key(new_key)

# Re-encrypt existing databases
old_client = ZeroGStorageClient(..., encryption_key=old_key)
new_client = ZeroGStorageClient(..., encryption_key=new_key)

# Download with old key, upload with new key
db_path = await old_client.load_from_0g_storage(inft_id)
await new_client.sync_to_0g_storage(inft_id, db_path)
```

```typescript
// TypeScript - Rotate encryption key
const newPassword = 'new_strong_password';
const newKey = generateEncryptionKey(newPassword);
client.rotateEncryptionKey(newKey);

// Re-encrypt existing databases
const oldClient = new ZeroGStorageClient({ ..., encryptionKey: oldKey });
const newClient = new ZeroGStorageClient({ ..., encryptionKey: newKey });

// Download with old key, upload with new key
const dbPath = await oldClient.loadFrom0gStorage(inftId);
await newClient.syncTo0gStorage(inftId, dbPath);
```

### 2. Integrity Validation

Always verify checksums after download:

```python
# Python
restored_path = await client.load_from_0g_storage(
    inft_id,
    verify_checksum=True  # Default, but explicit is better
)
```

```typescript
// TypeScript
const restoredPath = await client.loadFrom0gStorage(
  inftId,
  '/tmp',
  true  // verifyChecksum
);
```

### 3. Access Control

#### Owner-Based Permissions

Implement smart contract access controls:

```solidity
// Example Solidity contract
contract INFTStorage {
    mapping(string => address) public inftOwners;
    mapping(string => StoragePointer) public storagePointers;
    
    modifier onlyOwner(string memory inftId) {
        require(msg.sender == inftOwners[inftId], "Not authorized");
        _;
    }
    
    function updateStoragePointer(
        string memory inftId,
        string memory storageHash,
        string memory checksum
    ) external onlyOwner(inftId) {
        storagePointers[inftId] = StoragePointer({
            storageHash: storageHash,
            checksum: checksum,
            timestamp: block.timestamp
        });
    }
}
```

#### Role-Based Access

```python
# Python - Check ownership before operations
async def authorized_sync(inft_id: str, user_address: str):
    owner = await contract.functions.inftOwners(inft_id).call()
    
    if owner.lower() != user_address.lower():
        raise PermissionError(f"User {user_address} not authorized for iNFT {inft_id}")
    
    return await sync_to_0g_storage(inft_id)
```

### 4. Database Validation

Always validate SQLite integrity before/after operations:

```python
# Python - Built into sync/load operations
import sqlite3

def validate_database(db_path: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check integrity
    cursor.execute("PRAGMA integrity_check")
    result = cursor.fetchone()
    
    if result[0] != "ok":
        raise ValueError(f"Database integrity check failed: {result[0]}")
    
    conn.close()
```

## Advanced Features

### Custom Storage Backend

To integrate with actual 0G Storage SDK:

```python
# Python - Replace placeholder methods
class ZeroGStorageClient:
    async def upload_to_0g_storage(self, file_path: str):
        # Import actual 0G SDK
        from og_storage import StorageClient
        
        og_client = StorageClient(...)
        storage_hash = await og_client.upload(file_path)
        file_size = os.path.getsize(file_path)
        
        return storage_hash, file_size
    
    async def download_from_0g_storage(self, storage_hash: str, output_path: str):
        from og_storage import StorageClient
        
        og_client = StorageClient(...)
        await og_client.download(storage_hash, output_path)
        
        return os.path.getsize(output_path)
```

### Batch Operations

Process multiple iNFTs efficiently:

```python
# Python
async def batch_sync(inft_ids: List[str]):
    tasks = [sync_to_0g_storage(inft_id) for inft_id in inft_ids]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for inft_id, result in zip(inft_ids, results):
        if isinstance(result, Exception):
            print(f"Failed to sync {inft_id}: {result}")
        else:
            print(f"Synced {inft_id}: {result.file_hash}")
```

### Event Log Querying

```python
# Python - Query event logs
async def query_events(inft_id: str, start_time: int, end_time: int):
    log_path = f"/tmp/inft_{inft_id}_events.jsonl"
    
    events = []
    with open(log_path, "r") as f:
        for line in f:
            event_entry = json.loads(line)
            timestamp = datetime.fromisoformat(event_entry["timestamp"]).timestamp()
            
            if start_time <= timestamp <= end_time:
                events.append(event_entry["event"])
    
    return events
```

## Troubleshooting

### Common Issues

#### 1. Checksum Mismatch

**Problem**: Downloaded file checksum doesn't match expected value

**Solutions**:
- Verify 0G Storage network connectivity
- Check for network corruption during download
- Ensure encryption key matches original upload
- Verify on-chain pointer hasn't been tampered with

#### 2. Decryption Fails

**Problem**: Cannot decrypt downloaded database

**Solutions**:
- Confirm encryption key is correct
- Check if file was actually encrypted during upload
- Verify file wasn't corrupted during storage/download
- Ensure key rotation was tracked properly

#### 3. Database Corruption

**Problem**: SQLite integrity check fails

**Solutions**:
- Use WAL mode for concurrent access
- Always close connections properly
- Validate before upload
- Keep backups of critical databases

#### 4. Transaction Failures

**Problem**: On-chain pointer update fails

**Solutions**:
- Verify sufficient gas/balance
- Check smart contract permissions
- Ensure correct network and contract address
- Increase gas limit if needed

### Debug Mode

Enable detailed logging:

```python
# Python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("zero_g_storage")
logger.setLevel(logging.DEBUG)
```

```typescript
// TypeScript
// Set NODE_DEBUG environment variable
process.env.NODE_DEBUG = 'zero-g-storage';
```

## Integration Endpoints

### 0G Storage Network

- **Mainnet RPC**: `https://evmrpc.0g.ai`
- **Chain ID**: 16600
- **Block Explorer**: https://scan.0g.ai

### Smart Contract Deployment

Deploy the storage registry contract:

```solidity
// Deploy with your preferred framework (Hardhat, Foundry, etc.)
npx hardhat run scripts/deploy-storage-registry.js --network 0g
```

### Environment Variables

```bash
# Required
ZERO_G_RPC=https://evmrpc.0g.ai
ZERO_G_STORAGE_CONTRACT=0x...  # Your deployed contract
ZERO_G_PRIVATE_KEY=0x...       # For signing transactions
INFT_ENCRYPTION_PASSWORD=...   # For database encryption

# Optional
ZERO_G_CHAIN_ID=16600
ZERO_G_GAS_LIMIT=500000
```

## Best Practices Summary

1. **Always encrypt** sensitive AI/agent memory
2. **Verify checksums** after every download
3. **Rotate keys** periodically (e.g., quarterly)
4. **Validate database integrity** before and after operations
5. **Use environment variables** for configuration
6. **Implement access controls** in smart contracts
7. **Monitor on-chain pointers** for tampering
8. **Backup encryption keys** securely
9. **Test recovery procedures** regularly
10. **Log all operations** for audit trails

## Support

For issues or questions:
- GitHub Issues: https://github.com/onenoly1010/pi-forge-quantum-genesis/issues
- Documentation: See `/core/inft/README.md`
- 0G Network Docs: https://docs.0g.ai

## License

MIT License - See LICENSE file for details
