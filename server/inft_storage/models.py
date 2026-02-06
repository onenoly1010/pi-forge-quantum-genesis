"""
Pydantic models for iNFT Memory Schema

These models define the data structures for intelligent NFTs with
consciousness tracking, memory continuity, and 0G Storage integration.
"""

from typing import Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime


class INFTState(BaseModel):
    """Core state management for intelligent NFTs"""
    id: str = Field(..., description="Unique iNFT identifier")
    owner_address: str = Field(..., description="Ethereum address of the owner")
    consciousness_phase: Literal['awakening', 'evolving', 'transcendent'] = Field(
        default='awakening',
        description="Current consciousness evolution phase"
    )
    memory_checksum: Optional[str] = Field(None, description="Checksum for memory integrity verification")
    creation_block: int = Field(..., description="Block number at iNFT creation")
    last_sync_block: Optional[int] = Field(None, description="Last block synced to 0G Storage")
    metadata_uri: Optional[str] = Field(None, description="URI to additional metadata")
    created_at: int = Field(..., description="Unix timestamp of creation")
    updated_at: int = Field(..., description="Unix timestamp of last update")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "inft_0x1234567890abcdef",
                "owner_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1",
                "consciousness_phase": "awakening",
                "memory_checksum": "sha256:abc123...",
                "creation_block": 1000000,
                "last_sync_block": 1000100,
                "metadata_uri": "ipfs://QmXyZ...",
                "created_at": 1704067200,
                "updated_at": 1704067200
            }
        }


class EventLog(BaseModel):
    """Event tracking for all iNFT interactions"""
    event_id: str = Field(..., description="Unique event identifier")
    inft_id: str = Field(..., description="Associated iNFT ID")
    event_type: str = Field(..., description="Type of event (e.g., 'interaction', 'state_change')")
    event_subtype: Optional[str] = Field(None, description="Event subtype for categorization")
    actor_address: Optional[str] = Field(None, description="Ethereum address of the actor")
    metadata: Optional[str] = Field(None, description="JSON metadata for the event")
    timestamp: int = Field(..., description="Unix timestamp of the event")
    block_number: Optional[int] = Field(None, description="Block number if on-chain event")

    class Config:
        json_schema_extra = {
            "example": {
                "event_id": "evt_abc123",
                "inft_id": "inft_0x1234567890abcdef",
                "event_type": "interaction",
                "event_subtype": "user_message",
                "actor_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1",
                "metadata": '{"message": "Hello, iNFT!"}',
                "timestamp": 1704067200,
                "block_number": 1000100
            }
        }


class StateTransition(BaseModel):
    """Consciousness phase transitions with conditions"""
    transition_id: str = Field(..., description="Unique transition identifier")
    inft_id: str = Field(..., description="Associated iNFT ID")
    from_state: str = Field(..., description="Previous consciousness phase")
    to_state: str = Field(..., description="New consciousness phase")
    trigger_condition: str = Field(..., description="Condition that triggered the transition")
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score (0-1)")
    auto_approved: bool = Field(False, description="Whether transition was auto-approved")
    executed_at: int = Field(..., description="Unix timestamp of execution")

    class Config:
        json_schema_extra = {
            "example": {
                "transition_id": "trans_xyz789",
                "inft_id": "inft_0x1234567890abcdef",
                "from_state": "awakening",
                "to_state": "evolving",
                "trigger_condition": "interaction_count > 100",
                "confidence_score": 0.95,
                "auto_approved": True,
                "executed_at": 1704067200
            }
        }


class UserContext(BaseModel):
    """Encrypted context storage for personalization"""
    context_id: str = Field(..., description="Unique context identifier")
    inft_id: str = Field(..., description="Associated iNFT ID")
    context_type: str = Field(..., description="Type of context (e.g., 'preferences', 'history')")
    encrypted_data: bytes = Field(..., description="Encrypted context data")
    encryption_version: int = Field(default=1, description="Encryption algorithm version")
    last_accessed: Optional[int] = Field(None, description="Unix timestamp of last access")
    created_at: int = Field(..., description="Unix timestamp of creation")

    class Config:
        json_schema_extra = {
            "example": {
                "context_id": "ctx_def456",
                "inft_id": "inft_0x1234567890abcdef",
                "context_type": "user_preferences",
                "encrypted_data": b"encrypted_binary_data",
                "encryption_version": 1,
                "last_accessed": 1704067200,
                "created_at": 1704067200
            }
        }


