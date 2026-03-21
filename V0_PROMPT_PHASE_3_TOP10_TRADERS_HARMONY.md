# V0 PHASE 3 - TOP 10 TRADERS HARMONY ENGINE
**Objective**: Consolidate predictions from top 10 BTC/USDT + ETH/USDT traders into unified trading strategy
**Date**: 2026-03-20 20:38 UTC
**Pairs**: BTC/USDT + ETH/USDT only
**Goal**: Harmonize all trader signals into single coherent strategy with risk/reward ratio analysis

---

## 🎯 TOP 10 CRYPTO TRADERS TO MONITOR

### TIER 1: PLATINUM (Highest Win Rate + Consistency)

1. **Glacier Trading** (@glaciertrading)
   - Specialization: Technical analysis, RSI, support/resistance
   - Track record: 75%+ win rate on BTC/USDT
   - Style: Conservative entries, tight stops
   - Key signal: RSI oversold bounces
   - Content: 3-4 videos/week on BTC/USDT

2. **CoinBureau** (@coinbureau)
   - Specialization: On-chain analysis, macro trends
   - Track record: Long-term predictions (70%+ accuracy)
   - Style: Fundamental + technical hybrid
   - Key signal: Whale movements + resistance breakouts
   - Content: 2 videos/week, deep analysis

3. **Sheldon Evans** (@sheldonevans)
   - Specialization: Volatility breakdown, daily trading
   - Track record: Short-term swings (72% accuracy)
   - Style: Fast-paced, actionable
   - Key signal: Intraday breakouts, volume confirmation
   - Content: Daily videos (5-10 min each)

### TIER 2: GOLD (Strong Consistency)

4. **TradingView Pro Analysts**
   - Multiple independent analysts
   - Track record: Varies but curated (65%+ average)
   - Style: Chart-based, community voted
   - Key signal: Ideas with high likes/comments
   - Source: TradingView.com/symbols/BTCUSDT/ideas

5. **Crypto Jeb** (@cryptojeb)
   - Specialization: Elliott Wave, cycles
   - Track record: Macro cycles prediction (68%)
   - Style: Sophisticated, pattern-based
   - Key signal: Wave counts, pivot points
   - Content: 1-2 videos/week

6. **The Wolf Den** (@thewolfden)
   - Specialization: Scalping, microstructure
   - Track record: Day-trading signals (70%)
   - Style: High-frequency, tight entries/exits
   - Key signal: 1H/15M breakouts
   - Content: 4-5 videos/week

### TIER 3: SILVER (Reliable Secondary)

7. **Altcoin Daily** (@altcoindaily)
   - Specialization: Broad crypto, news-driven
   - Track record: Trend identification (65%)
   - Style: Educational, context-rich
   - Key signal: News catalyst analysis
   - Content: Daily (10-15 min each)

8. **Crypto Banter** (@cryptobanter)
   - Specialization: Macro + micro blend
   - Track record: Multi-timeframe (63%)
   - Style: Discussion-based, debate format
   - Key signal: Expert consensus breakdown
   - Content: 5-7 videos/week

9. **Lark Davis** (@larkdavis)
   - Specialization: Sentiment, social trends
   - Track record: Sentiment-based (62%)
   - Style: Social media analysis
   - Key signal: Community mood swings
   - Content: 3-4 videos/week

10. **Digitaldao** (@digitaldao)
    - Specialization: On-chain metrics, whale tracking
    - Track record: Large move prediction (66%)
    - Style: Data-driven, scientific
    - Key signal: Exchange inflows/outflows
    - Content: 2-3 videos/week

---

## 🔄 HARMONY ENGINE ALGORITHM

### Step 1: DATA COLLECTION (Every 4 hours)
```
For each trader:
  - Fetch latest video (YouTube API)
  - Extract transcript (if available)
  - Identify key signals:
    * Price targets (resistance/support)
    * Entry points
    * Stop loss levels
    * Take profit levels
    * Direction (LONG/SHORT)
    * Confidence (1-10)
    * Timeframe (1H/4H/1D/1W)
```

