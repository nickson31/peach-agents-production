# ARQUITECTURA RACHA3 — V0 + OpenClaw

## 1. ESTADO ACTUAL (demo estática en `/tmp/racha3`)

```
racha3/ (Vercel/Next.js 16.1.6 + Radix UI)
├─ app/page.tsx → Main layout con 4 tabs
├─ components/
│  ├─ tab-bar.tsx → Navegación (Chat, Swipe, Liked, Archived)
│  ├─ swipe-stack.tsx → Card swiper (Tinder-like)
│  ├─ leads-list.tsx → Vista de leads aceptados/archivados
│  ├─ chat-interface.tsx → Chat básico
│  └─ ui/* → Radix components
├─ lib/leads-data.ts → Mock data estática (23 leads de ejemplo)
└─ styles/globals.css → Tailwind

FLUJO ACTUAL:
├─ Usuario ve "Explorar" (swipe)
├─ Like/Dislike → se guarda en useState
├─ Tab "Aceptados" muestra liked leads
├─ Tab "Archivados" muestra disliked leads
├─ Tab "Asistente" → chat estático
└─ Todo en memoria (sin persistencia)
```

---

## 2. LAS 4 PÁGINAS FINALES

```
┌─────────────────────────────────────────────────────────────┐
│              RACHA3 — 4 PÁGINAS + AUTH                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. CHAT PAGE (Asistente)                                   │
│  ├─ Usuario conversa con OpenClaw agent                     │
│  ├─ Input: texto/audio (voice-to-text)                      │
│  ├─ Output: respuestas contextuales                         │
│  ├─ Memoria: conversación guardada en Supabase              │
│  └─ Acciones: puede crear bots, cargar datos, preguntar     │
│                                                             │
│  2. SWIPE PAGE (Explorar)                                   │
│  ├─ Cargar CSV/JSON via chat                                │
│  │  └─ "Sube tu CSV" → OpenClaw parses → tarjetas           │
│  ├─ Like/Dislike → guardado en Supabase                     │
│  ├─ Export: "Exporta aceptados como JSON"                   │
│  └─ Use case: Prospect lists, leads, custom data            │
│                                                             │
│  3. TRADING PAGE (Bot Configuration)                        │
│  ├─ Conectar brokers (TradingView, Binance, etc)            │
│  │  └─ Browser API → acceso a tu cuenta                     │
│  ├─ Crear bot (entry/tp/sl, risk, timeframes)              │
│  ├─ Backtesting en demo                                     │
│  ├─ Ver P&L en vivo                                         │
│  └─ Queries guardadas en Supabase + analytics               │
│                                                             │
│  4. CONFIG PAGE (Settings)                                  │
│  ├─ Perfil usuario (nombre, email, foto)                   │
│  ├─ API keys (encrypted en Supabase)                        │
│  ├─ Broker connections (estado, permisos)                   │
│  ├─ Preferencias (idioma, timezone, riesgo default)        │
│  ├─ Data export (descargar historico)                       │
│  └─ Integración OpenClaw (cuando esté ready)                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. ÁRBOL DE INFORMACIÓN (Data Flow)

### VERSIÓN V0 (MOCKUP — Sin OpenClaw, con APIs externas)

```
┌────────────────────────────────────────────────────────────────┐
│                    V0: MOCKUP ARCHITECTURE                     │
│              (Vercel + Supabase + Browser APIs)                │
└────────────────────────────────────────────────────────────────┘

