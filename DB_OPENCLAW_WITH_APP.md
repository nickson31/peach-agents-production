# DATABASE OPENCLAW VERSION — Full Product (Server + Hardware + App)

**Para Marc: Cómo evoluciona la base de datos cuando agregamos OpenClaw + hardware.**

---

## CAMBIOS FUNDAMENTALES

```
V0 (DEMO):
├─ Backtest = simulación histórica
├─ Estrategia = JSON guardado
├─ Usuario = ve resultados en web
└─ Revenue = calculada manual (0.5% por trade simulado)

OPENCLAW (PRODUCTION):
├─ Backtest = mismo + agent continuous monitoring
├─ Estrategia = agent config (ejecutada 24/7)
├─ Usuario = app (móvil) + web + hardware option
├─ Revenue = automático (agent tracks cada trade real)
└─ Hardware = trader puede ejecutar en su máquina local
```

---

## NUEVAS TABLAS (Agregar a V0)

### Agent Management

#### agent_configs

```sql
CREATE TABLE agent_configs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Owner
  strategy_id UUID NOT NULL REFERENCES strategies(id),
  user_id UUID NOT NULL REFERENCES users(id),
  
  -- Agent Identity
  agent_name VARCHAR(255),
  agent_version INT DEFAULT 1,
  
  -- Deployment
  deployment_type VARCHAR(50) NOT NULL,
    -- 'cloud' = runs on Racha servers (OpenClaw)
    -- 'hardware' = runs on trader's VPS/hardware
    -- 'hybrid' = both (failover)
  
  -- OpenClaw Integration
  openclaw_agent_id VARCHAR(255),  -- OpenClaw's agent ID
  openclaw_session_id VARCHAR(255),  -- Current session
  
  -- Broker Connections
  broker_api_credential_id UUID REFERENCES api_credentials(id),
  broker_type VARCHAR(50),  -- 'alpaca', 'binance', 'interactive_brokers'
  
  -- Strategy Execution
  strategy_config JSONB,  -- Entry/TP/SL/risk from strategies table
  custom_parameters JSONB,  -- User tweaks
  
  -- Execution Status
  status VARCHAR(50) DEFAULT 'initialized',
    -- 'initialized', 'deployed', 'monitoring', 'executing', 'paused', 'error'
  
  current_state JSONB,
    -- {positions_open: 1, last_check: timestamp, monitoring: true}
  
  error_logs TEXT[],
  
  -- Monitoring
  cpu_usage DECIMAL(5,2),  -- if hardware
  memory_usage DECIMAL(5,2),  -- if hardware
  last_heartbeat TIMESTAMP,
  
  -- Metrics
  uptime_percent DECIMAL(5,2) DEFAULT 100.0,
  total_executions INT DEFAULT 0,
  total_pnl DECIMAL(15,2) DEFAULT 0,
  
  -- Deployment Location (if hardware)
  hardware_location VARCHAR(255),  -- "user's home server"
  hardware_ip_address VARCHAR(50),
  hardware_public_key VARCHAR(255),  -- for SSH
  
  -- Timestamps
  created_at TIMESTAMP DEFAULT NOW(),
  deployed_at TIMESTAMP,
  updated_at TIMESTAMP DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_strategy_id (strategy_id),
  INDEX idx_user_id (user_id),
  INDEX idx_status (status),
  INDEX idx_deployment_type (deployment_type),
  UNIQUE KEY unique_strategy_user_deployment (strategy_id, user_id, deployment_type)
);
```

#### agent_execution_logs

```sql
CREATE TABLE agent_execution_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_config_id UUID NOT NULL REFERENCES agent_configs(id),
  
  -- Execution Event
  event_type VARCHAR(50),
    -- 'heartbeat', 'price_check', 'entry_trigger', 'tp_hit', 'sl_hit', 'error'
  
  -- Details
  event_data JSONB,
    -- {price: 1.0875, entry_triggered: true, order_id: '...'}
  
  -- Performance
  execution_time_ms INT,
  
  -- Logging
  log_level VARCHAR(20),  -- 'debug', 'info', 'warning', 'error'
  message TEXT,
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_agent_config_id (agent_config_id),
  INDEX idx_event_type (event_type),
  INDEX idx_created_at (created_at)
);
```

#### api_credentials

```sql
CREATE TABLE api_credentials (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  -- Broker
  broker VARCHAR(50) NOT NULL,  -- 'alpaca', 'binance', etc
  
  -- Encrypted credentials
  api_key TEXT,  -- pgp_sym_encrypt(api_key, 'secret')
  api_secret TEXT,  -- encrypted
  passphrase TEXT,  -- encrypted (if needed)
  
  -- Session
  session_token TEXT ENCRYPTED,
  token_expires_at TIMESTAMP,
  
  -- Status
  is_active BOOLEAN DEFAULT true,
  is_verified BOOLEAN DEFAULT false,
  last_verified_at TIMESTAMP,
  
  -- Audit
  created_at TIMESTAMP DEFAULT NOW(),
  last_used_at TIMESTAMP,
  
  -- Constraints
  UNIQUE KEY unique_user_broker (user_id, broker),
  INDEX idx_user_id (user_id),
  INDEX idx_broker (broker)
);
```

