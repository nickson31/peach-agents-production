#!/usr/bin/env python3
"""
SCALPING 60-SECOND SYSTEM
Deploy 10 orders every 60 seconds for 4 hours
Aggressive entries, fast exits
"""

import requests
import json
import base64
import time
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

def place_scalping_order(symbol, qty=5, direction='buy'):
    """Place aggressive scalping order"""
    
    # Get current price
    current_price = get_current_price(symbol)
    if not current_price:
        return {'status': 'error', 'symbol': symbol, 'issue': 'price_not_found'}
    
    # Aggressive entry: 0.5-1% below for buy, above for sell
    if direction == 'buy':
        entry_price = round(current_price * 0.995, 4)  # 0.5% aggressive
    else:
        entry_price = round(current_price * 1.005, 4)
    
    # Create order
    order_data = {
        'symbol': symbol,
        'qty': qty,
        'side': direction,
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
                'qty': qty,
                'direction': direction
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

def scalping_cycle(cycle_num):
    """One 60-second scalping cycle"""
    
    symbols = ['ETHE', 'GBTC', 'FXA']  # Focus on best performers
    orders_placed = []
    
    print(f"\n🔴 CYCLE #{cycle_num} - Scalping 60 seconds")
    print(f"   Time: {datetime.now().strftime('%H:%M:%S')}\n")
    
    for i, symbol in enumerate(symbols):
        # Alternate buy/sell
        direction = 'buy' if i % 2 == 0 else 'sell'
        
        order = place_scalping_order(symbol, qty=5, direction=direction)
        orders_placed.append(order)
        
        status = order.get('status', 'error')
        if status == 'placed':
            print(f"   ✅ {symbol}: {direction.upper()} @ ${order['entry_price']}")
        else:
            print(f"   ❌ {symbol}: {order.get('issue')}")
    
    return orders_placed

def run_scalping_system(duration_seconds=14400):  # 4 hours
    """Run scalping system for 4 hours (240 cycles × 60 seconds)"""
    
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║           SCALPING 60-SECOND SYSTEM - 4 HOUR TEST             ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")
    
    start_time = time.time()
    cycle_num = 0
    all_orders = []
    
    while time.time() - start_time < duration_seconds:
        cycle_num += 1
        
        # Run cycle
        orders = scalping_cycle(cycle_num)
        all_orders.extend(orders)
        
        # Count summary
        placed = sum(1 for o in orders if o['status'] == 'placed')
        failed = sum(1 for o in orders if o['status'] == 'error')
        
        print(f"   Summary: {placed} placed, {failed} failed")
        print(f"   Total so far: {sum(1 for o in all_orders if o['status'] == 'placed')} orders placed\n")
        
        # Wait 60 seconds before next cycle
        print(f"   ⏳ Waiting 60 seconds until next cycle...")
        time.sleep(60)
        
        # Safety: max 10 cycles for testing (600 seconds = 10 minutes)
        if cycle_num >= 10:
            print(f"\n   ⚠️  Stopping after {cycle_num} cycles (testing mode)")
            break
    
    print("\n" + "=" * 70 + "\n")
    
    # Summary
    total_placed = sum(1 for o in all_orders if o['status'] == 'placed')
    total_failed = sum(1 for o in all_orders if o['status'] == 'error')
    
    print(f"SCALPING 60-SECOND SYSTEM COMPLETE\n")
    print(f"Total cycles: {cycle_num}")
    print(f"Total orders placed: {total_placed}")
    print(f"Total failed: {total_failed}")
    print(f"Success rate: {total_placed / (total_placed + total_failed) * 100:.1f}%\n")
    
    # Save results
    results = {
        'system': 'scalping_60sec',
        'timestamp': datetime.now().isoformat(),
        'cycles': cycle_num,
        'total_placed': total_placed,
        'total_failed': total_failed,
        'orders': all_orders
    }
    
    results_file = Path("/home/ubuntu/.openclaw/workspace/SCALPING_60SEC_RESULTS.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"✅ Results saved to SCALPING_60SEC_RESULTS.json\n")
    
    return results

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    
    print("\n")
    
    # For testing: run 10 cycles (10 minutes) instead of full 4 hours
    results = run_scalping_system(duration_seconds=600)  # 10 minutes for testing
    
    print("=" * 70)
