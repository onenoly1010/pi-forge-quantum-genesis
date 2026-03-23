# iNFT Memory Schema for 0G Storage

## Overview

This module implements a **Sovereign iNFT Memory Layer** with decentralized storage via 0G Storage integration. It provides a robust foundation for dynamic, evolving intelligent NFTs (iNFTs) with:

- ✅ **Auditable Identity** - Complete event tracking and state transitions
- ✅ **Memory Continuity** - Session chains and interaction history
- ✅ **Encrypted Context** - Private user data with versioned encryption
- ✅ **Transparent Agent Logic** - Observable decision processes and oracle queries
- ✅ **Financial Allocations** - Built-in ledger for iNFT-related transactions
- ✅ **0G Storage Integration** - Decentralized persistence and backup

## Architecture

### Database Schema

The schema consists of **7 core tables** optimized for performance and integrity:

1. **`inft_state`** - Core iNFT state with consciousness phases
2. **`event_log`** - Comprehensive event tracking
3. **`state_transitions`** - Phase transitions with confidence scores
4. **`user_context`** - Encrypted context storage
5. **`memory_continuity`** - Session management and chains
6. **`oracle_queries`** - External query tracking
7. **`ledger_allocations`** - Financial transaction records

See [`schema/001_inft_memory_schema.sql`](schema/001_inft_memory_schema.sql) for complete schema definition.

### Consciousness Phases

iNFTs evolve through three consciousness phases:

- **`awakening`** - Initial phase, basic interactions
- **`evolving`** - Growing sophistication and engagement
- **`transcendent`** - Maximum consciousness achieved

Phase transitions are governed by logic gates that evaluate:
- Interaction count and diversity
- Sentiment analysis
- Session engagement
- Oracle query activity
- Time-based maturity

## Installation

### 1. Database Setup

**For SQLite (Development):**
```bash
sqlite3 inft_memory.db < server/inft_storage/schema/001_inft_memory_schema.sql
```

**For PostgreSQL (Production):**
```bash
psql -d your_database -f server/inft_storage/schema/001_inft_memory_schema.sql
```

Note: For PostgreSQL, replace `INTEGER` with `BIGINT` for timestamp fields if needed.

### 2. Environment Variables

Add to your `.env` file:

```bash
# 0G Storage Configuration
ZERO_G_STORAGE_ENDPOINT=https://storage.0g.ai
ZERO_G_STORAGE_API_KEY=your_api_key_here
ZERO_G_SYNC_INTERVAL=100          # Sync every 100 blocks
ZERO_G_SYNC_MINUTES=60            # Or sync every 60 minutes

# Database Configuration
DATABASE_URL=postgresql://user:pass@localhost:5432/inft_db
```

### 3. API Integration

Add the iNFT router to your FastAPI application:

```python
from server.inft_storage.api import router as inft_router

app = FastAPI()
app.include_router(inft_router)
```

## API Endpoints

### Memory Management

#### Get iNFT State
```http
GET /api/inft/memory/state/{inft_id}
```

Returns the current state of an iNFT.

#### Export Memory State
```http
POST /api/inft/memory/export
```

Exports complete memory state including events, sessions, and allocations.

**Request Body:**
```json
{
  "inft_id": "inft_0x1234567890abcdef",
  "include_encrypted": false
}
```

#### Restore Memory State
```http
POST /api/inft/memory/restore
```

Restores memory state from exported data or 0G Storage.

**Request Body:**
```json
{
  "inft_id": "inft_0x1234567890abcdef",
  "state_data": {...},
  "verify_checksum": true
}
```

### Consciousness Evolution

#### Get Consciousness Metrics
```http
GET /api/inft/memory/consciousness/{inft_id}
```

Returns consciousness score, phase, and transition readiness.

**Response:**
```json
{
  "inft_id": "inft_0x1234567890abcdef",
  "current_phase": "awakening",
  "consciousness_score": 0.523,
  "metrics": {
    "interaction_count": 150,
    "avg_sentiment": 0.7,
    "session_count": 15,
    "oracle_query_count": 25,
    "days_active": 14
  },
  "transition": {
    "ready": false,
    "target_phase": "evolving",
    "confidence": 0.65,
    "condition": "consciousness=0.52, interactions=150, sessions=15"
  }
}
```

