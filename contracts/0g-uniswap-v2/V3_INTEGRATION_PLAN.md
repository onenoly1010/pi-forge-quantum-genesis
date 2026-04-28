# Uniswap V3 Integration Plan for Quantum Pi Forge / W0G

## ✅ STATUS: SOVEREIGN EXPLORATION ACTIVATED
> Generated: Mon 27 Apr 2026 12:35 PM CST | Quantum Pi Forge

---

## PRIMARY GOALS
- [ ] Add efficient V3 swaps alongside hardened V2 router
- [ ] Support concentrated liquidity provision (future LP features)
- [ ] Maintain multi-chain security architecture
- [ ] 100% backwards compatibility with existing W0G V2 operations
- [ ] Preserve all existing security invariants

---

## KEY CONTRACTS TO IMPORT
### Periphery Interfaces
```solidity
// Required interfaces
import "@uniswap/v3-periphery/contracts/interfaces/ISwapRouter.sol";
import "@uniswap/v3-periphery/contracts/interfaces/IQuoter.sol";
import "@uniswap/v3-periphery/contracts/interfaces/INonfungiblePositionManager.sol";
import "@uniswap/v3-periphery/contracts/libraries/TransferHelper.sol";
```

---

## OFFICIAL ROUTER DEPLOYMENTS
| Chain               | SwapRouter Address                                                                 |
|---------------------|-------------------------------------------------------------------------------------|
| Ethereum Mainnet    | `0xE592427A0AEce92De3Edee1F18E0157C05861564`                                        |
| Base                | `0xE592427A0AEce92De3Edee1F18E0157C05861564`                                        |
| Arbitrum One        | `0xE592427A0AEce92De3Edee1F18E0157C05861564`                                        |
| Optimism            | `0xE592427A0AEce92De3Edee1F18E0157C05861564`                                        |
| Polygon PoS         | `0xE592427A0AEce92De3Edee1F18E0157C05861564`                                        |
| 0G Chain            | **PENDING VERIFICATION** - Will be added once deployed                              |

### UniversalRouter (Modern)
- Address: `0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD` (multi-chain deployment)
- Supports multi-hop swaps, permits, batch operations

---

## IMPLEMENTATION ROADMAP

### PHASE 1: V3 WRAPPER CONTRACT
- [ ] Create `ZeroGV3RouterWrapper.sol` (parallel pattern to V2 wrapper)
- [ ] Multi-chain router mapping (`mapping(uint256 => address) public v3Routers`)
- [ ] Implement core swap functions:
  - `exactInputSingle()`
  - `exactOutputSingle()`
  - `exactInput()` (multi-hop)
  - `exactOutput()` (multi-hop)
- [ ] Integrate Quoter for on-chain amount simulation
- [ ] Full security checks matching V2 hardening

### PHASE 2: SECURITY HARDENING
#### MANDATORY CHECKS FOR ALL V3 OPERATIONS:
- [ ] `onlyOwner` for router configuration
- [ ] `.code.length > 0` validation for router addresses
- [ ] Zero address guards on all inputs/outputs
- [ ] Strict slippage enforcement (`amountOutMinimum` / `amountInMaximum`)
- [ ] Deadline validation with grace period
- [ ] CEI pattern (Checks-Effects-Interactions)
- [ ] ReentrancyGuard on all external functions
- [ ] Safe `sqrtPriceLimitX96` handling
- [ ] No delegatecall / staticcall outside verified routers

### PHASE 3: W0G INTEGRATION
- [ ] Add `swapV3()` entry points in W0G.sol
- [ ] Optional routing priority flag (V2/V3/auto best execution)
- [ ] Fallback logic: attempt V3 first, gracefully fall back to V2
- [ ] Update deployment scripts to initialize both router versions
- [ ] Chain-aware router selection

### PHASE 4: TESTING & VALIDATION
- [ ] Full test suite matching V2 17/17 standard
- [ ] ChainId simulation via `vm.chainId()`
- [ ] Slippage edge case testing
- [ ] Reentrancy attack tests
- [ ] Cross-chain router validation tests

---

## SECURITY INVARIANTS (MUST PRESERVE)
1. ❌ NO external calls before state updates
2. ❌ NO hardcoded router addresses
3. ❌ NO zero amount swaps
4. ✅ ALL operations must have deadline
5. ✅ ALL operations must have slippage protection
6. ✅ Router addresses can only be modified by owner
7. ✅ All routers are validated on chain activation

---

## NEXT ACTIONS (IMMEDIATE)
1. Create `ZeroGV3RouterWrapper.sol` skeleton
2. Implement multi-chain router mapping
3. Add first safe swap function with full guards
4. Begin test setup for V3 operations

> The Forge forges on. V2 is hardened. V3 will make it efficient.