#!/usr/bin/env python3
"""Check live orders from the Alpaca account"""

import requests
import base64
import json
from datetime import datetime

ALPACA_KEY = "PKW445AWAOSGU2WJYCCFUZ47PR"
ALPACA_SECRET = "7tmQ6gY5c4hdmqwEN3UAgv4to78WsGkWPmxUox4G7x4X"

def alpaca_headers():
    auth = base64.b64encode(f"{ALPACA_KEY}:{ALPACA_SECRET}".encode()).decode()
    return {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/json"
    }

print("\n╔════════════════════════════════════════════════════════════════╗")
print("║          LIVE ORDER VERIFICATION - Alpaca Account             ║")
print("╚════════════════════════════════════════════════════════════════╝\n")

# Get all orders
try:
    resp = requests.get(
        "https://paper-api.alpaca.markets/v2/orders",
        headers=alpaca_headers(),
        timeout=10
    )
    
    if resp.status_code == 200:
        orders = resp.json()
        print(f"[✓] Found {len(orders)} orders in account\n")
        
        # Show recent orders
        for i, order in enumerate(orders[-5:], 1):
            print(f"Order {i}:")
            print(f"  ID: {order['id']}")
            print(f"  Symbol: {order['symbol']}")
            print(f"  Qty: {order['qty']}")
            print(f"  Price: ${order['limit_price']}")
            print(f"  Side: {order['side']}")
            print(f"  Status: {order['status']}")
            print(f"  Created: {order['created_at']}")
            print()
    else:
        print(f"[!] Error getting orders: {resp.status_code}")
except Exception as e:
    print(f"[!] Exception: {e}")

# Get account details
try:
    resp = requests.get(
        "https://paper-api.alpaca.markets/v2/account",
        headers=alpaca_headers(),
        timeout=10
    )
    
    if resp.status_code == 200:
        account = resp.json()
        print("="*70)
        print("ACCOUNT STATUS")
        print("="*70)
        print(f"Account: {account.get('account_number')}")
        print(f"Cash: ${float(account.get('cash', 0)):,.2f}")
        print(f"Buying Power: ${float(account.get('buying_power', 0)):,.2f}")
        print(f"Portfolio Value: ${float(account.get('portfolio_value', 0)):,.2f}")
        print(f"Status: {account.get('status')}")
except Exception as e:
    print(f"[!] Error: {e}")

print("\n[✓] Verification Complete\n")
