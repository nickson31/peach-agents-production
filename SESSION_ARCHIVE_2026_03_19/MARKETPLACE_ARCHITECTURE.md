# MARKETPLACE — Strategy Store (Private Portal)

## VISIÓN GENERAL

```
┌─────────────────────────────────────────────────────────────┐
│              STRATEGY MARKETPLACE                           │
│         (Private within Racha community)                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  "El Spotify de estrategias de trading"                    │
│                                                             │
│  ├─ Descubre estrategias (de olimpiadas, YouTube, users)   │
│  ├─ Valida con backtest personal                           │
│  ├─ Activa para que agente la ejecute (future OpenClaw)   │
│  └─ Creador gana 0.5-1% de tus ganancias                   │
│                                                             │
│  Solo para Racha users (private SaaS marketplace)          │
│  NOT: Public app store (evita regulación)                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## DATABASE: CENTRAL STRATEGY REGISTRY

### Main Table: `strategies` (The Product)

```sql
CREATE TABLE strategies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Identity & Versioning
  strategy_name VARCHAR(255) NOT NULL,
  strategy_version INT DEFAULT 1,  -- Updates allowed
  
  -- Creator
  creator_user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  creator_name VARCHAR(255),  -- Display name ("TradingMaster88")
  creator_avatar VARCHAR(510),
  
  -- Source (where did it come from?)
  source_type VARCHAR(50) NOT NULL,
    -- 'youtube_transcript' = extracted from YouTube video
    -- 'olimpiada_winner' = won an olimpiada
    -- 'user_upload' = user submitted manually
    -- 'platform_curated' = we found it and verified
  
  source_reference JSONB,
    -- YouTube: {video_id, channel_name, transcript_url}
    -- Olimpiada: {olimpiada_id, rank_position, date}
    -- User: {uploaded_by_user_id, date}
  
  -- Strategy Definition (THE CORE)
  symbol VARCHAR(50) NOT NULL,  -- EUR_USD, BTC_USD, etc
  timeframe VARCHAR(10) NOT NULL,  -- 1m, 5m, 15m, 1h, 4h, daily
  
  entry_logic JSONB,
    -- {
    --   trigger: "soporte + bounce",
    --   entry_price: 1.0875 (or NULL if dynamic),
    --   conditions: ["price_above_MA20", "volume_spike"],
    --   rules: "texto libre describing conditions"
    -- }
  
  exit_logic JSONB,
    -- {
    --   tp_price: 1.0750 (or NULL if dynamic),
    --   sl_price: 1.0950 (or NULL if risk-based),
    --   tp_exit_rule: "hit target",
    --   sl_exit_rule: "stop loss",
    --   time_exit_rule: "if open > 4 hours, close at EOD"
    -- }
  
  risk_management JSONB,
    -- {
    --   risk_percent_per_trade: 1.5,
    --   max_position_size: 10,  -- lots or units
    --   max_daily_loss_percent: 5.0,
    --   max_open_positions: 1,
    --   consecutive_loss_limit: 3  -- pause after 3 losses
    -- }
  
  -- Performance Metrics (aggregate from all users)
  stats JSONB,
    -- {
    --   total_backtests: 150,
    --   avg_win_rate: 0.67,
    --   avg_pnl: 2450,
    --   users_count: 23,  -- how many traders using it
    --   total_pnl_generated: 56350  -- sum of all users' profits
    -- }
  
  -- Popularity & Trust
  rating DECIMAL(3,2),  -- 0.0-5.0
  rating_count INT,
  reviews TEXT[],  -- ["Great strategy!", "5% slippage issues"]
  
  -- Visibility & Availability
  status VARCHAR(50) DEFAULT 'published',
    -- 'draft' = creator hasn't published yet
    -- 'published' = available in marketplace
    -- 'archived' = old, not accepting new users
  
  is_open_to_new_users BOOLEAN DEFAULT true,
  
  -- Revenue Model
  revenue_share_percent DECIMAL(3,2) NOT NULL,
    -- Typically: 0.5-1.0 (0.5% to 1% of trader's PnL)
  
  creator_earnings DECIMAL(15,2) DEFAULT 0,  -- Aggregate
  
  -- Metadata
  description TEXT,
  tags TEXT[],  -- ['EUR/USD', 'soporte', 'scalping', 'day-trading']
  
  best_market_conditions JSONB,
    -- {trending: 'uptrend', volatility: 'low-medium', time: 'NY session'}
  
  worst_market_conditions JSONB,
    -- {trending: 'sideways', volatility: 'extreme', time: 'overlap'}
  
  disclaimers TEXT,  -- "Past performance ≠ future. Backtest first."
  
  -- Timeline
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  published_at TIMESTAMP,
  
  -- Indexes
  PRIMARY KEY (id),
  INDEX idx_creator_user_id (creator_user_id),
  INDEX idx_symbol (symbol),
  INDEX idx_source_type (source_type),
  INDEX idx_status (status),
  INDEX idx_rating (rating DESC),
  INDEX idx_users_count (stats->'users_count' DESC)
);

