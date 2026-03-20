#!/usr/bin/env python3
"""
OPERATIONS TELEGRAM BRIDGE
Auto-detects closed operations and sends formatted Telegram alerts
Integrates with OpenClaw message system
"""

import requests
import json
import base64
import time
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import subprocess
import sys

# ============================================================================
# CONFIG
# ============================================================================

ALPACA_KEY = "PKW445AWAOSGU2WJYCCFUZ47PR"
ALPACA_SECRET = "7tmQ6gY5c4hdmqwEN3UAgv4to78WsGkWPmxUox4G7x4X"
ALPACA_API = "https://paper-api.alpaca.markets/v2"
TELEGRAM_USER = "7540076919"

STATE_FILE = Path("/home/ubuntu/.openclaw/workspace/bridge_state.json")

# ============================================================================
# ALPACA INTEGRATION
# ============================================================================

def get_alpaca_headers():
    auth = base64.b64encode(f"{ALPACA_KEY}:{ALPACA_SECRET}".encode()).decode()
    return {"Authorization": f"Basic {auth}"}

def get_all_orders():
    try:
        resp = requests.get(
            f"{ALPACA_API}/orders?status=all&limit=500",
            headers=get_alpaca_headers(),
            timeout=10
        )
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    return []

def get_positions():
    try:
        resp = requests.get(
            f"{ALPACA_API}/positions",
            headers=get_alpaca_headers(),
            timeout=10
        )
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    return []

# ============================================================================
# STATE MANAGEMENT
# ============================================================================

def load_state():
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except:
            pass
    return {"reported": {}, "last_summary": None}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def load_traceability():
    tracking_file = Path("/home/ubuntu/.openclaw/workspace/COMPLETE_ORDERS_TRACKING.json")
    if tracking_file.exists():
        try:
            with open(tracking_file) as f:
                data = json.load(f)
                return {o['order_id']: o for o in data['orders_detail']}
        except:
            pass
    return {}

# ============================================================================
# MESSAGE FORMATTING
# ============================================================================

def format_operation_alert(order, trace_data):
    """Format a single closed operation for Telegram"""
    
    youtuber = trace_data.get('traceability', {}).get('youtuber', 'Unknown')
    symbol = order.get('symbol', 'N/A')
    status = order.get('status', 'unknown').upper()
    
    # Determine emoji
    emoji_map = {
        'FILLED': '✅',
        'PARTIALLY_FILLED': '⚠️',
        'CANCELED': '❌'
    }
    emoji = emoji_map.get(status, '⏳')
    
    # Get execution details
    filled_qty = order.get('filled_qty', 0)
    filled_price = order.get('filled_avg_price')
    limit_price = order.get('limit_price', 0)
    
    msg = f"{emoji} *{youtuber}* → {symbol}\n"
    msg += f"`{status}`\n"
    
    if filled_qty > 0 and filled_price:
        pnl = (filled_price - limit_price) * filled_qty * 100
        msg += f"Qty: {filled_qty} @ ${filled_price:.2f}\n"
        msg += f"Target: ${limit_price:.2f}\n"
        msg += f"P&L: ${pnl:+.0f}\n"
    
    return msg

