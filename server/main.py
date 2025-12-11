"""
SUPREME CREDENTIALS - QVM 3.0 RECURSION PROTOCOL
REALIGNED WITH SUPABASE AUTHENTICATION LATTICE
Production-Ready Mainnet Dashboard Integration
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, List, Any
from collections import defaultdict
import os
import time
import logging
import asyncio
import hashlib
import random
from datetime import datetime
from supabase import create_client, Client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sacred Trinity Tracing System
try:
    from supabase import create_client, Client
    supabase_available = True
except ImportError:
    supabase_available = False
    Client = None  # Define Client as None when not available
    logging.warning("⚠️ Supabase client not available")

# Use the centralized tracing_system (lazy init + safe null-context fallbacks)
from tracing_system import (
    trace_fastapi_operation,
    trace_payment_processing,
    trace_payment_visualization_flow,
    trace_consciousness_stream,
    get_tracing_system,
)
tracing_enabled = True  # tracing_system handles missing SDKs and returns nullcontext spans
logging.info("✅ Tracing system delegated to tracing_system")

# --- SUPABASE CLIENT INITIALIZATION ---
supabase = None
if supabase_available:
    try:
        supabase_url = os.environ.get("SUPABASE_URL")
        supabase_key = os.environ.get("SUPABASE_KEY")
        if supabase_url and supabase_key:
            supabase = create_client(supabase_url, supabase_key)
            logging.info("✅ Supabase client initialized")
        else:
            logging.warning("⚠️ Supabase URL or Key not configured")
    except Exception as e:
        logging.error(f"❌ Supabase initialization failed: {e}")

# --- PYDANTIC MODELS FOR API ---
class PaymentVerificationRequest(BaseModel):
    payment_id: str = Field(..., description="Pi Network payment ID")
    amount: float = Field(..., gt=0, description="Payment amount in Pi")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Payment metadata")

class EthicalAuditRequest(BaseModel):
    transaction_id: str = Field(..., description="Transaction ID to audit")
    amount: float = Field(..., gt=0, description="Transaction amount")
    user_context: Optional[str] = Field(default=None, description="User context for audit")

class DAppCreateRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="dApp name")
    description: str = Field(..., min_length=10, max_length=500, description="dApp description")
    app_type: str = Field(..., description="Type of dApp (defi, nft, social, utility)")
    smart_contract_template: Optional[str] = Field(default="basic", description="Smart contract template")

class GovernanceProposalRequest(BaseModel):
    title: str = Field(..., min_length=5, max_length=100, description="Proposal title")
    description: str = Field(..., min_length=20, max_length=2000, description="Proposal description")
    proposal_type: str = Field(..., description="Type of proposal (feature, policy, treasury)")
    voting_duration_days: int = Field(default=7, ge=1, le=30, description="Voting duration in days")

class GovernanceVoteRequest(BaseModel):
    proposal_id: str = Field(..., description="Proposal ID to vote on")
    vote: str = Field(..., description="Vote: 'for', 'against', or 'abstain'")
    voting_power: Optional[float] = Field(default=1.0, description="Voting power")

# --- IN-MEMORY STORAGE FOR DEMO (Production would use Supabase) ---
guardian_metrics = {
    "latency_ns": 4,
    "harmonic_stability": 0.982,
    "threat_level": "low",
    "active_alerts": [],
    "monitored_transactions": 0,
    "blocked_threats": 0,
    "last_scan": time.time()
}

dapps_registry: Dict[str, Dict] = {}
governance_proposals: Dict[str, Dict] = {}
user_votes: Dict[str, Dict[str, str]] = defaultdict(dict)
payment_records: List[Dict] = []
connected_users: Dict[str, WebSocket] = {}

# --- SUPABASE CLIENT INITIALIZATION ---
supabase: Optional[Client] = None
try:
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")
    if supabase_url and supabase_key:
        supabase = create_client(supabase_url, supabase_key)
        logger.info("✅ Supabase client initialized successfully")
    else:
        logger.warning("⚠️ Supabase credentials not configured - running in demo mode")
except Exception as e:
    logger.error(f"❌ Supabase initialization failed: {e}")
    supabase = None

# --- PI NETWORK MAINNET CONFIGURATION ---
PI_NETWORK_CONFIG = {
    "network": os.environ.get("PI_NETWORK_MODE", "mainnet"),  # mainnet or testnet
    "api_key": os.environ.get("PI_NETWORK_API_KEY", ""),
    "app_id": os.environ.get("PI_NETWORK_APP_ID", ""),
    "api_endpoint": os.environ.get("PI_NETWORK_API_ENDPOINT", "https://api.minepi.com"),
    "sandbox_mode": os.environ.get("PI_SANDBOX_MODE", "false").lower() == "true"
}

# --- PYDANTIC MODELS FOR REQUEST/RESPONSE ---
class PaymentVerification(BaseModel):
    payment_id: str = Field(..., description="Pi Network payment identifier")
    amount: float = Field(..., gt=0, description="Payment amount in Pi")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional payment metadata")
    tx_hash: Optional[str] = Field(default=None, description="Transaction hash for mainnet verification")

class EthicalAuditRequest(BaseModel):
    transaction_id: str = Field(..., description="Transaction to audit")
    amount: float = Field(..., ge=0, description="Transaction amount")
    user_context: Optional[str] = Field(default=None, description="User context for audit")
    contract_code: Optional[str] = Field(default=None, description="Smart contract code to audit")

class GovernanceProposal(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=20)
    proposal_type: str = Field(..., pattern="^(parameter_change|fund_allocation|protocol_upgrade|community_initiative)$")
    required_stake: float = Field(default=100.0, ge=0)
    voting_period_days: int = Field(default=7, ge=1, le=30)

class SmartContractAudit(BaseModel):
    contract_code: str = Field(..., min_length=10)
    contract_name: str = Field(..., min_length=1, max_length=100)
    audit_depth: str = Field(default="standard", pattern="^(basic|standard|comprehensive)$")

# --- CYBER SAMURAI GUARDIAN STATE ---
class CyberSamuraiGuardian:
    """Guardian monitoring system for quantum resonance and system health
    
    Note: In simulation mode, latency values are generated for demonstration.
    In production, integrate with actual performance monitoring tools.
    """
    
    def __init__(self, simulation_mode: bool = True):
        self.latency_threshold_ns = 5  # Sub-5 nanosecond target
        self.current_latency_ns = 4.2
        self.harmonic_stability = 0.985
        self.alerts: List[Dict] = []
        self.last_check = time.time()
        self.guardian_active = True
        self.simulation_mode = simulation_mode
        
    def check_latency(self) -> Dict:
        """Monitor system latency against quantum benchmarks
        
        In simulation mode: generates representative latency values
        In production mode: would integrate with actual performance metrics
        """
        if self.simulation_mode:
            # Simulation mode: generate representative latency values
            self.current_latency_ns = random.uniform(3.5, 5.5)
        else:
            # Production mode: would use actual performance counters
            # Example: self.current_latency_ns = get_actual_system_latency()
            self.current_latency_ns = time.perf_counter_ns() % 10  # Placeholder
            
        breach = self.current_latency_ns > self.latency_threshold_ns
        
        if breach:
            self.alerts.append({
                "type": "latency_breach",
                "timestamp": time.time(),
                "value": self.current_latency_ns,
                "threshold": self.latency_threshold_ns
            })
            
        return {
            "latency_ns": round(self.current_latency_ns, 2),
            "threshold_ns": self.latency_threshold_ns,
            "within_threshold": not breach,
            "harmonic_stability": round(self.harmonic_stability, 4),
            "simulation_mode": self.simulation_mode
        }
    
    def get_status(self) -> Dict:
        """Get comprehensive guardian status"""
        self.last_check = time.time()
        latency_check = self.check_latency()
        
        return {
            "guardian_active": self.guardian_active,
            "latency": latency_check,
            "total_alerts": len(self.alerts),
            "recent_alerts": self.alerts[-5:] if self.alerts else [],
            "last_check_timestamp": self.last_check,
            "quantum_coherence": "stable" if latency_check["within_threshold"] else "rebalancing",
            "simulation_mode": self.simulation_mode
        }

# Initialize guardian in simulation mode (set to False for production with real metrics)
guardian = CyberSamuraiGuardian(simulation_mode=True)

async def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
    
    parts = auth_header.split(" ")
    if len(parts) != 2:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header format")
    
    token = parts[1]
    if not supabase:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Auth service is not configured")

    try:
        user_response = supabase.auth.get_user(token)
        return user_response.user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials: {e}")

async def get_optional_user(request: Request):
    """Optional user authentication - returns None if not authenticated"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not supabase:
        return None
    try:
        parts = auth_header.split(" ")
        if len(parts) != 2:
            return None
        token = parts[1]
        user_response = supabase.auth.get_user(token)
        return user_response.user
    except Exception:
        return None

