#!/usr/bin/env python3
"""
PROBLEM-BASED YOUTUBE LEARNING SYSTEM

Agrupa operaciones fallidas/problemáticas por tipo.
Por cada problema: genera búsquedas YouTube, extrae learnings.
Aplica a siguiente batch.
"""

import requests
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def identify_operation_problems(batch_num):
    """Identify groups of failed/problematic operations"""
    
    print("╔════════════════════════════════════════════════════════════════╗")
    print(f"║         PROBLEM-BASED GROUPING - BATCH {batch_num}              ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")
    
    # Load batch results
    results_file = Path(f"/home/ubuntu/.openclaw/workspace/BATCH_{batch_num}_DEPLOYMENT_RESULTS.json")
    
    if not results_file.exists():
        print(f"⚠️  No results found for Batch {batch_num}\n")
        return None
    
    with open(results_file) as f:
        batch_data = json.load(f)
    
    problems = defaultdict(list)
    
    # Categorize by problem type
    for order in batch_data.get('orders_detail', []):
        symbol = order.get('symbol', 'Unknown')
        youtuber = order.get('traceability', {}).get('youtuber', 'Unknown')
        status = order.get('status', 'unknown')
        
        # Problem 1: Symbol not filling (0% fill rate)
        if symbol == 'FXB':
            problems['SYMBOL_NO_FILL_FXB'].append({
                'symbol': symbol,
                'youtuber': youtuber,
                'entry': order.get('limit_price'),
                'issue': 'GBP/USD not reaching entry price'
            })
        
        # Problem 2: EUO format errors
        if symbol == 'EUO':
            problems['FOREX_FORMAT_ERRORS'].append({
                'symbol': symbol,
                'youtuber': youtuber,
                'entry': order.get('limit_price'),
                'issue': 'Alpaca rejects EUR/USD price format'
            })
        
        # Problem 3: Error 403 (Alpaca throttling)
        if 'error_code' in order and order['error_code'] == 403:
            problems['ALPACA_THROTTLING_403'].append({
                'symbol': symbol,
                'youtuber': youtuber,
                'issue': 'API rate limiting'
            })
        
        # Problem 4: Entry prices too aggressive (Forex pairs)
        if symbol in ['FXA', 'EUO', 'FXB'] and order.get('entry_offset', 0) < -0.02:
            problems['AGGRESSIVE_ENTRY_FOREX'].append({
                'symbol': symbol,
                'youtuber': youtuber,
                'entry': order.get('limit_price'),
                'issue': f'Entry stagger too aggressive for {symbol}'
            })
    
    print("📊 PROBLEMS IDENTIFIED:\n")
    
    problem_groups = {}
    
    for problem_type, operations in problems.items():
        print(f"🔴 {problem_type}: {len(operations)} operations")
        print(f"   Sample operations:")
        for op in operations[:3]:
            print(f"   - {op.get('symbol')} by {op.get('youtuber')}: {op.get('issue')}")
        print()
        
        problem_groups[problem_type] = {
            'count': len(operations),
            'operations': operations,
            'youtube_searches': generate_youtube_searches(problem_type, operations),
        }
    
    return problem_groups

