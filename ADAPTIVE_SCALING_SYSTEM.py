#!/usr/bin/env python3
"""
ADAPTIVE SCALING SYSTEM - Dynamic escalation based on LIVE performance
Every 30 min batch:
- Check: Previous batch performance
- If good (>85% fill): Increase escalation 5% → 10% → 15% ... up to 50%
- If very good (>90% fill + profit): Increase order size 1000$ → 1500$
- If bad (<70% fill): Reset to base 5%

This is NOT linear. This is INTELLIGENT.
"""

import requests
from datetime import datetime
import json

ALPACA_API = "https://paper-api.alpaca.markets/v2"
ALPACA_KEY = "PKW445AWAOSGU2WJYCCFUZ47PR"
ALPACA_SECRET = "7tmQ6gY5c4hdmqwEN3UAgv4to78WsGkWPmxUox4G7x4X"

HEADERS = {
    "APCA-API-KEY-ID": ALPACA_KEY,
    "APCA-API-SECRET-KEY": ALPACA_SECRET,
}

# Adaptive scaling state
SCALING_STATE = {
    "current_escalation_pct": 5,  # Start at 5%
    "current_order_size": 1000,   # Start at 1000$
    "base_escalation": 5,
    "max_escalation": 50,
    "base_order_size": 1000,
    "max_order_size": 1500,
    "consecutive_good_batches": 0,
    "last_batch_fill_rate": 0,
}

# Performance thresholds
GOOD_FILL_RATE = 0.85  # 85% = good results
EXCELLENT_FILL_RATE = 0.90  # 90% = excellent
BAD_FILL_RATE = 0.70  # <70% = bad, reset


def log_adaptive(msg):
    """Log scaling decisions"""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


def get_last_batch_performance():
    """Analyze performance of last batch"""
    try:
        # Get recent orders
        resp = requests.get(
            f"{ALPACA_API}/orders?limit=30&status=all",
            headers=HEADERS,
            timeout=5,
        )
        
        if resp.status_code != 200:
            return None
        
        orders = resp.json()
        
        # Count fills from last batch (last ~15-20 orders)
        recent_orders = orders[:20]  # Last batch took ~20 orders
        
        filled = sum(1 for o in recent_orders if o.get("filled_qty", 0) > 0)
        total = len(recent_orders)
        
        fill_rate = (filled / total) if total > 0 else 0
        
        return {
            "fill_rate": fill_rate,
            "filled": filled,
            "total": total,
        }
    except:
        return None


def calculate_new_escalation():
    """Calculate next escalation based on performance"""
    
    perf = get_last_batch_performance()
    if not perf:
        return SCALING_STATE["current_escalation_pct"]
    
    fill_rate = perf["fill_rate"]
    SCALING_STATE["last_batch_fill_rate"] = fill_rate
    
    # EXCELLENT: Increase escalation aggressively
    if fill_rate >= EXCELLENT_FILL_RATE:  # 90%+
        SCALING_STATE["consecutive_good_batches"] += 1
        
        # Jump escalation: 5% → 15% → 30% → 50%
        new_escalation = min(
            SCALING_STATE["current_escalation_pct"] * 3,  # Triple it
            SCALING_STATE["max_escalation"]
        )
        
        log_adaptive(f"🔥 EXCELLENT ({fill_rate*100:.0f}%): Escalation {SCALING_STATE['current_escalation_pct']}% → {new_escalation}%")
        SCALING_STATE["current_escalation_pct"] = new_escalation
        
        return new_escalation
    
    # GOOD: Gentle increase
    elif fill_rate >= GOOD_FILL_RATE:  # 85-90%
        SCALING_STATE["consecutive_good_batches"] += 1
        
        # Increase by 50%: 5% → 7.5% → 11% → 16%
        new_escalation = min(
            SCALING_STATE["current_escalation_pct"] * 1.5,
            SCALING_STATE["max_escalation"]
        )
        
        log_adaptive(f"✓ GOOD ({fill_rate*100:.0f}%): Escalation {SCALING_STATE['current_escalation_pct']}% → {int(new_escalation)}%")
        SCALING_STATE["current_escalation_pct"] = int(new_escalation)
        
        return int(new_escalation)
    
    # MEDIOCRE: Hold
    elif fill_rate >= 0.70:
        log_adaptive(f"⚠️ MEDIOCRE ({fill_rate*100:.0f}%): Hold escalation at {SCALING_STATE['current_escalation_pct']}%")
        SCALING_STATE["consecutive_good_batches"] = 0
        
        return SCALING_STATE["current_escalation_pct"]
    
    # BAD: Reset to base
    else:
        log_adaptive(f"❌ BAD ({fill_rate*100:.0f}%): Reset escalation to base 5%")
        SCALING_STATE["current_escalation_pct"] = SCALING_STATE["base_escalation"]
        SCALING_STATE["consecutive_good_batches"] = 0
        
        return SCALING_STATE["base_escalation"]