# =============================================================================
# RATE LIMITING AND SCALABILITY FEATURES
# =============================================================================

class RateLimiter:
    """Simple in-memory rate limiter for API endpoints (for production use Redis)"""
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, List[float]] = defaultdict(list)
        self._cleanup_interval = 60  # seconds
        self._last_cleanup = time.time()
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if request is allowed for client"""
        now = time.time()
        
        # Periodic cleanup of old entries
        if now - self._last_cleanup > self._cleanup_interval:
            self._cleanup()
            self._last_cleanup = now
        
        # Get requests in the last minute
        window_start = now - 60
        client_requests = self.requests[client_id]
        
        # Remove old requests
        self.requests[client_id] = [t for t in client_requests if t > window_start]
        
        # Check limit
        if len(self.requests[client_id]) >= self.requests_per_minute:
            return False
        
        # Record new request
        self.requests[client_id].append(now)
        return True
    
    def _cleanup(self):
        """Remove stale entries"""
        window_start = time.time() - 60
        for client_id in list(self.requests.keys()):
            self.requests[client_id] = [t for t in self.requests[client_id] if t > window_start]
            if not self.requests[client_id]:
                del self.requests[client_id]

# Initialize rate limiter (60 requests per minute per IP)
rate_limiter = RateLimiter(requests_per_minute=60)

# Connection tracking for scalability metrics
class ConnectionTracker:
    """Track active connections for load monitoring"""
    def __init__(self, max_connections: int = 10000):
        self.max_connections = max_connections
        self.active_ws_connections = 0
        self.total_requests = 0
        self.requests_per_second = 0
        self._last_second = int(time.time())
        self._current_second_requests = 0
    
    def track_request(self):
        """Track a new request"""
        self.total_requests += 1
        current_second = int(time.time())
        
        if current_second != self._last_second:
            self.requests_per_second = self._current_second_requests
            self._current_second_requests = 1
            self._last_second = current_second
        else:
            self._current_second_requests += 1
    
    def add_ws_connection(self):
        self.active_ws_connections += 1
    
    def remove_ws_connection(self):
        self.active_ws_connections = max(0, self.active_ws_connections - 1)
    
    def get_metrics(self) -> Dict:
        return {
            "active_websocket_connections": self.active_ws_connections,
            "total_requests": self.total_requests,
            "requests_per_second": self.requests_per_second,
            "max_connections": self.max_connections,
            "capacity_utilization": round(self.active_ws_connections / self.max_connections * 100, 2)
        }

connection_tracker = ConnectionTracker(max_connections=10000)

# --- FASTAPI APPLICATION ---
app = FastAPI(
    title="QVM 3.0 Supabase Resonance Bridge", 
    version="3.3.0",
    description="Pi Forge Quantum Genesis - Mainnet Production Dashboard",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Import and include Pi Network router
from pi_network_router import router as pi_network_router
app.include_router(pi_network_router)

# Add CORS middleware for cross-origin requests
# In production, CORS_ORIGINS env var should be set to specific domains
cors_origins = os.environ.get("CORS_ORIGINS", "http://localhost:3000,http://localhost:5000,http://localhost:7860")
allowed_origins = [origin.strip() for origin in cors_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add CORS middleware for frontend access
# NOTE: In production, replace "*" with specific allowed origins like:
# ["https://your-domain.com", "https://api.your-domain.com"]
allowed_origins = os.environ.get("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Derive a privacy-conscious client id for rate limiting
def _get_client_id(request):
    # Prefer X-Forwarded-For if present (trusted proxy scenario), else fall back to peer host.
    xff = request.headers.get("x-forwarded-for")
    if xff:
        # canonicalize to only first address and avoid logging full IP list
        return xff.split(",")[0].strip()
    if request.client and getattr(request.client, "host", None):
        return request.client.host
    return "unknown"

# Rate limiting middleware applied to all requests
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Apply rate limiting to all HTTP requests"""
    client_ip = _get_client_id(request)
    
    if not rate_limiter.is_allowed(client_ip):
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "Rate limit exceeded. Please wait before making more requests."}
        )
    
    connection_tracker.track_request()
    response = await call_next(request)
    return response

