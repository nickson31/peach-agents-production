# Mensaje para Marc — Base de Datos Completa (Demo V0 + OpenClaw)

---

Bro, aquí tienes la base de datos completa y bien explicada en Supabase para la demo sin OpenClaw. Lo explico todo bien. Y después, para la migración a OpenClaw, te digo la estrategia: guardaremos algunos .md pero reescribiremos toda la DB porque OpenClaw en nuestra app (AWS) ya tiene muy buena gestión de memoria.

---

## PARTE 1: DEMO V0 (SUPABASE - 4 SEMANAS)

### El Producto

La demo es un MVP: backtest tool + marketplace de estrategias + comunidad compartida. NO hay ejecución real, NO hay 24/7 monitoring. El usuario:

1. Ve investigación en vivo (BraveSearch)
2. Crea "olimpiadas de bots" (descarga transcripciones de YouTube, LLM extrae estrategias, backtest histórico)
3. Swipea leads (CSV upload)
4. Descubre estrategias en marketplace
5. Backtest en sus datos
6. Monetiza su estrategia (0.5-1% de ganancias simuladas)

Meta: 50 usuarios pagando $499/mes = $24.5K/mes dentro de 4 semanas. Eso genera suficiente dinero + $20K inversión para pagar 2 meses de tu desarrollo en OpenClaw.

### Stack V0

```
Frontend: Vercel (Next.js 16, React 19, Radix UI, Tailwind)
Backend: Node.js / Python FastAPI (Vercel Functions)
Database: Supabase PostgreSQL (hosted)
LLM: OpenRouter (gpt-4-turbo-mini)
Search: Brave Search API
YouTube: YouTube Data API
Auth: Supabase Auth

Costos:
├─ Supabase: $25/mo (free → pro cuando crezcamos)
├─ Vercel: $20/mo
├─ OpenRouter: $1K/mo (LLM calls)
├─ Brave Search: $100/mo
├─ TOTAL: ~$1.2K/mo infra
└─ GANANCIA: $25K/mo - $1.2K infra = $23.8K neto (before Stripe fees)
```

### Schema Supabase (13 Tablas)

**TIER 0: IDENTITY**

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  display_name VARCHAR(255),
  avatar_url VARCHAR(510),
  tier VARCHAR(50) DEFAULT 'free',  -- 'free', 'trader' ($499), 'pro' ($1999)
  subscription_active BOOLEAN DEFAULT false,
  subscription_expires_at TIMESTAMP,
  timezone VARCHAR(50) DEFAULT 'UTC',
  language VARCHAR(10) DEFAULT 'es',
  currency VARCHAR(10) DEFAULT 'USD',
  risk_default DECIMAL(3,1) DEFAULT 1.5,
  total_olimpiadas INT DEFAULT 0,
  total_strategies_created INT DEFAULT 0,
  lifetime_earnings DECIMAL(15,2) DEFAULT 0,
  stripe_customer_id VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  last_login_at TIMESTAMP,
  INDEX idx_email (email),
  INDEX idx_tier (tier),
  INDEX idx_created_at (created_at)
);

CREATE TABLE user_preferences (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  risk_percent DECIMAL(3,1) DEFAULT 1.5,
  max_daily_loss DECIMAL(5,2) DEFAULT 5.0,
  theme VARCHAR(50) DEFAULT 'dark',
  notify_new_strategies BOOLEAN DEFAULT true,
  notify_earnings BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW(),
  INDEX idx_user_id (user_id)
);
```

**TIER 1: CHAT & QUERIES**

```sql
CREATE TABLE conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255),
  context_type VARCHAR(50) DEFAULT 'general',
  context_data JSONB,
  is_archived BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT NOW(),
  last_message_at TIMESTAMP,
  INDEX idx_user_id (user_id),
  INDEX idx_context_type (context_type),
  INDEX idx_last_message_at (last_message_at)
);

CREATE TABLE chat_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  role VARCHAR(20) NOT NULL,  -- 'user', 'assistant'
  content TEXT NOT NULL,
  audio_url VARCHAR(510),
  audio_duration_seconds INT,
  llm_model VARCHAR(100),
  tokens_used INT,
  api_cost DECIMAL(10,6),
  response_time_ms INT,
  is_error BOOLEAN DEFAULT false,
  error_message TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  INDEX idx_conversation_id (conversation_id),
  INDEX idx_role (role),
  INDEX idx_created_at (created_at)
);

