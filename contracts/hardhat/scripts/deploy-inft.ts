import { ethers } from "hardhat";
import { checkDeploymentReadiness, verifyDeployment } from "./check-balance";

/**
 * Deploy OINIO iNFT Contracts (OINIOToken + OINIOModelRegistry)
 * 
 * This script deploys the Sovereign iNFT contracts to the configured network.
 * 
 * Usage:
 *   npx hardhat run scripts/deploy-inft.ts --network <network-name>
 * 
 * Networks:
 *   - zeroG: 0G Aristotle Mainnet
 *   - piMainnet: Pi Network Mainnet
 *   - piTestnet: Pi Network Testnet
 * 
 * Environment variables required:
 *   - PRIVATE_KEY: Deployer's private key
 *   - <NETWORK>_RPC: Network RPC URL (optional, uses defaults)
 */
async function main() {
  console.log("╔════════════════════════════════════════════════════════════╗");
  console.log("║   OINIO Sovereign iNFT Deployment Script (Hardhat)        ║");
  console.log("╚════════════════════════════════════════════════════════════╝\n");

  // Get network info
  const network = await ethers.provider.getNetwork();
  const chainId = Number(network.chainId);
  console.log(`Network: ${network.name}`);
  console.log(`Chain ID: ${chainId}\n`);

  // Get deployer
  const [deployer] = await ethers.getSigners();
  console.log("Deployer address:", deployer.address);

  // Pre-deployment checks
  const rpcUrl = 
    chainId === 16661 ? process.env.ZERO_G_RPC || "https://evmrpc.0g.ai" :
    chainId === 314159 ? process.env.PI_MAINNET_RPC || "https://rpc.mainnet.pi.network" :
    chainId === 2025 ? process.env.PI_TESTNET_RPC || "https://api.testnet.minepi.com/rpc" :
    "";

  await checkDeploymentReadiness(rpcUrl, "0.1");

  // Deploy OINIOToken
  console.log("═══════════════════════════════════════════════════════════");
  console.log("Step 1: Deploying OINIOToken...");
  console.log("═══════════════════════════════════════════════════════════\n");

  const OINIOToken = await ethers.getContractFactory("OINIOToken");
  const token = await OINIOToken.deploy(deployer.address);
  await token.waitForDeployment();
  const tokenAddress = await token.getAddress();

  console.log("✓ OINIOToken deployed to:", tokenAddress);
  console.log("  Transaction hash:", token.deploymentTransaction()?.hash);

  // Get token info
  const tokenName = await token.name();
  const tokenSymbol = await token.symbol();
  const tokenDecimals = await token.decimals();
  const totalSupply = await token.totalSupply();

  console.log(`  Name: ${tokenName}`);
  console.log(`  Symbol: ${tokenSymbol}`);
  console.log(`  Decimals: ${tokenDecimals}`);
  console.log(`  Total Supply: ${ethers.formatEther(totalSupply)} ${tokenSymbol}`);
  console.log();

  // Verify token deployment
  await verifyDeployment("OINIOToken", tokenAddress, [deployer.address]);

  // Deploy OINIOModelRegistry
  console.log("═══════════════════════════════════════════════════════════");
  console.log("Step 2: Deploying OINIOModelRegistry...");
  console.log("═══════════════════════════════════════════════════════════\n");

  const OINIOModelRegistry = await ethers.getContractFactory("OINIOModelRegistry");
  const registry = await OINIOModelRegistry.deploy(tokenAddress, deployer.address);
  await registry.waitForDeployment();
  const registryAddress = await registry.getAddress();

  console.log("✓ OINIOModelRegistry deployed to:", registryAddress);
  console.log("  Transaction hash:", registry.deploymentTransaction()?.hash);

  // Get registry info
  const registryName = await registry.name();
  const registrySymbol = await registry.symbol();
  const oinioTokenAddr = await registry.oinioToken();

  console.log(`  Name: ${registryName}`);
  console.log(`  Symbol: ${registrySymbol}`);
  console.log(`  OINIO Token: ${oinioTokenAddr}`);
  console.log();

  // Verify registry deployment
  await verifyDeployment("OINIOModelRegistry", registryAddress, [tokenAddress, deployer.address]);

  // Print deployment summary
  console.log("╔════════════════════════════════════════════════════════════╗");
  console.log("║               DEPLOYMENT SUMMARY                           ║");
  console.log("╚════════════════════════════════════════════════════════════╝\n");
  console.log(`Network: ${network.name}`);
  console.log(`Chain ID: ${chainId}`);
  console.log(`Deployer: ${deployer.address}`);
  console.log();
  console.log("Deployed Contracts:");
  console.log(`  OINIOToken:          ${tokenAddress}`);
  console.log(`  OINIOModelRegistry:  ${registryAddress}`);
  console.log();
  console.log("═══════════════════════════════════════════════════════════");
  console.log("NEXT STEPS");
  console.log("═══════════════════════════════════════════════════════════");
  console.log("1. Save the contract addresses above");
  console.log("2. Verify contracts on block explorer (if not done automatically):");
  console.log(`   npx hardhat verify --network ${network.name} ${tokenAddress} "${deployer.address}"`);
  console.log(`   npx hardhat verify --network ${network.name} ${registryAddress} "${tokenAddress}" "${deployer.address}"`);
  console.log("3. Update frontend configuration with contract addresses");
  console.log("4. Test contract interactions");
  console.log();
  console.log("Environment variable format (.env):");
  console.log(`OINIO_TOKEN_ADDRESS=${tokenAddress}`);
  console.log(`OINIO_REGISTRY_ADDRESS=${registryAddress}`);
  console.log();
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("\n❌ Deployment failed:", error);
    process.exit(1);
  });
