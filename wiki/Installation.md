# 📦 Installation Guide

**Last Updated**: December 2025

Comprehensive installation instructions for setting up the Quantum Pi Forge development environment.

---

## 🎯 Overview

This guide covers:
- Local development setup
- Docker-based development
- Production deployment
- Environment configuration
- Database setup
- Testing verification

For a faster setup, see [[Quick Start]].

---

## Prerequisites

### Required Software

- **Python 3.11+** - Primary backend language
- **Node.js 18+** - Frontend tooling (optional)
- **Git** - Version control
- **Docker** (optional) - Containerized development
- **PostgreSQL** or **Supabase** - Database

### Required Accounts

- **Pi Network Developer** - https://developer.pi
- **Supabase** (recommended) - https://supabase.com
- **Railway** or **Vercel** - Deployment platform (optional)

---

## 🐍 Python Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/onenoly1010/pi-forge-quantum-genesis.git
cd pi-forge-quantum-genesis
```

### 2. Create Virtual Environment

```bash
# Create venv
python -m venv .venv

# Activate (Linux/Mac)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install all dependencies
pip install -r server/requirements.txt

# For development (includes testing tools)
pip install -r server/requirements-dev.txt  # if available
```

### 4. Verify Installation

```bash
# Check Python version
python --version  # Should be 3.11+

# Verify key packages
python -c "import fastapi, flask, gradio; print('✅ Core packages installed')"
```

---

## 🐳 Docker Development Setup

### 1. Install Docker

- **Mac**: Docker Desktop for Mac
- **Windows**: Docker Desktop for Windows
- **Linux**: Docker Engine

### 2. Build Containers

```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build api
```

### 3. Start Services

```bash
# Start all services
docker-compose up -d

# Start specific service
docker-compose up -d api

# View logs
docker-compose logs -f
```

### 4. Verify Services

```bash
# Check running containers
docker-compose ps

# Test API
curl http://localhost:8000/health
```

---

## 🗄️ Database Setup

### Option 1: Supabase (Recommended)

#### Create Project

1. Go to https://supabase.com
2. Create a new project
3. Wait for provisioning (~2 minutes)
4. Note your project URL and anon key

#### Run Migrations

1. Go to SQL Editor in Supabase dashboard
2. Copy content from `supabase_migrations/001_payments_schema.sql`
3. Paste and execute in SQL Editor
4. Verify tables created:
   - `payments`
   - `users`
   - `sessions`

#### Configure Environment

```bash
# Add to .env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
DATABASE_URL=postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres
```

### Option 2: Local PostgreSQL

#### Install PostgreSQL

```bash
# Mac
brew install postgresql

# Ubuntu/Debian
sudo apt-get install postgresql

# Windows
# Download from https://www.postgresql.org/download/windows/
```

#### Create Database

```bash
# Start PostgreSQL
pg_ctl -D /usr/local/var/postgres start

# Create database
createdb pi_forge

# Run migrations
psql pi_forge < supabase_migrations/001_payments_schema.sql
```

#### Configure Environment

```bash
# Add to .env
DATABASE_URL=postgresql://localhost/pi_forge
```

---

## ⚙️ Environment Configuration

### 1. Copy Template

```bash
cp .env.example .env
```

### 2. Configure Variables

Edit `.env` with your settings:

```bash
# === Pi Network Configuration ===
PI_NETWORK_MODE=mainnet                    # or testnet for sandbox
PI_NETWORK_APP_ID=your-app-id              # From developer.pi
PI_NETWORK_API_KEY=your-api-key            # From developer.pi
PI_NETWORK_WEBHOOK_SECRET=your-secret      # Generate in Pi Portal

# === Database Configuration ===
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
DATABASE_URL=postgresql://...

# === Security ===
JWT_SECRET=generate-random-secret-here     # Use: openssl rand -hex 32
SECRET_KEY=another-random-secret           # Use: openssl rand -hex 32

# === Observability (Optional) ===
ENABLE_TELEMETRY=false                     # Set true for monitoring
SENTRY_DSN=                                # Optional error tracking

