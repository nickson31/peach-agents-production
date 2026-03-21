#!/usr/bin/env python3
"""
BATCH 2 RETRY - Rate Limited Orders
Reintenta las 14 órdenes que fueron rechazadas por rate limit
"""

import requests
import json
import base64
import time
from pathlib import Path
from datetime import datetime

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

# ============================================================================
# RETRY LOGIC
# ============================================================================

def retry_rate_limited_orders():
    """Retry the 14 rate-limited orders"""
    
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║        BATCH 2 - RETRY RATE LIMITED ORDERS                    ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")
    
    # These are the symbols/qtys that were rate limited
    retry_orders = [
        {'symbol': 'FXB', 'qty': 14, 'limit_price': 1.25, 'youtuber': 'ForexMentor'},
        {'symbol': 'FXA', 'qty': 10, 'limit_price': 0.65, 'youtuber': 'Traders Reality'},
        {'symbol': 'EUO', 'qty': 10, 'limit_price': 1.07, 'youtuber': 'Pips Hunter'},
        {'symbol': 'GBTC', 'qty': 10, 'limit_price': 45.23, 'youtuber': 'Candlestick King'},
        {'symbol': 'FXB', 'qty': 10, 'limit_price': 1.23, 'youtuber': 'Option Alpha'},
        {'symbol': 'ETHE', 'qty': 10, 'limit_price': 3449.98, 'youtuber': 'Option Alpha'},
        {'symbol': 'GBTC', 'qty': 10, 'limit_price': 45.23, 'youtuber': 'Option Alpha'},
        {'symbol': 'FXA', 'qty': 10, 'limit_price': 0.65, 'youtuber': 'Option Alpha'},
        {'symbol': 'EUO', 'qty': 10, 'limit_price': 1.07, 'youtuber': 'Option Alpha'},
        {'symbol': 'ETHE', 'qty': 10, 'limit_price': 3449.98, 'youtuber': 'The Trading Channel'},
        {'symbol': 'FXB', 'qty': 10, 'limit_price': 1.23, 'youtuber': 'Price Action Mastery'},
        {'symbol': 'ETHE', 'qty': 10, 'limit_price': 3449.98, 'youtuber': 'Smart Money Concepts'},
        {'symbol': 'GBTC', 'qty': 10, 'limit_price': 45.23, 'youtuber': 'Elite NZD Traders'},
        {'symbol': 'FXA', 'qty': 10, 'limit_price': 0.65, 'youtuber': 'Elite NZD Traders'},
    ]
    
    print(f"📋 Retrying {len(retry_orders)} rate-limited orders\n")
    
    deployed = []
    failed = []
    
    for idx, order in enumerate(retry_orders, 1):
        
        # Longer wait before retry
        if idx > 1:
            wait_time = 2
            print(f"   ⏳ Waiting {wait_time}s... ({idx-1}/{len(retry_orders)} completed)")
            time.sleep(wait_time)
        
        try:
            alpaca_order = {
                'symbol': order['symbol'],
                'qty': order['qty'],
                'side': 'buy',
                'type': 'limit',
                'limit_price': order['limit_price'],
                'time_in_force': 'day',
            }
            
            resp = requests.post(
                f"{ALPACA_API}/orders",
                json=alpaca_order,
                headers=get_alpaca_headers(),
                timeout=10
            )
            
            if resp.status_code == 200:
                alpaca_response = resp.json()
                order_id = alpaca_response.get('id')
                
                deployed.append({
                    **order,
                    'order_id': order_id,
                    'status': 'submitted',
                    'timestamp': datetime.now().isoformat()
                })
                
                print(f"✅ {idx:2d}. {order['symbol']} @ {order['limit_price']} | {order['qty']} qty | {order['youtuber']}")
            
            elif resp.status_code == 429:
                print(f"⏳ {idx:2d}. Rate limit again ({order['symbol']}) - skipping")
                failed.append(order)
            
            else:
                print(f"❌ {idx:2d}. Error {resp.status_code}: {order['symbol']}")
                failed.append(order)
        
        except Exception as e:
            print(f"❌ {idx:2d}. Exception: {str(e)[:60]}")
            failed.append(order)
    
    print("\n" + "=" * 70 + "\n")
    
    print(f"✅ Successfully deployed: {len(deployed)}/14")
    print(f"⏳ Still rate-limited: {len(failed)}")
    
    if failed:
        print(f"\n⚠️  Retry in 5 minutes for these orders:")
        for order in failed:
            print(f"   - {order['symbol']} @ {order['limit_price']} ({order['youtuber']})")
    
    # Save retry results
    retry_results = {
        'timestamp': datetime.now().isoformat(),
        'batch': 2,
        'retry_attempt': 1,
        'total_retried': len(retry_orders),
        'successfully_deployed': len(deployed),
        'still_rate_limited': len(failed),
        'deployed_orders': deployed,
        'failed_orders': failed
    }
    
    results_file = Path("/home/ubuntu/.openclaw/workspace/BATCH_2_RETRY_RESULTS.json")
    with open(results_file, "w") as f:
        json.dump(retry_results, f, indent=2)
    
    print(f"\n✅ Results saved: {results_file}\n")
    
    return retry_results

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    results = retry_rate_limited_orders()
    
    print("=" * 70)
    print("✅ BATCH 2 RETRY COMPLETE")
    print("=" * 70)
