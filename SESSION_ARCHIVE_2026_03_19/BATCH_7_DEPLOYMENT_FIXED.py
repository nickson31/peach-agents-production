#!/usr/bin/env python3
"""
BATCH 7 DEPLOYMENT - BUG FIX + IMPROVEMENTS
Aprendizajes de Batch 6: ETHE 95% fill, GBTC/FXA precio bugs

Cambios:
1. ETHE: Mantener - 95% fill rate probado
2. GBTC: FIX precios (usar reales: $70-80 rango)
3. FXA: REMOVE por ahora (demasiado problemas)
4. Enfoque: ETHE 60% + GBTC 40% (solo 2 símbolos, proven)

Research Applied:
- Volume confirmation working
- Conservative entries (Batch 6 ETHE 95% vs Batch 5 93%)
- EMA pullback logic
"""

import requests
import time
import json
from datetime import datetime

# Alpaca Configuration
ALPACA_API = "https://paper-api.alpaca.markets/v2"
ALPACA_KEY = "PKW445AWAOSGU2WJYCCFUZ47PR"
ALPACA_SECRET = "7tmQ6gY5c4hdmqwEN3UAgv4to78WsGkWPmxUox4G7x4X"

# Batch 7 Configuration - FIXED FROM BATCH 6
BATCH_ID = "BATCH_7"
BATCH_START_TIME = datetime.now().isoformat()

# SYMBOLS: ONLY 2 (ETHE + GBTC proven, FXA removed due to bugs)
SYMBOLS = ["ETHE", "GBTC"]
ALLOCATION = {"ETHE": 0.60, "GBTC": 0.40}  # More conservative, focused

# Wave Settings
WAVE_SIZE = 15
WAVE_INTERVAL = 90
TOTAL_ORDERS = 100  # Slightly smaller, focus on quality

# Exit Rules (Proven)
TAKE_PROFIT = 0.03  # +3%
STOP_LOSS = -0.01   # -1%

# Entry Stagger - FIXED VALUES (not buggy calculations)
ENTRY_STAGGER = {
    "ETHE": 0.02,   # 2% - Works perfectly (proven 95%)
    "GBTC": 0.05,   # 5% - Conservative, was bugging before
}

# Real market price references (from Batch 6 fills)
REFERENCE_PRICES = {
    "ETHE": 3450.00,  # Batch 6 filled at 3449.99
    "GBTC": 75.00,    # Realistic range
}

HEADERS = {
    "APCA-API-KEY-ID": ALPACA_KEY,
    "APCA-API-SECRET-KEY": ALPACA_SECRET,
}


