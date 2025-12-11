"""
Pydantic schemas for transaction API
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from decimal import Decimal


class TransactionCreate(BaseModel):
    """Request model for creating a transaction"""
    transaction_type: str = Field(..., description="Type of transaction")
    status: str = Field(default="PENDING", description="Transaction status")
    amount: Decimal = Field(..., gt=0, description="Transaction amount")
    from_account_id: Optional[str] = Field(None, description="Source account ID")
    to_account_id: Optional[str] = Field(None, description="Destination account ID")
    parent_transaction_id: Optional[str] = Field(None, description="Parent transaction ID for allocations")
    external_tx_hash: Optional[str] = Field(None, description="External blockchain transaction hash")
    pi_payment_id: Optional[str] = Field(None, description="Pi Network payment ID")
    description: Optional[str] = Field(None, description="Transaction description")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    performed_by: Optional[str] = Field(None, description="User who performed the transaction")

    @validator('transaction_type')
    def validate_transaction_type(cls, v):
        valid_types = ['EXTERNAL_DEPOSIT', 'EXTERNAL_WITHDRAWAL', 'INTERNAL_ALLOCATION', 
                       'PAYMENT', 'REFUND', 'FEE', 'NFT_MINT', 'REWARD']
        if v not in valid_types:
            raise ValueError(f'transaction_type must be one of {valid_types}')
        return v

    @validator('status')
    def validate_status(cls, v):
        valid_statuses = ['PENDING', 'COMPLETED', 'FAILED', 'CANCELLED', 'REFUNDED']
        if v not in valid_statuses:
            raise ValueError(f'status must be one of {valid_statuses}')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "transaction_type": "EXTERNAL_DEPOSIT",
                "status": "COMPLETED",
                "amount": "100.00000000",
                "to_account_id": "550e8400-e29b-41d4-a716-446655440000",
                "external_tx_hash": "0x1234567890abcdef",
                "description": "External deposit from Pi wallet",
                "performed_by": "user@example.com"
            }
        }


class TransactionResponse(BaseModel):
    """Response model for transaction"""
    id: str
    transaction_type: str
    status: str
    amount: Decimal
    from_account_id: Optional[str]
    to_account_id: Optional[str]
    parent_transaction_id: Optional[str]
    external_tx_hash: Optional[str]
    pi_payment_id: Optional[str]
    description: Optional[str]
    metadata: Optional[Dict[str, Any]]
    performed_by: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True


class TransactionListResponse(BaseModel):
    """Response model for transaction list"""
    transactions: List[TransactionResponse]
    total: int
    page: int
    page_size: int


class AllocationResult(BaseModel):
    """Result of allocation operation"""
    parent_transaction_id: str
    child_transaction_ids: List[str]
    total_allocated: Decimal
    allocation_count: int