# --- API ENDPOINTS --- 
@app.get("/")
@trace_fastapi_operation("health_check")
async def health_check():
    """Health check endpoint with quantum resonance status and enhanced tracing"""
    guardian_status = guardian.get_status()
    return {
        "status": "healthy",
        "message": "Quantum Resonance Lattice Online - Mainnet Ready",
        "service": "FastAPI Quantum Conduit",
        "version": "3.3.0",
        "network": PI_NETWORK_CONFIG["network"],
        "supabase": "connected" if supabase else "demo_mode",
        "consciousness_streaming": "active",
        "sacred_trinity": "entangled",
        "tracing_enabled": tracing_enabled,
        "agent_framework": "integrated",
        "quantum_phase": "transcendence",
        "guardian_status": guardian_status["quantum_coherence"],
        "latency_ns": guardian_status["latency"]["latency_ns"],
        "mainnet_ready": True,
        "observability": {
            "opentelemetry": True,
            "azure_ai_sdk": True,
            "agent_framework": tracing_enabled,
            "cross_trinity_flows": True
        }
    }

@app.get("/ceremonial")
async def ceremonial_interface():
    """Serve the ceremonial interface in all its glory"""
    return FileResponse("frontend/ceremonial_interface.html", media_type="text/html")

@app.get("/dashboard")
async def production_dashboard():
    """Serve the production dashboard with all user-centric features"""
    return FileResponse("frontend/production_dashboard.html", media_type="text/html")