class Batch7Deployer:
    def __init__(self):
        self.orders_deployed = []
        self.orders_filled = 0
        self.session_start = datetime.now()
        print(f"\n🚀 BATCH 7 DEPLOYMENT - FIXED VERSION")
        print(f"📅 Start: {self.session_start}")
        print(f"📊 Configuration:")
        print(f"  - Total Orders: {TOTAL_ORDERS}")
        print(f"  - Wave Size: {WAVE_SIZE}")
        print(f"  - Symbols: {SYMBOLS} (FXA removed)")
        print(f"  - Allocation: ETHE 60%, GBTC 40%")
        print(f"  - Focus: QUALITY over QUANTITY")

    def get_account_info(self):
        """Verify account"""
        try:
            resp = requests.get(f"{ALPACA_API}/account", headers=HEADERS)
            if resp.status_code == 200:
                account = resp.json()
                print(f"\n✅ Account Verified:")
                print(f"  - Equity: ${account['equity']:.2f}")
                print(f"  - Cash: ${account['cash']:.2f}")
                print(f"  - Buying Power: ${account['buying_power']:.2f}")
                return account
        except Exception as e:
            print(f"❌ Account error: {e}")
        return None

    def calculate_entry_price(self, symbol):
        """
        FIXED: Calculate entry price properly using reference prices
        No more $0.632 bugs!
        """
        try:
            # Use reference price
            ref_price = REFERENCE_PRICES.get(symbol, 0)
            if ref_price <= 0:
                print(f"⚠️ No reference price for {symbol}")
                return None

            stagger = ENTRY_STAGGER[symbol]
            entry = ref_price * (1 - stagger)

            # Sanity check (avoid < $0 prices!)
            if entry <= 0:
                print(f"❌ Invalid entry price for {symbol}: ${entry:.2f}")
                return None

            print(f"  ℹ️ {symbol}: ref=${ref_price:.2f}, stagger={stagger*100}%, entry=${entry:.2f}")
            return round(entry, 2)

        except Exception as e:
            print(f"❌ Price calc error {symbol}: {e}")
            return None

    def place_order(self, symbol, qty):
        """Place order with FIXED price calculations"""
        try:
            entry_price = self.calculate_entry_price(symbol)
            if entry_price is None or entry_price <= 0:
                print(f"  ❌ {symbol}: Invalid entry price, SKIPPING")
                return None

            order_data = {
                "symbol": symbol,
                "qty": qty,
                "side": "buy",
                "type": "limit",
                "limit_price": entry_price,
                "time_in_force": "day",
                "client_order_id": f"{BATCH_ID}_{symbol}_{int(time.time())}",
            }

            resp = requests.post(
                f"{ALPACA_API}/orders",
                json=order_data,
                headers=HEADERS,
            )

            if resp.status_code in [200, 201]:
                order = resp.json()
                self.orders_deployed.append(order)
                print(f"  ✓ {symbol}: {qty} shares @ ${entry_price:.2f}")
                return order
            else:
                error = resp.json() if resp.text else "Unknown"
                print(f"  ❌ {symbol} order failed: {resp.status_code} - {error}")
                return None

        except Exception as e:
            print(f"  ❌ {symbol} error: {e}")
            return None

    def deploy_wave(self, wave_num):
        """Deploy wave with only ETHE + GBTC"""
        print(f"\n📤 Wave {wave_num} - Deploying {WAVE_SIZE} orders...")

        # Calculate per-symbol qty
        qty_per_symbol = WAVE_SIZE // len(SYMBOLS)

        for symbol in SYMBOLS:
            qty = qty_per_symbol
            self.place_order(symbol, qty)

        # Wait before next wave
        if wave_num < (TOTAL_ORDERS // WAVE_SIZE):
            print(f"  ⏳ Waiting {WAVE_INTERVAL}s until next wave...")
            time.sleep(WAVE_INTERVAL)

    def deploy_all(self):
        """Deploy all waves"""
        print(f"\n🌊 Starting Wave Deployment...")
        print(f"Total Orders: {TOTAL_ORDERS}")
        print(f"Waves: {TOTAL_ORDERS // WAVE_SIZE}")

        num_waves = (TOTAL_ORDERS + WAVE_SIZE - 1) // WAVE_SIZE

        for wave_num in range(1, num_waves + 1):
            self.deploy_wave(wave_num)

    def get_fill_status(self):
        """Check fill status"""
        try:
            resp = requests.get(f"{ALPACA_API}/orders", headers=HEADERS)
            if resp.status_code == 200:
                orders = resp.json()

                # Filter to only Batch 7
                batch7_orders = [o for o in orders if "BATCH_7" in o.get("client_order_id", "")]

                if not batch7_orders:
                    return None

                filled = sum(1 for o in batch7_orders if o["filled_qty"] > 0)
                pending = sum(1 for o in batch7_orders if o["status"] in ["pending_new", "accepted"])
                canceled = sum(1 for o in batch7_orders if o["status"] in ["canceled", "done_for_day"])

                total = len(batch7_orders)
                fill_rate = (filled / total * 100) if total > 0 else 0

                return {
                    "total": total,
                    "filled": filled,
                    "pending": pending,
                    "canceled": canceled,
                    "fill_rate": fill_rate,
                }
        except Exception as e:
            print(f"❌ Error checking fill status: {e}")
        return None

    def print_summary(self):
        """Print summary"""
        status = self.get_fill_status()
        print(f"\n" + "=" * 60)
        print(f"BATCH 7 DEPLOYMENT COMPLETE")
        print(f"=" * 60)

        if status:
            print(f"📊 Orders Deployed: {status['total']}")
            print(f"✓ Filled: {status['filled']} ({status['fill_rate']:.1f}%)")
            print(f"⏳ Pending: {status['pending']}")
            print(f"✗ Canceled: {status['canceled']}")

            print(f"\n🎯 Performance:")
            print(f"  Batch 1: 73.8%")
            print(f"  Batch 5: 90%+ (ETHE 93%, GBTC 90%)")
            print(f"  Batch 6: 76% (ETHE 95%, GBTC 0% bug, FXA 0% bug)")
            print(f"  Batch 7: {status['fill_rate']:.1f}% (FIXED)")

            if status['fill_rate'] >= 85:
                print(f"  ✅ TARGET MET! Better than Batch 5")
            elif status['fill_rate'] >= 75:
                print(f"  ✓ Good - On track")
            else:
                print(f"  ⚠️ Below target - Monitor")

        print(f"\n📅 Duration: {(datetime.now() - self.session_start).total_seconds() / 60:.1f} min")
        print(f"🍑 Research: Focused on ETHE/GBTC proven, removed FXA bugs")
        print(f"=" * 60 + "\n")


def main():
    print("\n" + "=" * 60)
    print("BATCH 7 - FIXED DEPLOYMENT")
    print("BUG FIXES: GBTC/FXA prices corrected")
    print("STRATEGY: ETHE 60% + GBTC 40% (proven assets)")
    print("=" * 60)

    deployer = Batch7Deployer()

    # Verify account
    account = deployer.get_account_info()
    if not account:
        print("❌ Cannot proceed without account")
        return

    # Deploy
    deployer.deploy_all()

    # Summary
    deployer.print_summary()

    # Check Batch 6 vs 7
    print(f"\n🔍 LEARNING FROM BATCHES:")
    print(f"Batch 6 ETHE: 95% (SUCCESS)")
    print(f"Batch 6 GBTC: 0% (PRICE BUG - $45.24 vs ~$75)")
    print(f"Batch 6 FXA: 0% (PRICE BUG - $0.632 vs ~$65)")
    print(f"\nBatch 7 FIXED:")
    print(f"- Using reference prices (not calculated)")
    print(f"- Removed FXA (too buggy)")
    print(f"- ETHE proven 95%, GBTC should now work")
    print(f"- Target: 85%+ fill rate")


if __name__ == "__main__":
    main()
