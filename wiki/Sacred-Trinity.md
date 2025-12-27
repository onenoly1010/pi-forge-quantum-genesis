# 🔥 Sacred Trinity - FastAPI, Flask, Gradio Architecture

**Last Updated**: December 2025

The Sacred Trinity is the three-part technical architecture at the heart of Quantum Pi Forge: FastAPI, Flask, and Gradio working in harmony.

---

## 🌌 Overview

### The Trinity

Three synchronized services form the core of our platform:

1. **FastAPI** (Quantum Conduit) - Port 8000
2. **Flask** (Glyph Weaver) - Port 5000
3. **Gradio** (Truth Mirror) - Port 7860

Each service has a distinct role, yet they work together as one unified system aligned with the [[Genesis Declaration]].

---

## ⚡ FastAPI - Quantum Conduit (Port 8000)

### Role: Pulsing Heartbeat

The primary backend API handling:
- RESTful API endpoints
- WebSocket connections
- Pi Network authentication
- Payment processing
- Database operations
- Real-time data streaming

### Key Features

**Authentication & Authorization**:
```python
# Pi Network JWT authentication
@router.post("/auth/pi")
async def authenticate_pi_user(token: str):
    user = await pi_network.verify_token(token)
    return {"access_token": create_jwt(user)}
```

**Payment Processing**:
```python
# Pi Network payment flow
@router.post("/api/payments/approve")
async def approve_payment(payment_id: str):
    return await pi_network.approve(payment_id)
```

**WebSocket Streaming**:
```python
# Real-time consciousness streaming
@app.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    await websocket.accept()
    # Stream quantum data
```

### Technology Stack

- **Framework**: FastAPI 0.104+
- **Server**: Uvicorn ASGI
- **Database**: Supabase PostgreSQL
- **Authentication**: JWT + Pi Network OAuth
- **Observability**: OpenTelemetry tracing

### Endpoints

**Core**:
- `GET /` - Service info
- `GET /health` - Health check
- `GET /docs` - Swagger documentation
- `GET /api/metrics` - Prometheus metrics

**Authentication**:
- `POST /api/auth/pi` - Pi Network login
- `POST /api/auth/refresh` - Refresh token
- `GET /api/auth/me` - Current user

**Payments**:
- `POST /api/payments/approve` - Approve payment
- `POST /api/payments/complete` - Complete payment
- `POST /api/pi-webhooks/payment` - Pi webhook
- `GET /api/payments/history` - Payment history

**Pi Network**:
- `GET /api/pi-network/status` - Configuration status
- `POST /api/pi-identify` - User identification

**Guardian**:
- `GET /api/guardian/dashboard` - Guardian overview
- `GET /api/autonomous/decision-history` - Decision logs

### Deployment

**Local**:
```bash
uvicorn server.main:app --reload --port 8000
```

**Production**:
- **Platform**: Railway
- **URL**: https://pi-forge-quantum-genesis.railway.app
- **Auto-deploy**: Git push to main

**Details**: [[Deployment Guide]]

---

## 🎨 Flask - Glyph Weaver (Port 5000)

### Role: Lyrical Lens

The visualization and dashboard layer providing:
- Dynamic dashboards
- SVG visualizations
- Template rendering
- Data presentation
- Quantum analytics

### Key Features

**SVG Cascade Generation**:
```python
# 4-phase quantum SVG art
@app.route("/api/svg/cascade")
def generate_svg_cascade():
    phases = ["foundation", "growth", "harmony", "transcendence"]
    return render_svg_with_phases(phases)
```

**Quantum Dashboard**:
```python
# Analytics and metrics dashboard
@app.route("/dashboard")
def quantum_dashboard():
    metrics = collect_quantum_metrics()
    return render_template("dashboard.html", metrics=metrics)
```

**Archetype Processing**:
```python
# Quantum archetype visualization
@app.route("/archetype/<type>")
def render_archetype(type):
    return generate_archetype_svg(type)
```

### Technology Stack

- **Framework**: Flask 3.0+
- **Server**: Flask development server / Gunicorn
- **Templating**: Jinja2
- **Visualization**: SVG generation
- **Styling**: Custom CSS with quantum themes

