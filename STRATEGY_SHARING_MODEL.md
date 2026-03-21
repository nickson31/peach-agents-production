# STRATEGY SHARING MODEL — Within Trust Circles

## EL PROBLEMA

```
User A: Corre olimpiada, descubre Trader X #1
User B (amigo de User A): "Wow, ¿puedo usar ESA estrategia?"
System hoy: NO HAY FORMA

Solution: Strategy sharing + future agent templates
```

---

## LA SOLUCIÓN: 3 CAPAS

### CAPA 1: RESULTS SHARING (Visibilidad)

```
User A corre olimpiada de 20 traders.
Sistema genera: results link + sharing options

OPCIONES DE VISIBILIDAD:

├─ PRIVATE (default)
│  └─ Solo User A ve resultados
│     Shareable: Private link (anyone with URL)
│
├─ FRIENDS-ONLY
│  ├─ User A selecciona: "Compartir con estos amigos"
│  ├─ Friends verán: Resultados + estrategias top
│  └─ Friends pueden: Exportar/usar estrategias
│
├─ COMMUNITY
│  ├─ Linked a: Telegram group / Discord / Slack
│  ├─ All members verán: Resultados + rankings
│  └─ Members pueden: Source estrategias
│
└─ PUBLIC (opt-in, future)
   ├─ Show on leaderboard
   └─ (careful: regulatory + competition)
```

---

### CAPA 2: STRATEGY EXTRACTION & LIBRARY

#### What gets extracted from olimpiada:

```
User A's olimpiada results:
{
  olimpiada_id: "olimp_123",
  title: "EUR/USD - 20 YouTube Traders",
  date: "2026-03-19",
  results: [
    {
      rank: 1,
      trader_name: "TradingMaster88",
      symbol: "EUR_USD",
      entry: 1.0875,
      tp: 1.0750,
      sl: 1.0950,
      timeframe: "1h",
      strategy_rules: {
        trigger: "Soporte + bounce",
        risk_percent: 1.5,
        max_positions: 1
      },
      backtest_results: {
        win_rate: 0.68,
        total_pnl: 4250,
        num_trades: 42,
        max_drawdown: 0.05
      }
    },
    { rank: 2, ... },
    ...
  ]
}

USER A EXPORTS:
└─ "Strategy #1" as JSON (shareable)
   {
     strategy_id: "strat_abc123",
     source_trader: "TradingMaster88",
     source_olimpiada: "olimp_123",
     strategy: {
       symbol: "EUR_USD",
       entry: 1.0875,
       tp: 1.0750,
       sl: 1.0950,
       timeframe: "1h",
       rules: "soporte + bounce",
       risk: 1.5
     },
     backtest_validation: { win_rate: 0.68, pnl: 4250 },
     exportable: true
   }
```

---

### CAPA 3: STRATEGY LIBRARY (Discovery & Reuse)

#### User A's perspective (after olimpiada):

```
RESULTS PAGE:

┌─────────────────────────────────────────┐
│ Olimpiada: EUR/USD - 20 YouTube Traders │
├─────────────────────────────────────────┤
│                                         │
│ 🥇 #1: TradingMaster88                  │
│    Entry: 1.0875 | TP: 1.0750           │
│    Win Rate: 68% | P&L: +$4,250         │
│    [Export] [Copy] [Share]              │
│                                         │
│ 🥈 #2: ForexGuru                        │
│    Entry: 1.0850 | TP: 1.0700           │
│    Win Rate: 65% | P&L: +$3,800         │
│    [Export] [Copy] [Share]              │
│                                         │
│ 🥉 #3: CryptoWhiz                       │
│    ...                                  │
│                                         │
└─────────────────────────────────────────┘

USER A CLICKS: [Share]
├─ Option 1: "Copy link (anyone with URL can see)"
├─ Option 2: "Send to friends" → Select from contacts
├─ Option 3: "Post to community" → Telegram/Discord
└─ Option 4: "Save to my library"
```

#### User B's perspective (friend of User A):

