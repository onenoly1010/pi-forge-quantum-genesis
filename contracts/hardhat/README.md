# Hardhat Deployment Scripts

TypeScript-based deployment scripts using Hardhat for OINIO smart contracts.

## Quick Start

```bash
npm install
npm run check:balance
npm run deploy:0g:inft      # Deploy to 0G
npm run deploy:pi:inft      # Deploy to Pi Mainnet
```

## Prerequisites

- Node.js 20+
- Private key with funded wallet
- `.env` file configured (see `../.env.example`)

## Available Commands

| Command | Description |
|---------|-------------|
| `npm run compile` | Compile contracts |
| `npm run check:balance` | Check deployer balance and environment |
| `npm run deploy:0g:inft` | Deploy iNFT contracts to 0G |
| `npm run deploy:0g:dex` | Reference script for DEX (use Forge) |
| `npm run deploy:pi:inft` | Deploy iNFT contracts to Pi Mainnet |
| `npm run deploy:pi:testnet:inft` | Deploy iNFT contracts to Pi Testnet |

## Environment Configuration

Create `../.env` with:

```bash
PRIVATE_KEY=0x...
ZERO_G_RPC=https://evmrpc.0g.ai
PI_MAINNET_RPC=https://rpc.mainnet.pi.network
PI_TESTNET_RPC=https://api.testnet.minepi.com/rpc
```

## Deployment Process

### 1. Pre-Deployment Check
```bash
npm run check:balance
```

Verifies:
- ✓ Private key is set
- ✓ Network is accessible
- ✓ Balance is sufficient
- ✓ Gas price is available

### 2. Deploy Contracts
```bash
# To 0G Network
npm run deploy:0g:inft

# To Pi Network Mainnet
npm run deploy:pi:inft

# To Pi Network Testnet
npm run deploy:pi:testnet:inft
```

### 3. Verify on Block Explorer
```bash
npx hardhat verify --network <network> <address> "<constructor_arg1>" "<constructor_arg2>"
```

## Deployed Contracts

Deployment info is saved to `deployments/`:
- `OINIOToken-<chainId>.json`
- `OINIOModelRegistry-<chainId>.json`

## Contract Verification

### Automatic Verification
Add `--verify` flag during deployment (configured in hardhat.config.ts)

### Manual Verification
```bash
npx hardhat verify \
  --network zeroG \
  0x... \
  "0x..." # constructor args
```

## Troubleshooting

### Network Connection Issues
```bash
# Test RPC
curl -X POST https://evmrpc.0g.ai \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
```

### Insufficient Balance
```bash
# Check balance
npx hardhat run scripts/check-balance.ts --network <network>
```

### Compilation Errors
```bash
# Clean and rebuild
rm -rf artifacts cache
npx hardhat compile
```

## Script Details

### check-balance.ts
Pre-deployment safety checks:
- Environment validation
- Network connectivity
- Balance verification
- Gas price check
- Post-deployment verification helper

### deploy-inft.ts
Deploys:
1. OINIOToken (ERC-20)
2. OINIOModelRegistry (ERC-721)

Features:
- Comprehensive pre-flight checks
- Detailed deployment logging
- Automatic verification
- Deployment info persistence
- Next steps guidance

### deploy-dex.ts
Reference script for DEX deployment.

**Note:** DEX deployment is recommended via Forge (see `../0g-uniswap-v2/`).

## Network Configuration

### 0G Aristotle Mainnet
- **Chain ID:** 16661
- **RPC:** https://evmrpc.0g.ai
- **Explorer:** https://scan.0g.ai/

### Pi Network Mainnet
- **Chain ID:** 314159
- **RPC:** https://rpc.mainnet.pi.network
- **Explorer:** https://pi.blockscout.com/

### Pi Network Testnet
- **Chain ID:** 2025
- **RPC:** https://api.testnet.minepi.com/rpc
- **Explorer:** https://testnet.minepi.com/

## For More Information

See parent directory's [DEPLOYMENT_GUIDE.md](../DEPLOYMENT_GUIDE.md) for comprehensive deployment documentation.

## License

MIT