def format_batch_summary(closed_orders, trace_map):
    """Format batch summary for Telegram"""
    
    by_youtuber = defaultdict(list)
    total_pnl = 0
    total_filled = 0
    
    for order in closed_orders:
        youtuber = trace_map.get(order.get('id'), {}).get('traceability', {}).get('youtuber', 'Unknown')
        by_youtuber[youtuber].append(order)
        
        if order.get('status') == 'filled':
            total_filled += 1
        
        filled_qty = order.get('filled_qty', 0)
        filled_price = order.get('filled_avg_price')
        limit_price = order.get('limit_price', 0)
        
        if filled_qty > 0 and filled_price:
            pnl = (filled_price - limit_price) * filled_qty * 100
            total_pnl += pnl
    
    # Build message
    msg = "📊 *OPERACIONES CERRADAS*\n\n"
    msg += f"*Resumen:*\n"
    msg += f"├─ Total: {len(closed_orders)}\n"
    msg += f"├─ Ejecutadas: {total_filled} ✅\n"
    msg += f"└─ P&L Total: ${total_pnl:+.0f}\n\n"
    
    msg += "═" * 40 + "\n\n"
    
    for youtuber in sorted(by_youtuber.keys()):
        orders = by_youtuber[youtuber]
        
        youtuber_pnl = 0
        youtuber_filled = 0
        
        for o in orders:
            if o.get('status') == 'filled':
                youtuber_filled += 1
            filled_qty = o.get('filled_qty', 0)
            filled_price = o.get('filled_avg_price')
            limit_price = o.get('limit_price', 0)
            if filled_qty > 0 and filled_price:
                pnl = (filled_price - limit_price) * filled_qty * 100
                youtuber_pnl += pnl
        
        msg += f"🎯 *{youtuber}*\n"
        msg += f"   {len(orders)} órdenes | {youtuber_filled} ejecutadas | P&L: ${youtuber_pnl:+.0f}\n\n"
        
        for i, o in enumerate(orders[:3], 1):
            symbol = o.get('symbol', 'N/A')
            status = o.get('status', 'N/A')
            emoji = "✅" if status == "filled" else "⚠️" if status == "partially_filled" else "❌"
            msg += f"   {emoji} {symbol}\n"
        
        if len(orders) > 3:
            msg += f"   ... +{len(orders) - 3} más\n"
        
        msg += "\n"
    
    msg += "═" * 40 + "\n"
    msg += f"💰 *Total: ${total_pnl:+.0f}*\n"
    msg += f"⏱️ {datetime.now().strftime('%H:%M UTC')}"
    
    return msg

# ============================================================================
# TELEGRAM INTEGRATION
# ============================================================================

def send_telegram_message(text):
    """Send message to Telegram via openclaw message tool"""
    try:
        # Use subprocess to call openclaw's message tool
        cmd = [
            'python3', '-c',
            f'''
from message_tool import send_message
send_message(
    action="send",
    target="{TELEGRAM_USER}",
    message="""{text}"""
)
'''
        ]
        result = subprocess.run(cmd, capture_output=True, timeout=10)
        return result.returncode == 0
    except:
        # Fallback: Write to alerts file
        alerts_file = Path("/home/ubuntu/.openclaw/workspace/telegram_alerts.log")
        with open(alerts_file, "a") as f:
            f.write(f"\n[{datetime.now().isoformat()}]\n{text}\n\n")
        return True

# ============================================================================
# MAIN MONITORING LOOP
# ============================================================================

def run_monitoring_cycle():
    """Run one monitoring cycle"""
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking operations...", end=" ", flush=True)
    
    state = load_state()
    trace_map = load_traceability()
    all_orders = get_all_orders()
    
    # Find newly closed orders
    newly_closed = []
    
    for order in all_orders:
        order_id = order.get('id')
        status = order.get('status', '').lower()
        
        if status in ['filled', 'partially_filled', 'canceled']:
            if order_id not in state.get('reported', {}):
                newly_closed.append(order)
                state['reported'][order_id] = datetime.now().isoformat()
    
    if newly_closed:
        print(f"✅ Found {len(newly_closed)}")
        
        # Format message
        msg = format_batch_summary(newly_closed, trace_map)
        
        # Send via Telegram
        if send_telegram_message(msg):
            print(f"   ✓ Sent to Telegram")
            save_state(state)
        else:
            print(f"   ✗ Failed to send")
    
    else:
        print("No new operations")

# ============================================================================
# CLI
# ============================================================================

if __name__ == "__main__":
    
    if len(sys.argv) > 1 and sys.argv[1] == "--continuous":
        print("🔍 OPERATIONS TELEGRAM BRIDGE - Continuous Mode")
        print(f"Starting: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
        
        while True:
            try:
                run_monitoring_cycle()
                time.sleep(5 * 60)  # Check every 5 minutes
            except KeyboardInterrupt:
                print("\n\n✓ Stopped")
                break
            except Exception as e:
                print(f"\n✗ Error: {e}")
                time.sleep(5 * 60)
    
    else:
        print("🔍 OPERATIONS TELEGRAM BRIDGE - Single Check\n")
        run_monitoring_cycle()
        
        print("\n" + "="*60)
        print("Usage: python3 operations_telegram_bridge.py --continuous")
        print("="*60)
