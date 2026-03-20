# Mensaje para Nikita

Hola Nikita,

Aquí completo todo. Te explico cómo todo esto se interconecta para que la demo funcione.

---

## EL PRODUCTO V0 (Lo que vamos a lanzar)

Es simple: **traemos estrategias de YouTube → las ponemos a funcionar en vivo → compartimos earnings**.

**Fases del usuario:**

1. **Research Chat:** Preguntas sobre mercados (EUR/USD hoy, qué traders hablan de Bitcoin)
2. **Olimpiada:** "Dame 20 estrategias de traders YouTube EUR/USD" → Extraemos transcripciones → LLM parsea configs → Lanzamos 3 mejores COMO BOTS EN VIVO (paper trading Alpaca)
3. **Strategy Marketplace:** Browse estrategias que otros usuarios compartieron
4. **Monitor Live:** Ve bots ejecutando en tiempo real (entry → TP/SL close → P&L real)
5. **Monetize:** Su estrategia gana dinero cada vez que alguien la usa (+0.5%)

---

## ARQUITECTURA TÉCNICA (Cómo funciona detrás de escenas)

### Tech Stack V0
```
Frontend: Vercel (Next.js 16, React 19, Radix UI)
Backend: Node.js / FastAPI (Vercel Functions)
Database: Supabase PostgreSQL
LLM: OpenRouter (gpt-4-turbo-mini)
Search: Brave Search API
Paper Trading: Alpaca API (free sandbox)
Auth: Supabase Auth
```

### Database: 23 Tablas (Supabase)

**TIER 0: IDENTITY (Usuarios)**
```
users
├─ email, password, display_name
├─ tier (free/trader/pro)
├─ subscription_active, expires_at
├─ lifetime_earnings (total que han ganado)
└─ stripe_customer_id

user_preferences
├─ risk_percent, max_daily_loss
├─ theme, notifications
└─ auto_export_backtest
```

**TIER 1: CHAT & QUERIES (Investigación)**
```
conversations
├─ user_id, title, context_type
└─ archived, created_at

chat_messages
├─ conversation_id, role, content
├─ llm_model, tokens_used, api_cost
└─ response_time_ms

queries_log
├─ query_type, input_data, output_data
├─ status, error_message
└─ Para auditar qué preguntas hacen, cuáles funcionan mejor
```

**TIER 2: CSV & SWIPE (Lead Management)**
```
csv_imports
├─ filename, row_count, columns_detected
├─ parse_status
└─ data_sample

csv_rows
├─ csv_import_id, row_number, row_data
├─ swipe_action (accept/reject/duplicate)
└─ De dónde saca leads para outreach

swipe_actions
├─ user_id, csv_row_id, action
└─ Log de qué swiped el user
```

**TIER 3: OLIMPIADA (Competencia de bots)**
```
olimpiada_configs
├─ user_id, name, symbol (EUR/USD)
├─ timeframe, backtest_start_date, backtest_end_date
├─ traders_count, traders_list (JSON)
├─ backtest_results (JSON con rankings)
├─ status (pending/completed)
└─ Aquí guardamos cada "olimpiada" que crea el user
```

**TIER 4: STRATEGIES (Estrategias compartidas)**
```
strategies
├─ creator_user_id, creator_name, creator_avatar
├─ strategy_name, symbol, timeframe
├─ entry_logic, exit_logic, risk_management (JSON)
├─ stats (total_backtests, avg_win_rate, users_count, live_pnl)
├─ rating, reviews
├─ revenue_share_percent (0.5%)
├─ creator_earnings (cuánto ha ganado)
├─ status (published/draft/archived)
└─ El marketplace de estrategias

strategy_subscriptions
├─ user_id, strategy_id
├─ subscribed_at, activated_at
├─ custom_entry_offset, custom_tp_offset, custom_sl_offset
├─ custom_risk_percent (user puede tunear)
├─ status (saved/backtesting/deployed)
└─ Cuando un user "adopta" una estrategia

strategy_exports
├─ olimpiada_id, strategy_name, symbol
├─ entry_price, tp_price, sl_price
├─ strategy_rules (JSON con la config)
├─ backtest_win_rate, backtest_pnl
├─ visibility (private/shared/public)
├─ is_monetizable (¿genera ingresos?)
└─ De dónde sale la estrategia (olimpiada de ese user)
```

**TIER 5: REVENUE (Dinero)**
```
strategy_revenue
├─ strategy_id, user_id (trader), creator_id
├─ trade_pnl (ganancias de ese trade)
├─ creator_percent (0.5%), creator_earnings
├─ platform_percent (0.5%), platform_earnings
├─ Cuando se cierra un bot (TP o SL), se registra aquí
└─ Todo real, no backtest estimado

subscription_payments
├─ user_id, amount, tier
├─ stripe_payment_id, status
└─ Pagos de los $499/mes

creator_payouts
├─ creator_id, amount, period (mes)
├─ status (pending/paid)
├─ stripe_payout_id
└─ Pago a creadores cada mes
```

