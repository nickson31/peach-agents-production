#!/usr/bin/env python3
"""
CLOSED OPERATIONS ALERT
Detecta órdenes ejecutadas/cerradas y envía reporte a Telegram
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

STATE_FILE = Path("/home/ubuntu/.openclaw/workspace/operations_state.json")
ALERTS_FILE = Path("/home/ubuntu/.openclaw/workspace/closed_operations_alerts.json")

# ============================================================================
# UTILITIES
# ============================================================================

def get_alpaca_headers():
    auth = base64.b64encode(f"{ALPACA_KEY}:{ALPACA_SECRET}".encode()).decode()
    return {"Authorization": f"Basic {auth}"}

def get_all_orders():
    """Fetch all orders from Alpaca"""
    try:
        resp = requests.get(
            f"{ALPACA_API}/orders?status=all&limit=500",
            headers=get_alpaca_headers(),
            timeout=10
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print(f"[ERROR] Could not fetch orders: {e}")
    return []

def load_state():
    """Load tracking state"""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except:
            pass
    return {"last_report": {}, "alerts_sent": 0}

def save_state(state):
    """Save tracking state"""
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def save_alert(alert):
    """Save alert to file"""
    alerts = []
    if ALERTS_FILE.exists():
        try:
            with open(ALERTS_FILE) as f:
                alerts = json.load(f)
        except:
            pass
    
    alerts.append(alert)
    
    # Keep only last 100
    alerts = alerts[-100:]
    
    with open(ALERTS_FILE, "w") as f:
        json.dump(alerts, f, indent=2)

def load_traceability_data():
    """Load orden-to-YouTuber mapping"""
    tracking_file = Path("/home/ubuntu/.openclaw/workspace/COMPLETE_ORDERS_TRACKING.json")
    if tracking_file.exists():
        try:
            with open(tracking_file) as f:
                data = json.load(f)
                return {o['order_id']: o for o in data['orders_detail']}
        except:
            pass
    return {}

def format_message_columnar(closed_orders):
    """Format message in columns"""
    
    if not closed_orders:
        return None
    
    # Build header
    msg = "📊 **OPERACIONES CERRADAS**\n\n"
    msg += "```\n"
    msg += f"{'#':<4} {'YouTuber':<20} {'Symbol':<6} {'Status':<10} {'P&L':<10}\n"
    msg += "-" * 60 + "\n"
    
    total_pnl = 0
    
    for idx, order in enumerate(closed_orders, 1):
        youtuber = order.get('traceability', {}).get('youtuber', 'Unknown')[:18]
        symbol = order.get('symbol', 'N/A')
        status = order.get('status', 'N/A')
        
        # Calculate P&L
        filled_qty = order.get('execution', {}).get('filled_qty', 0)
        filled_price = order.get('execution', {}).get('filled_avg_price')
        limit_price = order.get('limit_price', 0)
        
        if filled_qty > 0 and filled_price:
            pnl = (filled_price - limit_price) * filled_qty * 100  # Simplified
            total_pnl += pnl
            pnl_str = f"${pnl:+.0f}"
        else:
            pnl_str = "N/A"
        
        msg += f"{idx:<4} {youtuber:<20} {symbol:<6} {status:<10} {pnl_str:<10}\n"
    
    msg += "-" * 60 + "\n"
    msg += f"{'TOTAL':<30} {'':6} {'':10} ${total_pnl:+.0f}\n"
    msg += "```\n"
    
    return msg

def format_message_paragraph(closed_orders):
    """Format message in paragraph style"""
    
    if not closed_orders:
        return None
    
    msg = "📊 **OPERACIONES CERRADAS**\n\n"
    
    by_youtuber = defaultdict(list)
    total_pnl = 0
    
    for order in closed_orders:
        youtuber = order.get('traceability', {}).get('youtuber', 'Unknown')
        by_youtuber[youtuber].append(order)
        
        # Simple P&L calc
        filled_qty = order.get('execution', {}).get('filled_qty', 0)
        filled_price = order.get('execution', {}).get('filled_avg_price', 0)
        limit_price = order.get('limit_price', 0)
        
        if filled_qty > 0 and filled_price:
            pnl = (filled_price - limit_price) * filled_qty * 100
            total_pnl += pnl
    
    for youtuber, orders in sorted(by_youtuber.items()):
        msg += f"🎯 **{youtuber}** ({len(orders)} operaciones)\n"
        
        for order in orders[:3]:  # Mostrar primeras 3
            symbol = order.get('symbol', 'N/A')
            status = order.get('status', 'N/A')
            filled_price = order.get('execution', {}).get('filled_avg_price')
            limit_price = order.get('limit_price', 0)
            
            if filled_price:
                diff = filled_price - limit_price
                emoji = "✅" if diff >= 0 else "❌"
                msg += f"  {emoji} {symbol}: ${filled_price} (target: ${limit_price})\n"
            else:
                msg += f"  ⏳ {symbol}: {status}\n"
        
        msg += "\n"
    
    msg += f"💰 **Total P&L**: ${total_pnl:+.0f}\n"
    
    return msg

def check_and_alert_closed_operations():
    """Main monitoring function"""
    
    print("🔄 Checking for closed operations...\n")
    
    # Load current state and traceability
    state = load_state()
    traceability = load_traceability_data()
    
    # Get all orders
    all_orders = get_all_orders()
    
    # Filter closed/filled orders
    closed_statuses = ['filled', 'partially_filled', 'canceled']
    newly_closed = []
    
    for order in all_orders:
        order_id = order.get('id')
        status = order.get('status', '').lower()
        
        if status in closed_statuses:
            # Check if this is new (not reported before)
            if order_id not in state.get('last_report', {}):
                # Add traceability info
                order_with_trace = {
                    **order,
                    'traceability': traceability.get(order_id, {})
                }
                newly_closed.append(order_with_trace)
                
                # Mark as reported
                state['last_report'][order_id] = {
                    'status': status,
                    'timestamp': datetime.now().isoformat(),
                    'reported': True
                }
    
    # Save state
    if newly_closed:
        save_state(state)
    
    # Generate messages
    if newly_closed:
        print(f"✅ Found {len(newly_closed)} newly closed operations\n")
        
        # Format as columns
        columnar_msg = format_message_columnar(newly_closed)
        
        # Format as paragraph
        paragraph_msg = format_message_paragraph(newly_closed)
        
        # Save alerts
        for order in newly_closed:
            save_alert({
                'timestamp': datetime.now().isoformat(),
                'order_id': order.get('id'),
                'symbol': order.get('symbol'),
                'status': order.get('status'),
                'youtuber': order.get('traceability', {}).get('youtuber', 'Unknown')
            })
        
        return {
            'found': len(newly_closed),
            'columnar': columnar_msg,
            'paragraph': paragraph_msg,
            'orders': newly_closed
        }
    
    return None

def send_telegram_alert(message_text):
    """
    Send alert to Telegram via OpenClaw message system
    (This would be called via the message tool)
    """
    print("📤 Message ready to send to Telegram:\n")
    print(message_text)
    return message_text

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--continuous":
        # Run in continuous monitoring mode
        print("🔍 Starting continuous monitoring (Ctrl+C to stop)\n")
        
        while True:
            result = check_and_alert_closed_operations()
            
            if result:
                print(f"\n{'='*70}")
                print("📊 OPERACIONES CERRADAS DETECTADAS")
                print(f"{'='*70}\n")
                
                # Print both formats
                print(result['columnar'])
                print("\n--- FORMATO PÁRRAFO ---\n")
                print(result['paragraph'])
                
                # In production, this would be sent via OpenClaw message tool
                # For now, we just print
            
            # Wait before next check
            time.sleep(60)  # Check every minute
    
    else:
        # Single check mode
        result = check_and_alert_closed_operations()
        
        if result:
            print(f"\n{'='*70}")
            print("📊 OPERACIONES CERRADAS")
            print(f"{'='*70}\n")
            print(result['columnar'])
        else:
            print("No newly closed operations found.")
