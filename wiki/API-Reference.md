# 📡 API Reference - Comprehensive API Documentation

**Last Updated**: December 2025

Complete API documentation for all Quantum Pi Forge services. For interactive documentation, visit `/docs` on any running service.

---

## 🎯 Overview

Quantum Pi Forge provides multiple API layers across the [[Sacred Trinity]]:

1. **FastAPI** (Port 8000) - Main REST API
2. **Flask** (Port 5000) - Visualization API
3. **Gradio** (Port 7860) - Interactive AI API

---

## ⚡ FastAPI - Main REST API

### Base URLs

**Local**: `http://localhost:8000`  
**Production**: `https://pi-forge-quantum-genesis.railway.app`

### Interactive Documentation

- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`
- **OpenAPI Spec**: `/openapi.json`

### Authentication

All authenticated endpoints require JWT token:

```http
Authorization: Bearer <your_jwt_token>
```

---

## 🔐 Authentication Endpoints

### Register User

```http
POST /api/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response**:
```json
{
  "id": "user-uuid",
  "email": "user@example.com",
  "created_at": "2025-12-21T00:00:00Z"
}
```

### Login

```http
POST /api/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": "user-uuid",
    "email": "user@example.com"
  }
}
```

### Pi Network Authentication

```http
POST /api/auth/pi
Content-Type: application/json

{
  "accessToken": "pi_network_access_token"
}
```

**Response**:
```json
{
  "access_token": "jwt_token",
  "user": {
    "pi_id": "pi_user_id",
    "username": "pi_username"
  }
}
```

---

## 💰 Payment Endpoints

### Approve Payment

**Complete documentation**: [[Payment API]]

```http
POST /api/payments/approve
Authorization: Bearer <token>
Content-Type: application/json

{
  "payment_id": "pi_payment_abc123",
  "amount": 0.15,
  "user_id": "user_uuid",
  "metadata": {}
}
```

**Response**:
```json
{
  "approved": true,
  "payment_id": "pi_payment_abc123",
  "status": "approved",
  "message": "Payment approved - proceed to blockchain"
}
```

### Complete Payment

```http
POST /api/payments/complete
Authorization: Bearer <token>
Content-Type: application/json

{
  "payment_id": "pi_payment_abc123",
  "txid": "blockchain_transaction_hash"
}
```

**Response**:
```json
{
  "success": true,
  "payment_id": "pi_payment_abc123",
  "status": "completed",
  "resonance_state": "harmony",
  "amount": 0.15
}
```

### Payment History

```http
GET /api/payments/history?user_id=<user_id>&limit=10
Authorization: Bearer <token>
```

**Response**:
```json
{
  "payments": [
    {
      "payment_id": "pi_payment_abc123",
      "amount": 0.15,
      "status": "completed",
      "created_at": "2025-12-21T00:00:00Z"
    }
  ],
  "total": 1
}
```

### Pi Webhook

```http
POST /api/pi-webhooks/payment
X-Pi-Signature: <webhook_signature>
Content-Type: application/json

{
  "payment": {
    "identifier": "pi_payment_abc123",
    "status": "completed",
    "transaction": {...}
  }
}
```

**Response**:
```json
{
  "status": "processed"
}
```

---

## 🏥 Health & Status

### Health Check

```http
GET /health
```

**Response**:
```text
OK
```

### Detailed Health

```http
GET /api/health
```

**Response**:
```json
{
  "status": "healthy",
  "database": "connected",
  "pi_network": "operational",
  "services": {
    "fastapi": "up",
    "flask": "up",
    "gradio": "up"
  },
  "timestamp": "2025-12-21T00:00:00Z"
}
```

### Pi Network Status

```http
GET /api/pi-network/status
```

**Response**:
```json
{
  "mode": "mainnet",
  "mainnet_ready": true,
  "webhook_configured": true,
  "api_ready": true,
  "endpoints_available": 13
}
```

### Metrics

```http
GET /api/metrics
```

**Response**: Prometheus-format metrics

---

## 🛡️ Guardian Endpoints

### Guardian Dashboard

```http
GET /api/guardian/dashboard
Authorization: Bearer <guardian_token>
```

**Response**:
```json
{
  "system_status": "healthy",
  "pending_decisions": 3,
  "recent_actions": [...],
  "safety_metrics": {
    "confidence_avg": 0.85,
    "success_rate": 0.95
  }
}
```

### Decision History

```http
GET /api/autonomous/decision-history?limit=50&hours=12
Authorization: Bearer <guardian_token>
```

**Response**:
```json
{
  "decisions": [
    {
      "id": "decision-123",
      "type": "deployment",
      "confidence": 0.92,
      "status": "auto_approved",
      "timestamp": "2025-12-21T00:00:00Z"
    }
  ],
  "total": 10
}
```

### Emergency Stop

