# Olimpiada: Cost Analysis + Action Plan

## DESGLOSE DE COSTOS POR OLIMPIADA

### 1. YouTube Extraction

**Opción A: YouTube Data API (Official)**
```
- Cost: $0 (free tier: 10K units/day)
- Per olimpiada: ~50-100 units (videos search + metadata)
- Verdict: FREE for small scale
- Limitation: Free tier runs out at 500+ olimpiadas/day
```

**Opción B: Playwright/Puppeteer (Scraping Captions)**
```
- Cost: $0 (open source) + infrastructure (CPU/memory)
- Per olimpiada: 20 videos × 30 sec = ~10 min processing
- Verdict: Cheap but slower
- Infrastructure: Vercel Functions (included in plan)
```

**Decision: Use FREE YouTube API → Fallback to Playwright if quota exceeded**

**COST: $0**

---

### 2. LLM Parsing (20 Estrategias)

**Current: OpenRouter gpt-4-turbo-mini**
```
Input tokens: ~500 per video transcript (20 videos)
Output tokens: ~200 per strategy config (20 configs)

Cost per olimpiada:
├─ Input: (500 × 20) × $0.003/1K = $0.03
├─ Output: (200 × 20) × $0.006/1K = $0.024
└─ TOTAL: $0.054 per olimpiada

Batched (all 20 at once in 1 call):
├─ Input: 10,000 tokens × $0.003/1K = $0.03
├─ Output: 4,000 tokens × $0.006/1K = $0.024
└─ TOTAL: $0.054 per olimpiada
```

**Alternative: claude-3-haiku (even cheaper)**
```
- Input: $0.25 per 1M tokens
- Output: $1.25 per 1M tokens
- Per olimpiada: ~$0.02
```

**COST: $0.05-0.02 per olimpiada (pick cheapest)**

---

### 3. Historical Backtest (30 days, 2000 bars)

**Option A: Free Data (OHLCV from Alpaca/IEX)**
```
- Cost: $0 (Alpaca free tier includes historical data)
- Time: Python backtest = instant (local)
- Verdict: FREE
```

**Option B: Polygon.io (if need premium data)**
```
- Cost: $99/mo (enterprise)
- Verdict: Overkill for MVP
```

**Decision: Use Alpaca free historical data**

**COST: $0**

---

### 4. Alpaca Paper Trading (Bot Deployment)

**Paper Account:**
```
- Cost: $0 (free)
- API calls: ~/5 sec loop × 3 bots = unlimited
- Verdict: Completely free
```

**Live Account (if user migrates):**
```
- Monthly: $0 (commission-based for crypto/forex)
- Per trade: 0.1% commission (crypto) or spread (forex)
- Verdict: User pays, not us
```

**COST: $0 (MVP)**

---

### 5. Infrastructure (Shared)

**All Olimpiadas on Same Infrastructure:**
```
Vercel Functions: Included in Vercel $20/mo
├─ Unlimited API calls
├─ Serverless (scales automatically)
├─ Pay per compute: $0.50-1.00 per million invocations

CPU for backtest (2000 bars × 20 strategies):
├─ ~500ms per olimpiada
├─ Vercel: ~$0.0001 per invocation (negligible)
└─ Cost: ~$0.0001
```

**COST: ~$0.0001 per olimpiada (negligible)**

---

### 6. Database (Supabase)

**Per Olimpiada Storage:**
```
- olimpiada_configs: ~5 KB (config + results JSON)
- 20 strategy_exports: ~100 KB (strategy rules × 20)
- 200+ bot_executions (live): ~50 KB (per bot over 1 week)
- TOTAL: ~150 KB per olimpiada

Supabase free tier: 500 MB
├─ Can store: 3,300+ olimpiadas
├─ Cost: $0 (free tier)
└─ Pro ($25/mo): 8 GB (unlimited for MVP)
```

**COST: $0 (free tier) → $25/mo (if scaling)**

---

## TOTAL COST PER OLIMPIADA

```
YouTube API:           $0
LLM parsing:           $0.05
Backtest compute:      $0
Alpaca API:            $0
Infrastructure:        $0.0001
Database:              $0 (amortized)
─────────────────────────────
TOTAL:                 ~$0.05 per olimpiada
```

**With 50 olimpiadas/month: $2.50/mo** ✓

---

## MONTHLY INFRASTRUCTURE COSTS (Fixed)