**TIER 6: COMMUNITY (Compartir)**
```
community_groups
├─ group_name, external_id, external_type
├─ is_private, description
└─ Discord groups, Telegram, etc

community_members
├─ user_id, community_id, role
└─ Quién participa en qué grupo

olimpiada_shares
├─ olimpiada_id, shared_by_user_id
├─ share_type, shared_with_user_ids
├─ share_link, link_expires_at
└─ Viral sharing del olimpiada
```

**TIER 7: AUDIT (Logging)**
```
action_log
├─ user_id, action_type, resource_type, resource_id
├─ action_metadata (JSON)
└─ Auditoría: qué hizo quién

audit_logs
├─ event_type, event_severity
├─ event_description, event_data
├─ ip_address, user_agent
└─ Seguridad: logins, cambios de config, etc
```

**TIER 8: REAL-TIME BOT EXECUTION (NEW - core de V0)**
```
bot_configs
├─ user_id, strategy_id (si viene de marketplace)
├─ bot_name, symbol (EUR/USD)
├─ entry_price, tp_price, sl_price, risk_percent
├─ source_type (youtube_transcript/natural_language/olimpiada/manual)
├─ status (deployed/waiting/executing/closed)
├─ alpaca_account_id (paper trading account)
├─ revenue_share_percent (0.5-1%)
└─ La configuración de CADA bot activo

bot_executions
├─ bot_config_id, user_id, strategy_id
├─ symbol, side (buy/sell), qty
├─ entry_price, entry_time, alpaca_order_id
├─ exit_price, exit_time, close_reason (tp_hit/sl_hit/manual)
├─ pnl, pnl_percent
└─ Cada trade que ejecutó el bot (entry → exit)

live_positions
├─ bot_config_id, user_id
├─ symbol, entry_price, current_price
├─ unrealized_pnl, unrealized_pnl_percent
├─ status (open/closing)
├─ updated_at (live updates)
└─ Posiciones abiertas AHORA (real-time)

strategy_revenue_live
├─ strategy_id, bot_config_id, user_id, creator_id
├─ trade_pnl (REAL, no backtest)
├─ creator_percent (0.5%), creator_earnings
├─ platform_earnings
├─ trade_closed_at, logged_at
└─ Revenue split INMEDIATO cuando se cierra un trade
```

---

## FLUJO EN VIVO (User Journey)

### Paso 1: Investigación (Chat)
```
User: "EUR/USD hoy, qué traders hablan de bounce en soporte?"

Backend:
├─ Brave Search: EUR/USD + soporte + bounce
├─ LLM analyze: Sintetiza resultados
├─ Costo: $0.01
└─ Reply: "3 setups posibles, win rate histórico 65%"

DB write:
├─ queries_log: user_id, query_type, input, output, cost
└─ Auditar qué busca, para mejorar
```

### Paso 2: Olimpiada (YouTube Extraction)
```
User: "Dame 20 traders EUR/USD en YouTube"

Backend:
├─1. YouTube search (API free tier)
├─2. Download transcripts (captions)
├─3. LLM extrae 20 estrategias (JSON):
│   │  {
│   │    "trader": "Trader XYZ",
│   │    "entry": 1.0875,
│   │    "tp": 1.0750,
│   │    "sl": 1.0950,
│   │    "win_rate": 0.68,
│   │    "logic": "soporte + bounce + volume"
│   │  },
│   │  ...
│   │
├─4. Backtest histórico (30 días, 2000 bars)
├─5. Rank por win_rate (mejor a peor)
└─6. Costo total: ~$0.20

Resultado:
├─ Trader A: 68% win rate, +$3,240 P&L
├─ Trader B: 65% win rate, +$2,850
└─ Trader C: 62% win rate, +$2,100

DB write:
├─ olimpiada_configs: user_id, name="EUR/USD Olimpiada", traders_list (JSON), results
├─ strategy_exports: 3 entries (para los top 3)
└─ strategies: 3 entries (si marcan como public/monetizable)
```

