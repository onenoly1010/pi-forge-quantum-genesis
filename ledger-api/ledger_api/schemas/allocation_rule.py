"""
Pydantic schemas for allocation rules API
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class AllocationItem(BaseModel):
    """Single allocation item in a rule"""
    account_name: str = Field(..., description="Target account name")
    percentage: Decimal = Field(..., gt=0, le=100, description="Allocation percentage")


class AllocationRuleCreate(BaseModel):
    """Request model for creating an allocation rule"""
    rule_name: str = Field(..., min_length=1, max_length=100, description="Unique rule name")
    is_active: bool = Field(default=True, description="Whether the rule is active")
    priority: int = Field(default=100, description="Rule priority (lower = higher priority)")
    allocation_config: List[AllocationItem] = Field(..., min_items=1, description="Allocation configuration")
    min_amount: Optional[Decimal] = Field(None, ge=0, description="Minimum amount for rule to apply")
    max_amount: Optional[Decimal] = Field(None, ge=0, description="Maximum amount for rule to apply")
    description: Optional[str] = Field(None, description="Rule description")

    @validator('allocation_config')
    def validate_percentages_sum_to_100(cls, v):
        total = sum(item.percentage for item in v)
        if abs(total - 100) > 0.01:  # Allow small floating point errors
            raise ValueError(f'Allocation percentages must sum to 100, got {total}')
        return v

    @validator('max_amount')
    def validate_amount_range(cls, v, values):
        if v is not None and 'min_amount' in values and values['min_amount'] is not None:
            if v < values['min_amount']:
                raise ValueError('max_amount must be greater than or equal to min_amount')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "rule_name": "custom_deposit_allocation",
                "is_active": True,
                "priority": 100,
                "allocation_config": [
                    {"account_name": "main_operating", "percentage": 50},
                    {"account_name": "reserve_fund", "percentage": 30},
                    {"account_name": "rewards_pool", "percentage": 20}
                ],
                "description": "Custom allocation rule for large deposits"
            }
        }


class AllocationRuleUpdate(BaseModel):
    """Request model for updating an allocation rule"""
    is_active: Optional[bool] = None
    priority: Optional[int] = None
    allocation_config: Optional[List[AllocationItem]] = None
    min_amount: Optional[Decimal] = None
    max_amount: Optional[Decimal] = None
    description: Optional[str] = None

    @validator('allocation_config')
    def validate_percentages_sum_to_100(cls, v):
        if v is not None:
            total = sum(item.percentage for item in v)
            if abs(total - 100) > 0.01:
                raise ValueError(f'Allocation percentages must sum to 100, got {total}')
        return v


class AllocationRuleResponse(BaseModel):
    """Response model for allocation rule"""
    id: str
    rule_name: str
    is_active: bool
    priority: int
    allocation_config: List[AllocationItem]
    min_amount: Optional[Decimal]
    max_amount: Optional[Decimal]
    description: Optional[str]
    created_by: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AllocationRuleListResponse(BaseModel):
    """Response model for allocation rule list"""
    rules: List[AllocationRuleResponse]
    total: int
