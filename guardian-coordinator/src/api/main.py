"""
Hephaestus Guardian Coordinator - FastAPI Backend
Main API application for guardian governance and multisig coordination.
"""

import os
import logging
from datetime import datetime, timedelta
from typing import List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.models.guardian import Guardian, GuardianCreate, GuardianListResponse
from src.models.approval import (
    Proposal, ProposalCreate, ProposalListResponse, ProposalStatus,
    VoteSubmission, VoteResponse, ExecutionRequest, ExecutionResponse,
    Vote, VoteChoice
)
from src.utils.multisig import verify_quorum, get_quorum_status, validate_vote_eligibility
from src.utils.pi_auth import get_current_guardian, create_test_token
from src.api.approval_flows import execute_proposal, calculate_quorum_status
from src.api.webhook_handler import router as webhook_router

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# In-memory storage (replace with database in production)
guardians_db: dict[str, Guardian] = {}
proposals_db: dict[int, Proposal] = {}
proposal_counter = 0


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info("Starting Hephaestus Guardian Coordinator API...")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    logger.info(f"API Port: {os.getenv('API_PORT', '8001')}")
    
    # Initialize with test data if in development
    if os.getenv('ENVIRONMENT', 'development') == 'development':
        _init_test_data()
    
    yield
    
    logger.info("Shutting down Guardian Coordinator API...")


app = FastAPI(
    title="Hephaestus Guardian Coordinator",
    description="Semi-autonomous guardian coordination system with multisig governance",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv('CORS_ORIGINS', '*').split(','),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include webhook router
app.include_router(webhook_router, prefix="/webhook", tags=["webhooks"])


# =============================================================================
# HEALTH & INFO ENDPOINTS
# =============================================================================

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "Hephaestus Guardian Coordinator",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "guardian-coordinator-api",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": os.getenv('ENVIRONMENT', 'development')
    }


# =============================================================================
# GUARDIAN MANAGEMENT ENDPOINTS
# =============================================================================

@app.post("/api/guardian/register", response_model=Guardian, status_code=status.HTTP_201_CREATED)
async def register_guardian(guardian: GuardianCreate):
    """
    Register a new guardian.
    
    This endpoint creates a new guardian account.
    """
    # Check if guardian already exists
    if guardian.guardian_id in guardians_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Guardian {guardian.guardian_id} already exists"
        )
    
    # Create guardian
    new_guardian = Guardian(
        id=f"uuid_{len(guardians_db) + 1}",
        guardian_id=guardian.guardian_id,
        display_name=guardian.display_name,
        public_key=guardian.public_key,
        discord_user_id=guardian.discord_user_id,
        wallet_address=guardian.wallet_address,
        status=guardian.status,
        role=guardian.role,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        metadata=guardian.metadata
    )
    
    guardians_db[guardian.guardian_id] = new_guardian
    logger.info(f"Registered new guardian: {guardian.guardian_id}")
    
    return new_guardian


@app.get("/api/guardian/list", response_model=GuardianListResponse)
async def list_guardians(
    status_filter: Optional[str] = None,
    limit: int = 100
):
    """List all guardians with optional filtering."""
    guardians_list = list(guardians_db.values())
    
    # Apply status filter
    if status_filter:
        guardians_list = [g for g in guardians_list if g.status == status_filter]
    
    # Apply limit
    guardians_list = guardians_list[:limit]
    
    return GuardianListResponse(
        total=len(guardians_list),
        guardians=guardians_list
    )


# =============================================================================
# PROPOSAL ENDPOINTS
# =============================================================================

