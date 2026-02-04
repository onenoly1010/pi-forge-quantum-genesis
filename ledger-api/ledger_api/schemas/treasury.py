"""
Pydantic schemas for treasury and reconciliation API
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class AccountBalance(BaseModel):
    """Account balance information"""
    account_name: str
    account_type: str
    current_balance: Decimal
    is_active: bool
    updated_at: datetime

    class Config:
        from_attributes = True


class TreasuryStatusResponse(BaseModel):
    """Treasury status response"""
    accounts: List[AccountBalance]
    total_balance: Decimal
    active_account_count: int
    timestamp: datetime


class ReconciliationRequest(BaseModel):
    """Request model for reconciliation"""
    external_wallet_balance: Decimal = Field(..., description="External wallet balance")
    external_source: Optional[str] = Field(None, description="Source of external balance")
    performed_by: str = Field(..., description="User performing reconciliation")

    class Config:
        json_schema_extra = {
            "example": {
                "external_wallet_balance": "1000.50000000",
                "external_source": "Pi Network Wallet",
                "performed_by": "admin@example.com"
            }
        }


class ReconciliationResponse(BaseModel):
    """Response model for reconciliation"""
    id: str
    external_wallet_balance: Decimal
    external_source: Optional[str]
    internal_total_balance: Decimal
    discrepancy: Decimal
    discrepancy_percentage: Optional[Decimal]
    status: str
    performed_by: str
    created_at: datetime

    class Config:
        from_attributes = True
