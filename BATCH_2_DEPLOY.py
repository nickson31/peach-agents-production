#!/usr/bin/env python3
"""
BATCH 2 DEPLOYMENT
100 operaciones optimizadas con +20% presupuesto
Aplicando lecciones de Batch 1
"""

import requests
import json
import base64
import time
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import random

# ============================================================================
# CONFIG
# ============================================================================

ALPACA_KEY = "PKW445AWAOSGU2WJYCCFUZ47PR"
ALPACA_SECRET = "7tmQ6gY5c4hdmqwEN3UAgv4to78WsGkWPmxUox4G7x4X"
ALPACA_API = "https://paper-api.alpaca.markets/v2"

# ============================================================================
# UTILITIES
# ============================================================================

def get_alpaca_headers():
    auth = base64.b64encode(f"{ALPACA_KEY}:{ALPACA_SECRET}".encode()).decode()
    return {"Authorization": f"Basic {auth}"}

def load_batch_1_strategies():
    """Load Batch 1 strategies with YouTuber info"""
    tracking_file = Path("/home/ubuntu/.openclaw/workspace/COMPLETE_ORDERS_TRACKING.json")
    if tracking_file.exists():
        try:
            with open(tracking_file) as f:
                data = json.load(f)
                return data.get('orders_detail', [])
        except:
            pass
    return []

def get_youtuber_score(youtuber):
    """Get YouTuber score from analysis"""
    scores = {
        'ForexMentor': 97.6,
        'CryptoBob': 94.6,
        'FullTimeForex': 91.6,
        'DayTradingReview': 62.3,
        'Traders Reality': 88.5,
        'Glacier Trading': 85.2,
        'Pips Hunter': 82.1,
        'Candlestick King': 80.5,
    }
    return scores.get(youtuber, 75.0)

def calculate_qty_for_youtuber(youtuber):
    """Calculate optimized qty based on YouTuber score"""
    score = get_youtuber_score(youtuber)
    
    if score > 95:  # TIER 1
        return 14
    elif score >= 90:  # TIER 2
        return 12
    else:  # TIER 3
        return 10

def calculate_entry_price_with_stagger(symbol, tier):
    """Calculate entry price with staggering based on tier"""
    
    # Base prices (from market) - Alpaca compatible format
    base_prices = {
        'EUO': 1.09,
        'FXB': 1.25,
        'ETHE': 3450.00,
        'GBTC': 45.25,
        'FXA': 0.67,
        'GLD': 191.10,
        'BTC': 43200.00,
        'ETH': 2280.00,
        'EUR': 1.09,
        'GBP': 1.25,
    }
    
    base = base_prices.get(symbol, 100.0)
    
    # Staggering: adjust by tier (whole cents/dollars only)
    if tier == 1:  # Exact (best quality)
        return round(base, 2)
    elif tier == 2:  # -$0.01 band (better fill)
        return round(base - 0.01, 2)
    else:  # -$0.02 band (more aggressive)
        return round(base - 0.02, 2)

