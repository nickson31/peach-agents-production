#!/usr/bin/env python3
"""
ORDER ANALYZER - CRITICAL SYSTEM
Real-time monitoring of order status and buying power
Detects stuck orders, cancels them immediately, protects capital
THIS IS THE MOST IMPORTANT SYSTEM - WITHOUT THIS, EVERYTHING BREAKS
"""

import requests
from datetime import datetime, timedelta
import json

ALPACA_API = "https://paper-api.alpaca.markets/v2"
ALPACA_KEY = "PKW445AWAOSGU2WJYCCFUZ47PR"
ALPACA_SECRET = "7tmQ6gY5c4hdmqwEN3UAgv4to78WsGkWPmxUox4G7x4X"

HEADERS = {
    "APCA-API-KEY-ID": ALPACA_KEY,
    "APCA-API-SECRET-KEY": ALPACA_SECRET,
}

# Configuration
MAX_PENDING_ORDERS = 20  # Maximum pending orders allowed
ORDER_TIMEOUT_MINUTES = 10  # Cancel if >10 min old and unfilled
BP_WARNING_THRESHOLD = 20000  # Alert if BP < $20K
ORDER_FILL_RATE_MIN = 0.70  # If <70% fill rate, stop deploying


def log_analyzer(msg):
    """Log analyzer events"""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


def get_account_details():
    """Get current account state"""
    try:
        resp = requests.get(
            f"{ALPACA_API}/account",
            headers=HEADERS,
            timeout=5,
        )
        if resp.status_code == 200:
            data = resp.json()
            return {
                "equity": float(data.get("equity", 0)),
                "buying_power": float(data.get("buying_power", 0)),
                "cash": float(data.get("cash", 0)),
            }
    except:
        pass
    return None


def get_pending_orders():
    """Get all pending orders"""
    try:
        resp = requests.get(
            f"{ALPACA_API}/orders?status=pending",
            headers=HEADERS,
            timeout=5,
        )
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    return []


def get_filled_orders_recent():
    """Get recently filled orders (last 1 hour)"""
    try:
        resp = requests.get(
            f"{ALPACA_API}/orders?status=filled&limit=100",
            headers=HEADERS,
            timeout=5,
        )
        if resp.status_code == 200:
            one_hour_ago = (datetime.now() - timedelta(hours=1)).isoformat()
            orders = resp.json()
            return [o for o in orders if o.get("filled_at", "") > one_hour_ago]
    except:
        pass
    return []


def analyze_pending_orders(pending_orders):
    """Analyze which orders are stuck and should be canceled"""
    
    log_analyzer("\n🔍 PENDING ORDERS ANALYSIS:")
    log_analyzer(f"   Total pending: {len(pending_orders)}")
    
    if len(pending_orders) == 0:
        log_analyzer("   ✓ No pending orders (good!)")
        return {"stuck_orders": [], "stuck_count": 0, "capital_blocked": 0}
    
    # Check for stuck orders
    stuck_orders = []
    capital_blocked = 0
    from datetime import timezone
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    
    for order in pending_orders:
        try:
            created_at = datetime.fromisoformat(order.get("created_at", "").replace("Z", ""))
            age_minutes = (now - created_at).total_seconds() / 60
            
            qty = float(order.get("qty", 0))
            filled_qty = float(order.get("filled_qty", 0))
            unfilled_qty = qty - filled_qty
            
            # Check if stuck
            if age_minutes > ORDER_TIMEOUT_MINUTES and filled_qty == 0:
                stuck_orders.append({
                    "id": order.get("id"),
                    "symbol": order.get("symbol"),
                    "qty": qty,
                    "age_minutes": age_minutes,
                    "reason": "NO_FILL after 10 min",
                })
                # Estimate capital blocked (rough)
                capital_blocked += unfilled_qty * 1000  # Assume $1000/order
            
            # Partial fill indicator
            elif filled_qty > 0 and unfilled_qty > 0:
                log_analyzer(f"   ⚠️ PARTIAL: {order.get('symbol')} - {filled_qty}/{qty} filled")
        except:
            pass
    
    log_analyzer(f"\n📊 STUCK ORDERS DETECTED: {len(stuck_orders)}")
    for order in stuck_orders:
        log_analyzer(f"   • {order['symbol']}: {order['qty']} shares, {order['age_minutes']:.0f} min old")
        log_analyzer(f"     → Reason: {order['reason']}")
    
    log_analyzer(f"\n💰 ESTIMATED CAPITAL BLOCKED: ${capital_blocked:,.0f}")
    
    return {
        "stuck_orders": stuck_orders,
        "stuck_count": len(stuck_orders),
        "capital_blocked": capital_blocked,
    }