---

### Real-time Monitoring

#### live_positions

```sql
CREATE TABLE live_positions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_config_id UUID NOT NULL REFERENCES agent_configs(id),
  
  -- Position
  symbol VARCHAR(50) NOT NULL,
  side VARCHAR(10),  -- 'long', 'short'
  qty DECIMAL(15,8),
  
  -- Entry
  entry_price DECIMAL(10,5),
  entry_time TIMESTAMP,
  
  -- Current
  current_price DECIMAL(10,5),
  current_price_at TIMESTAMP,
  
  -- Target
  tp_price DECIMAL(10,5),
  sl_price DECIMAL(10,5),
  
  -- P&L (live)
  unrealized_pnl DECIMAL(15,2),
  unrealized_pnl_percent DECIMAL(5,2),
  
  -- Status
  status VARCHAR(50) DEFAULT 'open',  -- 'open', 'closing', 'closed'
  
  -- Broker
  broker_position_id VARCHAR(255),
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_agent_config_id (agent_config_id),
  INDEX idx_status (status),
  INDEX idx_symbol (symbol)
);
```

#### live_trades

```sql
CREATE TABLE live_trades (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_config_id UUID NOT NULL REFERENCES agent_configs(id),
  
  -- Trade
  symbol VARCHAR(50) NOT NULL,
  side VARCHAR(10),
  qty DECIMAL(15,8),
  
  -- Entry
  entry_price DECIMAL(10,5),
  entry_time TIMESTAMP,
  
  -- Exit
  exit_price DECIMAL(10,5),
  exit_time TIMESTAMP,
  
  -- P&L
  pnl DECIMAL(15,2),
  pnl_percent DECIMAL(5,2),
  
  -- Duration
  duration_minutes INT,
  
  -- Reason
  close_reason VARCHAR(50),  -- 'tp_hit', 'sl_hit', 'manual'
  
  -- Broker
  broker_trade_id VARCHAR(255),
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_agent_config_id (agent_config_id),
  INDEX idx_symbol (symbol),
  INDEX idx_created_at (created_at)
);
```

---

### Hardware Integration

#### hardware_deployments

```sql
CREATE TABLE hardware_deployments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  -- Hardware info
  hardware_name VARCHAR(255),
  hardware_type VARCHAR(50),  -- 'vps', 'home_server', 'raspberry_pi'
  
  -- Connection
  public_ip VARCHAR(50),
  ssh_public_key VARCHAR(2048),
  
  -- OpenClaw Integration
  openclaw_device_pair_code VARCHAR(50),  -- From hardware pairing
  openclaw_device_id VARCHAR(255),
  is_paired BOOLEAN DEFAULT false,
  paired_at TIMESTAMP,
  
  -- Status
  status VARCHAR(50) DEFAULT 'pending',  -- 'pending', 'paired', 'online', 'offline', 'error'
  last_heartbeat TIMESTAMP,
  
  -- Specs
  cpu_cores INT,
  memory_gb INT,
  storage_gb INT,
  
  -- Agents Running
  agents_running INT DEFAULT 0,
  agents_config JSONB,  -- [{agent_id, strategy_id}]
  
  -- Logs
  error_logs TEXT[],
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_user_id (user_id),
  INDEX idx_status (status),
  INDEX idx_is_paired (is_paired)
);
```

#### hardware_health_checks

```sql
CREATE TABLE hardware_health_checks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  hardware_deployment_id UUID NOT NULL REFERENCES hardware_deployments(id),
  
  -- Health metrics
  cpu_usage DECIMAL(5,2),
  memory_usage DECIMAL(5,2),
  disk_usage DECIMAL(5,2),
  network_latency_ms INT,
  
  -- Status
  is_healthy BOOLEAN DEFAULT true,
  health_score INT,  -- 0-100
  
  -- Alerts
  alerts TEXT[],
  
  checked_at TIMESTAMP DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_hardware_deployment_id (hardware_deployment_id),
  INDEX idx_checked_at (checked_at)
);
```

---

### Notifications & Alerts

#### notifications