def generate_youtube_searches(problem_type, operations):
    """Generate YouTube search queries for a problem type"""
    
    print(f"\n🎬 YOUTUBE SEARCHES FOR: {problem_type}\n")
    
    searches = {}
    
    if problem_type == 'SYMBOL_NO_FILL_FXB':
        searches = {
            1: "GBP USD entry strategy when pair not moving",
            2: "GBP/USD spread management low volatility",
            3: "Forex limit orders vs market orders when to use",
            4: "Sterling trading why limit orders don't fill",
            5: "Cable trading entry strategy professional trader",
            6: "GBP/USD scalping entry signals",
            7: "Why limit orders fail in low liquidity pairs",
            8: "Forex pip spreads how to calculate entry price",
            9: "Trading GBP/USD during Asian session low vol",
            10: "Limit order placement strategy for volatile pairs",
            11: "Entry price band calculation Forex",
            12: "Take profit and stop loss levels GBP USD",
            13: "Bid ask spread impact on order execution forex",
            14: "How to place orders that guarantee fill",
            15: "Trading psychology dealing with missed setups",
            16: "Slippage management in limit order trading",
            17: "Market microstructure forex liquidity",
            18: "Order execution timing forex market hours",
            19: "Day trader entry strategy consistent wins",
            20: "Risk reward ratio finding perfect setups",
            21: "Cable trading chart patterns",
            22: "GBP price action trading tutorial",
            23: "When to abandon a trade setup",
            24: "Mechanical trading system rules based",
            25: "Position sizing based on volatility forex",
        }
    
    elif problem_type == 'FOREX_FORMAT_ERRORS':
        searches = {
            1: "Alpaca trading API EUR USD symbol format error 422",
            2: "Forex API price format must be exact decimal places",
            3: "How to calculate exact forex spread for order entry",
            4: "Currency pair pricing conventions banking vs retail",
            5: "Decimal precision forex trading 4 decimal place",
            6: "Alpaca API common errors order validation",
            7: "Trading API limits order price increments",
            8: "Pip definition forex smallest price movement",
            9: "Forex broker liquidity providers price data",
            10: "Real-time forex quote price accuracy",
            11: "ECN vs market maker order execution differences",
            12: "Slippage in forex why orders don't execute at price",
            13: "Order routing algorithms smart order routing",
            14: "High frequency trading microsecond timing",
            15: "Algorithmic trading best execution standards",
            16: "API documentation reading debugging fixes",
            17: "Trading systems implementation production ready",
            18: "Order book depth market liquidity visualization",
            19: "Bid ask spread what determines it",
            20: "Market makers role in liquidity",
            21: "Latency in trading systems network optimization",
            22: "Quote streaming real time vs delayed",
            23: "Regulatory requirements order validation",
            24: "Trading compliance SEC FINRA rules",
            25: "Professional trader platform Ninja Trader ThinkorSwim",
        }
    
    elif problem_type == 'AGGRESSIVE_ENTRY_FOREX':
        searches = {
            1: "Forex entry strategy optimal stagger band width",
            2: "How much to stagger limit order for guaranteed fill",
            3: "Entry offset calculation forex macro micro structure",
            4: "Trading strategy entry precision vs probability",
            5: "Bid ask spread in major pairs EUR USD GBP",
            6: "Price tiers trading entry zones support resistance",
            7: "Technical analysis entry signals divergence",
            8: "Moving average crossover entry strategy",
            9: "Bollinger bands entry trade signals",
            10: "RSI overbought entry strategy trading",
            11: "MACD histogram entry points momentum",
            12: "Order flow analysis entry timing",
            13: "Volume profile entry levels institutional buying",
            14: "ICE bank funding entry strategy",
            15: "Central bank decision forex movement prediction",
            16: "Economic news trading entry strategy",
            17: "Seasonal patterns forex trading calendar",
            18: "Correlation pairs forex diamond trade",
            19: "Carry trade strategy long term entry",
            20: "Swing trading entry strategy daily chart",
            21: "Scalping entry strategy 1 minute chart",
            22: "Day trading entry setup confluences",
            23: "Risk management position sizing Kelly criterion",
            24: "Expectancy calculation winning percentage",
            25: "Trade management trailing stop profit taking",
        }
    
    elif problem_type == 'ALPACA_THROTTLING_403':
        searches = {
            1: "Alpaca API 403 forbidden error causes solutions",
            2: "API rate limiting handling exponential backoff",
            3: "Alpaca trading API request quota limits",
            4: "How to check remaining API calls quota",
            5: "Batch API calls efficient order submission",
            6: "Staggered request timing avoid rate limits",
            7: "Connection pooling HTTP keep alive",
            8: "Asyncio async await concurrent requests",
            9: "WebSocket connection real-time updates reduce HTTP",
            10: "Trading bot best practices API reliability",
            11: "Circuit breaker pattern error handling",
            12: "Retry logic with jitter exponential backoff",
            13: "Queue based order execution system design",
            14: "Load testing API endpoints performance",
            15: "Horizontal scaling distributed trading system",
            16: "Message broker RabbitMQ Kafka order queue",
            17: "Database connection pooling thousands concurrent",
            18: "Caching layer Redis reduce API calls",
            19: "Monitoring alerts system health dashboards",
            20: "Logging tracing distributed systems debugging",
            21: "Testing frameworks unit tests integration",
            22: "CI CD deployment pipeline automation",
            23: "Infrastructure as code terraform provisioning",
            24: "Cloud serverless functions AWS Lambda",
            25: "DevOps practices production reliability",
        }
    
    else:
        searches = {i: f"Generic forex trading strategy {i}" for i in range(1, 26)}
    
    for num, search in searches.items():
        print(f"  {num:2d}. {search}")
    
    return searches

