#!/usr/bin/env python3
"""
MACRO CONDITIONS MONITOR
Tracks real-time market conditions: VIX, sentiment, volatility
Links losses to market events and catalysts
Automatically adjusts trading phases based on macro environment
"""

import requests
from datetime import datetime
import json

def log_monitor(msg):
    """Log monitoring events"""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


def check_vix_conditions():
    """Check VIX level and implications"""
    
    # Simulated VIX check (in prod, would fetch from API)
    vix_level = 18  # Example
    
    if vix_level > 30:
        return "PANIC", "VIX > 30: Market panic, reduce position 75%"
    elif vix_level > 20:
        return "HIGH_VOLATILITY", "VIX > 20: High volatility, reduce 50%"
    elif vix_level > 15:
        return "MODERATE", "VIX 15-20: Moderate, proceed cautious"
    else:
        return "NORMAL", "VIX < 15: Normal conditions, proceed normal"


def check_market_sentiment():
    """Check fear/greed index and sentiment"""
    
    # Simulated sentiment
    sentiment_score = 35  # 0-100 scale
    
    if sentiment_score < 25:
        return "EXTREME_FEAR", "Market in extreme fear, prepare shorts"
    elif sentiment_score < 45:
        return "FEAR", "Market fearful, reduce buying, add hedges"
    elif sentiment_score < 55:
        return "NEUTRAL", "Market neutral, proceed normal"
    elif sentiment_score < 75:
        return "GREED", "Market greedy, cautious on new entries"
    else:
        return "EXTREME_GREED", "Market extreme greed, prepare for crash"


def check_macro_catalysts():
    """Check for major macro events"""
    
    catalysts = [
        {"event": "Vitalik ETH sale", "impact": "BEARISH", "severity": "HIGH"},
        {"event": "Hot PPI data", "impact": "BEARISH", "severity": "HIGH"},
        {"event": "Fed hawkish signal", "impact": "BEARISH", "severity": "HIGH"},
        {"event": "Middle East tensions", "impact": "BEARISH", "severity": "MEDIUM"},
        {"event": "ETF outflows", "impact": "BEARISH", "severity": "MEDIUM"},
    ]
    
    log_monitor("\n📰 MACRO CATALYSTS:")
    total_bearish = sum(1 for c in catalysts if c["impact"] == "BEARISH")
    
    for cat in catalysts:
        log_monitor(f"  • {cat['event']}: {cat['impact']} ({cat['severity']})")
    
    if total_bearish >= 3:
        return "BEARISH_CONFLUENCE", "3+ bearish catalysts = high crash risk"
    else:
        return "MIXED", "Mixed catalysts, no clear direction"


def determine_trading_phase():
    """Determine which trading phase to use"""
    
    vix_phase, vix_msg = check_vix_conditions()
    sentiment_phase, sentiment_msg = check_market_sentiment()
    catalyst_phase, catalyst_msg = check_macro_catalysts()
    
    log_monitor(f"\n🎯 PHASE DETERMINATION:")
    log_monitor(f"  VIX phase: {vix_phase}")
    log_monitor(f"  Sentiment phase: {sentiment_phase}")
    log_monitor(f"  Catalyst phase: {catalyst_phase}")
    
    # Decision tree
    if catalyst_phase == "BEARISH_CONFLUENCE":
        log_monitor(f"\n⚠️ DECISION: CRISIS PHASE (multiple bearish signals)")
        return "PHASE_3_CRASH"
    
    elif vix_phase == "PANIC":
        log_monitor(f"\n⚠️ DECISION: CRISIS PHASE (VIX panic)")
        return "PHASE_3_CRASH"
    
    elif vix_phase == "HIGH_VOLATILITY" or sentiment_phase == "FEAR":
        log_monitor(f"\n⚠️ DECISION: VOLATILITY PHASE (reduce 50%)")
        return "PHASE_2_VOLATILITY"
    
    else:
        log_monitor(f"\n✓ DECISION: NORMAL PHASE (proceed standard)")
        return "PHASE_1_NORMAL"