# === Deployment (Optional) ===
RAILWAY_ENVIRONMENT=production
VERCEL_ENV=production
```

### 3. Generate Secrets

```bash
# Generate JWT secret
openssl rand -hex 32

# Generate secret key
openssl rand -hex 32
```

---

## 🔑 Pi Network Configuration

### 1. Create Pi App

1. Visit https://developer.pi
2. Click "Create App"
3. Fill in app details:
   - Name: Your app name
   - Category: Choose appropriate category
   - Description: App description

### 2. Get Credentials

1. Go to app dashboard
2. Copy **App ID**
3. Copy **API Key**
4. Add to `.env`

### 3. Configure Webhook

1. In Pi Developer Portal, go to app settings
2. Set **Webhook URL**: `https://your-domain.com/api/pi-webhooks/payment`
3. Click "Generate Secret"
4. Copy webhook secret
5. Add to `.env` as `PI_NETWORK_WEBHOOK_SECRET`

### 4. Test Connection

```bash
# Start server
uvicorn server.main:app --reload

# Test Pi Network status
curl http://localhost:8000/api/pi-network/status
```

---

## 🧪 Testing Setup

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=server --cov-report=html

# Run specific test file
pytest tests/test_health.py -v

# Run integration tests
./scripts/test_pi_integration.sh
```

### Disable Telemetry for Tests

```bash
# Tests should run with telemetry disabled
ENABLE_TELEMETRY=false pytest
```

---

## 🚀 Local Development

### Start Development Server

#### FastAPI (Port 8000)
```bash
uvicorn server.main:app --reload --port 8000
```

#### Flask (Port 5000)
```bash
cd server
python -m flask run --port 5000
```

#### Gradio (Port 7860)
```bash
python server/gradio_app.py
```

### Access Services

- **FastAPI API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Flask Dashboard**: http://localhost:5000
- **Gradio Interface**: http://localhost:7860

---

## 📊 Monitoring Setup (Optional)

### Start Observability Stack

```bash
# Start OpenTelemetry, Prometheus, Grafana
docker-compose up -d

# Enable telemetry in .env
ENABLE_TELEMETRY=true

# Start application with telemetry
ENABLE_TELEMETRY=true python server/main.py
```

### Access Monitoring

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)
- **OTLP HTTP**: http://localhost:4318
- **OTLP gRPC**: http://localhost:4317

**More details**: [[Monitoring Observability]]

---

## ✅ Verification

### Check Installation

```bash
# Run verification script
./scripts/verify_installation.sh

# Or manual checks:
python --version                           # 3.11+
pip list | grep fastapi                    # Installed
curl http://localhost:8000/health          # "OK"
```

### Verification Checklist

- [ ] Python 3.11+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Database created and migrated
- [ ] Environment variables configured
- [ ] Pi Network credentials set
- [ ] Server starts without errors
- [ ] Health endpoint responds
- [ ] Tests pass

---

## 🆘 Troubleshooting

### Import Errors

```bash
# Reinstall dependencies
pip install --force-reinstall -r server/requirements.txt
```

### Database Connection Issues

```bash
# Check database is running
psql -l  # List databases

# Test connection
python -c "from supabase import create_client; print('✅ Database connection works')"
```

### Port Already in Use

```bash
# Find process using port
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Kill process or use different port
uvicorn server.main:app --reload --port 8001
```

**More solutions**: [[Troubleshooting]]

---

## 📚 Next Steps

Installation complete! Now:

- **[[Quick Start]]** - Quick 5-minute setup
- **[[For Developers]]** - Development workflow
- **[[Deployment Guide]]** - Deploy to production
- **[[API Reference]]** - Explore the API

---

## See Also

- [[Quick Start]] - Faster setup guide
- [[For Developers]] - Developer workflow
- [[Deployment Guide]] - Production deployment
- [[Monitoring Observability]] - Set up monitoring
- [[Troubleshooting]] - Common issues

---

[[Home]] | [[Quick Start]] | [[For Developers]]
