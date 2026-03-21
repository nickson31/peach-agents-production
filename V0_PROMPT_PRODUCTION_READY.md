# V0 PRODUCTION PROMPT - ULTRA-DETAILED
**Purpose**: Update your existing V0 app (from ZIP) with new features while preserving all existing code
**Date**: 2026-03-20 12:43 UTC
**Status**: Ready for V0 deployment

---

## ⚠️ CRITICAL: PRESERVE EXISTING STRUCTURE

Your ZIP already contains a **fully working Next.js 16 app** with:
- ✅ All Shadcn/ui components (accordion, dialog, tabs, select, etc.)
- ✅ Tailwind CSS 4.2.0
- ✅ React 19.2.4 + React Hook Form
- ✅ Recharts for charting
- ✅ Next.js 16.1.6
- ✅ Complete folder structure: `app/`, `components/`, `lib/`, `hooks/`, `data/`, `styles/`

**DO NOT REPLACE** - Only UPDATE and ADD to existing structure

---

## 📁 EXISTING ZIP STRUCTURE (PRESERVE)

```
root/
├── app/
│   ├── layout.tsx (root layout - KEEP)
│   ├── page.tsx (home page - UPDATE)
│   └── api/
│       └── brave-search/ (search API - KEEP)
├── components/
│   ├── ui/ (all Shadcn components - KEEP)
│   ├── chat-interface.tsx (KEEP)
│   ├── lead-card.tsx (UPDATE THIS)
│   ├── leads-list.tsx (UPDATE THIS)
│   ├── peach-screen.tsx (UPDATE THIS)
│   ├── swipe-stack.tsx (KEEP)
│   └── tab-bar.tsx (UPDATE THIS)
├── hooks/ (KEEP ALL)
├── lib/ (KEEP ALL)
├── data/ (KEEP - has cards_demo_es.json with 87 leads)
├── styles/ (KEEP ALL)
├── package.json (VERIFIED - no changes needed)
├── tsconfig.json (KEEP)
├── next.config.mjs (KEEP)
├── postcss.config.mjs (KEEP)
└── components.json (KEEP)
```

**ALL DEPENDENCIES VERIFIED** - Nothing to upgrade

---

## 🎯 WHAT TO UPDATE (3 SCREENS)

### 1. LEADS SCREEN (components/leads-list.tsx + lead-card.tsx)

**Current**: Basic list view
**New**: Full featured signal management

**Changes**:
- ✅ Load 87 leads from `data/cards_demo_es.json` (already exists!)
- ✅ Add swipe stack UI (Tinder-style: left dismiss, right save)
- ✅ Add filters: Source (YouTube/RSS/Whale/YouTube), Symbol, Confidence
- ✅ Add detail modal: Click lead → full description + link
- ✅ Add status tracking: NEW | REVIEWED | ACTED_ON | DISMISSED
- ✅ Color code by signal_type: 🔴 BEARISH | 🟢 BULLISH | ⚪ NEUTRAL

**Data mapping** (from your existing JSON):
```javascript
leads.map(lead => ({
  id: lead.row_id,
  name: lead.nombre_completo,
  title: lead.subtitulo_tarjeta,
  signal: lead.badges_tarjeta?.includes('Crypto') ? 'BEARISH' : 'BULLISH',
  confidence: lead.metricas_tarjeta?.lead_quality_score || 80,
  description: lead.resumen_tarjeta,
  details: lead.detalle_expandible,
  status: 'NEW'
}))
```

**UI**: Keep existing card style, add swipe gestures + modal

---

### 2. TRADING SCREEN (peach-screen.tsx)

**Current**: Basic layout
**New**: Live trading dashboard

**Add these sections**:

#### A. Account Status Card (top)
```
Equity: $100,562 → $130,000 (target)
Buying Power: $142,066 ✅
Daily Gain: +$2,500 (+2.5%)
Batch Status: 3/8 ⏳
Fill Rate: 65% (target 70%)
```