USER LOGIN (Supabase Auth)
    ↓
    ├─ Postgres DB (Supabase)
    │  ├─ users (id, email, created_at, preferences)
    │  ├─ conversations (user_id, messages, created_at)
    │  ├─ csv_imports (user_id, filename, data JSON, created_at)
    │  ├─ swipe_cards (user_id, card_id, action 'like'/'dislike')
    │  ├─ bot_configs (user_id, broker, api_keys_encrypted, settings)
    │  ├─ bot_queries (user_id, query, response, timestamp)
    │  └─ analytics (user_id, action, metadata, timestamp)
    │
    ├─ FLOW 1: CHAT PAGE
    │  ├─ User: "Carga mi CSV de leads"
    │  ├─ Frontend → Supabase storage (or temp upload)
    │  ├─ Backend API (Node/Python) → Parse CSV
    │  ├─ OpenRouter API → LLM classifies columns
    │  ├─ Response: "Detecté: Name, Email, Company, Score"
    │  ├─ Save: conversations table
    │  └─ Output: JSON structure → Swipe page
    │
    ├─ FLOW 2: SWIPE PAGE
    │  ├─ Load CSV parsed data as cards
    │  ├─ User swipes → like/dislike action
    │  ├─ Save to swipe_cards table
    │  ├─ User: "Exporta aceptados"
    │  ├─ Generate JSON + download
    │  └─ Save to analytics (export action)
    │
    ├─ FLOW 3: TRADING PAGE
    │  ├─ User: "Conecta mi TradingView"
    │  ├─ Browser API SDK (Playwright/Puppeteer)
    │  │  └─ Opens TradingView login in iframe
    │  │  └─ User logins (we don't see password)
    │  │  └─ Get chart data, price feeds
    │  ├─ User: "Create bot: EUR/USD, entry 1.0875, TP 1.0750"
    │  ├─ Save to bot_configs table (encrypted API keys)
    │  ├─ Demo: Simulate trade execution
    │  ├─ OpenRouter API → Generate analysis
    │  ├─ Save to bot_queries table
    │  ├─ Response: "Bot would enter at 1.0875, expect +$1,250"
    │  └─ Save to analytics (bot_action)
    │
    ├─ FLOW 4: CONFIG PAGE
    │  ├─ Load user preferences from users table
    │  ├─ Update (timezone, risk settings, etc)
    │  ├─ Manage API keys (show as ••••)
    │  └─ Save to users table
    │
    └─ ANALYTICS & FEEDBACK
       ├─ All actions logged to analytics table
       ├─ Query → Response pairs saved
       ├─ User behavior tracked (for future ML)
       └─ Exportable: "Download my analytics as CSV"

DATA PERSISTENCE:
├─ Supabase PostgreSQL (user data, conversations, configs)
├─ Supabase Storage (uploaded CSVs, exports)
├─ Encrypted fields: API keys, broker credentials
└─ Audit log: who did what, when
```

---

### VERSIÓN FINAL (OpenClaw — Con agents en tu server)

```
┌────────────────────────────────────────────────────────────────┐
│           FINAL: OPENCLAW ARCHITECTURE                         │
│    (Your server + OpenClaw agents + Mobile/Web app)            │
└────────────────────────────────────────────────────────────────┘

USER LOGIN (OAuth via your server or OpenClaw identity)
    ↓
    ├─ PostgreSQL DB (tu server)
    │  ├─ users (id, email, created_at, preferences)
    │  ├─ conversations (user_id, messages, created_at)
    │  ├─ csv_imports (user_id, filename, data JSON)
    │  ├─ swipe_cards (user_id, card_id, action)
    │  ├─ bot_configs (user_id, broker, settings)
    │  ├─ bot_queries (user_id, query, response)
    │  ├─ bot_executions (execution logs)
    │  ├─ analytics (all user actions)
    │  └─ audit_logs (security)
    │
    ├─ FLOW 1: CHAT PAGE (OpenClaw Agent)
    │  ├─ User: "Carga mi CSV"
    │  ├─ Message → OpenClaw agent
    │  ├─ Agent task:
    │  │  ├─ Parse CSV
    │  │  ├─ Classify columns
    │  │  ├─ Generate JSON structure
    │  │  └─ Return response
    │  ├─ Save conversation to DB
    │  ├─ Response via WebSocket (real-time)
    │  └─ Trigger: Swipe page updates
    │
    ├─ FLOW 2: SWIPE PAGE (Simple, no agent needed)
    │  ├─ Display JSON from chat
    │  ├─ User swipes
    │  ├─ Save action to DB
    │  ├─ Export: Call OpenClaw agent if format conversion needed
    │  └─ Analytics logged
    │
    ├─ FLOW 3: TRADING PAGE (OpenClaw + Browser Agent)
    │  ├─ User: "Conecta TradingView"
    │  ├─ OpenClaw Browser Agent:
    │  │  ├─ Opens TV in iframe (or native browser control)
    │  │  ├─ User authenticates (credentials stay local)
    │  │  ├─ Agent monitors TV charts
    │  │  ├─ Extracts price data, indicators
    │  │  └─ Sends to backend
    │  ├─ User: "Create bot: EUR/USD..."
    │  ├─ Bot config → OpenClaw task (set entry/tp/sl)
    │  ├─ OpenClaw monitors in background
    │  ├─ When price triggers → Execute
    │  ├─ Live feedback: P&L, execution logs
    │  └─ All saved to analytics
    │
    ├─ FLOW 4: CONFIG PAGE (Simple settings)
    │  ├─ User updates preferences
    │  ├─ Save to DB
    │  └─ OpenClaw agents respect settings (risk, timezone, etc)
    │
    └─ CONTINUOUS BACKGROUND TASKS (OpenClaw Agents)
       ├─ Market monitoring (TradingView price feeds)
       ├─ Trade execution (if bot conditions met)
       ├─ Analytics aggregation (daily P&L reports)
       ├─ Opportunity detection (pattern matching)
       └─ Notifications (WebSocket/Push to app)
```

---

## 4. CONVERSIÓN V0 → OpenClaw

### Mapeo de APIs externas a OpenClaw tasks

```
V0 (MOCKUP)                          OPENCLAW (FINAL)
─────────────────────────────────────────────────────────

OpenRouter LLM                       OpenClaw Agent (LLM task)
├─ Parse CSV                         ├─ Parse CSV (same logic)
├─ Generate JSON                     ├─ Generate JSON
└─ Analyze                           └─ Analyze

Browser API (Playwright)             OpenClaw Browser Agent
├─ Open TradingView                  ├─ Open TradingView
├─ Monitor prices                    ├─ Monitor prices
├─ Extract data                      └─ Extract data

Brave Search API                     OpenClaw Web Search Agent
├─ Search for news                   ├─ Search for news
├─ Sentiment analysis                └─ Sentiment analysis

Supabase DB                          PostgreSQL (your server)
├─ Store conversations               ├─ Store conversations
├─ Store configs                     ├─ Store configs
└─ Store analytics                   └─ Store analytics
```

---

## 5. ESTRUCTURA DE QUERIES (Para DB + OpenClaw)

### Tipo 1: CSV Upload Query

```
QUERY:
{
  type: "csv_upload",
  user_id: "user_123",
  filename: "prospects.csv",
  file_content: "Name,Email,Company,Score\n..."
}

V0 RESPONSE:
{
  status: "success",
  parsed_columns: ["name", "email", "company", "score"],
  row_count: 342,
  preview: [{name: "John", email: "john@...", ...}, ...]
}

SAVED TO DB (analytics):
{
  user_id: "user_123",
  action: "csv_upload",
  metadata: {filename, row_count, columns},
  timestamp: "2026-03-19T08:15:00Z"
}
```

### Tipo 2: Bot Configuration Query

```
QUERY:
{
  type: "bot_create",
  user_id: "user_123",
  pair: "EUR_USD",
  entry: 1.0875,
  tp: 1.0750,
  sl: 1.0950,
  risk_percent: 1.5,
  timeframe: "1h"
}

V0 RESPONSE:
{
  status: "created",
  bot_id: "bot_abc123",
  config: {...},
  backtest: {
    trades: 42,
    win_rate: 0.68,
    profit: 4250,
    max_loss: 580
  }
}

SAVED TO DB (bot_configs + analytics):
{
  bot_id: "bot_abc123",
  user_id: "user_123",
  config: {...},
  backtest_results: {...},
  created_at: "2026-03-19T08:20:00Z"
}
```

### Tipo 3: Market Analysis Query

```
QUERY:
{
  type: "market_analysis",
  user_id: "user_123",
  pair: "EUR_USD",
  context: "Should I enter EUR/USD now?"
}

V0 RESPONSE (OpenRouter):
{
  analysis: "EUR testing support at 1.0850. Sentiment 65% long...",
  recommendation: "Wait for bounce in 1-2 hours",
  confidence: 71,
  entry_zones: [1.0850, 1.0875, 1.0900]
}

SAVED TO DB (bot_queries + analytics):
{
  query_id: "query_xyz",
  user_id: "user_123",
  type: "market_analysis",
  response: {...},
  timestamp: "2026-03-19T08:25:00Z"
}
```

---

## 6. DATABASE SCHEMA (Supabase V0)

```sql
-- Users
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  timezone VARCHAR(50) DEFAULT 'UTC',
  risk_default DECIMAL(3,1) DEFAULT 1.5
);