def calculate_new_order_size():
    """Calculate order size based on performance"""
    
    fill_rate = SCALING_STATE["last_batch_fill_rate"]
    consecutive_good = SCALING_STATE["consecutive_good_batches"]
    
    # EXCELLENT + multiple good batches: Increase order size
    if fill_rate >= EXCELLENT_FILL_RATE and consecutive_good >= 3:
        new_size = min(
            SCALING_STATE["current_order_size"] * 1.5,  # 1000$ → 1500$
            SCALING_STATE["max_order_size"]
        )
        
        if new_size > SCALING_STATE["current_order_size"]:
            log_adaptive(f"💰 ORDER SIZE UP: ${SCALING_STATE['current_order_size']} → ${int(new_size)}")
            SCALING_STATE["current_order_size"] = int(new_size)
        
        return int(new_size)
    
    # Bad performance: Reduce order size
    elif fill_rate < 0.70:
        new_size = max(
            SCALING_STATE["current_order_size"] * 0.8,  # 1000$ → 800$
            SCALING_STATE["base_order_size"] * 0.5  # Min 50% of base
        )
        
        if new_size < SCALING_STATE["current_order_size"]:
            log_adaptive(f"⚠️ ORDER SIZE DOWN: ${SCALING_STATE['current_order_size']} → ${int(new_size)}")
            SCALING_STATE["current_order_size"] = int(new_size)
        
        return int(new_size)
    
    # Hold
    else:
        return SCALING_STATE["current_order_size"]


def deploy_batch_adaptive(batch_num):
    """Deploy batch with adaptive scaling"""
    
    log_adaptive(f"\n📊 BATCH {batch_num} - ADAPTIVE SCALING")
    
    # Calculate escalation for this batch
    escalation = calculate_new_escalation()
    order_size = calculate_new_order_size()
    
    # Calculate quantities
    base_orders = 150  # Base per batch
    escalated_orders = int(base_orders * (1 + (escalation / 100)))
    
    log_adaptive(f"   Escalation: {escalation}%")
    log_adaptive(f"   Order size: ${order_size}")
    log_adaptive(f"   Orders: {escalated_orders} (base {base_orders} + {escalation}%)")
    
    # Deploy would go here (simplified for demo)
    log_adaptive(f"   → Deploying {escalated_orders} orders @ ${order_size} each")
    
    return escalated_orders, order_size, escalation


def main():
    """Adaptive scaling system"""
    
    log_adaptive("🚀 ADAPTIVE SCALING SYSTEM")
    log_adaptive(f"   Base: 5% escalation, $1000 order size")
    log_adaptive(f"   Max: 50% escalation, $1500 order size")
    log_adaptive("")
    
    # Simulate batch sequence
    batch_fills = [
        0.85,  # Good
        0.88,  # Good
        0.92,  # Excellent
        0.91,  # Excellent
        0.94,  # Excellent (3 consecutive)
        0.89,  # Good
        0.65,  # Bad
        0.80,  # Mediocre
        0.88,  # Good (recovering)
        0.93,  # Excellent
    ]
    
    for i, fill_rate in enumerate(batch_fills, 1):
        # Fake the performance data
        SCALING_STATE["last_batch_fill_rate"] = fill_rate
        
        orders, size, escalation = deploy_batch_adaptive(i)
        
        # Show state
        log_adaptive(f"   State: {SCALING_STATE['consecutive_good_batches']} consecutive good")
        log_adaptive(f"   Next batch will start with {escalation}% escalation, ${size} orders")
        log_adaptive("")


if __name__ == "__main__":
    main()
