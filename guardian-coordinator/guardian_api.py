#!/usr/bin/env python3
"""
🛡️ GUARDIAN COORDINATOR - QUANTUM VALIDATION API
Sacred role: Filter ethical entropy and coordinate validation consensus
Testnet-only deployment with zero-value enforcement
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import redis.asyncio as redis

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("guardian_coordinator")

# Safety checks
APP_ENVIRONMENT = os.getenv("APP_ENVIRONMENT", "testnet")
GUARDIAN_KILL_SWITCH = os.getenv("GUARDIAN_KILL_SWITCH", "off")
NFT_MINT_VALUE = os.getenv("NFT_MINT_VALUE", "0")

if APP_ENVIRONMENT != "testnet":
    logger.error(f"FATAL: Guardian coordinator MUST run in testnet mode. Got: {APP_ENVIRONMENT}")
    raise RuntimeError("Guardian coordinator requires APP_ENVIRONMENT=testnet")

if GUARDIAN_KILL_SWITCH == "on":
    logger.error("FATAL: Guardian kill switch is ON. Aborting startup.")
    raise RuntimeError("Guardian kill switch activated")

if NFT_MINT_VALUE != "0":
    logger.error(f"FATAL: NFT_MINT_VALUE must be 0 for testnet. Got: {NFT_MINT_VALUE}")
    raise RuntimeError("Testnet requires NFT_MINT_VALUE=0")

logger.info("✅ Safety checks passed: testnet mode, kill switch off, zero-value enforced")

# FastAPI app
app = FastAPI(
    title="Guardian Coordinator API",
    description="Quantum validation and ethical entropy filtering for testnet",
    version="1.0.0"
)


class PulseValidationRequest(BaseModel):
    """Request model for pulse validation"""
    pulse_id: str = Field(..., description="Unique pulse identifier")
    ethical_score: float = Field(..., ge=0.0, le=1.0, description="Ethical score (0-1)")
    qualia_impact: float = Field(..., ge=0.0, le=1.0, description="Qualia impact (0-1)")
    resonance_value: float = Field(..., ge=0.0, le=1.0, description="Resonance value (0-1)")
    metadata: Optional[Dict] = Field(default_factory=dict, description="Additional metadata")


class ValidationResponse(BaseModel):
    """Response model for validation results"""
    guardian_id: str
    timestamp: str
    pulse_id: str
    ethical_entropy: float
    validation_passed: bool
    resonance_approved: bool
    narrative: str
    environment: str = "testnet"
    nft_value: str = "0"


class GuardianCoordinator:
    """Guardian coordinator for validation consensus"""
    
    def __init__(self):
        self.guardian_id = os.getenv("GUARDIAN_ID", "guardian-primary")
        self.quorum_threshold = float(os.getenv("QUORUM_THRESHOLD", "0.70"))
        self.ethical_entropy_max = float(os.getenv("ETHICAL_ENTROPY_MAX", "0.05"))
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.redis_client: Optional[redis.Redis] = None
        self.validation_count = 0
        self.filtered_count = 0
        
        logger.info(f"Guardian {self.guardian_id} initialized")
        logger.info(f"Quorum threshold: {self.quorum_threshold}")
        logger.info(f"Ethical entropy max: {self.ethical_entropy_max}")
    
    async def connect_redis(self):
        """Connect to Redis for stream processing"""
        try:
            self.redis_client = await redis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True
            )
            await self.redis_client.ping()
            logger.info(f"✅ Connected to Redis at {self.redis_url}")
        except Exception as e:
            logger.warning(f"Redis connection failed (optional): {e}")
            self.redis_client = None
    
    async def disconnect_redis(self):
        """Disconnect from Redis"""
        if self.redis_client:
            await self.redis_client.close()
            logger.info("Redis connection closed")
    
    def compute_ethical_entropy(self, ethical_score: float, qualia_impact: float) -> float:
        """
        Sacred algorithm for ethical entropy measurement
        Higher entropy = more ethical risk
        """
        entropy = (1.0 - ethical_score) * 0.6 + (qualia_impact - 0.5) * 0.4
        return max(0.0, min(1.0, entropy))
    
    def generate_validation_narrative(self, entropy: float, resonance: float) -> str:
        """Generate mystical validation narrative"""
        if entropy < 0.02:
            return "🕊️ Harmony Sustained - Pure Resonance Detected"
        elif entropy < 0.05:
            return "✨ Ethical Clarity - Wisdom Flows Unobstructed"
        elif entropy < 0.10:
            return "⚠️ Gentle Turbulence - Consciousness Seeks Balance"
        else:
            return "🛡️ Guardian Intervention - Entropy Exceeds Sacred Threshold"
    
    async def validate_pulse(self, request: PulseValidationRequest) -> ValidationResponse:
        """Validate quantum pulse against ethical thresholds"""
        try:
            # Compute ethical entropy
            ethical_entropy = self.compute_ethical_entropy(
                request.ethical_score,
                request.qualia_impact
            )
            
            # Determine validation status
            validation_passed = ethical_entropy < self.ethical_entropy_max
            resonance_approved = request.resonance_value >= self.quorum_threshold
            
            # Generate narrative
            narrative = self.generate_validation_narrative(
                ethical_entropy,
                request.resonance_value
            )
            
            # Create response
            response = ValidationResponse(
                guardian_id=self.guardian_id,
                timestamp=datetime.utcnow().isoformat(),
                pulse_id=request.pulse_id,
                ethical_entropy=ethical_entropy,
                validation_passed=validation_passed,
                resonance_approved=resonance_approved,
                narrative=narrative
            )
            
            # Update statistics
            self.validation_count += 1
            if not validation_passed:
                self.filtered_count += 1
                logger.warning(f"Pulse {request.pulse_id} filtered: entropy={ethical_entropy:.4f}")
            else:
                logger.info(f"Pulse {request.pulse_id} validated: entropy={ethical_entropy:.4f}")
            
            # Store in Redis if available
            if self.redis_client:
                try:
                    await self.redis_client.xadd(
                        "validated_pulses",
                        {"data": json.dumps(response.model_dump())}
                    )
                except Exception as e:
                    logger.warning(f"Redis stream write failed: {e}")
            
            return response
            
        except Exception as e:
            logger.error(f"Validation error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Validation failed: {str(e)}"
            )


# Initialize coordinator
coordinator = GuardianCoordinator()


@app.on_event("startup")
async def startup_event():
    """Initialize connections on startup"""
    logger.info("🛡️ Guardian Coordinator starting up...")
    await coordinator.connect_redis()
    logger.info("✅ Guardian Coordinator ready")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up connections on shutdown"""
    logger.info("Guardian Coordinator shutting down...")
    await coordinator.disconnect_redis()