-- Conversations (Chat)
CREATE TABLE conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  messages JSONB,  -- [{role: 'user'/'assistant', content: '...'}]
  created_at TIMESTAMP DEFAULT NOW()
);

-- CSV Imports
CREATE TABLE csv_imports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  filename VARCHAR(255),
  data JSONB,  -- parsed CSV as JSON
  row_count INT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Swipe Cards
CREATE TABLE swipe_cards (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  csv_import_id UUID REFERENCES csv_imports(id),
  card_index INT,
  action VARCHAR(10),  -- 'like' or 'dislike'
  swiped_at TIMESTAMP DEFAULT NOW()
);

-- Bot Configs
CREATE TABLE bot_configs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  pair VARCHAR(50),  -- EUR_USD, BTC_USD, etc
  entry_price DECIMAL(10,5),
  tp_price DECIMAL(10,5),
  sl_price DECIMAL(10,5),
  risk_percent DECIMAL(3,1),
  timeframe VARCHAR(10),  -- 1h, 4h, daily
  broker VARCHAR(50),  -- 'tradingview', 'binance', etc
  api_key_encrypted VARCHAR(255),  -- encrypted
  created_at TIMESTAMP DEFAULT NOW()
);

-- Bot Queries (for analytics)
CREATE TABLE bot_queries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  bot_id UUID REFERENCES bot_configs(id),
  query_text TEXT,
  response_text TEXT,
  confidence INT,  -- 0-100
  created_at TIMESTAMP DEFAULT NOW()
);

