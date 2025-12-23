# 🔌 Payment API - Payment Flow & API Endpoints

**Last Updated**: December 2025

Complete API documentation for Pi Network payment integration.

---

## 🎯 Payment Flow

1. **Create Payment** (Pi SDK on frontend)
2. **Approve Payment** → `POST /api/payments/approve`
3. **User Confirms** (in Pi wallet)
4. **Blockchain Processes** (Pi Network)
5. **Webhook Notification** → `POST /api/pi-webhooks/payment`
6. **Complete Payment** → `POST /api/payments/complete`
7. **Confirmation** (to user)

---

## 📡 API Endpoints

### 1. Approve Payment

```http
POST /api/payments/approve
Authorization: Bearer <jwt_token>
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

---

### 2. Complete Payment

```http
POST /api/payments/complete
Authorization: Bearer <jwt_token>
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
  "amount": 0.15
}
```

---

### 3. Payment History

```http
GET /api/payments/history?user_id=<user_id>&limit=10
Authorization: Bearer <jwt_token>
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
  ]
}
```

---

### 4. Pi Webhook (Pi Network calls this)

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

## 🔐 Authentication

All endpoints (except webhook) require JWT:
```http
Authorization: Bearer <your_jwt_token>
```

---

## ✅ Testing

### Sandbox Mode

```bash
# Use testnet
export PI_NETWORK_MODE=testnet
export PI_SANDBOX_MODE=true

# Test payment
./scripts/test_pi_integration.sh
```

---

## See Also

- [[Pi Network Overview]] - Integration overview
- [[API Reference]] - Complete API docs
- [[Mainnet Guide]] - Production guide
- [[Quick Start]] - Setup guide

---

[[Home]] | [[Pi Network Overview]] | [[API Reference]]