#### B. Batch Timeline (visual)
```
11:40 UTC  11:55 UTC  12:10 UTC
[✓ B1]  →  [✓ B2]  →  [⏳ B3]
200 ord.   210 ord.   220 ord.
+$2.1K     +$2.3K     +$2.5K
```

#### C. Live Orders Table
Columns: order_id | symbol | qty | side | status | pnl
Update every 10 seconds from Alpaca API

#### D. Equity Performance Chart (use Recharts - already installed)
- X-axis: Time (11:40 UTC → 13:55 UTC)
- Y-axis: Equity ($100K → $130K+)
- Line: Real-time equity trend
- Markers: Batch deployment points

#### E. Safeguards Status Panel
```
Daily Loss Limit:      -1% 🟢 OK
Position Loss Exit:    -0.5% 🟢 OK
Min Buying Power:      $15K 🟢 OK
Stuck Order Timeout:   10min 🟢 OK
Fill Rate Threshold:   >70% 🟡 CAUTION (65% current)
```

**Update Frequency**: Every 10 seconds (use setInterval + fetch)

---

### 3. SETTINGS SCREEN (new component or update existing)

**Add these sections**:

#### A. Alpaca Connection
```
Base URL: https://paper-api.alpaca.markets/v2
API Key: [input - masked]
API Secret: [input - masked]
Status: 🟢 Connected
[Test Connection] [Save]
```

#### B. Trading Rules (editable, save to localStorage or Supabase)
```
Daily Loss Halt:     |-1%|
Position Stop Loss:  |-0.5%|
Min Buying Power:    |$15K|
Stuck Order Timeout: |600s|
Target Fill Rate:    |80%|
Batch Interval:      |15min|
```

#### C. Market Intelligence Status
```
YouTube Learning: ✅ Active (Next: 14:35 UTC)
RSS Sentiment: ✅ Active (Last: 58% BEARISH)
Market Phase: BEARISH
```

#### D. Data Connections (read-only display)
```
Supabase: Connected ✅
Alpaca: Connected ✅
YouTube: Active ✅
RSS Feeds: 12 sources active
```

---

## 🔌 API INTEGRATIONS

### Alpaca Paper Trading API
**Endpoint**: `https://paper-api.alpaca.markets/v2`

**Calls to implement**:
```typescript
// Get account
GET /account
Headers: { 'APCA-API-KEY-ID': key, 'APCA-API-SECRET-KEY': secret }

// Get orders
GET /orders?status=all&limit=100

// Create order
POST /orders
Body: { symbol, qty, side, type, time_in_force, ... }
```

**Poll frequency**: Every 10 seconds
**Used in**: Trading screen (equity, orders, fill rate)

### Supabase (if needed)
**Connection string**: `https://your-project.supabase.co`
**Public key**: `NEXT_PUBLIC_SUPABASE_KEY` in .env
**Usage**: Save settings, historical data (optional for MVP)

---

## 📊 PRE-LOADED DATA

### Leads JSON (87 rows - already in `data/cards_demo_es.json`)
The ZIP already has your leads! Use it:

```typescript
import leads from '@/data/cards_demo_es.json'

// Map to component format
const mappedLeads = leads.map(lead => ({
  id: lead.row_id,
  name: lead.nombre_completo,
  title: lead.subtitulo_tarjeta,
  confidence: lead.metricas_tarjeta?.lead_quality_score,
  signal: determineBearishBullish(lead.badges_tarjeta),
  ...lead
}))
```

---

## 🔧 ENVIRONMENT VARIABLES (.env.local)

Create this file:
```env
# Alpaca
NEXT_PUBLIC_ALPACA_BASE_URL=https://paper-api.alpaca.markets/v2
ALPACA_API_KEY=user_will_provide
ALPACA_API_SECRET=user_will_provide

# Supabase (optional)
NEXT_PUBLIC_SUPABASE_URL=user_will_provide
NEXT_PUBLIC_SUPABASE_ANON_KEY=user_will_provide

# YouTube/RSS (optional)
YOUTUBE_API_KEY=user_will_provide
```