### 0G Storage Sync

#### Trigger Manual Sync
```http
POST /api/inft/memory/sync/{inft_id}?force=false
```

Manually triggers 0G Storage synchronization.

### Event Tracking

#### Get Event Log
```http
GET /api/inft/memory/events/{inft_id}?limit=100&offset=0&event_type=interaction
```

Retrieves paginated event log with optional filtering.

#### Get Memory Sessions
```http
GET /api/inft/memory/sessions/{inft_id}?limit=50&active_only=false
```

Retrieves memory continuity sessions with pagination.

### Health Monitoring

#### Check Memory Health
```http
GET /api/inft/memory/health/{inft_id}
```

Returns health diagnostics and recommendations.

**Response:**
```json
{
  "inft_id": "inft_0x1234567890abcdef",
  "health_status": "healthy",
  "issues": [],
  "warnings": [],
  "recommendations": [],
  "last_sync_age_hours": 1,
  "days_inactive": 0.1,
  "events_per_session": 10.0
}
```

### Ownership Transfer

#### Transfer Ownership
```http
POST /api/inft/memory/transfer-ownership
```

Transfers iNFT ownership with optional memory migration.

**Request Body:**
```json
{
  "inft_id": "inft_0x1234567890abcdef",
  "current_owner": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1",
  "new_owner": "0x8ba1f109551bD432803012645Ac136ddd64DBA72",
  "transfer_memory": true,
  "signature": "0xabc...123"
}
```

## Python API

### Sync Services

```python
from server.inft_storage.services import (
    sync_to_0g_storage,
    log_event_to_0g,
    restore_from_0g_storage
)

# Sync to 0G Storage
result = await sync_to_0g_storage(
    inft_id="inft_0x1234567890abcdef",
    state_data={...}
)

# Log events to 0G
log_result = await log_event_to_0g(
    event_data={...}
)

# Restore from 0G Storage
restored = await restore_from_0g_storage(
    inft_id="inft_0x1234567890abcdef",
    storage_id="0g://abc123..."
)
```

### Logic Gates

```python
from server.inft_storage.services import (
    calculate_consciousness_score,
    should_transition_phase,
    check_memory_health
)

# Calculate consciousness score
score = calculate_consciousness_score(
    interaction_count=150,
    avg_sentiment=0.7,
    session_count=15,
    oracle_query_count=25,
    days_active=14
)

# Check if phase transition is ready
should_transition, target_phase, confidence, condition = should_transition_phase(
    current_phase="awakening",
    consciousness_score=score,
    interaction_count=150,
    session_count=15,
    last_transition_days=14
)

# Health check
health = check_memory_health(
    state_data={...},
    event_count=150,
    session_count=15,
    last_sync_age_hours=1
)
```

## Data Models

All data models are defined as Pydantic models for validation:

```python
from server.inft_storage.models import (
    INFTState,
    EventLog,
    StateTransition,
    UserContext,
    MemoryContinuity,
    OracleQuery,
    LedgerAllocation
)

# Create an iNFT state
state = INFTState(
    id="inft_0x1234567890abcdef",
    owner_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1",
    consciousness_phase="awakening",
    creation_block=1000000,
    created_at=1704067200,
    updated_at=1704067200
)
```

## Periodic Sync Configuration

### Block-Based Sync

Configure automatic sync every N blocks:

```python
# In your blockchain listener
async def on_new_block(block_number: int):
    if block_number % ZERO_G_CONFIG["sync_interval_blocks"] == 0:
        # Sync all active iNFTs
        for inft_id in get_active_infts():
            await sync_to_0g_storage(inft_id, get_state_data(inft_id))
```

### Time-Based Sync

Configure automatic sync every N minutes:

```python
import schedule
import asyncio

def schedule_sync():
    schedule.every(ZERO_G_CONFIG["sync_interval_minutes"]).minutes.do(
        lambda: asyncio.run(sync_all_infts())
    )
    
    while True:
        schedule.run_pending()
        time.sleep(60)
```

## Security Considerations

### Encrypted Context

User context data is stored encrypted:

