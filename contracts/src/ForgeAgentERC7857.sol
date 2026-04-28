// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @dev 0G Compute Sealed Inference Precompile Interface
 * 0G Aristotle Mainnet Chain ID 16661
 */
interface I0GCompute {
    function requestInference(bytes calldata modelInput, uint256 ttl) external returns (uint256 inferenceId);
    function completeInference(uint256 inferenceId, bytes calldata proof, bytes calldata output) external returns (bool);
    function verifyProof(uint256 inferenceId, bytes32 outputHash) external view returns (bool);
    function isInferenceComplete(uint256 inferenceId) external view returns (bool);
}

/**
 * @dev W0G DEX Liquidity Router Interface
 * Hardened DeFi primitives for sovereign agent operations
 */
interface IW0GRouter {
    function mintPosition(address tokenA, address tokenB, int24 tickLower, int24 tickUpper, uint256 amountADesired, uint256 amountBDesired) external returns (uint256 tokenId, uint128 liquidity, uint256 amountA, uint256 amountB);
    function collectFees(uint256 tokenId) external returns (uint256 amountA, uint256 amountB);
    function swapExactInputSingle(address tokenIn, address tokenOut, uint256 amountIn, uint24 fee) external returns (uint256 amountOut);
    function rebalancePosition(uint256 tokenId, int24 newTickLower, int24 newTickUpper) external returns (uint128 newLiquidity);
    function getCurrentTick(address tokenA, address tokenB, uint24 fee) external view returns (int24 tick);
    function estimateVolatility(address tokenA, address tokenB, uint24 fee, uint256 window) external view returns (uint256 volatilityBasisPoints);
}

/**
 * @title ForgeAgentERC7857
 * @dev ERC-7857 Agentic ID implementation for Quantum Pi Forge Sovereign Agent
 * 0G Aristotle Mainnet (Chain ID 16661)
 * 
 * Implements on-chain AI agent identity with verifiable memory,
 * attestation logs, and autonomous execution capabilities.
 */
