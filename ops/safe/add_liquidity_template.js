// Template: prepare unsigned addLiquidity tx for Router
// Usage: fill in token addresses, amounts, and output file will contain unsigned tx JSON

const { ethers } = require("ethers");
const fs = require("fs");

async function buildAddLiquidity({rpcUrl, routerAddress, tokenA, tokenB, amountA, amountB, recipient}){
  const provider = new ethers.providers.JsonRpcProvider(rpcUrl);
  // ABI: Router's addLiquidity signature - this is a template, confirm router ABI
  const routerAbi = ["function addLiquidity(address tokenA, address tokenB, uint amountADesired, uint amountBDesired, uint amountAMin, uint amountBMin, address to, uint deadline)"];
  const iface = new ethers.utils.Interface(routerAbi);

  const deadline = Math.floor(Date.now()/1000) + 3600; // 1h

  const data = iface.encodeFunctionData("addLiquidity", [tokenA, tokenB, amountA, amountB, 0, 0, recipient, deadline]);

  const unsigned = {
    to: routerAddress,
    value: "0",
    data
  };

  fs.writeFileSync("ops/safe/add_liquidity_unsigned.json", JSON.stringify(unsigned, null, 2));
  console.log("Wrote ops/safe/add_liquidity_unsigned.json — review before proposing in Safe.");
}

module.exports = { buildAddLiquidity };