### Paso 3: Launch Bots (Auto-Deploy Real-Time)
```
User: "Lanza los 3 mejores como bots"

Backend:
├─1. Create 3 bot_configs (entry=1.0875, tp=1.0750, sl=1.0950, etc)
├─2. Start monitoring loop (every 5 sec):
│   │  FOR EACH bot_config:
│   │  ├─ Get current price (Alpaca WebSocket)
│   │  ├─ IF price <= entry_price: Place limit order
│   │  ├─ IF order filled: Insert bot_executions (entry)
│   │  ├─ Monitor TP/SL
│   │  ├─ IF price >= TP: Close order (market), log exit
│   │  ├─ IF price <= SL: Close order (market), log exit
│   │  └─ Insert strategy_revenue_live (split calculated)
│   │
├─3. WebSocket to frontend: "Bot A: Entry pending", "Bot B: Entry executed", etc
└─4. Notifications: "✅ Entry executed! EUR/USD @ 1.0875"

User see:
├─ 🤖 Bot A: MONITORING entry
├─ 🤖 Bot B: POSITION OPEN, +$150 unrealized
├─ 🤖 Bot C: WAITING FOR ENTRY
└─ [Real-time P&L dashboard]

Bot A closes (TP hit):
├─ Exit: 1.0750, profit: +$1,250
├─ Creator earnings (0.5%): +$6.25
├─ Creator notification: "Your strategy made $6.25 this trade"
└─ User notification: "TP HIT! +$1,250"

DB writes:
├─ bot_executions: entry, exit, pnl (x3 bots)
├─ live_positions: closed (remove or mark closed)
├─ strategy_revenue_live: Creator earnings tracked
└─ strategies: stats updated (users_count++, live_pnl += 1250)
```

### Paso 4: Marketplace
```
User sees 100+ strategies:
├─ EUR/USD (65+ strategies, avg rating 4.2)
├─ GBP/USD (40+ strategies, avg rating 4.0)
└─ Gold (25+ strategies, avg rating 3.8)

Click "EUR/USD Strategy by Trader XYZ":
├─ Name: "Soporte + Bounce"
├─ Creator: Trader XYZ (11K followers)
├─ Rating: 4.5 ⭐ (128 reviews)
├─ Backtest (30d): 68% win rate, +$3,240
├─ Users using: 17
├─ This month earnings: +$105 (17 users × $6 average per user)
│
├─ [Test on MY data] → Backtest with user's own data
├─ [Subscribe] $0/mo (embedded in tier), revenue share active
└─ After subscribe: Auto can launch as bot or manual config

DB reads:
├─ strategies: strategy_id, stats, rating, creator_earnings
├─ strategy_subscriptions: Is user already subscribed?
├─ strategy_revenue_live: Creator's lifetime earnings
└─ bot_executions: Historical trades for this strategy
```

### Paso 5: Creator Dashboard
```
Creator sees:
├─ Strategy: "Soporte + Bounce"
├─ Subscribers: 17 users
├─ Active bots: 5 running now
├─ This month earnings: +$105
├─ Breakdown: 
│  ├─ User A: +$12 (2 trades)
│  ├─ User B: +$8 (1 trade)
│  └─ etc
├─ Payout: $105 pending (next month)
└─ Payout history: [Feb: +$85], [Jan: +$120]

All auto-calculated from strategy_revenue_live
```

---

## API ENDPOINTS (Backend to Frontend)

```
CHAT & RESEARCH:
POST /api/chat/message
├─ Input: {message, conversation_id}
├─ Output: {response, cost, tokens_used}
└─ Logs to: chat_messages, queries_log

POST /api/research/analyze
├─ Input: {query, topic}
└─ Output: {analysis, sources, cost}

OLIMPIADA:
POST /api/olimpiada/create
├─ Input: {symbol, num_traders, timeframe}
├─ Output: {olimpiada_id, results}
└─ Logs to: olimpiada_configs, strategy_exports, strategies

POST /api/olimpiada/launch-bots
├─ Input: {olimpiada_id, bot_count (default 3)}
├─ Output: {bot_ids[], status}
└─ Creates: bot_configs (x3), starts monitoring

BOTS (Real-Time):
GET /api/bots/live/:bot_id
├─ Output: {symbol, entry, tp, sl, current_price, unrealized_pnl, status}
└─ WebSocket: Subscribe for live updates

GET /api/bots/executions/:bot_id
├─ Output: [{entry_price, exit_price, pnl, entry_time, exit_time}, ...]
└─ All trades for this bot

POST /api/bots/close/:bot_id
├─ Manually close bot
└─ Logs to: bot_executions

STRATEGY MARKETPLACE:
GET /api/marketplace/strategies
├─ Query: {symbol, min_rating, sort_by}
└─ Output: [{strategy_id, name, creator, rating, users_count}, ...]

POST /api/strategy/subscribe
├─ Input: {strategy_id}
├─ Output: {subscription_id, status}
└─ Logs to: strategy_subscriptions

GET /api/strategy/revenue/live/:creator_id
├─ Output: {total_this_month, users, trades, breakdown}
└─ Reads: strategy_revenue_live (real-time)

TIER & PAYMENT:
POST /api/tier/upgrade
├─ Input: {new_tier} (free/trader/pro)
├─ Output: {subscription_active, expires_at}
└─ Integrates with Stripe

GET /api/creator/earnings/:creator_id
├─ Output: monthly breakdown, pending payout, history
```

---

