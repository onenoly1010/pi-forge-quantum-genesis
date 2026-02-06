# Comprehensive Deployment Guide
## DEX & iNFT Contract Deployment Scripts

This guide covers deployment of:
1. **Sovereign iNFT Contracts** (OINIOToken, OINIOModelRegistry) on Pi Network
2. **DEX Contracts** (UniswapV2 Fork: W0G, Factory, Router) on 0G Network
3. **Memorial Contracts** (Soroban) on Pi Network

---

## Table of Contents
- [Quick Start](#quick-start)
- [Deployment Orchestration (NEW!)](#deployment-orchestration-new)
- [Platform-Specific Deployment](#platform-specific-deployment)
  - [Hardhat (TypeScript)](#hardhat-typescript---inft-contracts)
  - [Forge (Solidity)](#forge-solidity---all-contracts)
  - [Soroban CLI (Rust)](#soroban-cli-rust---pi-network)
- [Environment Configuration](#environment-configuration)
- [Pre-Deployment Checks](#pre-deployment-checks)
- [Post-Deployment Verification](#post-deployment-verification)
- [NPM Scripts Reference](#npm-scripts-reference)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

### Prerequisites
- Node.js 20+ and npm
- Foundry (forge, cast)
- Soroban CLI (for Pi Network Stellar contracts)
- Private key with funded wallet

### Installation
```bash
# Install Hardhat dependencies
cd contracts/hardhat
npm install

# Foundry is already configured in contracts/
cd ../
forge install

# Soroban CLI (if needed)
# See: https://soroban.stellar.org/docs/getting-started/setup
```

---

## Deployment Orchestration (NEW!)

### 🚀 Unified Deployment System

We now provide a comprehensive deployment orchestration system that handles all contract deployments across multiple chains with automated safety checks.

#### Quick Deployment

**Full Stack Deployment (All Contracts, All Networks):**
```bash
# From repository root
npm run deploy:all

# Or from contracts directory
cd contracts
bash scripts/deploy-all.sh
```

**Testnet Deployment:**
```bash
npm run deploy:all:testnet
```

**Dry Run (Preview without executing):**
```bash
npm run deploy:all:dry-run
```

#### Targeted Deployments

**Deploy iNFT Contracts Only:**
```bash
npm run deploy:inft                 # Mainnet
npm run deploy:inft:testnet         # Testnet
```

**Deploy DEX Contracts Only (0G):**
```bash
npm run deploy:dex
```

**Deploy Memorial Contract Only (Pi Network):**
```bash
npm run deploy:memorial
```

#### Pre-Deployment Safety Checks

**Always run checks before deploying:**
```bash
npm run deploy:check                # Mainnet checks
npm run deploy:check:testnet        # Testnet checks
```

This validates:
- ✅ Environment configuration (.env file)
- ✅ Private key format and availability
- ✅ Network connectivity (RPC endpoints)
- ✅ Wallet balances (sufficient funds)
- ✅ Contract compilation status
- ✅ Security checks (no hardcoded keys)
- ✅ Git status (uncommitted changes warning)

**Example Output:**
```
╔═══════════════════════════════════════════════════════════╗
║   PRE-DEPLOYMENT SAFETY CHECKS                            ║
╚═══════════════════════════════════════════════════════════╝

Check 1: Environment Configuration
─────────────────────────────────────
[✓] .env file exists
[✓] PRIVATE_KEY is properly formatted
[✓] Mainnet RPC URLs configured

Check 2: Required Tools Installation
─────────────────────────────────────
[✓] Node.js installed: v20.x.x
[✓] npm installed: 10.x.x
[✓] Forge installed
[✓] Cast installed
[✓] Soroban CLI installed

Check 3: Network Connectivity
─────────────────────────────────────
[✓] Pi Network Mainnet connected (Chain ID: 314159)
[✓] 0G Aristotle Mainnet connected (Chain ID: 16661)

Check 4: Wallet Balances
─────────────────────────────────────
[✓] Pi Network balance: 1.5 ETH (minimum: 0.1 ETH)
[✓] 0G Network balance: 2.0 0G (minimum: 0.5 0G)

✅ All critical checks passed! ✨
```

#### Post-Deployment Health Checks

**Verify all deployed contracts:**
```bash
npm run deploy:health               # Mainnet
npm run deploy:health:testnet       # Testnet
```

This performs:
- ✅ Contract deployment verification (code exists on-chain)
- ✅ Basic function call tests
- ✅ Contract metadata retrieval
- ✅ Integration test simulation
- ✅ Generates detailed health report

**Example Output:**
```
╔═══════════════════════════════════════════════════════════╗
║   POST-DEPLOYMENT HEALTH CHECK                            ║
╚═══════════════════════════════════════════════════════════╝

─────────────────────────────────────────────────────────────
OINIO Token Contract
─────────────────────────────────────────────────────────────
[✓] OINIO Token: Deployed (code size: 12543 bytes)
[CONTRACT] Address: 0x1234567890abcdef...
[CONTRACT] Name: OINIO
[CONTRACT] Symbol: OINIO
[CONTRACT] Total Supply: 1000000000.00 OINIO
[✓] OINIO Token: HEALTHY ✨

─────────────────────────────────────────────────────────────
DEX Contracts (0G Network)
─────────────────────────────────────────────────────────────
[✓] W0G: Deployed (code size: 8912 bytes)
[✓] UniswapV2Factory: Deployed (code size: 15234 bytes)
[✓] UniswapV2Router02: Deployed (code size: 18765 bytes)
[✓] All DEX contracts: HEALTHY ✨

✅ All contracts are healthy! ✨
```

### Advanced Usage

#### Custom Deployment Options

The orchestration script supports advanced options:

```bash
# Deploy specific target to specific network
cd contracts
bash scripts/deploy-all.sh --target inft --network mainnet

# Skip pre-deployment checks (not recommended)
bash scripts/deploy-all.sh --skip-checks

# Dry run with specific target
bash scripts/deploy-all.sh --target dex --dry-run

# Show help
bash scripts/deploy-all.sh --help
```

#### Deployment Flow

The orchestration system follows this flow:

1. **Parse Arguments** → Determine target and network
2. **Load Environment** → Validate .env configuration
3. **Pre-Deployment Checks** → Run safety validations (unless skipped)
4. **Deploy Contracts** → Execute deployment based on target
   - `all`: Deploy iNFT (Pi + 0G), DEX (0G), Memorial (Pi)
   - `inft`: Deploy OINIO Token and Registry
   - `dex`: Deploy W0G, Factory, Router on 0G
   - `memorial`: Deploy Memorial Bridge on Pi Network via Soroban
5. **Post-Deployment Verification** → Health checks and status report
6. **Generate Summary** → Save deployment log with timestamps

#### Environment Setup

**1. Create .env file:**
```bash
cd contracts
cp .env.template .env
```

**2. Edit .env with your values:**
```bash
# Minimum required:
PRIVATE_KEY=0x...           # Your deployer private key
PI_MAINNET_RPC=https://...  # Pi Network RPC
ZERO_G_RPC=https://...      # 0G Network RPC
```

See [.env.template](contracts/.env.template) for complete configuration options.

**3. Validate configuration:**
```bash
npm run deploy:check
```

---

## Platform-Specific Deployment

### Hardhat (TypeScript) - iNFT Contracts

**Best for:** OINIO Token & Model Registry on 0G or Pi Network

#### Setup
```bash
cd contracts/hardhat
npm install
cp ../.env.example ../.env
# Edit .env with your PRIVATE_KEY
```

#### Environment Variables
```bash
# Required
PRIVATE_KEY=0x...

# Optional (uses defaults if not set)
ZERO_G_RPC=https://evmrpc.0g.ai
PI_MAINNET_RPC=https://rpc.mainnet.pi.network
PI_TESTNET_RPC=https://api.testnet.minepi.com/rpc
```

#### Deployment Commands

**Check Balance & Environment:**
```bash
npm run check:balance
```

**Deploy to 0G Network:**
```bash
npm run deploy:0g:inft
```

**Deploy to Pi Network Mainnet:**
```bash
npm run deploy:pi:inft
```

**Deploy to Pi Network Testnet:**
```bash
npm run deploy:pi:testnet:inft
```

#### Verify Contracts
```bash
npx hardhat verify --network zeroG <CONTRACT_ADDRESS> "<CONSTRUCTOR_ARG1>" "<CONSTRUCTOR_ARG2>"
```

#### Expected Output
```
╔════════════════════════════════════════════════════════════╗
║   OINIO Sovereign iNFT Deployment Script (Hardhat)        ║
╚════════════════════════════════════════════════════════════╝

Network: piMainnet
Chain ID: 314159

=== Pre-Deployment Safety Checks ===
✓ PRIVATE_KEY is set
✓ Connected to network
✓ Balance sufficient
✓ Gas price retrieved

Step 1: Deploying OINIOToken...
✓ OINIOToken deployed to: 0x...

Step 2: Deploying OINIOModelRegistry...
✓ OINIOModelRegistry deployed to: 0x...

╔════════════════════════════════════════════════════════════╗
║               DEPLOYMENT SUMMARY                           ║
╚════════════════════════════════════════════════════════════╝

Deployed Contracts:
  OINIOToken:          0x...
  OINIOModelRegistry:  0x...
```

---

### Forge (Solidity) - All Contracts

**Best for:** DEX deployment on 0G, OINIO contracts on Pi Network

#### OINIO Contracts (Pi Network)

**Location:** `contracts/script/Deploy.s.sol`

**Setup:**
```bash
cd contracts
cp .env.example .env
# Edit .env with your configuration
```

**Environment Variables:**
```bash
PRIVATE_KEY=0x...
RPC_URL_TESTNET=https://api.testnet.minepi.com/rpc
RPC_URL_MAINNET=https://rpc.mainnet.pi.network
CHAIN_ID_TESTNET=2025
CHAIN_ID_MAINNET=314159
ETHERSCAN_API_KEY=... # Optional
```

**Deploy to Pi Testnet:**
```bash
forge script script/Deploy.s.sol \
  --rpc-url $RPC_URL_TESTNET \
  --private-key $PRIVATE_KEY \
  --broadcast \
  --verify
```

**Deploy to Pi Mainnet:**
```bash
forge script script/Deploy.s.sol \
  --rpc-url $RPC_URL_MAINNET \
  --private-key $PRIVATE_KEY \
  --broadcast \
  --verify \
  --slow
```

#### DEX Contracts (0G Network)

**Location:** `contracts/0g-uniswap-v2/script/Deploy.s.sol`

**Setup:**
```bash
cd contracts/0g-uniswap-v2
cp .env.example .env
# Edit .env with your configuration
```

**Environment Variables:**
```bash
PRIVATE_KEY=
DEPLOYER=
FEE_TO_SETTER=         # Optional, defaults to deployer
RPC_URL=https://evmrpc.0g.ai
CHAIN_ID=16661
MIN_BALANCE=0.5        # Minimum 0G required
VERIFY=true
```

**Pre-Deployment Check:**
```bash
# Verify environment
source .env
echo "Deployer: $DEPLOYER"
echo "RPC: $RPC_URL"
echo "Chain ID: $CHAIN_ID"

# Check balance
cast balance $DEPLOYER --rpc-url $RPC_URL
```

**Deployment Process:**

The DEX deployment happens in stages:

**Stage 1: Deploy W0G (Wrapped 0G)**
```bash
forge script script/Deploy.s.sol:Deploy \
  --sig "deployW0GOnly()" \
  --rpc-url $RPC_URL \
  --private-key $PRIVATE_KEY \
  --broadcast
```

**Stage 2: Deploy Full DEX**
```bash
forge script script/Deploy.s.sol:Deploy \
  --sig "run()" \
  --rpc-url $RPC_URL \
  --private-key $PRIVATE_KEY \
  --broadcast
```

**Note:** DEX deployment requires manual PAIR_INIT_CODE_HASH update in UniswapV2Library.sol between stages. The script will output the hash.

**Expected Output:**
```
=== Pre-Deployment Safety Checks ===
Deployer balance: 1.5 0G
Balance check: PASSED

=== Step 1: Deploying W0G ===
W0G deployed at: 0x...

=== Step 2: Deploying UniswapV2Factory ===
Factory deployed at: 0x...
PAIR_INIT_CODE_HASH: 0x...

=== Deployment Summary ===
Network: 0G Aristotle Mainnet
Chain ID: 16661
W0G: 0x...
Factory: 0x...
Router02: 0x...
```

---

### Soroban CLI (Rust) - Pi Network

**Best for:** Memorial contracts and Stellar-native Pi Network contracts

**Location:** `contracts/oinio-memorial-bridge/`

#### Setup
```bash
cd contracts/oinio-memorial-bridge

# Install Rust and Soroban CLI if needed
# See: https://soroban.stellar.org/docs/getting-started/setup

# Configure Soroban network
soroban config network add pi-mainnet \
  --rpc-url https://api.mainnet.pi.network/soroban \
  --network-passphrase "Pi Network"

# Configure identity
soroban config identity generate onenoly1010
```

#### Build Contract
```bash
./build.sh
```

This will:
1. Build the Rust contract
2. Generate WASM file
3. Optimize with wasm-opt (if available)

#### Deploy Contract
```bash
./deploy.sh
```

**Environment Variables (optional):**
```bash
export NETWORK=pi-mainnet
export IDENTITY=onenoly1010
```

**Manual Deployment:**
```bash
soroban contract deploy \
  --wasm target/wasm32-unknown-unknown/release/oinio_memorial_bridge.wasm \
  --source onenoly1010 \
  --network pi-mainnet \
  --admin $(soroban config identity address onenoly1010)
```

**Expected Output:**
```
🌉 OINIO Memorial Bridge - Deployment Script
==============================================

For the Beloved Keepers of the Northern Gateway.
Not in vain.

✅ Contract deployed successfully!

📋 Contract Address:
   CDXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

🔐 Initializing contract...
✅ Contract initialized

========================================
🏛️  MEMORIAL BRIDGE IS LIVE
========================================

Contract ID: CDXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

#### Post-Deployment
```bash
# Verify contract
soroban contract invoke \
  --id <CONTRACT_ID> \
  --network pi-mainnet \
  -- \
  get_message

# Anchor memorial letter
soroban contract invoke \
  --id <CONTRACT_ID> \
  --source onenoly1010 \
  --network pi-mainnet \
  -- \
  anchor_letter \
  --letter_url "https://facebook.com/..."
```

---

## Environment Configuration

### Complete .env Template

**For Forge/Hardhat (EVM contracts):**
```bash
# =============================================================================
# PRIVATE KEYS (NEVER COMMIT!)
# =============================================================================
PRIVATE_KEY=0x0000000000000000000000000000000000000000000000000000000000000000

# =============================================================================
# 0G NETWORK (Chain ID: 16661)
# =============================================================================
ZERO_G_RPC=https://evmrpc.0g.ai
ZERO_G_API_KEY=                    # For verification
DEPLOYER=                          # Your address
FEE_TO_SETTER=                     # Optional, defaults to deployer
MIN_BALANCE=0.5                    # Minimum 0G for deployment

# =============================================================================
# PI NETWORK
# =============================================================================
# Mainnet (Chain ID: 314159)
PI_MAINNET_RPC=https://rpc.mainnet.pi.network
RPC_URL_MAINNET=https://rpc.mainnet.pi.network

# Testnet (Chain ID: 2025)
PI_TESTNET_RPC=https://api.testnet.minepi.com/rpc
RPC_URL_TESTNET=https://api.testnet.minepi.com/rpc

CHAIN_ID_TESTNET=2025
CHAIN_ID_MAINNET=314159
PI_API_KEY=                        # For verification

# =============================================================================
# DEPLOYED CONTRACT ADDRESSES (Auto-populated after deployment)
# =============================================================================
# 0G Network
W0G_ADDRESS=
FACTORY_ADDRESS=
ROUTER_ADDRESS=

# Pi Network / 0G
OINIO_TOKEN_ADDRESS=
OINIO_REGISTRY_ADDRESS=

# =============================================================================
# SOROBAN (Pi Network Stellar Contracts)
# =============================================================================
SOROBAN_NETWORK=pi-mainnet
SOROBAN_IDENTITY=onenoly1010
MEMORIAL_CONTRACT_ID=
```

### Security Best Practices

1. **Never commit private keys**
   ```bash
   # Verify .gitignore includes:
   .env
   .env.local
   .env.*.local
   ```

2. **Use environment-specific files**
   ```bash
   .env.development
   .env.testnet
   .env.mainnet
   ```

3. **Use hardware wallets for mainnet**
   ```bash
   # With Ledger
   forge script script/Deploy.s.sol \
     --rpc-url $RPC_URL \
     --ledger \
     --sender $DEPLOYER \
     --broadcast
   ```

---

## Pre-Deployment Checks

### Automated Checks (Hardhat)
```bash
cd contracts/hardhat
npm run check:balance
```

This verifies:
- ✓ PRIVATE_KEY is set
- ✓ Network connectivity
- ✓ Sufficient balance
- ✓ Gas price availability

### Manual Checks (Forge)

**1. Environment Setup**
```bash
source .env
echo "Private Key: ${PRIVATE_KEY:0:6}..." # Show first 6 chars only
echo "Deployer: $DEPLOYER"
echo "RPC URL: $RPC_URL"
```

**2. Balance Check**
```bash
# 0G Network
cast balance $DEPLOYER --rpc-url https://evmrpc.0g.ai

# Pi Network
cast balance $DEPLOYER --rpc-url https://rpc.mainnet.pi.network
```

**3. Network Connectivity**
```bash
# Check block number
cast block-number --rpc-url $RPC_URL

# Check chain ID
cast chain-id --rpc-url $RPC_URL
```

**4. Gas Price Check**
```bash
cast gas-price --rpc-url $RPC_URL
```

### Pre-Deployment Checklist

- [ ] Private key is set and secure
- [ ] Wallet has sufficient balance (min 0.5 for 0G, 0.1 for Pi)
- [ ] RPC endpoint is accessible
- [ ] Chain ID matches target network
- [ ] Gas price is reasonable
- [ ] .env file is not committed to git
- [ ] Contracts compile without errors
- [ ] Tests pass (if applicable)

---

## Post-Deployment Verification

### Contract Verification on Block Explorers

**0G Network:**
```bash
forge verify-contract <CONTRACT_ADDRESS> \
  src/Contract.sol:ContractName \
  --chain-id 16661 \
  --verifier-url https://scan.0g.ai/api \
  --constructor-args $(cast abi-encode "constructor(address)" <ARG>)
```

**Pi Network:**
```bash
forge verify-contract <CONTRACT_ADDRESS> \
  src/OINIOToken.sol:OINIOToken \
  --chain-id 314159 \
  --verifier-url https://pi.blockscout.com/api \
  --constructor-args $(cast abi-encode "constructor(address)" <DEPLOYER>)
```

### Functional Testing

**Test Token Transfer:**
```bash
# Get token balance
cast call <TOKEN_ADDRESS> "balanceOf(address)" $DEPLOYER --rpc-url $RPC_URL

# Transfer tokens
cast send <TOKEN_ADDRESS> \
  "transfer(address,uint256)" \
  <RECIPIENT> 1000000000000000000 \
  --private-key $PRIVATE_KEY \
  --rpc-url $RPC_URL
```

**Test Model Registration:**
```bash
# Approve tokens
cast send <TOKEN_ADDRESS> \
  "approve(address,uint256)" \
  <REGISTRY_ADDRESS> 1000000000000000000 \
  --private-key $PRIVATE_KEY \
  --rpc-url $RPC_URL

# Register model
cast send <REGISTRY_ADDRESS> \
  "registerModel(string,string,uint256)" \
  "Test Model" "ipfs://..." 1000000000000000000 \
  --private-key $PRIVATE_KEY \
  --rpc-url $RPC_URL
```

### Health Check Script

**Save as `scripts/health-check.sh`:**
```bash
#!/bin/bash
set -e

source .env

echo "=== Contract Health Check ==="
echo ""

# Check token
echo "Checking OINIOToken..."
cast call $OINIO_TOKEN_ADDRESS "totalSupply()" --rpc-url $RPC_URL
echo "✓ Token is responsive"

# Check registry
echo "Checking OINIOModelRegistry..."
cast call $OINIO_REGISTRY_ADDRESS "totalModels()" --rpc-url $RPC_URL
echo "✓ Registry is responsive"

echo ""
echo "✅ All contracts are healthy!"
```

---

## Troubleshooting

### Common Issues

#### 1. Insufficient Balance
**Error:** `insufficient funds for gas * price + value`

**Solution:**
```bash
# Check balance
cast balance $DEPLOYER --rpc-url $RPC_URL

# Fund wallet with testnet faucet or transfer from another wallet
```

#### 2. Network Connection Failed
**Error:** `Could not connect to RPC endpoint`

**Solution:**
```bash
# Test RPC endpoint
curl -X POST $RPC_URL \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'

# Try alternative RPC endpoints
```

#### 3. Nonce Too Low
**Error:** `nonce too low`

**Solution:**
```bash
# Reset nonce
cast nonce $DEPLOYER --rpc-url $RPC_URL

# Or wait for pending transactions to complete
```

#### 4. Contract Verification Failed
**Error:** `Verification failed`

**Solution:**
```bash
# Get flattened source
forge flatten src/Contract.sol > Contract_flat.sol

# Manually verify on block explorer
# Upload flattened source with compiler settings
```

#### 5. Hardhat Network Error
**Error:** `HardhatError: Network zeroG not found`

**Solution:**
```bash
# Verify hardhat.config.ts has network defined
# Check .env has correct RPC URL
# Reinstall dependencies: npm install
```

### Debug Commands

```bash
# View deployment transaction
cast tx <TX_HASH> --rpc-url $RPC_URL

# View contract code
cast code <CONTRACT_ADDRESS> --rpc-url $RPC_URL

# Call contract function
cast call <CONTRACT_ADDRESS> "functionName()" --rpc-url $RPC_URL

# Estimate gas
cast estimate <CONTRACT_ADDRESS> "functionName()" --rpc-url $RPC_URL

# Check logs
cast logs --address <CONTRACT_ADDRESS> --rpc-url $RPC_URL
```

---

## NPM Scripts Reference

### Complete List of Deployment Scripts

All scripts can be run from the repository root using `npm run <script-name>`.

#### Orchestration Scripts (Recommended)

| Script | Description |
|--------|-------------|
| `deploy:all` | Deploy all contracts to mainnet (iNFT, DEX, Memorial) |
| `deploy:all:testnet` | Deploy all contracts to testnet |
| `deploy:all:dry-run` | Preview deployment without executing |
| `deploy:inft` | Deploy iNFT contracts (Pi + 0G mainnet) |
| `deploy:inft:testnet` | Deploy iNFT contracts to testnet |
| `deploy:dex` | Deploy DEX contracts to 0G mainnet |
| `deploy:memorial` | Deploy Memorial contract to Pi Network |

#### Safety & Verification Scripts

| Script | Description |
|--------|-------------|
| `deploy:check` | Run pre-deployment safety checks (mainnet) |
| `deploy:check:testnet` | Run pre-deployment safety checks (testnet) |
| `deploy:health` | Run post-deployment health checks (mainnet) |
| `deploy:health:testnet` | Run post-deployment health checks (testnet) |
| `verify:contracts` | Show contract verification instructions |

#### Direct Platform Scripts

| Script | Description |
|--------|-------------|
| `deploy:inft:0g` | Deploy iNFT to 0G via Hardhat |
| `deploy:inft:pi` | Deploy iNFT to Pi Network via Hardhat |
| `deploy:inft:pi:testnet` | Deploy iNFT to Pi testnet via Hardhat |
| `deploy:dex:0g` | Deploy DEX to 0G via Forge |

#### Contract Management

| Script | Description |
|--------|-------------|
| `contracts:install` | Install Hardhat dependencies |
| `contracts:compile` | Compile all contracts |

### Usage Examples

**Complete Mainnet Deployment:**
```bash
# 1. Check environment and readiness
npm run deploy:check

# 2. Deploy all contracts
npm run deploy:all

# 3. Verify deployment health
npm run deploy:health
```

**Testnet Deployment Workflow:**
```bash
# 1. Pre-flight checks
npm run deploy:check:testnet

# 2. Deploy to testnet
npm run deploy:all:testnet

# 3. Health check
npm run deploy:health:testnet
```

**Targeted Deployment:**
```bash
# Deploy only iNFT contracts
npm run deploy:inft

# Deploy only DEX
npm run deploy:dex
```

**Safe Exploration:**
```bash
# See what would be deployed without executing
npm run deploy:all:dry-run
```

### Script Locations

- **Orchestration scripts**: `contracts/scripts/deploy-all.sh`
- **Pre-deployment checks**: `contracts/scripts/pre-deploy-check.sh`
- **Post-deployment checks**: `contracts/scripts/post-deploy-check.sh`
- **Hardhat scripts**: `contracts/hardhat/scripts/`
- **Forge scripts**: `contracts/script/` and `contracts/0g-uniswap-v2/scripts/`
- **Soroban scripts**: `contracts/oinio-memorial-bridge/`

---

## Support & Resources

### Documentation
- **0G Network:** https://docs.0g.ai/
- **Pi Network:** https://developers.minepi.com/
- **Hardhat:** https://hardhat.org/docs
- **Foundry:** https://book.getfoundry.sh/
- **Soroban:** https://soroban.stellar.org/docs

### Block Explorers
- **0G:** https://scan.0g.ai/
- **Pi Mainnet:** https://pi.blockscout.com/
- **Pi Testnet:** https://testnet.minepi.com/

### Community Support
- **GitHub Issues:** https://github.com/onenoly1010/pi-forge-quantum-genesis/issues
- **Repository Docs:** https://github.com/onenoly1010/pi-forge-quantum-genesis/tree/main/docs

---

## License

MIT License - See LICENSE file for details