### Routes

**Dashboard**:
- `GET /` - Main dashboard
- `GET /dashboard` - Quantum analytics
- `GET /metrics` - Visual metrics

**Visualization**:
- `GET /api/svg/cascade` - SVG cascade art
- `GET /archetype/<type>` - Archetype rendering
- `GET /visualize/<data>` - Data visualization

**Templates**:
- `GET /templates/<name>` - Dynamic templates
- `POST /render` - Custom rendering

### Deployment

**Local**:
```bash
python server/app.py
# Or with Flask CLI:
flask run --port 5000
```

**Production**:
- **Platform**: Railway or Vercel
- **URL**: Subdomain or custom domain
- **WSGI**: Gunicorn with workers

---

## ⚖️ Gradio - Truth Mirror (Port 7860)

### Role: Moral Melody

The ethical AI interface providing:
- AI model evaluation
- Ethical audits
- Interactive testing
- Veto Triad synthesis
- Canticle processing

### Key Features

**Ethical Audit Interface**:
```python
# Interactive ethical evaluation
def ethical_audit(input_text):
    fingerprint = generate_ethical_fingerprint(input_text)
    reflection = tender_reflection(input_text)
    synthesis = veto_triad_synthesis(fingerprint, reflection)
    return synthesis
```

**Veto Triad Calculation**:
```python
# Three-part ethical scoring
def veto_triad_synthesis(data):
    reactive_echo = calculate_reactive(data)
    tender_reflection = calculate_reflection(data)
    coherence = calculate_coherence(data)
    return {
        "reactive": reactive_echo,
        "reflection": tender_reflection,
        "coherence": coherence,
        "verdict": determine_verdict([reactive_echo, tender_reflection, coherence])
    }
```

**Model Evaluation**:
```python
# AI model testing interface
def evaluate_model(model_input):
    results = run_model_evaluation(model_input)
    metrics = calculate_performance(results)
    return format_evaluation_report(metrics)
```

### Technology Stack

- **Framework**: Gradio 4.0+
- **Interface**: Web-based GUI
- **AI Tools**: Model evaluation frameworks
- **Ethics**: Custom veto triad logic
- **Styling**: Gradio themes + custom CSS

### Interfaces

**Ethical Audit**:
- Text input for content
- Ethical fingerprint display
- Veto Triad scores
- Synthesis verdict

**Model Evaluation**:
- Model input/output testing
- Performance metrics
- Comparison tools
- Results visualization

**Canticle Processing**:
- Wisdom text input
- Resonance analysis
- Coherence scoring
- Synthesis output

### Deployment

**Local**:
```bash
python server/canticle_interface.py
```

**Production**:
- **Platform**: Railway or Spaces
- **URL**: Public Gradio interface
- **Sharing**: Gradio share links

---

## 🔗 Trinity Integration

### Cross-Service Communication

**FastAPI → Flask**:
```python
# FastAPI requests Flask visualizations
async def get_visualization(data):
    response = await http.get("http://flask:5000/api/svg/cascade")
    return response.json()
```

**FastAPI → Gradio**:
```python
# FastAPI sends data for ethical audit
async def request_ethical_audit(content):
    response = await http.post("http://gradio:7860/audit", json={"text": content})
    return response.json()
```

**Flask → FastAPI**:
```python
# Flask fetches data from FastAPI
def get_quantum_data():
    response = requests.get("http://fastapi:8000/api/metrics")
    return response.json()
```

### Shared Resources

**Database**: All services connect to Supabase  
**Authentication**: JWT tokens issued by FastAPI  
**Metrics**: Collected by FastAPI, visualized by Flask  
**Tracing**: OpenTelemetry across all services

### Synchronized Startup

```bash
# Launch all three services together
docker-compose up -d
# Or use launcher:
python sacred_trinity_tracing_launcher.py
```

---

## 📊 Observability

### OpenTelemetry Tracing

All three services instrumented with distributed tracing:

**FastAPI Traces**:
- Authentication flows
- Database operations
- Payment processing
- WebSocket connections

**Flask Traces**:
- SVG generation
- Dashboard rendering
- Template processing
- Quantum calculations