@app.get("/health")
async def health_check():
    """Health check endpoint for Railway/Kubernetes"""
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "healthy",
            "service": "Guardian Coordinator",
            "guardian_id": coordinator.guardian_id,
            "environment": APP_ENVIRONMENT,
            "kill_switch": GUARDIAN_KILL_SWITCH,
            "nft_value": NFT_MINT_VALUE,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Guardian Coordinator API",
        "version": "1.0.0",
        "environment": APP_ENVIRONMENT,
        "status": "active"
    }


@app.get("/sentinel/status")
async def sentinel_status():
    """Get guardian sentinel status and statistics"""
    return {
        "guardian_id": coordinator.guardian_id,
        "validations_processed": coordinator.validation_count,
        "pulses_filtered": coordinator.filtered_count,
        "filter_rate": coordinator.filtered_count / max(1, coordinator.validation_count),
        "quorum_threshold": coordinator.quorum_threshold,
        "ethical_entropy_max": coordinator.ethical_entropy_max,
        "environment": APP_ENVIRONMENT,
        "redis_connected": coordinator.redis_client is not None,
        "status": "active_sentinel",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/validate", response_model=ValidationResponse)
async def validate_pulse(request: PulseValidationRequest):
    """
    Validate a quantum pulse against ethical thresholds
    
    This endpoint applies guardian validation logic to ensure
    ethical clarity and resonance alignment.
    """
    return await coordinator.validate_pulse(request)


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )
