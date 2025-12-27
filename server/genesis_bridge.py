"""
Genesis Bridge - Pi Network Genesis Fee Payment Handler
Manages Genesis Pioneer initialization and sacred fee transactions

Sacred Fee Amounts:
- π (Pi): 3.14159 - Mathematical harmony
- φ (Phi): 1.618 - Golden ratio
- e (Euler): 2.718 - Natural growth
"""

import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional
from decimal import Decimal

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel, Field

from pi_network import (
    PiNetworkClient,
    PiNetworkConfig,
    PiNetworkError,
    PiPaymentError
)
from pi_network.payments import PaymentStatus

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/genesis", tags=["Genesis Bridge"])

# Initialize Pi Network client
pi_client = PiNetworkClient(PiNetworkConfig.from_env())

# Sacred fee amounts
SACRED_FEES = {
    "pi": Decimal("3.14159"),      # Mathematical harmony
    "phi": Decimal("1.618"),       # Golden ratio
    "euler": Decimal("2.718")      # Natural growth
}

# Cached Supabase client
_supabase_client = None
_supabase_available = None


def _get_supabase_client():
    """
    Get cached Supabase client instance
    
    Returns:
        Supabase client instance or None if unavailable
    """
    global _supabase_client, _supabase_available
    
    # Return cached result if already checked
    if _supabase_available is False:
        return None
    
    if _supabase_client is not None:
        return _supabase_client
    
    # Try to initialize Supabase client
    try:
        import importlib
        supabase_module = importlib.import_module('supabase')
        supabase_url = os.environ.get("SUPABASE_URL")
        supabase_service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
        
        if not supabase_url or not supabase_service_key:
            logger.debug("Supabase not configured")
            _supabase_available = False
            return None
        
        _supabase_client = supabase_module.create_client(supabase_url, supabase_service_key)
        _supabase_available = True
        logger.info("✅ Supabase client initialized for Genesis Bridge")
        return _supabase_client
        
    except ImportError:
        logger.debug("Supabase module not available")
        _supabase_available = False
        return None
    except Exception as e:
        logger.warning(f"Failed to initialize Supabase client: {e}")
        _supabase_available = False
        return None


# --- REQUEST/RESPONSE MODELS ---

class GenesisFeeRequest(BaseModel):
    """Genesis Fee payment initiation request"""
    user_id: str = Field(..., description="Pi Network user ID")
    fee_type: str = Field(..., description="Sacred fee type: pi, phi, or euler")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


class GenesisFeeResponse(BaseModel):
    """Genesis Fee payment response"""
    payment_id: str
    amount: float
    fee_type: str
    user_id: str
    status: str
    created_at: float
    metadata: Dict[str, Any]


class GenesisWebhookPayload(BaseModel):
    """Genesis Fee webhook payload"""
    payment_id: str = Field(..., description="Payment identifier")
    status: str = Field(..., description="Payment status")
    tx_hash: Optional[str] = Field(default=None, description="Blockchain transaction hash")
    user_id: str = Field(..., description="Pi Network user ID")
    amount: float = Field(..., description="Payment amount")
    timestamp: float = Field(..., description="Event timestamp")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Payment metadata")


class GenesisPioneerResponse(BaseModel):
    """Genesis Pioneer status response"""
    user_id: str
    is_genesis_pioneer: bool
    genesis_fee_paid: bool
    fee_type: Optional[str]
    payment_timestamp: Optional[float]
    resonance_initialized: bool


# --- ENDPOINTS ---

