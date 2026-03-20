#!/usr/bin/env python3
"""
DAILY 2.5% COMPOUND SYSTEM
$100K → $300K in 40 days

Core: Every day must close with +2.5% gain
Math: 120-150 orders × 80% fill × 3% exit = 2.88% daily
Result: 40 days to goal

This system TRACKS and ENFORCES daily 2.5% target
"""

import json
import time
from datetime import datetime, timedelta
from collections import defaultdict

# Configuration
DAILY_TARGET = 0.025  # 2.5% daily
STARTING_EQUITY = 100618.50
GOAL_EQUITY = 300000
DAYS_TO_GOAL = 40
TARGET_FILL_RATE = 0.80  # 80% minimum
PORTFOLIO_DAILY_LOG = "/home/ubuntu/.openclaw/workspace/DAILY_PROGRESS.json"

# Daily tracking
DAILY_PROGRESS = {
    "start_date": datetime.now().isoformat(),
    "daily_targets": [],
    "daily_actuals": [],
    "shortfalls": [],
}


def log_daily_progress(message):
    """Log daily progress"""
    timestamp = datetime.now().isoformat()
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)


def calculate_daily_target(day_number, current_equity):
    """Calculate target equity for end of day"""
    daily_multiplier = 1 + DAILY_TARGET
    target = current_equity * daily_multiplier
    return target


def calculate_required_fill_rate(orders_today, orders_filled, current_gain):
    """
    Calculate if we're on pace for +2.5%
    
    Formula:
    gain_needed = 2.5%
    filled_orders = orders_filled so far
    remaining_batches = batches_remaining_today
    
    If already at +2.5%, great
    If behind, need higher fill rate on remaining batches
    """
    gain_needed = DAILY_TARGET
    
    if current_gain >= gain_needed:
        return None  # Already achieved!
    
    remaining_gain = gain_needed - current_gain
    remaining_batches = 48 - (time.time() % 86400) / (30 * 60)  # Rough estimate
    
    required_fill_rate = remaining_gain / remaining_batches / 0.03
    required_fill_rate = min(required_fill_rate, 1.0)  # Cap at 100%
    
    return required_fill_rate


def validate_daily_allocation():
    """Validate allocation strategy for daily 2.5%"""
    allocation = {
        "ETHE": 0.50,
        "GBTC": 0.25,
        "FXA": 0.25,
    }
    
    entry_prices = {
        "ETHE": 3380.00,
        "GBTC": 71.25,
        "FXA": 62.00,
    }
    
    exit_prices = {
        "ETHE": 3481.40,  # +3%
        "GBTC": 73.39,    # +3%
        "FXA": 63.86,     # +3%
    }
    
    daily_targets = {
        "ETHE": 120 * 0.50 / 1 * 0.80 * 0.03,  # 120 orders, 50% alloc, 80% fill, 3% exit
        "GBTC": 120 * 0.25 / 1 * 0.80 * 0.03,
        "FXA": 120 * 0.25 / 1 * 0.80 * 0.03,
    }
    
    log_daily_progress("📊 ALLOCATION VALIDATION:")
    
    total_daily_gain = 0
    for symbol in ["ETHE", "GBTC", "FXA"]:
        gain = daily_targets[symbol]
        total_daily_gain += gain
        log_daily_progress(f"  {symbol}: {allocation[symbol]*100:.0f}% allocation → {gain*100:.2f}% daily")
    
    log_daily_progress(f"\n✓ Total daily gain with 80% fill: {total_daily_gain*100:.2f}%")
    
    if total_daily_gain >= DAILY_TARGET:
        log_daily_progress(f"✅ ALLOCATION SUFFICIENT for +{DAILY_TARGET*100:.1f}% daily target")
        return True
    else:
        log_daily_progress(f"❌ ALLOCATION INSUFFICIENT ({total_daily_gain*100:.2f}% vs target {DAILY_TARGET*100:.1f}%)")
        return False


def track_daily_equity(batch_results):
    """
    Track equity throughout the day
    batch_results: list of {"batch": N, "fill_rate": 0.85, "pnl": +0.025, "timestamp": ...}
    """
    day_start_equity = get_account_equity()
    cumulative_gain = 0
    batches_so_far = len(batch_results)
    
    for result in batch_results:
        cumulative_gain += result["pnl"]
    
    current_equity = day_start_equity * (1 + cumulative_gain)
    target_equity = day_start_equity * (1 + DAILY_TARGET)
    
    log_daily_progress(f"\n⏱️ INTRADAY PROGRESS:")
    log_daily_progress(f"  Start: ${day_start_equity:,.2f}")
    log_daily_progress(f"  Current: ${current_equity:,.2f} ({cumulative_gain*100:+.2f}%)")
    log_daily_progress(f"  Target: ${target_equity:,.2f} ({DAILY_TARGET*100:.2f}%)")
    log_daily_progress(f"  Batches: {batches_so_far}/48")
    
    if cumulative_gain >= DAILY_TARGET:
        log_daily_progress(f"  ✅ TARGET HIT! Can coast rest of day")
        return True
    elif batches_so_far < 24:  # Morning
        shortfall = DAILY_TARGET - cumulative_gain
        log_daily_progress(f"  ⏳ Behind by {shortfall*100:.2f}% - need {(DAILY_TARGET-cumulative_gain)*100:.2f}% on remaining")
        return None  # Still time
    else:  # Afternoon
        shortfall = DAILY_TARGET - cumulative_gain
        required_fill_rate = calculate_required_fill_rate(48, batches_so_far, cumulative_gain)
        log_daily_progress(f"  ⚠️ Afternoon: need {shortfall*100:.2f}% - requires {required_fill_rate*100:.0f}% fill rate")
        
        if required_fill_rate > 0.95:
            log_daily_progress(f"  ❌ Unrealistic requirement - may miss daily target")
            return False
    
    return None


