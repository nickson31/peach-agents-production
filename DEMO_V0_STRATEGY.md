# DEMO V0 STRATEGY — Levantar 20K

## VISIÓN GENERAL

```
┌─────────────────────────────────────────────────────────────┐
│         DEMO V0: PARA LEVANTAR 20K (3-6 meses)             │
│                                                             │
│  NO es el producto final. Es un MVP funcional que          │
│  demuestra el potencial con APIs limitadas + browser.      │
│                                                             │
│  Meta: Cerrar 20-30 clientes @ $500/mo = $10K-15K/mo MRR  │
│        Usar ese MRR para pagar OpenClaw + dev + hardware   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## LAS 4 PÁGINAS EN DEMO V0

### PÁGINA 1: CHAT (Research Agent + Browser Use Cases)

```
USER EXPERIENCE:

"Hola, quiero analizar EUR/USD hoy"
  ↓
AGENT RESPONDE:
  ├─ Research Agent (BraveSearch):
  │  ├─ Busca: eventos económicos, noticias FED, ECB
  │  ├─ Busca: sentiment traders (reddit, twitter, stocktwits)
  │  ├─ Compilas análisis
  │  └─ Responde: "EUR today: FED indecisión, soporte 1.0850, 65% long"
  │
  └─ User puede:
     ├─ Preguntar más: "¿Qué traders famosos dijeron de EUR?"
     ├─ Use case A: "Busca 20 traders en YouTube, analiza qué dicen"
     └─ Use case B: "Conecta mi Binance, alerta si EUR toca 1.0875"

───────────────────────────────────

Use Case A: OLIMPIADA DE BOTS
User query: "Buscame 20 traders angloparlantes en YouTube sobre EUR/USD. 
             Descargate 2-3 transcripciones de cada uno. 
             Crea 20 bots simulados basados en sus estrategias. 
             Ejecuta olimpiada en mis accounts demo. Aquí mis claves."

Agent workflow:
  1. YouTube Search (BraveSearch API)
     └─ Encuentra 20 traders con videos sobre EUR/USD
  
  2. Browser API (Playwright/Puppeteer)
     └─ Descarga automáticamente subtítulos/transcripciones
  
  3. LLM Analysis (OpenRouter)
     ├─ Analiza cada transcripción
     ├─ Extrae: estrategia, entry, tp, sl, risk
     └─ Crea 20 bot configs (sin ejecutar aún)
  
  4. Demo Account Execution (Limited)
     ├─ User da API keys (demo account only)
     ├─ Agent ejecuta 20 bots en paralelo
     ├─ Simulación: 1 mes de datos históricos en 5 minutos
     ├─ Results: P&L por trader, win rate, etc
     └─ Return: "Trader 5 (su estrategia) habría ganado $4,250 en EUR/USD"
  
  Disclaimers:
  ├─ "Este es sim, no real"
  ├─ "Backtest ≠ futuro"
  ├─ "Recomendamos paper trading primero"
  └─ All results guardados en DB

User value:
  └─ "Wow, ahora sé qué traders copiar" / "Mi estrategia estaría #3"

───────────────────────────────────

Use Case B: ALERT/TRADE en Exchange (VERY LIMITED)
User query: "Conecta mi Binance. Alerta si EUR toca 1.0875. 
            Y si toca, compra 0.1 BTC solo."

Agent workflow:
  1. Browser API → Conecta a Binance (credenciales locales, no guardadas)
  2. Price monitoring (Brave Search + Exchange API si free)
  3. If trigger:
     └─ Ejecuta trade (cantidad pre-approved, muy pequeño)
  4. Notify user
  
  Disclaimers:
  ├─ "Cantidad LIMITADA a $100 USD"
  ├─ "NO recomendamos live trading aún"
  ├─ "Es demo. Riesgo real pero pequeño"
  ├─ "En 1 mes haremos full OpenClaw + hardware"
  └─ "Después podrás dejar corriendo 24/7 sin límites"

User value:
  └─ "Wow, realmente funciona. Cerré, esta es la que quiero."
```

---

### PÁGINA 2: SWIPE (CSV Import - Sin cambios)

```
MISMO QUE ANTES:
├─ Cargar CSV de prospects
├─ Swipear (like/dislike)
├─ Exportar liked como JSON
└─ Todo guardado en Supabase
```

---

### PÁGINA 3: TRADING (Info Only - NO FUNCIONAL)

```
PANTALLA: Información sobre trading
├─ "¿Cómo crear un bot?" (tutorial)
├─ "Nuestros traders hacen X% mensual" (stats)
├─ "Próximas features:" (roadmap)
│  ├─ Full bot automation
│  ├─ Multi-exchange support
│  ├─ Hardware integration
│  └─ "Déjanos tu email para beta" → Lead capture
├─ "Ver demo de olimpiada de bots" (link a YouTube o tutorial)
└─ "Conecta tu exchange" (DISABLED - grey out)
   └─ "Coming in V2 (with OpenClaw)"

