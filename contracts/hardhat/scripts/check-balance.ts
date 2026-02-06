import { ethers } from "hardhat";
import * as fs from "fs";
import * as path from "path";

/**
 * Pre-deployment check utility
 * Verifies environment, balance, and network connectivity
 */
async function checkDeploymentReadiness(
  providerUrl: string,
  minBalance: string = "0.1"
): Promise<void> {
  console.log("=== Pre-Deployment Safety Checks ===\n");

  // Check environment variables
  console.log("1. Checking environment variables...");
  if (!process.env.PRIVATE_KEY) {
    throw new Error("PRIVATE_KEY not set in environment");
  }
  console.log("   ✓ PRIVATE_KEY is set");

  // Check provider connection
  console.log("\n2. Checking network connectivity...");
  try {
    const provider = new ethers.JsonRpcProvider(providerUrl);
    const network = await provider.getNetwork();
    console.log(`   ✓ Connected to network: ${network.name} (Chain ID: ${network.chainId})`);

    // Check balance
    console.log("\n3. Checking deployer balance...");
    const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider);
    const balance = await provider.getBalance(wallet.address);
    const balanceEth = ethers.formatEther(balance);
    
    console.log(`   Deployer address: ${wallet.address}`);
    console.log(`   Balance: ${balanceEth} ETH`);

    const minBalanceWei = ethers.parseEther(minBalance);
    if (balance < minBalanceWei) {
      throw new Error(
        `Insufficient balance: ${balanceEth} ETH. Minimum required: ${minBalance} ETH`
      );
    }
    console.log(`   ✓ Balance sufficient (min: ${minBalance} ETH)`);

    // Check gas price
    console.log("\n4. Checking gas price...");
    const feeData = await provider.getFeeData();
    if (feeData.gasPrice) {
      const gasPriceGwei = ethers.formatUnits(feeData.gasPrice, "gwei");
      console.log(`   Current gas price: ${gasPriceGwei} gwei`);
      console.log("   ✓ Gas price retrieved");
    }

    console.log("\n✅ All pre-deployment checks passed!\n");
  } catch (error) {
    console.error("\n❌ Pre-deployment check failed:", error);
    throw error;
  }
}

/**
 * Post-deployment verification
 * Verifies contract deployment and saves deployment info
 */
async function verifyDeployment(
  contractName: string,
  contractAddress: string,
  constructorArgs: any[]
): Promise<void> {
  console.log(`\n=== Post-Deployment Verification: ${contractName} ===\n`);

  try {
    // Check if contract code exists
    const provider = ethers.provider;
    const code = await provider.getCode(contractAddress);
    
    if (code === "0x") {
      throw new Error("No contract code found at address");
    }
    console.log(`✓ Contract code verified at ${contractAddress}`);
    console.log(`  Code size: ${(code.length - 2) / 2} bytes`);

    // Try to interact with contract
    const contract = await ethers.getContractAt(contractName, contractAddress);
    console.log("✓ Contract interface verified");

    // Save deployment info
    const deploymentInfo = {
      contractName,
      address: contractAddress,
      constructorArgs,
      network: (await provider.getNetwork()).name,
      chainId: Number((await provider.getNetwork()).chainId),
      deployer: await (await ethers.provider.getSigner()).getAddress(),
      timestamp: new Date().toISOString(),
      blockNumber: await provider.getBlockNumber(),
    };

    const deploymentsDir = path.join(__dirname, "..", "deployments");
    if (!fs.existsSync(deploymentsDir)) {
      fs.mkdirSync(deploymentsDir, { recursive: true });
    }

    const filePath = path.join(
      deploymentsDir,
      `${contractName}-${deploymentInfo.chainId}.json`
    );
    fs.writeFileSync(filePath, JSON.stringify(deploymentInfo, null, 2));
    console.log(`✓ Deployment info saved to ${filePath}`);

    console.log("\n✅ Post-deployment verification passed!\n");
    return;
  } catch (error) {
    console.error("\n❌ Post-deployment verification failed:", error);
    throw error;
  }
}

/**
 * Main check balance script
 */
async function main() {
  const network = await ethers.provider.getNetwork();
  const rpcUrl = network.name === "hardhat" 
    ? "http://localhost:8545" 
    : process.env.RPC_URL || "";

  await checkDeploymentReadiness(rpcUrl);
}

// Run if called directly
if (require.main === module) {
  main()
    .then(() => process.exit(0))
    .catch((error) => {
      console.error(error);
      process.exit(1);
    });
}

export { checkDeploymentReadiness, verifyDeployment };