@router.post("/initiate-fee", response_model=GenesisFeeResponse, status_code=status.HTTP_201_CREATED)
async def initiate_genesis_fee(request: GenesisFeeRequest):
    """
    Initiate Genesis Fee payment
    
    This endpoint creates a payment request for the Genesis Fee, which must be
    paid to become a Genesis Pioneer in the Quantum Pi Forge ecosystem.
    
    Args:
        request: Genesis Fee payment request with user ID and fee type
        
    Returns:
        Genesis Fee payment details including payment ID
        
    Raises:
        HTTPException: If fee type is invalid or payment creation fails
    """
    try:
        # Validate fee type
        if request.fee_type.lower() not in SACRED_FEES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid fee type. Must be one of: {', '.join(SACRED_FEES.keys())}"
            )
        
        # Get sacred fee amount
        fee_amount = float(SACRED_FEES[request.fee_type.lower()])
        
        # Create payment metadata
        payment_metadata = {
            "type": "genesis_fee",
            "fee_type": request.fee_type.lower(),
            "sacred_amount": str(SACRED_FEES[request.fee_type.lower()]),
            **(request.metadata or {})
        }
        
        # Create payment through Pi Network client
        payment = pi_client.payments.create_payment(
            amount=fee_amount,
            memo=f"Genesis Fee - {request.fee_type.upper()} ({fee_amount} Pi)",
            user_id=request.user_id,
            metadata=payment_metadata
        )
        
        logger.info(
            f"Genesis Fee payment initiated: {payment.payment_id} "
            f"for user {request.user_id} (type: {request.fee_type})"
        )
        
        # Record in genesis fee transactions (if Supabase is available)
        try:
            await _record_genesis_fee_transaction(
                payment_id=payment.payment_id,
                user_id=request.user_id,
                amount=fee_amount,
                fee_type=request.fee_type.lower(),
                status=payment.status.value,
                metadata=payment_metadata
            )
        except Exception as e:
            logger.warning(f"Failed to record genesis fee transaction: {e}")
        
        return GenesisFeeResponse(
            payment_id=payment.payment_id,
            amount=payment.amount,
            fee_type=request.fee_type.lower(),
            user_id=payment.user_id,
            status=payment.status.value,
            created_at=payment.created_at,
            metadata=payment.metadata
        )
        
    except PiPaymentError as e:
        logger.error(f"Pi Payment error during Genesis Fee initiation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Payment creation failed: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error during Genesis Fee initiation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@router.post("/webhook", status_code=status.HTTP_200_OK)
async def genesis_webhook_handler(payload: GenesisWebhookPayload, request: Request):
    """
    Handle Genesis Fee payment lifecycle webhooks
    
    This endpoint processes webhook events from the Pi Network for Genesis Fee
    payments, updating payment status and initializing Genesis Pioneer status
    when payment is completed.
    
    Args:
        payload: Webhook event payload
        request: FastAPI request object for security validation
        
    Returns:
        Success confirmation
        
    Raises:
        HTTPException: If webhook validation fails or processing error occurs
    """
    try:
        # Verify webhook authenticity (if webhook secret is configured)
        # SECURITY NOTE: In production, webhook signature verification MUST be implemented
        # to prevent unauthorized webhook calls. Use HMAC-SHA256 to verify the signature
        # from Pi Network using the webhook secret from the developer portal.
        webhook_secret = os.environ.get("PI_NETWORK_WEBHOOK_SECRET")
        if webhook_secret:
            # TODO: Implement webhook signature verification
            # Example: Verify signature from request headers using HMAC-SHA256
            # signature = request.headers.get("X-Pi-Signature")
            # expected_signature = hmac.new(webhook_secret.encode(), request.body, hashlib.sha256).hexdigest()
            # if not hmac.compare_digest(signature, expected_signature):
            #     raise HTTPException(status_code=401, detail="Invalid webhook signature")
            pass
        
        logger.info(
            f"Genesis Fee webhook received: payment_id={payload.payment_id}, "
            f"status={payload.status}, user_id={payload.user_id}"
        )
        
        # Update genesis fee transaction record
        try:
            await _update_genesis_fee_transaction(
                payment_id=payload.payment_id,
                status=payload.status,
                tx_hash=payload.tx_hash,
                timestamp=payload.timestamp
            )
        except Exception as e:
            logger.warning(f"Failed to update genesis fee transaction: {e}")
        
        # If payment completed, initialize Genesis Pioneer
        if payload.status == PaymentStatus.COMPLETED.value:
            try:
                await _initialize_genesis_pioneer(
                    user_id=payload.user_id,
                    payment_id=payload.payment_id,
                    amount=payload.amount,
                    tx_hash=payload.tx_hash,
                    metadata=payload.metadata or {}
                )
                logger.info(f"Genesis Pioneer initialized for user {payload.user_id}")
            except Exception as e:
                logger.error(f"Failed to initialize Genesis Pioneer: {e}")
                # Don't raise exception - webhook should still succeed
        
        return {"status": "success", "message": "Webhook processed successfully"}
        
    except Exception as e:
        logger.error(f"Error processing Genesis Fee webhook: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Webhook processing failed"
        )


@router.get("/pioneer-status/{user_id}", response_model=GenesisPioneerResponse)
async def get_genesis_pioneer_status(user_id: str):
    """
    Get Genesis Pioneer status for a user
    
    Args:
        user_id: Pi Network user ID
        
    Returns:
        Genesis Pioneer status including fee payment and resonance information
        
    Raises:
        HTTPException: If status check fails
    """
    try:
        # Query genesis fee transactions and user metadata
        pioneer_data = await _get_pioneer_status(user_id)
        
        return GenesisPioneerResponse(
            user_id=user_id,
            is_genesis_pioneer=pioneer_data.get("is_genesis_pioneer", False),
            genesis_fee_paid=pioneer_data.get("genesis_fee_paid", False),
            fee_type=pioneer_data.get("fee_type"),
            payment_timestamp=pioneer_data.get("payment_timestamp"),
            resonance_initialized=pioneer_data.get("resonance_initialized", False)
        )
        
    except Exception as e:
        logger.error(f"Error retrieving Genesis Pioneer status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve pioneer status"
        )


@router.get("/sacred-fees")
async def get_sacred_fees():
    """
    Get available sacred fee amounts
    
    Returns:
        Dictionary of sacred fee types and their amounts
    """
    return {
        "fees": {
            fee_type: {
                "amount": float(amount),
                "description": _get_fee_description(fee_type)
            }
            for fee_type, amount in SACRED_FEES.items()
        }
    }


# --- HELPER FUNCTIONS ---

def _get_fee_description(fee_type: str) -> str:
    """Get description for a sacred fee type"""
    descriptions = {
        "pi": "Mathematical harmony - π (3.14159)",
        "phi": "Golden ratio - φ (1.618)",
        "euler": "Natural growth - e (2.718)"
    }
    return descriptions.get(fee_type, "Unknown fee type")


async def _record_genesis_fee_transaction(
    payment_id: str,
    user_id: str,
    amount: float,
    fee_type: str,
    status: str,
    metadata: Dict[str, Any]
) -> None:
    """
    Record Genesis Fee transaction in database
    
    This function attempts to record the Genesis Fee transaction in Supabase.
    If Supabase is not available, it logs a warning and continues.
    """
    try:
        supabase = _get_supabase_client()
        if not supabase:
            logger.debug("Supabase not configured for Genesis Fee recording")
            return
        
        # Insert into genesis_fee_transactions table
        supabase.table("genesis_fee_transactions").insert({
            "payment_id": payment_id,
            "user_id": user_id,
            "amount": amount,
            "fee_type": fee_type,
            "status": status,
            "metadata": metadata,
            "created_at": datetime.utcnow().isoformat()
        }).execute()
        
        logger.debug(f"Genesis Fee transaction recorded: {payment_id}")
        
    except Exception as e:
        logger.debug("Supabase not available for Genesis Fee recording")
    except Exception as e:
        logger.warning(f"Failed to record Genesis Fee transaction: {e}")
        # Don't raise - this is non-critical


async def _update_genesis_fee_transaction(
    payment_id: str,
    status: str,
    tx_hash: Optional[str],
    timestamp: float
) -> None:
    """Update Genesis Fee transaction status"""
    try:
        supabase = _get_supabase_client()
        if not supabase:
            return
        
        update_data = {
            "status": status,
            "updated_at": datetime.utcnow().isoformat()
        }
        
        if tx_hash:
            update_data["tx_hash"] = tx_hash
        
        supabase.table("genesis_fee_transactions").update(update_data).eq(
            "payment_id", payment_id
        ).execute()
        
        logger.debug(f"Genesis Fee transaction updated: {payment_id}")
        
    except Exception as e:
        logger.warning(f"Failed to update Genesis Fee transaction: {e}")


async def _initialize_genesis_pioneer(
    user_id: str,
    payment_id: str,
    amount: float,
    tx_hash: Optional[str],
    metadata: Dict[str, Any]
) -> None:
    """
    Initialize Genesis Pioneer status for user
    
    This function:
    1. Updates user_metadata to mark user as Genesis Pioneer
    2. Initializes resonance_scores for the user
    3. Records NFT mint log entry
    """
    try:
        supabase = _get_supabase_client()
        if not supabase:
            logger.warning("Supabase not configured - cannot initialize Genesis Pioneer")
            return
        
        # Update user metadata
        supabase.table("user_metadata").upsert({
            "user_id": user_id,
            "is_genesis_pioneer": True,
            "genesis_fee_paid": True,
            "genesis_payment_id": payment_id,
            "genesis_tx_hash": tx_hash,
            "genesis_initialized_at": datetime.utcnow().isoformat()
        }).execute()
        
        # Initialize resonance scores
        supabase.table("resonance_scores").upsert({
            "user_id": user_id,
            "harmony_index": 0.5000,
            "ethical_entropy": 0.3000,
            "consciousness_level": 0.2500,
            "resonance_phase": "foundation",
            "total_payments": 1,
            "total_pi_volume": amount
        }).execute()
        
        # Log NFT mint event (if configured)
        nft_collection_id = os.environ.get("NFT_COLLECTION_ID")
        if nft_collection_id:
            # Use payment_id and user_id for unique NFT token ID to prevent collisions
            nft_token_id = f"genesis_{payment_id}_{user_id}"
            
            supabase.table("nft_mint_logs").insert({
                "user_id": user_id,
                "nft_token_id": nft_token_id,
                "nft_collection_id": nft_collection_id,
                "mint_transaction_hash": tx_hash,
                "mint_status": "pending",
                "resonance_snapshot": {
                    "harmony_index": 0.5000,
                    "ethical_entropy": 0.3000,
                    "consciousness_level": 0.2500,
                    "composite_score": 0.4650
                },
                "metadata": {
                    "genesis_fee_type": metadata.get("fee_type", "unknown"),
                    "genesis_payment_id": payment_id,
                    **metadata
                }
            }).execute()
        
        logger.info(f"Genesis Pioneer initialized: {user_id}")
        
    except Exception as e:
        logger.error(f"Failed to initialize Genesis Pioneer: {e}")
        raise


async def _get_pioneer_status(user_id: str) -> Dict[str, Any]:
    """Get Genesis Pioneer status from database"""
    try:
        supabase = _get_supabase_client()
        if not supabase:
            return {
                "is_genesis_pioneer": False,
                "genesis_fee_paid": False,
                "resonance_initialized": False
            }
        
        # Query user metadata
        metadata_result = supabase.table("user_metadata").select("*").eq(
            "user_id", user_id
        ).execute()
        
        # Query resonance scores
        resonance_result = supabase.table("resonance_scores").select("*").eq(
            "user_id", user_id
        ).execute()
        
        # Query genesis fee transactions
        fee_result = supabase.table("genesis_fee_transactions").select("*").eq(
            "user_id", user_id
        ).eq("status", "completed").execute()
        
        user_metadata = metadata_result.data[0] if metadata_result.data else {}
        resonance_data = resonance_result.data[0] if resonance_result.data else {}
        fee_data = fee_result.data[0] if fee_result.data else {}
        
        return {
            "is_genesis_pioneer": user_metadata.get("is_genesis_pioneer", False),
            "genesis_fee_paid": user_metadata.get("genesis_fee_paid", False),
            "fee_type": fee_data.get("fee_type"),
            "payment_timestamp": fee_data.get("created_at"),
            "resonance_initialized": bool(resonance_data)
        }
        
    except Exception as e:
        logger.warning(f"Failed to get pioneer status: {e}")
        return {
            "is_genesis_pioneer": False,
            "genesis_fee_paid": False,
            "resonance_initialized": False
        }