---

## 📝 FILE-BY-FILE CHANGES

### ✅ KEEP AS-IS (DO NOT TOUCH)
- `app/layout.tsx`
- `app/api/brave-search/route.ts`
- `components/ui/*` (all Shadcn components)
- `components/chat-interface.tsx`
- `components/swipe-stack.tsx`
- `lib/*`
- `hooks/*`
- `styles/*`
- `package.json`
- `tsconfig.json`
- `next.config.mjs`
- `postcss.config.mjs`

### 🔄 UPDATE (MODIFY EXISTING)
- `components/leads-list.tsx` → Add filters, swipe, modal, load from data/cards_demo_es.json
- `components/lead-card.tsx` → Add swipe gestures, status badge, confidence score
- `components/peach-screen.tsx` → Add account card, batch timeline, orders table, chart, safeguards
- `components/tab-bar.tsx` → Add "Settings" tab if not present
- `app/page.tsx` → Route to correct tab (Dashboard/Leads/Trading/Settings)

### ✨ CREATE NEW (ADD)
- `components/settings-panel.tsx` → Full settings screen (API config, rules, connections)
- `components/trading-dashboard.tsx` → Main trading screen (or update peach-screen.tsx)
- `app/settings/page.tsx` (optional) → Settings page route
- `lib/alpaca-client.ts` → Helper functions for Alpaca API calls

---

## 🚀 IMPLEMENTATION CHECKLIST

Before V0 generates:
- [ ] Preserve all existing components in `components/ui/`
- [ ] Use existing leads JSON from `data/cards_demo_es.json`
- [ ] Don't upgrade package.json dependencies
- [ ] Keep Tailwind CSS 4.2.0
- [ ] Keep React 19.2.4
- [ ] Add Alpaca API polling (10s interval)
- [ ] Add swipe gesture detection (Tinder-style)
- [ ] Add Recharts line chart for equity
- [ ] Add editable input fields for settings
- [ ] Add color-coded badges (BULLISH/BEARISH/NEUTRAL)

---

## ✅ POST-DEPLOYMENT VERIFICATION

After V0 generates, verify:

1. **Existing code still works**
   - npm run dev (should start without errors)
   - Navigate to each tab (Dashboard, Leads, Trading, Settings)
   - Existing leads display correctly

2. **New features work**
   - Leads: Can swipe, filter, view detail modal
   - Trading: Account card updates, equity chart renders, orders table shows data
   - Settings: Can edit API key, see connection status

3. **Alpaca integration**
   - curl test: `curl -H "APCA-API-KEY-ID: $KEY" https://paper-api.alpaca.markets/v2/account`
   - Should return account info (equity, buying_power, etc.)

4. **Real-time updates**
   - Trading screen equity updates every 10 seconds
   - Chart animates smoothly
   - Orders table refreshes

---

## 🔗 CONNECTIONS SUMMARY

```
Your App (V0)
├── Frontend: React 19 + Next.js 16 + Tailwind
├── Data source: data/cards_demo_es.json (87 leads)
├── API: Alpaca Paper Trading (user provides keys)
├── DB: Supabase (optional, for persistence)
├── GitHub: Push when done
└── Vercel: Deploy automatically
```

**No Twitter/X integration** - Removed as requested

---

## 🔌 OPENCLAW INTEGRATION (CRITICAL)

Your app (Vercel) needs to communicate with OpenClaw (localhost) for:
- Order deployment status updates
- Real-time equity/BP changes
- Market learning cycles
- System health checks

### Connectivity Architecture

