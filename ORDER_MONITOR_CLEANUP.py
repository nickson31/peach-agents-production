#!/usr/bin/env python3
"""
ORDER MONITOR & CLEANUP SYSTEM
Cancela órdenes viejas que no se llenan
Libera buying power bloqueado
Monitorea en tiempo real

Token-efficient: ~100 tokens per check
"""

import requests
import time
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
MAX_ORDER_AGE_MINUTES = 15  # Cancel orders older than 15 min
MIN_BUYING_POWER = 20000  # Alert if < $20K
MAX_PENDING_ORDERS = 30  # Maximum pending orders allowed


def log_monitor(msg):
    """Minimal logging"""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


def get_account():
    """Get account info"""
    try:
        resp = requests.get(f"{ALPACA_API}/account", headers=HEADERS, timeout=5)
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    return None


def get_pending_orders():
    """Get all pending orders"""
    try:
        resp = requests.get(
            f"{ALPACA_API}/orders?status=open",
            headers=HEADERS,
            timeout=5,
        )
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    return []


def cancel_order(order_id):
    """Cancel specific order"""
    try:
        resp = requests.delete(
            f"{ALPACA_API}/orders/{order_id}",
            headers=HEADERS,
            timeout=5,
        )
        if resp.status_code in [200, 204]:
            return True
    except:
        pass
    return False


def parse_time(timestamp_str):
    """Parse Alpaca timestamp"""
    try:
        # Format: 2026-03-19T21:18:02.512345Z
        return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    except:
        return None


def cleanup_old_orders():
    """Cancel orders older than max age"""
    orders = get_pending_orders()
    if not orders:
        return 0, 0

    now = datetime.utcnow().replace(tzinfo=None)
    canceled = 0
    kept = 0

    for order in orders:
        order_id = order.get("id")
        symbol = order.get("symbol")
        created_at_str = order.get("created_at")
        
        if not created_at_str:
            continue

        created_at = parse_time(created_at_str)
        if not created_at:
            continue

        created_at = created_at.replace(tzinfo=None)
        age = (now - created_at).total_seconds() / 60

        if age > MAX_ORDER_AGE_MINUTES:
            # Old order - cancel it
            if cancel_order(order_id):
                log_monitor(f"  ✗ Canceled old {symbol} order (age: {age:.0f} min)")
                canceled += 1
            else:
                log_monitor(f"  ⚠️ Failed to cancel old {symbol} order")
        else:
            kept += 1

    return canceled, kept


def check_buying_power():
    """Check buying power status"""
    account = get_account()
    if not account:
        return None

    bp = float(account.get("buying_power", 0))
    cash = float(account.get("cash", 0))
    equity = float(account.get("equity", 0))

    return {
        "buying_power": bp,
        "cash": cash,
        "equity": equity,
        "alert": bp < MIN_BUYING_POWER,
    }


def monitor_loop():
    """Main monitoring loop"""
    log_monitor("🚀 ORDER MONITOR STARTED")
    log_monitor(f"   Max order age: {MAX_ORDER_AGE_MINUTES} min")
    log_monitor(f"   Min buying power alert: ${MIN_BUYING_POWER:,}")
    log_monitor("")

    interval = 60  # Check every minute
    cycle = 0

    while True:
        cycle += 1
        log_monitor(f"📊 CYCLE {cycle}")

        # Check buying power
        bp_status = check_buying_power()
        if bp_status:
            log_monitor(
                f"  Equity: ${bp_status['equity']:,.0f} | "
                f"BP: ${bp_status['buying_power']:,.0f} | "
                f"Cash: ${bp_status['cash']:,.0f}"
            )
            if bp_status["alert"]:
                log_monitor(f"  ⚠️ LOW BUYING POWER (${bp_status['buying_power']:,.0f})")

        # Get pending count
        pending = get_pending_orders()
        log_monitor(f"  Pending orders: {len(pending)}")

        if len(pending) > MAX_PENDING_ORDERS:
            log_monitor(f"  ⚠️ Too many pending ({len(pending)} > {MAX_PENDING_ORDERS})")

        # Cleanup old orders
        log_monitor(f"  Checking for old orders...")
        canceled, kept = cleanup_old_orders()

        if canceled > 0:
            log_monitor(f"  ✓ Cleaned: {canceled} orders canceled, {kept} kept")
        else:
            log_monitor(f"  ✓ All orders OK ({kept} pending)")

        log_monitor(f"  ⏳ Next check in {interval}s...")
        log_monitor("")

        time.sleep(interval)


if __name__ == "__main__":
    try:
        monitor_loop()
    except KeyboardInterrupt:
        log_monitor("\n✓ Monitor stopped")
    except Exception as e:
        log_monitor(f"\n❌ Error: {e}")