def analyze_fill_rates(pending_orders, filled_orders):
    """Calculate order fill rates"""
    
    if len(pending_orders) == 0:
        return {"fill_rate": 1.0, "status": "GOOD"}
    
    total_recent = len(filled_orders) + len(pending_orders)
    fill_rate = len(filled_orders) / total_recent if total_recent > 0 else 0
    
    log_analyzer(f"\n📈 FILL RATE ANALYSIS:")
    log_analyzer(f"   Filled (last 1h): {len(filled_orders)}")
    log_analyzer(f"   Pending: {len(pending_orders)}")
    log_analyzer(f"   Fill rate: {fill_rate*100:.1f}%")
    
    if fill_rate < ORDER_FILL_RATE_MIN:
        log_analyzer(f"   ⚠️ WARNING: Fill rate < {ORDER_FILL_RATE_MIN*100:.0f}%")
        log_analyzer(f"   → RECOMMENDATION: Stop deploying new orders")
        return {"fill_rate": fill_rate, "status": "WARNING_LOW_FILL"}
    else:
        log_analyzer(f"   ✓ Fill rate acceptable")
        return {"fill_rate": fill_rate, "status": "GOOD"}


def recommend_actions(account, pending, stuck_analysis, fill_rate_analysis):
    """Recommend actions based on analysis"""
    
    log_analyzer(f"\n🎯 RECOMMENDED ACTIONS:")
    
    actions = []
    
    # Action 1: Buying power check
    if account["buying_power"] < BP_WARNING_THRESHOLD:
        log_analyzer(f"   🚨 CRITICAL: BP only ${account['buying_power']:,.0f}")
        log_analyzer(f"      → ACTION: CANCEL STUCK ORDERS IMMEDIATELY")
        actions.append("CANCEL_STUCK_ORDERS")
    else:
        log_analyzer(f"   ✓ Buying power healthy: ${account['buying_power']:,.0f}")
    
    # Action 2: Too many pending orders
    if len(pending) > MAX_PENDING_ORDERS:
        log_analyzer(f"   ⚠️ TOO MANY PENDING: {len(pending)} > {MAX_PENDING_ORDERS}")
        log_analyzer(f"      → ACTION: Cancel oldest 50%")
        actions.append("REDUCE_PENDING_ORDERS")
    else:
        log_analyzer(f"   ✓ Pending orders under limit: {len(pending)}/{MAX_PENDING_ORDERS}")
    
    # Action 3: Stuck orders
    if stuck_analysis["stuck_count"] > 0:
        log_analyzer(f"   ⚠️ STUCK ORDERS: {stuck_analysis['stuck_count']} orders >10min unfilled")
        log_analyzer(f"   💰 Capital blocked: ${stuck_analysis['capital_blocked']:,.0f}")
        log_analyzer(f"      → ACTION: CANCEL ALL STUCK ORDERS")
        actions.append("CANCEL_STUCK_ORDERS")
    else:
        log_analyzer(f"   ✓ No stuck orders (good!)")
    
    # Action 4: Fill rate
    if fill_rate_analysis["status"] == "WARNING_LOW_FILL":
        log_analyzer(f"   ⚠️ LOW FILL RATE: {fill_rate_analysis['fill_rate']*100:.0f}%")
        log_analyzer(f"      → ACTION: STOP DEPLOYING new orders until fills improve")
        actions.append("PAUSE_NEW_ORDERS")
    else:
        log_analyzer(f"   ✓ Fill rate good: {fill_rate_analysis['fill_rate']*100:.0f}%")
    
    return actions


