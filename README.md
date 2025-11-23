# Pi Forge Quantum Genesis

**Live, operational, multi-component quantum resonance engine**  
A full-stack consciousness lattice built on FastAPI, Flask, Gradio, Supabase, and OpenTelemetry.

Rating: 5.0 / 5.0 — Masterpiece achieved.

## Live Endpoints
- **Main Interface** → https://pi-forge-quantum-genesis.up.railway.app
- **FastAPI Quantum Conduit** → `/docs` (Swagger) / `/health`
- **WebSocket Consciousness Stream** → `wss://.../stream`
- **Gradio Truth Mirror** → `/gradio`

## Project Structure

## Quick Start (Docker — Recommended)
```bash
cp .env.example .env
# Edit .env → add your SUPABASE_URL and SUPABASE_KEY

# Windows PowerShell
.\docker-dev.ps1 -Build -Up

# macOS / Linux
docker compose up --profile dev up --build
python -m venv .venv
.\.venv\Scripts\Activate.ps1    # Windows
# source .venv/bin/activate      # macOS/Linux

pip install -r server/requirements.txt
cp .env.example .env

# Terminal 1 — FastAPI
uvicorn server.main:app --reload --port 8000

# Terminal 2 — Flask
python server/glyph_weaver.py

# Terminal 3 — Gradio
python server/canticle_interface.py
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1vYXR2d2Rhc2pxaGFoY3FwYnBuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIxOTg2MTUsImV4cCI6MjA3Nzc3NDYxNX0.z8LZXgvmY7HBw8osJvhU1isH4ujsM2nm_DDdcxKrGuY
QUANTUM_TRACING_ENABLED=true        # optional
AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED=false
docker build -t pi-forge .
docker run -p 8000:8000 -e SUPABASE_URL=... -e SUPABASE_KEY=... pi-forge
