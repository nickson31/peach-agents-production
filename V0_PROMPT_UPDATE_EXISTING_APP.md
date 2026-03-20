# V0 UPDATE PROMPT: Enhance Existing Peach Trading App
**Context**: You already generated the base app. This prompt updates 3 key screens with new features + integrations.

---

## 📝 WHAT WE HAVE

Your existing Peach app has:
- Dashboard + tabs layout ✅
- Basic structure ✅
- UI components ✅

## 🔄 WHAT WE'RE UPDATING

### 1. **UPDATE LEADS SCREEN** (components/leads-list.tsx + lead-card.tsx)

**Current**: Basic list view

**New Features**:
- Add **swipe stack UI** (Tinder-style: left dismiss, right save)
- Add **filters**: Source (YouTube/RSS/Twitter/Whale), Symbol (ETHE/GBTC/BTC), Confidence (>50%, >75%, >90%)
- Add **signal_type badge**: 🔴 BEARISH | 🟢 BULLISH | ⚪ NEUTRAL
- Add **data from Supabase**: Query from `youtube_learning_cycles` + `rss_sentiment_snapshots` + `twitter_sources`
- Add **status tracking**: NEW | REVIEWED | ACTED_ON | DISMISSED
- Add **detail modal**: Click lead → show full description + link to video/article

**Data Example**:
```json
{
  "id": "lead_1",
  "source": "YouTube",
  "symbol": "ETHE",
  "signal_type": "BEARISH",
  "confidence": 75,
  "title": "Glacier Trading: ETH Short at Resistance",
  "description": "Video shows ETH at $2,133 resistance...",
  "link": "https://youtube.com/watch?v=...",
  "created_at": "2026-03-20T10:14:00Z",
  "status": "NEW"
}
```

**UI**: Card with image (YouTube thumbnail), title, confidence %, signal type, [Dismiss] [Save] buttons

---

### 2. **UPDATE TRADING SCREEN** (components/trading-dashboard.tsx)

**Current**: Basic layout

**New Real-Time Features**:

#### A. **Account Status Card** (top):
```
┌─────────────────────────────────────────┐
│ Equity: $100,562 → $130,000 (target)   │
│ Buying Power: $142,066 ✅ Protected    │
│ Daily Gain: +$2,500 (+2.5%)            │
│ Batch Status: 3/8 ⏳ In Progress       │
│ Fill Rate: 65% ⚠️ Below 70% target    │
│ Positions: ETHE 1,838 | GBTC 150       │
└─────────────────────────────────────────┘
```

#### B. **Batch Timeline** (middle):
```
11:40 UTC  11:55 UTC  12:10 UTC  12:25 UTC
[✓ B1]  →  [✓ B2]  →  [⏳ B3]  →  [⚪ B4]
200 ord.   210 ord.   220 ord.   230 ord.
+$2.1K     +$2.3K     +$2.5K     pending
```

Each batch shows: Orders count, actual gain, fill rate on hover

#### C. **Live Orders Table**:
Columns: order_id | symbol | qty | side | status | filled_qty | entry_price | pnl

Real-time: Update every 10 seconds from Alpaca API

Color coding:
- ✅ Green (filled)
- ⏳ Gray (pending)
- 🔴 Red (error/stuck)

#### D. **Equity Performance Chart** (Recharts line chart):
- X-axis: Time (11:40 UTC → 13:55 UTC)
- Y-axis: Equity ($100K → $130K+)
- Line: Real-time equity trend
- Markers: Batch deployment points

#### E. **Safeguards Status** (right sidebar):
```
Daily Loss Limit:      -1% 🟢 OK
Position Loss Exit:    -0.5% 🟢 OK
Min Buying Power:      $15K 🟢 OK ($142K current)
Stuck Order Timeout:   10min 🟢 OK
Fill Rate Threshold:   >70% 🟡 CAUTION (65% current)
Max Pending Orders:    30 🟢 OK (2 current)
```