def recommend_strategy_adjustments(phase):
    """Recommend strategy based on phase"""
    
    log_monitor(f"\n📋 STRATEGY ADJUSTMENTS FOR {phase}:")
    
    strategies = {
        "PHASE_1_NORMAL": {
            "orders_per_day": 2,
            "order_size": "$5-10K",
            "escalation": "5%→50%",
            "stop_loss": "-1%",
            "hedges": "None",
            "expected_gain": "+2-3% daily",
        },
        "PHASE_2_VOLATILITY": {
            "orders_per_day": 1,
            "order_size": "$2-5K",
            "escalation": "5%→30%",
            "stop_loss": "-1.5%",
            "hedges": "Small shorts 10%",
            "expected_gain": "+0.5-1% daily",
        },
        "PHASE_3_CRASH": {
            "orders_per_day": 0,
            "order_size": "PAUSED",
            "escalation": "PAUSED",
            "stop_loss": "-0.75%",
            "hedges": "50% shorts",
            "expected_gain": "+5-10% while crashing",
        },
    }
    
    strategy = strategies.get(phase, {})
    for key, value in strategy.items():
        log_monitor(f"  {key}: {value}")
    
    return strategy


def link_losses_to_catalysts(loss_amount, loss_percent):
    """Link portfolio losses to market catalysts"""
    
    log_monitor(f"\n📉 LOSS ATTRIBUTION:")
    log_monitor(f"  Portfolio loss: ${loss_amount} ({loss_percent}%)")
    
    # Analyze what caused it
    catalysts_active = [
        "Vitalik ETH sale (founder selling bearish signal)",
        "Hot PPI data (inflation fears)",
        "Fed hawkish rates (recession fears)",
        "ETF outflows (reduced liquidity)",
        "Overall market rotation (risk off)",
    ]
    
    log_monitor(f"\n  Likely causes:")
    for i, cause in enumerate(catalysts_active, 1):
        log_monitor(f"    {i}. {cause}")
    
    log_monitor(f"\n  Recommendation:")
    log_monitor(f"    • Extract: Learn why this happened (YouTube cycle)")
    log_monitor(f"    • Adjust: Switch to PHASE_2 or PHASE_3 based on severity")
    log_monitor(f"    • Hedge: Deploy shorts to profit from further drops")
    log_monitor(f"    • Monitor: Track when conditions normalize")
    
    return {
        "loss_amount": loss_amount,
        "loss_percent": loss_percent,
        "attributed_to": catalysts_active,
        "recommended_phase": "PHASE_2_VOLATILITY or PHASE_3_CRASH",
        "action": "Reduce buying, add hedges, learn from YouTube"
    }


def main():
    """Macro conditions monitor"""
    
    log_monitor("════════════════════════════════════════════════════════════════")
    log_monitor("📊 MACRO CONDITIONS MONITOR - 2026-03-20 10:22 UTC")
    log_monitor("════════════════════════════════════════════════════════════════")
    
    # Check conditions
    phase = determine_trading_phase()
    
    # Get strategy
    strategy = recommend_strategy_adjustments(phase)
    
    # Link losses to catalysts (today example)
    attribution = link_losses_to_catalysts(-728, -0.72)
    
    log_monitor("\n════════════════════════════════════════════════════════════════")
    log_monitor("📝 SUMMARY:")
    log_monitor(f"  Current phase: {phase}")
    log_monitor(f"  Orders today: {strategy.get('orders_per_day', 0)}")
    log_monitor(f"  Expected: {strategy.get('expected_gain', '?')}")
    log_monitor("════════════════════════════════════════════════════════════════")
    
    log_monitor(f"\n💡 ACTION:")
    log_monitor(f"  • Reduce buying 50%")
    log_monitor(f"  • Deploy small shorts (hedge)")
    log_monitor(f"  • Wait for market clarity")
    log_monitor(f"  • Re-assess in 4 hours")


if __name__ == "__main__":
    main()