def create_batch_2_orders():
    """Create 100 optimized orders for Batch 2"""
    
    # Load Batch 1 strategies
    batch_1_strategies = load_batch_1_strategies()
    
    orders_to_deploy = []
    
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║           BATCH 2: GENERATING 100 OPTIMIZED ORDERS            ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")
    
    # ========================================================================
    # PART 1: REPEAT BATCH 1 STRATEGIES WITH OPTIMIZED QTY
    # ========================================================================
    
    print("PARTE 1: Estrategias repetidas de Batch 1 (optimizadas)\n")
    
    youtuber_order_count = defaultdict(int)
    
    for idx, strategy in enumerate(batch_1_strategies[:74], 1):  # Use first 74
        youtuber = strategy.get('traceability', {}).get('youtuber', 'Unknown')
        symbol = strategy.get('symbol', 'EUO')
        
        # Calculate optimized qty
        qty = calculate_qty_for_youtuber(youtuber)
        youtuber_order_count[youtuber] += 1
        
        # Determine tier (based on score)
        score = get_youtuber_score(youtuber)
        tier = 1 if score > 95 else (2 if score >= 90 else 3)
        
        # Calculate entry price with stagger
        entry_price = calculate_entry_price_with_stagger(symbol, tier)
        
        # Create order (same as Batch 1 but with optimized qty and entry)
        order = {
            'symbol': symbol,
            'qty': qty,
            'side': 'buy',
            'type': 'limit',
            'limit_price': entry_price,
            'time_in_force': 'day',
            'traceability': {
                'youtuber': youtuber,
                'batch': 2,
                'from_batch_1': True,
                'strategy_index': idx,
                'qty_increase_percent': 20 if tier >= 2 else 40 if tier == 1 else 0,
            }
        }
        
        orders_to_deploy.append(order)
        
        if idx % 10 == 0:
            print(f"  ✓ {idx}/74 estrategias de Batch 1 preparadas")
    
    print(f"\n✅ 74 órdenes de Batch 1 listas (optimizadas)\n")
    
    # ========================================================================
    # PART 2: NEW YOUTUBERS (20) - 26+ NEW ORDERS
    # ========================================================================
    
    print("PARTE 2: Nuevas estrategias (+20 YouTubers)\n")
    
    new_youtubers = [
        'Urban Forex', 'Crypto Saru', 'BitMex Academy', 'Option Alpha',
        'Warrior Trading', 'Stock Maniacs', 'The Trading Channel',
        'Price Action Mastery', 'Tech Trading Mastery', 'Smart Money Concepts',
        'Elite NZD Traders', 'Scalpers Connect', 'ChartGuys', 'FXStreet',
        'Babypips', 'Forex Factory', 'Trading with Nial Fuller',
        'The Forex Guys', '1Broker Academy', 'TradingView Academy'
    ]
    
    symbols_rotation = ['EUO', 'FXB', 'ETHE', 'GBTC', 'FXA']
    
    new_order_count = 0
    
    for yt_idx, youtuber in enumerate(new_youtubers):
        # Assign 1-2 strategies per new YouTuber
        strategies_per_yt = 2 if yt_idx < 10 else 1
        
        for strat_idx in range(strategies_per_yt):
            if new_order_count >= 26:
                break
            
            # Rotate symbols
            symbol = symbols_rotation[new_order_count % len(symbols_rotation)]
            
            # Assign tier (new YouTubers start at tier 3, can improve)
            tier = 3
            qty = calculate_qty_for_youtuber(youtuber)
            
            # Calculate entry price
            entry_price = calculate_entry_price_with_stagger(symbol, tier)
            
            order = {
                'symbol': symbol,
                'qty': qty,
                'side': 'buy',
                'type': 'limit',
                'limit_price': entry_price,
                'time_in_force': 'day',
                'traceability': {
                    'youtuber': youtuber,
                    'batch': 2,
                    'from_batch_1': False,
                    'new_youtuber': True,
                    'strategy_index': strat_idx + 1,
                }
            }
            
            orders_to_deploy.append(order)
            new_order_count += 1
            
            if new_order_count % 5 == 0:
                print(f"  ✓ {new_order_count}/26 nuevas órdenes preparadas")
    
    print(f"\n✅ {new_order_count} nuevas órdenes listas\n")
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    
    print("=" * 70 + "\n")
    print("📊 BATCH 2 SUMMARY\n")
    
    total_capital = 0
    for order in orders_to_deploy:
        total_capital += order['qty'] * order['limit_price']
    
    print(f"Total órdenes: {len(orders_to_deploy)}")
    print(f"Capital estimado: ${total_capital:,.2f}\n")
    
    print("Por YouTuber (Top 5):")
    yt_totals = defaultdict(lambda: {'count': 0, 'capital': 0, 'qty': 0})
    
    for order in orders_to_deploy:
        yt = order['traceability']['youtuber']
        yt_totals[yt]['count'] += 1
        yt_totals[yt]['capital'] += order['qty'] * order['limit_price']
        yt_totals[yt]['qty'] += order['qty']
    
    sorted_yts = sorted(yt_totals.items(), key=lambda x: x[1]['count'], reverse=True)
    for yt, data in sorted_yts[:5]:
        print(f"  {yt}: {data['count']} órdenes | {data['qty']} qty | ${data['capital']:,.0f}")
    
    print("\n" + "=" * 70 + "\n")
    
    return orders_to_deploy