USER INTERACTION:
└─ Mainly info gathering + email signup
```

---

### PÁGINA 4: CONFIG (Basic Settings)

```
PÁGINA: Settings
├─ Perfil (nombre, foto, email)
├─ Risk preferences (para cuando sale full bot)
├─ API keys (si user quiere guardar para Olimpiada/Exchange)
│  └─ Encrypted en Supabase, user puede revocar
├─ Data export (descargar todo)
└─ Suscripción (plan upgrade cuando haya paid tiers)
```

---

## DATABASE SCHEMA V0 (Simplificado)

```
SUPABASE (Solo lo que necesitamos para DEMO):

users
├─ id, email, created_at, timezone, risk_default
└─ api_keys_temp (for Olimpiada/Exchange)

conversations
├─ id, user_id, messages (chat history)
└─ context (qué está haciendo: research, olimpiada, etc)

queries_log
├─ id, user_id, query_type, input, output
├─ query_types:
│  ├─ research_analysis (BraveSearch)
│  ├─ olimpiada_create (YouTube + transcripts + backtest)
│  ├─ olimpiada_execute (demo trading)
│  └─ exchange_alert (monitor + trade)
└─ api_cost, tokens, timestamp

olimpiada_configs
├─ id, user_id, name ("Olimpiada EUR/USD")
├─ traders (20x array de bot configs)
├─ backtest_period (dates)
├─ results (P&L per bot)
└─ created_at

csv_imports, csv_rows, swipe_actions, user_preferences
└─ (same as before)

NO NEED (for DEMO):
├─ bot_configs (porque no hay bots propios yet)
├─ bot_backtests (olimpiada es ad-hoc)
└─ bot_executions (no real execution yet)
```

---

## API ENDPOINTS V0

### Backend (Node.js/Python FastAPI)

```
/api/chat
├─ POST → send message
├─ Workflow:
│  ├─ Detect intent: research / olimpiada / exchange_alert
│  ├─ Route to handler
│  └─ Response + save to Supabase

/api/research
├─ POST → analyze topic
├─ Input: {topic: "EUR/USD", time_period: "today"}
├─ Uses: BraveSearch API
├─ Output: {analysis, sources, sentiment}
├─ Cost: ~$0.01

/api/olimpiada/create
├─ POST → create olimpiada config
├─ Input: {traders: [...YouTube handles], symbol: "EUR_USD", period: "30 days"}
├─ Workflow:
│  ├─ YouTube search
│  ├─ Get transcripts (via YouTube API or manual upload)
│  ├─ LLM parse each transcript
│  ├─ Create 20 bot configs
│  └─ Save to DB
├─ Cost: ~$1-2 (LLM calls)
└─ Time: 5-10 minutes

/api/olimpiada/execute
├─ POST → run backtest
├─ Input: {olimpiada_id, historical_data}
├─ Workflow:
│  ├─ Simulate 20 bots trading
│  ├─ Calculate P&L
│  ├─ Rank by performance
│  └─ Save results
├─ Cost: ~$0.50
└─ Time: 2 minutes

/api/exchange/connect
├─ POST → validate API keys
├─ Input: {exchange: 'binance', api_key, api_secret}
├─ Returns: {valid: true/false, balance, permissions}

/api/exchange/alert
├─ POST → set price alert
├─ Input: {symbol: 'EUR_USD', price: 1.0875, action: 'alert' or 'trade', amount: 100}
├─ Workflow:
│  ├─ Monitor price (polling or WebSocket)
│  ├─ If trigger: notify + optional trade
│  └─ Log to audit
└─ Returns: {alert_id, status}

/api/csv/parse
├─ POST → upload + parse CSV
└─ (same as before)
```

---

## PROMPTS PARA OPENROUTER

### Prompt 1: Research Analysis

```
System:
"Eres un analista financiero experto en trading.
Tu tarea: analizar mercados, sentiment, eventos económicos.
Responde SIEMPRE en JSON con estructura: 
{
  analysis: 'string',
  key_events: ['event1', 'event2'],
  sentiment: 'bullish/bearish/neutral',
  key_levels: {support: X, resistance: Y},
  trader_sentiment_pct: N
}"

User:
"Analiza EUR/USD hoy. ¿Qué dijeron traders, news, eventos económicos?"

---

### Prompt 2: Extract Strategy from Transcript