-- Analytics (all user actions)
CREATE TABLE analytics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  action VARCHAR(50),  -- 'csv_upload', 'bot_create', 'swipe', etc
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  INDEX idx_user_action (user_id, action)
);

-- Audit Logs (security)
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  event VARCHAR(100),
  details JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 7. PRÓXIMOS PASOS

### IMMEDIATE (Week 1):
1. **Frontend structure (Next.js)**
   - [ ] Add Supabase auth (Vercel + Supabase integration)
   - [ ] Create 4 page layouts (Chat, Swipe, Trading, Config)
   - [ ] Connect to Supabase DB

2. **Backend API (Node.js or Python)**
   - [ ] Create `/api/chat` endpoint
   - [ ] Create `/api/csv/parse` endpoint
   - [ ] Create `/api/bot/create` endpoint
   - [ ] Create `/api/bot/backtest` endpoint
   - [ ] Integrate OpenRouter LLM

3. **Database (Supabase)**
   - [ ] Create tables (users, conversations, csv_imports, swipe_cards, bot_configs, etc)
   - [ ] Set up RLS (Row Level Security) policies
   - [ ] Enable real-time subscriptions (WebSocket)

### PHASE 2 (Week 2-3):
1. **Browser API Integration**
   - [ ] Add Puppeteer/Playwright SDK
   - [ ] Connect to TradingView (iframe authentication)
   - [ ] Extract price data, chart indicators
   - [ ] Save to DB

2. **Bot Logic**
   - [ ] Backtest engine
   - [ ] Live monitoring (demo)
   - [ ] P&L calculations
   - [ ] Execution simulation

3. **OpenRouter Integration**
   - [ ] CSV parsing via LLM
   - [ ] Market analysis prompts
   - [ ] Response templating

### PHASE 3 (Week 4+):
1. **OpenClaw Migration (Marc's responsibility)**
   - [ ] Convert API endpoints to OpenClaw tasks
   - [ ] Set up agent workflows
   - [ ] Configure prompt templates
   - [ ] Deploy on your server

---

## 8. KEY FILES TO CREATE

```
racha3/ (update structure)
├─ app/
│  ├─ page.tsx (already exists, keep structure)
│  ├─ (auth)/ → Auth pages (login, signup)
│  ├─ (dashboard)/
│  │  ├─ chat/ → Chat page
│  │  ├─ swipe/ → Swipe page
│  │  ├─ trading/ → Trading page
│  │  └─ config/ → Config page
│  └─ api/
│     ├─ auth/ → Supabase auth endpoints
│     ├─ chat → LLM chat logic
│     ├─ csv → CSV parsing
│     ├─ bot → Bot creation/management
│     └─ analytics → Query logging
│
├─ components/
│  ├─ (keep existing)
│  ├─ pages/
│  │  ├─ ChatPage.tsx
│  │  ├─ SwipePage.tsx
│  │  ├─ TradingPage.tsx
│  │  └─ ConfigPage.tsx
│  └─ (new)
│     ├─ ChatInterface.tsx (enhanced)
│     ├─ BotBuilder.tsx
│     ├─ BrokerConnect.tsx
│     └─ AnalyticsView.tsx
│
├─ lib/
│  ├─ supabase.ts → Client setup
│  ├─ openrouter.ts → LLM integration
│  ├─ browser-api.ts → Playwright/Puppeteer
│  └─ queries.ts → Pre-built DB queries
│
└─ .env.local
   ├─ NEXT_PUBLIC_SUPABASE_URL
   ├─ NEXT_PUBLIC_SUPABASE_ANON_KEY
   ├─ SUPABASE_SERVICE_ROLE_KEY
   ├─ OPENROUTER_API_KEY
   └─ BROWSER_API_KEY (if using external service)
```

---

## SUMMARY

| Aspecto | V0 (Mockup) | Final (OpenClaw) |
|---------|-----------|-----------------|
| Auth | Supabase | Supabase / OpenClaw |
| DB | Supabase PostgreSQL | PostgreSQL (tu server) |
| LLM | OpenRouter API calls | OpenClaw Agent tasks |
| Browser | Puppeteer/Playwright API | OpenClaw Browser Agent |
| Hosting | Vercel | Tu server + Vercel (frontend) |
| Real-time | Supabase Realtime | OpenClaw WebSocket |
| Execution | Demo/simulation | Real execution with OpenClaw |

**El mockup sirve como prototipo funcional que Marc convertirá a OpenClaw después.**