```
USER B RECEIVES:
├─ Link from User A: "Check out my olimpiada results"
├─ OR: Message in shared Telegram: "Best EUR/USD strategies found"

USER B CLICKS LINK:
├─ Sees: "User A's olimpiada results"
├─ Sees: Rankings + strategies
├─ Sees: #1 strategy details
│  ├─ Trader: TradingMaster88
│  ├─ Win rate: 68%
│  ├─ P&L: +$4,250
│  └─ Rules: soporte + bounce
│
└─ BUTTON: "Use this strategy" or "Add to my library"

USER B CLICKS: "Use this strategy"
├─ Action 1 (TODAY): "Backtest this on my own data"
│  ├─ System lets him pick: timeframe, symbol, period
│  ├─ Runs backtest WITH this strategy
│  ├─ Results: "On your data: 65% win rate, +$3,200"
│  └─ Decision: "Looks good, I'll use it"
│
└─ Action 2 (FUTURE - with OpenClaw):
   ├─ "I want to execute this 24/7"
   ├─ System: Creates agent config from strategy
   ├─ User connects account → agent runs automatically
   ├─ Agent monitors, trades, reports P&L
   └─ If User A monetized it: Both earn share

USER B SAVES:
├─ Strategy added to his "Strategies Library"
├─ Can view, backtest, tweak, share
└─ When OpenClaw ready: "One click to activate"
```

---

## DATABASE SCHEMA V0 (Add to existing)

```sql
-- NEW TABLES

-- Strategy extraction from olimpiadas
CREATE TABLE strategy_exports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  olimpiada_id UUID REFERENCES olimpiada_configs(id),
  
  -- Strategy metadata
  strategy_name VARCHAR(255),
  source_trader_name VARCHAR(255),  -- "TradingMaster88"
  
  -- Strategy definition
  symbol VARCHAR(50),
  timeframe VARCHAR(10),
  entry_price DECIMAL(10,5),
  tp_price DECIMAL(10,5),
  sl_price DECIMAL(10,5),
  strategy_rules JSONB,  -- {trigger: 'soporte', risk: 1.5}
  
  -- Validation
  backtest_win_rate DECIMAL(5,2),
  backtest_pnl DECIMAL(15,2),
  backtest_num_trades INT,
  
  -- Visibility & sharing
  visibility VARCHAR(50) DEFAULT 'private',  -- 'private', 'friends', 'community', 'public'
  shared_with_user_ids UUID[],  -- Who User A shared with
  shared_in_community_ids UUID[],  -- Telegram group IDs, etc
  
  -- Monetization (future)
  is_monetizable BOOLEAN DEFAULT false,
  creator_id UUID REFERENCES users(id),
  
  created_at TIMESTAMP DEFAULT NOW(),
  INDEX idx_olimpiada_id (olimpiada_id),
  INDEX idx_visibility (visibility),
  INDEX idx_creator_id (creator_id)
);

-- Users' personal strategy libraries
CREATE TABLE user_strategy_library (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  strategy_export_id UUID REFERENCES strategy_exports(id) ON DELETE SET NULL,
  
  -- Custom tweaks (if user modified the strategy)
  custom_entry DECIMAL(10,5),
  custom_tp DECIMAL(10,5),
  custom_sl DECIMAL(10,5),
  custom_risk_percent DECIMAL(3,1),
  
  -- Status
  status VARCHAR(50) DEFAULT 'saved',  -- 'saved', 'backtested', 'active' (future)
  
  -- Future: Agent config
  agent_enabled BOOLEAN DEFAULT false,  -- When OpenClaw ready
  agent_config_id VARCHAR(255),
  
  created_at TIMESTAMP DEFAULT NOW(),
  INDEX idx_user_id (user_id),
  INDEX idx_status (status)
);

-- Shared olimpiada results
CREATE TABLE olimpiada_shares (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  olimpiada_id UUID REFERENCES olimpiada_configs(id),
  shared_by_user_id UUID REFERENCES users(id),
  
  -- Share method
  share_type VARCHAR(50),  -- 'link', 'direct', 'community'
  shared_with_user_ids UUID[],  -- if direct share
  community_id VARCHAR(255),  -- if community share (Telegram group ID, etc)
  
  -- Privacy
  share_link VARCHAR(255) UNIQUE,  -- Public link if shared
  link_expires_at TIMESTAMP,  -- or null = permanent
  
  created_at TIMESTAMP DEFAULT NOW(),
  INDEX idx_olimpiada_id (olimpiada_id),
  INDEX idx_shared_by_user_id (shared_by_user_id)
);

-- Community groups (users in same trader community)
CREATE TABLE community_groups (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Group identity
  group_name VARCHAR(255),
  external_id VARCHAR(255),  -- Telegram group ID, Discord server ID, etc
  external_type VARCHAR(50),  -- 'telegram', 'discord', 'slack'
  
  -- Settings
  is_private BOOLEAN DEFAULT true,
  description TEXT,
  
  created_at TIMESTAMP DEFAULT NOW(),
  INDEX idx_external_id (external_id)
);

-- Users in communities
CREATE TABLE community_members (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  community_id UUID NOT NULL REFERENCES community_groups(id) ON DELETE CASCADE,
  
  role VARCHAR(50) DEFAULT 'member',  -- 'admin', 'member'
  joined_at TIMESTAMP DEFAULT NOW(),
  
  UNIQUE KEY unique_user_community (user_id, community_id),
  INDEX idx_user_id (user_id),
  INDEX idx_community_id (community_id)
);

-- Strategy usage tracking (when User B uses User A's strategy)
CREATE TABLE strategy_usage (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  strategy_export_id UUID REFERENCES strategy_exports(id),
  used_by_user_id UUID REFERENCES users(id),
  
  -- Usage context
  usage_type VARCHAR(50),  -- 'backtest', 'demo_trade', 'live_trade' (future)
  
  -- Results (if they backtest/execute)
  backtest_results JSONB,  -- {win_rate, pnl, num_trades}
  
  -- Future: Revenue share (if User A monetized)
  revenue_share_percent INT,  -- 0-70
  earnings_generated DECIMAL(15,2),
  
  used_at TIMESTAMP DEFAULT NOW(),
  INDEX idx_strategy_export_id (strategy_export_id),
  INDEX idx_used_by_user_id (used_by_user_id)
);
```

