# V0 PROMPT: PEACH TRADING PLATFORM - COMPLETE SYSTEM
**Date**: 2026-03-20 | **Target**: V0 Code Generation | **Output**: Production-Ready Next.js + Supabase App

---

## 📋 EXECUTIVE SUMMARY

Build a **professional trading platform frontend** that connects to:
- **Alpaca Paper Trading API** (PA320EPZBPGV)
- **Supabase Backend** (Postgres database + auth)
- **YouTube Learning Engine** (sentiment analysis from video transcripts)
- **RSS Sentiment Feeds** (real-time market signals)
- **Twitter/X Sources** (11 validated trading accounts)

The app is a dashboard + management platform for autonomous trading with intelligent market monitoring. Users can:
1. **Configure their Alpaca API** from the UI (demo account setup)
2. **Launch batch deployments** (8 batches × 200-270 orders each = $40K target)
3. **Monitor live orders** (fill rates, stuck orders, equity changes)
4. **View market intelligence** (YouTube consensus, RSS sentiment, whale alerts)
5. **Manage leads/prospects** (CRM-style for trading signals)
6. **Adjust trading rules** (safeguards, position sizing, stop losses)

**Tech Stack**: Next.js 14, React 18, TypeScript, Tailwind CSS, Supabase (Postgres), Recharts, Shadcn/ui

---

## 🎯 CORE FEATURES (MUST HAVE)

### 1. **LEADS SCREEN** (CRM-Style Lead Management)
**Purpose**: Track trading signals, YouTube video opportunities, RSS alerts as "leads"

**Fields per Lead**:
- `id` (UUID)
- `source` (YouTube, RSS, Twitter, Whale Alert)
- `symbol` (ETHE, GBTC, BTC, ETH, etc.)
- `signal_type` (BULLISH, BEARISH, NEUTRAL)
- `confidence` (0-100%)
- `title` (e.g., "Glacier Trading - ETH Short Opportunity")
- `description` (summary from video transcript or feed)
- `link` (URL to video or article)
- `created_at` (timestamp)
- `status` (NEW, REVIEWED, ACTED_ON, DISMISSED)
- `tags` (array: "educational", "whale-buy", "resistance-level", etc.)
- `trading_entry` (linked batch/order if already traded)

**UI Components**:
- Lead card with preview image (YouTube thumbnail fallback)
- Swipe stack (Tinder-style quick dismiss/save)
- List view with filters (source, symbol, confidence, status)
- Detail modal with full description + link
- Bulk actions (mark as reviewed, add tag, delete)
- Sort options (newest, highest confidence, by source)

**Data Source**: Populated from:
- YouTube learning cycle (25 videos analyzed every 4 hours → top signals)
- RSS feeds (12 sources: CoinTelegraph, Cointimes, etc.)
- Whale Alert RSS (large transactions)
- Twitter sources (11 validated accounts)

**Example Lead**:
```json
{
  "id": "lead_123",
  "source": "YouTube",
  "symbol": "ETHE",
  "signal_type": "BEARISH",
  "confidence": 75,
  "title": "Glacier Trading: ETH Shorts at Resistance",
  "description": "Video analysis shows ETH at $2,133 resistance. Recommends short entries with -1% stop loss. RSI overbought signals exit at +3% take profit.",
  "link": "https://youtube.com/watch?v=...",
  "created_at": "2026-03-20T10:14:00Z",
  "status": "NEW",
  "tags": ["technical-analysis", "resistance-level", "short-opportunity"],
  "trading_entry": "batch_1"
}
```

---

### 2. **TRADING SCREEN** (Live Order Dashboard)
**Purpose**: Monitor active batch deployments, order fills, equity changes, safeguards

**Main Panels**:

#### A. **Account Status Card** (Top)
```
Equity: $100,562 → $130,000 (target)
Buying Power: $142,066
Daily Gain: +$2,500 (+2.5%)
Open Positions: ETHE (1,838 @ $3,445) | GBTC (150 @ $73.25)
Status: 🟢 ACTIVE | Fill Rate: 65% ↑
```

#### B. **Batch Deployment Timeline** (Center)
- Visual timeline: Batch 1 → 8 (each batch is 15 min apart)
- Status for each: ✓ (completed), ⏳ (in progress), ⚪ (pending)
- Details on hover: orders count, actual gain, fill rate %, equity after