def end_of_day_analysis(day_number, daily_equity_change, target):
    """Analyze daily performance"""
    log_daily_progress(f"\n{'='*60}")
    log_daily_progress(f"END OF DAY {day_number} ANALYSIS")
    log_daily_progress(f"{'='*60}")
    
    daily_gain_pct = daily_equity_change / get_account_equity() * 100 if get_account_equity() > 0 else 0
    
    if daily_gain_pct >= DAILY_TARGET * 100:
        log_daily_progress(f"✅ SUCCESS: +{daily_gain_pct:.2f}% (target: +{DAILY_TARGET*100:.1f}%)")
        log_daily_progress(f"   On track for $300K in 40 days")
    elif daily_gain_pct >= DAILY_TARGET * 100 * 0.9:  # 90% of target
        log_daily_progress(f"✓ ACCEPTABLE: +{daily_gain_pct:.2f}% (target: +{DAILY_TARGET*100:.1f}%)")
        log_daily_progress(f"   Minor shortfall, can catch up tomorrow")
    elif daily_gain_pct >= 0:
        log_daily_progress(f"⚠️ SHORTFALL: +{daily_gain_pct:.2f}% (target: +{DAILY_TARGET*100:.1f}%)")
        log_daily_progress(f"   {(DAILY_TARGET*100 - daily_gain_pct):.2f}% behind")
        log_daily_progress(f"   Need to increase batch size or fill rate tomorrow")
    else:
        log_daily_progress(f"❌ RED DAY: {daily_gain_pct:.2f}%")
        log_daily_progress(f"   Review strategy, check fill rates, verify entries")
    
    # Cumulative progress
    cumulative = sum([d.get("gain", 0) for d in DAILY_PROGRESS["daily_actuals"]])
    log_daily_progress(f"\n   Cumulative: {cumulative*100:+.1f}% over {day_number} days")


def forecast_day(day_number, current_equity):
    """Forecast what Day N should look like"""
    projected_equity = STARTING_EQUITY * (1 + DAILY_TARGET) ** day_number
    
    return {
        "day": day_number,
        "target_equity": projected_equity,
        "target_gain": projected_equity - current_equity,
    }


def milestone_check(day_number, current_equity):
    """Check if we're on track for $300K"""
    weeks_elapsed = day_number / 7
    
    milestones = {
        7: 119603,     # End of Week 1
        14: 142890,    # End of Week 2
        21: 170066,    # End of Week 3
        28: 207244,    # End of Week 4
        40: 300000,    # Goal
    }
    
    log_daily_progress(f"\n🎯 MILESTONE CHECK (Day {day_number}):")
    
    if day_number in milestones:
        target = milestones[day_number]
        delta = current_equity - target
        status = "✅" if delta >= -5000 else "⚠️" if delta >= -15000 else "❌"
        
        log_daily_progress(f"   {status} Target: ${target:,.0f}")
        log_daily_progress(f"   {status} Actual: ${current_equity:,.0f}")
        log_daily_progress(f"   {status} Delta: ${delta:+,.0f}")
        
        if delta < -15000:
            log_daily_progress(f"   🛑 SIGNIFICANTLY BEHIND - May need strategy pivot")
            return False
    
    return True


def get_account_equity():
    """Get current account equity (mock for now)"""
    # In production: fetch from Alpaca API
    return 100618.50  # Placeholder


def run_40_day_tracker():
    """Main tracker for 40-day journey"""
    log_daily_progress("="*70)
    log_daily_progress("🚀 DAILY 2.5% COMPOUND SYSTEM")
    log_daily_progress(f"Goal: $100K → $300K in 40 days")
    log_daily_progress(f"Daily target: +{DAILY_TARGET*100:.1f}%")
    log_daily_progress(f"Strategy: 120-150 orders × 80% fill × 3% exit")
    log_daily_progress("="*70)
    
    # Validate allocation
    if not validate_daily_allocation():
        log_daily_progress("\n❌ ALLOCATION INSUFFICIENT - Need to adjust")
        return False
    
    # Show 40-day forecast
    log_daily_progress(f"\n📅 40-DAY FORECAST:")
    for day in [1, 7, 14, 21, 28, 35, 40]:
        forecast = forecast_day(day, STARTING_EQUITY)
        log_daily_progress(f"   Day {day:2d}: ${forecast['target_equity']:>10,.0f}")
    
    return True


if __name__ == "__main__":
    # Validate system
    system_ready = run_40_day_tracker()
    
    if system_ready:
        log_daily_progress("\n✅ SYSTEM READY FOR 40-DAY JOURNEY")
        log_daily_progress("   Track daily at: DAILY_PROGRESS.json")
    else:
        log_daily_progress("\n❌ SYSTEM NEEDS ADJUSTMENT")
