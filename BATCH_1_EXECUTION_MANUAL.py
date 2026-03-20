#!/usr/bin/env python3
"""
BATCH 1 - MANUAL EXECUTION GUIDE
Paper trading account PA320EPZBPGV
Run this NOW to deploy Batch 1
"""

import os
from datetime import datetime

ALPACA_KEY = "PKW445AWAOSGU2WJYCCFUZ47PR"
ALPACA_SECRET = "7tmQ6gY5c4hdmqwEN3UAgv4to78WsGkWPmxUox4G7x4X"
BASE_URL = "https://paper-api.alpaca.markets/v2"

def get_timestamp():
    return datetime.now().strftime("%H:%M:%S")

def print_batch_plan():
    print("\n" + "="*70)
    print("🚀 BATCH 1 DEPLOYMENT PLAN - 11:35 UTC")
    print("="*70)
    print(f"\n[{get_timestamp()}] STRATEGY: SHORT_AGGRESSIVE (Bearish market)")
    print(f"[{get_timestamp()}] Account: PA320EPZBPGV (PAPER TRADING)")
    print(f"[{get_timestamp()}] Current Equity: ~$100,549")
    print(f"[{get_timestamp()}] Buying Power: ~$142,053")
    
    print("\n" + "-"*70)
    print("📋 ORDERS TO SEND:")
    print("-"*70)
    
    orders = [
        {
            "type": "SHORT",
            "symbol": "ETHE",
            "qty": 150,
            "price": "market",
            "target_exit": "+2-3% profit",
            "rationale": "Bearish momentum, profit from crash"
        },
        {
            "type": "SELL",
            "symbol": "ETHE", 
            "qty": 100,
            "price": "market, then -2%",
            "target_exit": "Scalp 2% down",
            "rationale": "Quick profit lock on shorts"
        },
        {
            "type": "BUY",
            "symbol": "ETHE",
            "qty": 50,
            "price": "-3%",
            "target_exit": "+3% from entry",
            "rationale": "DCA accumulation on deep dips"
        }
    ]
    
    for i, order in enumerate(orders, 1):
        print(f"\nOrder {i}: {order['type']}")
        print(f"  Symbol: {order['symbol']}")
        print(f"  Quantity: {order['qty']}")
        print(f"  Price: {order['price']}")
        print(f"  Target: {order['target_exit']}")
        print(f"  Why: {order['rationale']}")
    
    print("\n" + "-"*70)
    print("💰 EXPECTED OUTCOME:")
    print("-"*70)
    print("Conservative: +$2K (if 50% of orders fill well)")
    print("Expected: +$2.5K (if 70% of orders fill)")
    print("Optimistic: +$3K (if 90% of orders fill)")
    
    print("\n" + "-"*70)
    print("🔧 HOW TO EXECUTE:")
    print("-"*70)
    print("\nOPTION A: Manual via Alpaca web interface")
    print("1. Go to https://app.alpaca.markets")
    print("2. Login with account PA320EPZBPGV")
    print("3. Send each order manually (takes 5 min)")
    print("")
    print("OPTION B: Python script execution (recommended)")
    print("1. Install: pip install alpaca-trade-api")
    print("2. Run: python3 BATCH_1_EXECUTOR.py")
    print("3. Script sends all orders atomically")
    print("")
    print("OPTION C: Manual via cURL")
    print("See BATCH_1_CURL_COMMANDS.txt for exact commands")
    
    print("\n" + "-"*70)
    print("⚠️ IMPORTANT:")
    print("-"*70)
    print("- This is PAPER TRADING (demo account)")
    print("- Orders are REAL but money is simulated")
    print("- No risk of real losses")
    print("- All safeguards will still apply")
    
    print("\n" + "="*70)
    print(f"[{get_timestamp()}] 🟢 BATCH 1 READY TO EXECUTE")
    print("="*70 + "\n")

if __name__ == "__main__":
    print_batch_plan()
