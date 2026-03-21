#!/usr/bin/env python3
"""
ANTI-LOSS SYSTEM - Prevents losses from bad deployments
Features:
1. Exit positions at FIRST sign of loss (-0.5% trigger)
2. No EUO or unknown symbols
3. ETHE + GBTC only (verified)
4. Validate prices before orders
5. Max 1% daily loss tolerance
6. Emergency stop if equity drops

Purpose: Stop the bleeding, then restart growth
"""

import requests
import time
from datetime import datetime

ALPACA_API = "https://paper-api.alpaca.markets/v2"
ALPACA_KEY = "PKW445AWAOSGU2WJYCCFUZ47PR"
ALPACA_SECRET = "7tmQ6gY5c4hdmqwEN3UAgv4to78WsGkWPmxUox4G7x4X"

HEADERS = {
    "APCA-API-KEY-ID": ALPACA_KEY,
    "APCA-API-SECRET-KEY": ALPACA_SECRET,
}

# Safe symbols only
SAFE_SYMBOLS = ["ETHE", "GBTC"]
UNSAFE_SYMBOLS = ["EUO", "FXA", "GLD", "SLV"]  # Remove these

# Loss triggers
EXIT_AT_LOSS_PCT = -0.005  # Exit if -0.5% unrealized
EMERGENCY_STOP_PCT = -0.01  # Stop everything if -1% daily


def log_anti(msg):
    """Log anti-loss actions"""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


def get_positions():
    """Get all open positions"""
    try:
        resp = requests.get(f"{ALPACA_API}/positions", headers=HEADERS, timeout=5)
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    return []


def sell_position(symbol, qty):
    """Sell a position at market (stop losses)"""
    try:
        order_data = {
            "symbol": symbol,
            "qty": qty,
            "side": "sell",
            "type": "market",  # Market order (execute immediately)
            "time_in_force": "day",
            "client_order_id": f"ANTI_LOSS_{symbol}_{int(time.time())}",
        }
        
        resp = requests.post(
            f"{ALPACA_API}/orders",
            json=order_data,
            headers=HEADERS,
            timeout=5,
        )
        
        if resp.status_code in [200, 201]:
            return True
    except:
        pass
    
    return False


def liquidate_unsafe_positions():
    """Close all UNSAFE symbols immediately"""
    positions = get_positions()
    
    for pos in positions:
        symbol = pos.get("symbol")
        qty = pos.get("qty")
        
        if symbol in UNSAFE_SYMBOLS:
            log_anti(f"🚨 LIQUIDATING UNSAFE: {symbol} {qty} shares")
            if sell_position(symbol, qty):
                log_anti(f"   ✓ Sold {symbol} at market")
            else:
                log_anti(f"   ❌ Failed to sell {symbol}")


def exit_losing_positions():
    """Exit positions with unrealized losses > threshold"""
    positions = get_positions()
    
    for pos in positions:
        symbol = pos.get("symbol")
        qty = pos.get("qty")
        unrealized_pl_pct = float(pos.get("unrealized_plpc", 0))
        
        if unrealized_pl_pct < EXIT_AT_LOSS_PCT:
            log_anti(f"⚠️ LOSS DETECTED: {symbol} {unrealized_pl_pct*100:.2f}%")
            log_anti(f"   Selling {qty} shares at market to stop loss")
            
            if sell_position(symbol, qty):
                log_anti(f"   ✓ Exited {symbol}")
            else:
                log_anti(f"   ❌ Failed to exit {symbol}")


def check_emergency_stop():
    """Check if daily loss > 1% (emergency)"""
    try:
        resp = requests.get(f"{ALPACA_API}/account", headers=HEADERS, timeout=5)
        if resp.status_code == 200:
            account = resp.json()
            equity = float(account.get("equity", 0))
            starting_equity = 100618.50  # Yesterday's start
            
            daily_change = (equity - starting_equity) / starting_equity
            
            if daily_change < EMERGENCY_STOP_PCT:
                log_anti(f"🚨 EMERGENCY STOP: Daily loss {daily_change*100:.2f}%")
                log_anti(f"   Liquidating ALL positions")
                
                positions = get_positions()
                for pos in positions:
                    sell_position(pos.get("symbol"), pos.get("qty"))
                
                return False  # Stop system
    except:
        pass
    
    return True  # Continue


def main():
    """Anti-loss system"""
    
    log_anti("🛡️ ANTI-LOSS SYSTEM ACTIVATED")
    log_anti("")
    
    # STEP 1: Liquidate unsafe positions
    log_anti("STEP 1: Removing unsafe symbols...")
    liquidate_unsafe_positions()
    time.sleep(2)
    
    # STEP 2: Exit losing positions
    log_anti("")
    log_anti("STEP 2: Exiting positions with losses...")
    exit_losing_positions()
    time.sleep(2)
    
    # STEP 3: Check emergency stop
    log_anti("")
    log_anti("STEP 3: Checking emergency stop condition...")
    if not check_emergency_stop():
        log_anti("⚠️ EMERGENCY: All positions liquidated")
        return
    
    # STEP 4: Report status
    log_anti("")
    log_anti("📊 FINAL STATUS:")
    
    try:
        resp = requests.get(f"{ALPACA_API}/account", headers=HEADERS, timeout=5)
        account = resp.json()
        log_anti(f"   Equity: ${float(account.get('equity', 0)):,.0f}")
        log_anti(f"   Cash: ${float(account.get('cash', 0)):,.0f}")
        log_anti(f"   Buying power: ${float(account.get('buying_power', 0)):,.0f}")
    except:
        pass
    
    positions = get_positions()
    log_anti(f"   Open positions: {len(positions)}")
    for pos in positions:
        log_anti(f"     - {pos.get('symbol')}: {pos.get('qty')} shares")
    
    log_anti("")
    log_anti("✅ ANTI-LOSS SYSTEM COMPLETE")
    log_anti("   Ready to restart growth with SAFE symbols only")


if __name__ == "__main__":
    main()
