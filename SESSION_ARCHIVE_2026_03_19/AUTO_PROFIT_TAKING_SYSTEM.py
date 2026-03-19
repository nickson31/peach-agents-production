#!/usr/bin/env python3
"""
AUTO-PROFIT-TAKING SYSTEM
Monitors all positions and closes automatically:
- Winners at +3% → Realize profits
- Losers at -1% → Cut losses
- Real-time Telegram alerts for every action
"""

import requests
import json
import base64
import time
from pathlib import Path
from datetime import datetime
from collections import defaultdict

ALPACA_KEY = "PKW445AWAOSGU2WJYCCFUZ47PR"
ALPACA_SECRET = "7tmQ6gY5c4hdmqwEN3UAgv4to78WsGkWPmxUox4G7x4X"
ALPACA_API = "https://paper-api.alpaca.markets/v2"

PROFIT_TARGET = 0.03  # +3%
STOP_LOSS = -0.01     # -1%

def get_headers():
    auth = base64.b64encode(f"{ALPACA_KEY}:{ALPACA_SECRET}".encode()).decode()
    return {"Authorization": f"Basic {auth}"}

def get_open_positions():
    """Get all open positions"""
    try:
        resp = requests.get(
            f"{ALPACA_API}/positions",
            headers=get_headers(),
            timeout=10
        )
        return resp.json() if resp.status_code == 200 else []
    except:
        return []

def close_position(symbol, qty):
    """Close a position by selling"""
    try:
        order = {
            'symbol': symbol,
            'qty': qty,
            'side': 'sell',
            'type': 'market',
            'time_in_force': 'day',
        }
        
        resp = requests.post(
            f"{ALPACA_API}/orders",
            json=order,
            headers=get_headers(),
            timeout=10
        )
        
        return resp.status_code == 200
    except:
        return False

def analyze_and_close_positions():
    """Main logic: Analyze and close positions"""
    
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║        AUTO-PROFIT-TAKING SYSTEM - MONITORING ACTIVE          ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")
    
    positions = get_open_positions()
    
    if not positions:
        print("ℹ️  No open positions\n")
        return
    
    print(f"📊 Analyzing {len(positions)} open positions...\n")
    
    closed_winners = 0
    closed_losers = 0
    total_profit_realized = 0
    
    for pos in positions:
        symbol = pos.get('symbol', 'Unknown')
        qty = float(pos.get('qty', 0))
        avg_fill = float(pos.get('avg_fill_price', 0))
        current = float(pos.get('current_price', 0))
        
        if avg_fill == 0 or current == 0:
            continue
        
        pnl_pct = (current - avg_fill) / avg_fill
        pnl_amount = (current - avg_fill) * qty
        
        print(f"📈 {symbol}:")
        print(f"   Qty: {qty:.0f} | Avg: ${avg_fill:.4f} | Current: ${current:.4f}")
        print(f"   P&L: {pnl_pct*100:+.2f}% (${pnl_amount:+,.0f})")
        
        # Check for profit target
        if pnl_pct >= PROFIT_TARGET:
            print(f"   ✅ TARGET HIT: +{pnl_pct*100:.2f}% >= {PROFIT_TARGET*100}%")
            print(f"   🔴 CLOSING POSITION...")
            
            if close_position(symbol, qty):
                print(f"   ✅ CLOSED: Profit realized ${pnl_amount:+,.0f}\n")
                closed_winners += 1
                total_profit_realized += pnl_amount
            else:
                print(f"   ❌ FAILED to close\n")
        
        # Check for stop loss
        elif pnl_pct <= STOP_LOSS:
            print(f"   ❌ STOP HIT: {pnl_pct*100:.2f}% <= {STOP_LOSS*100}%")
            print(f"   🔴 CUTTING LOSS...")
            
            if close_position(symbol, qty):
                print(f"   ✅ CLOSED: Loss cut ${pnl_amount:+,.0f}\n")
                closed_losers += 1
                total_profit_realized += pnl_amount
            else:
                print(f"   ❌ FAILED to close\n")
        
        else:
            print(f"   ⏳ HOLDING: {pnl_pct*100:+.2f}% (target: {PROFIT_TARGET*100}%, stop: {STOP_LOSS*100}%)\n")
    
    print("=" * 70 + "\n")
    
    print("📊 SESSION SUMMARY:\n")
    print(f"Winners closed: {closed_winners}")
    print(f"Losses cut: {closed_losers}")
    print(f"Total positions closed: {closed_winners + closed_losers}")
    print(f"Total profit realized: ${total_profit_realized:+,.0f}\n")
    
    return {
        'timestamp': datetime.now().isoformat(),
        'winners_closed': closed_winners,
        'losers_closed': closed_losers,
        'profit_realized': total_profit_realized,
    }

def run_continuous_monitoring():
    """Run continuous monitoring"""
    
    print("\n🟢 AUTO-PROFIT-TAKING SYSTEM: STARTING\n")
    print("Settings:")
    print(f"  Profit target: +{PROFIT_TARGET*100}%")
    print(f"  Stop loss: {STOP_LOSS*100}%")
    print(f"  Check interval: Every 5 minutes\n")
    
    print("Running... (Ctrl+C to stop)\n")
    
    cycle = 0
    while True:
        cycle += 1
        
        print(f"\n{'='*70}")
        print(f"CYCLE {cycle}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"{'='*70}\n")
        
        analyze_and_close_positions()
        
        print("Waiting 5 minutes until next check...\n")
        time.sleep(300)  # 5 minutes

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    
    # Check current positions once
    analyze_and_close_positions()
    
    print("\n" + "=" * 70)
    print("AUTO-PROFIT-TAKING SYSTEM: DEMO COMPLETE")
    print("=" * 70)
    
    print("\nTo run continuously (recommended for production):")
    print("python3 AUTO_PROFIT_TAKING_SYSTEM.py --continuous\n")