CREATE TABLE queries_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  query_type VARCHAR(50) NOT NULL,  -- 'research', 'olimpiada', 'strategy_analysis'
  input_data JSONB,
  output_data JSONB,
  llm_model VARCHAR(100),
  tokens_used INT,
  api_cost DECIMAL(10,6),
  response_time_ms INT,
  status VARCHAR(50) DEFAULT 'completed',
  error_message TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP,
  INDEX idx_user_id (user_id),
  INDEX idx_query_type (query_type),
  INDEX idx_status (status),
  INDEX idx_created_at (created_at)
);
```

**TIER 2: CSV & SWIPE (Lead Gen)**

```sql
CREATE TABLE csv_imports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  filename VARCHAR(255) NOT NULL,
  file_size_bytes INT,
  row_count INT,
  column_count INT,
  columns_detected TEXT[],
  parse_status VARCHAR(50) DEFAULT 'pending',
  parse_error TEXT,
  data_sample JSONB,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP,
  INDEX idx_user_id (user_id),
  INDEX idx_parse_status (parse_status)
);

CREATE TABLE csv_rows (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  csv_import_id UUID NOT NULL REFERENCES csv_imports(id) ON DELETE CASCADE,
  row_number INT NOT NULL,
  row_data JSONB NOT NULL,
  swipe_action VARCHAR(20),  -- 'like', 'dislike'
  swiped_at TIMESTAMP,
  is_duplicate BOOLEAN DEFAULT false,
  is_valid BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW(),
  INDEX idx_csv_import_id (csv_import_id),
  INDEX idx_swipe_action (swipe_action),
  UNIQUE KEY unique_row (csv_import_id, row_number)
);

CREATE TABLE swipe_actions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  csv_row_id UUID NOT NULL REFERENCES csv_rows(id) ON DELETE CASCADE,
  action VARCHAR(20) NOT NULL,
  reason TEXT,
  swiped_at TIMESTAMP DEFAULT NOW(),
  INDEX idx_user_id (user_id),
  INDEX idx_action (action)
);
```

**TIER 3: OLIMPIADA**

```sql
CREATE TABLE olimpiada_configs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  topic VARCHAR(255),
  symbol VARCHAR(50) NOT NULL,
  timeframe VARCHAR(10),
  backtest_start_date DATE,
  backtest_end_date DATE,
  data_period_days INT,
  traders_count INT,
  traders_list JSONB,  -- [{name, video_url, transcript_url}]
  backtest_results JSONB,  -- [{rank, trader_name, win_rate, pnl, config}]
  status VARCHAR(50) DEFAULT 'pending',
  error_message TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  INDEX idx_user_id (user_id),
  INDEX idx_status (status),
  INDEX idx_symbol (symbol)
);
```

**TIER 4: STRATEGIES & MARKETPLACE**

```sql
CREATE TABLE strategies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  creator_user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  creator_name VARCHAR(255),
  creator_avatar VARCHAR(510),
  strategy_name VARCHAR(255) NOT NULL,
  strategy_version INT DEFAULT 1,
  source_type VARCHAR(50),  -- 'youtube_transcript', 'olimpiada_winner', 'user_upload'
  source_reference JSONB,
  symbol VARCHAR(50) NOT NULL,
  timeframe VARCHAR(10) NOT NULL,
  entry_logic JSONB,  -- {trigger, conditions, entry_price}
  exit_logic JSONB,   -- {tp_price, sl_price}
  risk_management JSONB,  -- {risk_percent, max_positions, max_daily_loss}
  stats JSONB DEFAULT '{"total_backtests": 0, "avg_win_rate": 0, "users_count": 0}'::jsonb,
  rating DECIMAL(3,2),
  rating_count INT DEFAULT 0,
  reviews TEXT[],
  revenue_share_percent DECIMAL(3,2) DEFAULT 0.5,  -- 0.5% o 1.0%
  creator_earnings DECIMAL(15,2) DEFAULT 0,
  status VARCHAR(50) DEFAULT 'published',
  is_open_to_new_users BOOLEAN DEFAULT true,
  description TEXT,
  tags TEXT[],
  disclaimers TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  published_at TIMESTAMP,
  INDEX idx_creator_user_id (creator_user_id),
  INDEX idx_symbol (symbol),
  INDEX idx_status (status),
  INDEX idx_rating (rating DESC)
);

