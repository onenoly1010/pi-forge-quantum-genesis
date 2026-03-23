# Quick Reference - Deployment Commands

One-page reference for all deployment commands across platforms.

---

## 🚀 Quick Deploy Commands

### Check Environment (Always run first!)
```bash
# Hardhat
cd contracts/hardhat && npm run check:balance

# Forge
source contracts/.env && cast balance $DEPLOYER --rpc-url $RPC_URL
```

---

## Hardhat Deployments (iNFT Contracts)

```bash
# From repo root:

# 1. Install dependencies (first time only)
npm run contracts:install

# 2. Deploy to 0G Network
npm run deploy:inft:0g

# 3. Deploy to Pi Network Mainnet
npm run deploy:inft:pi

# 4. Deploy to Pi Network Testnet
npm run deploy:inft:pi:testnet
```

---

## Forge Deployments

### OINIO Contracts (Pi Network)
```bash
cd contracts

# Testnet
forge script script/Deploy.s.sol \
  --rpc-url $RPC_URL_TESTNET \
  --private-key $PRIVATE_KEY \
  --broadcast \
  --verify

# Mainnet
forge script script/Deploy.s.sol \
  --rpc-url $RPC_URL_MAINNET \
  --private-key $PRIVATE_KEY \
  --broadcast \
  --verify
```

### DEX Contracts (0G Network)
```bash
cd contracts/0g-uniswap-v2

# Deploy W0G
forge script script/Deploy.s.sol:Deploy \
  --sig "deployW0GOnly()" \
  --rpc-url $RPC_URL \
  --private-key $PRIVATE_KEY \
  --broadcast

# Deploy Full DEX (after W0G)
forge script script/Deploy.s.sol:Deploy \
  --sig "run()" \
  --rpc-url $RPC_URL \
  --private-key $PRIVATE_KEY \
  --broadcast
```

---

## Soroban Deployments (Pi Network)

```bash
cd contracts/oinio-memorial-bridge

# Build
./build.sh

# Deploy
./deploy.sh

# Or manually:
soroban contract deploy \
  --wasm target/wasm32-unknown-unknown/release/contract.wasm \
  --source onenoly1010 \
  --network pi-mainnet
```

---

## Verification Commands

### Hardhat
```bash
npx hardhat verify \
  --network <network> \
  <contract-address> \
  "<constructor-arg1>" \
  "<constructor-arg2>"
```

### Forge
```bash
forge verify-contract <address> \
  src/Contract.sol:ContractName \
  --chain-id <chain-id> \
  --constructor-args $(cast abi-encode "constructor(...)" <args>)
```

### Soroban
```bash
soroban contract inspect \
  --id <contract-id> \
  --network pi-mainnet
```

---

## Environment Setup

### One-time Setup
```bash
# 1. Copy environment template
cp contracts/.env.example contracts/.env

# 2. Edit with your values
nano contracts/.env

# 3. Install Hardhat dependencies
cd contracts/hardhat && npm install
```

### Required Variables
```bash
# Minimum required:
PRIVATE_KEY=0x...

# Networks (uses defaults if not set):
ZERO_G_RPC=https://evmrpc.0g.ai
PI_MAINNET_RPC=https://rpc.mainnet.pi.network
PI_TESTNET_RPC=https://api.testnet.minepi.com/rpc
```

---

## Pre-Deployment Checklist

- [ ] Private key is set in .env
- [ ] Wallet has sufficient balance (0.1+ ETH)
- [ ] RPC endpoint is accessible
- [ ] Contracts compile: `forge build` or `npm run compile`
- [ ] Network connectivity: `cast block-number --rpc-url $RPC_URL`
- [ ] .env is in .gitignore

---

## Common Issues & Quick Fixes

### "Insufficient Balance"
```bash
# Check balance
cast balance $DEPLOYER --rpc-url $RPC_URL
# Fund from faucet or transfer
```

### "Network Not Found"
```bash
# Check RPC
curl -X POST $RPC_URL \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
```

### "Nonce Too Low"
```bash
# Check nonce
cast nonce $DEPLOYER --rpc-url $RPC_URL
# Wait for pending transactions
```

### "Compilation Failed"
```bash
# Clean and rebuild
forge clean && forge build
# or
rm -rf cache artifacts && npm run compile
```

---

## Network Details

| Network | Chain ID | RPC URL | Explorer |
|---------|----------|---------|----------|
| 0G Mainnet | 16661 | https://evmrpc.0g.ai | https://scan.0g.ai |
| Pi Mainnet | 314159 | https://rpc.mainnet.pi.network | https://pi.blockscout.com |
| Pi Testnet | 2025 | https://api.testnet.minepi.com/rpc | https://testnet.minepi.com |

---

## Post-Deployment

### Save Contract Addresses
```bash
# To .env
echo "OINIO_TOKEN_ADDRESS=0x..." >> contracts/.env
echo "OINIO_REGISTRY_ADDRESS=0x..." >> contracts/.env
```

### Test Contracts
```bash
# Get token supply
cast call $OINIO_TOKEN_ADDRESS "totalSupply()" --rpc-url $RPC_URL

# Check registry
cast call $OINIO_REGISTRY_ADDRESS "totalModels()" --rpc-url $RPC_URL
```

---

## Documentation Links

- **Full Guide:** [contracts/DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Soroban Guide:** [contracts/SOROBAN_DEPLOYMENT.md](SOROBAN_DEPLOYMENT.md)
- **Hardhat Docs:** [contracts/hardhat/README.md](hardhat/README.md)
- **Main README:** [contracts/README.md](README.md)

---

## Support

For issues: https://github.com/onenoly1010/pi-forge-quantum-genesis/issues
