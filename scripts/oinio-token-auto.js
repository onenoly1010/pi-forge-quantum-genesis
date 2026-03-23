const { ethers } = require("ethers");

// Configuration
const PRIVATE_KEY = process.env.PRIVATE_KEY || "your-private-key-here";
const RPC_URL = process.env.RPC_URL || "https://your-rpc-url";
const TOKEN_ADDRESS = process.env.TOKEN_ADDRESS || "0xYourTokenAddress";

// OINIOToken ABI (minimal for interactions)
const OINIOTokenABI = [
    "function name() view returns (string)",
    "function symbol() view returns (string)",
    "function decimals() view returns (uint8)",
    "function totalSupply() view returns (uint256)",
    "function balanceOf(address account) view returns (uint256)",
    "function transfer(address to, uint256 amount) returns (bool)",
    "function burn(uint256 amount)",
    "function owner() view returns (address)",
    "function transferFrom(address from, address to, uint256 amount) returns (bool)",
    "function approve(address spender, uint256 amount) returns (bool)"
];

async function autoTokenOperations() {
    console.log("🤖 OINIO Token Auto Operations Started...");

    // Setup
    const provider = new ethers.JsonRpcProvider(RPC_URL);
    const wallet = new ethers.Wallet(PRIVATE_KEY, provider);
    const token = new ethers.Contract(TOKEN_ADDRESS, OINIOTokenABI, wallet);

    console.log(`📍 Connected to: ${TOKEN_ADDRESS}`);
    console.log(`👤 Operator: ${wallet.address}`);

    // Example operations (customize as needed)
    try {
        // Check balance
        const balance = await token.balanceOf(wallet.address);
        console.log(`💰 Current balance: ${ethers.formatEther(balance)} OINIO`);

        // Example: Transfer tokens (uncomment and customize)
        // const recipient = "0xRecipientAddress";
        // const amount = ethers.parseEther("100");
        // const tx = await token.transfer(recipient, amount);
        // await tx.wait();
        // console.log(`✅ Transferred ${ethers.formatEther(amount)} OINIO to ${recipient}`);

        // Example: Burn tokens (uncomment and customize)
        // const burnAmount = ethers.parseEther("10");
        // const burnTx = await token.burn(burnAmount);
        // await burnTx.wait();
        // console.log(`🔥 Burned ${ethers.formatEther(burnAmount)} OINIO`);

        // Example: Approve for staking (uncomment and customize)
        // const spender = "0xStakingContractAddress";
        // const approveAmount = ethers.parseEther("500");
        // const approveTx = await token.approve(spender, approveAmount);
        // await approveTx.wait();
        // console.log(`✅ Approved ${ethers.formatEther(approveAmount)} OINIO for ${spender}`);

    } catch (error) {
        console.error("❌ Operation failed:", error);
    }

    console.log("✅ Auto operations completed.");
}

async function main() {
    await autoTokenOperations();
}

main().catch(console.error);