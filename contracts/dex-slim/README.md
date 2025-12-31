# DEX Contracts - Slim Router

## Purpose

This directory contains the size-optimized UniswapV2 router implementation designed to fit within the 0G Aristotle Mainnet's 24KB bytecode limit.

## ✅ Compilation Success

**Deployed Bytecode**: 4,769 bytes  
**24KB Limit**: 24,576 bytes  
**Usage**: 19.41%  
**Status**: ✅ Ready for deployment

## Structure

```
dex-slim/
├── UniswapV2Router02Slim.sol  # Main router contract (optimized for size)
├── MockERC20.sol               # Mock ERC20 for testing
└── interfaces/
    ├── IERC20.sol               # ERC20 interface
    ├── IUniswapV2Factory.sol    # Factory interface
    └── IUniswapV2Pair.sol       # Pair interface
```

## Compilation

### Quick Compile (Recommended)

```bash
npm run compile:slim-router
```

This uses the local solc compiler directly and generates artifacts without network dependencies.

### With Hardhat

```bash
npx hardhat compile
```

**Note**: Requires network access to download Solidity compilers.

## Key Features

### Optimizations
- ✅ Removed all ETH-specific functions
- ✅ Inlined library functions
- ✅ Custom errors instead of string reverts
- ✅ Solidity 0.8.19 (no SafeMath needed)
- ✅ Optimizer runs=1, viaIR enabled
- ✅ Immutable variables

### Core Functions
- ✅ `addLiquidity` - Add liquidity to ERC20 pairs
- ✅ `removeLiquidity` - Remove liquidity from pairs
- ✅ `swapExactTokensForTokens` - Exact input swaps
- ✅ `swapTokensForExactTokens` - Exact output swaps

## Differences from Standard Router

### ⚠️ No Native ETH Support

The slim router **does not support** native ETH transactions. Users must:

1. Wrap ETH to WETH manually:
```solidity
weth.deposit({ value: ethAmount });
```

2. Approve the router:
```solidity
weth.approve(routerAddress, ethAmount);
```

3. Use WETH in trades:
```solidity
router.swapExactTokensForTokens(
  ethAmount,
  amountOutMin,
  [WETH, TOKEN],
  recipient,
  deadline
);
```

### Removed Functions

- ❌ `addLiquidityETH`
- ❌ `removeLiquidityETH`
- ❌ `swapExactETHForTokens`
- ❌ `swapTokensForExactETH`
- ❌ `swapExactTokensForETH`
- ❌ `swapETHForExactTokens`
- ❌ `receive()` fallback

## Testing

```bash
npx hardhat test
```

Test suite covers:
- Bytecode size verification
- Add/remove liquidity
- Token swaps
- Deadline enforcement
- Slippage protection

## Deployment

See [DEX_DEPLOYMENT.md](../../docs/DEX_DEPLOYMENT.md) for full deployment guide.

Quick start:

```bash
# Set environment variables
cp .env.example .env
# Edit .env with your private key and settings

# Deploy to testnet
npx hardhat run scripts/deploy-slim-router.js --network aristotle

# Deploy to mainnet
npx hardhat run scripts/deploy-slim-router.js --network aristotleMainnet
```

## Contract Addresses

### 0G Aristotle Mainnet (ChainID 16661)

- **Factory**: `0x307bFaA937768a073D41a2EbFBD952Be8E38BF91`
- **WETH**: `0x4200000000000000000000000000000000000006`
- **Router**: *To be deployed*

## Security

### Considerations

1. **Reduced Attack Surface** - Fewer functions = less code to audit
2. **No ETH Handling** - No reentrancy via fallback functions
3. **Manual WETH** - Users must handle wrapping/unwrapping
4. **Battle-Tested Base** - Built on UniswapV2Router02 logic

### Recommendations

- ✅ Code review complete
- ⏳ Full audit recommended before mainnet deployment
- ⏳ Community testing period on testnet
- ⏳ Gradual rollout with monitoring

## Documentation

- [Full Deployment Guide](../../docs/DEX_DEPLOYMENT.md)
- [Implementation Summary](../../SLIM_ROUTER_SUMMARY.md)
- [Hardhat Config](../../hardhat.config.js)

## Support

For questions or issues:
- GitHub: [pi-forge-quantum-genesis](https://github.com/onenoly1010/pi-forge-quantum-genesis/issues)
- Tests: `test/SlimRouter.test.js`
- Deployment: `scripts/deploy-slim-router.js`

---

**Version**: 1.0.0  
**Solidity**: 0.8.19  
**Target**: 0G Aristotle Mainnet  
**Status**: ✅ Verified & Ready
