from zerepy import ZerePyAgent
from dotenv import load_dotenv
from web3 import Web3
import random
import os
import json

# Load environment variables
print("📢 Loading environment variables...")
load_dotenv() 
SONIC_RPC_URL = os.getenv('SONIC_RPC_URL')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')

# Validate environment variables
if not SONIC_RPC_URL:
    raise ValueError("❌ SONIC_RPC_URL is not set! Check your .env file.")
if not PRIVATE_KEY:
    raise ValueError("❌ PRIVATE_KEY is not set! Check your .env file.")
if not CONTRACT_ADDRESS:
    raise ValueError("❌ CONTRACT_ADDRESS is not set! Check your .env file.")

print(f"✅ SONIC_RPC_URL: {SONIC_RPC_URL}")
print(f"✅ CONTRACT_ADDRESS: {CONTRACT_ADDRESS[:6]}...{CONTRACT_ADDRESS[-6:]} (partially hidden)")

# Blockchain connection
print("📢 Connecting to blockchain...")
w3 = Web3(Web3.HTTPProvider(SONIC_RPC_URL))

if not w3.is_connected():
    raise ConnectionError("❌ Blockchain connection failed! Check your RPC URL.")

print("✅ Connected to blockchain!")

# Load account
print("📢 Fetching account details...")
account = w3.eth.account.from_key(PRIVATE_KEY)
print(f"✅ Account loaded: {account.address[:6]}...{account.address[-6:]} (partially hidden)")

# Load contract ABI
ABI_PATH = "../contracts/artifacts/contracts/AI_MarketMaker.sol/AI_MarketMaker.json"

if not os.path.exists(ABI_PATH):
    raise FileNotFoundError(f"❌ ABI file not found at {ABI_PATH}")

print(f"📢 Loading contract ABI from {ABI_PATH}...")
with open(ABI_PATH, "r") as f:
    contract_abi = json.load(f)["abi"]

# Initialize the contract
print(f"📢 Initializing contract at {CONTRACT_ADDRESS}...")
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)
print("✅ Smart contract initialized successfully!")

# Initialize AI Market Maker
print("📢 Initializing AI Market Maker Agent...")
agent = ZerePyAgent(agent_name="MarketMakerAgent")
print(f"✅ AI Agent '{agent.name}' initialized successfully!")

# Function to execute trades
def execute_trade(action):
    """Executes a trade on the smart contract."""
    print(f"📢 Preparing trade action: {action}")

    if not isinstance(action, str):
        action = str(action)  # Convert to string if necessary

    amount = random.uniform(0.1, 5)  # Generates a random amount between 0.1 and 5 Sonic tokens
    amount = round(amount, 2)  # Round to 2 decimal places

    print(f"📢 Executing Trade: {action} with {amount} Sonic")

    print("📢 Fetching nonce...")
    nonce = w3.eth.get_transaction_count(account.address, "pending")
    print(f"✅ Nonce fetched: {nonce}")

    print("📢 Building transaction...")
    # sonic_amount = 1
    tx = contract.functions.executeTrade(action, int(amount * (10**18))).build_transaction({
        'from': account.address,
        'gas': 300000,
        'gasPrice': w3.to_wei('15', 'gwei'),
        'nonce': nonce,
    })
    print("✅ Transaction built successfully!")

    print("📢 Signing transaction...")
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    print(f"✅ Transaction signed! TX Hash: {signed_tx.hash.hex()}")

    print("🚀 Sending transaction to blockchain...")
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"✅ Trade executed! TX Hash: {tx_hash.hex()}")

    return tx_hash.hex()

# Run the AI trading loop
print("📢 Starting AI trading loop...")
while True:
    print("📢 Selecting action from AI agent...")
    action = agent.select_action()  # Correct function to pick an action
    print(f"✅ Action selected: {action}")

    execute_trade(action)
    print("⏳ Waiting before next trade...")
