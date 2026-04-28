// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import {ReentrancyGuard} from "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
// TickMath constants inline (avoids external dependency)
library TickMath {
    int24 internal constant MIN_TICK = -887272;
    int24 internal constant MAX_TICK = -MIN_TICK;
}

/// @dev Uniswap V3 SwapRouter Interface (minimal)
interface ISwapRouter {
    struct ExactInputSingleParams {
        address tokenIn;
        address tokenOut;
        uint24 fee;
        address recipient;
        uint256 deadline;
        uint256 amountIn;
        uint256 amountOutMinimum;
        uint160 sqrtPriceLimitX96;
    }

    function exactInputSingle(ExactInputSingleParams calldata params) external payable returns (uint256 amountOut);
}

/// @dev NonfungiblePositionManager Interface (minimal)
interface INonfungiblePositionManager {
    struct MintParams {
        address token0;
        address token1;
        uint24 fee;
        int24 tickLower;
        int24 tickUpper;
        uint256 amount0Desired;
        uint256 amount1Desired;
        uint256 amount0Min;
        uint256 amount1Min;
        address recipient;
        uint256 deadline;
    }

    function mint(MintParams calldata params) external payable returns (
        uint256 tokenId,
        uint128 liquidity,
        uint256 amount0,
        uint256 amount1
    );

    function collect(
        uint256 tokenId,
        address recipient,
        uint128 amount0Max,
        uint128 amount1Max
    ) external returns (uint256 amount0, uint256 amount1);

    function decreaseLiquidity(
        uint256 tokenId,
        uint128 liquidity,
        uint256 amount0Min,
        uint256 amount1Min,
        uint256 deadline
    ) external returns (uint256 amount0, uint256 amount1);
}

