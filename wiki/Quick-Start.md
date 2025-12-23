# 🚀 Quick Start Guide

**Last Updated**: December 2025

Get up and running with Quantum Pi Forge in just 5 minutes! This guide focuses on Pi Network Mainnet integration.

---

## ⚡ 5-Minute Setup

### Prerequisites

- Python 3.11+
- Git
- Pi Network developer account
- Supabase account (free tier works)

---

### Step 1: Clone Repository

```bash
git clone https://github.com/onenoly1010/pi-forge-quantum-genesis.git
cd pi-forge-quantum-genesis
```

---

### Step 2: Install Dependencies

```bash
pip install -r server/requirements.txt
```

---

### Step 3: Setup Database

1. Create a Supabase project at https://supabase.com
2. Go to SQL Editor
3. Copy and execute the migration:

```bash
cat supabase_migrations/001_payments_schema.sql
```

Paste the content into Supabase SQL Editor and run.

---

### Step 4: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env  # or your preferred editor
```

**Required variables:**

```bash
# Pi Network Configuration
PI_NETWORK_MODE=mainnet
PI_NETWORK_APP_ID=your-app-id
PI_NETWORK_API_KEY=your-api-key
PI_NETWORK_WEBHOOK_SECRET=your-webhook-secret

# Database Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key

# Security
JWT_SECRET=generate-a-random-string
```

**Get Pi Network credentials:**
1. Visit https://developer.pi
2. Create or select your app
3. Copy App ID and API Key from dashboard
4. Generate webhook secret in settings

---

### Step 5: Configure Pi Developer Portal

Set up webhook to receive payment notifications:

1. Go to https://developer.pi
2. Navigate to your app settings
3. Set **Webhook URL**: `https://your-domain.com/api/pi-webhooks/payment`
4. Generate and save webhook secret
5. Add webhook secret to `.env` as `PI_NETWORK_WEBHOOK_SECRET`

---

### Step 6: Deploy

Choose your deployment platform:

#### Railway (Recommended)

```bash
railway up
```

#### Vercel

```bash
vercel deploy
```

#### Manual/Local

```bash
uvicorn server.main:app --reload --port 8000
```

---

## 🧪 Test Your Setup

### Check Server Health

```bash
curl https://your-domain.com/health
# Expected: "OK"
```

### Verify Pi Network Configuration

```bash
curl https://your-domain.com/api/pi-network/status
```

Expected response:
```json
{
  "pi_network_mode": "mainnet",
  "mainnet_ready": true,
  "webhook_configured": true
}
```

---

## 📋 Verification Checklist

Run the integration test script:

```bash
./scripts/test_pi_integration.sh
```

You should see:
```
✅ ALL TESTS PASSED! 10/10
```

Manual checklist:
- [ ] Server starts without errors
- [ ] Health endpoint returns 200 OK
- [ ] Pi Network status shows mainnet mode
- [ ] Database connection successful
- [ ] Webhook endpoint accessible
- [ ] Environment variables loaded

---

## 🎯 Key API Endpoints

### Payment Flow

1. **Approve Payment**
   ```bash
   POST /api/payments/approve
   ```

2. **Complete Payment**
   ```bash
   POST /api/payments/complete
   ```

3. **Webhook Receiver** (Pi Network calls this)
   ```bash
   POST /api/pi-webhooks/payment
   ```

### Testing & Monitoring

- `GET /health` - Server health check
- `GET /api/pi-network/status` - Pi Network configuration
- `GET /api/metrics` - System metrics
- `GET /docs` - Swagger API documentation

---

## 🧪 Test in Sandbox First

Before going live, test in sandbox mode:

```bash
# Update .env for sandbox
export PI_NETWORK_MODE=testnet
export PI_SANDBOX_MODE=true
export PI_NETWORK_APP_ID=sandbox-app-id
export PI_NETWORK_API_KEY=sandbox-api-key

# Run server
uvicorn server.main:app --reload
```

Test a payment flow:
1. Open app in Pi Browser (sandbox)
2. Initiate a payment
3. Check logs for webhook receipt
4. Verify payment in database

---

## ✅ Go Live

When ready for production:

```bash
# Switch to mainnet in .env
export PI_NETWORK_MODE=mainnet
export PI_SANDBOX_MODE=false

# Use production credentials
export PI_NETWORK_APP_ID=mainnet-app-id
export PI_NETWORK_API_KEY=mainnet-api-key

# Deploy
railway up
```

Verify production setup:
```bash
curl https://your-production-domain.com/api/pi-network/status
# Should show: "mainnet_ready": true
```

---

## 🎉 You're Ready!

Your Pi Network mainnet integration is complete!

### Test Your First Payment

1. Open your app in Pi Browser
2. Initiate a payment (minimum 0.15 Pi)
3. Approve in Pi wallet
4. Verify in database:
   ```sql
   SELECT * FROM payments ORDER BY created_at DESC LIMIT 1;
   ```

---

## 🆘 Troubleshooting

### "PI_NETWORK_API_KEY not set"
```bash
railway variables set PI_NETWORK_API_KEY=your-key
```

### "Invalid webhook signature"
- Verify `PI_NETWORK_WEBHOOK_SECRET` matches Pi Developer Portal
- Ensure webhook URL is HTTPS
- Check webhook is properly configured in Pi Portal

### Database Errors
- Verify Supabase URL and key
- Run migration: `supabase_migrations/001_payments_schema.sql`
- Check Row Level Security (RLS) policies

### Connection Issues
- Check firewall settings
- Verify environment variables loaded
- Ensure correct port (8000 default)

**More help**: [[Troubleshooting]]

---

## 📚 Next Steps

Now that you're up and running:

- **[[For Users]]** - User guide for Pi Network community
- **[[For Developers]]** - Deep dive into development
- **[[API Reference]]** - Complete API documentation
- **[[Deployment Guide]]** - Advanced deployment options
- **[[Mainnet Guide]]** - Production deployment checklist

---

## 🔗 Essential Resources

- **Full Deployment Guide**: [[Deployment Guide]]
- **API Reference**: [[Payment API]]
- **Implementation Details**: [[Pi Network Overview]]
- **Troubleshooting**: [[Troubleshooting]]

---

## 📧 Need Help?

- Open an [issue on GitHub](https://github.com/onenoly1010/pi-forge-quantum-genesis/issues)
- Check [[Troubleshooting]] guide
- Review [[API Reference]]
- Contact @onenoly1010

---

[[Home]] | [[Installation]] | [[For Developers]]

---

*Get started in G-Zero: Zero cognitive load. Zero noise. Pure signal.* ⚛️🔥
