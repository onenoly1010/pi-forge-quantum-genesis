# 0G DEX Deployment Status

**Issue**: #108 - Resolve 0G Aristotle Mainnet DEX Router Address  
**Status**: 🔴 **BLOCKING MAINNET LAUNCH**  
**Priority**: CRITICAL  
**Date**: 2025-12-22  

---

## 🎯 What's Blocking Launch

The OINIO flash-launch system is **99% complete**. The **ONLY** missing piece is:

```bash
ZERO_G_UNIVERSAL_ROUTER=<address_needed>
```

Without this address, the system cannot execute swaps on 0G Aristotle Mainnet.

---

## 📊 Current State

### ✅ What's READY

1. **Complete Deployment Infrastructure**
   - Location: `/contracts/0g-uniswap-v2/`
   - Foundry scripts: `scripts/deploy.sh`
   - Deployment guide: `docs/0G_DEX_DEPLOYMENT.md`
   - Quick start: `docs/0G_DEX_QUICKSTART.md`
   - Status: ✅ **READY TO DEPLOY**

2. **Backend Integration**
   - Config: `server/config.py` ✅
   - Swap client: `server/integrations/zero_g_swap.py` ✅
   - Status: ✅ **IMPLEMENTED & TESTED**

3. **Configuration Templates**
   - Root: `.env.launch.example` ✅
   - Contracts: `contracts/0g-uniswap-v2/.env.example` ✅
   - Network config: `config/networks.json` ✅
   - Status: ✅ **READY FOR ADDRESSES**

4. **Documentation**
   - Full deployment guide: 26 pages ✅
   - Quick start: 4-page guide ✅
   - Integration examples: Complete ✅
   - Troubleshooting: Comprehensive ✅
   - Status: ✅ **PRODUCTION READY**

### ❌ What's MISSING

1. **Deployed Contract Addresses** 🔴
   - `ZERO_G_W0G=<NOT_DEPLOYED>`
   - `ZERO_G_FACTORY=<NOT_DEPLOYED>`
   - `ZERO_G_UNIVERSAL_ROUTER=<NOT_DEPLOYED>`
   - Status: ❌ **MUST RESOLVE**

2. **Live Configuration File** 🔴
   - `.env.launch` does NOT exist
   - Only template (`.env.launch.example`) exists
   - Status: ❌ **AWAITING ADDRESSES**

---

## 🔍 Resolution Options

### Option A: Find Canonical DEX (PREFERRED - 2-4 hours)

**Requires external research** (cannot be done in this sandbox):