**Example Timeline**:
```
11:40 UTC  11:55 UTC  12:10 UTC  12:25 UTC  ...
[✓ B1]  →  [✓ B2]  →  [⏳ B3]  →  [⚪ B4]  →  ...
200 orders 210 orders 220 orders 230 orders
$2.1K gain $2.3K gain ~$2.5K est ~pending
```

#### C. **Orders Table** (Bottom)
**Real-time streaming table** showing:
- `order_id` | `symbol` | `qty` | `side` (buy/sell) | `status` (filled/pending/partial)
- `filled_qty` | `entry_price` | `current_price` | `pnl` | `filled_at`
- Color coding: ✅ green (filled), ⏳ gray (pending), 🔴 red (error/stuck)

**Actions per order**:
- View details
- Cancel (if pending)
- Add to watchlist

#### D. **Safeguards Panel** (Right Side)
**Emergency stops active**:
- Daily loss limit: -1% (alarm if approaching)
- Position loss exit: -0.5% per trade
- Min buying power: $15K (currently $142K ✅)
- Stuck order timeout: 10 minutes
- Fill rate threshold: >70% (currently 65%, caution)
- Max pending orders: 30 (currently 2)

**Status for each**: 🟢 OK | 🟡 WARNING | 🔴 CRITICAL

#### E. **Performance Chart** (Left)
- Line chart: Equity over time (real-time updates)
- X-axis: Time (11:40 UTC → 13:55 UTC)
- Y-axis: Equity ($100K → $130K+)
- Overlay: batch deployment markers

**Example Chart**:
```
$130K │         ╱╲      ╱╲
       │        ╱  ╲    ╱  ╲
$120K │       ╱    ╲  ╱    ╲
       │      ╱      ╲╱
$110K │     ╱
       │    ╱
$100K │___╱
       └─────────────────────
       11:40  12:00  12:30  13:00
```

**Update Frequency**: Every 10 seconds (live streaming from Alpaca API)

---

### 3. **SETTINGS SCREEN** (Configuration + Rules)
**Purpose**: Let users configure Alpaca API, trading parameters, and safeguards

#### A. **Alpaca API Setup**
```
[ Account Setup ]

Alpaca Base URL: https://paper-api.alpaca.markets/v2
API Key: [input - masked by default]
API Secret: [input - masked]
Account Type: ○ Paper (selected)  ○ Live
           
Connection Status: 🟢 Connected | Account: PA320EPZBPGV

[Test Connection Button]
[Save Button]
```

#### B. **Trading Rules Configuration**
```
Daily Loss Halt:     |-1%|   (if equity drops 1%, stop all trading)
Position Stop Loss:  |-0.5%| (exit individual trades at -0.5% loss)
Min Buying Power:    |$15K|  (pause if BP < $15K)
Stuck Order Timeout: |600s|  (cancel pending orders after 10 min)
Target Fill Rate:    |80%|   (caution alert if <70%)
Batch Interval:      |15min| (15 minutes between batches)
```

Each rule shows:
- Current value (editable input)
- Description (tooltip)
- Last updated timestamp
- Reset to default button

#### C. **Strategy Selection**
```
Market Strategy
◉ SHORT_AGGRESSIVE (75% shorts, 25% DCA buys)
  └─ Best for: Bearish sentiment (YouTube 75% bearish)
  └─ Escalation: +5% per batch
  └─ Expected return: +$25-30K

○ DCA_HEAVY (30% shorts, 70% buys)
  └─ Best for: Neutral/bullish market
  └─ Escalation: +3% per batch
  
○ CUSTOM
  └─ Define your own rules
```

Active strategy shows: SHORT_AGGRESSIVE ✅

#### D. **Market Intelligence Settings**
```
YouTube Learning Cycle
- Enabled: ✓
- Frequency: Every 4 hours
- Videos to analyze: 25
- Next cycle: 14:35 UTC
- Last cycle result: 75% BEARISH (15/25 videos)

RSS Sentiment Feeds
- Enabled: ✓
- Frequency: Every 1 hour
- Feed count: 12 sources
- Last update: 12:10 UTC
- Current consensus: 58% BEARISH (7 bullish, 4 bearish, 1 neutral)

Twitter Sources
- Enabled: ✓
- Validated sources: 11
- Tier breakdown: 2 PLATINUM, 3 GOLD, 4 SILVER, 2 BRONZE
- Last alert: 12:15 UTC (Whale bought 500 ETHE)
```

