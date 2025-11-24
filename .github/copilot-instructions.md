# Pi Forge Quantum Genesis - Copilot Instructions

## Project Overview

Pi Forge Quantum Genesis is a multi-application repository featuring three distinct services forming a "Quantum Resonance Lattice":

1. **FastAPI Production Server** (`server/main.py`) - Primary API with Supabase auth & WebSocket (Port 8000)
2. **Flask Dashboard** (`server/app.py`) - Quantum resonance visualization (Port 5000)
3. **Gradio Interface** (`server/canticle_interface.py`) - Ethical AI audit tool (Port 7860)

## Architecture Principles

### Multi-Application Structure

All three applications run in a single deployment with:
- **FastAPI (8000)**: Async production core for APIs and WebSocket
- **Flask (5000)**: Sync visualization layer for templates and SVG rendering
- **Gradio (7860)**: Interactive ethics portal for standalone audits

**Key Pattern**: Single Dockerfile/Railway deployment; shared JWT auth; distinct responsibilities.

## Development Setup

### Local Development (Windows/PowerShell)

```powershell
# Quick start
.\scripts\run.ps1

# Or manually:
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r server/requirements.txt

# Start individual services:
uvicorn server.main:app --reload --host 0.0.0.0 --port 8000  # FastAPI
python server/app.py                                         # Flask (auto port 5000)
python server/canticle_interface.py                          # Gradio (auto port 7860)
```

### Environment Variables (Required)

Create `.env` file:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
JWT_SECRET=secure-random-string
```

## When to Modify Which Application

### Choose `main.py` (FastAPI) for:
- User authentication (login/register)
- Production APIs and WebSocket endpoints
- Database operations with Supabase
- Pi Network payment callbacks

### Choose `app.py` (Flask) for:
- Dashboard routes and resonance visualization
- SVG procedural generation
- Legacy template serving

### Choose `canticle_interface.py` (Gradio) for:
- Ethical audit interfaces
- Standalone model evaluation
- Gradio component modifications

## Key Integration Points

### Authentication & Database

```python
# Supabase client initialization (main.py)
from supabase import create_client
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

# JWT dependency injection
async def get_current_user(token: str = Depends(oauth2_scheme)):
    return supabase.auth.get_user(token)
```

**Database Schema**:
- `users`: Standard Supabase Auth table
- `payments`: id, user_id, tx_hash, resonance_state, amount
- `audits`: id, tx_id, risk_score, narrative

### Pi Network Integration

Payment flow involves:
1. Frontend initiates payment via Pi SDK
2. Backend verifies via `/api/verify-payment`
3. Resonance visualization triggers via WebSocket
4. SVG animation renders (4-phase cascade)

```javascript
// Frontend pattern (frontend/pi-forge-integration.js)
PiForge.renderResonanceViz(txHash)  // Triggers 4-phase SVG cascade
PiForge.updateResonanceState(event) // WebSocket sync
```

## Testing

### Health Endpoints
- FastAPI: `GET /` → `{"status": "healthy", "service": "FastAPI"}`
- Flask: `GET /health` → Health check template
- Gradio: Access UI at `http://localhost:7860`

### Running Tests
```powershell
# FastAPI tests
pytest server/test_main.py -v

# Flask tests  
pytest server/test_app.py -v

# Manual Gradio testing
python server/canticle_interface.py  # Visit http://localhost:7860
```

## Deployment

### Railway Configuration

**Critical**: Use `builder = "DOCKERFILE"` (NOT Nixpacks)

```toml
# railway.toml
[build]
builder = "DOCKERFILE"

[deploy]
numReplicas = 1
```

**Environment Setup**: Set `SUPABASE_URL` and `SUPABASE_KEY` in Railway dashboard before deployment.

### Dockerfile Pattern

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY server/ ./server/
COPY frontend/ ./frontend/
COPY . .
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "$PORT"]
```

## Code Patterns

### Async Patterns (FastAPI)
- All FastAPI routes use `async/await`
- Comprehensive error handling for service unavailability
- WebSocket endpoints require JWT token in query params

### Frontend Visualization
- SVG-based fractal animations with 4-phase cascade
- HSL color cycling: Red (Foundation) → Green (Growth) → Blue (Harmony) → Purple (Transcendence)
- Auto-cleanup after 10 seconds

### Testing Patterns
```python
# Async testing pattern
@pytest.mark.asyncio
async def test_endpoint():
    # Test implementation
```

## Common Issues

- **Supabase connection fails**: Check environment variables are set
- **WebSocket auth errors**: Ensure valid JWT token in query params
- **Railway deployment**: Always use Dockerfile builder, not Nixpacks
- **Port conflicts**: Ensure 8000, 5000, 7860 are available

## Quick Reference

### Development Commands

```powershell
# Windows/PowerShell
.\scripts\run.ps1                    # Start all services
```

```bash
# Individual services (cross-platform)
uvicorn server.main:app --reload    # FastAPI only
python server/app.py                # Flask only
python server/canticle_interface.py # Gradio only
```

### Testing Commands

```bash
pytest server/ -v                   # Run all tests
curl http://localhost:8000/         # FastAPI health
curl http://localhost:5000/health   # Flask health
```

### Environment Setup

```bash
cp .env.example .env                # Setup environment file
```

```python
# Test Supabase connection
import os
from supabase import create_client

try:
    client = create_client(
        os.getenv('SUPABASE_URL', ''),
        os.getenv('SUPABASE_KEY', '')
    )
    print('✅ Supabase connection successful')
except Exception as e:
    print(f'❌ Supabase connection failed: {e}')
```

## Project-Specific Conventions

- Use "Quantum Resonance" terminology in user-facing text
- Environment variables prefixed with service name (e.g., `SUPABASE_*`)
- WebSocket endpoints use descriptive paths (e.g., `/ws/collective-insight`)
- All FastAPI routes use async/await patterns
- Comprehensive error handling with descriptive logging

## Directory Structure

```
.
├── .github/
│   └── copilot-instructions.md
├── server/
│   ├── main.py              # FastAPI production server
│   ├── app.py               # Flask dashboard
│   ├── canticle_interface.py # Gradio audit tool
│   └── requirements.txt
├── frontend/
│   └── pi-forge-integration.js
├── scripts/
│   └── run.ps1              # Development launcher
├── tests/
│   ├── test_main.py
│   ├── test_app.py
│   └── test_quantum_resonance.py
├── Dockerfile
├── railway.toml
└── .env.example
```
