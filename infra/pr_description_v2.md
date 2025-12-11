# INFRA-002: Fully wired testnet deployment — Railway + GH Actions + rollback

**This PR is 100% ready to deploy the moment it merges.**

### What you get
- Real, working `railway.toml`
- Fully automated CI/CD with hard safety gates
- One-click Railway deployment of all four services
- Post-deploy smoke tests
- Manual confirmed rollback workflow

### Required secrets (add immediately after merge)
```
RAILWAY_TOKEN
RAILWAY_PROJECT_ID
TESTNET_GUARDIAN_URL      → https://guardian-coordinator.up.railway.app
TESTNET_FASTAPI_URL       → https://fastapi-server.up.railway.app
TESTNET_FLASK_URL         → https://flask-dashboard.up.railway.app
TESTNET_GRADIO_URL        → https://gradio-interface.up.railway.app
GUARDIAN_KILL_SWITCH → off
NFT_MINT_VALUE → 0
```

### After merge
1. Add the secrets above
2. Actions → "Deploy → Testnet" → Run workflow (type `testnet`)
3. Hephaestus Guardian goes live on testnet