#### E. **Data Connections** (User fills these in)
```
Supabase Connection
- Project URL: [input: your_project.supabase.co]
- Public Key: [input: public_anon_key]
- Service Role Key: [input: service_role_key]

YouTube API
- API Key: [input: your_youtube_api_key]
- Search terms: [comma-separated] (ETH price analysis, Bitcoin trading, ...)

RSS Feeds
- Custom feeds: [Add more feeds button]
- Example: https://feeds.coindesk.com/news

Twitter/X
- API Key: [input - if using Twitter API]
- Validated sources list: [read-only, shows 11 pre-validated]
```

[Save All Settings] [Test Connections] [Reset Defaults]

---

### 4. **UI LAYOUT & NAVIGATION**

**Main App Layout**:
```
┌─────────────────────────────────────────────────────┐
│ 🍑 PEACH AGENTS TRADING PLATFORM                    │
├─────────────────────────────────────────────────────┤
│ [Dashboard] [Leads] [Trading] [Settings] [Docs]    │
├─────────────────────────────────────────────────────┤
│                                                     │
│                   MAIN CONTENT AREA                 │
│                                                     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Tab Bar at Bottom** (mobile-friendly):
- 🏠 Dashboard (quick summary)
- 📊 Leads (signal management)
- 📈 Trading (live orders + performance)
- ⚙️ Settings (configuration)
- 📚 Docs (help + API reference)

**Color Scheme**:
- Background: Dark (#0f0f0f, #1a1a1a)
- Text: White (#ffffff)
- Accent: Peach/Orange (#ff9f43)
- Success: Green (#10b981)
- Warning: Yellow (#fbbf24)
- Error: Red (#ef4444)

---

## 🔌 API INTEGRATIONS

### 1. **Alpaca Paper Trading API**
**Endpoint**: `https://paper-api.alpaca.markets/v2`

**Key Endpoints Used**:
```
GET /account
  → Returns: equity, buying_power, cash, positions

GET /orders
  → Returns: all orders with status

POST /orders
  → Create new order (market/limit, buy/sell)

GET /positions
  → Current holdings

PATCH /orders/{order_id}
  → Cancel stuck order
```

**Auth**: Header `APCA-API-KEY-ID` + `APCA-API-SECRET-KEY`

**Real-time Updates**: Poll every 10 seconds OR use Alpaca WebSocket (if available)

---

### 2. **Supabase Database**
**Connection**: `@supabase/supabase-js` (already in package.json)

**Key Tables**:
```sql
trading_accounts (account info, equity tracking)
orders_executed (order history)
batch_deployments (batch status, gains)
youtube_learning_cycles (video analysis results)
rss_sentiment_snapshots (feed sentiment)
twitter_sources (validated traders, trust scores)
whale_transactions (on-chain activity)
market_conditions (VIX, crash probability)
system_health_checks (safeguard status)
trading_rules (current parameter values)
mission_targets (goals: +$40K today)
session_logs (session documentation)
```

**Example Query** (Get latest equity):
```typescript
const { data, error } = await supabase
  .from('trading_accounts')
  .select('current_equity, buying_power, status')
  .eq('account_id', 'PA320EPZBPGV')
  .single();
```

---

### 3. **YouTube Learning Engine**
**Data Source**: Stored in `youtube_learning_cycles` table

**Fields Available**:
- cycle_num (1, 2, 3, ...)
- search_date (when analyzed)
- videos_analyzed (25)
- bullish_signals (8)
- bearish_signals (15)
- consensus (BEARISH)
- confidence_percent (75%)
- top_insights (JSON array of key learnings)
- recommended_strategy (SHORT_AGGRESSIVE)

**UI Display**: Show latest cycle in "Market Intelligence" card on dashboard

---

### 4. **RSS Sentiment Feeds**
**Data Source**: Stored in `rss_sentiment_snapshots` table

**Update Frequency**: Every 1 hour

**Display**:
- Pie chart: Bullish % | Bearish % | Neutral %
- Recent feeds list (title, source, date)
- Overall trend arrow (↑ bullish / ↓ bearish / → neutral)

