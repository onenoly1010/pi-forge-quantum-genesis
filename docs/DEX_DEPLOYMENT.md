# 🔥 DEX Router Deployment Guide

## Overview

This guide covers the deployment of the **UniswapV2Router02Slim** - a size-optimized router contract designed to fit within the 0G Aristotle Mainnet's 24KB bytecode limit.

## Slim Router Optimization

The standard UniswapV2Router02 exceeds 0G's 24KB bytecode limit. Our optimized version achieves significant size reduction through:

### Removed Features
- ✂️ **All ETH-specific functions** - No `addLiquidityETH`, `swapETHForTokens`, `swapTokensForETH`, or `swapExactETHForTokens`
- ✂️ **ETH receive function** - Users must wrap ETH to WETH manually before trading
- ✂️ **Redundant multi-hop helpers** - Simplified swap path handling
- ✂️ **Unnecessary view functions** - Removed duplicate library function wrappers

### Optimizations Applied
- ✅ **Inlined library functions** - UniswapV2Library functions integrated directly
- ✅ **Custom errors** - More gas-efficient than string reverts (Solidity 0.8.19)
- ✅ **Immutable variables** - `factory`, `WETH`, and `initCodeHash` are immutable
- ✅ **Compiler settings** - Optimizer runs=1, viaIR enabled
- ✅ **SafeMath removal** - Solidity 0.8.19 has built-in overflow protection

### Core Functionality Retained
- ✅ `addLiquidity` - Add liquidity to any ERC20 pair
- ✅ `removeLiquidity` - Remove liquidity from any ERC20 pair
- ✅ `swapExactTokensForTokens` - Swap exact input amount for minimum output
- ✅ `swapTokensForExactTokens` - Swap maximum input for exact output amount

## Prerequisites

1. **Environment Setup**
   ```bash
   # Install dependencies
   npm install
   
   # Copy and configure environment variables
   cp .env.example .env
   ```

2. **Required Environment Variables**
   ```bash
   ZEROG_RPC_URL=https://evmrpc-testnet.0g.ai  # or mainnet URL
   PRIVATE_KEY=your_private_key_here
   FACTORY_ADDRESS=0x307bFaA937768a073D41a2EbFBD952Be8E38BF91
   WETH_ADDRESS=0x4200000000000000000000000000000000000006
   INIT_CODE_HASH=0x96e8ac4277198ff8b6f785478aa9a39f403cb768dd02cbee326c3e7da348845f
   ```

3. **Network Configuration**
   - Testnet: ChainID `42069`, RPC: `https://evmrpc-testnet.0g.ai`
   - Mainnet: ChainID `16661`, RPC: `https://evmrpc.0g.ai`

## Deployment Steps

### Step 1: Calculate INIT_CODE_HASH (Optional)

If you need to recalculate the init code hash for your factory:

```bash
npx hardhat run scripts/get-init-code-hash.js --network aristotle
```

This will output the `INIT_CODE_HASH` that you should add to your `.env` file.

### Step 2: Compile Contracts

```bash
npx hardhat compile
```

Expected output:
```
Compiled 10 Solidity files successfully
```

### Step 3: Deploy Slim Router

```bash
# For testnet (ChainID 42069)
npx hardhat run scripts/deploy-slim-router.js --network aristotle

# For mainnet (ChainID 16661)
npx hardhat run scripts/deploy-slim-router.js --network aristotleMainnet
```

Expected output:
```
🚀 Deploying Slim Router to 0G Aristotle Mainnet...
👤 Deployer: 0x...
🏭 Factory: 0x307bFaA937768a073D41a2EbFBD952Be8E38BF91
💧 WETH: 0x4200000000000000000000000000000000000006
🔑 Init Code Hash: 0x96e8ac4277198ff8b6f785478aa9a39f403cb768dd02cbee326c3e7da348845f
📦 Deploying contract...
✅ Router deployed: 0x...
📏 Bytecode size: XXXXX bytes
✅ Bytecode under 24KB limit! (XX.XX% used)
📝 Updated .env.launch with router address
🎉 DEPLOYMENT COMPLETE!
```

### Step 4: Verify Contract (Optional)

```bash
npx hardhat verify --network aristotle <ROUTER_ADDRESS> \
  "0x307bFaA937768a073D41a2EbFBD952Be8E38BF91" \
  "0x4200000000000000000000000000000000000006" \
  "0x96e8ac4277198ff8b6f785478aa9a39f403cb768dd02cbee326c3e7da348845f"
```

