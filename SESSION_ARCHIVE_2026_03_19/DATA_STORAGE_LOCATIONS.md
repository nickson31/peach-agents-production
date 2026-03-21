# PEACH&AGENTS - DONDE SE GUARDAN LOS DATOS

## 🎯 UBICACIONES EXACTAS

---

## 1. 🔐 AUTHENTICATION TOKENS

### Location: Browser Memory + Cookies (Optional)
```
Type: JWT Token
Stored in: Browser localStorage
Path: localStorage.getItem('peach_token')
Expires: 7 days (configurable)
Accessible by: Only your app domain
Deleted on: Token expiry OR user logout
```

### Code Location:
```typescript
// lib/auth.ts
localStorage.setItem('peach_token', token)
localStorage.getItem('peach_token')
```

---

## 2. 🤖 BOTS DATA

### Location 1: Browser Memory (Session)
```
Type: JavaScript Object
Stored in: React state (useBotsManagement hook)
Duration: Only while app is open
Survives refresh: NO
Example path: hooks/use-bots.ts
```

### Code:
```typescript
const [bots, setBots] = useState<Bot[]>([])
// Lost on refresh ❌
```

### Location 2: Browser Storage (Persistent)
```
Type: JSON string
Stored in: Browser localStorage
Path: localStorage.getItem('peach_bots')
Duration: Until user clears browser cache
Survives refresh: YES ✓
Survives closing browser: YES ✓
Example size: ~10-100 KB per bot
```

### Code:
```typescript
// Save to localStorage
localStorage.setItem('peach_bots', JSON.stringify(bots))

// Load from localStorage
const savedBots = JSON.parse(localStorage.getItem('peach_bots') || '[]')
```

### Location 3: Alpaca API (Live Orders Only)
```
Type: Live order data
Stored in: Alpaca servers (paper trading)
Path: https://paper-api.alpaca.markets/v2/orders
Duration: Until order completed/cancelled
Survives anything: YES (cloud backup) ✓
Owned by: Alpaca Inc (your trading data)
```

### Code:
```typescript
// lib/alpaca-client.ts
const orders = await alpacaClient.getOrders()
// Fetched real-time, not stored locally
```

---

## 3. 📊 BOT STATISTICS & PERFORMANCE

### Real-Time Performance (Session):
```
Type: Calculated metrics
Stored in: Memory (component state)
Duration: Only during active trading
Source: Alpaca API (live)
Example:
{
  fill_rate: 85.3,
  pnl: 234.50,
  orders_deployed: 100,
  orders_filled: 85
}
```

### Code:
```typescript
// hooks/use-bots.ts - updateBotStats()
const stats = {
  ordersDeployed: result.ordersDeployed,
  ordersFilled: result.ordersFilled,
  fillRate: result.fillRate,
}
// Updated real-time, not persisted
```

### Historical Performance: NOWHERE (now)
```
❌ NOT stored
❌ Lost on refresh
❌ No historical database

Add Supabase (Phase 2):
├─ Create table: bot_stats
├─ Store: { bot_id, fill_rate, pnl, timestamp }
└─ Query: Last 30 days performance
```

---

## 4. 📁 LEADS DATA

### Location 1: Browser Memory
```
Type: JavaScript array
Stored in: React state (context)
Duration: During session
Survives refresh: NO ❌
```

### Code:
```typescript
// lib/leads-context.tsx
const [leads, setLeads] = useState<Lead[]>([])
```

### Location 2: Browser localStorage
```
Type: JSON
Stored in: localStorage
Path: localStorage.getItem('peach_leads')
Duration: Persistent
Survives refresh: YES ✓
Example size: ~5-50 KB
```

### Code:
```typescript
useEffect(() => {
  localStorage.setItem('peach_leads', JSON.stringify(leads))
}, [leads])
```

### Location 3: Imported JSON Files
```
Type: .json files
Stored in: User's computer
How: File upload/import
Path: /data/cards_demo_es.json (example)
Survives everything: YES (user owns file) ✓
```

---

## 5. 🔑 API KEYS & SECRETS

### Development (Local):
```
Type: Environment variables
Stored in: .env.local file
Location: /peach-agents-platform/.env.local
Accessible by: Local dev server only
Protected by: .gitignore (NOT in git)
Example:
  ALPACA_KEY=PKW445AWAOSGU2WJYCCFUZ47PR
  JWT_SECRET=your-secret-key
  SAFE: ✓ Local machine only
```

### Production (Vercel):
```
Type: Environment secrets
Stored in: Vercel platform
Location: Vercel Dashboard → Settings → Env
Protected by: Vercel's security
Data center: Distributed (encrypted)
Access level: Only app runtime
Accessible in: /api routes only (server-side)
Client-side access: NEVER ❌
```

---

## 6. 🔐 USER SETTINGS & PREFERENCES

### Browser Storage:
```
Type: JSON
Stored in: localStorage
Path: localStorage.getItem('peach_settings')
Includes:
{
  theme: "dark",
  defaultStrategy: "trend-following",
  notifications: true
}
```

---

## 7. 📡 REAL-TIME DATA (Live Trading)

### Source: Alpaca API
```
Location: Cloud (Alpaca servers)
Fetched: Real-time (every 5 seconds)
Stored locally: NO (live only)
Example data:
{
  price: 45.23,
  bid: 45.21,
  ask: 45.25,
  timestamp: 1710923500
}
Data flow:
  Alpaca servers 
    → Fetch via API
    → Display on UI
    → Discard (fetch fresh)
```