```http
POST /api/guardian/emergency-stop
Authorization: Bearer <guardian_token>
Content-Type: application/json

{
  "reason": "Critical security vulnerability",
  "initiated_by": "guardian_username"
}
```

**Response**:
```json
{
  "status": "stopped",
  "all_operations_paused": true,
  "guardians_alerted": true
}
```

---

## 🎨 Flask Visualization API

**Base URL**: `http://localhost:5000`

### Dashboard Data

```http
GET /api/dashboard/data
```

**Response**:
```json
{
  "metrics": {
    "total_users": 1234,
    "payments_today": 56,
    "system_load": 0.45
  },
  "charts": {...}
}
```

### SVG Generation

```http
GET /api/svg/cascade?phase=harmony
```

**Response**: SVG XML content

### Quantum Metrics

```http
GET /api/quantum/metrics
```

**Response**:
```json
{
  "resonance_level": 0.87,
  "phase": "harmony",
  "coherence": 0.91
}
```

---

## ⚖️ Gradio AI Interface

**Base URL**: `http://localhost:7860`

### Ethical Audit

```http
POST /api/ethical-audit
Content-Type: application/json

{
  "text": "Content to audit",
  "context": "usage_context"
}
```

**Response**:
```json
{
  "verdict": "approved",
  "veto_triad": {
    "reactive": 0.85,
    "reflection": 0.90,
    "coherence": 0.88
  },
  "reasoning": "Content aligns with ethical guidelines"
}
```

### Model Evaluation

```http
POST /api/evaluate-model
Content-Type: application/json

{
  "model_input": {...},
  "test_cases": [...]
}
```

**Response**:
```json
{
  "performance": 0.92,
  "metrics": {
    "accuracy": 0.94,
    "precision": 0.91,
    "recall": 0.89
  }
}
```

---

## 📊 Rate Limiting

All APIs implement rate limiting:

**Public endpoints**: 100 requests/minute  
**Authenticated endpoints**: 1000 requests/minute  
**Guardian endpoints**: Unlimited

**Headers**:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1702345678
```

---

## 🔒 CORS Configuration

**Allowed Origins**:
- `https://pi-forge-quantum-genesis.railway.app`
- `https://onenoly1010.github.io`
- `http://localhost:*` (development)

**Allowed Methods**: GET, POST, PUT, DELETE, OPTIONS

---

## 🚨 Error Responses

### Standard Error Format

```json
{
  "detail": "Error message",
  "error_code": "ERROR_CODE",
  "timestamp": "2025-12-21T00:00:00Z"
}
```

### Common Status Codes

- **200** - Success
- **201** - Created
- **400** - Bad Request
- **401** - Unauthorized
- **403** - Forbidden
- **404** - Not Found
- **429** - Too Many Requests
- **500** - Internal Server Error
- **503** - Service Unavailable

---

## 🧪 Testing

### Local Testing

```bash
# Start services
docker-compose up -d

# Test FastAPI
curl http://localhost:8000/health

# Test Flask
curl http://localhost:5000/

# Test Gradio
curl http://localhost:7860/
```

### Integration Tests

```bash
# Run payment integration tests
./scripts/test_pi_integration.sh
```

---

## 📚 Additional Resources

### Full Documentation

For complete endpoint documentation with examples:

1. Visit `/docs` on running FastAPI service
2. Check [[Payment API]] for Pi Network details
3. See [[Sacred Trinity]] for architecture
4. Review source code in `/server/routes/`

### Source Files

- **FastAPI Routes**: `server/routes/*.py`
- **Flask Routes**: `server/app.py`
- **Gradio Interface**: `server/canticle_interface.py`
- **API Models**: `server/models/*.py`

---

## 🔗 SDK & Client Libraries

### JavaScript/TypeScript

```javascript
import { PiForgeClient } from '@quantum-pi-forge/sdk';

const client = new PiForgeClient({
  baseURL: 'https://pi-forge-quantum-genesis.railway.app',
  apiKey: 'your_api_key'
});

// Authenticate
const { accessToken } = await client.auth.login(email, password);

// Make payment
const payment = await client.payments.approve(paymentId, amount);
```

### Python

```python
from quantum_pi_forge import Client

client = Client(
    base_url='https://pi-forge-quantum-genesis.railway.app',
    api_key='your_api_key'
)

# Authenticate
token = client.auth.login(email, password)

# Make payment
payment = client.payments.approve(payment_id, amount)
```

---

## See Also

- [[Payment API]] - Detailed payment documentation
- [[Sacred Trinity]] - Service architecture
- [[For Developers]] - Development guide
- [[Deployment Guide]] - Deployment procedures

---

[[Home]] | [[Sacred Trinity]] | [[Payment API]]

---

*Complete, documented, accessible APIs for the entire constellation.* 📡⚛️🔥