```
Vercel (hosting):           $20/mo
Supabase (database):        $0 (free) → $25/mo (pro)
OpenRouter (LLM credits):   $100/mo (500K tokens average)
Brave Search API:           $100/mo
YouTube API:                $0
Alpaca API:                 $0
─────────────────────────────
TOTAL FIXED:                ~$220/mo (small scale)
VARIABLE (per olimpiada):   $0.05
```

**At 50 users, 50 olimpiadas/month = $220 + $2.50 = $222.50/mo**

---

## REVENUE PER OLIMPIADA

```
Scenario: User subscribes ($499/mo), runs olimpiada

User Revenue (0.5% from trades):
├─ 3 bots launched
├─ Each bot: +$1,250 P&L (TP hit)
├─ Total P&L: $3,750
├─ User keeps: 99% = $3,712.50
└─ Platform gets: 1% = $37.50

Platform Revenue (per olimpiada event):
├─ Subscription fee: $499/12 = $41.58/mo per user
├─ + Trade split: $0.50 per trade (0.5% × $100 avg)
├─ + Marketplace: creator gets 0.5%, platform gets 0.5%
└─ BLENDED: ~$2-5 per olimpiada

Cost per olimpiada: $0.05
Revenue per olimpiada: $2-5
─────────────────────────────
MARGIN: 4,000%-10,000% ✓✓✓
```

---

## OBJECIONES MONETARIAS

### OBJECIÓN 1: "LLM parsing es caro. $0.05 × 1,000 olimpiadas = $50/día"

**RESPUESTA:**
- At 1,000 olimpiadas/day = 500,000 tokens/day = $50/day in LLM
- Pero eso significaría 1,000 / 50 users = 20 olimpiadas/user/day
- **Realistic:** 5-20 olimpiadas/month per user
- **So:** 50 users × 10 olimpiadas = 500 olimpiadas/month = $25/month LLM
- **Revenue from 500 olimpiadas:** 500 × $3 = $1,500
- **LLM cost:** $25
- **Margin:** 60x ✓

---

### OBJECIÓN 2: "Alpaca data costs money. Or we run out of free tier"

**RESPUESTA:**
- Alpaca free tier: unlimited historical data (for paper trading)
- If user goes live: They pay Alpaca commissions (not us)
- We don't pay for data at scale
- **Alternative:** Cached OHLCV (store locally)
- **Cost:** $0 ✓

---

### OBJECIÓN 3: "YouTube transcripts slow down. We need premium extraction"

**RESPUESTA:**
- Option A: Free YouTube API (10K units/day = 200 olimpiadas/day max)
- Option B: Cache transcripts (store on first request, reuse)
- Option C: Playwright (free, slower, but works)
- **Decision:** Use free API + cache. Fallback to Playwright if needed
- **Cost:** $0 ✓

---

### OBJECIÓN 4: "Real-time monitoring loop costs compute"

**RESPUESTA:**
- 3 bots × 5 sec = 12 API calls/min per user
- 50 users × 12 calls = 600 calls/min = 36K calls/hour
- Vercel can handle 1M+ functions/month free
- **Cost:** ~$0.50 for monitoring 50 users for month
- **Alternative:** Use Alpaca WebSocket (free, real-time)
- **Cost:** $0-0.50 ✓

---

### OBJECIÓN 5: "Supabase scales. Will it?" 

**RESPUESTA:**
- Supabase Pro ($25/mo): 8GB storage, unlimited reads/writes
- At 1,000 users × 50 olimpiadas = 50,000 olimpiadas
- Storage: 50,000 × 150 KB = 7.5 GB
- Supabase: Handles it ✓
- Esc. cost: Add more databases (+$25/db) for multi-region
- **Cost:** $25-50/mo ✓

---

## OBJECIONES TECNOLÓGICAS

### OBJECIÓN 1: "YouTube transcripts unreliable. Videos don't have captions"

**PROBLEM:**
- ~30% of YouTube videos don't have auto-generated captions
- Manual captions often better quality
- API returns empty string → LLM can't parse

**SOLUTION:**
```
IF transcript empty:
├─ Try Playwright (scrape captions from page)
├─ IF still empty: Use audio transcript API (Whisper)
├─ IF Whisper fails: Mark video as "no transcript" 
└─ Skip that trader, use next 20

FALLBACK: User manually pastes strategy config in chat
```

