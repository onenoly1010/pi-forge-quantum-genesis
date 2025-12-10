"""
Approval and proposal models for the Hephaestus Guardian Coordinator.
Pydantic models for governance proposals and voting.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from enum import Enum


class ProposalStatus(str, Enum):
    """Proposal lifecycle status"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTED = "executed"
    EXPIRED = "expired"


class ProposalAction(str, Enum):
    """Available proposal action types"""
    DEPLOY_CONTRACT = "deploy_contract"
    TRANSFER_FUNDS = "transfer_funds"
    UPDATE_GUARDIAN = "update_guardian"
    CHANGE_QUORUM = "change_quorum"
    MINT_NFT = "mint_nft"
    CUSTOM = "custom"


class VoteChoice(str, Enum):
    """Vote options"""
    APPROVE = "approve"
    REJECT = "reject"
    ABSTAIN = "abstain"


class Vote(BaseModel):
    """Individual vote record"""
    guardian_id: str = Field(..., description="Guardian who cast the vote")
    vote: VoteChoice = Field(..., description="Vote choice")
    comment: Optional[str] = Field(None, description="Optional vote comment")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Vote timestamp")

    @validator('comment')
    def validate_comment(cls, v):
        """Limit comment length"""
        if v and len(v) > 500:
            raise ValueError('Comment must be 500 characters or less')
        return v


class ProposalBase(BaseModel):
    """Base proposal model"""
    action: ProposalAction = Field(..., description="Action to execute")
    description: str = Field(..., description="Proposal description", min_length=10, max_length=1000)
    params: Dict[str, Any] = Field(default_factory=dict, description="Action parameters")
    proposer: str = Field(..., description="Guardian who created the proposal")

    @validator('description')
    def validate_description(cls, v):
        """Ensure description is meaningful"""
        if v and v.strip():
            return v.strip()
        raise ValueError('Description must be a non-empty string')


class ProposalCreate(ProposalBase):
    """Model for creating a new proposal"""
    quorum_required: Optional[int] = Field(None, ge=1, description="Required vote count for approval")
    expires_in_hours: Optional[int] = Field(168, ge=1, le=720, description="Hours until expiration (default 7 days)")


class ProposalUpdate(BaseModel):
    """Model for updating proposal metadata"""
    description: Optional[str] = Field(None, min_length=10, max_length=1000)
    status: Optional[ProposalStatus] = None
    discord_thread_id: Optional[str] = None


class Proposal(ProposalBase):
    """Full proposal model with database fields"""
    id: int = Field(..., description="Database ID")
    proposal_id: str = Field(..., description="Unique proposal identifier")
    status: ProposalStatus = Field(default=ProposalStatus.PENDING, description="Current status")
    votes: List[Vote] = Field(default_factory=list, description="Vote records")
    votes_approve: int = Field(default=0, ge=0, description="Approve vote count")
    votes_reject: int = Field(default=0, ge=0, description="Reject vote count")
    quorum_required: int = Field(default=3, ge=1, description="Votes needed for approval")
    quorum_met: bool = Field(default=False, description="Whether quorum is met")
    executed: bool = Field(default=False, description="Whether proposal executed")
    executed_at: Optional[datetime] = Field(None, description="Execution timestamp")
    executed_by: Optional[str] = Field(None, description="Who executed the proposal")
    execution_result: Optional[Dict[str, Any]] = Field(None, description="Execution result data")
    discord_thread_id: Optional[str] = Field(None, description="Discord thread ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    expires_at: datetime = Field(..., description="Expiration timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    class Config:
        from_attributes = True


class ProposalListResponse(BaseModel):
    """Response model for listing proposals"""
    total: int = Field(..., description="Total proposal count")
    proposals: List[Proposal] = Field(..., description="Proposal list")
    active_count: int = Field(default=0, description="Count of active proposals")
    pending_count: int = Field(default=0, description="Count of pending proposals")


class VoteSubmission(BaseModel):
    """Model for submitting a vote"""
    guardian_id: str = Field(..., description="Guardian identifier")
    vote: VoteChoice = Field(..., description="Vote choice")
    comment: Optional[str] = Field(None, max_length=500, description="Optional comment")


class VoteResponse(BaseModel):
    """Response after submitting a vote"""
    proposal_id: str = Field(..., description="Proposal identifier")
    vote_accepted: bool = Field(..., description="Whether vote was accepted")
    votes_approve: int = Field(..., description="Current approve votes")
    votes_reject: int = Field(..., description="Current reject votes")
    quorum_required: int = Field(..., description="Required votes")
    quorum_met: bool = Field(..., description="Whether quorum is met")
    proposal_status: ProposalStatus = Field(..., description="Updated proposal status")
    executed: bool = Field(default=False, description="Whether proposal was auto-executed")
    message: str = Field(..., description="Response message")


class ExecutionRequest(BaseModel):
    """Request to execute an approved proposal"""
    proposal_id: str = Field(..., description="Proposal to execute")
    executor: str = Field(..., description="Guardian executing the proposal")
    force: bool = Field(default=False, description="Force execution (admin only)")


class ExecutionResponse(BaseModel):
    """Response after proposal execution"""
    proposal_id: str = Field(..., description="Proposal identifier")
    success: bool = Field(..., description="Whether execution succeeded")
    executed_at: datetime = Field(..., description="Execution timestamp")
    result: Dict[str, Any] = Field(default_factory=dict, description="Execution result")
    message: str = Field(..., description="Execution message")


class QuorumStatus(BaseModel):
    """Quorum calculation status"""
    proposal_id: str = Field(..., description="Proposal identifier")
    votes_approve: int = Field(..., ge=0, description="Approve votes")
    votes_reject: int = Field(..., ge=0, description="Reject votes")
    quorum_required: int = Field(..., ge=1, description="Required votes")
    quorum_met: bool = Field(..., description="Whether quorum is met")
    approval_percentage: float = Field(..., ge=0.0, le=100.0, description="Approval percentage")
    can_execute: bool = Field(..., description="Whether proposal can execute")
