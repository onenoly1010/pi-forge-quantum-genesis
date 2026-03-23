import { ethers } from "hardhat";
import { checkDeploymentReadiness, verifyDeployment } from "./check-balance";

/**
 * Deploy DEX Contracts (UniswapV2 Fork) on 0G Network
 * 
 * This script deploys the full UniswapV2-style DEX:
 * 1. WETH (W0G - Wrapped 0G)
 * 2. UniswapV2Factory
 * 3. UniswapV2Router02
 * 
 * Usage:
 *   npx hardhat run scripts/deploy-dex.ts --network zeroG
 * 
 * Environment variables required:
 *   - PRIVATE_KEY: Deployer's private key
 *   - ZERO_G_RPC: 0G network RPC URL (optional, uses default)
 *   - FEE_TO_SETTER: Address for fee collection (optional, uses deployer)
 */
async function main() {
  console.log("╔════════════════════════════════════════════════════════════╗");
  console.log("║   UniswapV2-Style DEX Deployment Script (Hardhat)         ║");
  console.log("║   Target: 0G Aristotle Mainnet                            ║");
  console.log("╚════════════════════════════════════════════════════════════╝\n");

  // Get network info
  const network = await ethers.provider.getNetwork();
  const chainId = Number(network.chainId);
  console.log(`Network: ${network.name}`);
  console.log(`Chain ID: ${chainId}\n`);

  // Verify we're on 0G network
  if (chainId !== 16661) {
    console.warn("⚠️  WARNING: This script is designed for 0G Aristotle Mainnet (Chain ID: 16661)");
    console.warn(`   Current chain ID: ${chainId}`);
    console.warn("   Proceeding anyway, but verify this is correct!\n");
  }

  // Get deployer
  const [deployer] = await ethers.getSigners();
  const feeToSetter = process.env.FEE_TO_SETTER || deployer.address;
  
  console.log("Deployer address:", deployer.address);
  console.log("Fee To Setter:", feeToSetter);
  console.log();

  // Pre-deployment checks
  const rpcUrl = process.env.ZERO_G_RPC || "https://evmrpc.0g.ai";
  await checkDeploymentReadiness(rpcUrl, "0.5");

  // Step 1: Deploy WETH (W0G - Wrapped 0G)
  console.log("═══════════════════════════════════════════════════════════");
  console.log("Step 1: Deploying W0G (Wrapped 0G)...");
  console.log("═══════════════════════════════════════════════════════════\n");

  console.log("⚠️  Note: This script assumes W0G contract exists in ../0g-dex/");
  console.log("   If using 0g-uniswap-v2, adjust the import path\n");

  // For this example, we'll create a minimal WETH interface
  // In production, import from actual contract location
  const WETH_ABI = [
    "function name() view returns (string)",
    "function symbol() view returns (string)",
    "function deposit() payable",
    "function withdraw(uint256)",
    "function balanceOf(address) view returns (uint256)"
  ];

  // Note: You'll need to compile and import the actual W0G contract
  // For now, we'll indicate where it should be deployed
  console.log("⚠️  Deploy W0G contract manually using Forge:");
  console.log("   cd ../0g-uniswap-v2");
  console.log("   forge script script/Deploy.s.sol --sig 'deployW0GOnly()' --rpc-url $ZERO_G_RPC --broadcast\n");
  
  const w0gAddress = process.env.W0G_ADDRESS;
  if (!w0gAddress) {
    throw new Error("W0G_ADDRESS not set. Deploy W0G first using Forge script.");
  }
  console.log("✓ Using W0G at:", w0gAddress);
  console.log();

  // Step 2: Deploy UniswapV2Factory
  console.log("═══════════════════════════════════════════════════════════");
  console.log("Step 2: Deploying UniswapV2Factory...");
  console.log("═══════════════════════════════════════════════════════════\n");

  console.log("⚠️  Note: Factory deployment requires UniswapV2Pair contract");
  console.log("   This is typically done with Forge. For Hardhat deployment:");
  console.log("   1. Copy ../0g-dex contracts to Hardhat sources");
  console.log("   2. Or use Forge for DEX deployment\n");

  const factoryAddress = process.env.FACTORY_ADDRESS;
  if (!factoryAddress) {
    console.log("⚠️  FACTORY_ADDRESS not set. Deploy Factory using Forge:");
    console.log("   See ../0g-uniswap-v2/script/Deploy.s.sol\n");
    
    console.log("═══════════════════════════════════════════════════════════");
    console.log("RECOMMENDED APPROACH");
    console.log("═══════════════════════════════════════════════════════════");
    console.log("For DEX deployment on 0G, use Forge instead of Hardhat:");
    console.log();
    console.log("cd ../0g-uniswap-v2");
    console.log("forge script script/Deploy.s.sol --rpc-url $ZERO_G_RPC --broadcast --verify");
    console.log();
    console.log("This is because:");
    console.log("1. DEX contracts are complex and Forge-optimized");
    console.log("2. PAIR_INIT_CODE_HASH calculation is Forge-specific");
    console.log("3. Library linking is easier with Forge");
    console.log();
    console.log("Use this Hardhat script for iNFT contracts (OINIO) instead.");
    console.log();
    
    return;
  }

  console.log("✓ Using Factory at:", factoryAddress);
  console.log();

  // Step 3: Deploy UniswapV2Router02
  console.log("═══════════════════════════════════════════════════════════");
  console.log("Step 3: Deploying UniswapV2Router02...");
  console.log("═══════════════════════════════════════════════════════════\n");

  const routerAddress = process.env.ROUTER_ADDRESS;
  if (!routerAddress) {
    console.log("⚠️  ROUTER_ADDRESS not set. Deploy using Forge script.\n");
    return;
  }

  console.log("✓ Using Router at:", routerAddress);
  console.log();

  // Print deployment summary
  console.log("╔════════════════════════════════════════════════════════════╗");
  console.log("║               DEPLOYMENT SUMMARY                           ║");
  console.log("╚════════════════════════════════════════════════════════════╝\n");
  console.log(`Network: ${network.name}`);
  console.log(`Chain ID: ${chainId}`);
  console.log(`Deployer: ${deployer.address}`);
  console.log(`Fee To Setter: ${feeToSetter}`);
  console.log();
  console.log("Deployed/Referenced Contracts:");
  console.log(`  W0G (Wrapped 0G):     ${w0gAddress}`);
  console.log(`  UniswapV2Factory:     ${factoryAddress}`);
  console.log(`  UniswapV2Router02:    ${routerAddress}`);
  console.log();
  console.log("═══════════════════════════════════════════════════════════");
  console.log("NEXT STEPS");
  console.log("═══════════════════════════════════════════════════════════");
  console.log("1. For actual DEX deployment, use Forge:");
  console.log("   cd ../0g-uniswap-v2");
  console.log("   forge script script/Deploy.s.sol --rpc-url $ZERO_G_RPC --broadcast");
  console.log();
  console.log("2. Update frontend configuration:");
  console.log(`   ZERO_G_W0G=${w0gAddress}`);
  console.log(`   ZERO_G_FACTORY=${factoryAddress}`);
  console.log(`   ZERO_G_ROUTER=${routerAddress}`);
  console.log();
  console.log("3. Verify contracts on 0G explorer");
  console.log("4. Test DEX functionality");
  console.log();
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("\n❌ Deployment script failed:", error);
    process.exit(1);
  });