-- View: Top Strategies (by rating, users, recent)
CREATE VIEW marketplace_top_strategies AS
SELECT
  id, strategy_name, creator_name, creator_avatar,
  symbol, timeframe,
  rating, rating_count,
  (stats->>'users_count')::INT as users_count,
  (stats->>'avg_win_rate')::DECIMAL as avg_win_rate,
  revenue_share_percent,
  created_at
FROM strategies
WHERE status = 'published' AND is_open_to_new_users = true
ORDER BY rating DESC, (stats->>'users_count')::INT DESC, created_at DESC;
```

---

### Execution Table: `strategy_subscriptions` (Who uses what)

```sql
CREATE TABLE strategy_subscriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Foreign keys
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  strategy_id UUID NOT NULL REFERENCES strategies(id) ON DELETE CASCADE,
  
  -- Subscription Details
  subscribed_at TIMESTAMP DEFAULT NOW(),
  activated_at TIMESTAMP,  -- When user started using it
  
  -- Custom Parameters (user can tweak)
  custom_entry_offset DECIMAL(5,3),  -- Add/subtract from entry
  custom_tp_offset DECIMAL(5,3),
  custom_sl_offset DECIMAL(5,3),
  custom_risk_percent DECIMAL(3,1),  -- Override strategy default
  
  -- Execution Status
  status VARCHAR(50) DEFAULT 'saved',
    -- 'saved' = in library, not running
    -- 'backtesting' = user testing
    -- 'paper_trading' = demo account (future)
    -- 'live_trading' = real account (future with OpenClaw)
    -- 'paused' = user paused it
    -- 'halted' = we halted (too much loss, etc)
  
  -- Backtesting (before going live)
  backtest_data JSONB,
    -- {
    --   period: '30 days',
    --   win_rate: 0.68,
    --   num_trades: 42,
    --   pnl: 3250,
    --   max_drawdown: 0.05,
    --   tested_at: '2026-03-19'
    -- }
  
  -- Live Performance (if executed with agent)
  live_pnl DECIMAL(15,2) DEFAULT 0,  -- Running total
  live_win_rate DECIMAL(5,2),
  live_trades_count INT DEFAULT 0,
  last_trade_at TIMESTAMP,
  
  -- Revenue Share Tracking
  total_trades_pnl DECIMAL(15,2),  -- Sum of all trades
  creator_earnings_share DECIMAL(15,2),  -- 0.5-1% of pnl
  platform_earnings_share DECIMAL(15,2),  -- Rest of cut
  
  subscription_fee_paid DECIMAL(15,2),  -- If user paid upfront (future)
  
  -- Metadata
  notes TEXT,  -- User's personal notes
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  -- Constraints & Indexes
  UNIQUE KEY unique_user_strategy (user_id, strategy_id),
  INDEX idx_user_id (user_id),
  INDEX idx_strategy_id (strategy_id),
  INDEX idx_status (status),
  INDEX idx_live_pnl (live_pnl DESC),
  INDEX idx_created_at (created_at)
);

