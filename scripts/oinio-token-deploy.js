const { ethers } = require("ethers");
const fs = require("fs");

// Configuration
const PRIVATE_KEY = process.env.PRIVATE_KEY || "your-private-key-here";
const RPC_URL = process.env.RPC_URL || "https://your-rpc-url";
const INITIAL_OWNER = process.env.INITIAL_OWNER || "0xYourOwnerAddress";

// OINIOToken Contract ABI and Bytecode (replace with actual compiled output)
const OINIOTokenABI = [
    // Minimal ABI for deployment
    "constructor(address initialOwner)",
    "function name() view returns (string)",
    "function symbol() view returns (string)",
    "function decimals() view returns (uint8)",
    "function totalSupply() view returns (uint256)",
    "function balanceOf(address account) view returns (uint256)",
    "function transfer(address to, uint256 amount) returns (bool)",
    "function burn(uint256 amount)",
    "function owner() view returns (address)"
];

const OINIOTokenBytecode = "0x" + fs.readFileSync("./contracts/out/OINIOToken.sol/OINIOToken.json", "utf8").bytecode; // Adjust path

async function deployOINIOToken() {
    console.log("🚀 Deploying OINIOToken...");

    // Setup provider and signer
    const provider = new ethers.JsonRpcProvider(RPC_URL);
    const wallet = new ethers.Wallet(PRIVATE_KEY, provider);

    console.log(`📍 Deployer: ${wallet.address}`);
    console.log(`👤 Initial Owner: ${INITIAL_OWNER}`);

    // Create contract factory
    const OINIOTokenFactory = new ethers.ContractFactory(OINIOTokenABI, OINIOTokenBytecode, wallet);

    // Deploy contract
    const token = await OINIOTokenFactory.deploy(INITIAL_OWNER);
    await token.waitForDeployment();

    const tokenAddress = await token.getAddress();
    console.log(`✅ OINIOToken deployed at: ${tokenAddress}`);

    // Verify deployment
    const name = await token.name();
    const symbol = await token.symbol();
    const totalSupply = await token.totalSupply();
    const owner = await token.owner();

    console.log(`📊 Token Details:`);
    console.log(`   Name: ${name}`);
    console.log(`   Symbol: ${symbol}`);
    console.log(`   Total Supply: ${ethers.formatEther(totalSupply)} OINIO`);
    console.log(`   Owner: ${owner}`);

    // Save deployment info
    const deploymentInfo = {
        contractAddress: tokenAddress,
        deployer: wallet.address,
        initialOwner: INITIAL_OWNER,
        name,
        symbol,
        totalSupply: totalSupply.toString(),
        network: await provider.getNetwork(),
        timestamp: new Date().toISOString()
    };

    fs.writeFileSync("./deployment-oinio-token.json", JSON.stringify(deploymentInfo, null, 2));
    console.log("💾 Deployment info saved to deployment-oinio-token.json");

    return tokenAddress;
}

async function main() {
    try {
        await deployOINIOToken();
        console.log("🎉 OINIOToken deployment completed successfully!");
    } catch (error) {
        console.error("❌ Deployment failed:", error);
        process.exit(1);
    }
}

main();