**Gradio Traces**:
- Ethical audits
- Veto Triad synthesis
- Model evaluation
- Canticle processing

### Monitoring Stack

```bash
# Start observability stack
docker-compose up -d

# Access points:
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000
# - OTLP: http://localhost:4318
```

**Full guide**: [[Monitoring Observability]]

---

## 🚀 Local Development

### Quick Start

```bash
# Terminal 1: FastAPI
uvicorn server.main:app --reload --port 8000

# Terminal 2: Flask
python server/app.py

# Terminal 3: Gradio
python server/canticle_interface.py
```

### Docker Compose

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Testing Trinity

```bash
# Test FastAPI
curl http://localhost:8000/health

# Test Flask
curl http://localhost:5000/

# Test Gradio
curl http://localhost:7860/
```

---

## 🏗️ Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│                    Users & Clients                   │
└────────────┬────────────────────────┬────────────────┘
             │                        │
             ▼                        ▼
    ┌────────────────┐      ┌────────────────┐
    │  Pi Browser    │      │  Web Browser   │
    │  Mobile App    │      │  Desktop App   │
    └────────┬───────┘      └────────┬───────┘
             │                        │
             └────────────┬───────────┘
                          │
              ┌───────────▼───────────┐
              │                       │
    ┌─────────▼─────────┐   ┌────────▼────────┐
    │   FastAPI 8000    │◄─►│   Flask 5000    │
    │ Quantum Conduit   │   │  Glyph Weaver   │
    │                   │   │                 │
    │ • REST APIs       │   │ • Dashboards    │
    │ • WebSocket       │   │ • SVG Art       │
    │ • Auth/Payments   │   │ • Visualizations│
    └─────────┬─────────┘   └────────┬────────┘
              │                      │
              │     ┌────────────────┘
              │     │
    ┌─────────▼─────▼─────┐
    │   Gradio 7860       │
    │   Truth Mirror      │
    │                     │
    │ • Ethical AI        │
    │ • Model Eval        │
    │ • Veto Triad        │
    └─────────┬───────────┘
              │
    ┌─────────▼───────────┐
    │  Shared Resources   │
    │                     │
    │ • Supabase DB       │
    │ • Pi Network        │
    │ • OpenTelemetry     │
    │ • Prometheus        │
    └─────────────────────┘
```

---

## 🎯 Use Cases

### For API Consumers
Use **FastAPI** for:
- Authentication
- Payment processing
- Data operations
- Real-time streams

### For Dashboard Users
Use **Flask** for:
- Visual analytics
- System metrics
- Quantum visualizations
- Report generation

### For AI Evaluation
Use **Gradio** for:
- Model testing
- Ethical audits
- Interactive evaluation
- Community feedback

---

## 📚 Technical Details

### Environment Variables

```bash
# FastAPI
PORT=8000
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-key
PI_NETWORK_API_KEY=your-pi-key

# Flask
FLASK_PORT=5000
FLASK_ENV=development

# Gradio
GRADIO_PORT=7860
GRADIO_SHARE=false

# Shared
DATABASE_URL=postgresql://...
JWT_SECRET=your-secret
ENABLE_TELEMETRY=true
```

### Performance

**FastAPI**:
- High throughput (1000+ req/sec)
- Async operations
- Low latency

**Flask**:
- Moderate throughput
- Synchronous rendering
- Template caching

**Gradio**:
- Interactive performance
- WebSocket streaming
- Dynamic updates

---

## 🛡️ Security

### Authentication Flow

1. User authenticates via FastAPI
2. JWT token issued
3. Token used across all services
4. Flask/Gradio validate via FastAPI

### Data Protection

- HTTPS/TLS encryption
- Secure cookie handling
- CORS configuration
- Rate limiting
- Input validation

---

## See Also

- [[API Reference]] - Complete API docs
- [[Deployment Guide]] - Deployment instructions
- [[Monitoring Observability]] - Observability setup
- [[For Developers]] - Development guide
- [[Genesis Declaration]] - Core principles

---

[[Home]] | [[Ecosystem Overview]] | [[API Reference]]

---

*Three services. One harmony. Infinite possibilities.* 🔥⚡⚖️
