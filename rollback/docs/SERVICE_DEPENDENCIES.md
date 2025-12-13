# 🔗 Service Dependencies Map

## Overview

This document maps the dependencies between services in the Quantum Resonance Lattice platform. Understanding these dependencies is critical for successful rollback operations.

---

## Service Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    QUANTUM RESONANCE LATTICE                │
└─────────────────────────────────────────────────────────────┘

┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│   FastAPI        │      │   Flask          │      │   Gradio         │
│   (Port 8000)    │      │   (Port 5000)    │      │   (Port 7860)    │
│                  │      │                  │      │                  │
│  - Auth Gateway  │      │  - Dashboard     │      │  - Audit UI      │
│  - API Endpoints │      │  - Visualization │      │  - Ethics Eval   │
│  - WebSocket     │      │  - SVG Render    │      │  - Standalone    │
│  - Pi Payments   │      │                  │      │                  │
└────────┬─────────┘      └────────┬─────────┘      └──────────────────┘
         │                         │
         │                         │
         └─────────┬───────────────┘
                   │
                   ▼
         ┌─────────────────┐
         │   Supabase DB   │
         │                 │
         │  - User Auth    │
         │  - Payments     │
         │  - Audits       │
         └─────────────────┘
```

---

## Service Dependency Matrix

| Service | Depends On | Optional Dependencies | Critical? |
|---------|------------|----------------------|-----------|
| **FastAPI** | Supabase | Pi Network API | ✅ Yes |
| **Flask** | None | None | ⚠️ No |
| **Gradio** | None | None | ⚠️ No |
| **Supabase** | External | None | ✅ Yes |
| **Pi Network** | External | None | ⚠️ No |

---

## Detailed Service Dependencies

### 1. FastAPI (Primary Service)

**Port**: 8000  
**Critical**: Yes  
**Type**: Asynchronous (async/await)

#### Dependencies

**Required**:
- **Supabase**: User authentication, database operations
  - Environment: `SUPABASE_URL`, `SUPABASE_KEY`
  - Impact if unavailable: Authentication fails, no database access
  - Fallback: Graceful degradation (some endpoints return 503)

**Optional**:
- **Pi Network API**: Payment processing
  - Environment: `PI_NETWORK_APP_ID`, `PI_NETWORK_API_KEY`
  - Impact if unavailable: Payment features disabled
  - Fallback: Sandbox mode continues to work

#### Provides

- REST API endpoints for frontend
- WebSocket streaming for real-time features
- Authentication token generation (JWT)
- Payment verification endpoints
- Health check endpoints

#### Startup Dependencies

```python
# Required before FastAPI can start:
1. Environment variables loaded (.env)
2. Supabase client initialized
3. Port 8000 available
4. Python dependencies installed
```

#### Rollback Considerations

- **Code rollback**: Safe, service auto-restarts
- **Database rollback**: May require Supabase migration rollback
- **Environment changes**: Restore previous .env if config changed

---

### 2. Flask (Dashboard Service)

**Port**: 5000  
**Critical**: No  
**Type**: Synchronous

#### Dependencies

**Required**: None (completely independent)

**Optional**: None

#### Provides

- Quantum resonance visualization dashboard
- SVG procedural generation
- Template rendering
- Health check endpoint

#### Startup Dependencies

```python
# Required before Flask can start:
1. Port 5000 available
2. Python dependencies installed
3. Template files present
```

#### Rollback Considerations

- **Code rollback**: Safe, independent service
- **Database rollback**: Not applicable (no database)
- **Environment changes**: Not applicable (no env vars)
- **Risk**: Very low - service has no external dependencies

---

### 3. Gradio (Audit Interface)

**Port**: 7860  
**Critical**: No  
**Type**: Standalone interface

#### Dependencies

**Required**: None (completely independent)

**Optional**: None

#### Provides

- Ethical AI audit interface
- Model evaluation tools
- Veto Triad synthesis
- Standalone assessment tools

#### Startup Dependencies

```python
# Required before Gradio can start:
1. Port 7860 available
2. Python dependencies installed (gradio package)
3. Interface definition file present
```

#### Rollback Considerations

- **Code rollback**: Safe, independent service
- **Database rollback**: Not applicable
- **Environment changes**: Not applicable
- **Risk**: Very low - standalone service

---

### 4. Supabase (External Database)

**Type**: External SaaS  
**Critical**: Yes (for FastAPI)

#### Configuration

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
```

#### Tables Used

- `users`: Supabase Auth table (managed by Supabase)
- `payments`: Custom table for Pi Network transactions
- `audits`: Custom table for AI audit records

#### Rollback Considerations

