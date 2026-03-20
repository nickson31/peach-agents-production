#!/usr/bin/env python3
"""
BATCH FEEDBACK SYSTEM
Monitorea cada batch, recopila datos, genera insights,
y autoriza el siguiente batch solo cuando hay learnings accionables
"""

import requests
import json
import base64
import time
from pathlib import Path
from datetime import datetime
from collections import defaultdict

ALPACA_KEY = "PKW445AWAOSGU2WJYCCFUZ47PR"
ALPACA_SECRET = "7tmQ6gY5c4hdmqwEN3UAgv4to78WsGkWPmxUox4G7x4X"
ALPACA_API = "https://paper-api.alpaca.markets/v2"

def get_headers():
    auth = base64.b64encode(f"{ALPACA_KEY}:{ALPACA_SECRET}".encode()).decode()
    return {"Authorization": f"Basic {auth}"}

def load_batch_metadata(batch_num):
    """Load metadata for a batch"""
    file = Path(f"/home/ubuntu/.openclaw/workspace/BATCH_{batch_num}_DEPLOYMENT_RESULTS.json")
    if file.exists():
        try:
            with open(file) as f:
                return json.load(f)
        except:
            pass
    return None

def analyze_batch_performance(batch_num):
    """Analyze performance of a deployed batch"""
    
    print("╔════════════════════════════════════════════════════════════════╗")
    print(f"║         BATCH {batch_num} FEEDBACK ANALYSIS - REAL-TIME DATA    ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")
    
    # Get current orders
    resp = requests.get(f"{ALPACA_API}/orders?status=all&limit=500", headers=get_headers(), timeout=10)
    all_orders = resp.json() if resp.status_code == 200 else []
    
    # Load batch metadata
    batch_meta = load_batch_metadata(batch_num)
    
    if not batch_meta:
        print(f"⚠️  No metadata found for Batch {batch_num}\n")
        return None
    
    print(f"📊 BATCH {batch_num} ANALYSIS\n")
    print(f"Deployment time: {batch_meta.get('timestamp', 'N/A')}")
    print(f"Total orders planned: {batch_meta.get('total_orders', 0)}")
    print(f"Capital allocated: ${batch_meta.get('total_capital', 0):,.0f}\n")
    
    print("=" * 70 + "\n")
    
    # Analyze fills by symbol
    symbol_stats = defaultdict(lambda: {'total': 0, 'filled': 0, 'pending': 0, 'canceled': 0})
    youtuber_stats = defaultdict(lambda: {'total': 0, 'filled': 0, 'pending': 0})
    
    for order in batch_meta.get('orders_detail', []):
        order_id = order.get('order_id')
        symbol = order.get('symbol', 'Unknown')
        youtuber = order.get('traceability', {}).get('youtuber', 'Unknown')
        
        # Find matching order in current orders
        matching = next((o for o in all_orders if o.get('id') == order_id), None)
        
        if matching:
            status = matching.get('status', 'unknown').lower()
            symbol_stats[symbol]['total'] += 1
            youtuber_stats[youtuber]['total'] += 1
            
            if status == 'filled':
                symbol_stats[symbol]['filled'] += 1
                youtuber_stats[youtuber]['filled'] += 1
            elif status == 'new':
                symbol_stats[symbol]['pending'] += 1
                youtuber_stats[youtuber]['pending'] += 1
            elif status == 'canceled':
                symbol_stats[symbol]['canceled'] += 1
    
    print("📈 PERFORMANCE BY SYMBOL:\n")
    
    for symbol in sorted(symbol_stats.keys()):
        stats = symbol_stats[symbol]
        total = stats['total']
        filled = stats['filled']
        pending = stats['pending']
        fill_rate = (filled / total * 100) if total > 0 else 0
        
        emoji = "🟢" if fill_rate > 70 else "🟡" if fill_rate > 40 else "🔴"
        print(f"{emoji} {symbol}:")
        print(f"   Total: {total} | Filled: {filled} ({fill_rate:.0f}%) | Pending: {pending}")
    
    print("\n" + "=" * 70 + "\n")
    
    print("👥 PERFORMANCE BY YOUTUBER:\n")
    
    sorted_yts = sorted(youtuber_stats.items(), key=lambda x: x[1]['filled'], reverse=True)
    
    for youtuber, stats in sorted_yts[:10]:  # Top 10
        total = stats['total']
        filled = stats['filled']
        fill_rate = (filled / total * 100) if total > 0 else 0
        
        emoji = "⭐" if fill_rate > 80 else "✅" if fill_rate > 60 else "⚠️"
        print(f"{emoji} {youtuber}: {filled}/{total} filled ({fill_rate:.0f}%)")
    
    print("\n" + "=" * 70 + "\n")
    
    # Generate insights
    print("💡 KEY INSIGHTS:\n")
    
    overall_fill_rate = 0
    total_filled = 0
    total_orders = 0
    
    for stats in symbol_stats.values():
        total_filled += stats['filled']
        total_orders += stats['total']
    
    if total_orders > 0:
        overall_fill_rate = (total_filled / total_orders * 100)
    
    print(f"Overall fill rate: {overall_fill_rate:.1f}%")
    print(f"Total filled: {total_filled} orders")
    print(f"Total pending: {sum(s['pending'] for s in symbol_stats.values())} orders")
    print(f"Total canceled: {sum(s['canceled'] for s in symbol_stats.values())} orders\n")
    
    # Identify best & worst symbols
    sorted_symbols = sorted(symbol_stats.items(), 
                           key=lambda x: (x[1]['filled'] / x[1]['total'] if x[1]['total'] > 0 else 0), 
                           reverse=True)
    
    if sorted_symbols:
        best_symbol = sorted_symbols[0][0]
        best_rate = (sorted_symbols[0][1]['filled'] / sorted_symbols[0][1]['total'] * 100) if sorted_symbols[0][1]['total'] > 0 else 0
        print(f"✅ Best symbol: {best_symbol} ({best_rate:.0f}% fill rate)")
        
        worst_symbol = sorted_symbols[-1][0]
        worst_rate = (sorted_symbols[-1][1]['filled'] / sorted_symbols[-1][1]['total'] * 100) if sorted_symbols[-1][1]['total'] > 0 else 0
        print(f"❌ Worst symbol: {worst_symbol} ({worst_rate:.0f}% fill rate)\n")
    
    # Identify best YouTuber
    sorted_yts_by_perf = sorted(youtuber_stats.items(),
                               key=lambda x: (x[1]['filled'] / x[1]['total'] if x[1]['total'] > 0 else 0),
                               reverse=True)
    
    if sorted_yts_by_perf:
        top_yt = sorted_yts_by_perf[0][0]
        top_rate = (sorted_yts_by_perf[0][1]['filled'] / sorted_yts_by_perf[0][1]['total'] * 100) if sorted_yts_by_perf[0][1]['total'] > 0 else 0
        print(f"⭐ Top YouTuber: {top_yt} ({top_rate:.0f}% success rate)")
    
    print("\n" + "=" * 70 + "\n")
    
    # Recommendations for next batch
    print("🎯 RECOMMENDATIONS FOR NEXT BATCH:\n")
    
    recommendations = []
    
    if best_symbol and best_rate > 80:
        recommendations.append(f"✅ Increase {best_symbol} allocation to 50% (proven {best_rate:.0f}% success)")
    
    if worst_symbol and worst_rate < 50:
        recommendations.append(f"❌ Reduce {worst_symbol} allocation (only {worst_rate:.0f}% success rate)")
    
    if overall_fill_rate > 75:
        recommendations.append("✅ Aggressive expansion authorized (fill rate >75%)")
    elif overall_fill_rate > 50:
        recommendations.append("⚠️ Moderate expansion (fill rate 50-75%) - hold before scaling")
    else:
        recommendations.append("🔴 Hold deployment - investigate fill rate issues first")
    
    if sort_yts_by_perf:
        top_yt_rate = (sorted_yts_by_perf[0][1]['filled'] / sorted_yts_by_perf[0][1]['total'] * 100) if sorted_yts_by_perf[0][1]['total'] > 0 else 0
        if top_yt_rate > 85:
            recommendations.append(f"✅ Allocate 30% of next batch to {top_yt} (top performer)")
    
    for rec in recommendations:
        print(f"  {rec}")
    
    print("\n" + "=" * 70 + "\n")
    
    # Ready for next batch?
    print("✅ READINESS FOR NEXT BATCH:\n")
    
    ready = overall_fill_rate > 60
    
    if ready:
        print(f"🟢 READY TO DEPLOY - Fill rate {overall_fill_rate:.1f}% is healthy")
    else:
        print(f"🔴 WAIT - Fill rate {overall_fill_rate:.1f}% needs investigation")
        print("   Recommend: Pause, analyze, then optimize before next batch")
    
    print("\n" + "=" * 70 + "\n")
    
    return {
        'batch_num': batch_num,
        'timestamp': datetime.now().isoformat(),
        'overall_fill_rate': overall_fill_rate,
        'total_filled': total_filled,
        'total_orders': total_orders,
        'best_symbol': best_symbol,
        'worst_symbol': worst_symbol,
        'recommendations': recommendations,
        'ready_for_next': ready,
    }

