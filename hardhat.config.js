require("@nomicfoundation/hardhat-toolbox");

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: {
    compilers: [
      {
        version: "0.8.19",
        settings: {
          optimizer: {
            enabled: true,
            runs: 1, // Minimize deployment size
          },
          viaIR: true, // Enable IR-based optimizer
        },
      },
      // Keep 0.5.16 for existing contracts
      {
        version: "0.5.16",
        settings: {
          optimizer: {
            enabled: true,
            runs: 200,
          },
        },
      },
      // Keep 0.6.6 for existing router
      {
        version: "0.6.6",
        settings: {
          optimizer: {
            enabled: true,
            runs: 200,
          },
        },
      },
    ],
  },
  networks: {
    // 0G Aristotle Testnet
    aristotle: {
      url: process.env.ZEROG_RPC_URL || "https://evmrpc-testnet.0g.ai",
      chainId: 42069,
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
      timeout: 60000,
    },
    // 0G Aristotle Mainnet
    aristotleMainnet: {
      url: process.env.ZEROG_RPC_URL || "https://evmrpc.0g.ai",
      chainId: 16661,
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
      timeout: 60000,
    },
  },
  paths: {
    sources: "./contracts/dex-slim",
    tests: "./test",
    cache: "./cache",
    artifacts: "./artifacts",
  },
};
