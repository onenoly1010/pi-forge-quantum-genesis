# 🎯 PHASE C EXECUTION GUIDE

**Current Status:** Phase A ✅ Complete | Phase B ✅ Complete | **Phase C 🔴 BLOCKER**

This guide walks you through completing Phase C step-by-step.

---

## 🚀 **STEP 1: Generate Secrets** (5 minutes)

### Option A: Using PowerShell Script (Recommended)

```powershell
.\secure-wallet.ps1 rotate-secrets
```

**Output will show:**
```
JWT_SECRET=<64-character-hex-string>
SESSION_SECRET=<48-character-hex-string>
```

**Copy these values to a secure notepad** — you'll need them in Step 2.

### Option B: Manual Generation (if script not found)

```powershell
# Generate JWT_SECRET (32 bytes = 64 hex chars)
$jwt = -join ((0..31) | ForEach-Object { '{0:x2}' -f (Get-Random -Maximum 256) })
Write-Host "JWT_SECRET=$jwt"

# Generate SESSION_SECRET (24 bytes = 48 hex chars)
$session = -join ((0..23) | ForEach-Object { '{0:x2}' -f (Get-Random -Maximum 256) })
Write-Host "SESSION_SECRET=$session"
```

---

## 🚂 **STEP 2: Configure Railway** (15 minutes)

### 2.1 Access Railway Dashboard

1. Open: https://railway.app/dashboard
2. Find your project: `pi-forge-quantum-genesis`
3. Click on the service
4. Click "Variables" tab

### 2.2 Add Environment Variables

Click "New Variable" for each:

```bash
# Database
SUPABASE_URL=https://YOUR_PROJECT.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Authentication
JWT_SECRET=<from-step-1>
SESSION_SECRET=<from-step-1>

# Pi Network
PI_NETWORK_MODE=mainnet
PI_NETWORK_APP_ID=<your-pi-app-id>
PI_NETWORK_API_KEY=<your-pi-api-key>
PI_NETWORK_WEBHOOK_SECRET=<your-webhook-secret>

# Application
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# CORS (if needed)
CORS_ORIGINS=https://quantum-resonance-clean.vercel.app,https://pi-forge-quantum-genesis.vercel.app
```

### 2.3 Where to Find Values

**Supabase Values:**
1. Open: https://supabase.com/dashboard
2. Select your project
3. Settings → API
4. Copy:
   - `URL` → SUPABASE_URL
   - `anon/public` key → SUPABASE_KEY

**Pi Network Values:**
1. Open: https://develop.pi/apps
2. Select your app
3. Copy:
   - App ID
   - API Key
   - Webhook Secret (from settings)

### 2.4 Deploy

1. Click "Redeploy" button
2. Wait 2-3 minutes for deployment
3. Check logs for errors

---

## ▲ **STEP 3: Configure Vercel** (10 minutes)

### 3.1 Access Vercel Dashboard

1. Open: https://vercel.com/dashboard
2. Find your project: `quantum-resonance-clean` or `pi-forge-quantum-genesis`
3. Settings → Environment Variables

### 3.2 Add Environment Variables

Click "Add" for each:

```bash
# Backend Connection
NEXT_PUBLIC_API_URL=https://pi-forge-quantum-genesis.railway.app

# Pi Network (Frontend)
NEXT_PUBLIC_PI_APP_ID=<your-pi-app-id>
PI_APP_SECRET=<your-app-secret>

# Optional: Analytics
NEXT_PUBLIC_ENVIRONMENT=production
```

### 3.3 Deploy

1. Go to "Deployments" tab
2. Click "..." menu on latest deployment
3. Click "Redeploy"
4. Wait 1-2 minutes

---

## 🔐 **STEP 4: Configure GitHub Secrets** (5 minutes)

### 4.1 Access GitHub Settings

1. Open: https://github.com/onenoly1010/pi-forge-quantum-genesis
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"

### 4.2 Add Secrets

```bash
RAILWAY_TOKEN
  ↳ Get from: https://railway.app/account/tokens

GHCR_TOKEN
  ↳ GitHub Settings → Developer settings → Personal access tokens
  ↳ Scopes: read:packages, write:packages

SUPABASE_ACCESS_TOKEN (optional)
  ↳ Get from: https://supabase.com/dashboard/account/tokens
```

