#!/usr/bin/env python3
"""
WAVE DEPLOYMENT SYSTEM
Deploy in adaptive waves (15 orders per wave, 2-3 min intervals)
Real-time feedback adaptation between waves
"""

import requests
import json
import base64
import time
from datetime import datetime
from pathlib import Path
from collections import defaultdict

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

def place_wave_order(symbol, qty=5, wave_num=1, stagger=-0.02):
    """Place order for this wave"""
    
    current_price = get_current_price(symbol)
    if not current_price:
        return {'status': 'error', 'symbol': symbol, 'issue': 'price_fetch_failed'}
    
    entry_price = round(current_price * (1 + stagger), 4)
    
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
                'qty': qty,
                'wave': wave_num,
                'timestamp': datetime.now().isoformat()
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

def get_wave_fills(wave_num, orders):
    """Get fill status of orders from a wave"""
    
    wave_orders = [o for o in orders if o.get('wave') == wave_num]
    
    fills = defaultdict(lambda: {'total': 0, 'filled': 0})
    
    for order in wave_orders:
        symbol = order.get('symbol', 'Unknown')
        fills[symbol]['total'] += 1
        
        # Query Alpaca for current status
        order_id = order.get('order_id')
        if order_id:
            try:
                resp = requests.get(f"{ALPACA_API}/orders/{order_id}", 
                                  headers=get_headers(), timeout=5)
                if resp.status_code == 200:
                    current_order = resp.json()
                    if current_order.get('status') == 'filled':
                        fills[symbol]['filled'] += 1
            except:
                pass
    
    return fills

def analyze_wave(wave_num, orders):
    """Analyze wave performance and recommend next wave"""
    
    print(f"\n🔍 ANALYZING WAVE {wave_num}\n")
    
    fills = get_wave_fills(wave_num, orders)
    
    analysis = {}
    
    for symbol, data in fills.items():
        total = data['total']
        filled = data['filled']
        fill_rate = (filled / total * 100) if total > 0 else 0
        
        analysis[symbol] = {
            'total': total,
            'filled': filled,
            'fill_rate': fill_rate
        }
        
        print(f"   {symbol}: {filled}/{total} ({fill_rate:.0f}%)")
    
    # Decide next wave allocation
    print(f"\n   📊 Allocation recommendation for Wave {wave_num + 1}:")
    
    next_allocation = {}
    
    # Sort by fill rate
    sorted_symbols = sorted(analysis.items(), key=lambda x: x[1]['fill_rate'], reverse=True)
    
    for idx, (symbol, data) in enumerate(sorted_symbols):
        fill_rate = data['fill_rate']
        
        if fill_rate > 85:
            qty = 10  # Increase high performers
            print(f"   ✅ {symbol} ({fill_rate:.0f}%) → INCREASE to {qty}")
        elif fill_rate > 60:
            qty = 5   # Keep middle performers
            print(f"   ⚠️  {symbol} ({fill_rate:.0f}%) → MAINTAIN at {qty}")
        else:
            qty = 2   # Reduce low performers
            print(f"   ❌ {symbol} ({fill_rate:.0f}%) → REDUCE to {qty}")
        
        next_allocation[symbol] = qty
    
    return next_allocation

def deploy_wave(wave_num, allocation):
    """Deploy one wave with given allocation"""
    
    print(f"\n{'='*70}")
    print(f"🌊 WAVE {wave_num} DEPLOYMENT")
    print(f"{'='*70}\n")
    
    print(f"Allocation:")
    for symbol, qty in allocation.items():
        print(f"  {symbol}: {qty} orders")
    
    print(f"\nDeploying...\n")
    
    wave_orders = []
    total_qty = 0
    
    for symbol, qty in allocation.items():
        for i in range(qty):
            order = place_wave_order(symbol, qty=1, wave_num=wave_num, stagger=-0.02)
            wave_orders.append(order)
            
            if order['status'] == 'placed':
                total_qty += 1
                print(f"  ✅ {symbol} ({i+1}/{qty})")
            else:
                print(f"  ❌ {symbol}: {order.get('issue')}")
    
    print(f"\nWave {wave_num} deployed: {total_qty} orders\n")
    
    return wave_orders

def run_wave_batch(num_waves=5, wave_interval_seconds=120):
    """Run batch with adaptive waves"""
    
    print("\n╔════════════════════════════════════════════════════════════════╗")
    print("║      INTELLIGENT WAVE DEPLOYMENT SYSTEM                      ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")
    
    all_orders = []
    
    # Initial allocation
    current_allocation = {
        'ETHE': 5,
        'GBTC': 5,
        'FXA': 5
    }
    
    for wave in range(1, num_waves + 1):
        
        # Deploy wave
        wave_orders = deploy_wave(wave, current_allocation)
        all_orders.extend(wave_orders)
        
        # Wait for orders to fill
        print(f"⏳ Waiting {wave_interval_seconds} seconds for fills...\n")
        time.sleep(wave_interval_seconds)
        
        # Analyze if not last wave
        if wave < num_waves:
            next_allocation = analyze_wave(wave, all_orders)
            current_allocation = next_allocation
    
    print(f"\n{'='*70}")
    print("✅ WAVE BATCH COMPLETE")
    print(f"{'='*70}\n")
    
    # Summary
    total_placed = sum(1 for o in all_orders if o['status'] == 'placed')
    total_failed = sum(1 for o in all_orders if o['status'] == 'error')
    
    print(f"Total waves: {num_waves}")
    print(f"Total orders: {total_placed + total_failed}")
    print(f"Successful: {total_placed}")
    print(f"Failed: {total_failed}")
    print(f"Success rate: {total_placed / (total_placed + total_failed) * 100:.1f}%\n")
    
    # Save results
    results = {
        'system': 'wave_deployment',
        'timestamp': datetime.now().isoformat(),
        'waves': num_waves,
        'wave_interval': wave_interval_seconds,
        'total_orders': total_placed + total_failed,
        'successful': total_placed,
        'failed': total_failed,
        'orders': all_orders
    }
    
    results_file = Path("/home/ubuntu/.openclaw/workspace/WAVE_DEPLOYMENT_RESULTS.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"✅ Results saved to WAVE_DEPLOYMENT_RESULTS.json\n")
    
    return results

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    
    print("\n")
    
    # Run wave batch (5 waves, 120 seconds each for testing)
    # In production: run_wave_batch(num_waves=10, wave_interval_seconds=120)
    results = run_wave_batch(num_waves=3, wave_interval_seconds=30)  # Testing: 3 waves, 30 sec
    
    print("=" * 70)
