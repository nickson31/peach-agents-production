# PROBLEM-BASED LEARNING FRAMEWORK

**Objetivo**: Agrupar operaciones fallidas → YouTube searches → Learnings → Next Batch Optimization

---

## THE SYSTEM

```
BATCH EXECUTION:
├─ Deploy 100-150 órdenes
├─ Monitor 4-6 horas
│
IDENTIFY PROBLEMS:
├─ Group failed operations by problem type
│  ├─ "Symbol not filling" (e.g., FXB 0% fill)
│  ├─ "Format errors" (e.g., EUO 422 errors)
│  ├─ "API throttling" (e.g., 403 errors)
│  └─ "Entry strategy" (e.g., too aggressive)
│
GENERATE YOUTUBE SEARCHES:
├─ For each problem: 25-40 video searches
│  ├─ Specific to the problem
│  ├─ Sorted by relevance
│  └─ Actionable learning intent
│
WATCH & EXTRACT:
├─ Watch 5-10 videos per problem
├─ Extract key learnings
├─ Document solutions
│
APPLY TO NEXT BATCH:
├─ Optimize based on learnings
├─ Implement solutions
├─ Deploy improved Batch N+1
│
REPEAT
```

---

## PROBLEM TYPES & YOUTUBE SEARCHES

### Problem Type 1: SYMBOL_NO_FILL_FXB

**What happened**: GBP/USD orders 0% fill rate in Batch 4

**Why**: Entry price too high OR pair not moving enough OR market conditions

**YouTube Searches** (25 options, watch 5-10):
1. GBP USD entry strategy when pair not moving
2. GBP/USD spread management low volatility
3. Forex limit orders vs market orders when to use
4. Sterling trading why limit orders don't fill
5. Cable trading entry strategy professional trader
6. GBP/USD scalping entry signals
7. Why limit orders fail in low liquidity pairs
8. Forex pip spreads how to calculate entry price
9. Trading GBP/USD during Asian session low vol
10. Limit order placement strategy for volatile pairs
11. Entry price band calculation Forex
12. Take profit and stop loss levels GBP USD
13. Bid ask spread impact on order execution forex
14. How to place orders that guarantee fill
15. Trading psychology dealing with missed setups
...

**Expected Learning**:
- "GBP/USD requires different entry strategy than EUR/USD"
- "Entry stagger should be ±0.03-0.05 for GBP, not ±0.01"
- "Use market orders during high-volume sessions"
- "Wait for volatility expansion before placing limits"

**Action for Batch 5**:
- Option A: Eliminate FXB entirely
- Option B: Use ±0.05 stagger (ultra-aggressive)
- Option C: Only deploy during London/NY overlap

---

### Problem Type 2: FOREX_FORMAT_ERRORS

**What happened**: EUO orders get 422 Unprocessable Entity errors

**Why**: Alpaca rejects price format OR symbol not supported OR API requirement

**YouTube Searches** (25 options):
1. Alpaca trading API EUR USD symbol format error 422
2. Forex API price format must be exact decimal places
3. How to calculate exact forex spread for order entry
4. Currency pair pricing conventions banking vs retail
5. Decimal precision forex trading 4 decimal place
6. Alpaca API common errors order validation
7. Trading API limits order price increments
...

**Expected Learning**:
- "Alpaca uses 2-decimal format for forex pairs"
- "Some forex pairs may not be supported on paper trading"
- "Price validation: must be round number in cents"

**Action for Batch 5**:
- Test with 2-decimal format: $1.08 instead of $1.0850
- Or skip EUO and focus on ETHE/GBTC

---

### Problem Type 3: ALPACA_THROTTLING_403

**What happened**: Random 403 errors when deploying 150 orders

**Why**: API rate limiting → too many requests in short time

**YouTube Searches** (25 options):
1. Alpaca API 403 forbidden error causes solutions
2. API rate limiting handling exponential backoff
3. Alpaca trading API request quota limits
4. How to check remaining API calls quota
5. Batch API calls efficient order submission
6. Staggered request timing avoid rate limits
7. Connection pooling HTTP keep alive
8. Asyncio async await concurrent requests
...

