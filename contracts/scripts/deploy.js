const hre = require("hardhat");

async function main() {
  console.log("Deploying AI_MarketMaker smart contract...");

  // Get the contract factory
  const MarketMaker = await hre.ethers.getContractFactory("AI_MarketMaker");

  // Deploy the contract
  const marketMaker = await MarketMaker.deploy();

  // Wait for deployment to complete
  await marketMaker.waitForDeployment();

  // Get the deployed contract address
  const contractAddress = await marketMaker.getAddress();
  console.log(`✅ AI_MarketMaker deployed to: ${contractAddress}`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("❌ Deployment failed:", error);
    process.exit(1);
  });
