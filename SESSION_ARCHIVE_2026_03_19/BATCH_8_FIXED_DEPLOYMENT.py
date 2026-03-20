#!/usr/bin/env python3
"""
BATCH 8 - FIXED VERSION
Aprendizajes de Batch 7 failures:

Problems identified:
1. ETHE entry $3,381 = TOO LOW (rejected/no fill)
2. GBTC entry $71.25 = OK but slow fill
3. Wave intervals 90s = OK
4. 403 errors = API rate limiting or auth

Solutions:
1. Increase ETHE entry to $3,450+ (more realistic)
2. Increase GBTC entry to $75+ (better fills)
3. Reduce wave size slightly (avoid rate limits)
4. Add delay between symbols (sequential, not parallel)
5. Verify fresh prices before each order
6. Add retry logic for failures
"""

import requests
import time
from datetime import datetime

ALPACA_API = "https://paper-api.alpaca.markets/v2"
ALPACA_KEY = "PKW445AWAOSGU2WJYCCFUZ47PR"
ALPACA_SECRET = "7tmQ6gY5c4hdmqwEN3UAgv4to78WsGkWPmxUox4G7x4X"

HEADERS = {
    "APCA-API-KEY-ID": ALPACA_KEY,
    "APCA-API-SECRET-KEY": ALPACA_SECRET,
}

# BATCH 8 CONFIGURATION - FIXED
BATCH_8_CONFIG = {
    "batch_id": "BATCH_8",
    "total_orders": 105,  # +5% from Batch 7's 100
    "wave_size": 12,  # Reduced from 15 (avoid rate limits)
    "wave_interval": 100,  # Increased from 90s (safer)
    "symbols": {
        "ETHE": {
            "allocation": 0.60,
            "entry_stagger": 0.01,  # 1% from current price (MORE AGGRESSIVE)
            "reference_price": 3480.00,  # INCREASED from 3,381
            "qty_per_wave": 6,
            "retry_count": 3,
        },
        "GBTC": {
            "allocation": 0.40,
            "entry_stagger": 0.03,  # 3% from current (more realistic)
            "reference_price": 75.50,  # INCREASED from 71.25
            "qty_per_wave": 6,
            "retry_count": 3,
        },
    },
    "take_profit": 0.03,
    "stop_loss": -0.01,
}


def log_batch(message):
    """Log batch events"""
    timestamp = datetime.now().isoformat()
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)


def get_fresh_price(symbol):
    """Get fresh price from Alpaca API"""
    try:
        resp = requests.get(
            f"{ALPACA_API}/v1/last/quote",
            params={"symbols": symbol},
            headers=HEADERS,
            timeout=5,
        )
        if resp.status_code == 200:
            data = resp.json()
            if symbol in data and "ap" in data[symbol]:
                return float(data[symbol]["ap"])
    except Exception as e:
        log_batch(f"  ⚠️ Price fetch error {symbol}: {e}")
    
    return None


def place_order_with_retry(symbol, qty, limit_price, retry=0):
    """Place order with retry logic"""
    max_retries = BATCH_8_CONFIG["symbols"][symbol]["retry_count"]
    
    order_data = {
        "symbol": symbol,
        "qty": qty,
        "side": "buy",
        "type": "limit",
        "limit_price": round(limit_price, 2),
        "time_in_force": "day",
        "client_order_id": f"BATCH_8_{symbol}_T{retry}_{int(time.time())}",
    }
    
    try:
        resp = requests.post(
            f"{ALPACA_API}/orders",
            json=order_data,
            headers=HEADERS,
            timeout=5,
        )
        
        if resp.status_code in [200, 201]:
            order = resp.json()
            log_batch(f"  ✓ {symbol}: {qty} @ ${limit_price:.2f} (status: {order.get('status', '?')})")
            return order
        elif resp.status_code == 429:  # Rate limited
            if retry < max_retries:
                log_batch(f"  ⚠️ {symbol} rate limited - retry {retry+1}/{max_retries}")
                time.sleep(2)
                return place_order_with_retry(symbol, qty, limit_price, retry + 1)
            else:
                log_batch(f"  ❌ {symbol} rate limit - max retries reached")
                return None
        elif resp.status_code == 403:  # Forbidden/Auth
            log_batch(f"  ❌ {symbol} 403 error (auth/permission)")
            return None
        else:
            error = resp.json().get("message", f"HTTP {resp.status_code}")
            log_batch(f"  ❌ {symbol} error: {error}")
            return None
    
    except Exception as e:
        log_batch(f"  ❌ {symbol} exception: {e}")
        return None


def deploy_batch_8():
    """Deploy Batch 8 with fixes"""
    log_batch("=" * 70)
    log_batch("🚀 BATCH 8 DEPLOYMENT - FIXED VERSION")
    log_batch(f"   Total orders: {BATCH_8_CONFIG['total_orders']}")
    log_batch(f"   Wave size: {BATCH_8_CONFIG['wave_size']}")
    log_batch(f"   Wave interval: {BATCH_8_CONFIG['wave_interval']}s")
    log_batch("=" * 70)
    
    # Verify account
    try:
        resp = requests.get(f"{ALPACA_API}/account", headers=HEADERS)
        account = resp.json()
        log_batch(f"✓ Account: ${account['equity']:.2f} equity, ${account['buying_power']:.2f} buying power")
    except Exception as e:
        log_batch(f"❌ Account error: {e}")
        return False
    
    orders_deployed = 0
    orders_failed = 0
    
    # Calculate number of waves
    num_waves = (BATCH_8_CONFIG["total_orders"] + BATCH_8_CONFIG["wave_size"] - 1) // BATCH_8_CONFIG["wave_size"]
    
    for wave_num in range(1, num_waves + 1):
        log_batch(f"\n📤 Wave {wave_num}/{num_waves}")
        
        # Deploy ETHE first, then GBTC (sequential to avoid rate limits)
        for symbol in ["ETHE", "GBTC"]:
            config = BATCH_8_CONFIG["symbols"][symbol]
            qty = config["qty_per_wave"]
            
            # Get fresh price
            fresh_price = get_fresh_price(symbol)
            if fresh_price:
                log_batch(f"  🔍 {symbol} live price: ${fresh_price:.2f}")
                # Use fresh price with stagger
                entry_price = fresh_price * (1 - config["entry_stagger"])
            else:
                # Fallback to reference
                entry_price = config["reference_price"] * (1 - config["entry_stagger"])
                log_batch(f"  📌 {symbol} fallback price: ${entry_price:.2f}")
            
            # Place order
            order = place_order_with_retry(symbol, qty, entry_price)
            
            if order:
                orders_deployed += qty
            else:
                orders_failed += qty
            
            # Small delay between symbols (sequential)
            time.sleep(0.5)
        
        # Wait before next wave
        if wave_num < num_waves:
            log_batch(f"  ⏳ Waiting {BATCH_8_CONFIG['wave_interval']}s...")
            time.sleep(BATCH_8_CONFIG["wave_interval"])
    
    # Summary
    log_batch(f"\n" + "=" * 70)
    log_batch(f"✅ BATCH 8 COMPLETE")
    log_batch(f"   Orders deployed: {orders_deployed}")
    log_batch(f"   Orders failed: {orders_failed}")
    log_batch(f"   Success rate: {orders_deployed / (orders_deployed + orders_failed) * 100 if (orders_deployed + orders_failed) > 0 else 0:.1f}%")
    log_batch("=" * 70)
    
    return True


if __name__ == "__main__":
    deploy_batch_8()
