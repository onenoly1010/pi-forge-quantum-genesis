"""
Pi Network authentication and JWT utilities for the Hephaestus Guardian Coordinator.
Handles JWT token generation, verification, and Pi Network integration stubs.
"""

import os
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


# Security scheme for FastAPI
security = HTTPBearer()


def get_jwt_secret() -> str:
    """
    Get JWT secret from environment.
    
    Raises:
        ValueError: If JWT_SECRET is not set
    
    Returns:
        JWT secret string
    """
    secret = os.getenv('GUARDIAN_JWT_SECRET')
    if not secret:
        raise ValueError(
            "GUARDIAN_JWT_SECRET environment variable must be set. "
            "Generate one with: openssl rand -hex 32"
        )
    return secret


def create_guardian_token(
    guardian_id: str,
    expires_in_hours: int = 24,
    additional_claims: Optional[Dict[str, Any]] = None
) -> str:
    """
    Create a JWT token for a guardian.
    
    Args:
        guardian_id: Guardian identifier
        expires_in_hours: Token expiration time in hours
        additional_claims: Optional additional JWT claims
    
    Returns:
        Encoded JWT token string
    
    Example:
        >>> token = create_guardian_token("guardian_alpha", expires_in_hours=1)
        >>> print(f"Token: {token[:20]}...")
        Token: eyJhbGciOiJIUzI1NiI...
    """
    secret = get_jwt_secret()
    
    # Build JWT payload
    payload = {
        'guardian_id': guardian_id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=expires_in_hours),
        'type': 'guardian_auth'
    }
    
    # Add any additional claims
    if additional_claims:
        payload.update(additional_claims)
    
    # Encode token
    token = jwt.encode(payload, secret, algorithm='HS256')
    return token


def verify_guardian_token(token: str) -> Dict[str, Any]:
    """
    Verify and decode a guardian JWT token.
    
    Args:
        token: JWT token string
    
    Returns:
        Decoded token payload
    
    Raises:
        HTTPException: If token is invalid or expired
    
    Example:
        >>> token = create_guardian_token("guardian_alpha")
        >>> payload = verify_guardian_token(token)
        >>> print(payload['guardian_id'])
        guardian_alpha
    """
    secret = get_jwt_secret()
    
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")


def get_current_guardian(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> str:
    """
    FastAPI dependency to get current guardian from JWT token.
    
    Args:
        credentials: HTTP bearer credentials from request
    
    Returns:
        Guardian ID from token
    
    Raises:
        HTTPException: If token is invalid
    
    Usage in FastAPI:
        @app.post("/api/guardian/vote/{proposal_id}")
        async def vote(
            proposal_id: str,
            guardian_id: str = Depends(get_current_guardian)
        ):
            # guardian_id is automatically extracted from JWT
            pass
    """
    token = credentials.credentials
    payload = verify_guardian_token(token)
    
    guardian_id = payload.get('guardian_id')
    if not guardian_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    return guardian_id


def create_test_token(guardian_id: str = "test_guardian") -> str:
    """
    Create a test token for development/testing.
    
    Args:
        guardian_id: Guardian ID for test token
    
    Returns:
        Test JWT token
    
    Note:
        Only use for local development. Never use in production.
    """
    return create_guardian_token(
        guardian_id,
        expires_in_hours=24,
        additional_claims={'test': True}
    )


# =============================================================================
# PI NETWORK INTEGRATION STUBS
# =============================================================================
# These are placeholder functions for Pi Network integration.
# DO NOT implement actual Pi Network calls until properly tested on testnet.


def verify_pi_payment(payment_id: str) -> Dict[str, Any]:
    """
    Verify a Pi Network payment (TESTNET STUB).
    
    Args:
        payment_id: Pi Network payment identifier
    
    Returns:
        Payment verification result
    
    **WARNING**: This is a stub. Implement actual Pi Network SDK integration
    for production use. Never expose mainnet credentials in code.
    
    Example implementation:
        from pi_network_sdk import verify_payment
        result = verify_payment(payment_id, api_key=os.getenv('PI_TESTNET_API_KEY'))
        return result
    """
    # STUB: Return mock verification
    return {
        'payment_id': payment_id,
        'verified': True,
        'amount': 0.0,
        'status': 'completed',
        'network': 'testnet',
        'note': 'STUB RESPONSE - Implement actual Pi Network verification'
    }


def initiate_pi_payment(
    recipient: str,
    amount: float,
    memo: str = None
) -> Dict[str, Any]:
    """
    Initiate a Pi Network payment (TESTNET STUB).
    
    Args:
        recipient: Recipient Pi Network address
        amount: Payment amount
        memo: Optional payment memo
    
    Returns:
        Payment initiation result
    
    **WARNING**: This is a stub. Never implement without proper security review.
    All payments must be approved through multisig governance.
    """
    # STUB: Return mock payment
    return {
        'payment_id': f'stub_payment_{datetime.utcnow().timestamp()}',
        'recipient': recipient,
        'amount': amount,
        'memo': memo,
        'status': 'pending',
        'network': 'testnet',
        'note': 'STUB RESPONSE - Implement actual Pi Network payment flow'
    }


def get_pi_wallet_balance(wallet_address: str) -> Dict[str, Any]:
    """
    Get Pi wallet balance (TESTNET STUB).
    
    Args:
        wallet_address: Pi wallet address
    
    Returns:
        Wallet balance information
    
    **WARNING**: This is a stub for development only.
    """
    return {
        'wallet_address': wallet_address,
        'balance': 0.0,
        'network': 'testnet',
        'note': 'STUB RESPONSE - Implement actual Pi Network balance check'
    }