/// @title ZeroGV3RouterWrapper - Sovereign Uniswap V3 Integration for W0G
/// @notice Hardened multi-chain V3 router wrapper with full security parity
/// @dev Maintains backwards compatibility with V2 architecture patterns
contract ZeroGV3RouterWrapper is ReentrancyGuard {
    using SafeERC20 for IERC20;

    /// @dev Uniswap V3 Router Address Mapping
    mapping(uint256 => address) public swapRouterByChain;
    mapping(uint256 => address) public swapRouter02ByChain;
    mapping(uint256 => address) public positionManagerByChain;
    mapping(uint256 => address) public quoterByChain;

    /// @dev Default Fallback Addresses (verified multi-chain deployments)
    address public constant DEFAULT_SWAP_ROUTER = 0xE592427A0AEce92De3Edee1F18E0157C05861564;
    address public constant DEFAULT_SWAP_ROUTER_02 = 0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45;
    address public constant DEFAULT_POSITION_MANAGER = 0xC36442b4a4522E871399CD717aBDD847Ab11FE88;
    address public constant DEFAULT_QUOTER = 0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6;
    address public constant UNIVERSAL_ROUTER = 0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD;

    /// @dev Fee Tier Constants
    uint24 public constant FEE_LOWEST = 500;   // 0.05%
    uint24 public constant FEE_STANDARD = 3000; // 0.3%
    uint24 public constant FEE_HIGH = 10000;   // 1%

    error ZeroAmount();
    error InsufficientOutput();
    error DeadlineExpired();
    error InvalidSlippage();
    error InvalidTickRange();
    error TickRangeTooNarrow();
    error InvalidTickSpacing();

    event V3SwapExecuted(
        address indexed tokenIn,
        address indexed tokenOut,
        uint256 amountIn,
        uint256 amountOut,
        uint24 fee,
        uint256 chainId
    );

    constructor() {
        // Initialize common chain mappings
        // Ethereum Mainnet
        swapRouterByChain[1] = DEFAULT_SWAP_ROUTER;
        swapRouter02ByChain[1] = DEFAULT_SWAP_ROUTER_02;
        positionManagerByChain[1] = DEFAULT_POSITION_MANAGER;
        quoterByChain[1] = DEFAULT_QUOTER;

        // Arbitrum
        swapRouterByChain[42161] = DEFAULT_SWAP_ROUTER;
        swapRouter02ByChain[42161] = DEFAULT_SWAP_ROUTER_02;
        positionManagerByChain[42161] = DEFAULT_POSITION_MANAGER;
        quoterByChain[42161] = DEFAULT_QUOTER;

        // Optimism
        swapRouterByChain[10] = DEFAULT_SWAP_ROUTER;
        swapRouter02ByChain[10] = DEFAULT_SWAP_ROUTER_02;
        positionManagerByChain[10] = DEFAULT_POSITION_MANAGER;
        quoterByChain[10] = DEFAULT_QUOTER;

        // Base
        swapRouterByChain[8453] = DEFAULT_SWAP_ROUTER;
        swapRouter02ByChain[8453] = DEFAULT_SWAP_ROUTER_02;
        positionManagerByChain[8453] = DEFAULT_POSITION_MANAGER;
        quoterByChain[8453] = DEFAULT_QUOTER;

        // Polygon
        swapRouterByChain[137] = DEFAULT_SWAP_ROUTER;
        swapRouter02ByChain[137] = DEFAULT_SWAP_ROUTER_02;
        positionManagerByChain[137] = DEFAULT_POSITION_MANAGER;
        quoterByChain[137] = DEFAULT_QUOTER;
    }

    /// @notice Execute exact input single hop swap on Uniswap V3
    /// @dev Fully hardened with CEI, reentrancy protection, zero checks
    function exactInputSingle(
        address tokenIn,
        address tokenOut,
        uint24 fee,
        uint256 amountIn,
        uint256 amountOutMinimum,
        uint256 deadline,
        uint160 sqrtPriceLimitX96
    ) external nonReentrant returns (uint256 amountOut) {
        if (amountIn == 0) revert ZeroAmount();
        if (amountOutMinimum == 0) revert InvalidSlippage();
        if (block.timestamp > deadline) revert DeadlineExpired();

        uint256 chainId = block.chainid;
        address router = getSwapRouter(chainId);

        // Transfer tokens from caller (CEI pattern - pull first)
        IERC20(tokenIn).safeTransferFrom(msg.sender, address(this), amountIn);

        // Approve router
        IERC20(tokenIn).forceApprove(router, amountIn);

        // Execute swap
        amountOut = ISwapRouter(router).exactInputSingle(
            ISwapRouter.ExactInputSingleParams({
                tokenIn: tokenIn,
                tokenOut: tokenOut,
                fee: fee,
                recipient: msg.sender,
                deadline: deadline,
                amountIn: amountIn,
                amountOutMinimum: amountOutMinimum,
                sqrtPriceLimitX96: sqrtPriceLimitX96
            })
        );

        if (amountOut < amountOutMinimum) revert InsufficientOutput();

        emit V3SwapExecuted(tokenIn, tokenOut, amountIn, amountOut, fee, chainId);
    }

    /// @dev Get appropriate SwapRouter for current chain with fallback
    function getSwapRouter(uint256 chainId) public view returns (address) {
        address router = swapRouter02ByChain[chainId];
        if (router != address(0)) return router;
        
        router = swapRouterByChain[chainId];
        if (router != address(0)) return router;
        
        return DEFAULT_SWAP_ROUTER_02;
    }

    /// @dev Get NonfungiblePositionManager address
    function getPositionManager(uint256 chainId) public view returns (address) {
        address manager = positionManagerByChain[chainId];
        return manager != address(0) ? manager : DEFAULT_POSITION_MANAGER;
    }

    /// @dev Get Quoter address
    function getQuoter(uint256 chainId) public view returns (address) {
        address quoter = quoterByChain[chainId];
        return quoter != address(0) ? quoter : DEFAULT_QUOTER;
    }

    /// @dev Get tick spacing for given fee tier
    function getTickSpacing(uint24 fee) public pure returns (uint24 tickSpacing) {
        if (fee == FEE_LOWEST) return 10;
        if (fee == FEE_STANDARD) return 60;
        if (fee == FEE_HIGH) return 200;
        revert InvalidTickSpacing();
    }

    /// @dev Returns the nearest tick that is a multiple of tickSpacing and within valid bounds
    function nearestUsableTick(int24 tick_, uint24 tickSpacing) internal pure returns (int24 result) {
        result = int24((int256(tick_) / int256(uint256(tickSpacing))) * int256(uint256(tickSpacing)));
        
        if (result < TickMath.MIN_TICK) {
            result += int24(tickSpacing);
        } else if (result > TickMath.MAX_TICK) {
            result -= int24(tickSpacing);
        }

        return result;
    }


    event LiquidityMinted(
        uint256 indexed tokenId,
        address indexed token0,
        address indexed token1,
        uint24 fee,
        uint128 liquidity,
        uint256 amount0,
        uint256 amount1,
        uint256 chainId
    );

    event FeesCollected(
        uint256 indexed tokenId,
        uint256 amount0,
        uint256 amount1
    );

    event PositionRebalanced(
        uint256 indexed tokenId,
        uint256 indexed newTokenId,
        int24 oldTickLower,
        int24 oldTickUpper,
        int24 newTickLower,
        int24 newTickUpper,
        uint128 liquidity,
        uint256 volatility
    );

    /// @notice Mint concentrated liquidity position on Uniswap V3
    /// @dev Hardened implementation with CEI, slippage protection, deadline enforcement
    function mintPosition(
        address token0,
        address token1,
        uint24 fee,
        int24 tickLower,
        int24 tickUpper,
        uint256 amount0Desired,
        uint256 amount1Desired,
        uint256 amount0Min,
        uint256 amount1Min,
        address recipient,
        uint256 deadline
    ) external virtual nonReentrant returns (
        uint256 tokenId,
        uint128 liquidity,
        uint256 amount0,
        uint256 amount1
    ) {
        if (amount0Desired == 0 && amount1Desired == 0) revert ZeroAmount();
        if (block.timestamp > deadline) revert DeadlineExpired();

        uint256 chainId = block.chainid;
        address positionManager = getPositionManager(chainId);

        // Tick spacing validation and alignment
        uint24 tickSpacing = getTickSpacing(fee);
        
        // Align ticks to nearest valid tick spacing boundaries
        tickLower = nearestUsableTick(tickLower, tickSpacing);
        tickUpper = nearestUsableTick(tickUpper, tickSpacing);

        // Enforce valid tick range constraints
        int24 tickSpacingInt = int24(int256(uint256(tickSpacing)));

        if (tickLower >= tickUpper) revert InvalidTickRange();
        if ((tickUpper - tickLower) < tickSpacingInt) revert TickRangeTooNarrow();
        if (tickLower % tickSpacingInt != 0 || tickUpper % tickSpacingInt != 0) revert InvalidTickSpacing();

        // Pull tokens from caller first (CEI pattern)
        if (amount0Desired > 0) {
            IERC20(token0).safeTransferFrom(msg.sender, address(this), amount0Desired);
            IERC20(token0).forceApprove(positionManager, amount0Desired);
        }

        if (amount1Desired > 0) {
            IERC20(token1).safeTransferFrom(msg.sender, address(this), amount1Desired);
            IERC20(token1).forceApprove(positionManager, amount1Desired);
        }

        // Mint concentrated liquidity position
        (tokenId, liquidity, amount0, amount1) = INonfungiblePositionManager(positionManager).mint(
            INonfungiblePositionManager.MintParams({
                token0: token0,
                token1: token1,
                fee: fee,
                tickLower: tickLower,
                tickUpper: tickUpper,
                amount0Desired: amount0Desired,
                amount1Desired: amount1Desired,
                amount0Min: amount0Min,
                amount1Min: amount1Min,
                recipient: recipient,
                deadline: deadline
            })
        );

        // Refund unused tokens
        if (amount0Desired > amount0) {
            IERC20(token0).safeTransfer(msg.sender, amount0Desired - amount0);
        }

        if (amount1Desired > amount1) {
            IERC20(token1).safeTransfer(msg.sender, amount1Desired - amount1);
        }

        emit LiquidityMinted(tokenId, token0, token1, fee, liquidity, amount0, amount1, chainId);
    }

    /// @notice Collect accumulated fees from V3 position
    function collectFees(
        uint256 tokenId,
        address recipient,
        uint128 amount0Max,
        uint128 amount1Max
    ) external virtual nonReentrant returns (uint256 amount0, uint256 amount1) {
        uint256 chainId = block.chainid;
        address positionManager = getPositionManager(chainId);

        (amount0, amount1) = INonfungiblePositionManager(positionManager).collect(
            tokenId,
            recipient,
            amount0Max,
            amount1Max
        );

        emit FeesCollected(tokenId, amount0, amount1);
    }
}