- **Schema changes**: May require manual Supabase migration rollback
- **Data rollback**: Use Supabase dashboard to restore from backup
- **Connection issues**: FastAPI gracefully degrades
- **Risk**: Medium - requires careful coordination

---

### 5. Pi Network API (External Service)

**Type**: External API  
**Critical**: No (optional feature)

#### Configuration

```bash
PI_NETWORK_APP_ID=your-app-id
PI_NETWORK_API_KEY=your-api-key
PI_NETWORK_API_ENDPOINT=https://api.minepi.com
PI_SANDBOX_MODE=false
```

#### Rollback Considerations

- **API changes**: Not in our control
- **Configuration rollback**: Restore previous API keys if changed
- **Risk**: Low - service is optional

---

## Startup Sequence

### Production (Railway)

```
1. Railway provisions container
2. Environment variables loaded from Railway config
3. Docker container starts
4. FastAPI service starts (port 8000)
   └─ Initializes Supabase client
   └─ Connects to database
5. Flask service starts (port 5000)
   └─ Independent startup
6. Gradio service starts (port 7860)
   └─ Independent startup
7. Health checks verify all services
```

### Development (Local)

```
1. Activate virtual environment (.venv)
2. Load environment variables (.env)
3. Start services in parallel:
   ├─ uvicorn server.main:app --port 8000 (FastAPI)
   ├─ python server/app.py (Flask auto-selects 5000)
   └─ python server/canticle_interface.py (Gradio auto-selects 7860)
4. Services run independently
```

---

## Shutdown Sequence

### Graceful Shutdown

```
1. Stop accepting new requests
2. Complete in-flight requests
3. Close database connections
4. Flush logs
5. Exit cleanly
```

### Emergency Shutdown (Rollback)

```
1. Kill all Python processes
2. Clear Python cache
3. Reset git repository
4. Restart services
```

---

## Dependency Failure Scenarios

### Scenario 1: Supabase Unavailable

**Impact**: 
- ✅ FastAPI: Gracefully degrades, returns 503 for DB operations
- ✅ Flask: Unaffected (no dependency)
- ✅ Gradio: Unaffected (no dependency)

**Resolution**:
- Check Supabase status: https://status.supabase.com
- Verify environment variables correct
- Test connection with verification script

### Scenario 2: Pi Network API Down

**Impact**:
- ⚠️ FastAPI: Payment endpoints return errors
- ✅ Other endpoints: Continue working
- ✅ Flask: Unaffected
- ✅ Gradio: Unaffected

**Resolution**:
- Use sandbox mode as fallback
- Display maintenance message for payments
- Core platform remains functional

### Scenario 3: Port Conflicts

**Impact**:
- ❌ Service fails to start if port occupied
- ⚠️ Other services may still run

**Resolution**:
```bash
# Check port usage
lsof -i :8000  # FastAPI
lsof -i :5000  # Flask
lsof -i :7860  # Gradio

# Kill process using port
kill -9 <PID>

# Restart service
```

---

## Rollback Impact by Service

### FastAPI Rollback

**Impact**:
- 🔴 **High**: Authentication may be disrupted
- 🔴 **High**: Payment processing affected
- 🔴 **High**: API endpoints temporarily unavailable

**Duration**: 5-10 minutes

**Mitigation**:
- Communicate downtime window
- Use health endpoint to verify restoration
- Test authentication immediately after rollback

### Flask Rollback

**Impact**:
- 🟡 **Low**: Dashboard temporarily unavailable
- 🟢 **None**: No effect on FastAPI or Gradio

**Duration**: 2-3 minutes

**Mitigation**:
- Independent service, minimal risk
- Can rollback without affecting other services

### Gradio Rollback

**Impact**:
- 🟡 **Low**: Audit interface temporarily unavailable
- 🟢 **None**: No effect on FastAPI or Flask

**Duration**: 2-3 minutes

**Mitigation**:
- Independent service, minimal risk
- Can rollback without affecting other services

---

## Cross-Service Communication

Currently, services operate independently with no direct inter-service communication. They share:

- **Database**: FastAPI → Supabase
- **File System**: Shared frontend assets
- **Environment**: Common .env configuration

Future improvements could add:
- Service mesh for inter-service communication
- Shared cache (Redis)
- Message queue for async tasks

---

## Testing Dependencies

Before rollback:
```bash
# Verify all services can communicate
./rollback/scripts/verify-rollback.sh --check-only
```

After rollback:
```bash
# Verify all dependencies restored
./rollback/scripts/verify-rollback.sh
```

---

© 2025 Pi Forge Collective — Quantum Genesis Initiative
