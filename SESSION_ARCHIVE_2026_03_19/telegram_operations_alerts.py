#!/usr/bin/env python3
"""
TELEGRAM OPERATIONS ALERTS
Detecta operaciones cerradas y envía alertas formatadas a Telegram
Integración con OpenClaw message system
"""

import requests
import json
import base64
import time
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ============================================================================
# CONFIG
# ============================================================================

ALPACA_KEY = "PKW445AWAOSGU2WJYCCFUZ47PR"
ALPACA_SECRET = "7tmQ6gY5c4hdmqwEN3UAgv4to78WsGkWPmxUox4G7x4X"
ALPACA_API = "https://paper-api.alpaca.markets/v2"
TELEGRAM_USER = "7540076919"

STATE_FILE = Path("/home/ubuntu/.openclaw/workspace/telegram_alerts_state.json")

# ============================================================================
# UTILITIES
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

def load_state():
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except:
            pass
    return {"reported_orders": {}}

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

def format_telegram_message(closed_orders):
    """Format message for Telegram (supports markdown)"""
    
    if not closed_orders:
        return None
    
    # Group by YouTuber
    by_youtuber = defaultdict(list)
    total_pnl = 0
    total_filled = 0
    
    for order in closed_orders:
        youtuber = order.get('traceability', {}).get('youtuber', 'Unknown')
        by_youtuber[youtuber].append(order)
        
        # Calculate P&L
        filled_qty = order.get('execution', {}).get('filled_qty', 0)
        filled_price = order.get('execution', {}).get('filled_avg_price')
        limit_price = order.get('limit_price', 0)
        
        if filled_qty > 0:
            total_filled += 1
            if filled_price:
                pnl = (filled_price - limit_price) * filled_qty * 100
                total_pnl += pnl
    
    # Build message
    msg = "📊 *OPERACIONES EJECUTADAS*\n\n"
    msg += f"Total cerradas: {len(closed_orders)}\n"
    msg += f"Ejecutadas: {total_filled}\n"
    msg += f"P&L Total: ${total_pnl:+.0f}\n\n"
    
    msg += "═" * 40 + "\n\n"
    
    for youtuber in sorted(by_youtuber.keys()):
        orders = by_youtuber[youtuber]
        msg += f"🎯 *{youtuber}*\n"
        msg += f"   {len(orders)} operaciones\n\n"
        
        for i, order in enumerate(orders[:5], 1):  # Mostrar primeras 5
            symbol = order.get('symbol', 'N/A')
            status = order.get('status', 'N/A')
            filled_qty = order.get('execution', {}).get('filled_qty', 0)
            filled_price = order.get('execution', {}).get('filled_avg_price')
            limit_price = order.get('limit_price', 0)
            
            # Determine emoji
            if status == 'filled':
                emoji = "✅"
            elif status == 'partially_filled':
                emoji = "⚠️"
            elif status == 'canceled':
                emoji = "❌"
            else:
                emoji = "⏳"
            
            msg += f"   {emoji} {symbol}"
            
            if filled_price:
                diff = filled_price - limit_price
                pnl = diff * filled_qty * 100
                if diff >= 0:
                    msg += f" +${pnl:.0f}"
                else:
                    msg += f" -${abs(pnl):.0f}"
            
            msg += f"\n"
        
        if len(orders) > 5:
            msg += f"   ... +{len(orders) - 5} más\n"
        
        msg += "\n"
    
    msg += "═" * 40 + "\n"
    msg += f"💰 *Total: ${total_pnl:+.0f}*\n"
    msg += f"⏱️ {datetime.now().strftime('%H:%M:%S UTC')}"
    
    return msg

def format_simple_alert(order):
    """Format single order alert (quick notification)"""
    
    youtuber = order.get('traceability', {}).get('youtuber', 'Unknown')
    symbol = order.get('symbol', 'N/A')
    status = order.get('status', 'N/A')
    filled_price = order.get('execution', {}).get('filled_avg_price')
    limit_price = order.get('limit_price', 0)
    filled_qty = order.get('execution', {}).get('filled_qty', 0)
    
    emoji = "✅" if status == "filled" else "⚠️" if status == "partially_filled" else "❌"
    
    msg = f"{emoji} *{youtuber}* - {symbol}\n"
    msg += f"`{status.upper()}`\n"
    
    if filled_price and filled_qty > 0:
        pnl = (filled_price - limit_price) * filled_qty * 100
        msg += f"P&L: ${pnl:+.0f}"
    
    return msg

def check_and_alert():
    """Check for closed operations and prepare alerts"""
    
    state = load_state()
    traceability = load_traceability()
    all_orders = get_all_orders()
    
    # Find newly closed orders
    newly_closed = []
    
    for order in all_orders:
        order_id = order.get('id')
        status = order.get('status', '').lower()
        
        # Check if closed and not yet reported
        if status in ['filled', 'partially_filled', 'canceled']:
            if order_id not in state.get('reported_orders', {}):
                # Add traceability
                order_with_trace = {
                    **order,
                    'traceability': traceability.get(order_id, {})
                }
                newly_closed.append(order_with_trace)
                
                # Mark as reported
                state['reported_orders'][order_id] = {
                    'status': status,
                    'timestamp': datetime.now().isoformat()
                }
    
    if newly_closed:
        save_state(state)
    
    return newly_closed

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import sys
    
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║     TELEGRAM OPERATIONS ALERTS - Ready to Send                 ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")
    
    # Check for closed operations
    closed_ops = check_and_alert()
    
    if closed_ops:
        print(f"✅ Found {len(closed_ops)} newly closed operations\n")
        
        # Generate formatted message
        formatted_msg = format_telegram_message(closed_ops)
        
        if formatted_msg:
            print("MESSAGE TO SEND TO TELEGRAM:\n")
            print("=" * 70)
            print(formatted_msg)
            print("=" * 70)
            
            # In production, this would be sent via OpenClaw message tool
            print("\n✓ Ready to send via Telegram")
            print(f"  Recipient: {TELEGRAM_USER}")
            print(f"  Format: Markdown (Telegram compatible)")
            
            # Optional: Show individual alerts
            print(f"\nIndividual alerts ({len(closed_ops)} total):")
            for order in closed_ops[:3]:
                print(f"\n{format_simple_alert(order)}")
                print("-" * 40)
    
    else:
        print("No newly closed operations found.")
        print("\nTo use in production, run with --continuous flag:")
        print("python3 telegram_operations_alerts.py --continuous")
