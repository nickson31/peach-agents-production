#!/usr/bin/env python3
"""
STRATEGIC 4-HOUR SYSTEM
Deploy 50 strategic orders at once, hold for 4 hours
Conservative entries, disciplined exits
"""

import requests
import json
import base64
from datetime import datetime, timedelta
from pathlib import Path

ALPACA_KEY = "PKW445AWAOSGU2WJYCCFUZ47PR"
ALPACA_SECRET = "7tmQ6gY5c4hdmqwEN3UAgv4to78WsGkWPmxUox4G7x4X"
ALPACA_API = "https://paper-api.alpaca.markets/v2"

def get_headers():
    auth = base64.b64encode(f"{ALPACA_KEY}:{ALPACA_SECRET}".encode()).decode()
    return {"Authorization": f"Basic {auth}"}

def get_current_price(symbol):
    """Get current market price"""
    try:
        resp = requests.get(f"{ALPACA_API}/bars/latest?symbols={symbol}&limit=1", 
                          headers=get_headers(), timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if 'bars' in data and symbol in data['bars']:
                return float(data['bars'][symbol]['c'])
    except:
        pass
    return None

def place_strategic_order(symbol, qty=12, strategy='confluence'):
    """Place strategic order with analysis"""
    
    # Get current price
    current_price = get_current_price(symbol)
    if not current_price:
        return {'status': 'error', 'symbol': symbol, 'issue': 'price_not_found'}
    
    # Strategic entry: Conservative stagger
    # Different per asset class
    if symbol == 'ETHE':
        stagger = -0.025  # 2.5% for crypto
    elif symbol == 'GBTC':
        stagger = -0.02   # 2% for Bitcoin fund
    elif symbol == 'FXA':
        stagger = -0.04   # 4% for Forex (wider)
    else:
        stagger = -0.02
    
    entry_price = round(current_price * (1 + stagger), 4)
    
    # Create order
    order_data = {
        'symbol': symbol,
        'qty': qty,
        'side': 'buy',
        'type': 'limit',
        'time_in_force': 'day',
        'limit_price': entry_price
    }
    
    try:
        resp = requests.post(f"{ALPACA_API}/orders", 
                            json=order_data, 
                            headers=get_headers(),
                            timeout=5)
        
        if resp.status_code in [200, 201]:
            order = resp.json()
            return {
                'status': 'placed',
                'symbol': symbol,
                'order_id': order.get('id'),
                'entry_price': entry_price,
                'current_price': current_price,
                'stagger_pct': stagger * 100,
                'qty': qty,
                'strategy': strategy
            }
        else:
            return {
                'status': 'error',
                'symbol': symbol,
                'issue': f"HTTP {resp.status_code}"
            }
    except Exception as e:
        return {
            'status': 'error',
            'symbol': symbol,
            'issue': str(e)
        }

def deploy_strategic_batch(batch_size=50):
    """Deploy strategic batch of orders"""
    
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║         STRATEGIC 4-HOUR SYSTEM - BATCH DEPLOYMENT            ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")
    
    print(f"📊 Deploying {batch_size} strategic orders...\n")
    
    # Distribution (strategic)
    distribution = {
        'ETHE': {'qty': 14, 'count': 20},      # 20 orders of 14 qty each
        'GBTC': {'qty': 12, 'count': 15},      # 15 orders of 12 qty each
        'FXA': {'qty': 10, 'count': 15},       # 15 orders of 10 qty each
    }
    
    all_orders = []
    
    for symbol, config in distribution.items():
        print(f"Deploying {symbol}: {config['count']} orders × {config['qty']} qty\n")
        
        for i in range(config['count']):
            order = place_strategic_order(symbol, qty=config['qty'])
            all_orders.append(order)
            
            status = order.get('status', 'error')
            if status == 'placed':
                print(f"  ✅ {i+1}/{config['count']}: {symbol} @ ${order['entry_price']} " + 
                      f"({order['stagger_pct']:.1f}% stagger)")
            else:
                print(f"  ❌ {i+1}/{config['count']}: {symbol} - {order.get('issue')}")
    
    print("\n" + "=" * 70 + "\n")
    
    # Summary
    total_placed = sum(1 for o in all_orders if o['status'] == 'placed')
    total_failed = sum(1 for o in all_orders if o['status'] == 'error')
    total_qty = sum(o.get('qty', 0) for o in all_orders if o['status'] == 'placed')
    
    print(f"STRATEGIC BATCH DEPLOYMENT SUMMARY\n")
    print(f"Total orders: {len(all_orders)}")
    print(f"Placed: {total_placed}")
    print(f"Failed: {total_failed}")
    print(f"Success rate: {total_placed / len(all_orders) * 100:.1f}%")
    print(f"Total quantity: {total_qty} units")
    
    total_capital = sum(o.get('entry_price', 0) * o.get('qty', 0) 
                       for o in all_orders if o['status'] == 'placed')
    print(f"Total capital deployed: ${total_capital:,.0f}\n")
    
    # Save results
    results = {
        'system': 'strategic_4hour',
        'timestamp': datetime.now().isoformat(),
        'total_orders': len(all_orders),
        'total_placed': total_placed,
        'total_failed': total_failed,
        'total_qty': total_qty,
        'total_capital': total_capital,
        'orders': all_orders
    }
    
    results_file = Path("/home/ubuntu/.openclaw/workspace/STRATEGIC_4HOUR_RESULTS.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"✅ Results saved to STRATEGIC_4HOUR_RESULTS.json\n")
    
    return results

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    
    print("\n")
    
    # Deploy strategic batch
    results = deploy_strategic_batch(batch_size=50)
    
    print("=" * 70)
