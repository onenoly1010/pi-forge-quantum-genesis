import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";
import "@nomicfoundation/hardhat-verify";
import * as dotenv from "dotenv";

dotenv.config({ path: "../.env" });

const config: HardhatUserConfig = {
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,
      },
    },
  },
  networks: {
    // 0G Aristotle Mainnet
    zeroG: {
      url: process.env.ZERO_G_RPC || "https://evmrpc.0g.ai",
      chainId: 16661,
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
      gasPrice: 20000000000, // 20 gwei
    },
    // 0G Testnet (if available)
    zeroGTestnet: {
      url: process.env.ZERO_G_TESTNET_RPC || "https://evmrpc-testnet.0g.ai",
      chainId: 16660, // Adjust if different
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
    },
    // Pi Network Testnet
    piTestnet: {
      url: process.env.PI_TESTNET_RPC || "https://api.testnet.minepi.com/rpc",
      chainId: 2025,
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
    },
    // Pi Network Mainnet
    piMainnet: {
      url: process.env.PI_MAINNET_RPC || "https://rpc.mainnet.pi.network",
      chainId: 314159,
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
    },
  },
  etherscan: {
    apiKey: {
      zeroG: process.env.ZERO_G_API_KEY || "",
      piTestnet: process.env.PI_API_KEY || "",
      piMainnet: process.env.PI_API_KEY || "",
    },
    customChains: [
      {
        network: "zeroG",
        chainId: 16661,
        urls: {
          apiURL: "https://scan.0g.ai/api",
          browserURL: "https://scan.0g.ai",
        },
      },
      {
        network: "piTestnet",
        chainId: 2025,
        urls: {
          apiURL: "https://testnet.minepi.com/api",
          browserURL: "https://testnet.minepi.com",
        },
      },
      {
        network: "piMainnet",
        chainId: 314159,
        urls: {
          apiURL: "https://pi.blockscout.com/api",
          browserURL: "https://pi.blockscout.com",
        },
      },
    ],
  },
  paths: {
    sources: "../src",
    tests: "../test",
    cache: "./cache",
    artifacts: "./artifacts",
  },
};

export default config;
