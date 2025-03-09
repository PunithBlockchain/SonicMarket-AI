import json
from web3 import Web3

# ✅ Sonic Blockchain Details
SONIC_RPC_URL = "https://rpc.blaze.soniclabs.com"
CONTRACT_ADDRESS = "0x9a7357C62D613cC383200B5Fd96217cBa55D9b91"

ABI = [
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "string", "name": "action", "type": "string"},
            {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"}
        ],
        "name": "TradeExecuted",
        "type": "event"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "action", "type": "string"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"}
        ],
        "name": "executeTrade",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# ✅ Connect to Blockchain
print("📢 Connecting to Sonic Blockchain...")
w3 = Web3(Web3.HTTPProvider(SONIC_RPC_URL))

if w3.is_connected():
    print("✅ Successfully connected to Sonic blockchain!")
else:
    raise ConnectionError("❌ Could not connect to Sonic blockchain. Check RPC URL.")

# ✅ Load Contract
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
print(f"📢 Contract loaded at: {CONTRACT_ADDRESS}")

def clean_action_value(action):
    """Cleans and extracts the action name properly."""
    try:
        print(f"🔍 Raw action value: {action}")  # ✅ Debugging print

        # ✅ If action is a dictionary, extract the 'name' field
        if isinstance(action, dict) and "name" in action:
            return action["name"].replace("-", " ").title()  # ✅ Converts "adjust-liquidity" → "Adjust Liquidity"

        # ✅ If action is already a string, return it in title format
        if isinstance(action, str):
            return action.replace("-", " ").title()

    except Exception as e:
        print(f"❌ Error parsing action value: {e}")
        return "Unknown"

def get_trade_data():
    """Fetch past trade events from the Sonic blockchain"""
    try:
        print("📢 Fetching past trades from blockchain...")

        latest_block = w3.eth.block_number
        start_block = max(0, latest_block - 100)  # Fetch last 100 blocks
        print(f"🔄 Scanning blocks {start_block} to {latest_block} for trades...")

        events = contract.events.TradeExecuted.get_logs(fromBlock=start_block, toBlock="latest")

        trades = []
        for event in events:
            block_details = w3.eth.get_block(event["blockNumber"])
            timestamp = block_details.timestamp  # Fetch timestamp

            # ✅ Extract & clean action
            action_raw = event["args"]["action"]
            action_clean = clean_action_value(action_raw)

            # ✅ Convert amount properly
            sonic_amount = round(float(event["args"]["amount"]) / 1e18, 2)

            trade = {
                "action": action_clean,  # ✅ Always a clean string
                "amount": sonic_amount,  # ✅ Proper amount format
                "txHash": event["transactionHash"].hex(),
                "timestamp": timestamp
            }
            trades.append(trade)
            print(f"✅ Trade found: {trade}")  # Debugging print

        print(f"✅ Total {len(trades)} trades fetched.")
        return trades

    except Exception as e:
        print(f"❌ Error fetching trades: {e}")
        return {"error": str(e)}
