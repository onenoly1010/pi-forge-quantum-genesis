"""
Multisig quorum verification utilities for the Hephaestus Guardian Coordinator.
Core logic for verifying whether proposals have reached required quorum.
"""

from typing import List, Dict, Tuple
from src.models.approval import Vote, VoteChoice


def verify_quorum(
    votes: List[Vote] | List[Dict],
    required_quorum: int,
    total_guardians: int = None
) -> Tuple[int, int, bool]:
    """
    Verify whether a proposal has reached the required quorum.
    
    Args:
        votes: List of Vote objects or dictionaries with vote data
        required_quorum: Number of approve votes needed
        total_guardians: Total number of guardians (optional, for validation)
    
    Returns:
        Tuple of (approve_count, required_quorum, quorum_met)
    
    Example:
        >>> from src.models.approval import Vote, VoteChoice
        >>> votes = [
        ...     Vote(guardian_id="g1", vote=VoteChoice.APPROVE),
        ...     Vote(guardian_id="g2", vote=VoteChoice.APPROVE),
        ...     Vote(guardian_id="g3", vote=VoteChoice.REJECT)
        ... ]
        >>> approve_count, required, met = verify_quorum(votes, 2)
        >>> print(f"Votes: {approve_count}/{required}, Met: {met}")
        Votes: 2/2, Met: True
    """
    # Handle both Vote objects and dictionaries
    approve_count = 0
    reject_count = 0
    
    for vote in votes:
        # Handle Vote objects
        if hasattr(vote, 'vote'):
            vote_choice = vote.vote
        # Handle dictionaries
        elif isinstance(vote, dict):
            vote_choice = vote.get('vote')
        else:
            continue
        
        # Count votes
        if vote_choice == VoteChoice.APPROVE or vote_choice == 'approve':
            approve_count += 1
        elif vote_choice == VoteChoice.REJECT or vote_choice == 'reject':
            reject_count += 1
        # Abstain votes don't count toward either side
    
    # Validate quorum requirement
    if required_quorum < 1:
        raise ValueError(f"Required quorum must be at least 1, got {required_quorum}")
    
    # Optional: Validate against total guardians
    if total_guardians is not None:
        if required_quorum > total_guardians:
            raise ValueError(
                f"Required quorum ({required_quorum}) cannot exceed "
                f"total guardians ({total_guardians})"
            )
    
    # Check if quorum is met
    quorum_met = approve_count >= required_quorum
    
    return approve_count, required_quorum, quorum_met


def calculate_approval_percentage(
    votes: List[Vote] | List[Dict]
) -> float:
    """
    Calculate the approval percentage from votes.
    
    Args:
        votes: List of Vote objects or dictionaries
    
    Returns:
        Approval percentage (0.0 to 100.0)
    
    Example:
        >>> votes = [Vote(guardian_id="g1", vote=VoteChoice.APPROVE),
        ...          Vote(guardian_id="g2", vote=VoteChoice.REJECT)]
        >>> percentage = calculate_approval_percentage(votes)
        >>> print(f"{percentage}%")
        50.0%
    """
    if not votes:
        return 0.0
    
    approve_count = 0
    reject_count = 0
    
    for vote in votes:
        vote_choice = vote.vote if hasattr(vote, 'vote') else vote.get('vote')
        
        if vote_choice == VoteChoice.APPROVE or vote_choice == 'approve':
            approve_count += 1
        elif vote_choice == VoteChoice.REJECT or vote_choice == 'reject':
            reject_count += 1
    
    # Calculate percentage (excluding abstentions)
    total_votes = approve_count + reject_count
    if total_votes == 0:
        return 0.0
    
    return (approve_count / total_votes) * 100.0


def check_duplicate_vote(
    votes: List[Vote] | List[Dict],
    guardian_id: str
) -> bool:
    """
    Check if a guardian has already voted.
    
    Args:
        votes: List of existing votes
        guardian_id: Guardian to check
    
    Returns:
        True if guardian has already voted, False otherwise
    """
    for vote in votes:
        vote_guardian = vote.guardian_id if hasattr(vote, 'guardian_id') else vote.get('guardian_id')
        if vote_guardian == guardian_id:
            return True
    return False


def get_quorum_status(
    votes: List[Vote] | List[Dict],
    required_quorum: int,
    total_guardians: int = None
) -> Dict:
    """
    Get comprehensive quorum status information.
    
    Args:
        votes: List of votes
        required_quorum: Required approval votes
        total_guardians: Total guardians (optional)
    
    Returns:
        Dictionary with detailed quorum information
    """
    approve_count, req_quorum, quorum_met = verify_quorum(
        votes, required_quorum, total_guardians
    )
    
    reject_count = sum(
        1 for v in votes
        if (v.vote if hasattr(v, 'vote') else v.get('vote')) in [VoteChoice.REJECT, 'reject']
    )
    
    abstain_count = sum(
        1 for v in votes
        if (v.vote if hasattr(v, 'vote') else v.get('vote')) in [VoteChoice.ABSTAIN, 'abstain']
    )
    
    approval_percentage = calculate_approval_percentage(votes)
    
    return {
        'votes_approve': approve_count,
        'votes_reject': reject_count,
        'votes_abstain': abstain_count,
        'total_votes': len(votes),
        'quorum_required': req_quorum,
        'quorum_met': quorum_met,
        'approval_percentage': approval_percentage,
        'can_execute': quorum_met,
        'votes_needed': max(0, req_quorum - approve_count)
    }


def validate_vote_eligibility(
    guardian_id: str,
    votes: List[Vote] | List[Dict],
    guardian_status: str = 'active'
) -> Tuple[bool, str]:
    """
    Validate if a guardian is eligible to vote.
    
    Args:
        guardian_id: Guardian attempting to vote
        votes: Existing votes
        guardian_status: Guardian's current status
    
    Returns:
        Tuple of (is_eligible, reason_if_not)
    """
    # Check if guardian is active
    if guardian_status != 'active':
        return False, f"Guardian status is '{guardian_status}', must be 'active' to vote"
    
    # Check for duplicate vote
    if check_duplicate_vote(votes, guardian_id):
        return False, "Guardian has already voted on this proposal"
    
    return True, "Eligible to vote"