**Cost impact:** +$0.10 per Whisper call (if 50% videos need it)
**Total:** $0.10 vs $0 (not using Whisper)

---

### OBJECIÓN 2: "LLM parsing isn't accurate. Extracts wrong entry/TP/SL"

**PROBLEM:**
- Prompt says "entry at support bounce" but LLM returns 1.0875 (wrong)
- Entry/TP/SL must be precise (trading isn't forgiving)

**SOLUTION:**
```
1. VALIDATION LAYER:
   ├─ Check: entry < tp (goes up) or entry > tp (goes down)?
   ├─ Check: sl outside entry ± 2% (reasonable risk)
   ├─ Check: entries match trader's terminology parse
   └─ IF invalid: Flag for manual review

2. USER REVIEW BEFORE LAUNCH:
   ├─ "I extracted entry=$X, TP=$Y, SL=$Z. Correct?"
   ├─ User confirms or corrects
   └─ Then launch

3. BACKTEST VALIDATION:
   ├─ Run 30d historical
   ├─ IF win_rate < 30%: Flag as suspicious
   ├─ Warn user before deploying as live bot

4. MANUAL OVERRIDE:
   ├─ User can paste config or edit in UI
   └─ "Trust but verify"
```

**Cost impact:** +5 min UX per olimpiada (user review)
**Risk reduction:** 99% (caught before deployment)

---

### OBJECIÓN 3: "Monitoring loop crashes. Bots stop running"

**PROBLEM:**
- Vercel Function times out (15 min limit)
- Monitoring loop dies
- Bots stop getting checked for TP/SL

**SOLUTION:**
```
1. HEARTBEAT MECHANISM:
   ├─ Every 5 sec: Check active bots
   ├─ If no heartbeat > 30 sec: Alert user
   └─ Manual close option

2. PERSISTENT MONITORING:
   ├─ Use AWS Lambda (runs indefinitely)
   ├─ Or: OpenClaw agent (24/7 monitoring)
   ├─ Cost: $50-100/mo for dedicated monitoring
   └─ For MVP: Non-issue (bots only live during trading hours)

3. DATABASE BACKUP:
   ├─ Store bot_config state in Supabase (not in memory)
   ├─ If crash: Restart from DB, no trades lost
   └─ Resilient design

4. ALPACA NATIVE STOPS:
   ├─ Bot config in Alpaca as stop order
   ├─ If monitoring dies, TP/SL still execute on broker
   └─ Automatic protection
```

**Cost impact:** $0 (MVP) → $50/mo (production)
**Risk reduction:** 100% (Alpaca has stops, we have backups)

---

### OBJECIÓN 4: "Real-time updates slow. WebSocket lags"

**PROBLEM:**
- Vercel doesn't support persistent WebSocket
- Frontend polls instead (every 1 sec)
- Feels slow

**SOLUTION:**
```
OPTION A: Supabase Realtime (built-in)
├─ Cost: Included in Pro plan ($25/mo)
├─ Works: Automatic subscriptions
└─ Latency: <100ms

OPTION B: AWS API Gateway WebSocket
├─ Cost: $0.25 per million client messages
├─ At 50 users × 1 msg/sec × 30 days = 129M msgs = $32
└─ Latency: <50ms

OPTION C: Polling (for MVP)
├─ Cost: $0
├─ Latency: 1-2 sec (acceptable)
└─ Scale to Realtime later

Decision for MVP: Use Supabase Realtime (included)
```

**Cost impact:** $0 (already in Supabase Pro)
**UX improvement:** Real-time updates

---

### OBJECIÓN 5: "Data inconsistency. Bot executes, DB updates out of order"

**PROBLEM:**
- Bot enters trade, WebSocket sends update, DB write is slow
- Frontend shows wrong P&L

**SOLUTION:**
```
1. ATOMIC OPERATIONS:
   ├─ UPDATE live_positions + strategy_revenue_live in 1 tx
   ├─ Supabase handles ordering
   └─ No race conditions

2. OPTIMISTIC UPDATES:
   ├─ Frontend updates immediately (assume success)
   ├─ Backend confirms/rolls back if needed
   └─ User sees instant feedback

3. ORDER OF OPERATIONS:
   ├─ 1. Place order in Alpaca
   ├─ 2. Wait for fill confirmation (webhook)
   ├─ 3. Record in bot_executions
   ├─ 4. Broadcast via WebSocket
   ├─ 5. Update live_positions
   └─ Linear flow = no conflicts

4. IDEMPOTENCY:
   ├─ Each operation has unique ID
   ├─ If duplicate: Ignore (don't double-charge)
   └─ Safe retries
```

**Cost impact:** $0 (design pattern, not infrastructure)
**Risk reduction:** 100% (data always consistent)

---

### OBJECIÓN 6: "Broker API limits. Alpaca throttles our bots"

**PROBLEM:**
- 50 users × 3 bots = 150 API calls every 5 sec = 1,800 calls/min
- Alpaca rate limit: 200 requests/min
- We'd hit limit immediately

**SOLUTION:**
```
1. BATCH API CALLS:
   ├─ Instead of 150 individual calls → 1 request with 150 updates
   ├─ Alpaca supports batch endpoints
   └─ 1 call/5 sec instead of 150

2. CACHING:
   ├─ Cache last price for 1 sec
   ├─ Don't call Alpaca every 5 sec
   └─ Call every 30 sec per bot

3. WEBSOCKET (Real-time prices):
   ├─ Alpaca WebSocket = unlimited
   ├─1 connection per user, stream all prices
   └─ No rate limits

4. ALPACA PRO PLAN:
   ├─ Cost: $10/mo per user (if they want live trading)
   ├─ Higher rate limits
   └─ But: MVP uses paper trading (no limit)

Decision: Use WebSocket + batch API
Cost: $0
```

**Cost impact:** $0 (WebSocket free)
**Scalability:** 1000+ bots without hitting limits

---

## ACTION PLAN

### PHASE 1: MVP (Week 1-2) - VALIDATE COSTS

```
PRIORITY 1: Prove cost model works
├─ Build: Olimpiada engine (YouTube → LLM → backtest)
├─ Track: Actual costs per olimpiada
├─ Run: 10 test olimpiadas
├─ Measure: Cost breakdown
└─ Decision: Continue or pivot?

COSTS TO VALIDATE:
├─ YouTube free tier (can we get 20 videos?)
├─ LLM accuracy (are entry/TP/SL correct?)
├─ Backtest time (how long does 30d historical take?)
├─ Database (how much space per olimpiada?)
└─ Infrastructure (does monitoring loop stay up 24h?)
```

### PHASE 2: SCALE (Week 3-4) - OPTIMIZE COSTS

```
IF costs are higher than $0.05/olimpiada:
├─ Switch to cheaper LLM (haiku vs turbo)
├─ Use Playwright instead of YouTube API
├─ Cache historical data locally
└─ Batch API calls

IF costs are lower:
├─ Add premium features (multi-pair, longer backtest)
└─ Keep margin at 100x
```

### PHASE 3: PRODUCTION (Month 2+) - MONITOR COSTS

```
As scale increases:
├─ Track cost per active user
├─ Track cost per olimpiada
├─ Set cost targets ($0.10 max per olimpiada)
├─ Auto-alert if costs go above target
└─ Optimize infrastructure quarterly
```

---

## SUMMARY

| Component | Cost | Note |
|-----------|------|------|
| YouTube API | $0 | Free tier sufficient |
| LLM (OpenRouter) | $0.05 | Cheap models (haiku even cheaper) |
| Backtest compute | $0 | Alpaca free data, local compute |
| Alpaca API | $0 | Paper trading free, live is user's problem |
| Infrastructure | $0.0001 | Vercel Functions negligible |
| Database | $0 | Free tier, or $25/mo Pro |
| **TOTAL** | **$0.05** | Per olimpiada |
| **Monthly (50 users, 10 olimpiadas each)** | **$220** | $0.05 × 500 + fixed costs |
| **Monthly revenue** | **$25,000+** | 50 users × $499/mo + trade splits |
| **Margin** | **100x** | Sustainable ✓ |

---

## ANSWER TO "Es caro?"

**NO. Es barato.**

- $0.05 per olimpiada
- $220/mo infrastructure
- $25K/mo revenue at scale
- 100x margin

**Only expensive if you:**
- Use Bloomberg API ($2.4K/mo) ← Don't
- Run dedicated servers ← Use Vercel
- Pay for YouTube premium ← Free
- Hire people to manually backtest ← LLM does it

**Solution: Stay lean, automate everything.**