---

### 5. **Twitter Sources**
**Data Source**: Stored in `twitter_sources` table

**Pre-Validated Sources** (11 total):
```
PLATINUM (Trust Score 90-100):
- 1. Glacier Trading (@GlacierTrading)
- 2. CryptoQuant (@cryptoquant)

GOLD (Trust Score 75-89):
- 3. Glassnode (@glassnode)
- 4. The Block (@theblockdata)
- 5. CoinBureau (@coinbureau)

SILVER (Trust Score 60-74):
- 6. TradingView (@TradingView)
- 7. Messari (@MessariCrypto)
- 8. Coingecko (@coingecko)
- 9. Santiment (@Santiment)

BRONZE (Trust Score <60):
- 10. CoinMarketCap (@CoinMarketCap)
- 11. CoinJournal (@CoinJournal)
```

**UI Display**: Tier badges, trust scores, recent calls link

---

## 🗄️ SUPABASE SCHEMA (Already Prepared)

Use this exact schema (copy/paste into Supabase SQL Editor):

```sql
-- See: SUPABASE_SCHEMA_2026_03_20_UPDATED.sql
-- 14 tables, 3 views, row-level security
-- All documented with comments
```

**Pre-populated Rules**:
```sql
INSERT INTO trading_rules (rule_name, parameter_value, description) VALUES
  ('daily_loss_halt', -1, 'Stop all trading if daily equity drops 1%'),
  ('position_loss_exit', -0.5, 'Exit trade if position drops 0.5%'),
  ('min_buying_power', 15000, 'Pause trading if BP < $15K'),
  ('stuck_order_timeout', 600, '10-minute timeout for pending orders'),
  ('target_fill_rate', 80, 'Target fill rate for batches (%)'),
  ('batch_interval_minutes', 15, 'Interval between batch deployments'),
  ('short_mode_confidence', 75, 'Minimum confidence for SHORT strategy'),
  ('market_vol_threshold', 20, 'VIX level triggering volatile mode');
```

---

## 📦 REQUIRED COMPONENTS (From Shadcn/ui)

Install these components into the app:
```bash
npx shadcn-ui@latest add card
npx shadcn-ui@latest add button
npx shadcn-ui@latest add input
npx shadcn-ui@latest add tabs
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add badge
npx shadcn-ui@latest add alert
npx shadcn-ui@latest add progress
npx shadcn-ui@latest add table
npx shadcn-ui@latest add chart (for Recharts)
```

**Custom Components Needed**:
- `components/leads-list.tsx` (Leads screen)
- `components/lead-card.tsx` (Individual lead card with swipe)
- `components/trading-dashboard.tsx` (Trading screen)
- `components/settings-panel.tsx` (Settings screen)
- `components/order-table.tsx` (Live orders table)
- `components/equity-chart.tsx` (Recharts line chart)
- `components/safeguards-panel.tsx` (Safeguard status cards)
- `components/batch-timeline.tsx` (Batch deployment timeline)
- `components/market-intel.tsx` (YouTube + RSS display)

---

## 🚀 KEY FEATURES TO BUILD

### Real-Time Updates
- Alpaca orders: Poll API every 10 seconds, update UI
- Equity: Live update as orders fill
- Safeguard alerts: Highlight if any threshold breached
- Batch status: Show progress as orders deploy

### Lead Management
- Filter leads by source, symbol, confidence
- Swipe dismiss/save leads
- Bulk tag operations
- Link leads to executed trades (traceability)

### Batch Deployment Controls
- Start/pause current batch
- Manual override safeguards (with confirmation)
- View pending vs filled orders per batch
- Download batch report (CSV)

### Settings Persistence
- Save all settings to Supabase `trading_rules` table
- Load settings on app boot
- Validate inputs (no negative batch intervals, etc.)
- Show "unsaved changes" warning if navigating away

---

## 📝 PAGE ROUTES (Next.js App Router)

```
app/
├── page.tsx                  (Dashboard home)
├── leads/
│   └── page.tsx              (Leads screen)
├── trading/
│   └── page.tsx              (Trading dashboard)
├── settings/
│   └── page.tsx              (Settings screen)
├── api/
│   ├── alpaca/account/route.ts
│   ├── alpaca/orders/route.ts
│   ├── supabase/leads/route.ts
│   ├── supabase/batches/route.ts
│   └── rules/route.ts
└── layout.tsx                (Root layout)
```