```sql
CREATE TABLE notifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  -- Content
  title VARCHAR(255),
  message TEXT,
  notification_type VARCHAR(50),
    -- 'trade_executed', 'tp_hit', 'sl_hit', 'agent_error', 'hardware_offline'
  
  -- References
  agent_config_id UUID REFERENCES agent_configs(id),
  trade_id UUID REFERENCES live_trades(id),
  
  -- Delivery
  channels JSONB,  -- {email: true, push: true, sms: false}
  is_read BOOLEAN DEFAULT false,
  read_at TIMESTAMP,
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_user_id (user_id),
  INDEX idx_is_read (is_read),
  INDEX idx_created_at (created_at)
);
```

---

### Analytics & Reporting

#### daily_performance

```sql
CREATE TABLE daily_performance (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  -- Date
  performance_date DATE,
  
  -- Trading Metrics
  trades_count INT,
  winning_trades INT,
  losing_trades INT,
  win_rate DECIMAL(5,2),
  
  -- P&L
  total_pnl DECIMAL(15,2),
  avg_win DECIMAL(15,2),
  avg_loss DECIMAL(15,2),
  
  -- Risk
  max_drawdown DECIMAL(5,2),
  
  -- Agents
  agents_active INT,
  agents_errors INT,
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_user_id (user_id),
  INDEX idx_performance_date (performance_date)
);
```

---

## CAMBIOS EN TABLAS EXISTENTES

### strategies (Agregar columnas)

```sql
ALTER TABLE strategies ADD COLUMN (
  agent_template JSONB,  -- Estructura para OpenClaw agent
  openclaw_agent_definition TEXT,  -- YAML/JSON del agent
  requires_hardware BOOLEAN DEFAULT false,
  min_hardware_spec JSONB,  -- {cpu: 2, memory: 4, storage: 50}
  execution_cost_usd_per_month DECIMAL(10,2),  -- Server/compute cost
  last_agent_execution TIMESTAMP,
  agent_execution_count INT DEFAULT 0
);
```

### strategy_subscriptions (Agregar columnas)

```sql
ALTER TABLE strategy_subscriptions ADD COLUMN (
  agent_config_id UUID REFERENCES agent_configs(id),
  agent_status VARCHAR(50),  -- 'inactive', 'monitoring', 'executing'
  agent_activated_at TIMESTAMP,
  agent_deactivated_at TIMESTAMP,
  live_pnl DECIMAL(15,2) DEFAULT 0,  -- Real trading results
  live_trades_count INT DEFAULT 0,
  hardware_deployment_id UUID REFERENCES hardware_deployments(id),  -- if user's hardware
  is_paper_trading BOOLEAN DEFAULT true
);
```

### strategy_revenue (Agregar columnas)

```sql
ALTER TABLE strategy_revenue ADD COLUMN (
  trade_source VARCHAR(50),  -- 'backtest', 'paper_trade', 'live_trade'
  agent_config_id UUID REFERENCES agent_configs(id),
  execution_timestamp TIMESTAMP,
  is_real_money BOOLEAN DEFAULT false
);
```

---

## WORKFLOW: V0 → OPENCLAW

### SCENARIO: Trader A finds strategy, monetizes it

```
STEP 1: DEMO (V0 - Supabase only)
├─ Find strategy in marketplace
├─ Backtest on historical data: 68% win rate
├─ Subscribe: $0.5% revenue share
└─ Strategy stays in library (not executing)

STEP 2: UPGRADE to OPENCLAW
├─ Trader A: "I want to activate this 24/7"
├─ System creates: agent_config (OpenClaw template)
├─ Trader chooses deployment:
│  ├─ OPTION A: Cloud (Racha servers)
│  │  └─ Monthly cost: $20-50/agent
│  │  └─ Agent runs in our OpenClaw instance
│  │  └─ Status: Always on
│  │
│  └─ OPTION B: Hardware (trader's VPS/home)
│     ├─ Monthly cost: $0 (trader's hardware)
│     ├─ Download: OpenClaw agent software
│     ├─ Install: On VPS (pairing code)
│     ├─ Connect: To app via WebSocket
│     └─ Status: Monitored but runs locally
│
├─ Trader selects: Cloud ($30/mo)
├─ System: Deploys agent_config to OpenClaw
├─ Agent wakes up: Starts monitoring EUR/USD
└─ agent_configs table updated

STEP 3: LIVE TRADING
├─ Agent monitors 24/7
├─ Every 10 seconds: Price check
├─ Entry trigger → Order execution
├─ Trade stored: live_trades table
├─ Revenue calculated: strategy_revenue table
│  └─ Trader earns: 99%
│  └─ Creator: 0.5%
│  └─ Platform: 0.5%
│
├─ Notifications sent:
│  ├─ "Trade executed!"
│  ├─ "TP hit! +$250"
│  └─ All pushed to app + email
│
└─ Analytics updated: daily_performance

STEP 4: MONETIZATION
├─ Creator dashboard:
│  ├─ "This month: $2,500 (50 traders using it)"
│  ├─ Breakdown by trader
│  ├─ Graph: earnings over time
│  └─ [Withdraw to bank]
│
└─ Payout: Monthly via Stripe Connect

STEP 5: SCALE
├─ User B finds same strategy
├─ Also activates on hardware (own VPS)
├─ Creator now earning from 2 traders
├─ Each trader: independent agent running
├─ Creator: completely passive
└─ Platform: 0.5% from both users' trades
```

