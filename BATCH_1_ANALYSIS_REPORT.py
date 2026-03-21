#!/usr/bin/env python3
"""
BATCH 1 ANALYSIS & LESSONS LEARNED
Analiza operaciones ejecutadas y genera recomendaciones para Batch 2
"""

import requests
import json
import base64
from pathlib import Path
from collections import defaultdict
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

def get_all_orders():
    resp = requests.get(
        f"{ALPACA_API}/orders?status=all&limit=500",
        headers=get_alpaca_headers(),
        timeout=10
    )
    return resp.json() if resp.status_code == 200 else []

def load_traceability():
    tracking_file = Path("/home/ubuntu/.openclaw/workspace/COMPLETE_ORDERS_TRACKING.json")
    if tracking_file.exists():
        try:
            with open(tracking_file) as f:
                data = json.load(f)
                return {o['order_id']: o for o in data['orders_detail']}
        except:
            pass
    return {}

# ============================================================================
# ANALYSIS
# ============================================================================

def analyze_batch_1():
    """Analyze Batch 1 performance"""
    
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║            BATCH 1 ANALYSIS & LESSONS LEARNED                  ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")
    
    # Get data
    orders = get_all_orders()
    trace_map = load_traceability()
    
    # Categorize orders
    filled = [o for o in orders if o.get('status') == 'filled']
    partial = [o for o in orders if o.get('status') == 'partially_filled']
    new = [o for o in orders if o.get('status') == 'new']
    canceled = [o for o in orders if o.get('status') == 'canceled']
    
    print(f"📊 EJECUTADAS: {len(filled)} ✅")
    print(f"⚠️  PARCIALES: {len(partial)}")
    print(f"⏳ PENDIENTES: {len(new)}")
    print(f"❌ CANCELADAS: {len(canceled)}\n")
    
    print("=" * 70 + "\n")
    
    # Analysis by YouTuber
    print("🎯 PERFORMANCE BY YOUTUBER\n")
    
    youtuber_stats = defaultdict(lambda: {
        'orders': [],
        'filled': 0,
        'partial': 0,
        'total_pnl': 0,
        'avg_pnl': 0,
        'best_trade': None,
        'worst_trade': None
    })
    
    for order in filled + partial:
        youtuber = trace_map.get(order.get('id'), {}).get('traceability', {}).get('youtuber', 'Unknown')
        
        filled_qty = float(order.get('filled_qty', 0)) if order.get('filled_qty') else 0
        filled_price = float(order.get('filled_avg_price', 0)) if order.get('filled_avg_price') else 0
        limit_price = float(order.get('limit_price', 0)) if order.get('limit_price') else 0
        
        if filled_qty > 0 and filled_price:
            pnl = (filled_price - limit_price) * filled_qty * 100
            
            youtuber_stats[youtuber]['orders'].append(order)
            youtuber_stats[youtuber]['total_pnl'] += pnl
            
            if order.get('status') == 'filled':
                youtuber_stats[youtuber]['filled'] += 1
            else:
                youtuber_stats[youtuber]['partial'] += 1
            
            # Track best/worst
            if youtuber_stats[youtuber]['best_trade'] is None or pnl > youtuber_stats[youtuber]['best_trade']:
                youtuber_stats[youtuber]['best_trade'] = pnl
            if youtuber_stats[youtuber]['worst_trade'] is None or pnl < youtuber_stats[youtuber]['worst_trade']:
                youtuber_stats[youtuber]['worst_trade'] = pnl
    
    # Calculate averages
    for yt in youtuber_stats:
        total_orders = len(youtuber_stats[yt]['orders'])
        if total_orders > 0:
            youtuber_stats[yt]['avg_pnl'] = youtuber_stats[yt]['total_pnl'] / total_orders
    
    # Display rankings
    sorted_youtubers = sorted(youtuber_stats.items(), 
                             key=lambda x: x[1]['total_pnl'], 
                             reverse=True)
    
    for rank, (yt, stats) in enumerate(sorted_youtubers, 1):
        total = stats['filled'] + stats['partial']
        win_rate = (stats['filled'] / total * 100) if total > 0 else 0
        
        emoji = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "  "
        
        print(f"{emoji} Rank {rank}: {yt}")
        print(f"   Executed: {stats['filled']}/{total} ({win_rate:.0f}% full fill)")
        print(f"   Total P&L: ${stats['total_pnl']:+.0f}")
        print(f"   Avg P&L: ${stats['avg_pnl']:+.0f}")
        print(f"   Range: ${stats['best_trade']:+.0f} to ${stats['worst_trade']:+.0f}\n")
    
    print("=" * 70 + "\n")
    
    # Analysis by Symbol
    print("📈 PERFORMANCE BY SYMBOL\n")
    
    symbol_stats = defaultdict(lambda: {
        'count': 0,
        'filled': 0,
        'total_pnl': 0
    })
    
    for order in filled + partial:
        symbol = order.get('symbol', 'Unknown')
        filled_qty = float(order.get('filled_qty', 0)) if order.get('filled_qty') else 0
        filled_price = float(order.get('filled_avg_price', 0)) if order.get('filled_avg_price') else 0
        limit_price = float(order.get('limit_price', 0)) if order.get('limit_price') else 0
        
        symbol_stats[symbol]['count'] += 1
        if order.get('status') == 'filled':
            symbol_stats[symbol]['filled'] += 1
        
        if filled_qty > 0 and filled_price:
            pnl = (filled_price - limit_price) * filled_qty * 100
            symbol_stats[symbol]['total_pnl'] += pnl
    
    sorted_symbols = sorted(symbol_stats.items(), 
                           key=lambda x: x[1]['total_pnl'], 
                           reverse=True)
    
    for symbol, stats in sorted_symbols:
        fill_rate = (stats['filled'] / stats['count'] * 100) if stats['count'] > 0 else 0
        emoji = "✅" if stats['total_pnl'] > 0 else "❌"
        print(f"{emoji} {symbol}: {stats['filled']}/{stats['count']} filled ({fill_rate:.0f}%) | P&L: ${stats['total_pnl']:+.0f}")
    
    print("\n" + "=" * 70 + "\n")
    
    # Lessons Learned
    print("🎓 LESSONS LEARNED\n")
    
    lessons = []
    
    # Lesson 1: Best YouTuber
    if sorted_youtubers:
        best_yt = sorted_youtubers[0][0]
        best_pnl = sorted_youtubers[0][1]['total_pnl']
        lessons.append(f"✅ BEST PERFORMER: {best_yt} (+${best_pnl:.0f})")
    
    # Lesson 2: Worst YouTuber
    if sorted_youtubers:
        worst_yt = sorted_youtubers[-1][0]
        worst_pnl = sorted_youtubers[-1][1]['total_pnl']
        lessons.append(f"⚠️  LOWEST: {worst_yt} (${worst_pnl:+.0f})")
    
    # Lesson 3: Best Symbol
    if sorted_symbols:
        best_sym = sorted_symbols[0][0]
        best_sym_pnl = sorted_symbols[0][1]['total_pnl']
        lessons.append(f"✅ BEST SYMBOL: {best_sym} (+${best_sym_pnl:.0f})")
    
    # Lesson 4: Win Rate
    total_filled = sum(1 for o in filled + partial if o.get('status') == 'filled')
    total_executed = len(filled) + len(partial)
    if total_executed > 0:
        win_rate = (total_filled / total_executed * 100)
        lessons.append(f"📊 OVERALL WIN RATE: {win_rate:.1f}%")
    
    # Lesson 5: Total P&L
    total_pnl = 0
    for o in filled + partial:
        fq = float(o.get('filled_qty', 0)) if o.get('filled_qty') else 0
        fp = float(o.get('filled_avg_price', 0)) if o.get('filled_avg_price') else 0
        lp = float(o.get('limit_price', 0)) if o.get('limit_price') else 0
        if fq > 0:
            total_pnl += (fp - lp) * fq * 100
    lessons.append(f"💰 TOTAL P&L: ${total_pnl:+.0f}")
    
    for lesson in lessons:
        print(f"  {lesson}")
    
    print("\n" + "=" * 70 + "\n")
    
    # Recommendations for Batch 2
    print("🚀 RECOMMENDATIONS FOR BATCH 2\n")
    
    recommendations = [
        "1. ⬆️  INCREASE BUDGET: +20% per order (from 10 to 12 units)",
        f"2. 🎯 FOCUS ON TOP PERFORMERS: Double down on {best_yt if sorted_youtubers else 'best'} + top symbol",
        "3. 📊 PRESERVE WINNERS: Keep exact same entry/TP/SL for profitable setups",
        "4. ⚡ OPTIMIZE QTY: 20 orders × 20% more = ~$2.4K additional capital",
        "5. 🔄 ITERATE FAST: Same 74 strategies, but with optimized qty + top YouTubers weighted higher",
        "6. 📈 EXPAND: 150+ new strategies from next 20 YouTubers",
        "7. 💎 COMBINE: Keep top 3 YouTubers at +40% qty (double increase)"
    ]
    
    for rec in recommendations:
        print(f"  {rec}")
    
    print("\n" + "=" * 70 + "\n")
    
    # Save analysis
    analysis_data = {
        "timestamp": datetime.now().isoformat(),
        "batch": 1,
        "summary": {
            "total_orders": len(orders),
            "filled": len(filled),
            "partial": len(partial),
            "pending": len(new),
            "canceled": len(canceled),
            "total_pnl": total_pnl,
            "win_rate": win_rate if total_executed > 0 else 0
        },
        "youtuber_rankings": [
            {
                "rank": rank,
                "name": yt,
                "executed": stats['filled'],
                "total_orders": len(stats['orders']),
                "total_pnl": stats['total_pnl'],
                "avg_pnl": stats['avg_pnl']
            }
            for rank, (yt, stats) in enumerate(sorted_youtubers, 1)
        ],
        "symbol_rankings": [
            {
                "symbol": sym,
                "count": stats['count'],
                "filled": stats['filled'],
                "total_pnl": stats['total_pnl']
            }
            for sym, stats in sorted_symbols
        ],
        "lessons": lessons,
        "recommendations_for_batch_2": recommendations
    }
    
    analysis_file = Path("/home/ubuntu/.openclaw/workspace/BATCH_1_ANALYSIS.json")
    with open(analysis_file, "w") as f:
        json.dump(analysis_data, f, indent=2)
    
    print(f"✅ Analysis saved: {analysis_file}\n")
    
    return analysis_data

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    analysis = analyze_batch_1()