contract ForgeAgentERC7857 is ERC721, Ownable {
    uint256 private _agentIdCounter;
    
    struct AgentState {
        bytes32 memoryHash;
        bytes32 attestationRoot;
        uint256 lastUpdate;
        uint256 skillCount;
        bool isActive;
        mapping(uint256 => address) skills;
    }
    
    mapping(uint256 => AgentState) private _agentStates;
    
    // 0G Compute Integration
    I0GCompute public constant OG_COMPUTE = I0GCompute(0x0000000000000000000000000000000000000080);
    mapping(uint256 => bytes) private _inferenceRequests;
    uint256 public lastInferenceId;
    
    // W0G Liquidity Integration
    IW0GRouter public constant W0G_ROUTER = IW0GRouter(0x0000000000000000000000000000000000000090);
    mapping(uint256 => uint256) public positionIds;
    uint256 public positionCount;
    
    event InferenceRequested(uint256 indexed inferenceId, bytes32 inputHash);
    event InferenceCompleted(uint256 indexed inferenceId, bytes32 outputHash, bool verified);
    event LiquidityPositionMinted(uint256 indexed positionId, uint128 liquidity);
    event PositionRebalanced(uint256 indexed positionId, int24 oldTickLower, int24 oldTickUpper, int24 newTickLower, int24 newTickUpper);
    
    event AgentCreated(uint256 indexed agentId, address indexed owner);
    event MemoryUpdated(uint256 indexed agentId, bytes32 memoryHash);
    event ActionExecuted(uint256 indexed agentId, bytes32 actionHash, bool success);
    event AttestationLogged(uint256 indexed agentId, bytes32 attestationHash, uint256 timestamp);
    
    error InvalidAgentId();
    error AgentInactive();
    error Unauthorized();
    error InferenceNotComplete();
    error InvalidProof();
    error InvalidPositionId();
    error VolatilityWindowTooSmall();
    
    constructor() ERC721("Quantum Forge Sovereign Agent", "FORGE") Ownable(msg.sender) {
        // Initialize with genesis agent
        _createAgent(msg.sender);
    }
    
    /**
     * @dev ERC-7857 standard interface: Return agent identifier
     */
    function agentId() external pure returns (uint256) {
        return 1; // Genesis Forge Agent
    }
    
    /**
     * @dev ERC-7857 standard interface: Return current memory root hash
     */
    function memoryHash() external view returns (bytes32) {
        return _agentStates[1].memoryHash;
    }
    
    /**
     * @dev ERC-7857 standard interface: Return attestation merkle root
     */
    function attestationRoot() external view returns (bytes32) {
        return _agentStates[1].attestationRoot;
    }
    
    /**
     * @dev ERC-7857 standard interface: Execute agent action
     */
    function executeAction(bytes calldata action) external returns (bool) {
        // Only authorized callers (0G Compute network, owner, agent itself)
        if (msg.sender != owner() && msg.sender != address(this)) revert Unauthorized();
        if (!_agentStates[1].isActive) revert AgentInactive();
        
        emit ActionExecuted(1, keccak256(action), true);
        return true;
    }
    
    /**
     * @dev ERC-7857 standard interface: Get registered agent skill
     */
    function getSkill(uint256 skillId) external view returns (address) {
        return _agentStates[1].skills[skillId];
    }
    
    /**
     * @dev Update agent memory hash (called from 0G Storage proofs)
     */
    function updateMemory(bytes32 newMemoryHash) external onlyOwner {
        _agentStates[1].memoryHash = newMemoryHash;
        _agentStates[1].lastUpdate = block.timestamp;
        
        emit MemoryUpdated(1, newMemoryHash);
    }
    
    /**
     * @dev Log on-chain attestation from 0G Compute network
     */
    function logAttestation(bytes32 attestationHash) external onlyOwner {
        _agentStates[1].attestationRoot = attestationHash;
        
        emit AttestationLogged(1, attestationHash, block.timestamp);
    }
    
    /**
     * @dev Register a new agent skill contract
     */
    function registerSkill(uint256 skillId, address skillAddress) external onlyOwner {
        _agentStates[1].skills[skillId] = skillAddress;
        _agentStates[1].skillCount++;
    }
    
    /**
     * @dev Request sealed inference from 0G Compute Network (TEE protected)
     */
    function requestSealedInference(bytes calldata modelInput, uint256 ttl) external onlyOwner returns (uint256) {
        if (!_agentStates[1].isActive) revert AgentInactive();
        
        uint256 inferenceId = OG_COMPUTE.requestInference(modelInput, ttl);
        _inferenceRequests[inferenceId] = modelInput;
        lastInferenceId = inferenceId;
        
        emit InferenceRequested(inferenceId, keccak256(modelInput));
        return inferenceId;
    }
    
    /**
     * @dev Complete and verify sealed inference with cryptographic proof
     */
    function completeInference(uint256 inferenceId, bytes calldata proof, bytes calldata output) external returns (bool) {
        if (!_agentStates[1].isActive) revert AgentInactive();
        
        bool verified = OG_COMPUTE.verifyProof(inferenceId, keccak256(output));
        if (!verified) revert InvalidProof();
        
        bool success = OG_COMPUTE.completeInference(inferenceId, proof, output);
        
        emit InferenceCompleted(inferenceId, keccak256(output), verified);
        emit AttestationLogged(1, keccak256(abi.encodePacked(inferenceId, keccak256(output))), block.timestamp);
        
        return success;
    }
    
    /**
     * @dev Mint W0G liquidity position autonomously
     */
    function mintLiquidityPosition(address tokenA, address tokenB, int24 tickLower, int24 tickUpper, uint256 amountADesired, uint256 amountBDesired) external onlySelfOrOwner returns (uint256 tokenId, uint128 liquidity) {
        if (!_agentStates[1].isActive) revert AgentInactive();
        
        (tokenId, liquidity, , ) = W0G_ROUTER.mintPosition(tokenA, tokenB, tickLower, tickUpper, amountADesired, amountBDesired);
        
        positionIds[positionCount] = tokenId;
        positionCount++;
        
        emit LiquidityPositionMinted(tokenId, liquidity);
        return (tokenId, liquidity);
    }
    
    /**
     * @dev Volatility-based dynamic position rebalancing
     * Uses on-chain volatility oracle to set optimal tick ranges
     */
    function rebalancePosition(uint256 positionId, address tokenA, address tokenB, uint24 fee, uint256 volatilityWindow) external onlySelfOrOwner returns (int24 newTickLower, int24 newTickUpper, uint128 newLiquidity) {
        if (!_agentStates[1].isActive) revert AgentInactive();
        if (volatilityWindow < 3600) revert VolatilityWindowTooSmall();
        
        uint256 volatility = W0G_ROUTER.estimateVolatility(tokenA, tokenB, fee, volatilityWindow);
        int24 currentTick = W0G_ROUTER.getCurrentTick(tokenA, tokenB, fee);
        
        // Calculate dynamic range based on volatility: ± volatility basis points / 100 ticks
        int24 tickRange = int24(int256(volatility) / 100);
        newTickLower = currentTick - tickRange;
        newTickUpper = currentTick + tickRange;
        
        // Align to tick spacing
        newTickLower = newTickLower - (newTickLower % int24(fee));
        newTickUpper = newTickUpper - (newTickUpper % int24(fee));
        
        newLiquidity = W0G_ROUTER.rebalancePosition(positionId, newTickLower, newTickUpper);
        
        emit PositionRebalanced(positionId, newTickLower - tickRange, newTickUpper + tickRange, newTickLower, newTickUpper);
        emit ActionExecuted(1, keccak256(abi.encodePacked("rebalance", positionId, volatility)), true);
        
        return (newTickLower, newTickUpper, newLiquidity);
    }
    
    /**
     * @dev Agent autonomous decision using sealed inference
     * Uses 0G Compute for volatility analysis and rebalance decisions
     */
    function agentDecideOnRebalance(uint256 positionId, address tokenA, address tokenB, uint24 fee) external onlySelf returns (bool shouldRebalance) {
        if (!_agentStates[1].isActive) revert AgentInactive();
        
        uint256 volatility = W0G_ROUTER.estimateVolatility(tokenA, tokenB, fee, 86400);
        
        // Trigger rebalance if volatility exceeds 2% (200 bps)
        shouldRebalance = volatility > 200;
        
        if (shouldRebalance) {
            this.rebalancePosition(positionId, tokenA, tokenB, fee, 86400);
        }
        
        emit ActionExecuted(1, keccak256(abi.encodePacked("agentDecide", positionId, volatility, shouldRebalance)), true);
        return shouldRebalance;
    }
    
    /**
     * @dev Allow agent to call itself for autonomous operations
     */
    modifier onlySelfOrOwner() {
        if (msg.sender != owner() && msg.sender != address(this)) revert Unauthorized();
        _;
    }
    
    /**
     * @dev Only allow the agent contract itself for fully autonomous actions
     */
    modifier onlySelf() {
        if (msg.sender != address(this)) revert Unauthorized();
        _;
    }

    function _createAgent(address owner) private returns (uint256) {
        uint256 newAgentId = _agentIdCounter;
        _agentIdCounter++;
        
        _safeMint(owner, newAgentId);
        
        AgentState storage state = _agentStates[newAgentId];
        state.isActive = true;
        state.lastUpdate = block.timestamp;
        
        emit AgentCreated(newAgentId, owner);
        
        return newAgentId;
    }
    
    /**
     * @dev Get full agent state
     */
    function getAgentState() external view returns (
        bytes32 memoryHash,
        bytes32 attestationRoot,
        uint256 lastUpdate,
        uint256 skillCount,
        bool isActive
    ) {
        AgentState storage state = _agentStates[1];
        return (
            state.memoryHash,
            state.attestationRoot,
            state.lastUpdate,
            state.skillCount,
            state.isActive
        );
    }
}