@app.post("/api/guardian/proposal", response_model=Proposal, status_code=status.HTTP_201_CREATED)
async def create_proposal(proposal: ProposalCreate):
    """
    Create a new guardian proposal.
    
    Any guardian can create a proposal. The proposal requires quorum votes to execute.
    """
    global proposal_counter
    proposal_counter += 1
    
    # Determine quorum requirement
    quorum_required = proposal.quorum_required or int(os.getenv('GUARDIAN_QUORUM_REQUIRED', 3))
    
    # Create proposal
    new_proposal = Proposal(
        id=proposal_counter,
        proposal_id=f"proposal_{proposal_counter}",
        action=proposal.action,
        description=proposal.description,
        params=proposal.params,
        proposer=proposal.proposer,
        status=ProposalStatus.PENDING,
        votes=[],
        votes_approve=0,
        votes_reject=0,
        quorum_required=quorum_required,
        quorum_met=False,
        executed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(hours=proposal.expires_in_hours or 168),
        metadata={}
    )
    
    proposals_db[proposal_counter] = new_proposal
    logger.info(
        f"Created proposal {new_proposal.proposal_id} "
        f"by {proposal.proposer}: {proposal.action}"
    )
    
    return new_proposal


@app.get("/api/guardian/proposals", response_model=ProposalListResponse)
async def list_proposals(
    status_filter: Optional[ProposalStatus] = None,
    limit: int = 100
):
    """List all proposals with optional filtering."""
    proposals_list = list(proposals_db.values())
    
    # Apply status filter
    if status_filter:
        proposals_list = [p for p in proposals_list if p.status == status_filter]
    
    # Sort by created_at descending
    proposals_list.sort(key=lambda p: p.created_at, reverse=True)
    
    # Apply limit
    proposals_list = proposals_list[:limit]
    
    # Calculate counts
    active_count = len([p for p in proposals_db.values() if p.status == ProposalStatus.PENDING])
    pending_count = active_count
    
    return ProposalListResponse(
        total=len(proposals_list),
        proposals=proposals_list,
        active_count=active_count,
        pending_count=pending_count
    )


@app.get("/api/guardian/proposals/{proposal_id}", response_model=Proposal)
async def get_proposal(proposal_id: str):
    """Get a specific proposal by ID."""
    # Find proposal
    proposal = None
    for p in proposals_db.values():
        if p.proposal_id == proposal_id:
            proposal = p
            break
    
    if not proposal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proposal {proposal_id} not found"
        )
    
    return proposal


# =============================================================================
# VOTING ENDPOINTS
# =============================================================================

@app.post("/api/guardian/vote/{proposal_id}", response_model=VoteResponse)
async def submit_vote(
    proposal_id: str,
    vote_data: VoteSubmission
):
    """
    Submit a vote on a proposal.
    
    Guardians can vote approve, reject, or abstain on any active proposal.
    When quorum is reached, the proposal is automatically executed.
    """
    # Find proposal
    proposal = None
    for p in proposals_db.values():
        if p.proposal_id == proposal_id:
            proposal = p
            break
    
    if not proposal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proposal {proposal_id} not found"
        )
    
    # Check if proposal is still open
    if proposal.status != ProposalStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Proposal is {proposal.status}, cannot vote"
        )
    
    # Check if expired
    if datetime.utcnow() > proposal.expires_at:
        proposal.status = ProposalStatus.EXPIRED
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Proposal has expired"
        )
    
    # Validate vote eligibility
    guardian_status = 'active'  # TODO: Look up actual guardian status
    eligible, reason = validate_vote_eligibility(
        vote_data.guardian_id,
        proposal.votes,
        guardian_status
    )
    
    if not eligible:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=reason
        )
    
    # Add vote
    new_vote = Vote(
        guardian_id=vote_data.guardian_id,
        vote=vote_data.vote,
        comment=vote_data.comment,
        timestamp=datetime.utcnow()
    )
    
    proposal.votes.append(new_vote)
    
    # Update vote counts
    proposal.votes_approve = sum(1 for v in proposal.votes if v.vote == VoteChoice.APPROVE)
    proposal.votes_reject = sum(1 for v in proposal.votes if v.vote == VoteChoice.REJECT)
    
    # Check quorum
    approve_count, required, quorum_met = verify_quorum(
        proposal.votes,
        proposal.quorum_required
    )
    proposal.quorum_met = quorum_met
    
    # Auto-execute if quorum met
    executed = False
    if quorum_met and not proposal.executed:
        try:
            result = await execute_proposal(proposal, vote_data.guardian_id)
            if result.success:
                proposal.status = ProposalStatus.EXECUTED
                proposal.executed = True
                proposal.executed_at = datetime.utcnow()
                proposal.executed_by = vote_data.guardian_id
                proposal.execution_result = result.result
                executed = True
                logger.info(f"Proposal {proposal_id} auto-executed after reaching quorum")
        except Exception as e:
            logger.error(f"Failed to auto-execute proposal {proposal_id}: {str(e)}")
    
    proposal.updated_at = datetime.utcnow()
    
    logger.info(
        f"Vote recorded: {vote_data.guardian_id} voted {vote_data.vote} on {proposal_id} "
        f"({proposal.votes_approve}/{proposal.quorum_required})"
    )
    
    return VoteResponse(
        proposal_id=proposal_id,
        vote_accepted=True,
        votes_approve=proposal.votes_approve,
        votes_reject=proposal.votes_reject,
        quorum_required=proposal.quorum_required,
        quorum_met=proposal.quorum_met,
        proposal_status=proposal.status,
        executed=executed,
        message=f"Vote recorded. Quorum: {proposal.votes_approve}/{proposal.quorum_required}"
    )