-- View: User's Active Strategies
CREATE VIEW user_active_strategies AS
SELECT
  ss.id as subscription_id,
  s.strategy_name,
  s.creator_name,
  s.symbol,
  s.timeframe,
  ss.status,
  ss.live_pnl,
  ss.live_win_rate,
  ss.live_trades_count,
  (s.stats->>'avg_win_rate')::DECIMAL as expected_win_rate
FROM strategy_subscriptions ss
JOIN strategies s ON ss.strategy_id = s.id
WHERE ss.user_id = $1 AND ss.status NOT IN ('archived', 'halted')
ORDER BY ss.live_pnl DESC;
```

---

### Revenue Tracking: `strategy_revenue` (The Money)

```sql
CREATE TABLE strategy_revenue (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Trade Reference
  strategy_id UUID NOT NULL REFERENCES strategies(id),
  user_id UUID NOT NULL REFERENCES users(id),  -- the trader
  creator_id UUID NOT NULL REFERENCES users(id),  -- strategy creator
  
  -- Trade Result
  trade_pnl DECIMAL(15,2),  -- User's profit/loss
  trade_date TIMESTAMP,
  
  -- Revenue Split
  creator_percent DECIMAL(5,2),  -- 0.5 or 1.0, etc
  creator_earnings DECIMAL(15,2),  -- Calculated
  platform_percent DECIMAL(5,2),  -- 0.5 to 1.0
  platform_earnings DECIMAL(15,2),
  
  -- Status
  is_settled BOOLEAN DEFAULT false,  -- Paid out to creator?
  settled_at TIMESTAMP,
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_strategy_id (strategy_id),
  INDEX idx_creator_id (creator_id),
  INDEX idx_user_id (user_id),
  INDEX idx_is_settled (is_settled),
  INDEX idx_created_at (created_at)
);

-- View: Creator Earnings Dashboard
CREATE VIEW creator_earnings_dashboard AS
SELECT
  creator_id,
  strategy_id,
  (SELECT strategy_name FROM strategies WHERE id = strategy_id) as strategy_name,
  COUNT(*) as total_trades,
  SUM(trade_pnl) as total_user_pnl,
  SUM(creator_earnings) as creator_total_earnings,
  SUM(CASE WHEN is_settled = false THEN creator_earnings ELSE 0 END) as pending_earnings,
  COUNT(DISTINCT user_id) as active_users,
  ROUND(AVG(CASE WHEN trade_pnl > 0 THEN 1.0 ELSE 0 END) * 100, 2) as user_win_rate
FROM strategy_revenue
GROUP BY creator_id, strategy_id;
```

---

## STORAGE ARCHITECTURE

### Where strategies live:

```
┌──────────────────────────────────────────────────────┐
│           STRATEGY STORAGE LAYERS                    │
└──────────────────────────────────────────────────────┘

TIER 1: SUPABASE JSONB (Fast queries, indexed)
├─ Full strategy definition (entry_logic, exit_logic, risk)
├─ Stats + ratings
├─ Creator info
└─ For: Browse, search, filter in marketplace

TIER 2: SUPABASE JSONB BACKUPS (Historical)
├─ Old strategy versions
├─ Audit trail (what changed?)
└─ For: Detect if creator cheated (changed strategy after good results)

TIER 3: S3 (Long-term archive)
├─ If strategy becomes huge (~1MB+ data)
├─ Full backtest history
├─ All trade executions
└─ For: Analytics, compliance

