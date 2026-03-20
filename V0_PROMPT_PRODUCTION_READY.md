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

