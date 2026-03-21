#!/usr/bin/env python3
"""
Alpaca Background Monitor - OpenClaw Persistent Agent
Monitorea órdenes 24/7 y envía alerts a Telegram
"""

import requests
import json
import base64
import time
import sys
from datetime import datetime
from pathlib import Path

# ============================================================================
# CONFIG
# ============================================================================

ALPACA_KEY = "PKW445AWAOSGU2WJYCCFUZ47PR"
ALPACA_SECRET = "7tmQ6gY5c4hdmqwEN3UAgv4to78WsGkWPmxUox4G7x4X"
ALPACA_API = "https://paper-api.alpaca.markets/v2"

TELEGRAM_USER = "7540076919"
CHECK_INTERVAL = 30  # segundos

STATE_FILE = Path("/home/ubuntu/.openclaw/workspace/monitor_state.json")
ALERTS_FILE = Path("/home/ubuntu/.openclaw/workspace/monitor_alerts.json")

# ============================================================================
# UTILITIES
# ============================================================================

def get_alpaca_headers():
    """Create Alpaca API headers"""
    auth = base64.b64encode(f"{ALPACA_KEY}:{ALPACA_SECRET}".encode()).decode()
    return {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/json"
    }

def get_orders():
    """Fetch all orders from Alpaca"""
    try:
        resp = requests.get(
            f"{ALPACA_API}/orders",
            headers=get_alpaca_headers(),
            timeout=10
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print(f"[ERROR] Could not fetch orders: {e}")
    return []

def get_positions():
    """Fetch all positions from Alpaca"""
    try:
        resp = requests.get(
            f"{ALPACA_API}/positions",
            headers=get_alpaca_headers(),
            timeout=10
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print(f"[ERROR] Could not fetch positions: {e}")
    return []

def load_state():
    """Load monitor state from file"""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except:
            pass
    return {
        "last_check": None,
        "orders_seen": {},
        "alerts_sent": 0,
        "removed_duplicates": 0
    }

def save_state(state):
    """Save monitor state to file"""
    state["last_check"] = datetime.utcnow().isoformat()
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def send_telegram_alert(message: str):
    """Send alert to Telegram"""
    print(f"[ALERT] {message}")
    
    # Save to alerts file
    alerts = []
    if ALERTS_FILE.exists():
        try:
            with open(ALERTS_FILE) as f:
                alerts = json.load(f)
        except:
            pass
    
    alerts.append({
        "timestamp": datetime.utcnow().isoformat(),
        "message": message
    })
    
    # Keep only last 100 alerts
    alerts = alerts[-100:]
    
    with open(ALERTS_FILE, "w") as f:
        json.dump(alerts, f, indent=2)
    
    # TODO: Integrate with OpenClaw message tool
    # For now, just print + save to file

def detect_duplicates(orders):
    """Remove duplicate orders (same symbol, qty, price)"""
    seen = {}
    duplicates = []
    unique = []
    
    for order in orders:
        key = (order['symbol'], order['qty'], order.get('limit_price'))
        if key in seen:
            duplicates.append(order['id'])
        else:
            seen[key] = order['id']
            unique.append(order)
    
    return unique, duplicates

def monitor_orders():
    """Main monitoring loop"""
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║     ALPACA BACKGROUND MONITOR - Started                       ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")
    
    state = load_state()
    
    while True:
        try:
            # 1. Fetch current orders
            orders = get_orders()
            positions = get_positions()
            
            # 2. Detect duplicates
            unique_orders, duplicates = detect_duplicates(orders)
            
            if duplicates:
                print(f"\n[⚠️] Found {len(duplicates)} duplicate orders. Canceling...")
                for order_id in duplicates:
                    try:
                        requests.delete(
                            f"{ALPACA_API}/orders/{order_id}",
                            headers=get_alpaca_headers(),
                            timeout=5
                        )
                        state["removed_duplicates"] += 1
                        send_telegram_alert(f"🗑️ Orden duplicada cancelada: {order_id[:8]}...")
                    except Exception as e:
                        print(f"[ERROR] Could not cancel {order_id}: {e}")
            
            # 3. Check for order status changes
            for order in unique_orders:
                order_id = order['id']
                
                if order_id not in state["orders_seen"]:
                    # New order
                    state["orders_seen"][order_id] = {
                        "symbol": order['symbol'],
                        "qty": order['qty'],
                        "price": order.get('limit_price', 'market'),
                        "status": order['status'],
                        "filled_qty": order.get('filled_qty', 0),
                        "created_at": order['created_at']
                    }
                    
                    send_telegram_alert(
                        f"✅ Orden creada: {order['symbol']} {order['qty']} @ ${order.get('limit_price', 'market')}\n"
                        f"ID: {order_id[:8]}..."
                    )
                    state["alerts_sent"] += 1
                
                else:
                    # Check for status change
                    old_status = state["orders_seen"][order_id]["status"]
                    new_status = order['status']
                    
                    if old_status != new_status:
                        state["orders_seen"][order_id]["status"] = new_status
                        
                        if new_status == "filled":
                            send_telegram_alert(
                                f"🎯 Orden ejecutada: {order['symbol']} {order['qty']} @ ${order.get('filled_avg_price', '?')}\n"
                                f"ID: {order_id[:8]}..."
                            )
                            state["alerts_sent"] += 1
                        
                        elif new_status == "partially_filled":
                            send_telegram_alert(
                                f"⚠️ Ejecución parcial: {order['symbol']} {order.get('filled_qty', 0)}/{order['qty']} @ ${order.get('filled_avg_price', '?')}\n"
                                f"ID: {order_id[:8]}..."
                            )
                            state["alerts_sent"] += 1
                        
                        elif new_status == "canceled":
                            send_telegram_alert(
                                f"❌ Orden cancelada: {order['symbol']} {order['qty']} @ ${order.get('limit_price', 'market')}\n"
                                f"ID: {order_id[:8]}..."
                            )
                            state["alerts_sent"] += 1
            
            # 4. Report positions
            if positions:
                print(f"\n[📊] Posiciones activas: {len(positions)}")
                for pos in positions:
                    print(f"  {pos['symbol']}: {pos['qty']} units | P&L: ${pos.get('unrealized_pl', 0):.2f}")
            
            # 5. Report summary
            print(f"\n[✓] Check completado:")
            print(f"   Órdenes: {len(unique_orders)} activas")
            print(f"   Posiciones: {len(positions)} abiertas")
            print(f"   Duplicados removidos (total): {state['removed_duplicates']}")
            print(f"   Alerts enviados (total): {state['alerts_sent']}")
            print(f"   Próximo check: {CHECK_INTERVAL}s\n")
            
            # 6. Save state
            save_state(state)
            
        except Exception as e:
            print(f"[ERROR] Monitoring error: {e}")
        
        # Wait before next check
        time.sleep(CHECK_INTERVAL)

def show_status():
    """Show current monitoring status"""
    state = load_state()
    
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║     ALPACA MONITOR - STATUS                                   ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")
    
    orders = get_orders()
    positions = get_positions()
    
    print(f"Last check: {state.get('last_check', 'Never')}")
    print(f"Total orders tracked: {len(state['orders_seen'])}")
    print(f"Duplicates removed: {state['removed_duplicates']}")
    print(f"Alerts sent: {state['alerts_sent']}\n")
    
    print(f"Active orders ({len(orders)}):")
    for order in orders[-5:]:
        print(f"  {order['symbol']} {order['qty']} @ ${order.get('limit_price', 'market')} | {order['status']}")
    
    print(f"\nOpen positions ({len(positions)}):")
    for pos in positions:
        print(f"  {pos['symbol']}: {pos['qty']} | P&L: ${pos.get('unrealized_pl', 0):.2f}")
    
    # Show recent alerts
    if ALERTS_FILE.exists():
        with open(ALERTS_FILE) as f:
            alerts = json.load(f)
        
        print(f"\nRecent alerts (last 5):")
        for alert in alerts[-5:]:
            print(f"  {alert['timestamp']}: {alert['message']}")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--status":
            show_status()
        elif sys.argv[1] == "--check-now":
            monitor_orders()
    else:
        # Run in background
        try:
            monitor_orders()
        except KeyboardInterrupt:
            print("\n[✓] Monitor stopped")
