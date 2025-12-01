# Forge Primer

> *Your guide to navigating the Pi Forge Quantum Genesis ecosystem*

## Welcome, Pioneer

The Pi Forge is a multi-dimensional platform where blockchain meets quantum-inspired principles. This primer will help you understand the core concepts and get started with contributing.

---

## Core Concepts

### Quantum Resonance Lattice
The system operates as a harmonious triad:
- **FastAPI Production Server** (port 8000): The pulsing heartbeat
- **Flask Dashboard** (port 5000): The lyrical lens
- **Gradio Interface** (port 7860): The moral melody

### The Four Phases of Resonance
1. **Foundation** (Red): Initial state, establishing connection
2. **Growth** (Green): Processing and expanding
3. **Harmony** (Blue): Verification and balance
4. **Transcendence** (Purple): Completion and elevation

---

## Getting Started

### Prerequisites
- Python 3.10 or higher
- Node.js 18+ (for frontend development)
- Docker (optional, for containerized deployment)

### Local Development
```powershell
# Clone and setup
git clone https://github.com/onenoly1010/pi-forge-quantum-genesis.git
cd pi-forge-quantum-genesis

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate   # Unix/Mac

# Install dependencies
pip install -r server/requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your Supabase credentials

# Start the services
uvicorn server.main:app --reload --port 8000
```

---

## Contributing

### Commit Vows
Follow the Commit Vows convention for all commits:
- `feat(scope): description` - New features
- `fix(scope): description` - Bug fixes
- `docs(scope): description` - Documentation changes
- `chore(scope): description` - Maintenance tasks
- `test(scope): description` - Test additions/modifications

### Code Review Process
1. Create a feature branch from `main`
2. Make focused, atomic commits
3. Open a pull request with clear description
4. Address reviewer feedback
5. Obtain guardian approval before merge

---

## Architecture Overview

```
pi-forge-quantum-genesis/
├── server/               # Backend services
│   ├── main.py          # FastAPI production app
│   ├── app.py           # Flask dashboard
│   └── canticle_interface.py  # Gradio ethics tool
├── frontend/            # Client-side assets
├── docs/                # Documentation
├── covenants/           # Phase-specific covenants
├── assets/              # Static resources
│   └── glyphs/          # Resonance phase SVGs
└── ledger/              # Transaction records
```

---

## Resources

- [Covenant of Resonant Efficiency](../COVENANT_OF_RESONANT_EFFICIENCY.md)
- [Guardian Directory](./GUARDIANS.md)
- [Telemetry Overview](./TELEMETRY.md)
- [Ritual Calendar](./RITUAL_CALENDAR.md)

---

*Last Updated: {current_date}*
