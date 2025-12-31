const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  console.log("🚀 Deploying Slim Router to 0G Aristotle Mainnet...");
  
  const [deployer] = await hre.ethers.getSigners();
  const network = await hre.ethers.provider.getNetwork();
  
  console.log(`👤 Deployer: ${deployer.address}`);
  console.log(`🌐 Network: ${hre.network.name} (ChainID: ${network.chainId})`);
  
  // Existing deployment addresses
  const FACTORY_ADDRESS = "0x307bFaA937768a073D41a2EbFBD952Be8E38BF91";
  const WETH_ADDRESS = process.env.WETH_ADDRESS || "0x4200000000000000000000000000000000000006";
  
  // Calculate INIT_CODE_HASH from factory
  let INIT_CODE_HASH = process.env.INIT_CODE_HASH;
  
  if (!INIT_CODE_HASH) {
    console.log("⚠️  INIT_CODE_HASH not found in .env - using default");
    INIT_CODE_HASH = "0x96e8ac4277198ff8b6f785478aa9a39f403cb768dd02cbee326c3e7da348845f";
  }
  
  console.log(`🏭 Factory: ${FACTORY_ADDRESS}`);
  console.log(`💧 WETH: ${WETH_ADDRESS}`);
  console.log(`🔑 Init Code Hash: ${INIT_CODE_HASH}`);
  
  // Deploy Router
  const SlimRouter = await hre.ethers.getContractFactory("UniswapV2Router02Slim");
  console.log("📦 Deploying contract...");
  
  const router = await SlimRouter.deploy(FACTORY_ADDRESS, WETH_ADDRESS, INIT_CODE_HASH);
  await router.waitForDeployment();
  
  const routerAddress = await router.getAddress();
  console.log(`✅ Router deployed: ${routerAddress}`);
  
  // Verify bytecode size
  const code = await hre.ethers.provider.getCode(routerAddress);
  const bytecodeSize = (code.length - 2) / 2; // Remove 0x and divide by 2
  console.log(`📏 Bytecode size: ${bytecodeSize} bytes`);
  
  if (bytecodeSize > 24576) {
    console.error(`❌ ERROR: Bytecode exceeds 24KB limit (${bytecodeSize} bytes)`);
    process.exit(1);
  } else {
    console.log(`✅ Bytecode under 24KB limit! (${((bytecodeSize/24576)*100).toFixed(2)}% used)`);
  }
  
  // Update .env.launch
  const envPath = path.join(__dirname, "..", ".env.launch");
  let envContent = "";
  
  if (fs.existsSync(envPath)) {
    envContent = fs.readFileSync(envPath, "utf8");
  }
  
  const newEntry = `DEX_ROUTER_ADDRESS=${routerAddress}`;
  
  if (envContent.includes("DEX_ROUTER_ADDRESS=")) {
    envContent = envContent.replace(/DEX_ROUTER_ADDRESS=.*/, newEntry);
  } else {
    envContent += `\n${newEntry}\n`;
  }
  
  fs.writeFileSync(envPath, envContent);
  console.log(`📝 Updated .env.launch with router address`);
  
  // Create deployment summary
  const summary = {
    network: hre.network.name,
    chainId: Number(network.chainId),
    timestamp: new Date().toISOString(),
    contracts: {
      router: routerAddress,
      factory: FACTORY_ADDRESS,
      weth: WETH_ADDRESS,
    },
    bytecodeSize: `${bytecodeSize} bytes (${((bytecodeSize/24576)*100).toFixed(2)}% of limit)`,
    deployer: deployer.address,
  };
  
  const summaryPath = path.join(__dirname, "..", "deployments", "slim-router-deployment.json");
  fs.mkdirSync(path.dirname(summaryPath), { recursive: true });
  fs.writeFileSync(summaryPath, JSON.stringify(summary, null, 2));
  
  console.log("\n🎉 DEPLOYMENT COMPLETE!");
  console.log(`📊 Summary saved to: ${summaryPath}`);
  console.log("\n🔥 Next steps:");
  console.log("   1. Verify contract on 0G explorer");
  console.log("   2. Create OINIO/0G pair via Factory");
  console.log("   3. Update Forge UI with new router address");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
