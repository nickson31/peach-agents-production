# PEACH&AGENTS - SUPABASE INTEGRATION

## 🎯 CURRENT STATE

**Data Handling NOW:**
```
✓ Authentication: JWT (stateless, no database needed)
✓ Bots: In-memory (frontend state + localStorage)
✓ Leads: In-memory (frontend state)
✓ Performance: Calculated real-time from Alpaca API
✓ Database: NONE (single-user, paper trading only)
```

---

## ❓ DO YOU NEED SUPABASE?

### Use Supabase if you want:
- ✅ **Persistent bot history** - Save bots across sessions
- ✅ **Trade history** - Store all past trades
- ✅ **Performance analytics** - Long-term P&L tracking
- ✅ **Multiple users** - Support more than one account
- ✅ **Lead database** - Search history, saved leads
- ✅ **Audit trail** - Log all actions

### Skip Supabase if:
- ✅ **Single-user only** - Just you/one client using it
- ✅ **Live trading only** - Don't care about history
- ✅ **Paper trading** - Testing mode only
- ✅ **Session-based** - Clear on refresh is fine

---

## 🔄 CURRENT DATA FLOW

```
User Login
    ↓
JWT Token (stateless)
    ↓
Create Bot
    ↓
Store in localStorage (browser only)
    ↓
Deploy to Alpaca
    ↓
Real-time updates from Alpaca API
    ↓
Display on dashboard
    ↓
(Close browser → Data gone)
```

---

## 💾 HOW TO ADD SUPABASE

### OPTION 1: Store Bot History Only

**Best for:** Tracking bot performance over time

**What to save:**
```sql
CREATE TABLE bots (
  id UUID PRIMARY KEY,
  name TEXT,
  strategy TEXT,
  symbols TEXT[],
  allocation JSONB,
  config JSONB,
  status TEXT,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TABLE bot_stats (
  id UUID PRIMARY KEY,
  bot_id UUID REFERENCES bots,
  orders_deployed INT,
  orders_filled INT,
  fill_rate FLOAT,
  pnl FLOAT,
  timestamp TIMESTAMP
);

CREATE TABLE trades (
  id UUID PRIMARY KEY,
  bot_id UUID REFERENCES bots,
  symbol TEXT,
  entry_price FLOAT,
  exit_price FLOAT,
  quantity INT,
  pnl FLOAT,
  timestamp TIMESTAMP
);
```

**Setup Time:** 30 min

---

### OPTION 2: Full Multi-User System

**Best for:** Supporting multiple traders

**What to save:**
```sql
-- Users
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email TEXT UNIQUE,
  username TEXT UNIQUE,
  password_hash TEXT,
  created_at TIMESTAMP
);

-- Bots (per user)
CREATE TABLE user_bots (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users,
  name TEXT,
  strategy TEXT,
  symbols TEXT[],
  allocation JSONB,
  status TEXT,
  created_at TIMESTAMP
);

-- Leads (per user)
CREATE TABLE user_leads (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users,
  source TEXT,
  data JSONB,
  created_at TIMESTAMP
);

-- Portfolio (per user)
CREATE TABLE user_portfolios (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users,
  total_pnl FLOAT,
  filled_rate FLOAT,
  updated_at TIMESTAMP
);
```

**Setup Time:** 2-3 hours

---

## 🔐 SUPABASE SETUP (If needed)

### Step 1: Create Supabase Project
```
1. Go to supabase.com
2. Sign up (free tier available)
3. Create new project
4. Get connection string
```

### Step 2: Add to Environment
```
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIs...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGc...
```

### Step 3: Install Client
```bash
pnpm add @supabase/supabase-js
```

### Step 4: Create Client
```typescript
// lib/supabase.ts
import { createClient } from '@supabase/supabase-js'

export const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)
```

### Step 5: Use in API Routes
```typescript
// app/api/bots/save/route.ts
import { supabase } from '@/lib/supabase'

export async function POST(req: Request) {
  const { bot } = await req.json()
  
  const { data, error } = await supabase
    .from('bots')
    .insert([bot])
  
  if (error) return Response.json({ error })
  return Response.json({ data })
}
```

---

## 🚀 RECOMMENDATION

### For RIGHT NOW:
**✅ SKIP Supabase**
- Single-user mode works without DB
- JWT auth is stateless
- No database overhead
- Faster deployment
- Cheaper (no Supabase costs)
- Redis/caching not needed

### Bots/leads stored in:
- `localStorage` (browser - persists on refresh)
- Memory (session-based)
- Can export/import via JSON

### For LATER (Phase 2):
**Add Supabase if you want:**
- [ ] Multi-user support
- [ ] Historical analytics
- [ ] Audit trails
- [ ] Shared leads library
- [ ] Performance dashboards

---

## 📊 DATA PERSISTENCE NOW

### What PERSISTS (browser localStorage):
```javascript
// Automatically saved
{
  bots: [
    {
      id: "bot-123",
      name: "My Bot",
      status: "monitoring",
      stats: { ... }
    }
  ],
  leads: [ ... ],
  folders: [ ... ]
}
```

### What DOESN'T persist (in-memory):
```
JWT Token (refreshes on each session)
Alpaca connection (recreated per deployment)
Real-time order updates (live from Alpaca)
```

### Import/Export (Manual):
```typescript
// Users can export their bots
const json = JSON.stringify(bots)
// Download as .json file

// Import from file
const imported = JSON.parse(fileContent)
```

---

## 💡 HYBRID APPROACH (Recommended)

**Keep current setup:**
- ✅ JWT auth (no DB)
- ✅ localStorage persistence (local)
- ✅ Real-time from Alpaca (API)

**Add only if needed:**
- Optional backup to Supabase
- Historical analytics (not real-time)
- Export bot configs to share

**Benefits:**
- Works day 1 (no DB setup)
- Add DB later if needed
- No extra costs now
- No extra complexity

---

## ⚡ QUICK ANSWER

| Question | Answer |
|----------|--------|
| Works without Supabase? | ✅ Yes (currently designed this way) |
| Need Supabase to deploy? | ❌ No |
| How are bots stored? | localStorage (browser) |
| How is auth stored? | JWT tokens (stateless) |
| Persist across refresh? | ✅ Yes (localStorage) |
| Persist across devices? | ❌ No (need database) |
| Add Supabase later? | ✅ Easy to add |
| Performance hit without DB? | ❌ None (faster actually) |

---

## 🎯 DECISION MATRIX

```
If you want...                    Do this
────────────────────────────────────────────────
Just deploy & run              → Don't add Supabase
Single user, me only           → Don't add Supabase
Multi-user support needed      → Add Supabase
Long-term analytics            → Add Supabase
Audit trail required           → Add Supabase
Share bots between users       → Add Supabase
Export/import bots             → Add Supabase (Phase 2)
```

---

## 🔗 FILES TO KEEP AS-IS

If you DON'T add Supabase:
```
✅ Keep all current files
✅ No changes to hooks/use-bots.ts
✅ No changes to lib/alpaca-client.ts
✅ No database layer needed
✅ Deploy as-is to Vercel
```

---

**ANSWER: Yes, you CAN add Supabase later. Don't need it now.** 🚀