---

## DATABASE SIZE COMPARISON

```
V0 (DEMO):
├─ Storage: ~100 MB (strategies, backtests, olimpiadas)
├─ Users: 500
├─ Queries/sec: 10-50
└─ Cost: Supabase $25/mo

OPENCLAW (PRODUCTION):
├─ Storage: ~10 GB (live trades, agent logs, execution history)
├─ Users: 5,000
├─ Queries/sec: 100-500 (real-time position updates)
├─ New tables: 7 (agent_configs, live_positions, hardware_deployments, etc)
└─ Cost: 
   ├─ PostgreSQL (managed): $500/mo
   ├─ OpenClaw server: $2,000-5,000/mo (for agents)
   ├─ Hardware support: $500/mo (DevOps)
   └─ TOTAL: ~$3K-6K/mo infra
```

---

## MIGRATION SCRIPT (V0 → OPENCLAW)

```sql
-- When adding OpenClaw to existing deployment:

-- 1. Add new tables
CREATE TABLE agent_configs (...);
CREATE TABLE agent_execution_logs (...);
CREATE TABLE api_credentials (...);
CREATE TABLE live_positions (...);
CREATE TABLE live_trades (...);
CREATE TABLE hardware_deployments (...);
CREATE TABLE hardware_health_checks (...);
CREATE TABLE notifications (...);
CREATE TABLE daily_performance (...);

-- 2. Add columns to existing tables
ALTER TABLE strategies ADD COLUMN agent_template JSONB;
ALTER TABLE strategy_subscriptions ADD COLUMN agent_config_id UUID;
ALTER TABLE strategy_revenue ADD COLUMN trade_source VARCHAR(50);

-- 3. Backfill data (if existing strategies)
-- Mark all existing strategy_subscriptions as 'paper_trading'
UPDATE strategy_subscriptions 
SET is_paper_trading = true 
WHERE agent_config_id IS NULL;

-- 4. Enable RLS for new tables
ALTER TABLE agent_configs ENABLE ROW LEVEL SECURITY;
ALTER TABLE live_positions ENABLE ROW LEVEL SECURITY;
-- ... etc
```

---

## API ENDPOINTS (New for OpenClaw)

```
── AGENT MANAGEMENT ──

POST /api/agents/create
├─ Input: {strategy_id, deployment_type}
├─ Creates: agent_config
└─ Response: {agent_id, openclaw_agent_id}

POST /api/agents/deploy
├─ Input: {agent_config_id}
├─ Action: Upload to OpenClaw / Hardware
└─ Response: {status, deployment_url}

GET /api/agents/status/:agent_id
├─ Returns: current status, P&L, trades
└─ Real-time via WebSocket

POST /api/agents/pause
POST /api/agents/resume
POST /api/agents/terminate

── HARDWARE MANAGEMENT ──

POST /api/hardware/pair
├─ Input: {pairing_code from hardware}
├─ Action: Link hardware to OpenClaw
└─ Response: {hardware_deployment_id}

GET /api/hardware/health/:hardware_id
├─ Returns: CPU, memory, uptime, latency
└─ Real-time monitoring

── LIVE TRADES ──

GET /api/trades/live
├─ Returns: current open positions
└─ Streaming updates

GET /api/trades/history
├─ Returns: closed trades + P&L
└─ Filterable by strategy, date

── NOTIFICATIONS ──

GET /api/notifications
POST /api/notifications/read
POST /api/notifications/preferences
```

---

## SUMMARY FOR MARC

**Cambios principales V0 → OPENCLAW:**

```
V0:
├─ Backtest = simulación
├─ Revenue = teórico (0.5% de ganancias simuladas)
├─ User interacción = web only
└─ Storage = ~100 MB

OPENCLAW:
├─ Live trading = real execution via agents
├─ Revenue = automático (0.5% de ganancias reales)
├─ Hardware option = trader puede ejecutar localmente
├─ User interacción = app + web + hardware dashboard
├─ Real-time monitoring = cada trade, cada posición
├─ Storage = ~10 GB (más logs, ejecuciones)
└─ 7 nuevas tablas + columnas en existentes
```

**Key difference:**

V0: Backtest tool + marketplace (SaaS)
OPENCLAW: Automated trading platform (24/7 agent execution)

**El database es el mismo, pero:**
- V0 = estrategias guardadas como JSON
- OPENCLAW = estrategias convertidas a agents ejecutados en vivo
