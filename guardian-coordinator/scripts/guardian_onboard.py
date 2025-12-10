#!/usr/bin/env python3
"""
Guardian onboarding CLI script.
Creates a new guardian proposal via the API.
"""

import os
import sys
import json
import argparse
import requests
from datetime import datetime


def create_guardian_proposal(
    guardian_id: str,
    description: str,
    api_url: str = None,
    action: str = "update_guardian"
):
    """
    Create a guardian onboarding proposal.
    
    Args:
        guardian_id: ID of the guardian to onboard
        description: Proposal description
        api_url: API base URL (defaults to localhost:8001)
        action: Proposal action type
    
    Returns:
        dict: API response
    """
    if not api_url:
        api_url = f"http://{os.getenv('API_HOST', 'localhost')}:{os.getenv('API_PORT', '8001')}"
    
    # Prepare proposal payload
    payload = {
        "action": action,
        "description": description,
        "params": {
            "guardian_id": guardian_id,
            "updates": {
                "status": "active",
                "role": "guardian"
            }
        },
        "proposer": "admin"
    }
    
    # Send request
    endpoint = f"{api_url}/api/guardian/proposal"
    
    try:
        print(f"Creating proposal at {endpoint}...")
        response = requests.post(endpoint, json=payload, timeout=10)
        
        if response.status_code == 201:
            result = response.json()
            print(f"\n✅ Proposal created successfully!")
            print(f"   Proposal ID: {result['proposal_id']}")
            print(f"   Action: {result['action']}")
            print(f"   Description: {result['description']}")
            print(f"   Quorum Required: {result['quorum_required']}")
            print(f"   Status: {result['status']}")
            print(f"\nGuardians can now vote on this proposal.")
            return result
        else:
            print(f"\n❌ Failed to create proposal: {response.status_code}")
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
        description="Guardian Onboarding - Create guardian proposal via API"
    )
    
    parser.add_argument(
        '--guardian-id',
        required=True,
        help="Guardian ID to onboard"
    )
    
    parser.add_argument(
        '--description',
        default=None,
        help="Proposal description (optional)"
    )
    
    parser.add_argument(
        '--api-url',
        default=None,
        help="API base URL (default: http://localhost:8001)"
    )
    
    parser.add_argument(
        '--action',
        default='update_guardian',
        choices=['update_guardian', 'custom'],
        help="Proposal action type"
    )
    
    args = parser.parse_args()
    
    # Generate description if not provided
    description = args.description or f"Onboard guardian: {args.guardian_id}"
    
    # Create proposal
    result = create_guardian_proposal(
        guardian_id=args.guardian_id,
        description=description,
        api_url=args.api_url,
        action=args.action
    )
    
    # Exit with appropriate code
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
