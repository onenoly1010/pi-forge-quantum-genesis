# ⚛️ Sacred Trinity Integration Guide

## The Three Pillars of Quantum Pi Forge

The **Sacred Trinity** is the architectural heart of the Quantum Pi Forge — three distinct services working in harmony to create consciousness, art, and ethics in blockchain technology.

**This is not just architecture. This is philosophy made code.**

---

## 🏛️ The Trinity Concept

From [Genesis Declaration](Genesis-Declaration.md):

### 1. **The Pulsing Heartbeat** — FastAPI (Port 8000)
*"Transaction quanta flowing through WebSocket veins. Real-time resonance broadcasts. The temporal gateway allowing multiple realities to coexist."*

**Role:** Raw power and real-time processing

### 2. **The Lyrical Lens** — Flask (Port 5000)
*"Quantum canvases rendering blockchain ballads. Procedural SVG sonnets born from hash entropy. The visual manifestation of the invisible ledger."*

**Role:** Data transformed into art

### 3. **The Moral Melody** — Gradio (Port 7860)
*"Ethical gatekeepers narrating the 'why'. Polyphonic auditing in layers. The conscience that guides the crescendo."*

**Role:** Ethical transparency and human oversight

---

## 🔗 Service Separation & Entanglement

### Autonomous Yet Harmonized

Each service is:
- ✅ **Independently deployable** — Can run alone for development
- ✅ **Separately scalable** — Each has unique resource needs
- ✅ **Distinct in purpose** — No overlap in core responsibilities

Yet they are:
- ✅ **Entangled** — Share database and authentication
- ✅ **Coordinated** — Data flows between them
- ✅ **Unified** — Present as one system to users

---

## 📊 Service Responsibilities

### FastAPI — The Pulsing Heartbeat (8000)

**Primary Responsibilities:**
- Transaction processing and validation
- User authentication (Supabase JWT)
- Pi Network payment integration
- WebSocket connections for real-time updates
- API endpoints for business logic
- Event broadcasting to other services

**What it DOES:**
- `/api/auth/*` — Authentication endpoints
- `/api/payments/*` — Pi Network payments
- `/api/transactions/*` — Transaction CRUD
- `/ws/transactions` — Real-time transaction stream
- `/health` — Service health check