def deploy_orders_to_alpaca(orders_to_deploy):
    """Deploy orders to Alpaca with staggering"""
    
    print("🚀 DEPLOYING TO ALPACA (Staggered)\n")
    
    deployed_orders = []
    batch_size = 10
    stagger_interval = 5  # seconds
    
    total_batches = (len(orders_to_deploy) + batch_size - 1) // batch_size
    
    for batch_num in range(total_batches):
        batch_start = batch_num * batch_size
        batch_end = min(batch_start + batch_size, len(orders_to_deploy))
        batch = orders_to_deploy[batch_start:batch_end]
        
        print(f"📤 Batch {batch_num + 1}/{total_batches}: Deploying {len(batch)} orders...")
        print(f"   Time: {datetime.now().strftime('%H:%M:%S UTC')}\n")
        
        for order_num, order in enumerate(batch, 1):
            try:
                # Prepare order for Alpaca API
                alpaca_order = {
                    'symbol': order['symbol'],
                    'qty': order['qty'],
                    'side': order['side'],
                    'type': order['type'],
                    'limit_price': order['limit_price'],
                    'time_in_force': order['time_in_force'],
                }
                
                # Submit to Alpaca
                resp = requests.post(
                    f"{ALPACA_API}/orders",
                    json=alpaca_order,
                    headers=get_alpaca_headers(),
                    timeout=10
                )
                
                if resp.status_code == 200:
                    alpaca_response = resp.json()
                    order_id = alpaca_response.get('id')
                    
                    # Create deployment record
                    deployed = {
                        **order,
                        'order_id': order_id,
                        'status': 'submitted',
                        'timestamp': datetime.now().isoformat(),
                        'alpaca_response': alpaca_response
                    }
                    deployed_orders.append(deployed)
                    
                    emoji = "✅"
                    print(f"   {emoji} {order['symbol']} @ {order['limit_price']} | {order['qty']} qty | YouTuber: {order['traceability']['youtuber']}")
                
                else:
                    print(f"   ❌ Error: {resp.status_code} - {order['symbol']}")
                    print(f"      Response: {resp.text[:100]}")
            
            except Exception as e:
                print(f"   ❌ Exception: {str(e)[:80]}")
        
        # Wait between batches (except last one)
        if batch_num < total_batches - 1:
            print(f"\n   ⏱️  Waiting {stagger_interval}s before next batch...")
            time.sleep(stagger_interval)
        
        print()
    
    print("=" * 70 + "\n")
    print(f"✅ DEPLOYMENT COMPLETE: {len(deployed_orders)}/{len(orders_to_deploy)} órdenes enviadas\n")
    
    return deployed_orders

def save_batch_2_results(deployed_orders):
    """Save Batch 2 results to file"""
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'batch': 2,
        'total_orders': len(deployed_orders),
        'total_capital': sum(o['qty'] * o['limit_price'] for o in deployed_orders),
        'orders_detail': deployed_orders
    }
    
    results_file = Path("/home/ubuntu/.openclaw/workspace/BATCH_2_DEPLOYMENT_RESULTS.json")
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"✅ Results saved: {results_file}\n")
    
    return results

def generate_telegram_message(results):
    """Generate Telegram notification"""
    
    msg = "🚀 *BATCH 2 - DEPLOYMENT COMPLETE*\n\n"
    msg += f"*Total Órdenes:* {results['total_orders']}\n"
    msg += f"*Capital Total:* ${results['total_capital']:,.0f}\n"
    msg += f"*Timestamp:* {datetime.now().strftime('%H:%M:%S UTC')}\n\n"
    
    msg += "═══════════════════════════════════\n\n"
    
    # Top YouTubers
    yt_totals = defaultdict(lambda: {'count': 0})
    for order in results['orders_detail']:
        yt = order['traceability']['youtuber']
        yt_totals[yt]['count'] += 1
    
    msg += "*Top YouTubers:\n*"
    sorted_yts = sorted(yt_totals.items(), key=lambda x: x[1]['count'], reverse=True)
    for yt, data in sorted_yts[:5]:
        msg += f"├─ {yt}: {data['count']} órdenes\n"
    
    msg += f"... +{len(yt_totals) - 5} more\n\n"
    
    msg += "═══════════════════════════════════\n\n"
    msg += "✅ Monitoring: 24/7 via Telegram\n"
    msg += "📊 Alerts: Real-time updates\n"
    msg += "🎯 Next: Watch for fills over next hours\n"
    
    return msg

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    
    print("\n")
    
    # Generate orders
    orders_to_deploy = create_batch_2_orders()
    
    print("\n✅ Ready to deploy to Alpaca")
    time.sleep(1)
    
    # Deploy to Alpaca
    deployed_orders = deploy_orders_to_alpaca(orders_to_deploy)
    
    # Save results
    results = save_batch_2_results(deployed_orders)
    
    # Generate message
    msg = generate_telegram_message(results)
    print("📱 TELEGRAM MESSAGE:\n")
    print(msg)
    
    print("\n" + "=" * 70)
    print("✅ BATCH 2 DEPLOYMENT COMPLETE")
    print("=" * 70)