# =============================================================================
# EXECUTION ENDPOINT
# =============================================================================

@app.post("/api/guardian/execute", response_model=ExecutionResponse)
async def execute_proposal_endpoint(request: ExecutionRequest):
    """
    Manually execute an approved proposal.
    
    This endpoint allows manual execution of approved proposals.
    Normally proposals auto-execute when quorum is reached.
    """
    # Find proposal
    proposal = None
    for p in proposals_db.values():
        if p.proposal_id == request.proposal_id:
            proposal = p
            break
    
    if not proposal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proposal {request.proposal_id} not found"
        )
    
    # Execute
    try:
        result = await execute_proposal(proposal, request.executor, request.force)
        
        # Update proposal
        if result.success:
            proposal.status = ProposalStatus.EXECUTED
            proposal.executed = True
            proposal.executed_at = result.executed_at
            proposal.executed_by = request.executor
            proposal.execution_result = result.result
            proposal.updated_at = datetime.utcnow()
        
        return result
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# =============================================================================
# UTILITY ENDPOINTS
# =============================================================================

@app.get("/api/guardian/test-token")
async def get_test_token(guardian_id: str = "test_guardian"):
    """
    Generate a test JWT token for local development.
    
    **WARNING**: This endpoint should be disabled in production.
    """
    if os.getenv('ENVIRONMENT') == 'production':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Test tokens not available in production"
        )
    
    token = create_test_token(guardian_id)
    
    return {
        'guardian_id': guardian_id,
        'token': token,
        'expires_in_hours': 24,
        'note': 'This is a test token for development only'
    }


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def _init_test_data():
    """Initialize test data for development."""
    logger.info("Initializing test data...")
    
    # Create test guardians
    test_guardians = [
        GuardianCreate(
            guardian_id=f"guardian_{i}",
            display_name=f"Guardian {i}",
            status="active",
            role="guardian"
        )
        for i in range(1, 6)
    ]
    
    for guardian in test_guardians:
        guardians_db[guardian.guardian_id] = Guardian(
            id=f"uuid_{len(guardians_db) + 1}",
            guardian_id=guardian.guardian_id,
            display_name=guardian.display_name,
            public_key=None,
            discord_user_id=None,
            wallet_address=None,
            status=guardian.status,
            role=guardian.role,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            metadata={}
        )
    
    logger.info(f"Created {len(guardians_db)} test guardians")


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv('API_PORT', 8001))
    host = os.getenv('API_HOST', '0.0.0.0')
    
    uvicorn.run(
        "src.api.main:app",
        host=host,
        port=port,
        reload=os.getenv('ENVIRONMENT') == 'development'
    )
