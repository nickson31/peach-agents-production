#!/usr/bin/env python3
"""
BATCH 5: WAVE-BASED DEPLOYMENT - OPTIMIZED FROM BATCH 1-4 LEARNINGS
Deploy 100 orders in 10 waves (2-3 min intervals)
ETHE 50%, GBTC 40%, FXA 10% (if improved entry)
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

def place_batch5_order(symbol, qty=12, wave_num=1, stagger=-0.02):
    """Place optimized Batch 5 order"""
    
    current_price = get_current_price(symbol)
    if not current_price:
        return {'status': 'error', 'symbol': symbol, 'issue': 'price_fetch_failed', 'wave': wave_num}
    
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
                'current_price': current_price,
                'qty': qty,
                'wave': wave_num,
                'timestamp': datetime.now().isoformat()
            }
        else:
            return {
                'status': 'error',
                'symbol': symbol,
                'issue': f"HTTP {resp.status_code}",
                'wave': wave_num
            }
    except Exception as e:
        return {
            'status': 'error',
            'symbol': symbol,
            'issue': str(e),
            'wave': wave_num
        }

def get_wave_performance(wave_num, all_orders):
    """Analyze performance of previous wave"""
    
    wave_orders = [o for o in all_orders if o.get('wave') == wave_num]
    
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

def get_next_wave_allocation(current_wave, wave_performance):
    """Decide allocation for next wave based on performance"""
    
    if not wave_performance:
        # First wave - start with planned allocation
        return {'ETHE': 5, 'GBTC': 4}
    
    allocation = {}
    
    for symbol, data in wave_performance.items():
        fill_rate = (data['filled'] / data['total'] * 100) if data['total'] > 0 else 0
        
        if fill_rate > 85:
            # High performers - increase
            allocation[symbol] = max(data['total'] + 2, 8)
        elif fill_rate > 60:
            # Medium - maintain
            allocation[symbol] = data['total']
        else:
            # Low - reduce
            allocation[symbol] = max(data['total'] - 2, 2)
    
    # If not enough symbols, use defaults
    if 'ETHE' not in allocation:
        allocation['ETHE'] = 5
    if 'GBTC' not in allocation:
        allocation['GBTC'] = 4
    
    return allocation

def deploy_wave(wave_num, allocation):
    """Deploy one wave"""
    
    wave_orders = []
    
    print(f"\n🌊 WAVE {wave_num} DEPLOYMENT ({datetime.now().strftime('%H:%M:%S')})")
    print(f"   Allocation: {allocation}")
    
    for symbol, qty in allocation.items():
        for i in range(qty):
            order = place_batch5_order(symbol, qty=12, wave_num=wave_num, stagger=-0.02)
            wave_orders.append(order)
            
            status_icon = "✅" if order['status'] == 'placed' else "❌"
            print(f"   {status_icon} {symbol}")
    
    placed = sum(1 for o in wave_orders if o['status'] == 'placed')
    print(f"   → {placed}/{len(wave_orders)} placed")
    
    return wave_orders

def run_batch5_waves():
    """Run Batch 5 with adaptive waves"""
    
    print("\n╔════════════════════════════════════════════════════════════════╗")
    print("║      BATCH 5: OPTIMIZED WAVE DEPLOYMENT                      ║")
    print("║      Based on Batch 1-4 Learnings (ETHE 50%, GBTC 40%)      ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")
    
    all_orders = []
    current_allocation = {'ETHE': 5, 'GBTC': 4}  # Start: ETHE 50%, GBTC 40%
    
    for wave in range(1, 11):  # 10 waves
        
        # Deploy wave
        wave_orders = deploy_wave(wave, current_allocation)
        all_orders.extend(wave_orders)
        
        print(f"   ⏳ Waiting 90 seconds for fills...")
        time.sleep(90)  # 90 seconds between waves (1.5 min)
        
        # Analyze if not last wave
        if wave < 10:
            print(f"\n   🔍 Analyzing Wave {wave}...")
            wave_perf = get_wave_performance(wave, all_orders)
            
            for symbol, data in wave_perf.items():
                fill_rate = (data['filled'] / data['total'] * 100) if data['total'] > 0 else 0
                print(f"      {symbol}: {data['filled']}/{data['total']} ({fill_rate:.0f}%)")
            
            # Get next allocation
            current_allocation = get_next_wave_allocation(wave, wave_perf)
            print(f"   📊 Next wave allocation: {current_allocation}")
    
    print(f"\n{'='*70}\n")
    print("✅ BATCH 5 WAVE DEPLOYMENT COMPLETE\n")
    
    # Summary
    total_placed = sum(1 for o in all_orders if o['status'] == 'placed')
    total_failed = sum(1 for o in all_orders if o['status'] == 'error')
    
    print(f"📊 FINAL SUMMARY:")
    print(f"   Total waves: 10")
    print(f"   Total orders: {total_placed + total_failed}")
    print(f"   Placed: {total_placed}")
    print(f"   Failed: {total_failed}")
    print(f"   Success rate: {total_placed / (total_placed + total_failed) * 100:.1f}%\n")
    
    # By symbol
    by_symbol = defaultdict(lambda: {'total': 0, 'placed': 0})
    for order in all_orders:
        symbol = order.get('symbol')
        by_symbol[symbol]['total'] += 1
        if order['status'] == 'placed':
            by_symbol[symbol]['placed'] += 1
    
    print(f"   By Symbol:")
    for symbol in sorted(by_symbol.keys()):
        data = by_symbol[symbol]
        fill_rate = data['placed'] / data['total'] * 100 if data['total'] > 0 else 0
        print(f"   {symbol}: {data['placed']}/{data['total']} ({fill_rate:.0f}%)")
    
    print()
    
    # Save results
    results = {
        'system': 'batch_5_waves',
        'timestamp': datetime.now().isoformat(),
        'waves': 10,
        'total_orders': total_placed + total_failed,
        'placed': total_placed,
        'failed': total_failed,
        'success_rate': total_placed / (total_placed + total_failed) * 100,
        'orders': all_orders,
        'learnings_applied': {
            'replicate': ['ETHE 93%', 'GBTC improved'],
            'eliminated': ['FXB 0%', 'EUO errors', 'GLD 0%'],
            'strategy': 'ETHE 50%, GBTC 40%, adaptive waves'
        }
    }
    
    results_file = Path("/home/ubuntu/.openclaw/workspace/BATCH_5_OPTIMIZED_RESULTS.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"✅ Results saved to BATCH_5_OPTIMIZED_RESULTS.json\n")
    
    return results

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("\n")
    results = run_batch5_waves()
    print("=" * 70)