CREATE TABLE strategy_subscriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  strategy_id UUID NOT NULL REFERENCES strategies(id) ON DELETE CASCADE,
  subscribed_at TIMESTAMP DEFAULT NOW(),
  activated_at TIMESTAMP,
  custom_entry_offset DECIMAL(5,3),
  custom_tp_offset DECIMAL(5,3),
  custom_sl_offset DECIMAL(5,3),
  custom_risk_percent DECIMAL(3,1),
  status VARCHAR(50) DEFAULT 'saved',  -- 'saved', 'backtesting'
  backtest_data JSONB,  -- {win_rate, pnl, num_trades, max_drawdown, tested_at}
  notes TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE KEY unique_user_strategy (user_id, strategy_id),
  INDEX idx_user_id (user_id),
  INDEX idx_strategy_id (strategy_id),
  INDEX idx_status (status)
);

CREATE TABLE strategy_exports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  olimpiada_id UUID REFERENCES olimpiada_configs(id) ON DELETE CASCADE,
  strategy_name VARCHAR(255),
  source_trader_name VARCHAR(255),
  symbol VARCHAR(50),
  timeframe VARCHAR(10),
  entry_price DECIMAL(10,5),
  tp_price DECIMAL(10,5),
  sl_price DECIMAL(10,5),
  strategy_rules JSONB,
  backtest_win_rate DECIMAL(5,2),
  backtest_pnl DECIMAL(15,2),
  backtest_num_trades INT,
  visibility VARCHAR(50) DEFAULT 'private',  -- 'private', 'friends', 'community'
  shared_with_user_ids UUID[],
  shared_in_community_ids UUID[],
  is_monetizable BOOLEAN DEFAULT false,
  creator_id UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  INDEX idx_olimpiada_id (olimpiada_id),
  INDEX idx_visibility (visibility)
);
```

**TIER 5: REVENUE**

```sql
CREATE TABLE strategy_revenue (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  strategy_id UUID NOT NULL REFERENCES strategies(id),
  user_id UUID NOT NULL REFERENCES users(id),
  creator_id UUID NOT NULL REFERENCES users(id),
  trade_pnl DECIMAL(15,2),
  trade_date TIMESTAMP,
  creator_percent DECIMAL(5,2),
  creator_earnings DECIMAL(15,2),
  platform_percent DECIMAL(5,2),
  platform_earnings DECIMAL(15,2),
  is_settled BOOLEAN DEFAULT false,
  settled_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  INDEX idx_strategy_id (strategy_id),
  INDEX idx_creator_id (creator_id),
  INDEX idx_is_settled (is_settled)
);

CREATE TABLE subscription_payments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  amount DECIMAL(15,2) NOT NULL,
  currency VARCHAR(10) DEFAULT 'USD',
  tier VARCHAR(50),
  stripe_payment_id VARCHAR(255),
  status VARCHAR(50),
  created_at TIMESTAMP DEFAULT NOW(),
  processed_at TIMESTAMP,
  INDEX idx_user_id (user_id),
  INDEX idx_status (status)
);

CREATE TABLE creator_payouts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  creator_id UUID NOT NULL REFERENCES users(id),
  amount DECIMAL(15,2) NOT NULL,
  currency VARCHAR(10) DEFAULT 'USD',
  period_start DATE,
  period_end DATE,
  status VARCHAR(50) DEFAULT 'pending',
  bank_account_id VARCHAR(255),
  stripe_payout_id VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW(),
  paid_at TIMESTAMP,
  INDEX idx_creator_id (creator_id),
  INDEX idx_status (status)
);
```

**TIER 6: COMMUNITY**

```sql
CREATE TABLE community_groups (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  group_name VARCHAR(255),
  external_id VARCHAR(255),  -- Telegram group ID, Discord server ID
  external_type VARCHAR(50),
  is_private BOOLEAN DEFAULT true,
  description TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  INDEX idx_external_id (external_id)
);

CREATE TABLE community_members (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  community_id UUID NOT NULL REFERENCES community_groups(id) ON DELETE CASCADE,
  role VARCHAR(50) DEFAULT 'member',
  joined_at TIMESTAMP DEFAULT NOW(),
  UNIQUE KEY unique_user_community (user_id, community_id),
  INDEX idx_user_id (user_id),
  INDEX idx_community_id (community_id)
);

