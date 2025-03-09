from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fetch_trades import get_trade_data

app = FastAPI()

# ✅ Enable CORS to allow frontend requests from http://localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change to ["http://localhost:3000"] for specific frontend)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/trades")
def get_trades():
    """API Endpoint to fetch trades from blockchain"""
    print("📢 API called: Fetching trades from blockchain...")
    trades = get_trade_data()
    print(f"✅ API Response: {len(trades)} trades found.")
    return trades