Each shows: Threshold | Current Value | Status Badge

**Update Frequency**: Every 10 seconds (poll Alpaca API)

**Data Source**: 
- Alpaca `/account` endpoint → equity, buying_power
- Alpaca `/orders` endpoint → order status
- Supabase `batch_deployments` table → batch gains
- Supabase `system_health_checks` table → safeguard status

---

### 3. **UPDATE SETTINGS SCREEN** (components/settings-panel.tsx)

**Current**: Basic form

**New Sections**:

#### A. **Alpaca Connection** (editable):
```
Base URL: https://paper-api.alpaca.markets/v2
API Key: [input - masked]
API Secret: [input - masked]
Account Type: ○ Paper ✓  ○ Live
Connection Status: 🟢 Connected | PA320EPZBPGV
[Test Connection] [Save]
```

#### B. **Trading Rules** (editable, saved to Supabase):
```
Daily Loss Halt:     |-1%|    [Save]
Position Stop Loss:  |-0.5%|  [Save]
Min Buying Power:    |$15K|   [Save]
Stuck Order Timeout: |600s|   [Save]
Target Fill Rate:    |80%|    [Save]
Batch Interval:      |15min|  [Save]
```

Each rule: Input + Save button + Tooltip

#### C. **Strategy Selection**:
```
◉ SHORT_AGGRESSIVE (75% shorts, 25% DCA)
  └─ For: Bearish market
  └─ Escalation: +5% per batch

○ DCA_HEAVY (70% buys, 30% shorts)
  └─ For: Neutral/bullish market

○ CUSTOM (user-defined)
```

#### D. **Market Intelligence Status**:
```
YouTube Learning:
- Status: ✅ Active
- Frequency: Every 4 hours
- Next cycle: 14:35 UTC
- Last result: 75% BEARISH (15/25 videos)

RSS Sentiment:
- Status: ✅ Active
- Feeds: 12 sources
- Last update: 12:10 UTC
- Consensus: 58% BEARISH

Twitter Sources:
- Status: ✅ Active
- Validated: 11 accounts
- Tier breakdown: 2 PLATINUM, 3 GOLD, 6 SILVER+
```

#### E. **Data Connections** (user fills):
```
Supabase Connection:
- Project URL: [input]
- Public Key: [input]
- Service Key: [input]

Alpaca Connection:
- API Key: [input - already in Section A]
- API Secret: [input - already in Section A]

YouTube API:
- API Key: [input]
- Usage: Link to video transcripts

Twitter/X:
- Pre-Validated Sources: [read-only list of 11]
```

[Test All Connections] [Save Settings] [Reset Defaults]

**Data Saved To**: Supabase `trading_rules` table

---

## 📊 PRE-POPULATED LEADS DATA

The app should come with a **pre-loaded JSON dataset** of 87 leads (entrepreneurs, investors, advisors in crypto/fintech/blockchain):

Each lead includes:
- `row_id`, `nombre_completo`, `subtitulo_tarjeta`
- `signal_type` (BULLISH, BEARISH, NEUTRAL)
- `confidence` (0-100%)
- `badges_tarjeta` (skills/tags)
- `metricas_tarjeta` (capital_score, crypto_score, etc.)
- `detalle_expandible` (areas, experience, education, languages, industries)

**File location**: `data/leads_complete.json` in your repo

**Usage**: Load on app boot, store in state/Supabase, display in Leads screen with filters

---

## 🔌 API INTEGRATIONS TO ADD

### Alpaca API Calls:
```typescript
// Get account status
const account = await fetch('https://paper-api.alpaca.markets/v2/account', {
  headers: { 'APCA-API-KEY-ID': apiKey, 'APCA-API-SECRET-KEY': apiSecret }
})

// Get orders
const orders = await fetch('https://paper-api.alpaca.markets/v2/orders', {
  headers: { ... }
})

// Poll every 10 seconds in useEffect
setInterval(fetchAccountStatus, 10000)
```