CREATE TABLE olimpiada_shares (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  olimpiada_id UUID REFERENCES olimpiada_configs(id),
  shared_by_user_id UUID REFERENCES users(id),
  share_type VARCHAR(50),
  shared_with_user_ids UUID[],
  community_id UUID REFERENCES community_groups(id),
  share_link VARCHAR(255) UNIQUE,
  link_expires_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  INDEX idx_olimpiada_id (olimpiada_id),
  INDEX idx_share_link (share_link)
);
```

**TIER 7: AUDIT**

```sql
CREATE TABLE action_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  action_type VARCHAR(100) NOT NULL,
  resource_type VARCHAR(50),
  resource_id UUID,
  action_metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  INDEX idx_user_id (user_id),
  INDEX idx_action_type (action_type)
);

CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  event_type VARCHAR(100) NOT NULL,
  event_severity VARCHAR(50),
  event_description TEXT,
  event_data JSONB,
  ip_address VARCHAR(50),
  user_agent VARCHAR(510),
  created_at TIMESTAMP DEFAULT NOW(),
  INDEX idx_event_type (event_type),
  INDEX idx_created_at (created_at)
);
```

### Flujo Usuario V0

```
USER FINDS APP → "Racha: Trading Strategy Olympiad"

1. SIGNUP
   └─ Email + password (Supabase Auth)
   └─ Free tier (1 olimpiada, 5 research queries/day)

2. CHAT (Research Agent)
   └─ "Analiza EUR/USD hoy"
   └─ System: BraveSearch + LLM
   └─ Response: Macro context, setups, sentiment
   └─ Cost: $0.01 per query

3. OLIMPIADA
   └─ "Busca 20 traders EUR/USD en YouTube"
   └─ System:
      ├─ YouTube search
      ├─ Transcripts extraction
      ├─ LLM: Extract 20 strategies
      ├─ Backtest: 30 días datos históricos
      └─ Results: Ranking, P&L, win rate
   └─ Cost: $0.20 per olimpiada

4. MARKETPLACE
   └─ Browse 100+ estrategias
   └─ Filter: Win rate, users, revenue share
   └─ Click: "Backtest on my data"
   └─ System: Test 30 days histórico
   └─ Results: 68% win rate, +$3,240

5. SUBSCRIBE & MONETIZE
   └─ "Voy a comprar $499/mes"
   └─ Now: 20 olimpiadas/mes + unlimited research
   └─ Also: Can list his own strategy
   └─ Revenue: 0.5% of all trades using his strategy

6. EARNINGS DASHBOARD
   └─ "50 traders using my strategy"
   └─ "This month: +$2,500 (50 × $50 avg trade)"
   └─ Payout: Monthly via Stripe
   └─ Completely passive
```

### API Endpoints V0

```
POST /api/chat/message
├─ Input: {message}
├─ LLM: Parse intent (research, olimpiada, etc)
└─ Response: {answer, cost}

POST /api/research/analyze
├─ Input: {query, topic}
├─ BraveSearch + LLM
└─ Response: {analysis, sources}

POST /api/olimpiada/create
├─ Input: {symbol, timeframe, num_traders}
├─ YouTube search + LLM parse + backtest
└─ Response: {results, rankings}

POST /api/olimpiada/share
├─ Input: {olimpiada_id, share_type}
├─ Share link OR friends OR community
└─ Response: {share_link, shared}

GET /api/marketplace/strategies
├─ Query: {symbol, min_win_rate, sort_by}
└─ Response: [{strategy}, ...]

POST /api/strategy/backtest
├─ Input: {strategy_id, period}
├─ Run backtest on user's historical data
└─ Response: {win_rate, pnl, trades}

POST /api/strategy/subscribe
├─ Input: {strategy_id}
├─ Add to library
└─ Response: {subscription_id}

GET /api/creator/earnings
├─ Dashboard: Monthly earnings
└─ Response: {revenue, users, breakdown}

POST /api/tier/upgrade
├─ Input: {new_tier}
├─ Stripe payment
└─ Response: {subscription_active}
```

### Environment Variables V0

```
NEXT_PUBLIC_SUPABASE_URL=https://<project>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<anon_key>
SUPABASE_SERVICE_ROLE_KEY=<service_role_key>