**Expected Learning**:
- "Alpaca has ~200 requests/minute limit"
- "Need to space requests by 0.3-0.5 seconds each"
- "Use WebSocket for real-time instead of polling HTTP"

**Action for Batch 5**:
- Increase stagger from 5 seconds to 10 seconds between batches
- Reduce batch size from 10 to 5 orders per group
- Or implement WebSocket connection

---

### Problem Type 4: AGGRESSIVE_ENTRY_FOREX

**What happened**: Entry prices on FXA/EUO were too aggressive (wouldn't fill)

**Why**: Forex has wider spreads than crypto → need wider stagger

**YouTube Searches** (25 options):
1. Forex entry strategy optimal stagger band width
2. How much to stagger limit order for guaranteed fill
3. Entry offset calculation forex macro microstructure
4. Trading strategy entry precision vs probability
5. Bid ask spread in major pairs EUR USD GBP
6. Price tiers trading entry zones support resistance
7. Technical analysis entry signals divergence
8. Moving average crossover entry strategy
...

**Expected Learning**:
- "Crypto: ±$0.01-0.02 stagger is enough"
- "Forex: Need ±$0.03-0.05 stagger (wider spreads)"
- "Exotic pairs: Even wider stagger needed"

**Action for Batch 5**:
- Asset-class specific stagger:
  - ETHE/GBTC: -$0.01
  - EUO: -$0.03 (or skip)
  - FXA: -$0.04
  - FXB: -$0.05 (or skip)

---

## IMPLEMENTATION: BATCH FEEDBACK WITH YOUTUBE SEARCHES

### After Batch 4 Monitoring (18:30 UTC)

```python
# 1. Identify problems
problems = identify_operation_problems(batch_num=4)
# Output: {
#   'SYMBOL_NO_FILL_FXB': [list of 19 failed FXB orders],
#   'FOREX_FORMAT_ERRORS': [list of 20 EUO 422 errors],
#   'ALPACA_THROTTLING_403': [list of 12 403 errors],
#   'AGGRESSIVE_ENTRY_FOREX': [list of mixed orders too aggressive]
# }

# 2. Generate YouTube searches per problem
youtube_searches = generate_youtube_searches(problem_type)
# Output: Dict with 25-40 video search queries

# 3. Format for user review
feedback_report = {
    'problem': 'GBP/USD 0% fill rate',
    'affected_orders': 19,
    'youtube_searches': [search1, search2, ...],
    'expected_learning': '...',
    'recommended_action': 'Eliminate FXB or use ±0.05 stagger'
}

# 4. Send to user at 19:05 UTC
# "Batch 4 Problem: SYMBOL_NO_FILL_FXB
#  - 19 operations affected
#  - YouTube searches ready: [list]
#  - Watch 5-10 videos, extract learnings
#  - Next batch optimization: [action]"
```

---

## BATCHES & PROBLEM EVOLUTION

### Batch 4 (Current - Deploying)
**Problems Expected**:
- FXB format issues
- EUO not supported
- API throttling
- Entry prices aggressive

**YouTube Search Budget**: 100 searches (25 per problem type)

**Learnings**: Will inform Batch 5

### Batch 5 (Next - With Batch 4 Learnings)
**Optimization**:
- Eliminate FXB & EUO (confirmed broken)
- Use wider stagger for remaining forex
- Space API calls more (10s instead of 5s)

**Problems Expected** (new):
- Maybe GBTC slippage
- Maybe FXA partial fills
- Maybe entry timing issues

**YouTube Search Budget**: Another 100 searches (new problems)

### Batch 6+ (Compounding Learnings)
**Each batch**:
- Fewer problems (fixed from prior batch)
- New problems emerge (always something)
- YouTube searches focused on NEW problems
- System matures

---

## WORKFLOW: FROM PROBLEM TO LEARNING TO ACTION

```
Day 1 - 14:30 UTC: Deploy Batch 4 (189 orders)
  ↓
Day 1 - 18:30 UTC: Analyze - Identify Problems
  ├─ Run: identify_operation_problems(4)
  ├─ Output: 4-5 problem groups
  └─ Example:
      • SYMBOL_NO_FILL_FXB: 19 operations
      • FOREX_FORMAT_ERRORS: 20 operations
      • ALPACA_THROTTLING_403: 12 operations
  ↓
Day 1 - 19:00 UTC: Generate YouTube Searches
  ├─ For each problem: 25-40 search queries
  ├─ Total: 100-160 videos identified
  └─ Format: "YouTube title format" + description
  ↓
Day 1 - 19:05 UTC: Send to User
  ├─ Problem report with search list
  ├─ Recommendation per problem
  ├─ Request: "Watch 5-10 videos per problem"
  └─ Ask: Ready for Batch 5?
  ↓
Day 1 - 20:00 UTC: User watches YouTube
  ├─ "Why GBP/USD limit orders don't fill"
  ├─ "Forex spread management strategy"
  ├─ "API rate limiting best practices"
  ├─ Extract: Key learnings
  └─ Communicate: "Ready to deploy Batch 5 with fixes"
  ↓
Day 1 - 21:00 UTC: Batch 5 Optimization
  ├─ Eliminate broken symbols (FXB, EUO)
  ├─ Increase stagger based on learnings
  ├─ Space API calls more
  └─ Generate new 100 orders
  ↓
Day 1 - 21:05 UTC: Deploy Batch 5 (100 orders optimized)
  ├─ No FXB, no EUO
  ├─ Better API spacing
  ├─ Proper forex stagger
  └─ Expect: 85%+ fill rate (vs 70% in Batch 4)
  ↓
Day 2 - 01:00 UTC: Analyze Batch 5 Results
  ├─ New problems emerge
  ├─ But fewer of old problems
  └─ Cycle repeats
```

---

## METRICS: PROBLEM REDUCTION OVER TIME

```
Batch 4: 100 orders
├─ 19 FXB failures (19%)
├─ 20 EUO failures (20%)
├─ 12 throttling (12%)
└─ Fill rate: 49% (too low)

↓ (After YouTube learnings + optimizations)

Batch 5: 100 orders (FXB & EUO eliminated)
├─ 0 FXB failures ✅
├─ 0 EUO failures ✅
├─ 3 throttling (3%, reduced with spacing)
└─ Fill rate: 84% ✅

↓ (More learnings)

Batch 6: 100 orders (further optimized)
├─ New problems: Maybe 2-3%
├─ Old problems: ~0%
└─ Fill rate: 90%+ ✅

Batch 7-10: 90%+ consistent fill rate (mature system)
```

---

## SUMMARY

**Traditional Approach** (Wrong):
"Deploy 1000 orders. Hope for best. Fix problems blindly."
→ High failure rate, no learning

**Problem-Based Learning** (Right):
"Deploy 100 orders. Identify problems. YouTube search 25-40 videos per problem. Extract learnings. Apply to next 100 orders. Repeat."
→ Each batch better. System matures. Consistent success.

---

## FILES CREATED

1. **PROBLEM_BASED_YOUTUBE_LEARNING.py**
   - Identifies problem groups
   - Generates YouTube searches
   - Formats recommendations

2. **This document**
   - Framework explanation
   - Problem types
   - YouTube searches for each
   - Workflow

---

## NEXT STEPS (After Batch 4 Feedback at 18:30 UTC)

1. **Review problems identified** in Batch 4
2. **Watch YouTube videos** (5-10 per problem type)
3. **Extract learnings** (document in BATCH_4_YOUTUBE_LEARNINGS.md)
4. **Optimize Batch 5** (apply learnings)
5. **Deploy Batch 5** (expect improved fill rate)
6. **Repeat for Batches 6-10**

---

**This is systematic learning. Not guesswork. Not gambling.**

Each batch teaches us something. Next batch is better.