TIER 4: VERTORdb or similar (Future - ML)
├─ Strategy embeddings (vectorize the strategy)
├─ Similar strategy search ("Find strategies like this")
└─ For: Recommendations, discovery machine learning
```

---

## MARKETPLACE UI/UX

### Page 1: Marketplace Browse

```
┌──────────────────────────────────────────────────────┐
│     MARKETPLACE — Discover Strategies                 │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Search: [EUR/USD    ]  Filter: [Symbol ▼] [Sort ▼] │
│  Tags: [Soporte] [Bounce] [Day Trading] ...          │
│                                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │ #1 🏆 "Soporte Bounce EUR/USD"                 │  │
│  │                                                │  │
│  │ Creator: TradingMaster88  ⭐ 4.9 (150 ratings) │  │
│  │ Symbol: EUR/USD | Timeframe: 1h                │  │
│  │ Win Rate: 68% | Users: 45 | Revenue: 0.5%     │  │
│  │                                                │  │
│  │ "Soporte + volumen spike. Uptrend only. SL    │  │
│  │  muy conservative (25 pips). Perfecto en     │  │
│  │  London session."                              │  │
│  │                                                │  │
│  │ [View Details] [Test It] [Add to Library]     │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │ #2 "Divergence GBP/USD"                        │  │
│  │                                                │  │
│  │ Creator: ForexAcademy  ⭐ 4.7 (89 ratings)    │  │
│  │ Symbol: GBP/USD | Timeframe: 4h                │  │
│  │ Win Rate: 52% | Users: 12 | Revenue: 1.0%     │  │
│  │                                                │  │
│  │ [View Details] [Test It] [Add to Library]     │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │ #3 "Crypto Scalper BTC"                        │  │
│  │ ...                                            │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
└──────────────────────────────────────────────────────┘

FILTERS:
├─ Symbol: [EUR/USD] [GBP/USD] [BTC/USD] ...
├─ Timeframe: [1m-5m] [15m-1h] [4h] [daily]
├─ Win Rate: [50%-60%] [60%-70%] [70%+]
├─ Users: [1-10] [10-50] [50+]
├─ Revenue Share: [0.5%] [0.75%] [1.0%]
├─ Market Condition: [Trending] [Ranging] [Volatile]
└─ Sort By: [Rating] [Users] [Recent] [Win Rate]
```

### Page 2: Strategy Detail

```
┌──────────────────────────────────────────────────────┐
│  "Soporte Bounce EUR/USD"                            │
│  Creator: TradingMaster88                            │
├──────────────────────────────────────────────────────┤
│                                                      │
│  LEFT COLUMN: STRATEGY RULES                        │
│  ──────────────────────────────                     │
│  Entry:                                              │
│  ├─ "EUR/USD = soporte reconocido"                   │
│  ├─ "Volumen > 1.5x media"                           │
│  ├─ "Precio toca soporte + rebota 10 pips"          │
│  └─ Entry: 1.0875                                    │
│                                                      │
│  Exit:                                               │
│  ├─ TP: 1.0750 (125 pips)                           │
│  ├─ SL: 1.0950 (75 pips)                            │
│  └─ Risk:Reward = 1:1.67                             │
│                                                      │
│  Risk Management:                                    │
│  ├─ Risk per trade: 1.5%                             │
│  ├─ Max daily loss: 5%                               │
│  ├─ Max positions: 1                                 │
│  └─ Pause after 3 losses                             │
│                                                      │
│  Best For:                                           │
│  ├─ Market: Uptrend                                  │
│  ├─ Session: London (08:00-16:00)                   │
│  └─ Volatility: Low-Medium                           │
│                                                      │
│  ───────────────────────────────────────────       │
│  Creator: TradingMaster88                            │
│  ├─ YouTube: 450K suscriptores                       │
│  ├─ Trading exp: 8+ años                             │
│  └─ [View Channel]                                   │
│                                                      │
│  RIGHT COLUMN: PERFORMANCE                          │
│  ─────────────────────────────                      │
│  Overall Stats:                                      │
│  ├─ Rating: ⭐⭐⭐⭐⭐ 4.9 (150 reviews)             │
│  ├─ Users: 45 active                                 │
│  ├─ Total P&L: +$102,645                             │
│  └─ Revenue per creator: $513/mo                     │
│                                                      │
│  User Reviews:                                       │
│  ├─ "Game changer! +$2K first month" ⭐⭐⭐⭐⭐    │
│  ├─ "Works in London session, slippage at 8:05" ⭐⭐⭐⭐ │
│  ├─ "Didn't work for me in choppy markets" ⭐⭐⭐   │
│  └─ [View All Reviews]                               │
│                                                      │
│  Performance Chart:                                  │
│  ├─ [Cumulative P&L — all users]                    │
│  ├─ [Win Rate over time]                             │
│  ├─ [Drawdown history]                               │
│  └─ [User count growth]                              │
│                                                      │
│  Revenue Model:                                      │
│  ├─ Creator Gets: 0.5% of your trades              │
│  │   Example: If you make $1,000, creator gets $5   │
│  ├─ Platform Gets: 0.5% ($5)                         │
│  └─ You Keep: 99% ($990)                             │
│                                                      │
│  BUTTONS:                                            │
│  ├─ [Add to My Library]                              │
│  ├─ [Backtest on My Data]                            │
│  ├─ [Share Strategy]                                 │
│  └─ [Report/Flag Strategy]                           │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### Page 3: Backtest & Activate