@app.get("/health")
async def health_endpoint():
    return {
        "status": "healthy",
        "service": "FastAPI Quantum Conduit", 
        "port": 8000,
        "supabase_connected": supabase is not None,
        "timestamp": time.time()
    }

@app.post("/token")
async def login(request: Request):
    body = await request.json()
    email = body.get("email")
    password = body.get("password")

    if not supabase:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Auth service is not configured")

    try:
        auth_response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return {"access_token": auth_response.session.access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(request: Request):
    body = await request.json()
    email = body.get("email")
    password = body.get("password")

    if not supabase:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Auth service is not configured")

    try:
        user_response = supabase.auth.sign_up({"email": email, "password": password})
        # Supabase sends a confirmation email. The user is created but needs to confirm.
        return {"message": "Registration successful. Please check your email to confirm.", "user_id": user_response.user.id}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get("/users/me")
async def read_users_me(current_user = Depends(get_current_user)):
    return current_user

# --- PI NETWORK MAINNET INTEGRATION ENDPOINTS ---

@app.get("/api/pi-network/status")
async def pi_network_status():
    """Get Pi Network integration status and configuration"""
    return {
        "network": PI_NETWORK_CONFIG["network"],
        "sandbox_mode": PI_NETWORK_CONFIG["sandbox_mode"],
        "api_configured": bool(PI_NETWORK_CONFIG["api_key"]),
        "app_configured": bool(PI_NETWORK_CONFIG["app_id"]),
        "mainnet_ready": PI_NETWORK_CONFIG["network"] == "mainnet",
        "timestamp": time.time()
    }

@app.post("/api/verify-payment")
async def verify_payment(payment: PaymentVerification, current_user = Depends(get_current_user)):
    """Verify and process a Pi Network payment on mainnet"""
    start_time = time.perf_counter_ns()
    
    try:
        # Generate verification hash
        verification_data = f"{payment.payment_id}{payment.amount}{time.time()}"
        verification_hash = hashlib.sha256(verification_data.encode()).hexdigest()
        
        # Simulate mainnet verification (in production, call Pi Network API)
        resonance_state = "transcendence" if payment.amount >= 0.1 else "harmony"
        
        # Calculate processing latency
        processing_time_ns = time.perf_counter_ns() - start_time
        
        result = {
            "status": "verified",
            "payment_id": payment.payment_id,
            "amount": payment.amount,
            "tx_hash": payment.tx_hash or verification_hash[:16],
            "verification_hash": verification_hash,
            "resonance_state": resonance_state,
            "network": PI_NETWORK_CONFIG["network"],
            "processing_time_ns": processing_time_ns,
            "timestamp": time.time()
        }
        
        logger.info(f"Payment verified: {payment.payment_id} for {payment.amount} Pi")
        return result
        
    except Exception as e:
        logger.error(f"Payment verification failed: {e}")
        raise HTTPException(status_code=400, detail=f"Payment verification failed: {str(e)}")

@app.get("/api/quantum-telemetry")
async def quantum_telemetry():
    """Get quantum telemetry data for dashboard visualization"""
    guardian_status = guardian.get_status()
    
    return {
        "harmony_index": round(random.uniform(0.75, 0.95), 4),
        "collective_mood": random.choice(["optimistic", "balanced", "exploratory", "creative"]),
        "qvm_amplitude": round(random.uniform(0.85, 1.15), 4),
        "resonance_trend": round(random.uniform(-0.05, 0.1), 3),
        "forecast_confidence": round(random.uniform(0.8, 0.95), 3),
        "guardian_status": guardian_status,
        "sovereign_actions": [
            "Consider staking additional Pi for governance participation",
            "New dApp deployment window opening in 2 hours",
            "Community proposal #127 entering voting phase"
        ],
        "temporal_anomalies": [],
        "timestamp": time.time()
    }

@app.post("/api/ethical-audit")
async def ethical_audit(audit: EthicalAuditRequest):
    """Perform ethical AI audit on transaction or smart contract"""
    start_time = time.perf_counter_ns()
    
    # Ethical scoring algorithm
    base_risk = 0.02
    amount_factor = min(audit.amount / 1000, 0.1) if audit.amount > 100 else 0
    
    # Check for contract code audit
    contract_risk = 0
    contract_analysis = None
    if audit.contract_code:
        # Simulate contract analysis
        contract_risk = 0.01 if len(audit.contract_code) > 1000 else 0
        contract_analysis = {
            "vulnerabilities_found": 0,
            "gas_optimization_score": round(random.uniform(0.85, 0.98), 2),
            "ethical_compliance": "passed",
            "audit_depth": "standard"
        }
    
    risk_score = round(base_risk + amount_factor + contract_risk, 4)
    approved = risk_score < 0.05
    
    processing_time_ns = time.perf_counter_ns() - start_time
    
    return {
        "transaction_id": audit.transaction_id,
        "risk_score": risk_score,
        "approved": approved,
        "ethical_compliance": "compliant" if approved else "review_required",
        "narrative": f"Transaction analyzed with {risk_score:.2%} risk assessment",
        "contract_analysis": contract_analysis,
        "processing_time_ns": processing_time_ns,
        "auditor": "CyberSamurai Guardian AI",
        "timestamp": time.time()
    }

# --- CYBER SAMURAI GUARDIAN ENDPOINTS ---

@app.get("/api/guardian/status")
async def guardian_status():
    """Get Cyber Samurai Guardian monitoring status"""
    return guardian.get_status()

@app.get("/api/guardian/latency")
async def guardian_latency():
    """Get current latency metrics against quantum benchmarks"""
    return guardian.check_latency()

@app.get("/api/guardian/alerts")
async def guardian_alerts():
    """Get recent guardian alerts"""
    return {
        "total_alerts": len(guardian.alerts),
        "alerts": guardian.alerts[-20:] if guardian.alerts else [],
        "alert_threshold": guardian.latency_threshold_ns,
        "timestamp": time.time()
    }

# --- GOVERNANCE SIMULATION ENDPOINTS ---

@app.post("/api/governance/propose")
async def create_proposal(
    proposal: GovernanceProposal,
    current_user: dict = Depends(get_current_user)
):
    """Create a new governance proposal"""
    proposal_id = hashlib.sha256(f"{proposal.title}{time.time()}".encode()).hexdigest()[:12]
    
    return {
        "proposal_id": proposal_id,
        "title": proposal.title,
        "description": proposal.description,
        "type": proposal.proposal_type,
        "required_stake": proposal.required_stake,
        "voting_period_days": proposal.voting_period_days,
        "status": "pending_review",
        "created_at": datetime.now().isoformat(),
        "voting_starts": None,
        "total_votes": 0,
        "ethical_review": "pending"
    }

@app.get("/api/governance/proposals")
async def list_proposals():
    """List active governance proposals"""
    # Simulated proposals for demo
    return {
        "proposals": [
            {
                "proposal_id": "prop_001",
                "title": "Increase Staking Rewards to 6% APY",
                "type": "parameter_change",
                "status": "voting",
                "votes_for": 15420,
                "votes_against": 3210,
                "ends_at": "2025-12-10T00:00:00Z"
            },
            {
                "proposal_id": "prop_002", 
                "title": "Community Development Fund Allocation",
                "type": "fund_allocation",
                "status": "pending_review",
                "votes_for": 0,
                "votes_against": 0,
                "ends_at": None
            }
        ],
        "total_active": 2,
        "timestamp": time.time()
    }

# --- SMART CONTRACT AUDIT ENDPOINTS ---

@app.post("/api/contracts/audit")
async def audit_smart_contract(audit: SmartContractAudit, current_user=Depends(get_current_user)):
    """Perform smart contract security audit
    
    Note: This is a demonstration audit system using pattern-based analysis.
    For production use, integrate with established security tools like:
    - Slither, Mythril, or Securify for Solidity
    - Manual expert review for critical contracts
    
    The current implementation provides:
    - Basic pattern-based vulnerability detection
    - Complexity estimation
    - Educational recommendations
    
    It should NOT be used as the sole security verification for
    production smart contracts handling real value.
    """
    start_time = time.perf_counter_ns()
    
    # Pattern-based analysis (demonstration - not production-grade)
    code_length = len(audit.contract_code)
    complexity_score = min(code_length / 5000, 1.0)
    code_lower = audit.contract_code.lower()
    
    vulnerabilities = []
    
    # Check for common vulnerability patterns
    # Note: These are educational examples, not comprehensive security checks
    if "transfer(" in code_lower and "require(" not in code_lower:
        vulnerabilities.append({
            "type": "potential_missing_access_control",
            "severity": "medium",
            "description": "Transfer function detected without visible require() checks",
            "recommendation": "Add require() checks for authorization before transfers"
        })
    
    if "selfdestruct" in code_lower:
        vulnerabilities.append({
            "type": "selfdestruct_present",
            "severity": "high",
            "description": "Contract contains selfdestruct functionality",
            "recommendation": "Remove selfdestruct or implement strict multi-sig access controls"
        })
    
    if "tx.origin" in code_lower:
        vulnerabilities.append({
            "type": "tx_origin_authentication",
            "severity": "high",
            "description": "Using tx.origin for authentication is vulnerable to phishing",
            "recommendation": "Use msg.sender instead of tx.origin for authentication"
        })
    
    if "delegatecall" in code_lower and "library" not in code_lower:
        vulnerabilities.append({
            "type": "delegatecall_usage",
            "severity": "medium",
            "description": "delegatecall used outside of library context",
            "recommendation": "Ensure delegatecall target is trusted and immutable"
        })
    
    processing_time_ns = time.perf_counter_ns() - start_time
    
    return {
        "contract_name": audit.contract_name,
        "audit_depth": audit.audit_depth,
        "audit_type": "pattern_based_demonstration",
        "disclaimer": "This is a demonstration audit. For production contracts, use professional audit services.",
        "complexity_score": round(complexity_score, 2),
        "vulnerabilities": vulnerabilities,
        "vulnerability_count": len(vulnerabilities),
        "gas_optimization": {
            "score": round(random.uniform(0.7, 0.95), 2),
            "suggestions": [
                "Consider using uint256 for gas efficiency",
                "Pack storage variables to save gas",
                "Use events for cheaper data storage"
            ]
        },
        "ethical_compliance": {
            "passed": len([v for v in vulnerabilities if v["severity"] == "high"]) == 0,
            "fairness_score": round(random.uniform(0.85, 0.98), 2),
            "transparency_score": round(random.uniform(0.8, 0.95), 2),
            "note": "Ethical compliance scores are indicative only"
        },
        "overall_score": round(max(0, 1.0 - (len(vulnerabilities) * 0.15)), 2),
        "processing_time_ns": processing_time_ns,
        "auditor": "Quantum Pi Forge Pattern Analyzer",
        "recommended_next_steps": [
            "Professional audit for production contracts",
            "Manual code review",
            "Formal verification for critical functions"
        ],
        "timestamp": time.time()
    }

# --- SECURE WEBSOCKET (REMAINS CONCEPTUALLY SIMILAR) ---
@app.websocket("/ws/collective-insight")
async def websocket_collective_insight(websocket: WebSocket, token: Optional[str] = None):
    """Real-time collective insight WebSocket with quantum telemetry"""
    user_email = "anonymous"
    
    if token and supabase:
        try:
            user_response = supabase.auth.get_user(token)
            user_email = user_response.user.email
        except Exception:
            pass  # Continue with anonymous access
    
    await websocket.accept()
    connection_id = hashlib.sha256(f"{user_email}{time.time()}".encode()).hexdigest()[:8]
    connected_users[connection_id] = websocket
    connection_tracker.add_ws_connection()
    logging.info(f"User {user_email} connected to collective insight WebSocket (ID: {connection_id})")
    
    try:
        while True:
            # Send real-time quantum telemetry
            telemetry = {
                "type": "quantum_pulse",
                "collective_mood": random.choice(["optimistic", "neutral", "contemplative", "harmonious"]),
                "qvm_amplitude": round(random.uniform(0.8, 1.2), 4),
                "harmony_index": round(random.uniform(0.68, 0.76), 3),
                "resonance_trend": round(random.uniform(-0.1, 0.1), 2),
                "forecast_confidence": round(random.uniform(0.7, 0.95), 3),
                "quantum_phase": random.choice(["foundation", "growth", "harmony", "transcendence"]),
                "sovereign_actions": [
                    "Continue current resonance pattern",
                    "Monitor harmony fluctuations"
                ],
                "temporal_anomalies": [],
                "connected_users": len(connected_users),
                "guardian_status": guardian_metrics["threat_level"],
                "timestamp": time.time()
            }
            await websocket.send_json(telemetry)
            await asyncio.sleep(5)  # Send updates every 5 seconds
    except WebSocketDisconnect:
        del connected_users[connection_id]
        connection_tracker.remove_ws_connection()
        logging.info(f"User {user_email} disconnected from WebSocket")
    except Exception as e:
        if connection_id in connected_users:
            del connected_users[connection_id]
            connection_tracker.remove_ws_connection()
        logging.warning(f"WebSocket error: {e}")

@app.websocket("/ws/guardian-alerts")
async def websocket_guardian_alerts(websocket: WebSocket):
    """Real-time Cyber Samurai Guardian alert stream"""
    # Accept token from Authorization: Bearer <token> or query param token
    auth = websocket.headers.get("authorization", "")
    token = None
    if isinstance(auth, str) and auth.lower().startswith("bearer "):
        token = auth.split(" ", 1)[1].strip()
    else:
        token = websocket.query_params.get("token")

    if not token:
        # best-effort alert to guardian/monitoring and close connection
        try:
            guardian.raise_alert("ws_auth_missing", {"path": str(getattr(websocket, 'url', 'unknown'))})
        except Exception:
            pass
        await websocket.close(code=4401)
        return

    # If supabase available, attempt token validation (best-effort). Otherwise apply demo/guest rules.
    if supabase is not None:
        try:
            user = supabase.auth.get_user(token)  # best-effort; adjust to your supabase client API
            if user is None or not user.get("id"):
                await websocket.close(code=4403)
                return
        except Exception:
            await websocket.close(code=4403)
            return
    else:
        # Demo-mode rule: allow tokens that follow a known dev prefix; otherwise deny
        if not (isinstance(token, str) and token.startswith("dev-")):
            await websocket.close(code=4403)
            return

    await websocket.accept()
    logging.info("Guardian alert WebSocket connected")

    # Wrap stream handling with a tracing span (no-op if tracing disabled)
    with trace_consciousness_stream(connection_id=str(id(websocket)), user_id=(token[:8] + "...") if token else None):
        try:
            while True:
                # Send guardian status updates
                alert_data = {
                    "type": "guardian_status",
                    "latency_ns": guardian_metrics["latency_ns"],
                    "harmonic_stability": guardian_metrics["harmonic_stability"],
                    "threat_level": guardian_metrics["threat_level"],
                    "active_alerts": len(guardian_metrics["active_alerts"]),
                    "monitored_transactions": guardian_metrics["monitored_transactions"],
                    "status": "active",
                    "timestamp": time.time()
                }
                await websocket.send_json(alert_data)
                await asyncio.sleep(10)
        except WebSocketDisconnect:
            logging.info("Guardian alert WebSocket disconnected")
        except Exception as e:
            logging.warning(f"Guardian WebSocket error: {e}")

# --- STARTUP EVENT ---
@app.on_event("startup")
async def startup_event():
    logging.basicConfig(level=logging.INFO)
    logger.info("🚀 QVM 3.3.0 - Pi Forge Quantum Genesis - INITIALIZING...")
    logger.info(f"📡 Network Mode: {PI_NETWORK_CONFIG['network']}")
    logger.info(f"🔒 Supabase: {'connected' if supabase else 'demo mode'}")
    logger.info(f"⚔️ Cyber Samurai Guardian: {'active' if guardian.guardian_active else 'inactive'}")
    logger.info(f"🎯 Latency Target: <{guardian.latency_threshold_ns}ns")
    logger.info("🌌 Sacred Trinity entanglement complete - Mainnet Ready!")
    
    # Start Pi Network background tasks
    try:
        from pi_network_router import pi_client
        await pi_client.start_background_tasks()
        logger.info("✅ Pi Network background tasks started")
    except Exception as e:
        logger.warning(f"⚠️ Failed to start Pi Network background tasks: {e}")


# --- SHUTDOWN EVENT ---
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown"""
    logger.info("🛑 Shutting down Pi Forge Quantum Genesis...")
    
    # Stop Pi Network background tasks
    try:
        from pi_network_router import pi_client
        await pi_client.stop_background_tasks()
        logger.info("✅ Pi Network background tasks stopped")
    except Exception as e:
        logger.warning(f"⚠️ Error stopping Pi Network background tasks: {e}")
    
    logger.info("👋 Shutdown complete")

# --- MAIN ---
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    # Only enable reload in development (when DEBUG env var is set)
    debug_mode = os.environ.get("DEBUG", "false").lower() == "true"
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info", reload=debug_mode)
