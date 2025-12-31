const hre = require("hardhat");

async function main() {
  console.log("🔑 Calculating INIT_CODE_HASH for deployed Factory...");
  
  // Get pair creation bytecode
  const PairFactory = await hre.ethers.getContractFactory("UniswapV2Pair");
  const pairBytecode = PairFactory.bytecode;
  
  // Calculate keccak256 hash
  const initCodeHash = hre.ethers.keccak256(pairBytecode);
  
  console.log(`✅ INIT_CODE_HASH: ${initCodeHash}`);
  console.log(`\n📝 Add this to your .env file:`);
  console.log(`INIT_CODE_HASH=${initCodeHash}`);
  
  return initCodeHash;
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