```
┌─────────────────────────────────────────────────┐
│ VERCEL (Cloud)                                  │
│ Your V0 App (React)                             │
│ ├─ Leads Screen                                 │
│ ├─ Trading Dashboard                           │
│ └─ Settings Panel                               │
└─────────────────────┬───────────────────────────┘
                      │ HTTPS API
                      ↓
┌─────────────────────────────────────────────────┐
│ OPENCLAW (Local: ip-172-31-32-188)              │
│ ├─ Trading System (running)                     │
│ ├─ Order Monitor (every 60s)                    │
│ ├─ Deployment Scripts                           │
│ ├─ Market Learning (YouTube/RSS)                │
│ └─ Supabase sync                                │
└─────────────────────────────────────────────────┘
```

### OpenClaw Endpoints (Expose these)

Your OpenClaw needs to expose REST API endpoints:

```bash
# 1. Get current account status
GET http://localhost:3001/api/account
Response: {
  equity: 100562,
  buying_power: 142066,
  cash: 45918,
  positions: [{ symbol: 'ETHE', qty: 1838, entry: 3445 }]
}

# 2. Get recent orders
GET http://localhost:3001/api/orders?limit=50
Response: {
  orders: [
    { id: 'xxx', symbol: 'ETHE', qty: 1, side: 'buy', status: 'filled', filled_price: 3445 }
  ]
}

# 3. Get batch deployments
GET http://localhost:3001/api/batches
Response: {
  batches: [
    { batch_num: 1, orders_count: 200, fill_rate: 65, actual_gain: 2100, equity_after: 102700 }
  ]
}

# 4. Get market conditions
GET http://localhost:3001/api/market-conditions
Response: {
  market_phase: 'BEARISH',
  vix: 18.5,
  youtube_consensus: 75,
  rss_sentiment: 58,
  recommended_strategy: 'SHORT_AGGRESSIVE'
}

# 5. Get system health
GET http://localhost:3001/api/health
Response: {
  deployment_running: true,
  order_monitor_active: true,
  stuck_orders: 0,
  last_update: '2026-03-20T12:43:00Z'
}
```

### Setting up OpenClaw API (Node.js Express example)

Create `openclaw-api-server.js` in your OpenClaw workspace:

```javascript
const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());

// 1. Account status endpoint
app.get('/api/account', async (req, res) => {
  // Fetch from Alpaca API
  const alpacaResponse = await fetch(
    'https://paper-api.alpaca.markets/v2/account',
    { headers: {...} }
  );
  const account = await alpacaResponse.json();
  res.json({
    equity: account.equity,
    buying_power: account.buying_power,
    cash: account.cash,
    positions: account.positions
  });
});

// 2. Orders endpoint
app.get('/api/orders', async (req, res) => {
  const limit = req.query.limit || 50;
  const alpacaResponse = await fetch(
    `https://paper-api.alpaca.markets/v2/orders?status=all&limit=${limit}`,
    { headers: {...} }
  );
  const orders = await alpacaResponse.json();
  res.json({ orders });
});

// 3. Batches endpoint (from Supabase)
app.get('/api/batches', async (req, res) => {
  // Fetch from Supabase batch_deployments table
  const batches = await supabase
    .from('batch_deployments')
    .select('*')
    .order('deployment_time', { ascending: false })
    .limit(50);
  res.json({ batches: batches.data });
});

// 4. Market conditions endpoint (from Supabase)
app.get('/api/market-conditions', async (req, res) => {
  const conditions = await supabase
    .from('market_conditions')
    .select('*')
    .order('check_time', { ascending: false })
    .limit(1)
    .single();
  res.json(conditions.data);
});

// 5. Health check endpoint
app.get('/api/health', async (req, res) => {
  res.json({
    deployment_running: isDeploymentRunning(),
    order_monitor_active: isOrderMonitorActive(),
    stuck_orders: getStuckOrdersCount(),
    last_update: new Date().toISOString()
  });
});

app.listen(3001, () => console.log('OpenClaw API on :3001'));
```

### V0 App: How to Connect

In your `lib/openclaw-client.ts`:

```typescript
const OPENCLAW_API = process.env.NEXT_PUBLIC_OPENCLAW_URL || 'http://localhost:3001';

