# ⚡ QUICK ACTION: Resolve 0G DEX Blocker

**🔴 CRITICAL**: OINIO launch blocked by missing `ZERO_G_UNIVERSAL_ROUTER` address

**⏱️ TIME REQUIRED**: 2-4 hours  
**👤 ACTION NEEDED**: @onenoly1010

---

## 🎯 The Problem

```
❌ ZERO_G_UNIVERSAL_ROUTER = <missing>
❌ System cannot execute swaps
❌ Launch blocked
```

## ✅ The Solution

**TWO OPTIONS** - Choose one and execute:

---

## Option A: Find Canonical DEX (2-4 hours)

### Step 1: Research (2 hours)

**Discord** (https://discord.gg/0gnetwork):
```
Channel: #dev or #support
Question: "What is the canonical DEX router address for 
          Aristotle Mainnet (Chain ID 16661)?"
Ping: @0g-team @moderators
```

**Block Explorer** (https://chainscan.0g.ai):
```
Search: "router" OR "swap" OR "dex"
Filter: Verified contracts only
Look for: UniswapV2Router02, PancakeRouter
```

**Documentation** (https://docs.0g.ai):
```
Search: "DeFi" OR "DEX" OR "swap"
Check: Ecosystem page, GitHub repos
```

### Step 2: If Found (30 min)

```bash
# Create .env.launch
cat > .env.launch << 'EOF'
ZERO_G_CHAIN_ID=16661
ZERO_G_RPC_URL=https://evmrpc.0g.ai
ZERO_G_W0G=0x[FROM_CANONICAL_DEX]
ZERO_G_FACTORY=0x[FROM_CANONICAL_DEX]
ZERO_G_UNIVERSAL_ROUTER=0x[FROM_CANONICAL_DEX]
ROUTER_SOURCE=canonical
ROUTER_DEPLOYED_BY=0g_team
ROUTER_TYPE=uniswap_v2
ROUTER_DEPLOYMENT_DATE=2025-12-22
EOF

# Verify
export ZERO_G_UNIVERSAL_ROUTER="0x..."
export ZERO_G_W0G="0x..."
export ZERO_G_FACTORY="0x..."
python scripts/verify_0g_dex.py
```

### Step 3: Test (30 min)

```bash
# Test wrap
cast send $ZERO_G_W0G "deposit()" \
  --value 0.01ether \
  --private-key $PRIVATE_KEY \
  --rpc-url https://evmrpc.0g.ai

# ✅ Done! Launch unblocked!
```

---

## Option B: Deploy Own DEX (2-3 hours)

### Step 1: Install Foundry (15 min)

```bash
# Install
curl -L https://foundry.paradigm.xyz | bash
foundryup

# Verify
forge --version
```

### Step 2: Setup Project (15 min)

```bash
cd /path/to/pi-forge-quantum-genesis
cd contracts/0g-uniswap-v2

# Install dependencies
./scripts/setup.sh

# Configure
cp .env.example .env
nano .env
```

Edit `.env`:
```bash
PRIVATE_KEY=your_private_key_here  # NO 0x prefix
DEPLOYER=0xYourWalletAddress
FEE_TO_SETTER=0xYourWalletAddress
RPC_URL=https://evmrpc.0g.ai
CHAIN_ID=16661
```

**⚠️ CRITICAL**: Wallet needs **0.5+ 0G balance**

### Step 3: Deploy Phase 1 (30 min)

```bash
# Deploy W0G + Factory
./scripts/deploy.sh

# Output will show:
# W0G deployed at: 0x...
# Factory deployed at: 0x...
# PAIR_INIT_CODE_HASH: 0x...

# ✏️ COPY THE PAIR_INIT_CODE_HASH!
```

### Step 4: Update Init Hash (5 min)

```bash
# Open library file
nano lib/v2-periphery/contracts/libraries/UniswapV2Library.sol

# Find line ~26:
# hex'96e8ac4277198ff8b6f785478aa9a39f403cb768dd02cbee326c3e7da348845f'

# Replace with your PAIR_INIT_CODE_HASH:
# hex'YOUR_HASH_FROM_STEP_3_HERE'

# Save and rebuild
forge build
```

### Step 5: Deploy Phase 2 (15 min)

```bash
# Deploy Router
./scripts/deploy.sh --resume

# Output:
# Router02 deployed at: 0x...
```

### Step 6: Create Config (10 min)

```bash
cd /path/to/pi-forge-quantum-genesis

# Create .env.launch
cat > .env.launch << 'EOF'
ZERO_G_CHAIN_ID=16661
ZERO_G_RPC_URL=https://evmrpc.0g.ai
ZERO_G_W0G=0x[FROM_STEP_3]
ZERO_G_FACTORY=0x[FROM_STEP_3]
ZERO_G_UNIVERSAL_ROUTER=0x[FROM_STEP_5]
ROUTER_SOURCE=self_deployed
ROUTER_DEPLOYED_BY=onenoly1010
ROUTER_TYPE=uniswap_v2
ROUTER_DEPLOYMENT_DATE=2025-12-22
EOF

# Fill in actual addresses from deployment logs!
```

### Step 7: Verify (15 min)

```bash
# Validate deployment
cd contracts/0g-uniswap-v2
./scripts/post-deploy.sh

# Verify contracts work
cd ../..
export ZERO_G_W0G="0x..."
export ZERO_G_FACTORY="0x..."
export ZERO_G_UNIVERSAL_ROUTER="0x..."
python scripts/verify_0g_dex.py
```

### Step 8: Test (15 min)

```bash
# Test wrap
cast send $ZERO_G_W0G "deposit()" \
  --value 0.01ether \
  --private-key $PRIVATE_KEY \
  --rpc-url https://evmrpc.0g.ai

# Check balance
cast call $ZERO_G_W0G \
  "balanceOf(address)(uint256)" \
  $YOUR_ADDRESS \
  --rpc-url https://evmrpc.0g.ai

# ✅ Done! Launch unblocked!
```

---

## 🎯 Success Checklist

After completing either option:

- [ ] `.env.launch` file exists
- [ ] All three addresses filled in:
  - [ ] ZERO_G_W0G
  - [ ] ZERO_G_FACTORY  
  - [ ] ZERO_G_UNIVERSAL_ROUTER
- [ ] Addresses verified on https://chainscan.0g.ai
- [ ] Python verification passes: `python scripts/verify_0g_dex.py`
- [ ] Test transaction succeeds
- [ ] Backend can read contracts
- [ ] ✅ **LAUNCH UNBLOCKED!**

---

## 📊 Decision Matrix

```
Need DEX address?
│
├─ Have time to research? (2-4 hrs)
│  └─ YES → Option A (Find canonical)
│
└─ Need to launch ASAP? (2-3 hrs)
   └─ YES → Option B (Deploy own)
```

---

## 🆘 Troubleshooting

### "Cannot connect to RPC"
```bash
# Test RPC
curl -X POST https://evmrpc.0g.ai \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_chainId","params":[],"id":1}'
# Should return: {"jsonrpc":"2.0","id":1,"result":"0x4115"}
```

### "Insufficient balance"
- Need minimum **0.5 0G** in deployer wallet
- Get 0G from exchange or faucet
- Check balance: `cast balance $YOUR_ADDRESS --rpc-url https://evmrpc.0g.ai`

### "Build failed"
```bash
cd contracts/0g-uniswap-v2
forge clean
rm -rf lib cache out
./scripts/setup.sh
```

### "Verification failed"
- Check addresses are correct
- Verify contracts exist on Chainscan
- Ensure RPC URL is correct
- Try again with correct addresses

---

## 📚 Full Documentation

If you need more details:

- **Full Guide**: `docs/0G_DEX_DEPLOYMENT.md` (26 pages)
- **Quick Start**: `docs/0G_DEX_QUICKSTART.md` (4 pages)
- **Deployment Status**: `DEPLOYMENT_STATUS_0G_DEX.md` (this repo)
- **Checklist**: `contracts/0g-uniswap-v2/DEPLOYMENT_CHECKLIST.md`

---

## ⏱️ Timeline Estimate

| Task | Time | Status |
|------|------|--------|
| **Choose option** | 5 min | ⏳ Start here |
| **Research (Option A)** | 2-4 hrs | ⏳ Or skip to B |
| **Deploy (Option B)** | 2-3 hrs | ⏳ Or skip to A |
| **Configure** | 15 min | ⏳ After A or B |
| **Verify** | 15 min | ⏳ Almost done |
| **Test** | 15 min | ⏳ Final check |
| **✅ DONE** | - | 🎉 Launch! |

---

## 🚀 Start Now

**Pick one and GO:**

### Starting Option A (Research)?
1. Open Discord: https://discord.gg/0gnetwork
2. Post question in #dev
3. Search block explorer: https://chainscan.0g.ai
4. Check docs: https://docs.0g.ai

### Starting Option B (Deploy)?
1. Open terminal
2. Run: `curl -L https://foundry.paradigm.xyz | bash`
3. Run: `foundryup`
4. Run: `cd contracts/0g-uniswap-v2 && ./scripts/setup.sh`

---

**Everything is ready. Just need addresses. Let's GO! 🚀**
