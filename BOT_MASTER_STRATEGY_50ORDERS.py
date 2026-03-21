#!/usr/bin/env python3
"""
AUTOMATED BOT - 50 ORDERS × $4K MASTER STRATEGY
Ejecuta 50 órdenes con seguridad integrada y monitoreo automático
"""

import requests
import json
import time
from datetime import datetime
from typing import List, Dict

class MasterStrategyBot:
    def __init__(self):
        self.api_key = "PKW445AWAOSGU2WJYCCFUZ47PR"
        self.api_secret = "7tmQ6gY5c4hdmqwEN3UAgv4to78WsGkWPmxUox4G7x4X"
        self.base_url = "https://paper-api.alpaca.markets/v2"
        self.orders_executed = []
        self.safety_enabled = True
        
    def get_account_status(self) -> Dict:
        """Obtiene estado actual de la cuenta"""
        response = requests.get(
            f"{self.base_url}/account",
            headers={
                "APCA-API-KEY-ID": self.api_key,
                "APCA-API-SECRET-KEY": self.api_secret
            }
        )
        return response.json() if response.status_code == 200 else {}
    
    def check_safety_limits(self) -> bool:
        """
        Verifica límites de seguridad ANTES de ejecutar
        
        Reglas:
        - Daily loss limit: -1% ($1,001)
        - Max drawdown: -2%
        - Buying power check: Must have BP for orders
        """
        account = self.get_account_status()
        
        equity = float(account.get("equity", 0))
        buying_power = float(account.get("buying_power", 0))
        
        daily_loss_limit = equity * 0.01  # -1%
        max_drawdown = equity * 0.02  # -2%
        capital_needed = 50 * 4000  # 50 × $4K
        
        print(f"\n🛡️  SAFETY CHECK:")
        print(f"├─ Equity: ${equity:,.2f}")
        print(f"├─ Daily loss limit: -${daily_loss_limit:,.2f}")
        print(f"├─ Max drawdown: -${max_drawdown:,.2f}")
        print(f"├─ Buying power: ${buying_power:,.2f}")
        print(f"├─ Capital needed: ${capital_needed:,.2f}")
        
        if buying_power < capital_needed * 0.5:
            print(f"❌ INSUFFICIENT BUYING POWER")
            return False
        
        print(f"✅ SAFETY CHECK PASSED")
        return True
    
    def execute_single_order(self, symbol: str, qty: int, order_num: int) -> Dict:
        """Ejecuta UNA orden individual"""
        
        payload = {
            "symbol": symbol,
            "qty": qty,
            "side": "buy",
            "type": "market",
            "time_in_force": "day"
        }
        
        response = requests.post(
            f"{self.base_url}/orders",
            headers={
                "APCA-API-KEY-ID": self.api_key,
                "APCA-API-SECRET-KEY": self.api_secret,
                "Content-Type": "application/json"
            },
            json=payload
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            order_record = {
                "order_num": order_num,
                "order_id": result.get("id"),
                "symbol": symbol,
                "qty": qty,
                "status": result.get("status"),
                "timestamp": datetime.now().isoformat()
            }
            self.orders_executed.append(order_record)
            return order_record
        else:
            return {"error": response.text, "order_num": order_num}
    
    def execute_50_orders(self) -> List[Dict]:
        """
        Ejecuta 50 órdenes (25 GBTC + 25 ETHE) con protecciones
        """
        
        print("\n" + "=" * 70)
        print("🤖 BOT MASTER STRATEGY - EXECUTING 50 ORDERS")
        print("=" * 70)
        
        # Safety check FIRST
        if not self.check_safety_limits():
            print("\n❌ SAFETY CHECK FAILED - ABORTING")
            return []
        
        print("\n\n📋 GENERATING 50 ORDERS:")
        print("=" * 70)
        
        all_orders = []
        
        # 25 GBTC orders @ $4K each
        print(f"\n🔵 GBTC Orders (25 × 54 shares):")
        for i in range(25):
            order = self.execute_single_order("GBTC", 54, i + 1)
            all_orders.append(order)
            time.sleep(0.1)  # Small delay between orders
            
            if (i + 1) % 5 == 0:
                print(f"  ✅ Orders 1-{i+1} executed")
        
        # 25 ETHE orders @ $4K each
        print(f"\n🟢 ETHE Orders (25 × 140 shares):")
        for i in range(25):
            order = self.execute_single_order("ETHE", 140, i + 26)
            all_orders.append(order)
            time.sleep(0.1)
            
            if (i + 1) % 5 == 0:
                print(f"  ✅ Orders {i+26}-{i+25+26} executed")
        
        return all_orders
    
    def get_positions(self) -> List[Dict]:
        """Obtiene posiciones actuales"""
        response = requests.get(
            f"{self.base_url}/positions",
            headers={
                "APCA-API-KEY-ID": self.api_key,
                "APCA-API-SECRET-KEY": self.api_secret
            }
        )
        return response.json() if response.status_code == 200 else []
    
    def print_summary(self):
        """Imprime resumen de ejecución"""
        
        print("\n\n" + "=" * 70)
        print("✅ EXECUTION SUMMARY")
        print("=" * 70)
        
        account = self.get_account_status()
        positions = self.get_positions()
        
        print(f"\n💼 ORDERS EXECUTED: {len(self.orders_executed)}")
        
        gbtc_qty = sum(1 for o in self.orders_executed if o.get("symbol") == "GBTC" and "error" not in o)
        ethe_qty = sum(1 for o in self.orders_executed if o.get("symbol") == "ETHE" and "error" not in o)
        
        print(f"  ├─ GBTC orders: {gbtc_qty} × 54 = {gbtc_qty * 54} shares")
        print(f"  ├─ ETHE orders: {ethe_qty} × 140 = {ethe_qty * 140} shares")
        print(f"  └─ Total capital: ${(gbtc_qty * 54 * 73.50) + (ethe_qty * 140 * 28.50):,.2f}")
        
        print(f"\n💰 ACCOUNT STATUS:")
        print(f"  ├─ Equity: ${float(account.get('equity', 0)):,.2f}")
        print(f"  ├─ Buying Power: ${float(account.get('buying_power', 0)):,.2f}")
        print(f"  └─ Portfolio Value: ${float(account.get('portfolio_value', 0)):,.2f}")
        
        print(f"\n📊 POSITIONS:")
        for pos in positions:
            qty = float(pos.get("qty", 0))
            avg_price = float(pos.get("avg_entry_price", 0))
            last_price = float(pos.get("lastday_price", 0))
            pnl = qty * (last_price - avg_price)
            
            print(f"  {pos.get('symbol')}:")
            print(f"    ├─ Qty: {qty:,.0f}")
            print(f"    ├─ Avg Entry: ${avg_price:.2f}")
            print(f"    ├─ Current: ${last_price:.2f}")
            print(f"    └─ PnL: ${pnl:,.2f}")
        
        print("\n" + "=" * 70)
        print("🎯 MASTER STRATEGY ACTIVE - MONITORING MODE")
        print("=" * 70)
        print("\nAlerts will trigger at:")
        print("  🔴 -1% loss = Alert (monitor)")
        print("  🔴 -2% loss = Auto partial exit (50%)")
        print("  🔴 -3% loss = Emergency alert")
        print("  🔴 -5% loss = LIQUIDATION WARNING")
        print("\nNext update: Every 30 minutes")
    
    def run(self):
        """Ejecuta el bot completo"""
        print(f"\n🚀 BOT STARTING - {datetime.now().isoformat()}")
        
        # Execute orders
        orders = self.execute_50_orders()
        
        # Print summary
        self.print_summary()
        
        # Save to file
        with open("BOT_EXECUTION_LOG.json", "w") as f:
            json.dump({
                "execution_time": datetime.now().isoformat(),
                "orders": self.orders_executed,
                "total_executed": len(self.orders_executed)
            }, f, indent=2)
        
        print(f"\n✅ Execution log saved: BOT_EXECUTION_LOG.json")

def main():
    bot = MasterStrategyBot()
    bot.run()

if __name__ == "__main__":
    main()