export async function getAccountStatus() {
  const res = await fetch(`${OPENCLAW_API}/api/account`);
  return res.json();
}

export async function getRecentOrders(limit = 50) {
  const res = await fetch(`${OPENCLAW_API}/api/orders?limit=${limit}`);
  return res.json();
}

export async function getBatches() {
  const res = await fetch(`${OPENCLAW_API}/api/batches`);
  return res.json();
}

export async function getMarketConditions() {
  const res = await fetch(`${OPENCLAW_API}/api/market-conditions`);
  return res.json();
}

export async function getSystemHealth() {
  const res = await fetch(`${OPENCLAW_API}/api/health`);
  return res.json();
}
```

In your Trading Screen component:

```typescript
import { getAccountStatus, getBatches } from '@/lib/openclaw-client';

export default function TradingDashboard() {
  const [account, setAccount] = useState(null);
  const [batches, setBatches] = useState([]);

  useEffect(() => {
    // Poll every 10 seconds
    const interval = setInterval(async () => {
      const accData = await getAccountStatus();
      const batchData = await getBatches();
      setAccount(accData);
      setBatches(batchData.batches);
    }, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <AccountCard equity={account?.equity} bp={account?.buying_power} />
      <BatchTimeline batches={batches} />
    </div>
  );
}
```

### Environment Variables for OpenClaw Connection

Add to `.env.local`:

```env
# For localhost development
NEXT_PUBLIC_OPENCLAW_URL=http://localhost:3001

# For production (Vercel → OpenClaw via VPN/public IP)
# NEXT_PUBLIC_OPENCLAW_URL=https://your-openclaw-public-url.com
```

### Deployment Strategy

1. **Local Development** (you):
   - Run V0 app locally: `npm run dev`
   - Run OpenClaw API server: `node openclaw-api-server.js`
   - App calls `http://localhost:3001/api/*`
   - Everything works ✅

2. **Vercel Deployment**:
   - App deployed to Vercel (cloud)
   - OpenClaw stays local (but needs public endpoint)
   - Options:
     a) Expose OpenClaw via ngrok/Cloudflare tunnel
     b) Use VPN (Tailscale) to connect Vercel → Local
     c) Use Supabase as bridge (bidirectional sync)

3. **Recommended: Supabase as Bridge**
   - OpenClaw writes to Supabase (batches, orders, conditions)
   - V0 app reads from Supabase
   - No need to expose OpenClaw publicly
   - More secure ✅

---

## OpenClaw Sync to Supabase (Recommended)

Create `openclaw-sync.py` in OpenClaw that writes data to Supabase:

```python
import supabase_client
from datetime import datetime

def sync_batch_to_supabase(batch_data):
    supabase.table('batch_deployments').insert({
        'batch_num': batch_data['batch_num'],
        'deployment_time': datetime.now(),
        'strategy': 'SHORT_AGGRESSIVE',
        'orders_count': batch_data['orders'],
        'fill_rate_percent': batch_data['fill_rate'],
        'actual_gain': batch_data['gain'],
        'equity_after': batch_data['equity']
    })

def sync_account_to_supabase(account_data):
    supabase.table('trading_accounts').update({
        'current_equity': account_data['equity'],
        'buying_power': account_data['bp']
    }).eq('account_id', 'PA320EPZBPGV')
```

Then V0 app just reads from Supabase:

```typescript
// Much simpler - no polling local API
const { data: batches } = await supabase
  .from('batch_deployments')
  .select('*')
  .order('deployment_time', { ascending: false });
```

---

## 📌 CRITICAL NOTES

1. **ZIP is production-ready** - Don't break it
2. **87 leads are already loaded** - Use them directly
3. **All UI components exist** - Only update specific screens
4. **No new dependencies** - package.json stays the same
5. **Preserve folder structure** - Add files, don't reorganize
6. **Test locally first** - `npm run dev` before pushing

---

**END OF PROMPT**

**Output**: Updated Next.js app, ready to push to GitHub → Vercel → Production

