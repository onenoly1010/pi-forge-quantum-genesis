#!/usr/bin/env python3
"""
Quorum check utility.
Fetches a proposal and verifies quorum status locally.
"""

import os
import sys
import argparse
import requests


def check_quorum(
    proposal_id: str,
    api_url: str = None
):
    """
    Check quorum status for a proposal.
    
    Args:
        proposal_id: Proposal ID to check
        api_url: API base URL (defaults to localhost:8001)
    
    Returns:
        dict: Proposal data with quorum status
    """
    if not api_url:
        api_url = f"http://{os.getenv('API_HOST', 'localhost')}:{os.getenv('API_PORT', '8001')}"
    
    # Fetch proposal
    endpoint = f"{api_url}/api/guardian/proposals/{proposal_id}"
    
    try:
        print(f"Fetching proposal {proposal_id} from {endpoint}...")
        response = requests.get(endpoint, timeout=10)
        
        if response.status_code == 200:
            proposal = response.json()
            
            print(f"\n📋 Proposal: {proposal['proposal_id']}")
            print(f"   Description: {proposal['description']}")
            print(f"   Action: {proposal['action']}")
            print(f"   Proposer: {proposal['proposer']}")
            print(f"   Status: {proposal['status']}")
            print(f"\n📊 Voting Status:")
            print(f"   ✅ Approve: {proposal['votes_approve']}")
            print(f"   ❌ Reject: {proposal['votes_reject']}")
            print(f"   Total Votes: {len(proposal['votes'])}")
            print(f"   Quorum Required: {proposal['quorum_required']}")
            
            # Calculate approval percentage
            total_votes = proposal['votes_approve'] + proposal['votes_reject']
            if total_votes > 0:
                approval_pct = (proposal['votes_approve'] / total_votes) * 100
                print(f"   Approval %: {approval_pct:.1f}%")
            
            # Quorum status
            print(f"\n🎯 Quorum Status:")
            if proposal['quorum_met']:
                print(f"   ✅ QUORUM MET ({proposal['votes_approve']}/{proposal['quorum_required']})")
            else:
                votes_needed = proposal['quorum_required'] - proposal['votes_approve']
                print(f"   ⏳ PENDING - Need {votes_needed} more vote(s)")
            
            # Execution status
            print(f"\n⚡ Execution Status:")
            if proposal['executed']:
                print(f"   ✅ EXECUTED")
                if proposal.get('executed_at'):
                    print(f"   Executed at: {proposal['executed_at']}")
                if proposal.get('executed_by'):
                    print(f"   Executed by: {proposal['executed_by']}")
            else:
                print(f"   ⏳ NOT EXECUTED")
            
            # Vote details
            if proposal['votes']:
                print(f"\n🗳️  Vote Details:")
                for i, vote in enumerate(proposal['votes'], 1):
                    vote_emoji = {"approve": "✅", "reject": "❌", "abstain": "⏸️"}.get(vote['vote'], "❓")
                    print(f"   {i}. {vote_emoji} {vote['guardian_id']}: {vote['vote']}")
                    if vote.get('comment'):
                        print(f"      Comment: {vote['comment']}")
            
            return proposal
        
        elif response.status_code == 404:
            print(f"\n❌ Proposal {proposal_id} not found")
            return None
        
        else:
            print(f"\n❌ Failed to fetch proposal: {response.status_code}")
            print(f"   Error: {response.text}")
            return None
    
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Cannot connect to API at {api_url}")
        print("   Make sure the Guardian API is running.")
        return None
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return None


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Quorum Check - Verify proposal quorum status"
    )
    
    parser.add_argument(
        '--proposal-id',
        required=True,
        help="Proposal ID to check"
    )
    
    parser.add_argument(
        '--api-url',
        default=None,
        help="API base URL (default: http://localhost:8001)"
    )
    
    args = parser.parse_args()
    
    # Check quorum
    result = check_quorum(
        proposal_id=args.proposal_id,
        api_url=args.api_url
    )
    
    # Exit with appropriate code
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