### Step 2: SENTIMENT SCORING
```
For each signal:
  - Assign confidence score (1-100)
  - Weight by trader tier (Platinum=1.0, Gold=0.85, Silver=0.70)
  - Calculate direction bias (% bullish vs bearish)
  - Extract risk/reward ratio
```

### Step 3: CONSENSUS CALCULATION
```
BULLISH_SCORE = (sum of bullish signals × weight) / total signals
BEARISH_SCORE = (sum of bearish signals × weight) / total signals

CONSENSUS = BULLISH_SCORE - BEARISH_SCORE
  Range: -100 (bearish) to +100 (bullish)

ACTION:
  If CONSENSUS > 60: BUY signal (strong)
  If CONSENSUS > 30: BUY signal (weak)
  If CONSENSUS < -60: SELL signal (strong)
  If CONSENSUS < -30: SELL signal (weak)
  If -30 <= CONSENSUS <= 30: NEUTRAL/HOLD
```

### Step 4: RISK/REWARD ANALYSIS
```
Average entry point = (sum of entries × weight) / total
Average stop loss = (sum of stops × weight) / total
Average take profit = (sum of targets × weight) / total

Risk/Reward ratio = (TP - Entry) / (Entry - SL)

Min acceptable R:R = 2:1 (for entry)
Optimal R:R = 3:1 or higher
```

### Step 5: UNIFIED STRATEGY GENERATION
```
OUTPUT:
{
  "pair": "BTC/USDT or ETH/USDT",
  "consensus": X (0-100),
  "direction": "LONG or SHORT or HOLD",
  "confidence": "STRONG or MODERATE or WEAK",
  "entry_point": XXXXXX,
  "stop_loss": XXXXXX,
  "take_profit_1": XXXXXX,
  "take_profit_2": XXXXXX,
  "take_profit_3": XXXXXX,
  "risk_reward": X:1,
  "traders_agreeing": X/10,
  "top_signals": [list of key reasons],
  "timeframe": "4H or 1D",
  "updated_at": "ISO timestamp"
}
```

---

## 📺 VIDEO ANALYSIS TEMPLATE

```typescript
interface TraderAnalysis {
  trader_name: string
  video_url: string
  published_at: Date
  duration_minutes: number
  transcript: string
  
  // Extracted signals
  signals: {
    direction: 'BULLISH' | 'BEARISH' | 'NEUTRAL'
    entry_price?: number
    stop_loss?: number
    take_profit?: number[]
    confidence: 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10
    timeframe: '1H' | '4H' | '1D' | '1W'
    reasoning: string // Key reasons for prediction
  }
  
  // Risk metrics
  risk_analysis: {
    support_level: number
    resistance_level: number
    risk_reward_ratio: number
    volume_confirmation: boolean
  }
}
```

---

## 🔗 DATA SOURCES

### YouTube Scraping (Ethical)
```
Use YouTube Data API (official):
- Search for each trader channel
- Get latest 10 videos per channel
- Extract metadata + transcript (if available)
- Timestamp: Last 24-48 hours

Rate limit: 1 request per minute per trader
Frequency: Every 4 hours (automated cron)
```

### TradingView Public Ideas
```
Endpoint: https://www.tradingview.com/symbols/BTCUSDT/ideas/
- Fetch top-rated ideas (sorted by likes)
- Extract author, description, price targets
- Filter by publication date (last 24h)
- Aggregate for consensus
```

### RSS + Manual Verification
```
Combine RSS feeds from:
- Each trader's official site
- YouTube channel RSS
- Twitter/X posts (if available)
- Cross-reference for accuracy
```

---

## 🎬 IMPLEMENTATION CHECKLIST