### Supabase Queries:
```typescript
// Get latest leads
const { data: leads } = await supabase
  .from('youtube_learning_cycles')
  .select('*')
  .order('created_at', { ascending: false })
  .limit(50)

// Get batch status
const { data: batches } = await supabase
  .from('batch_deployments')
  .select('*')
  .order('deployment_time', { ascending: false })

// Save trading rule
await supabase
  .from('trading_rules')
  .update({ parameter_value: newValue })
  .eq('rule_name', 'daily_loss_halt')
```

### Real-Time Subscriptions (optional, for live updates):
```typescript
supabase
  .channel('orders')
  .on('postgres_changes', 
    { event: '*', schema: 'public', table: 'orders_executed' },
    (payload) => {
      console.log('New order:', payload)
      setOrders(prev => [...prev, payload.new])
    }
  )
  .subscribe()
```

---

## 📊 DATA STRUCTURE ASSUMPTIONS

### From Supabase (tables already exist):

**youtube_learning_cycles**:
- cycle_num, search_date, videos_analyzed
- bullish_signals, bearish_signals, neutral_signals
- consensus (BULLISH/BEARISH/NEUTRAL), confidence_percent
- top_insights (JSON), recommended_strategy

**rss_sentiment_snapshots**:
- snapshot_time, total_items_analyzed
- bullish_count, bearish_count, neutral_count
- overall_sentiment, confidence_percent

**batch_deployments**:
- batch_num, deployment_time, strategy
- orders_count, orders_filled, fill_rate_percent
- expected_gain, actual_gain
- equity_before, equity_after, bp_remaining
- status (pending/completed/failed)

**trading_rules**:
- rule_name (daily_loss_halt, position_loss_exit, etc)
- parameter_value, active, description

**twitter_sources**:
- source_name, handle, followers, verified
- trust_score (0-100), tier (PLATINUM/GOLD/SILVER/BRONZE)
- specialty, proven_calls, active

**orders_executed**:
- order_id, symbol, qty, side, order_type
- status (pending/filled/partial), filled_qty, filled_price
- created_at, filled_at

---

## 🎨 DESIGN GUIDELINES

- **Real-time updates**: Charts & tables refresh every 10 seconds
- **Color scheme**: Dark background (#0f0f0f), white text, peach accents (#ff9f43)
- **Status indicators**: 🟢 green (ok), 🟡 yellow (warning), 🔴 red (critical)
- **Mobile responsive**: All screens work on phone/tablet/desktop
- **Animations**: Smooth transitions, no heavy animations (keep fast)

---

## ✅ CHECKLIST FOR THIS UPDATE

- [ ] Leads screen: Add swipe stack + filters + Supabase data
- [ ] Trading screen: Real-time account status + batch timeline + order table + equity chart + safeguards
- [ ] Settings screen: Add all input fields + test connection buttons + rule saving
- [ ] Alpaca API: Implement account + orders polling (10s interval)
- [ ] Supabase queries: Implement all data fetches
- [ ] Real-time updates: Charts & tables auto-refresh
- [ ] Error handling: Show friendly errors + retry buttons
- [ ] Environment variables: .env example with all needed keys

---

## 📦 ADD THESE TO package.json (if not already there)

```json
{
  "dependencies": {
    "recharts": "^2.10.3",
    "@supabase/supabase-js": "^2.38.0",
    "react-icons": "^4.12.0"
  }
}
```

---

## 🚀 OUTPUT EXPECTATION

After this update, the app should:
1. **Leads screen**: Functional, pulling data from Supabase, filterable, swipeable
2. **Trading screen**: Live equity + orders, real-time updates, charts working
3. **Settings screen**: All inputs work, data saves to Supabase, connections testable
4. **API integration**: Alpaca API working, Supabase queries working
5. **Production-ready**: Can push to GitHub → Vercel immediately

The output from V0 should be a complete, updated Next.js app ready to deploy.

---

**END UPDATE PROMPT**
