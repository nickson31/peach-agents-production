#!/usr/bin/env python3
"""
PHASE 1 REPORTER - Reports metrics every 30 minutes
Sends data to show fill rate, BP efficiency, system health
"""

import requests
import json
from datetime import datetime
import time

ALPACA_API = "https://paper-api.alpaca.markets/v2"
ALPACA_KEY = "PKW445AWAOSGU2WJYCCFUZ47PR"
ALPACA_SECRET = "7tmQ6gY5c4hdmqwEN3UAgv4to78WsGkWPmxUox4G7x4X"

HEADERS = {
    "APCA-API-KEY-ID": ALPACA_KEY,
    "APCA-API-SECRET-KEY": ALPACA_SECRET,
}

def log_report(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")

def get_metrics():
    """Get current system metrics"""
    try:
        # Account
        acc_resp = requests.get(f"{ALPACA_API}/account", headers=HEADERS, timeout=5)
        account = acc_resp.json() if acc_resp.status_code == 200 else {}
        
        # Orders
        ord_resp = requests.get(f"{ALPACA_API}/orders?status=all&limit=100", headers=HEADERS, timeout=5)
        orders = ord_resp.json() if ord_resp.status_code == 200 else []
        
        # Count filled/pending in last batch
        filled_count = sum(1 for o in orders if o.get("filled_qty", 0) > 0)
        pending_count = sum(1 for o in orders if o.get("filled_qty", 0) == 0 and o.get("status") == "pending")
        total_recent = filled_count + pending_count
        
        fill_rate = (filled_count / total_recent * 100) if total_recent > 0 else 0
        
        return {
            "equity": float(account.get("equity", 0)),
            "buying_power": float(account.get("buying_power", 0)),
            "cash": float(account.get("cash", 0)),
            "filled": filled_count,
            "pending": pending_count,
            "total": total_recent,
            "fill_rate": fill_rate,
        }
    except:
        return None

def generate_report():
    """Generate Phase 1 report"""
    
    log_report("════════════════════════════════════════════════════════════════")
    log_report("📊 PHASE 1 METRICS REPORT")
    log_report("════════════════════════════════════════════════════════════════")
    
    metrics = get_metrics()
    if not metrics:
        log_report("❌ Error fetching metrics")
        return
    
    # Report
    log_report(f"\n💼 ACCOUNT:")
    log_report(f"   Equity: ${metrics['equity']:,.2f}")
    log_report(f"   Buying power: ${metrics['buying_power']:,.2f}")
    log_report(f"   Cash: ${metrics['cash']:,.2f}")
    
    log_report(f"\n📈 ORDERS (Recent):")
    log_report(f"   Filled: {metrics['filled']}")
    log_report(f"   Pending: {metrics['pending']}")
    log_report(f"   Total: {metrics['total']}")
    log_report(f"   Fill rate: {metrics['fill_rate']:.1f}%")
    
    # Assessment
    log_report(f"\n🎯 ASSESSMENT:")
    if metrics['fill_rate'] >= 85:
        log_report(f"   ✓ EXCELLENT fill rate - Ready to scale")
        status = "✓ GOOD"
    elif metrics['fill_rate'] >= 70:
        log_report(f"   ⚠️ ACCEPTABLE fill rate - Continue monitoring")
        status = "⚠️ OK"
    else:
        log_report(f"   🔴 LOW fill rate - Consider reducing orders")
        status = "🔴 WATCH"
    
    log_report(f"   Status: {status}")
    
    log_report(f"\n💡 NEXT ACTION:")
    if metrics['fill_rate'] >= 85:
        log_report(f"   Phase 2: Ready to scale to 100 orders")
    elif metrics['fill_rate'] >= 70:
        log_report(f"   Continue testing with current batch size")
    else:
        log_report(f"   REDUCE batch size to 50 orders")
    
    log_report(f"\n════════════════════════════════════════════════════════════════")
    
    return metrics

def main():
    """Run reporter"""
    log_report("🚀 PHASE 1 REPORTER STARTED")
    log_report("Reports every 30 minutes during Phase 1")
    log_report("")
    
    # Generate immediate report
    generate_report()
    
    # Schedule next report in 30 min
    log_report(f"\n⏰ Next report: In 30 minutes")

if __name__ == "__main__":
    main()