```
System:
"Eres un expert en parsing estrategias de trading de transcripciones.
Dada una transcripción de video de un trader, extrae:
{
  trader_name: string,
  strategy: string (description),
  entry_logic: string,
  exit_logic: string,
  entry_price: number (if specific),
  tp: number,
  sl: number,
  risk_percent: number,
  pairs: [string],
  timeframe: string,
  confidence: 0-100 (qué tan claro estaba)
}

IMPORTANTE: Si no está claro, put null. NO inventes."

User:
"[Full YouTube transcript of trader explaining EUR/USD strategy]"
```

---

### Prompt 3: Olimpiada Results Analysis

```
System:
"Eres analista de resultados de backtesting.
Dado un array de 20 bots + resultados, genera:
{
  top_3_traders: [{name, strategy, pnl, win_rate}],
  bottom_3_traders: [...],
  best_edge: string,
  riskiest_strategy: string,
  recommendation: string
}

Usa formato JSON limpio."

User:
"[Array of 20 bot results from olimpiada]"
```

---

## MONETIZACIÓN V0

### Pricing (Para Demo)

```
GRATUITO (Demo):
├─ Chat + Research analysis (3 queries/day)
├─ Swipe page (unlimited)
├─ Olimpiada creation (1 free, after that $5 each)
├─ Exchange alert (disabled, "beta")
└─ Email: hey@racha.network to upgrade

PLAN BETA ($9.99/mes):
├─ Unlimited research queries
├─ Unlimited olimpiadas
├─ Exchange alerts (LIMITED: $100 max per trade)
├─ Email support
└─ "Early access. Descuento permanente cuando lancem full product."

PLAN PRO ($49/mes) - Futuro:
├─ Full bot automation (con OpenClaw)
├─ Multi-exchange
├─ Paper + Live trading
├─ Hardware option
└─ "Cuando tengamos 100 clientes en Beta"
```

### Conversión Flow

```
USER: Free → Plays with Olimpiada → Loves it
↓
"Wow, esto es increíble. ¿Puedo hacer más?"
↓
Upsell: "Beta access $9.99/mo: unlimited olimpiadas + alerts"
↓
Converts → $10/mo × 100 clientes = $1,000/mo
↓
→ Ramp up, when at $10K/mo → Launch full OpenClaw version
→ Existing customers upgrade to $99-499/mo
→ Revenue: $10K → $50K+/mo
```

---

## ROADMAP V0 (8 SEMANAS)

### Semana 1-2: Setup + Auth

- [ ] Supabase project + schema (simplified)
- [ ] Vercel deployment
- [ ] Supabase Auth (email/password)
- [ ] Layout básico (4 páginas)

### Semana 3: Research Agent

- [ ] Integrate BraveSearch API
- [ ] OpenRouter LLM setup
- [ ] Chat interface (basic messages)
- [ ] Research queries via chat

### Semana 4: CSV + Swipe

- [ ] CSV upload + parsing
- [ ] Swipe UI (cards, animations)
- [ ] Save swipes to DB
- [ ] Export liked rows

### Semana 5: Olimpiada V0.1

- [ ] YouTube search integration
- [ ] Transcript fetching (API or manual)
- [ ] Bot config extraction (LLM parse)
- [ ] Save configs to DB

### Semana 6: Olimpiada Execution

- [ ] Backtest engine (simulate 20 bots on historical data)
- [ ] Calculate P&L
- [ ] Rank results
- [ ] UI para ver resultados

### Semana 7: Exchange Alert (BETA)

- [ ] Browser API setup (Playwright)
- [ ] Exchange API integration (Binance, etc)
- [ ] Price monitoring (poll or WebSocket)
- [ ] Trade execution (VERY small amounts: $50 max)
- [ ] Disclaimers + warnings

### Semana 8: Polish + Launch

- [ ] Bug fixes
- [ ] Landing page
- [ ] Stripe integration (payments)
- [ ] Email capture
- [ ] Launch on ProductHunt / Twitter

---

## TECHNICAL STACK V0

```
Frontend:
├─ Next.js 16 (Vercel)
├─ React 19
├─ Radix UI + Tailwind (keep existing)
├─ WebSocket (real-time chat)
└─ Framer Motion (animations)

Backend:
├─ Node.js (Vercel Functions) or Python (FastAPI on fly.io)
├─ OpenRouter SDK (LLM calls)
├─ BraveSearch API (research)
├─ YouTube Data API (search + transcripts)
├─ Playwright/Puppeteer (browser automation)
└─ Exchange APIs (Binance, etc)

Database:
├─ Supabase PostgreSQL
├─ Row Level Security (RLS)
├─ Real-time subscriptions
└─ Backups included

Infrastructure:
├─ Vercel (frontend)
├─ Fly.io or similar (backend, if needed)
├─ Supabase (database)
├─ CloudFlare (optional: DDoS protection)
└─ Stripe (payments)

APIs (Cost per month estimate):
├─ OpenRouter: $50-100 (LLM calls)
├─ BraveSearch: $5-10 (research)
├─ YouTube API: $0 (free tier)
├─ Supabase: $0-25 (free → pro)
├─ Vercel: $0-20 (free → pro)
└─ TOTAL: ~$100/mo infra
```