---

## 🔐 ENVIRONMENT VARIABLES

User must provide these (they'll fill manually):
```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_public_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

NEXT_PUBLIC_ALPACA_BASE_URL=https://paper-api.alpaca.markets/v2
ALPACA_API_KEY=user_provides_this
ALPACA_API_SECRET=user_provides_this

YOUTUBE_API_KEY=user_provides_this
```

---

## 📊 DISPLAY DATA EXAMPLES

### Dashboard Summary Card
```
🍑 PEACH AGENTS - SESSION 2026-03-20

Mission: +$40K Today (2 hours runtime)
Status: ✅ IN PROGRESS

Current Equity:    $100,562 ↗ (target $130K)
Buying Power:      $142,066 ✅ Protected
Daily Gain:        +$2,500 (+2.49%)
Batch Progress:    Batch 3/8 ⏳ (in progress)
Fill Rate:         65% (⚠️ below 70% target)

Market Consensus:  🔴 BEARISH (YouTube 75%, RSS 58%)
Strategy Active:   SHORT_AGGRESSIVE (66% shorts, 34% DCA)

Safeguard Status:  ✅ All 7 active
Next Update:       12:25 UTC
```

### Leads Card Example
```
┌─────────────────────────────┐
│ 🎥 Glacier Trading          │
│ ETHE Short Opportunity      │
│                             │
│ Confidence: 78% 🔴 BEARISH  │
│ Source: YouTube             │
│ Created: 12:10 UTC          │
│                             │
│ "ETH at resistance $2,133.  │
│  RSI overbought. Recommend  │
│  short with -1% stop loss,  │
│  +3% take profit."          │
│                             │
│ [← Dismiss] [Save →]        │
└─────────────────────────────┘
```

---

## ✅ DEPLOYMENT CHECKLIST

1. **Supabase Setup**
   - Create Supabase project
   - Run schema SQL (provided)
   - Get API keys & URLs

2. **GitHub Repo**
   - V0 output → GitHub repo
   - .env.example in repo root

3. **Vercel Deployment**
   - Connect GitHub repo
   - Add env variables
   - Deploy (should auto-build)

4. **User Configuration**
   - User fills in Alpaca API + Supabase keys via Settings screen
   - User tests connection
   - System ready for trading

---

## 🎨 DESIGN REQUIREMENTS

- **Mobile-first** layout (works on phone + tablet + desktop)
- **Dark theme** (matches existing peach-agents branding)
- **Real-time charts** using Recharts
- **Accessibility**: ARIA labels, keyboard navigation
- **Performance**: Lazy-load components, memoize expensive renders
- **Responsive tables**: Horizontal scroll on mobile

---

## 📌 IMPORTANT NOTES FOR V0

1. **This is a FRONTEND for existing backend services**. The app connects to:
   - Alpaca (existing paper trading account)
   - Supabase (database you'll set up)
   - YouTube/RSS feeds (pre-analyzed, stored in DB)

2. **User provides their own API keys** via Settings. App doesn't generate them.

3. **Real-time updates**: Use `setInterval` or Supabase real-time subscriptions to update charts/tables.

4. **Error handling**: Show friendly error messages (e.g., "Connection failed, retrying..." with retry button).

5. **Deployment-ready**: Output should be production-ready Next.js code that can be pushed to GitHub → Vercel immediately.

---

## 🔗 CONNECTIONS USER WILL FILL

**In Settings Screen**:
```
Alpaca Connection:
- Base URL: https://paper-api.alpaca.markets/v2 ← Already filled
- API Key: [USER FILLS]
- API Secret: [USER FILLS]

Supabase Connection:
- Project URL: [USER FILLS]
- Anon Key: [USER FILLS]
- Service Key: [USER FILLS]

YouTube API:
- API Key: [USER FILLS]

Twitter/X:
- Sources: [READ-ONLY, pre-populated with 11 sources]
```

---

**END OF PROMPT**

**Output Format**: Next.js 14 app with all features above, production-ready, deployable to Vercel.
**Testing**: User tests via Settings → [Test Connection] buttons before launching trading.
**Support**: Built-in documentation tabs with API reference + user guide.
