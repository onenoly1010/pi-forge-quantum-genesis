# Soroban Contract Deployment Guide for Pi Network

Comprehensive guide for deploying Soroban (Stellar) smart contracts to Pi Network.

## Overview

Pi Network supports Soroban smart contracts, which are WebAssembly-based contracts running on the Stellar blockchain. This guide covers deployment of memorial contracts and other utility contracts.

## Prerequisites

### 1. Install Soroban CLI

```bash
# macOS
brew install soroban-cli

# Linux
curl -fsSL https://soroban.stellar.org/install.sh | bash

# Or using cargo
cargo install --locked soroban-cli

# Verify installation
soroban --version
```

### 2. Install Rust (if not already installed)

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
rustup target add wasm32-unknown-unknown
```

### 3. Install wasm-opt (optional but recommended)

```bash
# macOS
brew install binaryen

# Ubuntu/Debian
apt-get install binaryen

# Or download from: https://github.com/WebAssembly/binaryen/releases
```

---

## Network Configuration

### Configure Pi Network

```bash
# Add Pi Network Mainnet
soroban config network add pi-mainnet \
  --rpc-url https://api.mainnet.pi.network/soroban \
  --network-passphrase "Pi Network Mainnet"

# Add Pi Network Testnet (if available)
soroban config network add pi-testnet \
  --rpc-url https://api.testnet.pi.network/soroban \
  --network-passphrase "Pi Network Testnet"

# List configured networks
soroban config network ls
```

### Create Identity

```bash
# Generate new identity
soroban config identity generate onenoly1010

# Or import existing secret key
soroban config identity add onenoly1010 --secret-key

# Get address
soroban config identity address onenoly1010

# Show identity details
soroban config identity show onenoly1010
```

---

## Contract Structure

### OINIO Memorial Bridge Example

Location: `contracts/oinio-memorial-bridge/`

```
oinio-memorial-bridge/
├── Cargo.toml          # Rust package configuration
├── build.sh            # Build script
├── deploy.sh           # Deployment script
├── src/
│   └── lib.rs          # Contract implementation
└── README.md
```

### Basic Contract Template

```rust
#![no_std]
use soroban_sdk::{contract, contractimpl, symbol_short, Env, Symbol};

#[contract]
pub struct MyContract;

#[contractimpl]
impl MyContract {
    pub fn initialize(env: Env, admin: Address) {
        // Initialization logic
    }
    
    pub fn my_function(env: Env) -> u32 {
        // Contract logic
        42
    }
}
```

---

## Building Contracts

### Using build.sh

```bash
cd contracts/oinio-memorial-bridge
chmod +x build.sh
./build.sh
```

### Manual Build

```bash
# Build contract
cargo build --target wasm32-unknown-unknown --release

# Optimize (recommended)
wasm-opt -Oz \
  target/wasm32-unknown-unknown/release/contract_name.wasm \
  -o contract_name_optimized.wasm