---

## MARKETING STRATEGY V0

### Positioning

```
"The fastest way to find winning trading strategies.
Upload videos, we extract them, we test them on your demos.
See which traders' strategies would've made you money."

Not: "AI trading bot" (too scary, regulated)
Yes: "Strategy discovery + backtesting" (educational, safe)
```

### Launch Channels

```
1. Twitter (@racha.network or @nickson31)
   └─ "We built an olympiad of trading strategies. 
       Try free: [link]"

2. Reddit (r/trading, r/algotrading, r/forex)
   └─ Genuine post about strategy discovery

3. YouTube (your channel + traders' channels)
   └─ "I tested 20 traders' strategies against each other.
       Here's what happened."

4. ProductHunt
   └─ "Olimpiada: Trade Strategy Comparison Engine"

5. LinkedIn (target traders + investors)
   └─ Share results + testimonials

6. Email (existing network)
   └─ "Hey, we built something cool..."
```

### Early Adopters Target

```
├─ Day traders (Twitter/Reddit active)
├─ Crypto traders (YouTube channels, Discord)
├─ Strategy developers (Codeforces, GitHub)
├─ Finance students (universities, bootcamps)
└─ Goal: 100-200 free users in month 1
        20-30 convert to Beta ($10/mo)
        $200-300/mo MRR in month 2
```

---

## WHAT NOT TO DO (Regulatory)

```
❌ Don't claim: "Make $X per month guaranteed"
❌ Don't show: "Past performance = future results"
❌ Don't allow: Users trading with >$100 until full launch
❌ Don't store: Credit card details (Stripe handles)
❌ Don't hide: Disclaimers about demo/simulation
❌ Don't target: US residents directly (ambiguous regulations)

✅ DO show: Disclaimers everywhere
✅ DO limit: Trade amounts in beta
✅ DO educate: "This is backtesting, not prediction"
✅ DO collect: User feedback for improvements
✅ DO hire: Lawyer for v2 (when serious money)
```

---

## SUCCESS METRICS (V0)

```
MONTH 1:
├─ 500+ signups
├─ 100+ daily active users
├─ 20+ olimpiadas created
└─ 5+ YouTube videos made about us

MONTH 2:
├─ 2,000+ total signups
├─ 30+ Beta conversions ($300/mo MRR)
├─ 50+ olimpiadas
└─ Press mentions (tech blogs)

MONTH 3:
├─ 5,000+ total users
├─ 100+ Beta subscribers ($1,000/mo MRR)
├─ Enough $ to start OpenClaw dev
└─ Ready to hire first contractor
```

---

## WHAT CHANGES WHEN MARC ADDS OPENCLAW

```
V0 (NOW):
├─ Research: BraveSearch API calls
├─ Estrategy parsing: OpenRouter LLM
├─ Olimpiada: Simulation only (no live)
└─ Exchange: Browser API (very limited)

V1 (WITH OPENCLAW):
├─ Research: OpenClaw Web Agent (24/7 monitoring)
├─ Strategy parsing: OpenClaw Agent (batch + streaming)
├─ Olimpiada: Real-time bot execution (OpenClaw agents)
├─ Exchange: OpenClaw Agent in your server (24/7 live trading)
├─ Hardware: Option to run OpenClaw on your own server/box
└─ Limits removed: No $100 cap, full automation
```

---

## SUMMARY: V0 IS THE GATEWAY TO $20K

```
"We're not building the final product yet.
We're building a proof-of-concept that shows users:
'This is possible. And we can do it better with OpenClaw.'

V0 is the DEMO. V1 is the PRODUCT."

Timeline:
├─ Weeks 1-4: Build + Launch V0 (low cost)
├─ Weeks 5-8: Get 100 Beta users
├─ Months 2-3: Generate $1K-3K/mo MRR
├─ Month 4+: Use that to pay Marc for OpenClaw integration
│            + hire marketing + grow to $10K/mo
├─ Month 6+: Launch V1 with full OpenClaw
│            + existing customers upgrade
└─ Month 12+: $50K+/mo ARR → Hire team → Scale
```

**The demo is the elevator pitch that closes the funding round.**