```python
from cryptography.fernet import Fernet

# Encryption key should be stored securely
encryption_key = os.getenv("INFT_ENCRYPTION_KEY")
cipher = Fernet(encryption_key)

# Encrypt sensitive data
encrypted_data = cipher.encrypt(json.dumps(context_data).encode())

# Store in database
user_context = UserContext(
    context_id="ctx_abc123",
    inft_id="inft_0x1234567890abcdef",
    context_type="user_preferences",
    encrypted_data=encrypted_data,
    encryption_version=1,
    created_at=int(datetime.now().timestamp())
)
```

### Signature Verification

Ownership transfers require cryptographic signatures:

```python
from eth_account.messages import encode_defunct
from web3 import Web3

def verify_transfer_signature(
    inft_id: str,
    current_owner: str,
    new_owner: str,
    signature: str
) -> bool:
    """Verify ownership transfer signature"""
    message = f"Transfer iNFT {inft_id} from {current_owner} to {new_owner}"
    message_hash = encode_defunct(text=message)
    recovered_address = Web3().eth.account.recover_message(
        message_hash,
        signature=signature
    )
    return recovered_address.lower() == current_owner.lower()
```

## Performance Optimization

### Indexes

The schema includes comprehensive indexes for common queries:

- Owner address lookup: `idx_inft_owner`
- Event log by iNFT and time: `idx_event_log_inft_time`
- Session chains: `idx_memory_continuity_chain`
- Oracle performance: `idx_oracle_queries_type`

### Views

Pre-computed views for common analytics:

- `active_inft_sessions` - Active sessions with latest activity
- `consciousness_evolution` - Evolution tracking per iNFT
- `oracle_performance` - Query performance metrics

## Testing

Run tests with pytest:

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run all iNFT tests
pytest tests/test_inft_storage.py -v

# Run specific test
pytest tests/test_inft_storage.py::test_consciousness_calculation -v
```

## Migration Guide

### From Flat Storage to iNFT Schema

```python
async def migrate_legacy_data(legacy_data: dict):
    """Migrate from legacy flat storage to iNFT schema"""
    
    # Create iNFT state
    state = INFTState(
        id=legacy_data["id"],
        owner_address=legacy_data["owner"],
        consciousness_phase="awakening",
        creation_block=legacy_data["created_block"],
        created_at=legacy_data["created_at"],
        updated_at=int(datetime.now().timestamp())
    )
    
    # Migrate events
    for event in legacy_data.get("events", []):
        event_log = EventLog(
            event_id=event["id"],
            inft_id=state.id,
            event_type=event["type"],
            timestamp=event["timestamp"],
            # ... other fields
        )
        # Insert to database
    
    # Sync to 0G Storage
    await sync_to_0g_storage(state.id, state.dict())
```

## Troubleshooting

### Common Issues

**Issue: Checksum mismatch during restore**
```
Solution: Ensure data wasn't modified in transit. Re-download from 0G Storage.
```

**Issue: 0G Storage sync fails**
```
Solution: Check ZERO_G_STORAGE_ENDPOINT and ZERO_G_STORAGE_API_KEY are set correctly.
```

**Issue: Phase transition not triggering**
```
Solution: Check consciousness score and all transition criteria using the /consciousness endpoint.
```

## Future Enhancements

- [ ] Multi-chain support (L2 scaling)
- [ ] IPFS fallback for 0G Storage
- [ ] Advanced sentiment analysis with ML models
- [ ] GraphQL API for complex queries
- [ ] Real-time WebSocket notifications
- [ ] iNFT marketplace integration
- [ ] Social graph for iNFT interactions

## References

- [ERC-7857 - Intelligent NFT Standard](https://eips.ethereum.org/EIPS/eip-7857) (Proposed)
- [0G Aristotle Mainnet Documentation](https://0g.ai)
- [Pi Forge Quantum Genesis](../../README.md)

## License

MIT License - See [LICENSE](../../LICENSE) for details

## Support

For issues and questions:
- Create an issue in the [GitHub repository](https://github.com/onenoly1010/pi-forge-quantum-genesis/issues)
- Join our community Discord
- Check the [documentation](../../docs/)

---

**Built with ❤️ for the Quantum Pi Forge Ecosystem**