OPENROUTER_API_KEY=<key>
BRAVE_SEARCH_API_KEY=<key>
YOUTUBE_API_KEY=<key>

NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=<key>
STRIPE_SECRET_KEY=<key>
STRIPE_WEBHOOK_SECRET=<key>

NEXT_PUBLIC_API_URL=http://localhost:3000
```

### Deployment V0

- **Frontend:** Vercel (auto-deploy from GitHub)
- **Database:** Supabase PostgreSQL (managed)
- **Functions:** Vercel Serverless (API routes)
- **Storage:** Supabase Storage (CSV uploads)
- **Payments:** Stripe (subscription management)

---

## PARTE 2: ESTRATEGIA OPENCLAW (REESCRITURA TOTAL, NO MIGRACIÓN)

Ahora viene lo importante: **NO vamos a migrar la base de datos V0 a OpenClaw**. V0 es temporal (3-6 meses), OPENCLAW es permanente. Guardamos algunos .md para documentación histórica, pero **reescribimos TODO en PostgreSQL**. ¿Por qué?

1. **Supabase = shared infrastructure, limits**. OpenClaw en tu AWS = full control, mejor memory management
2. **V0 schema = backtest results, simulación**. OPENCLAW schema = live execution, real trades
3. **Clean slate = mejor performance**. No llevar bagaje de V0

OpenClaw en tu AWS tiene gestión de memoria excelente. Vamos a aprovecharla.

### Timeline Paralela

```
SEMANA 1-4: TÚ CONSTRUYES V0 (4 semanas)
└─ Vercel + Supabase, generas $25K MRR

SEMANA 5-12 PARALELA: MARC CONSTRUYE OPENCLAW (8 semanas)
├─ PostgreSQL en tu AWS
├─ OpenClaw agent framework
├─ Hardware pairing system
├─ Mobile app (React Native)
└─ Funded by V0 revenue + $20K investment

MES 3: SOFT LAUNCH
├─ V0: Still making $25K/mo (50 users)
├─ OPENCLAW: Beta (20 users testing)
├─ Two products, two databases, zero overlap
└─ De-risk: If OPENCLAW fails, V0 keeps printing money

MES 4+: FULL OPENCLAW LAUNCH
├─ Archive V0 Supabase database
├─ OPENCLAW production
├─ User migration incentives (not forced)
└─ Scale to $100K+/mo
```

### ¿Qué Guardamos de V0?

```
.md files to keep (for historical reference):
├─ ARCHITECTURE.md (strategy overview)
├─ DATABASE_V0.md (V0 schema reference)
├─ DB_V0_COMPLETE_FOR_MARC.md (SQL script)
├─ DEMO_V0_STRATEGY.md (business logic)
├─ STRATEGY_SHARING_MODEL.md (marketplace concept)
└─ AGENT_CONFIG_CUSTOMIZATION.md (config patterns)

DATABASE:
├─ Keep: Supabase backup (final snapshot)
├─ Export: All user data as CSV (users, olimpiadas, strategies)
├─ Archive: To S3 or cold storage (compliance + historical)
└─ Delete: After 1 month post-launch OPENCLAW (optional)