### Code:
```typescript
// Real-time polling
const bars = await alpaca.getBars('ETHE')
// New fetch, no storage
```

---

## 📊 STORAGE COMPARISON TABLE

| Data Type | Storage | Persistent | Secure | Size |
|-----------|---------|-----------|--------|------|
| Auth Token | Memory + localStorage | 7 days | High | ~1 KB |
| Bots | localStorage | Yes | Medium | ~50 KB |
| Leads | localStorage | Yes | Medium | ~50 KB |
| Performance | Memory only | NO | High | ~10 KB |
| Real-time prices | Memory (live) | NO | N/A | ~1-50 KB |
| API Keys | Vercel Secrets | N/A | Ultra | Hidden |
| Settings | localStorage | Yes | Low | ~5 KB |

---

## 🗺️ COMPLETE DATA MAP

```
┌─────────────────────────────────────────────┐
│           PEACH&AGENTS DATA MAP             │
└─────────────────────────────────────────────┘

CLIENT (Browser) - User's Computer
├─ localStorage (Persistent local storage)
│  ├─ peach_token (JWT auth)
│  ├─ peach_bots (Bot configs)
│  ├─ peach_leads (Lead data)
│  ├─ peach_settings (Settings)
│  └─ Size: ~150 KB max
│
├─ Memory (Session only - Lost on close)
│  ├─ React state (real-time data)
│  ├─ Component props
│  └─ Real-time calculations
│
└─ Cookies (Optional)
   └─ Session management (if enabled)

VERCEL (Edge servers in USA)
├─ Environment Secrets
│  ├─ JWT_SECRET
│  ├─ ALPACA_KEY
│  └─ Encrypted at rest
│
└─ Function logs (temporary)
   └─ Deleted after 24h

ALPACA SERVERS (Cloud)
├─ Live Orders
│  ├─ Order ID
│  ├─ Price
│  ├─ Status
│  └─ Owned by: Alpaca Inc
│
├─ Account Info
│  ├─ Equity
│  ├─ Cash balance
│  └─ Paper trading only
│
└─ Market Data
   ├─ Real-time prices
   ├─ Historical bars
   └─ Fetched on-demand

GITHUB
├─ Source code (Version control)
├─ .env.example (NOT secrets)
└─ NO sensitive data

NOWHERE (No Database)
├─ Historical performance data
├─ Trade history (could add later)
├─ User profiles (Phase 2)
└─ Audit logs (Phase 2)
```

---

## 🔒 SECURITY BY LOCATION

### ULTRA SECURE (Encrypted, server-side):
```
✅ Vercel Secrets (API keys)
✅ Alpaca account data (trading data)
✅ JWT tokens (signed, can't tamper)
```

### SECURE (Local, encrypted by browser):
```
✅ localStorage (same-origin only)
✅ Browser cookies (httpOnly if enabled)
```

### LESS SECURE (Plain JSON):
```
⚠️ localStorage (if browser compromised)
⚠️ Browser memory (if malware active)
```

---

## 📥 IMPORT/EXPORT FLOWS

### Export Bots as JSON:
```
localStorage['peach_bots']
    ↓
JSON.stringify()
    ↓
Download .json file
    ↓
User's computer (safe)
    ↓
Can share, backup, restore
```

### Import Leads from ZIP:
```
User uploads ZIP
    ↓
Extract JSON files
    ↓
Process in memory
    ↓
Save to localStorage
    ↓
Display on dashboard
```

---

## ⚙️ CONFIGURATION STORAGE

### Development (.env.local):
```bash
Location: /peach-agents-platform/.env.local
Owner: You (local machine)
Visibility: Private (in .gitignore)
Read by: Next.js dev server
Protect with: File permissions
```

### Production (Vercel):
```
Location: Vercel Dashboard
Owner: You (Vercel account)
Visibility: Private (encrypted)
Read by: App runtime only
Protect with: Vercel's security
```

---

## 🗑️ DATA DELETION

### Automatic:
```
✓ Auth tokens (expire after 7 days)
✓ Vercel function logs (after 24h)
✓ React memory (on refresh)
```

### Manual (User action):
```
✓ localStorage (browser settings → clear cache)
✓ Downloaded JSON files (delete file)
✓ Bot configs (click "Delete" in UI)
```

### Server-side (By developer):
```
✓ Alpaca orders (API call to cancel)
✓ Vercel secrets (remove from dashboard)
✓ GitHub repo (delete repository)
```

---

## 🚀 TO ADD PERSISTENT DATABASE (Phase 2)

Add Supabase to store:
```
├─ Bots (persist across sessions)
├─ Bot Stats (historical performance)
├─ Trades (all executed trades)
├─ Leads (searchable, indexed)
└─ Users (if multi-user)

Storage: PostgreSQL (Supabase)
Location: Supabase data centers
Size limit: Free tier 500MB
Cost: Free to $320+/month
```

---

## 📋 SUMMARY

**Where data lives RIGHT NOW:**

| Type | Where | Duration |
|------|-------|----------|
| Auth | localStorage | 7 days |
| Bots | localStorage | Persistent |
| Leads | localStorage | Persistent |
| Performance | Memory | Session only |
| Prices | Memory | Live only |
| Secrets | Vercel | Runtime only |
| Orders | Alpaca API | Until completed |

**Total local storage used:** ~150-200 KB
**Total cloud data:** Only Alpaca orders + Vercel secrets

---

**ANSWER: Everything stays in browser localStorage or Alpaca servers. No database yet.** 🍑