```
┌──────────────────────────────────────────────────────┐
│  "Test Strategy on Your Data"                        │
├──────────────────────────────────────────────────────┤
│                                                      │
│  BACKTEST SETUP:                                     │
│  ├─ Symbol: [EUR_USD ▼]                              │
│  ├─ Period: [Last 30 days ▼]                         │
│  ├─ Custom Entry: [+0.0005 offset] (optional)       │
│  ├─ Custom TP: [+0.0 offset]                         │
│  ├─ Custom Risk: [1.5% ▼]                            │
│  └─ [RUN BACKTEST]                                   │
│                                                      │
│  ✓ RESULTS:                                          │
│  ├─ Win Rate: 68% (29/43 trades)                    │
│  ├─ Total P&L: +$3,240                               │
│  ├─ Max Drawdown: -5.2%                              │
│  ├─ Avg Win: $145                                    │
│  ├─ Avg Loss: -$95                                   │
│  └─ Profit Factor: 2.45                              │
│                                                      │
│  Chart: [Equity Curve]                               │
│                                                      │
│  ───────────────────────────────────────────       │
│  "Results look good! Ready to use?"                  │
│                                                      │
│  ❌ DISCLAIMERS:                                     │
│  ├─ "Backtest ≠ Future Performance"                 │
│  ├─ "Slippage, spread not included"                 │
│  ├─ "Past data may not repeat"                       │
│  └─ [I Understand]                                   │
│                                                      │
│  NEXT STEPS:                                         │
│  ├─ [Save Without Using]                             │
│  ├─ [Activate in Paper Trading] (future)             │
│  └─ [Schedule for Live Trading] (future)             │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### Page 4: Creator Dashboard

```
┌──────────────────────────────────────────────────────┐
│  YOUR STRATEGIES — Creator Dashboard                 │
├──────────────────────────────────────────────────────┤
│                                                      │
│  "Soporte Bounce EUR/USD"                            │
│  Status: Published | Active Users: 45                │
│  Rating: 4.9 ⭐ | Revenue: 0.5%                     │
│                                                      │
│  ┌─────────────────────────────────────────────┐   │
│  │ This Month Earnings:                        │   │
│  │ ├─ User P&L Total: $102,645                 │   │
│  │ ├─ Your 0.5%: $513 ✓ Paid                   │   │
│  │ └─ Next Payout: April 1                      │   │
│  └─────────────────────────────────────────────┘   │
│                                                      │
│  Monthly:                                            │
│  ├─ Jan: $245 earned                                 │
│  ├─ Feb: $392 earned                                 │
│  ├─ Mar: $513 earned (growing! 📈)                  │
│  └─ [View Detailed Breakdown]                        │
│                                                      │
│  Active Users (45):                                  │
│  ├─ User A: +$8,500 (earned you $42.50)              │
│  ├─ User B: +$2,100 (earned you $10.50)              │
│  ├─ User C: -$500 (you earned $0)                    │
│  └─ [View All]                                       │
│                                                      │
│  Top Performers (using your strategy):               │
│  ├─ #1: User X with +$15K this month                 │
│  ├─ #2: User Y with +$9.2K                           │
│  └─ #3: User Z with +$7.8K                           │
│                                                      │
│  Reviews & Feedback:                                 │
│  ├─ New review from User: "This saved my trading"    │
│  ├─ User Z flagged: "Slippage in ny session"        │
│  └─ [Respond to Feedback]                            │
│                                                      │
│  ACTIONS:                                            │
│  ├─ [Edit Strategy] (will version it)                │
│  ├─ [Pause Strategy] (no new users)                  │
│  ├─ [Archive] (old strategy)                         │
│  ├─ [Increase Revenue %] (to 0.75%)                  │
│  └─ [Withdraw Earnings] (to bank)                    │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## INTEGRATION FLOW: How trader uses strategy