---

## API ENDPOINTS (Add to existing)

```
── STRATEGY SHARING ──

POST /api/strategy/export
├─ Input: {olimpiada_id, strategy_rank}
├─ Output: {strategy_export_id, json}
├─ Action: Extract strategy from olimpiada results

POST /api/strategy/share
├─ Input: {strategy_export_id, visibility, shared_with_user_ids, community_ids}
├─ Output: {share_link, settings}
├─ Action: Update visibility + generate shareable link

GET /api/strategy/share/:share_link
├─ Public endpoint (no auth needed)
├─ Output: {olimpiada_results, top_strategies}
├─ Anyone with link can see

POST /api/strategy/add-to-library
├─ Input: {strategy_export_id}
├─ Output: {library_id, can_backtest}
├─ Action: Add to User B's library

POST /api/strategy/backtest-library
├─ Input: {strategy_export_id, symbol, timeframe, data_period}
├─ Output: {results, win_rate, pnl}
├─ Action: Backtest User A's strategy on User B's data

── COMMUNITY ──

POST /api/community/link
├─ Input: {external_id, external_type} (Telegram group ID, etc)
├─ Output: {community_id}
├─ Action: Link Telegram/Discord to Racha

POST /api/community/sync
├─ Syncs olimpiadas + results to linked community
├─ Posts: "New olimpiada results in app!"
└─ With share link

── FUTURE (OPENCLAW) ──

POST /api/agent/from-strategy
├─ Input: {strategy_export_id}
├─ Output: {agent_config_id}
├─ Action: Create agent template from strategy JSON

POST /api/agent/activate
├─ Input: {agent_config_id, user_account_id}
├─ Output: {agent_running}
├─ Action: Start agent executing strategy on account
```

---

## USER FLOW EXAMPLE (End-to-End)