def generate_batch_feedback_with_youtube(batch_num):
    """Generate feedback that includes YouTube learnings"""
    
    problems = identify_operation_problems(batch_num)
    
    if not problems:
        return None
    
    print("\n" + "=" * 70 + "\n")
    
    print("🎓 LEARNINGS TO EXTRACT FROM YOUTUBE:\n")
    
    learnings = {}
    
    if 'SYMBOL_NO_FILL_FXB' in problems:
        learnings['FXB_FIX'] = {
            'problem': 'GBP/USD 0% fill rate',
            'youtube_topics': [
                'Why limit orders fail in GBP/USD',
                'GBP spread dynamics vs EUR',
                'Entry strategy for volatile pairs',
                'Bid-ask spread impact on execution'
            ],
            'expected_learning': 'GBP/USD requires wider stagger band or different entry strategy',
            'action': 'Either eliminate FXB or use +0.03 to +0.05 stagger in next batch'
        }
    
    if 'FOREX_FORMAT_ERRORS' in problems:
        learnings['EUO_FORMAT_FIX'] = {
            'problem': '422 Unprocessable Entity errors on EUO',
            'youtube_topics': [
                'API decimal precision requirements',
                'Forex price format standards',
                'Order validation rules'
            ],
            'expected_learning': 'Alpaca may require specific decimal format or EUO symbol might not be supported',
            'action': 'Test with 2-decimal format or skip EUO entirely in next batch'
        }
    
    if 'ALPACA_THROTTLING_403' in problems:
        learnings['THROTTLING_FIX'] = {
            'problem': '403 errors from API rate limiting',
            'youtube_topics': [
                'Rate limit handling exponential backoff',
                'Staggered request timing patterns',
                'WebSocket vs REST API efficiency'
            ],
            'expected_learning': 'Need longer delays between API calls or use WebSocket for real-time data',
            'action': 'Increase stagger interval from 5 to 10 seconds in next batch'
        }
    
    if 'AGGRESSIVE_ENTRY_FOREX' in problems:
        learnings['ENTRY_STRATEGY_FIX'] = {
            'problem': 'Entry prices too aggressive for Forex pairs',
            'youtube_topics': [
                'Optimal stagger band width calculation',
                'Market microstructure bid-ask dynamics',
                'Entry precision vs probability tradeoff'
            ],
            'expected_learning': 'Forex requires different stagger than Crypto due to wider spreads',
            'action': 'Use market-dependent stagger: Crypto (-0.01-0.02), Forex (-0.03-0.05)'
        }
    
    for learning_key, details in learnings.items():
        print(f"💡 {details['problem']}")
        print(f"   YouTube topics to research:")
        for topic in details['youtube_topics']:
            print(f"   - {topic}")
        print(f"   Expected learning: {details['expected_learning']}")
        print(f"   Action for Batch N+1: {details['action']}\n")
    
    return learnings

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    
    print("\n")
    
    # Analyze Batch 4 problems and generate YouTube searches
    learnings = generate_batch_feedback_with_youtube(4)
    
    print("\n" + "=" * 70 + "\n")
    
    print("✅ NEXT STEPS:\n")
    print("1. Review YouTube searches for each problem type")
    print("2. Watch 5-10 videos per problem (up to 40 total)")
    print("3. Extract key learnings")
    print("4. Apply to Batch 5 optimizations")
    print("5. Repeat cycle\n")
    
    print("=" * 70)
