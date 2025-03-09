require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config(); // Ensure dotenv is imported

const SONIC_PRIVATE_KEY = process.env.SONIC_PRIVATE_KEY;

if (!SONIC_PRIVATE_KEY || SONIC_PRIVATE_KEY.length !== 64) {
  throw new Error("❌ Invalid PRIVATE_KEY: Expected 32-byte (64 characters) hex string");
}

module.exports = {
  solidity: "0.8.26",
  paths: {
    sources: "./contracts",   // Ensure it compiles only from the correct folder
    artifacts: "./artifacts",
    cache: "./cache"
  },
  settings: {
    optimizer: {
      enabled: true,
      runs: 200
    }
  },
  networks: {
    sonic: {
      url: "https://rpc.blaze.soniclabs.com",
      accounts: [`0x${SONIC_PRIVATE_KEY}`]  // Ensure private key has "0x" prefix
    }
  },
  exclude: ["node_modules"]
};
