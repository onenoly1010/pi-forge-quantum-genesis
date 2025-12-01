# 🔥 Forge Primer

**Pi Forge Quantum Genesis — Onboarding Guide**

Welcome to the Quantum Pi Forge. This primer will guide you through the architecture, setup, and first steps in contributing to our mythic-operational system.

---

## Architecture Overview

The Pi Forge Quantum Genesis is a **multi-application repository** with three distinct services:

```
┌─────────────────────────────────────────────────────────────────┐
│                    QUANTUM RESONANCE LATTICE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   FastAPI    │    │    Flask     │    │   Gradio     │       │
│  │   (8000)     │    │   (5000)     │    │   (7860)     │       │
│  │              │    │              │    │              │       │
│  │  Production  │    │  Dashboard   │    │   Ethical    │       │
│  │     API      │◄──►│    Viz       │◄──►│    Audit     │       │
│  └──────┬───────┘    └──────────────┘    └──────────────┘       │
│         │                                                        │
│         ▼                                                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Supabase PostgreSQL                     │   │
│  │                  (Authentication + RLS)                    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Service Roles

| Service   | Port  | Purpose                                       |
|-----------|-------|-----------------------------------------------|
| FastAPI   | 8000  | Primary API, WebSocket, Supabase auth         |
| Flask     | 5000  | Quantum resonance dashboard, SVG generation   |
| Gradio    | 7860  | Ethical AI audit tool, model evaluation       |

---

## Quick Setup

### 1. Clone the Repository

```bash
git clone https://github.com/onenoly1010/pi-forge-quantum-genesis.git
cd pi-forge-quantum-genesis
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your Supabase credentials:
# SUPABASE_URL=https://your-project.supabase.co
# SUPABASE_KEY=your-anon-key
# JWT_SECRET=secure-random-string
```

### 3. Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
pip install -r server/requirements.txt
```

### 4. Run Services

```bash
# FastAPI (Production API)
uvicorn server.main:app --reload --host 0.0.0.0 --port 8000

# Flask (Dashboard) - in a separate terminal
python server/app.py

# Gradio (Ethical Audit) - in a separate terminal
python server/canticle_interface.py
```

---

## Resonance Phases

The Pi Forge operates through four quantum phases, each represented by a glyph:

| Phase          | Glyph                           | Description                        |
|----------------|----------------------------------|-----------------------------------|
| Foundation     | `assets/glyphs/foundation.svg`   | Initialization and base setup     |
| Growth         | `assets/glyphs/growth.svg`       | Feature development and expansion |
| Harmony        | `assets/glyphs/harmony.svg`      | Integration and synchronization   |
| Transcendence  | `assets/glyphs/transcendence.svg`| Production readiness and mastery  |

---

## Next Steps

1. Read the [Covenant of Resonant Efficiency](../COVENANT_OF_RESONANT_EFFICIENCY.md) for the full roadmap
2. Review [Guardians](./GUARDIANS.md) to understand team roles
3. Check [Telemetry](./TELEMETRY.md) for monitoring dashboards
4. Explore the codebase and find your first contribution

---

*© 2025 Pi Forge Collective — Quantum Genesis Initiative*
