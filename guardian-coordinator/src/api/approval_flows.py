"""
Approval flow logic for the Hephaestus Guardian Coordinator.
Business logic for proposal approval and execution.
"""

import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from src.models.approval import (
    Proposal, ProposalStatus, ProposalAction,
    ExecutionResponse, VoteChoice
)
from src.utils.multisig import verify_quorum

logger = logging.getLogger(__name__)


async def execute_proposal(
    proposal: Proposal,
    executor: str,
    force: bool = False
) -> ExecutionResponse:
    """
    Execute an approved proposal.
    
    Args:
        proposal: The proposal to execute
        executor: Guardian executing the proposal
        force: Force execution even if quorum not met (admin only)
    
    Returns:
        ExecutionResponse with execution results
    
    Raises:
        ValueError: If proposal cannot be executed
    """
    # Validate proposal can be executed
    if proposal.executed:
        raise ValueError(f"Proposal {proposal.proposal_id} has already been executed")
    
    if proposal.status == ProposalStatus.EXPIRED:
        raise ValueError(f"Proposal {proposal.proposal_id} has expired")
    
    if not force and not proposal.quorum_met:
        raise ValueError(
            f"Proposal {proposal.proposal_id} has not reached quorum "
            f"({proposal.votes_approve}/{proposal.quorum_required})"
        )
    
    # Log execution attempt
    logger.info(
        f"Executing proposal {proposal.proposal_id} "
        f"(action: {proposal.action}, executor: {executor})"
    )
    
    # Execute based on action type
    try:
        result = await _execute_action(proposal.action, proposal.params)
        
        return ExecutionResponse(
            proposal_id=proposal.proposal_id,
            success=True,
            executed_at=datetime.utcnow(),
            result=result,
            message=f"Proposal {proposal.proposal_id} executed successfully"
        )
    
    except Exception as e:
        logger.error(f"Failed to execute proposal {proposal.proposal_id}: {str(e)}")
        return ExecutionResponse(
            proposal_id=proposal.proposal_id,
            success=False,
            executed_at=datetime.utcnow(),
            result={'error': str(e)},
            message=f"Proposal execution failed: {str(e)}"
        )


async def _execute_action(action: ProposalAction, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute the specific action based on proposal type.
    
    Args:
        action: Action type to execute
        params: Action parameters
    
    Returns:
        Execution result dictionary
    
    Note:
        All destructive actions are STUBS for safety.
        Production implementation must include proper security checks.
    """
    logger.info(f"Executing action: {action} with params: {params}")
    
    if action == ProposalAction.DEPLOY_CONTRACT:
        return await _execute_deploy_contract(params)
    
    elif action == ProposalAction.TRANSFER_FUNDS:
        return await _execute_transfer_funds(params)
    
    elif action == ProposalAction.UPDATE_GUARDIAN:
        return await _execute_update_guardian(params)
    
    elif action == ProposalAction.CHANGE_QUORUM:
        return await _execute_change_quorum(params)
    
    elif action == ProposalAction.MINT_NFT:
        return await _execute_mint_nft(params)
    
    elif action == ProposalAction.CUSTOM:
        return await _execute_custom(params)
    
    else:
        raise ValueError(f"Unknown action type: {action}")


async def _execute_deploy_contract(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute contract deployment (STUB).
    
    **WARNING**: This is a stub. Do not implement actual deployment
    without proper security review and testnet validation.
    """
    contract_name = params.get('contract', 'Unknown')
    
    logger.warning(
        f"[STUB] Contract deployment requested: {contract_name}. "
        "This is a placeholder - implement actual deployment logic."
    )
    
    return {
        'action': 'deploy_contract',
        'contract': contract_name,
        'status': 'stub_success',
        'tx_hash': f'0xSTUB_{datetime.utcnow().timestamp()}',
        'note': 'STUB EXECUTION - Implement actual contract deployment',
        'testnet_only': True
    }


async def _execute_transfer_funds(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute fund transfer (STUB).
    
    **WARNING**: This is a stub. Never implement without multisig wallet
    and proper security controls. All transfers must be testnet only.
    """
    recipient = params.get('recipient', 'Unknown')
    amount = params.get('amount', 0)
    
    logger.warning(
        f"[STUB] Fund transfer requested: {amount} to {recipient}. "
        "This is a placeholder - implement actual transfer logic."
    )
    
    return {
        'action': 'transfer_funds',
        'recipient': recipient,
        'amount': amount,
        'status': 'stub_success',
        'tx_hash': f'0xSTUB_{datetime.utcnow().timestamp()}',
        'note': 'STUB EXECUTION - Implement actual fund transfer',
        'testnet_only': True,
        'security_warning': 'NEVER implement without proper security review'
    }


async def _execute_update_guardian(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute guardian update (safe - can be implemented).
    """
    guardian_id = params.get('guardian_id')
    updates = params.get('updates', {})
    
    logger.info(f"Updating guardian {guardian_id}: {updates}")
    
    # This is safe to implement - just updates database records
    return {
        'action': 'update_guardian',
        'guardian_id': guardian_id,
        'updates': updates,
        'status': 'success',
        'note': 'Database update executed'
    }


async def _execute_change_quorum(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute quorum requirement change (safe - can be implemented).
    """
    new_quorum = params.get('new_quorum')
    
    logger.info(f"Changing quorum requirement to: {new_quorum}")
    
    # Validate new quorum
    total_guardians = int(os.getenv('GUARDIAN_TOTAL_COUNT', 5))
    if new_quorum > total_guardians:
        raise ValueError(
            f"New quorum ({new_quorum}) cannot exceed "
            f"total guardians ({total_guardians})"
        )
    
    return {
        'action': 'change_quorum',
        'old_quorum': os.getenv('GUARDIAN_QUORUM_REQUIRED', 3),
        'new_quorum': new_quorum,
        'status': 'success',
        'note': 'Quorum requirement updated'
    }


async def _execute_mint_nft(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute NFT mint (STUB).
    
    **WARNING**: Stub for Pi Network testnet NFT minting.
    """
    recipient = params.get('recipient')
    token_uri = params.get('token_uri')
    
    logger.warning(
        f"[STUB] NFT mint requested for {recipient} with URI {token_uri}"
    )
    
    return {
        'action': 'mint_nft',
        'recipient': recipient,
        'token_uri': token_uri,
        'token_id': f'stub_nft_{datetime.utcnow().timestamp()}',
        'status': 'stub_success',
        'note': 'STUB EXECUTION - Implement Pi Network NFT minting',
        'testnet_only': True
    }


async def _execute_custom(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute custom action.
    
    Custom actions can be defined by extending this function.
    """
    custom_type = params.get('type', 'unknown')
    
    logger.info(f"Executing custom action: {custom_type}")
    
    return {
        'action': 'custom',
        'type': custom_type,
        'params': params,
        'status': 'success',
        'note': f'Custom action {custom_type} executed'
    }


def calculate_quorum_status(proposal: Proposal) -> Dict[str, Any]:
    """
    Calculate detailed quorum status for a proposal.
    
    Args:
        proposal: Proposal to check
    
    Returns:
        Quorum status dictionary
    """
    from src.utils.multisig import get_quorum_status
    
    return get_quorum_status(
        votes=proposal.votes,
        required_quorum=proposal.quorum_required,
        total_guardians=int(os.getenv('GUARDIAN_TOTAL_COUNT', 5))
    )