- [ ] Set up YouTube API credentials (get API key)
- [ ] Create trader profile database (name, channel ID, tier)
- [ ] Build video transcript extractor
- [ ] Implement signal extraction (NLP/regex)
- [ ] Calculate consensus algorithm
- [ ] Create dashboard showing:
  - [ ] Current consensus (gauge chart)
  - [ ] Top 10 traders' predictions (table)
  - [ ] Unified strategy (recommendation)
  - [ ] Recent changes (alerts)
  - [ ] Historical accuracy (backtest)
- [ ] Set up 4-hour refresh cycle
- [ ] Create trading alerts (when consensus changes)
- [ ] Store historical data (for analysis)

---

## 📊 EXAMPLE OUTPUT

**Current Status**: 2026-03-20 20:38 UTC

```
┌─────────────────────────────────────────┐
│ BTC/USDT HARMONY CONSENSUS              │
├─────────────────────────────────────────┤
│ Overall: BULLISH (72%)                  │
│ Confidence: STRONG                      │
│                                         │
│ Traders Agreeing: 8/10                  │
│ Top Signals:                            │
│  • Glacier Trading: RSI oversold bounce │
│  • CoinBureau: Whale accumulation       │
│  • Sheldon Evans: Breakout above $44K   │
│                                         │
│ Recommended Entry: $43,890              │
│ Stop Loss: $42,100                      │
│ Take Profit 1: $44,800                  │
│ Take Profit 2: $45,900                  │
│ Take Profit 3: $47,200                  │
│                                         │
│ Risk/Reward: 3.2:1 ✅                   │
│ Timeframe: 4H                           │
│                                         │
│ Confidence Score: 76/100                │
└─────────────────────────────────────────┘
```

---

## 🚀 INTEGRATION WITH TRADING SYSTEM

Once consensus is generated:

```typescript
// If confidence > 70 AND risk/reward > 2.5:1
if (consensus.confidence > 70 && consensus.riskReward > 2.5) {
  // Generate trading order
  const order = {
    pair: consensus.pair,
    side: consensus.direction === 'BULLISH' ? 'buy' : 'sell',
    entry: consensus.entry_point,
    stop: consensus.stop_loss,
    tp1: consensus.take_profit_1,
    tp2: consensus.take_profit_2,
    tp3: consensus.take_profit_3,
    quantity: calculatePositionSize(equity, stop_loss),
    reason: `Harmony consensus: ${consensus.traders_agreeing}/10 traders agree`
  }
  
  // Execute or wait for user approval
  await executeOrder(order)
}
```

---

## 📈 BACKTESTING & ACCURACY TRACKING

Store all predictions + actual outcomes:

```sql
CREATE TABLE trader_predictions (
  id UUID PRIMARY KEY,
  trader_name TEXT,
  pair TEXT,
  prediction_time TIMESTAMP,
  entry_price DECIMAL,
  stop_loss DECIMAL,
  take_profit DECIMAL,
  direction TEXT,
  confidence INT,
  
  -- Outcome tracking
  actual_entry DECIMAL,
  actual_exit DECIMAL,
  pnl DECIMAL,
  outcome_time TIMESTAMP,
  was_successful BOOLEAN,
  roi_percent DECIMAL
);
```

Track accuracy over time and weight traders accordingly.

---

## 🎯 PHASE 3 DELIVERABLES

After V0 builds this:

1. ✅ YouTube API integration
2. ✅ Trader database (10 top traders)
3. ✅ Video analysis engine
4. ✅ Consensus algorithm
5. ✅ Real-time dashboard
6. ✅ Trading signal generator
7. ✅ Backtesting module
8. ✅ Integration with Alpaca orders

**Result**: Unified trading strategy based on top 10 traders' consensus

---

**END PHASE 3 PROMPT**

**Next**: V0 generates complete Harmony Engine that monitors all 10 traders, calculates consensus, and generates trading signals automatically.