## Contract Addresses (0G Aristotle Mainnet)

### Deployed Infrastructure
- **Factory**: `0x307bFaA937768a073D41a2EbFBD952Be8E38BF91`
- **WETH**: `0x4200000000000000000000000000000000000006`
- **Router (Slim)**: *Deploy using steps above*

### Supporting Contracts
- **Cultural Charter**: `0xBA244c9De8fC17C840B41B220893f8ef6f0287C0`
- **Leverage Protocol**: `0x8A884650222b731058445597cd403E730bF401B5`
- **Truth Engine**: `0x29b676B5254386C5437A1fdDe383f6B1DC0Dd068`

## Usage Examples

### Adding Liquidity

```javascript
const router = await ethers.getContractAt("UniswapV2Router02Slim", ROUTER_ADDRESS);
const tokenA = await ethers.getContractAt("IERC20", TOKEN_A_ADDRESS);
const tokenB = await ethers.getContractAt("IERC20", TOKEN_B_ADDRESS);

// Approve tokens
await tokenA.approve(ROUTER_ADDRESS, amountADesired);
await tokenB.approve(ROUTER_ADDRESS, amountBDesired);

// Add liquidity
await router.addLiquidity(
  TOKEN_A_ADDRESS,
  TOKEN_B_ADDRESS,
  amountADesired,
  amountBDesired,
  amountAMin,
  amountBMin,
  yourAddress,
  deadline
);
```

### Swapping Tokens

```javascript
// Approve input token
await tokenIn.approve(ROUTER_ADDRESS, amountIn);

// Perform swap
await router.swapExactTokensForTokens(
  amountIn,
  amountOutMin,
  [TOKEN_IN_ADDRESS, TOKEN_OUT_ADDRESS],
  yourAddress,
  deadline
);
```

### Working with Native ETH

Since ETH functions are removed, you must wrap ETH to WETH first:

```javascript
const weth = await ethers.getContractAt("IWETH", WETH_ADDRESS);

// Wrap ETH to WETH
await weth.deposit({ value: ethAmount });

// Now use WETH in router calls
await weth.approve(ROUTER_ADDRESS, ethAmount);
await router.swapExactTokensForTokens(...);
```

## Troubleshooting

### Bytecode Size Issues

If the bytecode exceeds 24KB:
1. Ensure `viaIR: true` is set in `hardhat.config.cjs`
2. Verify `optimizer.runs: 1` is set
3. Check that you're compiling with Solidity 0.8.19

### Transaction Failures

Common issues:
- **Expired deadline**: Ensure deadline is in the future (Unix timestamp in seconds)
- **Insufficient allowance**: Approve tokens before calling router functions
- **Slippage**: Increase slippage tolerance by adjusting min/max amounts

### Network Connection Issues

- Verify RPC URL is correct for your target network
- Check that your wallet has sufficient 0G tokens for gas
- Ensure ChainID matches the network (42069 testnet, 16661 mainnet)

## Testing

Run the test suite:

```bash
npx hardhat test
```

Tests validate:
- ✅ Bytecode size < 24KB
- ✅ Add liquidity functionality
- ✅ Remove liquidity functionality
- ✅ Swap exact tokens for tokens
- ✅ Integration with Factory

## Security Considerations

1. **Audits**: This slim router removes safety features for size optimization
2. **ETH Handling**: Users must wrap/unwrap ETH manually
3. **Slippage**: Always set appropriate minimum/maximum amounts
4. **Deadlines**: Use reasonable deadlines to prevent transaction delays
5. **Approvals**: Only approve exact amounts needed, not unlimited

## Next Steps

After successful deployment:

1. ✅ Verify contract on 0G block explorer
2. ✅ Create OINIO/0G trading pair via Factory
3. ✅ Update Forge UI with new router address
4. ✅ Add liquidity to initial pairs
5. ✅ Test swap functionality with small amounts
6. ✅ Announce router availability to community

## Support

For issues or questions:
- GitHub Issues: [pi-forge-quantum-genesis](https://github.com/onenoly1010/pi-forge-quantum-genesis)
- Documentation: `/docs` directory
- Community: Check project README for community channels

---

**Last Updated**: 2025-12-31  
**Version**: 1.0.0  
**Network**: 0G Aristotle Mainnet