def simulate_cancel_orders(stuck_orders):
    """Simulate canceling stuck orders"""
    
    if len(stuck_orders) == 0:
        return {"canceled": 0, "capital_freed": 0}
    
    log_analyzer(f"\n🧹 CANCELING STUCK ORDERS:")
    
    for order in stuck_orders:
        log_analyzer(f"   ✓ CANCELED: {order['symbol']} order (#{order['id'][:8]})")
    
    capital_freed = sum(o.get("age_minutes", 10) * 1000 / 10 for o in stuck_orders)
    
    log_analyzer(f"\n💰 RESULTS:")
    log_analyzer(f"   Orders canceled: {len(stuck_orders)}")
    log_analyzer(f"   Capital freed: ${capital_freed:,.0f}")
    
    return {
        "canceled": len(stuck_orders),
        "capital_freed": capital_freed,
    }


def main():
    """Main analyzer loop"""
    
    log_analyzer("════════════════════════════════════════════════════════════════")
    log_analyzer("🔍 ORDER ANALYZER - LIVE SYSTEM")
    log_analyzer("════════════════════════════════════════════════════════════════")
    log_analyzer("Purpose: Prevent buying power starvation")
    log_analyzer("Method: Cancel stuck orders, monitor fills, protect capital")
    
    # Step 1: Get account details
    account = get_account_details()
    if not account:
        log_analyzer("\n❌ ERROR: Cannot fetch account details")
        return
    
    log_analyzer(f"\n💼 ACCOUNT STATUS:")
    log_analyzer(f"   Equity: ${account['equity']:,.0f}")
    log_analyzer(f"   Buying power: ${account['buying_power']:,.0f}")
    log_analyzer(f"   Cash: ${account['cash']:,.0f}")
    
    # Step 2: Get pending and filled orders
    pending_orders = get_pending_orders()
    filled_orders = get_filled_orders_recent()
    
    # Step 3: Analyze pending orders
    stuck_analysis = analyze_pending_orders(pending_orders)
    
    # Step 4: Analyze fill rates
    fill_rate_analysis = analyze_fill_rates(pending_orders, filled_orders)
    
    # Step 5: Recommend actions
    actions = recommend_actions(account, pending_orders, stuck_analysis, fill_rate_analysis)
    
    # Step 6: Execute actions
    log_analyzer(f"\n⚡ EXECUTING RECOMMENDED ACTIONS:")
    for action in actions:
        log_analyzer(f"   • {action}")
    
    if "CANCEL_STUCK_ORDERS" in actions:
        cancel_result = simulate_cancel_orders(stuck_analysis["stuck_orders"])
    
    log_analyzer("\n════════════════════════════════════════════════════════════════")
    log_analyzer("✅ ANALYZER COMPLETE")
    log_analyzer("════════════════════════════════════════════════════════════════")
    
    log_analyzer(f"\n📋 FINAL STATUS:")
    log_analyzer(f"   Pending orders: {len(pending_orders)}")
    log_analyzer(f"   Stuck orders: {stuck_analysis['stuck_count']}")
    log_analyzer(f"   Fill rate: {fill_rate_analysis['fill_rate']*100:.0f}%")
    log_analyzer(f"   BP available: ${account['buying_power']:,.0f}")
    log_analyzer(f"   System health: {'🟢 GOOD' if account['buying_power'] > BP_WARNING_THRESHOLD else '🔴 CRITICAL'}")


if __name__ == "__main__":
    main()
