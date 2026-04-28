// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@uniswap/v3-periphery/contracts/interfaces/ISwapRouter.sol";

/**
 * @title ZeroGV3RouterWrapper
 * @author Quantum Pi Forge Sovereign System
 * @notice Secure multi-chain Uniswap V3 Router wrapper with full security hardening
 * @dev Mirrors ZeroGRouterWrapper V2 pattern for consistent security architecture
 */
contract ZeroGV3RouterWrapper is Ownable, ReentrancyGuard {

    // Multi-chain V3 Router mapping: chainId => SwapRouter address
    mapping(uint256 => address) public v3Routers;

    // Events
    event V3RouterUpdated(uint256 indexed chainId, address indexed router);
    event V3SwapExecuted(uint256 indexed chainId, address tokenIn, address tokenOut, uint256 amountIn, uint256 amountOut);

    error InvalidRouterAddress();
    error RouterNotConfiguredForChain();
    error ZeroAddress();
    error ZeroAmount();
    error DeadlineExpired();
    error InsufficientOutputAmount();

    constructor() {
        // Initialize with known official router deployments
        // Ethereum Mainnet
        v3Routers[1] = 0xE592427A0AEce92De3Edee1F18E0157C05861564;
        // Base
        v3Routers[8453] = 0xE592427A0AEce92De3Edee1F18E0157C05861564;
        // Arbitrum One
        v3Routers[42161] = 0xE592427A0AEce92De3Edee1F18E0157C05861564;
        // Optimism
        v3Routers[10] = 0xE592427A0AEce92De3Edee1F18E0157C05861564;
        // Polygon
        v3Routers[137] = 0xE592427A0AEce92De3Edee1F18E0157C05861564;
    }

    /**
     * @notice Set V3 Router address for a specific chain
     * @dev Only callable by owner, performs full contract validation
     */
    function setV3Router(uint256 chainId, address router) external onlyOwner {
        if (router == address(0)) revert ZeroAddress();
        if (router.code.length == 0) revert InvalidRouterAddress();

        v3Routers[chainId] = router;
        emit V3RouterUpdated(chainId, router);
    }

    /**
     * @notice Get active router for current chain
     */
    function getActiveRouter() public view returns (ISwapRouter) {
        address router = v3Routers[block.chainid];
        if (router == address(0)) revert RouterNotConfiguredForChain();
        return ISwapRouter(router);
    }

    /**
     * @notice Execute single hop exact input swap on V3
     * @dev Full security checks, CEI pattern, reentrancy protected
     */
    function exactInputSingle(
        address tokenIn,
        address tokenOut,
        uint24 fee,
        uint256 amountIn,
        uint256 amountOutMinimum,
        uint256 deadline,
        uint160 sqrtPriceLimitX96
    ) external nonReentrant returns (uint256 amountOut) {
        // Pre-checks
        if (tokenIn == address(0) || tokenOut == address(0)) revert ZeroAddress();
        if (amountIn == 0) revert ZeroAmount();
        if (block.timestamp > deadline) revert DeadlineExpired();

        ISwapRouter router = getActiveRouter();

        // Transfer tokens from caller
        TransferHelper.safeTransferFrom(tokenIn, msg.sender, address(this), amountIn);
        TransferHelper.safeApprove(tokenIn, address(router), amountIn);

        // Execute swap
        ISwapRouter.ExactInputSingleParams memory params = ISwapRouter.ExactInputSingleParams({
            tokenIn: tokenIn,
            tokenOut: tokenOut,
            fee: fee,
            recipient: msg.sender,
            deadline: deadline,
            amountIn: amountIn,
            amountOutMinimum: amountOutMinimum,
            sqrtPriceLimitX96: sqrtPriceLimitX96
        });

        amountOut = router.exactInputSingle(params);

        if (amountOut < amountOutMinimum) revert InsufficientOutputAmount();

        emit V3SwapExecuted(block.chainid, tokenIn, tokenOut, amountIn, amountOut);
    }
}

library TransferHelper {
    function safeApprove(address token, address to, uint value) internal {
        (bool success, bytes memory data) = token.call(abi.encodeWithSelector(0x095ea7b3, to, value));
        require(success && (data.length == 0 || abi.decode(data, (bool))), 'APPROVE_FAILED');
    }

    function safeTransferFrom(address token, address from, address to, uint value) internal {
        (bool success, bytes memory data) = token.call(abi.encodeWithSelector(0x23b872dd, from, to, value));
        require(success && (data.length == 0 || abi.decode(data, (bool))), 'TRANSFER_FROM_FAILED');
    }
}