class MemoryContinuity(BaseModel):
    """Session management for continuous memory"""
    session_id: str = Field(..., description="Unique session identifier")
    inft_id: str = Field(..., description="Associated iNFT ID")
    prior_session_id: Optional[str] = Field(None, description="Previous session in the chain")
    session_start: int = Field(..., description="Unix timestamp of session start")
    session_end: Optional[int] = Field(None, description="Unix timestamp of session end")
    interaction_count: int = Field(default=0, description="Number of interactions in session")
    avg_response_time_ms: Optional[int] = Field(None, description="Average response time in milliseconds")
    dominant_topic: Optional[str] = Field(None, description="Primary topic of conversation")
    sentiment_score: Optional[float] = Field(None, ge=-1.0, le=1.0, description="Sentiment score (-1 to 1)")

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "sess_ghi789",
                "inft_id": "inft_0x1234567890abcdef",
                "prior_session_id": "sess_abc123",
                "session_start": 1704067200,
                "session_end": 1704070800,
                "interaction_count": 42,
                "avg_response_time_ms": 250,
                "dominant_topic": "quantum_physics",
                "sentiment_score": 0.8
            }
        }


class OracleQuery(BaseModel):
    """External oracle query tracking"""
    query_id: str = Field(..., description="Unique query identifier")
    inft_id: str = Field(..., description="Associated iNFT ID")
    query_type: str = Field(..., description="Type of oracle query")
    query_params: Optional[str] = Field(None, description="JSON query parameters")
    response_data: Optional[str] = Field(None, description="JSON response data")
    response_time_ms: Optional[int] = Field(None, description="Response time in milliseconds")
    success: bool = Field(..., description="Whether query was successful")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    timestamp: int = Field(..., description="Unix timestamp of query")

    class Config:
        json_schema_extra = {
            "example": {
                "query_id": "qry_jkl012",
                "inft_id": "inft_0x1234567890abcdef",
                "query_type": "price_feed",
                "query_params": '{"symbol": "ETH/USD"}',
                "response_data": '{"price": 2500.00}',
                "response_time_ms": 150,
                "success": True,
                "error_message": None,
                "timestamp": 1704067200
            }
        }


class LedgerAllocation(BaseModel):
    """Financial allocations for iNFT operations"""
    allocation_id: str = Field(..., description="Unique allocation identifier")
    inft_id: str = Field(..., description="Associated iNFT ID")
    source_account: str = Field(..., description="Source account address")
    destination_account: str = Field(..., description="Destination account address")
    amount: float = Field(..., gt=0, description="Allocation amount")
    currency: str = Field(default="ETH", description="Currency type")
    allocation_rule: Optional[str] = Field(None, description="Rule that triggered allocation")
    executed_at: int = Field(..., description="Unix timestamp of execution")
    transaction_hash: Optional[str] = Field(None, description="Blockchain transaction hash")

    class Config:
        json_schema_extra = {
            "example": {
                "allocation_id": "alloc_mno345",
                "inft_id": "inft_0x1234567890abcdef",
                "source_account": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1",
                "destination_account": "0x8ba1f109551bD432803012645Ac136ddd64DBA72",
                "amount": 0.5,
                "currency": "ETH",
                "allocation_rule": "creator_royalty_5pct",
                "executed_at": 1704067200,
                "transaction_hash": "0xabc...123"
            }
        }


# Request/Response models for API endpoints

class INFTMemoryExportRequest(BaseModel):
    """Request to export iNFT memory state"""
    inft_id: str
    include_encrypted: bool = False
    

class INFTMemoryExportResponse(BaseModel):
    """Response containing exported memory state"""
    inft_id: str
    state: INFTState
    event_count: int
    session_count: int
    oracle_query_count: int
    allocation_count: int
    export_timestamp: int
    memory_checksum: str


class INFTMemoryRestoreRequest(BaseModel):
    """Request to restore iNFT memory state"""
    inft_id: str
    state_data: dict
    verify_checksum: bool = True


class INFTMemoryRestoreResponse(BaseModel):
    """Response after memory restoration"""
    inft_id: str
    success: bool
    restored_events: int
    restored_sessions: int
    checksum_verified: bool
    message: str


class INFTOwnershipTransferRequest(BaseModel):
    """Request to transfer iNFT ownership"""
    inft_id: str
    current_owner: str
    new_owner: str
    transfer_memory: bool = True
    signature: str


class INFTOwnershipTransferResponse(BaseModel):
    """Response after ownership transfer"""
    inft_id: str
    success: bool
    new_owner: str
    transfer_timestamp: int
    transaction_hash: Optional[str]
    message: str