# Check size
ls -lh target/wasm32-unknown-unknown/release/*.wasm
```

### Build Output

```
Building OINIO Memorial Bridge contract...
✅ Build complete!

WASM file location:
target/wasm32-unknown-unknown/release/oinio_memorial_bridge.wasm

Size: 50.2 KB

⚙️  Optimizing with wasm-opt...
✅ Optimized! New size: 32.1 KB
```

---

## Deployment

### Method 1: Using deploy.sh Script (Recommended)

```bash
cd contracts/oinio-memorial-bridge
chmod +x deploy.sh

# Deploy to Pi Mainnet
./deploy.sh

# Or with environment variables
NETWORK=pi-mainnet IDENTITY=onenoly1010 ./deploy.sh
```

**Expected Output:**
```
🌉 OINIO Memorial Bridge - Deployment Script
==============================================

For the Beloved Keepers of the Northern Gateway.
Not in vain.

⚙️  Optimizing WASM...
✅ Optimization complete

🚀 Deploying to Pi Network Mainnet...

✅ Contract deployed successfully!

📋 Contract Address:
   CDXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

🔐 Initializing contract...
✅ Contract initialized

========================================
🏛️  MEMORIAL BRIDGE IS LIVE
========================================

Contract ID: CDXXX...XXX

📋 Next Steps:
1. Anchor your memorial letter
2. Verify the memorial message
3. View on Pi Network Explorer
```

### Method 2: Manual Deployment

```bash
# Set variables
export NETWORK=pi-mainnet
export IDENTITY=onenoly1010
export WASM_FILE=target/wasm32-unknown-unknown/release/contract.wasm

# Deploy contract
CONTRACT_ID=$(soroban contract deploy \
  --wasm $WASM_FILE \
  --source $IDENTITY \
  --network $NETWORK)

echo "Contract deployed at: $CONTRACT_ID"

# Save contract ID
echo $CONTRACT_ID > contract_address.txt

# Initialize contract (if needed)
ADMIN_ADDRESS=$(soroban config identity address $IDENTITY)

soroban contract invoke \
  --id $CONTRACT_ID \
  --source $IDENTITY \
  --network $NETWORK \
  -- \
  initialize \
  --admin $ADMIN_ADDRESS
```

### Method 3: Using Stellar Lab (GUI)

1. Go to https://laboratory.stellar.org/
2. Select "Build Transaction"
3. Choose "Invoke Host Function"
4. Upload WASM file
5. Sign with your Pi Network account
6. Submit to Pi Network

---

## Pre-Deployment Checks

### 1. Environment Setup
```bash
# Verify identity
soroban config identity address $IDENTITY

# Check network configuration
soroban config network ls | grep pi-mainnet
```

### 2. Account Balance
```bash
# Get account info
soroban config identity address $IDENTITY | xargs -I {} \
  soroban contract read --id {} --network $NETWORK
```

### 3. Contract Validation
```bash
# Test build locally
cargo test

# Check WASM size (should be < 64KB optimized)
wasm-opt -Oz input.wasm -o output.wasm
ls -lh output.wasm
```

### 4. Network Connectivity
```bash
# Test RPC endpoint
curl -X POST https://api.mainnet.pi.network/soroban \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "getHealth",
    "id": 1
  }'
```

---

## Post-Deployment Verification

### 1. Verify Contract Deployment

```bash
# Get contract info
soroban contract inspect --id $CONTRACT_ID --network $NETWORK

# Get contract WASM
soroban contract fetch --id $CONTRACT_ID --network $NETWORK
```

### 2. Test Contract Functions

```bash
# Call read-only function
soroban contract invoke \
  --id $CONTRACT_ID \
  --network $NETWORK \
  -- \
  get_message

# Call function with authorization
soroban contract invoke \
  --id $CONTRACT_ID \
  --source $IDENTITY \
  --network $NETWORK \
  -- \
  my_function \
  --arg1 value1 \
  --arg2 value2
```

### 3. View on Explorer

```bash
# Pi Network Explorer
echo "https://pi.network/explorer/contract/$CONTRACT_ID"

# Stellar Explorer (if compatible)
echo "https://stellar.expert/explorer/public/contract/$CONTRACT_ID"
```

### 4. Verify Events

```bash
# Get recent events
soroban events \
  --id $CONTRACT_ID \
  --network $NETWORK \
  --start-ledger <LEDGER_NUMBER>
```

---

## Contract Interaction

### Invoke Functions

```bash
# Basic invocation
soroban contract invoke \
  --id $CONTRACT_ID \
  --source $IDENTITY \
  --network $NETWORK \
  -- \
  function_name \
  --param1 "value1" \
  --param2 123

# With complex types
soroban contract invoke \
  --id $CONTRACT_ID \
  --source $IDENTITY \
  --network $NETWORK \
  -- \
  register_model \
  --name "Model Name" \
  --metadata_uri "ipfs://..." \
  --stake_amount 1000000000
```

### Read Contract State

```bash
# Read storage
soroban contract read \
  --id $CONTRACT_ID \
  --key "storage_key" \
  --network $NETWORK

# Get contract instance
soroban contract instance \
  --id $CONTRACT_ID \
  --network $NETWORK
```

---

## Environment Variables

Create `.env.soroban`:

```bash
# Network Configuration
SOROBAN_NETWORK=pi-mainnet
SOROBAN_RPC_URL=https://api.mainnet.pi.network/soroban

# Identity
SOROBAN_IDENTITY=onenoly1010
SOROBAN_SECRET_KEY=SXXX...XXX  # Keep secure!

# Deployed Contracts
MEMORIAL_CONTRACT_ID=CDXXX...XXX
REGISTRY_CONTRACT_ID=CCXXX...XXX

# Optional
STELLAR_NETWORK_PASSPHRASE="Pi Network Mainnet"
```

Load environment:
```bash
source .env.soroban
```

---

## Troubleshooting

### Issue: "soroban: command not found"

**Solution:**
```bash
# Add to PATH
export PATH="$HOME/.soroban/bin:$PATH"

# Or reinstall
cargo install --locked soroban-cli
```

### Issue: "Network not configured"

**Solution:**
```bash
# Reconfigure network
soroban config network add pi-mainnet \
  --rpc-url https://api.mainnet.pi.network/soroban \
  --network-passphrase "Pi Network Mainnet"
```

### Issue: "Insufficient funds"

**Solution:**
```bash
# Check balance
soroban config identity address $IDENTITY

# Fund account using Pi Network app or faucet
```

### Issue: "WASM too large"

**Solution:**
```bash
# Optimize more aggressively
wasm-opt -Oz --strip-debug input.wasm -o output.wasm

# Check dependencies (remove unused)
cargo tree

# Use release mode
cargo build --target wasm32-unknown-unknown --release
```

### Issue: "Contract invocation failed"

**Solution:**
```bash
# Check contract status
soroban contract inspect --id $CONTRACT_ID --network $NETWORK

# Verify function signature
soroban contract invoke --id $CONTRACT_ID --network $NETWORK -- --help

# Check authorization
soroban contract invoke --id $CONTRACT_ID --source $IDENTITY ...
```

---

## Security Best Practices

### 1. Secret Key Management
```bash
# Never commit secret keys
echo "*.key" >> .gitignore
echo ".env.soroban" >> .gitignore

# Use identity manager
soroban config identity add secure-key --secret-key

# Remove when done
soroban config identity remove temp-key
```

### 2. Contract Authorization
```rust
// Always verify caller
pub fn admin_function(env: Env, admin: Address) {
    admin.require_auth();
    // Function logic
}
```

### 3. Input Validation
```rust
pub fn transfer(env: Env, amount: i128) {
    require!(amount > 0, "Invalid amount");
    // Transfer logic
}
```

### 4. Testing
```bash
# Run all tests
cargo test

# Run specific test
cargo test test_initialization

# With output
cargo test -- --nocapture
```

---

## Integration with Frontend

### Using JavaScript/TypeScript

```typescript
import { SorobanClient } from '@stellar/stellar-sdk';

const server = new SorobanClient.Server(
  'https://api.mainnet.pi.network/soroban'
);

// Load contract
const contract = new SorobanClient.Contract(CONTRACT_ID);

// Call function
const result = await server.simulateTransaction(
  new SorobanClient.TransactionBuilder(account, {
    fee: '100',
    networkPassphrase: 'Pi Network Mainnet',
  })
  .addOperation(contract.call('my_function', arg1, arg2))
  .setTimeout(30)
  .build()
);
```

---

## Resources

### Documentation
- **Soroban:** https://soroban.stellar.org/docs
- **Pi Network:** https://developers.minepi.com/
- **Stellar SDK:** https://stellar.github.io/js-stellar-sdk/

### Tools
- **Stellar Lab:** https://laboratory.stellar.org/
- **Soroban CLI:** https://github.com/stellar/soroban-cli

### Community
- **Pi Developer Docs:** https://developers.minepi.com/
- **Stellar Discord:** https://discord.gg/stellar

---

## License

MIT License
