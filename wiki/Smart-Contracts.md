# 📜 Smart Contracts - OINIO Token & Model Registry

**Last Updated**: December 2025

Complete documentation for smart contracts deployed across Pi Network and 0G Aristotle networks.

---

## 🎯 Overview

Quantum Pi Forge utilizes smart contracts for:
- **OINIO Token** - Governance and utility token
- **Model Registry** - AI model verification and tracking
- **DEX Contracts** - Decentralized exchange (0G Aristotle)
- **Payment Processing** - Pi Network integration

---

## 🏛️ Contract Architecture

### Networks

**Pi Network Mainnet**:
- OINIO Token
- Model Registry
- Payment integration

**0G Aristotle Testnet**:
- DEX (Uniswap V2 fork)
- Liquidity pools
- Token swaps

---

## 💎 OINIO Token Contract

### Overview

**Network**: Pi Network Mainnet  
**Standard**: ERC-20 compatible  
**Supply**: Fixed/Dynamic (TBD)  
**Purpose**: Governance and utility

### Key Functions

```solidity
// Transfer tokens
function transfer(address to, uint256 amount) public returns (bool)

// Approve spending
function approve(address spender, uint256 amount) public returns (bool)

// Transfer from
function transferFrom(address from, address to, uint256 amount) public returns (bool)

// Get balance
function balanceOf(address account) public view returns (uint256)
```

### Token Economics

- **Use Cases**: Governance voting, platform fees, staking rewards
- **Distribution**: Community allocation, team vesting, liquidity
- **Burning**: Deflationary mechanism (if applicable)

---

## 🧠 Model Registry Contract

### Overview

**Network**: Pi Network Mainnet  
**Purpose**: Track and verify AI models  
**Features**: Immutable record, reputation system, version control

### Key Functions

```solidity
// Register new model
function registerModel(
    string memory modelHash,
    string memory metadata,
    address owner
) public returns (uint256 modelId)

// Update model
function updateModel(uint256 modelId, string memory newHash) public

// Get model info
function getModel(uint256 modelId) public view returns (Model memory)

// Verify model
function verifyModel(uint256 modelId) public returns (bool)
```

### Model Struct

```solidity
struct Model {
    uint256 id;
    string hash; // IPFS or content hash
    address owner;
    uint256 timestamp;
    bool verified;
    uint256 reputation;
}
```

---

## 💱 DEX Contracts (0G Aristotle)

### Overview

**Network**: 0G Aristotle Testnet  
**Type**: Uniswap V2 Fork  
**Purpose**: Decentralized token exchange

### Core Contracts

**Factory**:
```solidity
// Create pair
function createPair(address tokenA, address tokenB) external returns (address pair)

// Get pair
function getPair(address tokenA, address tokenB) external view returns (address pair)
```

**Router**:
```solidity
// Add liquidity
function addLiquidity(
    address tokenA,
    address tokenB,
    uint amountADesired,
    uint amountBDesired,
    uint amountAMin,
    uint amountBMin,
    address to,
    uint deadline
) external returns (uint amountA, uint amountB, uint liquidity)

// Swap exact tokens
function swapExactTokensForTokens(
    uint amountIn,
    uint amountOutMin,
    address[] calldata path,
    address to,
    uint deadline
) external returns (uint[] memory amounts)
```

### Deployment Info

**Location**: `contracts/0g-uniswap-v2/`  
**Status**: Testnet deployed  
**Verification**: On-chain verified

---

## 🔐 Security Features

### Access Control

- **Owner-only functions**: Critical operations restricted
- **Multi-sig support**: Guardian approval for major changes
- **Timelock**: Delayed execution for sensitive updates

### Auditing

- **Code reviews**: Multiple reviewer approval
- **Automated scanning**: Security tools integration
- **Formal verification**: Critical functions verified

### Emergency Controls

```solidity
// Pause contract
function pause() external onlyOwner

// Unpause contract
function unpause() external onlyOwner

// Emergency withdraw
function emergencyWithdraw() external onlyOwner
```

---

## 📍 Contract Addresses

### Pi Network Mainnet

```
OINIO Token: [TBD - To be deployed]
Model Registry: [TBD - To be deployed]
```

### 0G Aristotle Testnet

```
Factory: [Check contracts/0g-uniswap-v2/DEPLOYMENT.md]
Router: [Check contracts/0g-uniswap-v2/DEPLOYMENT.md]
WETH: [Check contracts/0g-uniswap-v2/DEPLOYMENT.md]
```

---

## 🛠️ Development

### Setup

```bash
cd contracts

# Install dependencies
npm install

# Compile contracts
npx hardhat compile

# Run tests
npx hardhat test
```

### Deployment

```bash
# Deploy to testnet
npx hardhat run scripts/deploy.js --network testnet

# Verify on explorer
npx hardhat verify --network testnet CONTRACT_ADDRESS
```

### Testing

```bash
# Unit tests
npx hardhat test

# Coverage
npx hardhat coverage

# Gas report
REPORT_GAS=true npx hardhat test
```

---

## 📚 Integration Examples

### JavaScript/Web3.js

```javascript
const Web3 = require('web3');
const OINIOToken = require('./abi/OINIOToken.json');

const web3 = new Web3('https://rpc.pi.network');
const contract = new web3.eth.Contract(
  OINIOToken.abi,
  'OINIO_TOKEN_ADDRESS'
);

// Get balance
const balance = await contract.methods.balanceOf(address).call();

// Transfer tokens
await contract.methods.transfer(recipient, amount).send({from: sender});
```

### Python/Web3.py

```python
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://rpc.pi.network'))
contract = w3.eth.contract(address='OINIO_TOKEN_ADDRESS', abi=abi)

# Get balance
balance = contract.functions.balanceOf(address).call()

# Transfer tokens
tx = contract.functions.transfer(recipient, amount).transact({'from': sender})
```

---

## 🔍 Verification

### On-Chain Verification

All contracts verified on block explorers:
- **Pi Network**: Pi Explorer
- **0G Aristotle**: 0G Explorer

### Source Code

Available in repository:
```
contracts/
├── src/
│   ├── OINIOToken.sol
│   ├── ModelRegistry.sol
│   └── ...
├── 0g-uniswap-v2/
│   ├── contracts/
│   └── scripts/
└── test/
```

---

## 📖 Documentation

### Full Contract Docs

See repository files:
- `contracts/README.md` - Overview
- `contracts/DEPLOYMENT_CHECKLIST.md` - Deployment guide
- `contracts/VERIFICATION.md` - Verification procedures
- `contracts/0g-uniswap-v2/README.md` - DEX documentation

### API Reference

Smart contract ABIs available in:
- `contracts/artifacts/` - Compiled contracts
- `contracts/abi/` - ABI JSON files

---

## See Also

- [[Pi Network Overview]] - Pi Network integration
- [[Payment API]] - Payment flow
- [[Ecosystem Overview]] - Complete architecture
- [[Verification System]] - Multi-chain verification

---

[[Home]] | [[Ecosystem Overview]] | [[Payment API]]

---

*Immutable code. Transparent logic. Trustless execution.* 📜⚛️🔥
