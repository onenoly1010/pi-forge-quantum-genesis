# Render setup instructions

This document shows steps to deploy `pi-forge-backend` on Render and verifies required environment variables.

### Quick steps (UI)
1. Sign in to https://dashboard.render.com
2. New → Web Service → Connect GitHub → select `onenoly1010/pi-forge-quantum-genesis`
3. Configure:
   - **Name:** `pi-forge-backend`
   - **Environment:** Docker
   - **Dockerfile Path:** `Dockerfile`
   - **Branch:** `main`
4. Under **Environment** add the following variables (use secrets for sensitive values):
   - PORT = `8000`
   - PI_API_KEY = (set from your Pi Developer Portal)
   - PI_APP_ID = `Quantum Pi Forge`
   - PI_APP_SECRET = (set in Render secrets — **not** present in repo `.env`)
   - SAFE_MULTISIG_ADDRESS = (your created Safe address)
   - AI_SIGNER_PRIVATE_KEY = (secret; repo uses `AI_PRIVATE_KEY` — keep alias in mind)
   - AI_WALLET_ADDRESS = `0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67`
   - OINIO_CONTRACT_ADDRESS = `0x07f43E5B1A8a0928B364E40d5885f81A543B05C7`
   - POLYGON_RPC_URL = `https://polygon-rpc.com`

### Verification checklist
- [ ] Confirm `PI_API_KEY` exists in your Pi Developer Console
- [ ] Add `PI_APP_SECRET` to Render; it's missing in repo `.env`
- [ ] Add `AI_SIGNER_PRIVATE_KEY` as a secret in Render (do not commit private keys)
- [ ] If your code expects `SERVER_PORT`, ensure `PORT` is mapped or update app to read `PORT` first

### Notes & Recommendations
- The repo `.env` uses `SERVER_PORT` and `AI_PRIVATE_KEY`. For Render use `PORT` and `AI_SIGNER_PRIVATE_KEY` as environment-variable names; the code currently reads `AI_PRIVATE_KEY` and `SERVER_PORT`, so we set both envs in the manifest to ensure compatibility.
- To avoid leaking secrets, do NOT commit real private keys. Use the Render Dashboard secret store.
- If you want IaC for Render, `infra/render.yaml` is included at the repo root — use it for automation or import into Render.

### Troubleshooting
- If your service fails to start, check `PORT` mapping and logs in Render Dashboard. Ensure the Dockerfile exposes/binds to the provided `PORT`.