---

## ✅ **STEP 5: Verify Deployment** (10 minutes)

### 5.1 Test Railway Backend

```powershell
# Test health endpoint
Invoke-WebRequest -Uri "https://pi-forge-quantum-genesis.railway.app/health" -Method GET

# Expected: Status 200, JSON response
```

### 5.2 Test Vercel Frontend

```powershell
# Open in browser
start "https://quantum-resonance-clean.vercel.app"

# Check browser console for errors (F12)
```

### 5.3 Run Full Verification

```powershell
python verify_production.py
```

**Expected Results:**
- ✅ Environment Configuration
- ✅ File Structure
- ✅ Python Syntax
- ✅ Health Endpoints (200 responses)

---

## 🗄️ **STEP 6: Database Migration** (10 minutes)

### 6.1 Access Supabase SQL Editor

1. Open: https://supabase.com/dashboard
2. Select your project
3. Click "SQL Editor"

### 6.2 Run Migration

1. Open file: `supabase_migrations/001_payments_schema.sql`
2. Copy entire contents
3. Paste into Supabase SQL Editor
4. Click "Run" (bottom right)
5. Verify "Success" message

### 6.3 Verify Tables Created

1. Click "Table Editor" (left sidebar)
2. Should see new tables:
   - `payments`
   - `transactions`
   - `user_balances`
   - (or whatever your schema defines)

---

## 📊 **SUCCESS CHECKLIST**

Mark each as you complete it:

- [ ] Step 1: Secrets generated
- [ ] Step 2: Railway variables configured (8 variables)
- [ ] Step 2: Railway redeployed successfully
- [ ] Step 3: Vercel variables configured (3 variables)
- [ ] Step 3: Vercel redeployed successfully
- [ ] Step 4: GitHub secrets configured (2-3 secrets)
- [ ] Step 5: Railway health endpoint returns 200
- [ ] Step 5: Vercel frontend loads without errors
- [ ] Step 5: verify_production.py passes
- [ ] Step 6: Database migration completed
- [ ] Step 6: Tables visible in Supabase

---

## ⏱️ **TIME TRACKING**

- **Estimated Total:** 55 minutes
- **Started:** _____________
- **Completed:** _____________
- **Actual Duration:** _____________

---

## 🆘 **TROUBLESHOOTING**

### Railway Not Starting

**Check Logs:**
1. Railway dashboard → Logs tab
2. Look for errors like:
   - `KeyError: 'SUPABASE_URL'` → Missing variable
   - `Connection refused` → Wrong database URL
   - `401 Unauthorized` → Wrong API key

**Fix:** Double-check variable names match exactly (case-sensitive)

### Vercel Build Failing

**Check Build Logs:**
1. Vercel → Deployments → Failed deployment → View Logs
2. Common issues:
   - `MODULE_NOT_FOUND` → Missing dependency
   - `Type error` → TypeScript issue
   - `NEXT_PUBLIC_ not defined` → Missing env var

**Fix:** Ensure all `NEXT_PUBLIC_*` variables are set

### Health Endpoint 500 Error

**Likely Causes:**
- Database connection failed
- Missing environment variable
- Python dependency error

**Debug:**
```powershell
# Check Railway logs for stack trace
# Look for lines starting with "ERROR" or "Exception"
```

---

## 📞 **QUICK REFERENCE LINKS**

- **Railway Dashboard:** https://railway.app/dashboard
- **Vercel Dashboard:** https://vercel.com/dashboard
- **Supabase Dashboard:** https://supabase.com/dashboard
- **GitHub Secrets:** https://github.com/onenoly1010/pi-forge-quantum-genesis/settings/secrets/actions
- **Pi Network Developer:** https://develop.pi/apps

---

## 🎯 **NEXT: After Phase C Complete**

Once all checks pass, proceed to:

**Phase D: Quality Gates**
- Add linting configuration
- Set up automated tests
- Update documentation

**Then:**
- Archive old repositories (30 min)
- Final verification (15 min)
- **PROJECT COMPLETE** 🎉

---

**Last Updated:** January 13, 2026  
**Guide Version:** 1.0