```
STEP 1: FIND
├─ Browse marketplace
├─ Filter by symbol, win rate, users
└─ Find "Soporte Bounce EUR/USD" (45 users, 4.9⭐)

STEP 2: PREVIEW
├─ Click strategy
├─ See: rules, creator, reviews, performance
├─ See: "Creator gets 0.5% of your profits"
└─ Think: "If I make $1K, creator makes $5. Fair."

STEP 3: BACKTEST
├─ Click [Backtest on My Data]
├─ Choose: timeframe, period, custom tweaks
├─ System runs: simulates on last 30 days
├─ Results: 68% win rate, +$3,240
└─ Decision: "This works!"

STEP 4: ADD TO LIBRARY
├─ Click [Add to My Library]
├─ Stored in: user_strategy_library
├─ Can now:
│  ├─ View anytime
│  ├─ Tweak parameters
│  ├─ Re-backtest with new data
│  └─ Run backtest weekly to validate
└─ NOT running yet (simulation only)

FUTURE (OPENCLAW):
├─ Click [Activate Agent]
├─ System creates: agent config from strategy
├─ Deploys agent: to OpenClaw server
├─ Agent starts: monitoring EUR/USD 24/7
│
├─ When price triggers:
│  ├─ Agent executes trade
│  ├─ Tracks P&L
│  └─ Sends notification
│
├─ Revenue split:
│  ├─ You earn: 99%
│  ├─ Creator earns: 0.5%
│  ├─ Platform earns: 0.5%
│  └─ Example: $100 profit = You: $99, Creator: $0.50, Platform: $0.50
│
├─ Earnings track:
│  ├─ Stored: strategy_revenue table
│  ├─ Creator dashboard updates live
│  └─ Payout: Monthly to creator's bank
│
└─ Creator can:
   ├─ See who's using strategy
   ├─ See their P&L
   ├─ See total earnings
   ├─ Read reviews
   └─ Withdraw money
```

---

## REVENUE MODEL MECHANICS

### Example: Strategy earning money

```
User A discovers: "Soporte Bounce EUR/USD" (Creator: TradingMaster88)
User A subscribes: 0.5% revenue share

Month 1:
├─ User A trades with strategy
├─ Total P&L: +$10,000
├─ Creator share (0.5%): $50
├─ Platform share (0.5%): $50
├─ User A keeps: $9,900
└─ All tracked in strategy_revenue table

Creator Dashboard shows:
├─ "This month: +$50 from User A"
├─ "Total from all users: +$513"
├─ "Earnings paid: Yes (already in account)"

Platform Dashboard shows:
├─ "Marketplace total P&L: $102,645"
├─ "Platform earned: $513"
├─ "Creator earned: $513"
├─ Revenue split: 50/50 platform/creator
```

### Calculation Logic

```python
def calculate_revenue_split(trade_pnl: float, revenue_share_percent: float):
    """
    trade_pnl: User's profit/loss
    revenue_share_percent: 0.5 or 1.0 (e.g., 0.5%)
    """
    
    # Only split on profits (creator doesn't share losses)
    if trade_pnl <= 0:
        creator_earnings = 0
        platform_earnings = 0
    else:
        # Convert percent to decimal (0.5% = 0.005)
        revenue_share_decimal = revenue_share_percent / 100
        
        # Split revenue between creator and platform
        total_revenue = trade_pnl * revenue_share_decimal
        creator_earnings = total_revenue * 0.5  # 50% to creator
        platform_earnings = total_revenue * 0.5  # 50% to platform
    
    user_net = trade_pnl - (creator_earnings + platform_earnings)
    
    return {
        'user_keeps': user_net,
        'creator_earns': creator_earnings,
        'platform_earns': platform_earnings
    }

# Example
pnl = 1000
revenue_share = 0.5  # 0.5%

result = calculate_revenue_split(pnl, revenue_share)
# {
#   'user_keeps': 995,
#   'creator_earns': 2.50,
#   'platform_earns': 2.50
# }
```

