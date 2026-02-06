# Deployment Scripts

Comprehensive deployment automation for OINIO contracts across multiple chains.

## Quick Reference

### Main Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `deploy-all.sh` | Orchestrate all deployments | `bash deploy-all.sh [--target TARGET] [--network NETWORK]` |
| `pre-deploy-check.sh` | Safety checks before deployment | `bash pre-deploy-check.sh [--network NETWORK]` |
| `post-deploy-check.sh` | Health checks after deployment | `bash post-deploy-check.sh [--network NETWORK]` |

### From Repository Root

```bash
# Full deployment with checks
npm run deploy:check          # Pre-flight checks
npm run deploy:all            # Deploy everything
npm run deploy:health         # Post-deployment verification

# Targeted deployments
npm run deploy:inft           # iNFT contracts only
npm run deploy:dex            # DEX contracts only
npm run deploy:memorial       # Memorial contract only

# Testnet
npm run deploy:all:testnet    # Deploy to testnet
npm run deploy:check:testnet  # Testnet pre-checks
npm run deploy:health:testnet # Testnet health checks
```

## Script Details

### deploy-all.sh

**Purpose:** Unified deployment orchestration across all platforms (Hardhat, Forge, Soroban)

**Features:**
- Multi-target deployment (all, inft, dex, memorial)
- Network selection (mainnet, testnet)
- Dry-run mode for safe preview
- Automated pre/post-deployment checks
- Deployment summary generation

**Options:**
```bash
--target <TARGET>    # all, inft, dex, memorial
--network <NETWORK>  # mainnet, testnet
--skip-checks        # Skip pre-deployment checks
--dry-run            # Show plan without executing
--help               # Show help message
```

**Examples:**
```bash
# Deploy everything to mainnet
bash deploy-all.sh

# Deploy iNFT to testnet
bash deploy-all.sh --target inft --network testnet

# Preview DEX deployment
bash deploy-all.sh --target dex --dry-run
```

### pre-deploy-check.sh

**Purpose:** Comprehensive pre-deployment validation

**Checks:**
1. ✅ Environment Configuration (.env file, keys, RPC URLs)
2. ✅ Required Tools (Node.js, npm, forge, cast, soroban)
3. ✅ Network Connectivity (RPC endpoint accessibility)
4. ✅ Wallet Balances (sufficient funds for deployment)
5. ✅ Contract Compilation (artifacts exist or can be built)
6. ✅ Git Status (uncommitted changes warning)
7. ✅ Security Checks (no hardcoded keys, .env in .gitignore)

**Usage:**
```bash
# Check mainnet readiness
bash pre-deploy-check.sh

# Check testnet readiness
bash pre-deploy-check.sh --network testnet
```

**Exit Codes:**
- `0`: All checks passed
- `1`: One or more checks failed

### post-deploy-check.sh

**Purpose:** Verify deployed contracts and test basic functionality

**Checks:**
1. ✅ Contract Deployment (code exists on-chain)
2. ✅ Contract Metadata (name, symbol, supply)
3. ✅ Function Callability (view functions work)
4. ✅ Integration Tests (basic interactions)
5. ✅ Deployment Records (logs and artifacts)

**Features:**
- Auto-detects contract addresses from .env
- Supports multiple networks (Pi, 0G, Soroban)
- Generates detailed health report
- Tests using cast (if available)

**Usage:**
```bash
# Check mainnet deployments
bash post-deploy-check.sh

# Check testnet deployments
bash post-deploy-check.sh --network testnet
```

## Environment Setup

### Required .env Variables

```bash
# Minimum required
PRIVATE_KEY=0x...
PI_MAINNET_RPC=https://rpc.mainnet.pi.network
ZERO_G_RPC=https://evmrpc.0g.ai

# For testnet
PI_TESTNET_RPC=https://api.testnet.minepi.com/rpc

# Deployed addresses (populated after deployment)
OINIO_TOKEN_ADDRESS=
OINIO_REGISTRY_ADDRESS=
W0G_ADDRESS=
FACTORY_ADDRESS=
ROUTER_ADDRESS=
MEMORIAL_CONTRACT_ID=
```

See [../.env.template](../.env.template) for complete configuration.

### Setup Steps

1. **Copy template:**
   ```bash
   cd contracts
   cp .env.template .env
   ```

2. **Edit .env:**
   - Add your `PRIVATE_KEY`
   - Verify RPC URLs
   - Adjust gas settings if needed

3. **Validate:**
   ```bash
   npm run deploy:check
   ```

## Deployment Workflow

### Recommended Flow

```bash
# 1. Setup environment
cd contracts
cp .env.template .env
# Edit .env with your configuration

# 2. Pre-deployment checks
npm run deploy:check

# 3. Deploy contracts
npm run deploy:all

# 4. Verify deployment
npm run deploy:health

# 5. Update frontend config
# Copy addresses from .env to frontend/.env
```

### Testnet Flow

```bash
# 1. Configure testnet in .env
PI_TESTNET_RPC=https://api.testnet.minepi.com/rpc

# 2. Run testnet deployment
npm run deploy:check:testnet
npm run deploy:all:testnet
npm run deploy:health:testnet
```

## Troubleshooting

### Script Permissions

If scripts aren't executable:
```bash
cd contracts/scripts
chmod +x *.sh
```

### Environment Issues

If environment variables aren't loaded:
```bash
# Verify .env exists
ls -la contracts/.env

# Check .env format (no spaces around =)
cat contracts/.env
```

### Network Connectivity

If RPC checks fail:
```bash
# Test RPC manually
curl -X POST https://rpc.mainnet.pi.network \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_chainId","params":[],"id":1}'
```

### Balance Issues

If balance checks fail:
```bash
# Check balance with cast
cast balance YOUR_ADDRESS --rpc-url https://rpc.mainnet.pi.network
```

## Output Files

### Deployment Logs

Scripts generate logs in `contracts/deployments/`:
- `deployment_mainnet_YYYYMMDD_HHMMSS.txt`
- `health_check_mainnet_YYYYMMDD_HHMMSS.txt`

### Hardhat Deployment Records

Hardhat creates JSON files in `contracts/hardhat/deployments/`:
- `OINIOToken-<chainId>.json`
- `OINIOModelRegistry-<chainId>.json`

### Soroban Contract Address

Saved in `contracts/oinio-memorial-bridge/`:
- `contract_address.txt`

## Integration with CI/CD

These scripts are designed for automation:

```yaml
# GitHub Actions example
- name: Pre-deployment checks
  run: npm run deploy:check

- name: Deploy contracts
  run: npm run deploy:all
  env:
    PRIVATE_KEY: ${{ secrets.DEPLOYER_KEY }}

- name: Health check
  run: npm run deploy:health
```

## Security Notes

⚠️ **Never commit .env files with real private keys!**

✅ Best practices:
- Use separate keys for testnet and mainnet
- Use hardware wallets for mainnet deployments
- Rotate keys after suspicious activity
- Keep private keys encrypted at rest
- Enable 2FA on all accounts

## Support

- **Documentation:** [../DEPLOYMENT_GUIDE.md](../DEPLOYMENT_GUIDE.md)
- **Issues:** https://github.com/onenoly1010/pi-forge-quantum-genesis/issues
- **0G Docs:** https://docs.0g.ai/
- **Pi Network:** https://developers.minepi.com/
- **Hardhat:** https://hardhat.org/docs
- **Foundry:** https://book.getfoundry.sh/
- **Soroban:** https://soroban.stellar.org/docs
