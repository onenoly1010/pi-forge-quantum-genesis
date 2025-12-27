# 🌐 Mainnet Guide - Production Deployment Checklist

**Last Updated**: December 2025

Complete checklist for Pi Network Mainnet production deployment.

---

## ✅ Pre-Deployment Checklist

### Environment Configuration
- [ ] `PI_NETWORK_MODE=mainnet`
- [ ] `PI_SANDBOX_MODE=false`
- [ ] Production App ID configured
- [ ] Production API Key configured
- [ ] Webhook secret configured
- [ ] Database URL set
- [ ] JWT secret generated

### Pi Network Configuration
- [ ] App approved in Pi Developer Portal
- [ ] Webhook URL configured (HTTPS)
- [ ] Webhook secret generated
- [ ] App tested in sandbox
- [ ] Terms of service accepted

### Infrastructure
- [ ] HTTPS enabled
- [ ] Domain configured
- [ ] Health checks responding
- [ ] Monitoring enabled
- [ ] Backup strategy in place
- [ ] Logs accessible

---

## 🚀 Deployment Steps

### 1. Final Testing in Sandbox
```bash
# Test in sandbox
export PI_NETWORK_MODE=testnet
./scripts/test_pi_integration.sh

# Verify all tests pass
```

### 2. Switch to Mainnet
```bash
# Update environment
export PI_NETWORK_MODE=mainnet
export PI_SANDBOX_MODE=false
export PI_NETWORK_APP_ID=mainnet-app-id
export PI_NETWORK_API_KEY=mainnet-api-key
```

### 3. Deploy to Production
```bash
# Deploy
railway up

# Verify health
curl https://your-domain.com/health
```

### 4. Verify Configuration
```bash
curl https://your-domain.com/api/pi-network/status
# Should show: "mainnet_ready": true
```

### 5. Test Real Payment
1. Open app in Pi Browser
2. Initiate small test payment (0.15 Pi)
3. Approve in Pi wallet
4. Verify in database
5. Check webhook received

---

## 📊 Post-Deployment

### Monitor
- Payment success rate
- Error rates
- Response times
- Webhook delivery

### Verify
- [ ] Payments processing correctly
- [ ] Webhooks received
- [ ] Database updated
- [ ] Users can authenticate
- [ ] No errors in logs

---

## 🆘 Rollback Plan

If issues occur:

```bash
# Switch back to sandbox
export PI_NETWORK_MODE=testnet

# Redeploy
railway up

# Investigate issues
railway logs
```

---

## See Also

- [[Pi Network Overview]] - Integration overview
- [[Payment API]] - API documentation
- [[Deployment Guide]] - Deployment procedures
- [[Troubleshooting]] - Common issues

---

[[Home]] | [[Pi Network Overview]] | [[Deployment Guide]]