1. **Join 0G Discord** (https://discord.gg/0gnetwork)
   - Ask in #dev or #support: "What is the canonical DEX router address for Aristotle Mainnet (Chain ID 16661)?"
   - Ping: @0g-team, @moderators
   - Look for: Official announcements, pinned messages

2. **Check 0G Block Explorer** (https://chainscan.0g.ai)
   - Search: "router", "swap", "dex", "uniswap"
   - Filter: Verified contracts only
   - Check: Recent deployments, high transaction volume
   - Look for: UniswapV2Router02, PancakeRouter, similar

3. **Review 0G Documentation** (https://docs.0g.ai)
   - Search: Ecosystem projects, DeFi integrations
   - Check: GitHub repos (https://github.com/0glabs)
   - Look for: Official DEX announcements

4. **Community Research**
   - Twitter: Search "@0G_labs DEX" or "0G swap"
   - Telegram: Check official 0G channels
   - Medium: Look for 0G ecosystem updates

**If Found:**
```bash
# Update .env.launch with canonical address
ZERO_G_UNIVERSAL_ROUTER=0x[CANONICAL_ADDRESS]
ZERO_G_W0G=0x[W0G_ADDRESS_FROM_CANONICAL]
ZERO_G_FACTORY=0x[FACTORY_ADDRESS_FROM_CANONICAL]
ROUTER_SOURCE=canonical
```

**Timeline**: 2-4 hours (research + verification)

---

### Option B: Deploy Own DEX (FALLBACK - 2-3 hours)

**Infrastructure is 100% ready**. Follow these steps:

#### Step 1: Prerequisites (15 min)
```bash
# Install Foundry
curl -L https://foundry.paradigm.xyz | bash
foundryup

# Verify installation
forge --version
cast --version
```

#### Step 2: Prepare Wallet (10 min)
- Minimum balance: **0.5 0G** (recommended: 1.0 0G)
- Get private key from funded wallet
- Never commit private keys!

#### Step 3: Deploy Contracts (60 min)
```bash
cd /contracts/0g-uniswap-v2

# Setup dependencies
./scripts/setup.sh

# Configure deployment
cp .env.example .env
# Edit .env with your private key and deployer address

# Deploy Phase 1: W0G + Factory
./scripts/deploy.sh

# Copy PAIR_INIT_CODE_HASH from output

# Update UniswapV2Library.sol with init code hash
nano lib/v2-periphery/contracts/libraries/UniswapV2Library.sol
forge build

# Deploy Phase 2: Router
./scripts/deploy.sh --resume

# Validate deployment
./scripts/post-deploy.sh
```

**Timeline**: 2-3 hours (including testing)

**Detailed Guide**: See `docs/0G_DEX_DEPLOYMENT.md` (26 pages)  
**Quick Start**: See `docs/0G_DEX_QUICKSTART.md` (4 pages)

---

## ⚡ QUICK ACTION PLAN

Choose your path and execute:

### Path A: Research First (Recommended)
```
1. Research canonical DEX (2-4 hrs)
   ├─ Check Discord
   ├─ Search block explorer  
   ├─ Review docs
   └─ Verify contract
   
2. If found → Update config (5 min)
3. If not found → Path B
```

### Path B: Deploy Now (Fallback)
```
1. Install Foundry (15 min)
2. Fund wallet (external)
3. Deploy contracts (60 min)
4. Validate deployment (30 min)
5. Update config (5 min)
```

---

## 📝 Configuration Update Process

Once you have addresses (from either path):

### Step 1: Create `.env.launch`
```bash
cd /home/runner/work/pi-forge-quantum-genesis/pi-forge-quantum-genesis

# Copy template
cp .env.launch.example .env.launch

# Edit with real addresses
nano .env.launch
```

### Step 2: Fill in Addresses
```bash
# Network Configuration
ZERO_G_CHAIN_ID=16661
ZERO_G_RPC_URL=https://evmrpc.0g.ai
ZERO_G_BLOCK_EXPLORER=https://chainscan.0g.ai

# Deployed Contract Addresses
ZERO_G_W0G=0x[YOUR_W0G_ADDRESS]
ZERO_G_FACTORY=0x[YOUR_FACTORY_ADDRESS]
ZERO_G_UNIVERSAL_ROUTER=0x[YOUR_ROUTER_ADDRESS]

# Metadata
ROUTER_SOURCE=canonical  # or "self_deployed"
ROUTER_DEPLOYED_BY=onenoly1010
ROUTER_TYPE=uniswap_v2
ROUTER_DEPLOYMENT_DATE=2025-12-22
```

### Step 3: Verify Configuration
```bash
# Run verification script
export ZERO_G_W0G="0x..."
export ZERO_G_FACTORY="0x..."
export ZERO_G_UNIVERSAL_ROUTER="0x..."
export ZERO_G_RPC_URL="https://evmrpc.0g.ai"

python scripts/verify_0g_dex.py
```

Expected output:
```
✅ W0G Exists: PASSED
✅ Factory Exists: PASSED
✅ Router Exists: PASSED
✅ ALL TESTS PASSED ✅
```

### Step 4: Test Integration
```bash
# Test W0G wrap
cast send $ZERO_G_W0G "deposit()" \
  --value 0.01ether \
  --private-key $PRIVATE_KEY \
  --rpc-url https://evmrpc.0g.ai

# Check balance
cast call $ZERO_G_W0G \
  "balanceOf(address)(uint256)" \
  $YOUR_ADDRESS \
  --rpc-url https://evmrpc.0g.ai
```

---

## ✅ Success Criteria

Once resolved, verify all these are TRUE:

- [ ] DEX router address identified or deployed
- [ ] Address verified on 0G block explorer (https://chainscan.0g.ai)
- [ ] `.env.launch` file exists with real addresses
- [ ] Verification script passes all tests
- [ ] Test wrap/unwrap transaction successful
- [ ] Backend can connect to contracts
- [ ] System ready for flash launch

---

## 🚨 Important Notes

### Security
- ⚠️ Never commit `.env.launch` with real addresses
- ⚠️ Never commit private keys
- ⚠️ Verify all addresses on block explorer
- ⚠️ Test with small amounts first

### Validation
- ✅ All contracts must be verified on Chainscan
- ✅ Router factory() must match Factory address
- ✅ Router WETH() must match W0G address
- ✅ Test transaction must succeed

### Timeline
- **Critical Deadline**: 48 hours from issue creation (Dec 16)
- **Current Status**: 6 days overdue (as of Dec 22)
- **Action Required**: IMMEDIATE

---

## 📚 Resources

### Documentation
- Full Guide: `docs/0G_DEX_DEPLOYMENT.md` (26 pages)
- Quick Start: `docs/0G_DEX_QUICKSTART.md` (4 pages)
- Integration: `contracts/0g-uniswap-v2/INTEGRATION_EXAMPLE.md`
- Checklist: `contracts/0g-uniswap-v2/DEPLOYMENT_CHECKLIST.md`

### External Resources
- 0G Discord: https://discord.gg/0gnetwork
- 0G Docs: https://docs.0g.ai
- Block Explorer: https://chainscan.0g.ai
- GitHub: https://github.com/0glabs

### Deployment Scripts
- Setup: `contracts/0g-uniswap-v2/scripts/setup.sh`
- Deploy: `contracts/0g-uniswap-v2/scripts/deploy.sh`
- Validate: `contracts/0g-uniswap-v2/scripts/post-deploy.sh`
- Verify: `scripts/verify_0g_dex.py`

---

## 🎬 Next Immediate Actions

**For @onenoly1010:**

1. **Choose Path** (5 min)
   - Research first? → Path A
   - Deploy now? → Path B

2. **Execute Path** (2-4 hrs)
   - Follow steps above
   - Document addresses
   - Verify on block explorer

3. **Update Configuration** (15 min)
   - Create `.env.launch`
   - Run verification
   - Test integration

4. **Close Issue** (5 min)
   - Update Issue #108
   - Mark as resolved
   - Proceed to launch!

---

**Status**: ⏳ Awaiting external action (research or deployment)  
**Blocker**: Cannot deploy contracts from sandboxed environment  
**Next**: User must execute one of the paths above  

**Everything else is READY. This is the ONLY blocker! 🚀**