IMPORTANT:
└─ NO DATA MIGRATION to PostgreSQL
└─ NO SQL conversion V0 → OPENCLAW
└─ OPENCLAW starts fresh (new users create new accounts)
└─ V0 users can opt-in to OPENCLAW beta (separate login)
```

### OPENCLAW Schema (PostgreSQL - AWS, Nuevo)

Esto se reescribe completamente. Different tables, different structure, different purpose.

**CORE EXECUTION (Live Trading)**

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP,
  tier VARCHAR(50),  -- 'free', 'starter', 'pro', 'enterprise'
  subscription_active BOOLEAN,
  -- [Different structure from V0, optimized for live execution]
);

CREATE TABLE strategies (
  id UUID PRIMARY KEY,
  creator_id UUID,
  strategy_name VARCHAR(255),
  -- [Includes agent_template (OpenClaw config)]
  -- [NOT backtest results, just the definition]
);

CREATE TABLE agent_configs (
  id UUID PRIMARY KEY,
  strategy_id UUID,
  user_id UUID,
  deployment_config JSONB,  -- Cloud vs Hardware config
  status VARCHAR(50),  -- deployed, monitoring, executing
  openclaw_agent_id VARCHAR(255),
  -- [Result of user deploying strategy]
  -- [Either on cloud ($45/mo) or hardware (free)]
);

CREATE TABLE agent_execution_logs (
  id UUID PRIMARY KEY,
  agent_config_id UUID,
  event_type VARCHAR(50),  -- heartbeat, entry_trigger, tp_hit, sl_hit
  event_data JSONB,
  execution_time_ms INT,
  created_at TIMESTAMP,
  -- [Every agent action logged]
);

CREATE TABLE live_positions (
  id UUID PRIMARY KEY,
  agent_config_id UUID,
  symbol VARCHAR(50),
  entry_price DECIMAL(10,5),
  current_price DECIMAL(10,5),
  unrealized_pnl DECIMAL(15,2),
  status VARCHAR(50),  -- open, closing
  updated_at TIMESTAMP,
  -- [Real-time position tracking]
);

CREATE TABLE live_trades (
  id UUID PRIMARY KEY,
  agent_config_id UUID,
  symbol VARCHAR(50),
  entry_price DECIMAL(10,5),
  exit_price DECIMAL(10,5),
  pnl DECIMAL(15,2),
  created_at TIMESTAMP,
  closed_at TIMESTAMP,
  -- [Real-time trade execution]
);

CREATE TABLE strategy_revenue (
  id UUID PRIMARY KEY,
  strategy_id UUID,
  user_id UUID,
  creator_id UUID,
  trade_pnl DECIMAL(15,2),
  creator_earnings DECIMAL(15,2),
  platform_earnings DECIMAL(15,2),
  trade_source VARCHAR(50),  -- 'live_trade' (not 'backtest')
  -- [REAL revenue split on REAL trades]
);

CREATE TABLE hardware_deployments (
  id UUID PRIMARY KEY,
  user_id UUID,
  hardware_name VARCHAR(255),
  openclaw_device_id VARCHAR(255),
  is_paired BOOLEAN,
  status VARCHAR(50),  -- online, offline, error
  last_heartbeat TIMESTAMP,
  -- [User's VPS/home server running agent]
);

CREATE TABLE notifications (
  id UUID PRIMARY KEY,
  user_id UUID,
  title VARCHAR(255),
  notification_type VARCHAR(50),  -- trade_executed, tp_hit, agent_error
  channels JSONB,  -- {email: true, push: true, sms: false}
  is_read BOOLEAN,
  created_at TIMESTAMP,
  -- [Real-time alerts]
);

CREATE TABLE daily_performance (
  id UUID PRIMARY KEY,
  user_id UUID,
  performance_date DATE,
  trades_count INT,
  win_rate DECIMAL(5,2),
  total_pnl DECIMAL(15,2),
  -- [Aggregated stats]
);
```

