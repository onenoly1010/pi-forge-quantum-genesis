# Deployment Scripts - Usage Examples

This document provides real-world usage examples and expected outputs for the deployment scripts.

## Table of Contents
- [Quick Start](#quick-start)
- [Pre-Deployment Checks](#pre-deployment-checks)
- [Deployment Execution](#deployment-execution)
- [Post-Deployment Verification](#post-deployment-verification)
- [Common Workflows](#common-workflows)
- [Troubleshooting Examples](#troubleshooting-examples)

---

## Quick Start

### First-Time Setup

```bash
# 1. Navigate to contracts directory
cd contracts

# 2. Copy environment template
cp .env.template .env

# 3. Edit .env with your configuration
nano .env  # or your preferred editor

# Required minimal configuration:
# PRIVATE_KEY=0x...
# PI_MAINNET_RPC=https://rpc.mainnet.pi.network
# ZERO_G_RPC=https://evmrpc.0g.ai

# 4. Validate configuration
bash scripts/pre-deploy-check.sh
```

### Expected Output (Success):

```
╔═══════════════════════════════════════════════════════════╗
║   PRE-DEPLOYMENT SAFETY CHECKS                            ║
╚═══════════════════════════════════════════════════════════╝

[INFO] Network: mainnet

[INFO] Check 1: Environment Configuration
─────────────────────────────────────
[✓] .env file exists
[✓] PRIVATE_KEY is properly formatted
[✓] Mainnet RPC URLs configured

[INFO] Check 2: Required Tools Installation
─────────────────────────────────────
[✓] Node.js installed: v20.11.0
[✓] npm installed: 10.2.4
[✓] Forge installed: forge 0.2.0
[✓] Cast installed
[✓] Soroban CLI installed: soroban 20.3.0

[INFO] Check 3: Network Connectivity
─────────────────────────────────────
[INFO] Testing Pi Network Mainnet: https://rpc.mainnet.pi.network
[✓] Pi Network Mainnet connected (Chain ID: 314159)
[INFO] Testing 0G Aristotle Mainnet: https://evmrpc.0g.ai
[✓] 0G Aristotle Mainnet connected (Chain ID: 16661)

[INFO] Check 4: Wallet Balances
─────────────────────────────────────
[INFO] Deployer address: 0x1234567890abcdef...
[INFO] Pi Network Mainnet balance: 1.5 ETH
[✓] Balance sufficient (minimum: 0.1 ETH)

[INFO] 0G Aristotle Mainnet balance: 2.0 ETH
[✓] Balance sufficient (minimum: 0.5 ETH)

[INFO] Check 5: Contract Compilation Status
─────────────────────────────────────
[INFO] Checking Hardhat compilation...
[✓] Hardhat artifacts exist
[INFO] Checking Forge compilation...
[✓] Forge artifacts exist
[INFO] Checking Soroban contract build...
[✓] Soroban contract built

[INFO] Check 6: Git Repository Status
─────────────────────────────────────
[INFO] Current branch: main
[✓] Working directory is clean

[INFO] Check 7: Security Checks
─────────────────────────────────────
[✓] .env is in .gitignore
[INFO] Scanning for potential hardcoded secrets...
[✓] No hardcoded private keys detected

╔═══════════════════════════════════════════════════════════╗
║   PRE-DEPLOYMENT CHECK SUMMARY                            ║
╚═══════════════════════════════════════════════════════════╝

[✓] All critical checks passed! ✨

[INFO] You are ready to deploy to mainnet
```

---

## Pre-Deployment Checks

### Check Mainnet Readiness

```bash
npm run deploy:check
# or
cd contracts && bash scripts/pre-deploy-check.sh
```

### Check Testnet Readiness

```bash
npm run deploy:check:testnet
# or
cd contracts && bash scripts/pre-deploy-check.sh --network testnet
```

### Example: Insufficient Balance

```
[INFO] Check 4: Wallet Balances
─────────────────────────────────────
[INFO] Deployer address: 0x1234567890abcdef...
[INFO] Pi Network Mainnet balance: 0.05 ETH
[✗] Insufficient balance (minimum: 0.1 ETH)

╔═══════════════════════════════════════════════════════════╗
║   PRE-DEPLOYMENT CHECK SUMMARY                            ║
╚═══════════════════════════════════════════════════════════╝

[✗] Failed checks: 1

[✗] Please fix the issues above before deploying
```

**Solution:** Fund your wallet before proceeding.

---

## Deployment Execution

### Dry Run (Preview)

```bash
npm run deploy:all:dry-run
# or
cd contracts && bash scripts/deploy-all.sh --dry-run
```

**Expected Output:**

```
╔═══════════════════════════════════════════════════════════╗
║   DEPLOYMENT ORCHESTRATION SCRIPT                         ║
║   Multi-Chain, Multi-Tool Deployment System               ║
╚═══════════════════════════════════════════════════════════╝

[INFO] Deployment Configuration:
  Target: all
  Network: mainnet
  Skip Checks: false
  Dry Run: true

[INFO] Starting deployment process...

[INFO] Deploying ALL contracts to specified networks...

[INFO] Deploying iNFT contracts to Pi Network (mainnet)...
[INFO] [DRY RUN] Would deploy OINIO Token and Model Registry to Pi Network

[INFO] Deploying iNFT contracts to 0G Network...
[INFO] [DRY RUN] Would deploy OINIO Token and Model Registry to 0G

[INFO] Deploying DEX contracts to 0G Network...
[INFO] [DRY RUN] Would deploy W0G, Factory, and Router to 0G

[INFO] Deploying Memorial Bridge to Pi Network via Soroban...
[INFO] [DRY RUN] Would deploy Memorial contract via Soroban

╔═══════════════════════════════════════════════════════════╗
║   DEPLOYMENT COMPLETE                                     ║
╚═══════════════════════════════════════════════════════════╝

[INFO] This was a dry run. No actual deployments were made.
```

### Full Deployment (Mainnet)

```bash
npm run deploy:all
# or
cd contracts && bash scripts/deploy-all.sh
```

### Testnet Deployment

```bash
npm run deploy:all:testnet
# or
cd contracts && bash scripts/deploy-all.sh --network testnet
```

### Targeted Deployments

**iNFT Contracts Only:**
```bash
npm run deploy:inft
# or
cd contracts && bash scripts/deploy-all.sh --target inft
```

**DEX Contracts Only:**
```bash
npm run deploy:dex
# or
cd contracts && bash scripts/deploy-all.sh --target dex
```

**Memorial Contract Only:**
```bash
npm run deploy:memorial
# or
cd contracts && bash scripts/deploy-all.sh --target memorial
```

---

## Post-Deployment Verification

### Health Check (Mainnet)

```bash
npm run deploy:health
# or
cd contracts && bash scripts/post-deploy-check.sh
```

**Expected Output (Success):**

```
╔═══════════════════════════════════════════════════════════╗
║   POST-DEPLOYMENT HEALTH CHECK                            ║
╚═══════════════════════════════════════════════════════════╝

[INFO] Network: mainnet

═══════════════════════════════════════════════════════════
CHECKING DEPLOYED CONTRACTS
═══════════════════════════════════════════════════════════

─────────────────────────────────────────────────────────────
OINIO Token Contract
─────────────────────────────────────────────────────────────

[INFO] Checking OINIO Token at 0x1234567890abcdef...
[✓] OINIO Token: Deployed (code size: 12543 bytes)
[CONTRACT] Address: 0x1234567890abcdef...
[CONTRACT] Network: Pi Network mainnet
[CONTRACT] Name: OINIO
[CONTRACT] Symbol: OINIO
[CONTRACT] Decimals: 18
[CONTRACT] Total Supply: 1000000000.00 OINIO
[✓] OINIO Token: HEALTHY ✨

─────────────────────────────────────────────────────────────
OINIO Model Registry Contract
─────────────────────────────────────────────────────────────

[INFO] Checking OINIO Registry at 0xabcdef1234567890...
[✓] OINIO Registry: Deployed (code size: 15234 bytes)
[CONTRACT] Address: 0xabcdef1234567890...
[CONTRACT] Network: Pi Network mainnet
[CONTRACT] Name: OINIO Model Registry
[CONTRACT] Symbol: OINIOREG
[✓] OINIO Registry: HEALTHY ✨

─────────────────────────────────────────────────────────────
DEX Contracts (0G Network)
─────────────────────────────────────────────────────────────

[INFO] Checking W0G (Wrapped 0G) at 0xfedcba0987654321...
[✓] W0G (Wrapped 0G): Deployed (code size: 8912 bytes)
[CONTRACT] Address: 0xfedcba0987654321...
[CONTRACT] Network: 0G Aristotle Mainnet
[CONTRACT] Name: Wrapped 0G
[CONTRACT] Symbol: W0G
[✓] W0G: HEALTHY ✨

[INFO] Checking UniswapV2Factory at 0x0987654321fedcba...
[✓] UniswapV2Factory: Deployed (code size: 15234 bytes)
[CONTRACT] Address: 0x0987654321fedcba...
[CONTRACT] Network: 0G Aristotle Mainnet
[CONTRACT] Fee Recipient: 0x...
[✓] UniswapV2Factory: HEALTHY ✨

[INFO] Checking UniswapV2Router02 at 0x5678901234abcdef...
[✓] UniswapV2Router02: Deployed (code size: 18765 bytes)
[CONTRACT] Address: 0x5678901234abcdef...
[CONTRACT] Network: 0G Aristotle Mainnet
[CONTRACT] Factory: 0x0987654321fedcba...
[CONTRACT] WETH: 0xfedcba0987654321...
[✓] UniswapV2Router02: HEALTHY ✨

─────────────────────────────────────────────────────────────
Soroban Contracts (Pi Network)
─────────────────────────────────────────────────────────────

[CONTRACT] Memorial Bridge Contract ID: CDXXXXX...
[INFO] Verifying Soroban contract...
[✓] Memorial Bridge: DEPLOYED ✨

═══════════════════════════════════════════════════════════
BASIC INTEGRATION TESTS
═══════════════════════════════════════════════════════════

[INFO] Testing OINIO Token transfer simulation...
[✓] Token balanceOf function works

[INFO] Generating health report...
[✓] Health report saved to deployments/health_check_mainnet_20260206_102030.txt

╔═══════════════════════════════════════════════════════════╗
║   HEALTH CHECK SUMMARY                                    ║
╚═══════════════════════════════════════════════════════════╝

[✓] All contracts are healthy! ✨

[INFO] Next steps:
  1. Update frontend with contract addresses
  2. Test contract interactions
  3. Monitor events and logs
  4. Set up alerting for critical functions
```

---

## Common Workflows

### Workflow 1: Complete Mainnet Deployment

```bash
# Step 1: Setup
cd /path/to/pi-forge-quantum-genesis
cd contracts
cp .env.template .env
# Edit .env with your private key and configuration

# Step 2: Pre-flight checks
npm run deploy:check

# Expected: All checks pass ✅

# Step 3: Deploy all contracts
npm run deploy:all

# Expected: 
# - iNFT contracts deployed to Pi Network
# - iNFT contracts deployed to 0G Network
# - DEX contracts deployed to 0G Network
# - Memorial contract deployed to Pi Network

# Step 4: Verify deployment
npm run deploy:health

# Expected: All contracts healthy ✅

# Step 5: Update .env with addresses
# Copy contract addresses from deployment output to .env

# Step 6: Verify on block explorers
# Pi Network: https://pi.blockscout.com/
# 0G Network: https://scan.0g.ai/
```

### Workflow 2: Testnet Testing

```bash
# Step 1: Configure testnet
cd contracts
# Edit .env to ensure testnet RPCs are set

# Step 2: Check testnet readiness
npm run deploy:check:testnet

# Step 3: Deploy to testnet
npm run deploy:all:testnet

# Step 4: Verify testnet deployment
npm run deploy:health:testnet

# Step 5: Test interactions
# Use testnet addresses to test frontend integration
```

### Workflow 3: Iterative Development

```bash
# Deploy only iNFT contracts for testing
npm run deploy:inft:testnet

# Make changes to contracts...

# Redeploy
npm run deploy:inft:testnet

# Verify
npm run deploy:health:testnet
```

### Workflow 4: Production Deployment with Safety

```bash
# Always start with a dry run
npm run deploy:all:dry-run

# Review the deployment plan

# Run actual deployment
npm run deploy:check
npm run deploy:all
npm run deploy:health

# Save deployment artifacts
git add contracts/deployments/*.txt
git commit -m "chore: Save deployment artifacts"
```

---

## Troubleshooting Examples

### Problem: Missing Private Key

**Error:**
```
[ERROR] PRIVATE_KEY not set in .env
```

**Solution:**
```bash
# Add to .env
PRIVATE_KEY=0x1234567890abcdef...

# Re-run checks
npm run deploy:check
```

### Problem: Network Connectivity

**Error:**
```
[✗] Pi Network Mainnet connection failed
```

**Solution:**
```bash
# Test RPC manually
curl -X POST https://rpc.mainnet.pi.network \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_chainId","params":[],"id":1}'

# Try alternative RPC or check firewall
```

### Problem: Insufficient Balance

**Error:**
```
[✗] Insufficient balance (minimum: 0.5 ETH)
```

**Solution:**
```bash
# Check current balance
cast balance YOUR_ADDRESS --rpc-url https://evmrpc.0g.ai

# Fund wallet via:
# - Testnet faucet
# - Transfer from another wallet
# - Purchase from exchange
```

### Problem: Contract Not Compiling

**Error:**
```
[!] Hardhat contracts not compiled
```

**Solution:**
```bash
cd contracts/hardhat
npm install
npm run compile

# Verify
ls -la artifacts/
```

### Problem: Security Warning

**Error:**
```
[✗] .env is NOT in .gitignore - SECURITY RISK!
```

**Solution:**
```bash
# Add to .gitignore
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore

# Verify
git status  # .env should not appear
```

---

## Script Output Locations

### Deployment Logs

All deployment logs are saved to `contracts/deployments/`:

- `deployment_mainnet_YYYYMMDD_HHMMSS.txt` - Main deployment summary
- `health_check_mainnet_YYYYMMDD_HHMMSS.txt` - Health check report

### Hardhat Deployment Records

Hardhat saves detailed deployment info to `contracts/hardhat/deployments/`:

- `OINIOToken-314159.json` - Pi Network mainnet
- `OINIOToken-16661.json` - 0G Network mainnet
- `OINIOModelRegistry-314159.json`
- `OINIOModelRegistry-16661.json`

### Soroban Contract Address

Saved to `contracts/oinio-memorial-bridge/contract_address.txt`

---

## Next Steps After Successful Deployment

1. **Update Frontend Configuration**
   ```bash
   # Copy addresses to frontend .env
   NEXT_PUBLIC_OINIO_TOKEN_ADDRESS=0x...
   NEXT_PUBLIC_OINIO_REGISTRY_ADDRESS=0x...
   NEXT_PUBLIC_ZERO_G_W0G=0x...
   NEXT_PUBLIC_ZERO_G_FACTORY=0x...
   NEXT_PUBLIC_ZERO_G_ROUTER=0x...
   ```

2. **Verify on Block Explorers**
   - Pi Network: https://pi.blockscout.com/
   - 0G Network: https://scan.0g.ai/

3. **Test Contract Interactions**
   ```bash
   # Test token transfer
   cast send $OINIO_TOKEN_ADDRESS \
     "transfer(address,uint256)" \
     $RECIPIENT 1000000000000000000 \
     --private-key $PRIVATE_KEY \
     --rpc-url $PI_MAINNET_RPC
   ```

4. **Set Up Monitoring**
   - Monitor contract events
   - Set up alerts for critical functions
   - Track gas usage and transaction costs

5. **Document Deployment**
   - Save contract addresses
   - Document any deployment issues
   - Update team documentation

---

## Support

For issues or questions:
- **GitHub Issues:** https://github.com/onenoly1010/pi-forge-quantum-genesis/issues
- **Documentation:** See [DEPLOYMENT_GUIDE.md](../DEPLOYMENT_GUIDE.md)
- **Scripts Reference:** See [scripts/README.md](README.md)