---

## API ENDPOINTS

```
── MARKETPLACE BROWSE ──

GET /api/marketplace/strategies
├─ Query params:
│  ├─ symbol?: 'EUR_USD'
│  ├─ timeframe?: '1h'
│  ├─ min_win_rate?: 60
│  ├─ limit_users?: '10-50'
│  ├─ sort_by?: 'rating' | 'users' | 'recent'
│  └─ limit?: 20
└─ Response: [{strategy}, ...]

GET /api/marketplace/strategies/:id
├─ Input: strategy_id
└─ Response: full strategy detail + reviews + creator info

── SUBSCRIPTIONS ──

POST /api/marketplace/subscribe
├─ Input: {strategy_id, custom_risk?, custom_entry_offset?}
├─ Creates: strategy_subscriptions row
└─ Response: {subscription_id, status: 'saved'}

GET /api/marketplace/my-strategies
├─ User's subscribed strategies
└─ Response: user's library

DELETE /api/marketplace/unsubscribe/:subscription_id
├─ Remove strategy from library
└─ Status: deleted

── BACKTEST ──

POST /api/marketplace/backtest
├─ Input:
│  ├─ strategy_id
│  ├─ symbol
│  ├─ period: '30 days'
│  ├─ custom_params?: {entry_offset, tp_offset, ...}
│  └─ historical_data?: [...] (pre-loaded or fetch)
├─ Backend: runs backtest simulation
└─ Response: {win_rate, pnl, drawdown, trades_detail}

── CREATOR DASHBOARD ──

GET /api/creator/strategies
├─ All strategies I created
└─ Response: [{strategy_with_stats}, ...]

GET /api/creator/earnings/:strategy_id
├─ Monthly earnings from strategy
└─ Response: {this_month: 513, active_users: 45, top_performers: [...]}

POST /api/creator/withdraw
├─ Input: {strategy_id, amount}
├─ Initiates payout to bank
└─ Response: {withdrawal_id, status}

── REVIEWS ──

POST /api/marketplace/review
├─ Input: {strategy_id, rating: 1-5, comment: 'string'}
└─ Creates review + updates strategy.rating

GET /api/marketplace/reviews/:strategy_id
└─ All reviews for strategy
```

---

## SECURITY & COMPLIANCE

```
✅ DO:
├─ Require backtest before live execution
├─ Warn: "Past performance ≠ future"
├─ Audit: Track every trade + revenue calc
├─ Transparency: Show creator earnings public
├─ Fraud detection: Flag unusual performance jumps
└─ Escrow: Hold revenue, pay monthly (not real-time)

❌ DON'T:
├─ Guarantee returns
├─ Share user trade data without consent
├─ Allow high-risk strategies (>10% daily loss)
├─ Front-run trades (execute before creator notifies)
├─ Manipulate pricing/rankings
└─ Penalize users for losing trades
```

---

## SUMMARY: Marketplace = The Moat

```
VALUE FOR CREATORS:
├─ Validation: "45 traders believe in my strategy"
├─ Income: $500+/mo passive
├─ Reach: "My YouTube audience just became leads"
└─ Community: "Get feedback on my edge"

VALUE FOR USERS:
├─ Discovery: "Find winning strategies without work"
├─ Risk: "Backtest before using"
├─ Passive: "Strategy runs 24/7 (future)"
└─ Transparency: "See exact P&L + ratings"

VALUE FOR PLATFORM:
├─ Engagement: Users come back daily to check earnings
├─ Stickiness: Passive income keeps them invested
├─ Network effect: More strategies = more users
├─ Revenue: 0.5% of all trades
├─ Moat: Hard to replicate (require community)
└─ Growth: Viral (traders tell friends about earnings)

This is the product that scales.
```