```
STEP 1: User A Runs Olimpiada
├─ Query: "EUR/USD strategies from YouTube, 20 traders"
├─ System: YouTube search → parse transcripts → backtest
├─ Results: 20 traders ranked by P&L
└─ Top: TradingMaster88 (68% win rate, +$4,250)

STEP 2: User A Shares Results
├─ Clicks: [Share Results]
├─ Options:
│  ├─ Send link to User B (his friend)
│  ├─ Post to Telegram group "Traders Union"
│  └─ Or both
└─ Database update: olimpiada_shares, visibility='friends'

STEP 3: User B Sees Link
├─ Telegram message: "Check out strategies I found for EUR/USD"
├─ User B clicks link
├─ App loads: Share page with results
├─ Sees: TradingMaster88 is #1
└─ Button: "Use this strategy"

STEP 4: User B Previews
├─ Clicks: "Use this strategy"
├─ System shows:
│  ├─ Strategy rules (entry, tp, sl, risk)
│  ├─ Original backtest (68% win rate)
│  └─ Option: "Backtest on MY data"
│
└─ User B: "Let me see how it would've done on last 30 days"

STEP 5: User B Backtests Strategy
├─ Clicks: "Backtest with my data"
├─ System:
│  ├─ Gets his historical EUR/USD data (30 days)
│  ├─ Simulates: TradingMaster88's strategy
│  ├─ Returns: Results (65% win rate, +$3,200)
│  └─ Button: "Save to my library"
│
└─ User B: "Great! I'll use this."

STEP 6: User B Adds to Library
├─ Clicks: "Save to my library"
├─ Stored in: user_strategy_library
├─ Can now:
│  ├─ Run whenever he wants
│  ├─ Tweak parameters
│  ├─ Compare with other strategies
│  └─ (FUTURE) Activate agent to run 24/7
│
└─ Logged: strategy_usage (type='backtest')

FUTURE (OPENCLAW READY):
├─ User B: "I want this strategy running on my account"
├─ Clicks: [Activate Agent]
├─ System:
│  ├─ Creates agent config from strategy JSON
│  ├─ Deploys agent to OpenClaw server
│  ├─ Connects User B's account
│  ├─ Agent monitors EUR/USD 24/7
│  └─ Executes + reports P&L
│
├─ If User A monetized:
│  ├─ User A gets: 70% of profits
│  ├─ Platform gets: 30%
│  └─ Logged: strategy_usage(type='live_trade', earnings_generated)
│
└─ User A PASSIVE INCOME: +$300/month from User B alone
   (User A could have 50 traders = $15K/mo passive)
```

---

## COMMUNITY INTEGRATION (Telegram Example)

```
POST to Telegram:

"🏆 EUR/USD Trading Olympiad Results (Racha)

#1: TradingMaster88
├─ Win Rate: 68%
├─ P&L: +$4,250
└─ [View Strategy] [Try Backtest] [Link]

#2: ForexGuru
├─ Win Rate: 65%
├─ P&L: +$3,800
└─ [View] [Try] [Link]

#3: CryptoWhiz
└─ ...

👉 [Full Results + All Strategies]
👉 [Add my own strategy]
👉 [Join Racha]"

WHEN USER CLICKS [Full Results]:
└─ Share link → Opens in app
   └─ User sees all 20 strategies
   └─ Can add to library
   └─ Friends see his activity
```

---

## MONETIZATION PATH (Future with OpenClaw)

```
STRATEGY CREATOR (e.g., TradingMaster88):

Option 1: Give away
├─ Someone discovers his strategy
├─ Likes it
└─ → Leads to users finding his YouTube channel
   → Commission/sponsorships

Option 2: Revenue share (future, with OpenClaw)
├─ System: "Would you like to monetize this?"
├─ User B uses strategy: 50 traders use it
├─ Each trader earns $300/mo with strategy
├─ TradingMaster88 gets: 70% × (50 × $300) = $10,500/mo
├─ Platform gets: 30%
└─ → Win-win: creator makes money, users make money, we make money

Option 3: Premium strategy (future)
├─ System: "Make strategy private, list on marketplace"
├─ Users pay: $50-500/mo for access
├─ Creator gets: 80%
└─ Platform gets: 20%
```

---

## PRIVACY & SAFETY

```
✅ DO:
├─ Let users control visibility (private by default)
├─ Let users share with friends/communities
├─ Encrypt sensitive strategy parameters
├─ Track usage for future revenue share
└─ Disclaimer: "Past results ≠ future performance"

❌ DON'T:
├─ Show strategies withoutpermission
├─ Sell strategies to third parties
├─ Clone or modify without consent
├─ Promise guaranteed returns
└─ Allow impersonation ("I created this")
```

---

## SUMMARY

**3-layer sharing model:**

1. **Results Visibility** — Private link → Share with friends → Post to community
2. **Strategy Extraction** — Export strategy JSON → Add to library → Backtest
3. **Agent Integration** (Future) — Strategy → Agent config → Automated execution

**Key insight:** Strategies are the NEW PRODUCT.

Strategy creator (Trader A) gains:
├─ Validation ("my strategy actually works")
├─ Reach ("others want to use it")
├─ Income (70% revenue share)
└─ Community ("become known as top trader")

Strategy user (Trader B) gains:
├─ Discovery ("found winning strategy without work")
├─ Validation ("backtested on my data")
├─ Automation ("agent runs it 24/7")
└─ Passive income ("profits from others' work")

Platform gains:
├─ 30% revenue share
├─ Stickiness (community effects)
├─ Network effects (more strategies = more users)
└─ Moat (hard to replicate strategy network)

**This is the viral loop that scales without marketing.**