**20 tables total** (I'm just showing the critical ones). Different design, optimized for live execution + agent management + hardware integration.

### Key Differences OPENCLAW vs V0

```
V0 (Supabase):
├─ strategy_subscriptions.backtest_data = {win_rate: 0.68, pnl: 3250}
├─ strategy_revenue = calculated on backtest completion
├─ No agent_configs (just stored strategy JSON)
├─ No live_positions or live_trades
└─ Query pattern: Historical (S3 backtest results)

OPENCLAW (PostgreSQL):
├─ agent_configs + deployment_config = {cloud: {...}, hardware: {...}}
├─ live_positions + live_trades = REAL-TIME updates every 5 sec
├─ strategy_revenue = calculated on REAL trade completion
├─ agent_execution_logs = every heartbeat, every action
└─ Query pattern: Real-time streaming (WebSocket subscriptions)
```

### Chat-Driven Setup (OPENCLAW)

User never touches terminal:

```
USER: "Activate this strategy 24/7"

CHAT RESPONSE:
"Cloud ($45/mo) or Hardware (free)?"

USER: "Cloud"

AUTO:
├─ Create agent_config
├─ deployment_config.deployment_type = 'cloud'
├─ Deploy to OpenClaw infrastructure
├─ Status: 'deployed'
└─ Notification: "Agent live!"

OR:

USER: "Hardware, my AWS"

CHAT RESPONSE:
"One-liner install:
bash <(curl ...) --pairing-code ABC-123-XYZ"

AUTO (after user runs command):
├─ hardware_deployments.is_paired = true
├─ agent_config connected
├─ Status: 'deployed'
└─ Notification: "Agent live on your hardware!"

ALL VIA CHAT. NO TERMINAL KNOWLEDGE NEEDED.
```

### API OpenClaw (New)

```
POST /api/agents/deploy
├─ Input: {strategy_id, deployment_type}
├─ Auto-creates agent_config
└─ Deploy to OpenClaw or wait for hardware pairing

POST /api/agents/pause
POST /api/agents/resume
POST /api/agents/terminate

GET /api/agents/status/:agent_id
└─ Real-time status + live P&L

GET /api/trades/live
└─ Current open positions

GET /api/trades/history
└─ Closed trades + real revenue split

POST /api/hardware/pair
├─ Input: {pairing_code}
└─ Link hardware to agent

GET /api/earnings/creator/:creator_id
└─ Monthly payouts from REAL trades
```

### Infrastructure OPENCLAW

```
AWS (Your servers):
├─ PostgreSQL managed: $500/mo
├─ OpenClaw EC2 instances: $2K-5K/mo (agent execution)
├─ Backup/redundancy: $500/mo
└─ Load balancer: $200/mo
TOTAL: ~$3.2K-6K/mo

HANDLES:
├─ 1000+ concurrent traders
├─ 100-500 agents running 24/7
├─ Real-time price feeds
├─ Hardware connections (user VPS)
└─ Live P&L streaming
```

---

## PARTE 3: LA ESTRATEGIA FINAL

### Months 1-2: V0 Cash Engine

```
Goal: 50 users pagando $499/mo
Revenue: $25K/mo
Costs: $1.2K/mo
Profit: $23.8K
Use: Pay Marc + contractors to build OPENCLAW
```

### Months 3-4: Parallel Products

```
V0 still running: $25K/mo
OPENCLAW in beta: 20 users testing, 0 revenue yet
Total revenue: $25K/mo
Total costs: $3K (V0) + $15K (OPENCLAW dev) = $18K
Profit: $7K/mo (still positive)
```

### Month 5+: OPENCLAW Full Launch

```
V0 archived (historical)
OPENCLAW production: 50 users @ average $800/mo
Revenue: $40K/mo
Costs: $20K/mo (infra + team)
Profit: $20K/mo (sustainable)
Scale to 500 users: $200K+/mo revenue
```

### Why This Works

```
✅ De-risk: V0 makes money while building OPENCLAW
✅ Proof: 50 paid users = market validation
✅ Funding: $25K/mo + $20K investment = 2 months dev time
✅ Clean separation: V0 and OPENCLAW are independent
✅ Zero migration headaches: Just rewrite OPENCLAW from scratch
✅ Faster deployment: OPENCLAW optimized for AWS + memory management
✅ Better tech: PostgreSQL > Supabase for real-time agents
```

---

## TL;DR Para Marc

**V0: 4 semanas, Supabase, 13 tablas, temporal.**
- Goal: $25K/mo con 50 users
- Tech: Vercel + Supabase + OpenRouter
- Stack: Next.js + React + Radix UI
- Schema: [13 tablas arriba]
- Deployment: Vercel (auto)

**OPENCLAW: 8 semanas (paralelo), PostgreSQL, 20 tablas, permanente.**
- Goal: Scale a 1000+ users
- Tech: AWS + OpenClaw framework + React Native
- Stack: FastAPI o Node.js + PostgreSQL + React Native
- Schema: Rewrite from scratch (optimized for live execution)
- Deployment: AWS (managed)

**NO migration: V0 archives, OPENCLAW starts fresh.**

Guardamos .md para referencia, reescribimos DB porque AWS + OpenClaw tiene mejor memory management.

**Timeline:**
- Semanas 1-4: Tú = V0
- Semanas 5-12 (paralelo): Marc = OPENCLAW
- Mes 3: Soft launch (both)
- Mes 4+: OPENCLAW full, V0 archived

**Funding:**
- V0 genera $25K/mo
- + $20K investment
- = Sufficient para 2 meses Marc full-time + contractor

Todo aquí. Todo explicado. Listo para que Marc empiece. 🚀

---
