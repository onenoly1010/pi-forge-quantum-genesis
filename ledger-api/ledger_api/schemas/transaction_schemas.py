"""
Pydantic schemas for transaction-related requests and responses.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from decimal import Decimal


class TransactionCreate(BaseModel):
    """Schema for creating a new transaction."""
    transaction_hash: Optional[str] = Field(None, description="Blockchain transaction hash")
    transaction_type: str = Field(..., description="Type of transaction")
    from_account_id: Optional[int] = Field(None, description="Source account ID")
    to_account_id: Optional[int] = Field(None, description="Destination account ID")
    amount: Decimal = Field(..., gt=0, description="Transaction amount")
    status: str = Field("PENDING", description="Transaction status")
    purpose: Optional[str] = Field(None, description="Transaction purpose")
    meta_data: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")
    
    @validator('transaction_type')
    def validate_transaction_type(cls, v):
        valid_types = ['EXTERNAL_DEPOSIT', 'EXTERNAL_WITHDRAWAL', 'INTERNAL_ALLOCATION', 'INTERNAL_TRANSFER']
        if v not in valid_types:
            raise ValueError(f'transaction_type must be one of {valid_types}')
        return v
    
    @validator('status')
    def validate_status(cls, v):
        valid_statuses = ['PENDING', 'COMPLETED', 'FAILED', 'CANCELLED']
        if v not in valid_statuses:
            raise ValueError(f'status must be one of {valid_statuses}')
        return v
    
    @validator('to_account_id', always=True)
    def validate_account_flow(cls, to_account_id, values):
        """Validate that account flow matches transaction type business rules."""
        transaction_type = values.get('transaction_type')
        from_account_id = values.get('from_account_id')
        
        if not transaction_type:
            return to_account_id
        
        # EXTERNAL_DEPOSIT: no from_account, must have to_account
        if transaction_type == 'EXTERNAL_DEPOSIT':
            if from_account_id is not None:
                raise ValueError('EXTERNAL_DEPOSIT must not have from_account_id (funds come from external source)')
            if to_account_id is None:
                raise ValueError('EXTERNAL_DEPOSIT must have to_account_id (destination account)')
        
        # EXTERNAL_WITHDRAWAL: must have from_account, no to_account
        elif transaction_type == 'EXTERNAL_WITHDRAWAL':
            if from_account_id is None:
                raise ValueError('EXTERNAL_WITHDRAWAL must have from_account_id (source account)')
            if to_account_id is not None:
                raise ValueError('EXTERNAL_WITHDRAWAL must not have to_account_id (funds go to external destination)')
        
        # INTERNAL_ALLOCATION: no from_account, must have to_account
        elif transaction_type == 'INTERNAL_ALLOCATION':
            if from_account_id is not None:
                raise ValueError('INTERNAL_ALLOCATION must not have from_account_id (system allocation)')
            if to_account_id is None:
                raise ValueError('INTERNAL_ALLOCATION must have to_account_id (destination account)')
        
        # INTERNAL_TRANSFER: must have both from_account and to_account
        elif transaction_type == 'INTERNAL_TRANSFER':
            if from_account_id is None:
                raise ValueError('INTERNAL_TRANSFER must have from_account_id (source account)')
            if to_account_id is None:
                raise ValueError('INTERNAL_TRANSFER must have to_account_id (destination account)')
        
        return to_account_id
    
    class Config:
        json_schema_extra = {
            "example": {
                "transaction_hash": "0x1234567890abcdef",
                "transaction_type": "EXTERNAL_DEPOSIT",
                "to_account_id": 1,
                "amount": 100.50,
                "status": "COMPLETED",
                "purpose": "Initial deposit from Pi wallet",
                "metadata": {"wallet_address": "GXXX...XXX"}
            }
        }


class TransactionResponse(BaseModel):
    """Schema for transaction response."""
    id: int
    transaction_hash: Optional[str]
    transaction_type: str
    from_account_id: Optional[int]
    to_account_id: Optional[int]
    amount: Decimal
    status: str
    purpose: Optional[str]
    parent_transaction_id: Optional[int]
    meta_data: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class AllocationResult(BaseModel):
    """Schema for allocation engine results."""
    parent_transaction_id: int
    child_transaction_ids: List[int] = Field(default_factory=list)
    total_allocated: Decimal
    allocations: List[Dict[str, Any]] = Field(default_factory=list)
    
    class Config:
        json_schema_extra = {
            "example": {
                "parent_transaction_id": 123,
                "child_transaction_ids": [124, 125, 126, 127],
                "total_allocated": 100.0,
                "allocations": [
                    {"account_id": 1, "account_name": "Reserve Treasury", "amount": 40.0},
                    {"account_id": 2, "account_name": "Development Fund", "amount": 25.0}
                ]
            }
        }


class TransactionFilter(BaseModel):
    """Schema for filtering transactions."""
    transaction_type: Optional[str] = None
    status: Optional[str] = None
    from_account_id: Optional[int] = None
    to_account_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = Field(100, ge=1, le=1000)
    offset: int = Field(0, ge=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "transaction_type": "EXTERNAL_DEPOSIT",
                "status": "COMPLETED",
                "limit": 50,
                "offset": 0
            }
        }
