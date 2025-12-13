"""
Guardian data models for the Hephaestus Guardian Coordinator.
Pydantic models for guardian identity and management.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class GuardianStatus(str, Enum):
    """Guardian account status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class GuardianRole(str, Enum):
    """Guardian role levels"""
    ADMIN = "admin"
    GUARDIAN = "guardian"
    OBSERVER = "observer"


class GuardianBase(BaseModel):
    """Base guardian model with common fields"""
    guardian_id: str = Field(..., description="Unique guardian identifier")
    display_name: Optional[str] = Field(None, description="Human-readable display name")
    public_key: Optional[str] = Field(None, description="Guardian public key for verification")
    discord_user_id: Optional[str] = Field(None, description="Discord user ID")
    wallet_address: Optional[str] = Field(None, description="Blockchain wallet address")
    status: GuardianStatus = Field(default=GuardianStatus.ACTIVE, description="Guardian status")
    role: GuardianRole = Field(default=GuardianRole.GUARDIAN, description="Guardian role")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    @validator('guardian_id')
    def validate_guardian_id(cls, v):
        """Validate guardian ID format"""
        if not v or len(v) < 3:
            raise ValueError('Guardian ID must be at least 3 characters')
        return v.lower()


class GuardianCreate(GuardianBase):
    """Model for creating a new guardian"""
    pass


class GuardianUpdate(BaseModel):
    """Model for updating guardian information"""
    display_name: Optional[str] = None
    public_key: Optional[str] = None
    discord_user_id: Optional[str] = None
    wallet_address: Optional[str] = None
    status: Optional[GuardianStatus] = None
    role: Optional[GuardianRole] = None
    metadata: Optional[Dict[str, Any]] = None


class Guardian(GuardianBase):
    """Full guardian model with database fields"""
    id: str = Field(..., description="Database UUID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    last_activity: Optional[datetime] = Field(None, description="Last activity timestamp")

    class Config:
        from_attributes = True


class GuardianListResponse(BaseModel):
    """Response model for listing guardians"""
    total: int = Field(..., description="Total number of guardians")
    guardians: list[Guardian] = Field(..., description="List of guardians")


class GuardianAuthToken(BaseModel):
    """Guardian authentication token"""
    guardian_id: str = Field(..., description="Guardian identifier")
    token: str = Field(..., description="JWT authentication token")
    expires_at: datetime = Field(..., description="Token expiration time")


class GuardianVoteWeight(BaseModel):
    """Guardian voting power and weight"""
    guardian_id: str
    weight: int = Field(default=1, ge=0, description="Vote weight (normally 1)")
    can_vote: bool = Field(default=True, description="Whether guardian can vote")
    reason: Optional[str] = Field(None, description="Reason if cannot vote")