def should_deploy_next_batch(current_batch_analysis):
    """Determine if we should deploy the next batch based on current performance"""
    
    if not current_batch_analysis:
        return False
    
    fill_rate = current_batch_analysis.get('overall_fill_rate', 0)
    
    if fill_rate > 70:
        return True  # Aggressive expansion authorized
    elif fill_rate > 50:
        return "hold"  # Wait and gather more data
    else:
        return False  # Stop and investigate

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    
    print("\n")
    
    # Analyze Batch 4 (current batch deployed)
    batch_4_analysis = analyze_batch_performance(4)
    
    if batch_4_analysis:
        print("\n" + "=" * 70 + "\n")
        
        decision = should_deploy_next_batch(batch_4_analysis)
        
        print("📋 NEXT BATCH DEPLOYMENT DECISION:\n")
        
        if decision is True:
            print("✅ AUTHORIZED: Deploy Batch 5 immediately with recommendations")
            print("   Fill rate is healthy, learnings incorporated, ready to scale\n")
        elif decision == "hold":
            print("⏸️  HOLD: Collect more data before Batch 5 deployment")
            print("   Fill rate is moderate - wait 1-2 hours then reassess\n")
        else:
            print("🔴 BLOCKED: Do NOT deploy Batch 5 until issues resolved")
            print("   Fill rate too low - investigate root causes first\n")
        
        print("=" * 70 + "\n")
        
        # Save analysis
        analysis_file = Path("/home/ubuntu/.openclaw/workspace/BATCH_4_FEEDBACK_ANALYSIS.json")
        with open(analysis_file, "w") as f:
            json.dump(batch_4_analysis, f, indent=2)
        
        print(f"✅ Analysis saved to BATCH_4_FEEDBACK_ANALYSIS.json\n")