## ENVIRONMENT VARIABLES (.env)

```
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://<project>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<anon_key>
SUPABASE_SERVICE_ROLE_KEY=<service_role_key>

# LLM
OPENROUTER_API_KEY=<key>
OPENROUTER_MODEL=gpt-4-turbo-mini

# APIs
BRAVE_SEARCH_API_KEY=<key>
YOUTUBE_API_KEY=<key>
ALPACA_API_KEY=<key>
ALPACA_SECRET_KEY=<key>
ALPACA_BASE_URL=https://paper-api.alpaca.markets  # Paper trading

# Stripe
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=<key>
STRIPE_SECRET_KEY=<key>
STRIPE_WEBHOOK_SECRET=<key>

# WebSocket (real-time)
NEXT_PUBLIC_WEBSOCKET_URL=wss://<your-server>/ws

# URLs
NEXT_PUBLIC_API_URL=https://<your-domain>/api
NEXT_PUBLIC_APP_URL=https://<your-domain>
```

---

## TIMELINE & MILESTONES

```
WEEK 1: Auth + Chat + Research
├─ Login/signup (Supabase Auth)
├─ Chat interface (Vercel + React)
├─ Research agent (BraveSearch + LLM)
└─ Cost: $0.01 per query

WEEK 2: Olimpiada + Real-time Bots
├─ YouTube extraction (transcripts)
├─ LLM strategy parsing
├─ Monitoring loop (Alpaca paper trading)
├─ Live P&L updates (WebSocket)
└─ Launch 3 bots simultaneously

WEEK 3: UI + Stripe + Marketplace
├─ Marketplace UI (browse strategies)
├─ Stripe integration (3 tiers: $0, $499, $1,999)
├─ Strategy detail page (backtest, subscribe)
├─ Creator dashboard
└─ Revenue tracking dashboard

WEEK 4: Polish + Launch
├─ Bug fixes, performance
├─ Edge case handling
├─ Documentation
├─ Go live
└─ Launch: End of Week 4

MONTH 2-3: Traction
├─ Twitter outreach (500 traders)
├─ YouTube collaborations
├─ Product Hunt launch
├─ Target: 50 paid users = $25K/mo
```

---

## PRECIOS (Tiers)

```
FREE
├─ 1 olimpiada/mes
├─ 5 research queries/día
├─ No marketplace access
└─ $0/mo

TRADER ($499/mes)
├─ 20 olimpiadas/mes
├─ Unlimited research
├─ Full marketplace access
├─ Create + monetize strategies (0.5% revenue share)
├─ Live bot deployment (3 at a time)
└─ Creator dashboard

PRO ($1,999/mes)
├─ Unlimited olimpiadas
├─ Unlimited research  
├─ Unlimited bots
├─ Priority support
├─ Early access to OPENCLAW
└─ All features
```

---

## SUCCESS METRICS (First 3 months)

```
MONTH 1:
├─ 100+ signups
├─ 20 free users (testing)
├─ 0 paid (validating)

MONTH 2:
├─ 250+ total signups
├─ 50 free users
├─ 10-20 paid ($5K-10K MRR)
├─ 50+ bots deployed
└─ 5+ live creators

MONTH 3:
├─ 500+ total signups
├─ 100+ free users
├─ 50+ paid ($25K+ MRR)
├─ 200+ bots deployed
├─ 20+ live creators
└─ Marketplace: $30K+ traded via strategies
```

---

## NEXT STEPS

**For you (Nikita):**
1. Define research doc structure (template for daily findings)
2. Start daily research docs (feed insights into system)
3. Test 5 strategies manually on Alpaca sandbox (validate quality)
4. Create QA checklist (what makes a strategy "good"?)

**For Marc (CTO):**
1. Deploy Supabase schema (SQL script ready)
2. Build backend: /api/chat, /api/olimpiada, /api/bots/*, /api/marketplace/*
3. Integrate Alpaca paper trading (monitoring loop + order execution)
4. Frontend: 4 pages + WebSocket real-time updates

**For David (if involved):**
- Prepare outreach emails (500 traders)
- List YouTube channels to collaborate with
- Plan Product Hunt launch

---

## TL;DR

The whole system is **3 value loops:**

1. **Research Loop:** Chat + LLM → User makes better trades
2. **Olimpiada Loop:** YouTube → Extract → Test → Launch → Watch live
3. **Marketplace Loop:** Winners share → Creators earn passive → More winners join

All powered by real-time paper trading.**No simulation.** Real execution. Real P&L. Real revenue split.

Database tracks **everything:** Every message, every strategy, every trade, every dollar earned.

Clean, simple, scalable.

Vercel hosting → Supabase DB → Alpaca paper account → OpenRouter LLM = **full product for $1.2K/mo infra, generating $25K/mo revenue Month 3.**

---

**Ready to ship.** 🚀