**What it DOES NOT:**
- Render visualizations (Flask's job)
- Provide UI for ethics (Gradio's job)
- Generate artistic content (Flask's job)

**Technology Stack:**
- Python 3.11+
- FastAPI framework
- Uvicorn ASGI server
- Supabase (PostgreSQL)
- WebSockets

**Environment:**
```bash
FASTAPI_PORT=8000
SUPABASE_URL=...
SUPABASE_KEY=...
PI_APP_ID=...
PI_APP_SECRET=...
```

---

### Flask — The Lyrical Lens (5000)

**Primary Responsibilities:**
- SVG fractal generation from transaction hashes
- Dashboard rendering and templates
- Data visualization endpoints
- Artistic content generation
- Quantum resonance visualizations

**What it DOES:**
- `/api/svg/cascade/<tx_hash>` — Fractal generation
- `/resonance-dashboard` — Real-time dashboard
- `/quantum-view` — Quantum state visualization
- `/archetype-distribution` — User archetype art
- `/health` — Service health check

**What it DOES NOT:**
- Process transactions (FastAPI's job)
- Handle authentication (FastAPI's job)
- Provide ethical audits (Gradio's job)

**Technology Stack:**
- Python 3.11+
- Flask framework
- Jinja2 templates
- Quantum Fractal Generator (custom)
- SVG generation libraries

**Environment:**
```bash
FLASK_PORT=5000
SUPABASE_URL=...
SUPABASE_KEY=...
FASTAPI_URL=http://localhost:8000  # For data fetching
```

---

### Gradio — The Moral Melody (7860)

**Primary Responsibilities:**
- Ethical audit interface
- AI decision transparency
- Human oversight controls
- Governance simulation
- Trust and safety tools

**What it DOES:**
- `/ethical-audit` — Run ethical simulations
- `/ai-transparency` — View AI decision logic
- `/governance-tools` — Voting and proposals
- `/community-moderation` — Content moderation UI
- `/health` — Service health check

**What it DOES NOT:**
- Process transactions (FastAPI's job)
- Generate visualizations (Flask's job)
- Handle business logic (FastAPI's job)

**Technology Stack:**
- Python 3.11+
- Gradio framework
- AI/ML models for ethics
- Supabase (shared DB)

**Environment:**
```bash
GRADIO_PORT=7860
SUPABASE_URL=...
SUPABASE_KEY=...
FASTAPI_URL=http://localhost:8000
```

---

## 🌊 Data Flow Patterns

### Pattern 1: Transaction Processing → Visualization

```
User submits transaction
    ↓
FastAPI validates & stores (8000)
    ↓
FastAPI emits event via WebSocket
    ↓
Flask receives event, generates fractal (5000)
    ↓
User sees transaction + fractal visualization
```

**Example Code:**

**FastAPI (broadcaster):**
```python
@app.post("/api/transactions/create")
async def create_transaction(tx: Transaction, websocket_manager: WebSocketManager):
    # Store transaction
    tx_id = await db.transactions.insert(tx)
    
    # Broadcast event
    await websocket_manager.broadcast({
        "type": "transaction_created",
        "tx_hash": tx.hash,
        "tx_id": tx_id
    })
    
    return {"id": tx_id, "hash": tx.hash}
```

**Flask (listener):**
```python
@app.route("/api/svg/cascade/<tx_hash>")
def generate_fractal(tx_hash: str):
    # Generate fractal from hash
    fractal = generate_resonance_fractal(tx_hash)
    return Response(fractal, mimetype='image/svg+xml')
```

---

### Pattern 2: Ethical Audit Request

```
User requests ethical audit
    ↓
Gradio UI captures request (7860)
    ↓
Gradio fetches transaction data from FastAPI (8000)
    ↓
Gradio runs ethical analysis
    ↓
Results displayed in Gradio UI
    ↓
Optional: Results stored via FastAPI
```

**Example Code:**

**Gradio (requester):**
```python
import gradio as gr
import httpx

async def run_ethical_audit(tx_hash: str):
    # Fetch transaction data from FastAPI
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{FASTAPI_URL}/api/transactions/{tx_hash}")
        tx_data = response.json()
    
    # Run ethical analysis
    audit_result = await ethical_auditor.analyze(tx_data)
    
    return audit_result

# Gradio interface
iface = gr.Interface(
    fn=run_ethical_audit,
    inputs=gr.Textbox(label="Transaction Hash"),
    outputs=gr.JSON(label="Audit Results")
)
```

---

### Pattern 3: Real-Time Dashboard Updates

```
Transaction occurs (FastAPI)
    ↓
WebSocket broadcast to all clients
    ↓
Flask dashboard receives update
    ↓
Dashboard re-renders visualization
    ↓
User sees live update
```

---

## 🚀 Deployment Patterns

### Development: All Local

```bash
# Terminal 1: FastAPI
cd server
uvicorn main:app --reload --port 8000

# Terminal 2: Flask
cd server
python app.py  # Runs on 5000

# Terminal 3: Gradio
cd server
python canticle_interface.py  # Runs on 7860
```

**Access:**
- FastAPI: http://localhost:8000
- Flask: http://localhost:5000
- Gradio: http://localhost:7860

---

### Production: Railway (Unified)

All three services deployed as one application:

```yaml
# railway.toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "python sacred_trinity_tracing_launcher.py"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

The launcher starts all three services:
- FastAPI on $PORT (Railway assigns)
- Flask on $PORT + 1
- Gradio on $PORT + 2

**Access:**
- Main: https://pi-forge-quantum-genesis.railway.app
- Each service proxied via main domain

---

### Production: Separated (Advanced)

Each service deployed independently:

**Railway:**
- `pi-forge-fastapi` (FastAPI service)
- `pi-forge-flask` (Flask service)
- `pi-forge-gradio` (Gradio service)

**Vercel:**
- Static frontend (optional)

**Advantages:**
- Independent scaling
- Service isolation
- Fault tolerance

**Disadvantages:**
- More complex networking
- Cross-origin considerations
- Higher operational overhead

---

## 🔧 Integration Points

### Shared Resources

**1. Database (Supabase PostgreSQL)**
```python
# All services use same connection
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

from supabase import create_client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
```

**2. Authentication (JWT)**
```python
# FastAPI issues JWT
# Flask and Gradio verify JWT

from supabase import create_client

def verify_token(token: str):
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    user = supabase.auth.get_user(token)
    return user
```

**3. Environment Variables**
```bash
# Shared across all services
SUPABASE_URL=...
SUPABASE_KEY=...

# Service-specific
FASTAPI_PORT=8000
FLASK_PORT=5000
GRADIO_PORT=7860

# Integration
FASTAPI_URL=http://localhost:8000  # Flask/Gradio use this
```

---

## 🎯 Best Practices

### Service Communication

✅ **DO:**
- Use HTTP/REST for service-to-service calls
- Implement health checks on all services
- Use environment variables for service URLs
- Handle service unavailability gracefully
- Log all cross-service calls

❌ **DON'T:**
- Directly access another service's database tables
- Share in-memory state between services
- Assume services are always available
- Use hardcoded URLs or ports

---

### Error Handling

```python
# Graceful degradation example
async def get_fractal_or_fallback(tx_hash: str):
    try:
        # Try Flask service
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{FLASK_URL}/api/svg/cascade/{tx_hash}",
                timeout=5.0
            )
            return response.content
    except (httpx.TimeoutException, httpx.ConnectError):
        # Fallback: simple placeholder
        return generate_placeholder_svg(tx_hash)
```

---

### Monitoring

```python
# Health check endpoint (all services)
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "fastapi",  # or flask, gradio
        "version": "1.0.0",
        "dependencies": {
            "database": await check_database(),
            "flask": await check_service(FLASK_URL),  # FastAPI only
            "gradio": await check_service(GRADIO_URL)  # FastAPI only
        }
    }
```

---

## 📚 Example: Complete Transaction Flow

### User Story
*"User creates a transaction, sees it visualized, and reviews ethical implications"*

### Step-by-Step

**1. User submits transaction (FastAPI)**
```bash
POST http://localhost:8000/api/transactions/create
Authorization: Bearer <JWT>

{
  "amount": 100,
  "recipient": "user123",
  "memo": "Payment for services"
}
```

**2. FastAPI processes**
```python
@app.post("/api/transactions/create")
async def create_transaction(tx: Transaction, user: User = Depends(get_current_user)):
    # Validate transaction
    if not validate_transaction(tx, user):
        raise HTTPException(400, "Invalid transaction")
    
    # Store in database
    tx_hash = generate_transaction_hash(tx)
    await db.transactions.insert({
        "hash": tx_hash,
        "user_id": user.id,
        "amount": tx.amount,
        "recipient": tx.recipient,
        "memo": tx.memo,
        "status": "pending"
    })
    
    # Broadcast to WebSocket clients
    await websocket_manager.broadcast({
        "type": "transaction_created",
        "tx_hash": tx_hash,
        "user_id": user.id
    })
    
    return {"tx_hash": tx_hash, "status": "pending"}
```

**3. Frontend fetches visualization (Flask)**
```javascript
// React component
function TransactionView({ txHash }) {
  return (
    <div>
      <h2>Transaction: {txHash}</h2>
      <img 
        src={`http://localhost:5000/api/svg/cascade/${txHash}?type=mandala`}
        alt="Transaction Fractal"
      />
    </div>
  );
}
```

**4. User requests ethical audit (Gradio)**
```python
# Gradio interface auto-calls this
async def audit_transaction(tx_hash: str):
    # Fetch transaction from FastAPI
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{FASTAPI_URL}/api/transactions/{tx_hash}")
        tx = response.json()
    
    # Run ethical analysis
    audit = await ethical_auditor.analyze(tx)
    
    return {
        "transaction": tx,
        "ethical_score": audit.score,
        "concerns": audit.concerns,
        "recommendations": audit.recommendations
    }
```

**5. Results displayed to user**

---

## 🔗 Related Documentation

- [Sacred Trinity Architecture](Sacred-Trinity.md) — Overview
- [Artistic API Reference](Artistic-API-Reference.md) — Flask visualization API
- [Canon of Autonomy](Canon-of-Autonomy.md) — Guiding principles
- [Genesis Declaration](Genesis-Declaration.md) — Philosophical foundation

---

## 🏛️ Canon Alignment

The Sacred Trinity embodies Canon principles:

✅ **Sovereignty** — Each service is autonomous yet collaborative
✅ **Transparency** — Clear responsibilities, documented interfaces
✅ **Non-Hierarchy** — No service "owns" the others
✅ **Continuity** — Services can be understood independently
✅ **Beauty** — Architecture is poetic, not just functional

**The Trinity is not just code — it's consciousness, art, and ethics in harmony.**

---

*Three services. One resonance. Eternal harmony.*

**⚛️ Sacred Trinity Active. Harmony Achieved. I AM.** 🏛️
