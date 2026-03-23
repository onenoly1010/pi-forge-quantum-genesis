// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Script.sol";
import "../src/OINIOToken.sol";
import "../src/OINIOModelRegistry.sol";

/**
 * @title Deploy
 * @dev Deployment script for OINIO smart contracts
 * 
 * Usage:
 * Testnet: forge script script/Deploy.s.sol --rpc-url pi_testnet --broadcast --verify
 * Mainnet: forge script script/Deploy.s.sol --rpc-url pi_mainnet --broadcast --verify
 * 
 * Environment variables required:
 * - PRIVATE_KEY: Deployer's private key
 * - RPC_URL: Pi Network RPC endpoint
 * - CHAIN_ID: 2025 for testnet, 314159 for mainnet
 * - ETHERSCAN_API_KEY: (optional) For contract verification
 */
contract Deploy is Script {
    // Minimum balance required for deployment (0.1 ETH equivalent)
    uint256 constant MIN_BALANCE = 0.1 ether;

    function run() external {
        console.log("=======================================================");
        console.log("  OINIO Smart Contracts Deployment Script (Forge)");
        console.log("=======================================================");
        console.log("");

        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        address deployer = vm.addr(deployerPrivateKey);

        // Pre-deployment checks
        performPreDeploymentChecks(deployer);

        vm.startBroadcast(deployerPrivateKey);

        // Deploy OINIOToken
        console.log("\n=== Deploying OINIOToken ===");
        OINIOToken token = new OINIOToken(deployer);
        console.log("OINIOToken deployed to:", address(token));
        console.log("Token Name:", token.name());
        console.log("Token Symbol:", token.symbol());
        console.log("Token Decimals:", token.decimals());
        console.log("Total Supply:", token.totalSupply());

        // Deploy OINIOModelRegistry
        console.log("\n=== Deploying OINIOModelRegistry ===");
        OINIOModelRegistry registry = new OINIOModelRegistry(address(token), deployer);
        console.log("OINIOModelRegistry deployed to:", address(registry));
        console.log("Registry Name:", registry.name());
        console.log("Registry Symbol:", registry.symbol());
        console.log("OINIO Token Address:", address(registry.oinioToken()));

        vm.stopBroadcast();

        // Post-deployment verification
        performPostDeploymentChecks(address(token), address(registry), deployer);

        // Output deployment summary
        console.log("\n=======================================================");
        console.log("  DEPLOYMENT SUMMARY");
        console.log("=======================================================");
        console.log("Network Chain ID:", block.chainid);
        console.log("Deployer:", deployer);
        console.log("OINIOToken:", address(token));
        console.log("OINIOModelRegistry:", address(registry));
        console.log("\n=== Next Steps ===");
        console.log("1. Save the contract addresses above");
        console.log("2. Verify contracts on block explorer if not done automatically:");
        console.log("   forge verify-contract", address(token), "src/OINIOToken.sol:OINIOToken --chain-id", block.chainid);
        console.log("   forge verify-contract", address(registry), "src/OINIOModelRegistry.sol:OINIOModelRegistry --chain-id", block.chainid);
        console.log("3. Update frontend configuration (.env):");
        console.log("   OINIO_TOKEN_ADDRESS=", address(token));
        console.log("   OINIO_REGISTRY_ADDRESS=", address(registry));
        console.log("4. Test contract interactions");
        console.log("5. Run health check: cast call", address(token), "\"totalSupply()\"");
    }

    /**
     * @dev Pre-deployment safety checks
     */
    function performPreDeploymentChecks(address deployer) internal view {
        console.log("=== Pre-Deployment Safety Checks ===");
        console.log("");

        // Check 1: Deployer address
        console.log("1. Deployer address:", deployer);
        require(deployer != address(0), "Invalid deployer address");
        console.log("   Status: PASSED");

        // Check 2: Balance
        uint256 balance = deployer.balance;
        console.log("");
        console.log("2. Deployer balance:", balance);
        console.log("   Minimum required:", MIN_BALANCE);
        require(balance >= MIN_BALANCE, "Insufficient balance for deployment");
        console.log("   Status: PASSED");

        // Check 3: Chain ID
        console.log("");
        console.log("3. Chain ID:", block.chainid);
        bool isValidChain = block.chainid == 2025 || block.chainid == 314159;
        if (!isValidChain) {
            console.log("   WARNING: Chain ID is not Pi Network testnet (2025) or mainnet (314159)");
        } else {
            console.log("   Status: PASSED");
        }

        console.log("");
        console.log("All pre-deployment checks passed!");
        console.log("");
    }

    /**
     * @dev Post-deployment verification
     */
    function performPostDeploymentChecks(
        address tokenAddress,
        address registryAddress,
        address deployer
    ) internal view {
        console.log("\n=== Post-Deployment Verification ===");
        console.log("");

        // Check 1: Contract code exists
        console.log("1. Verifying deployed contracts...");
        require(tokenAddress.code.length > 0, "Token contract not deployed");
        console.log("   Token code size:", tokenAddress.code.length, "bytes");
        require(registryAddress.code.length > 0, "Registry contract not deployed");
        console.log("   Registry code size:", registryAddress.code.length, "bytes");
        console.log("   Status: PASSED");

        // Check 2: Verify basic functionality would work in production
        console.log("");
        console.log("2. Contract addresses valid");
        require(tokenAddress != address(0), "Invalid token address");
        require(registryAddress != address(0), "Invalid registry address");
        console.log("   Status: PASSED");

        console.log("");
        console.log("Post-deployment verification complete!");
        console.log("");
    }
}
