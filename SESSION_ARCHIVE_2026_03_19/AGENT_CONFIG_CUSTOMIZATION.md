# AGENT CONFIG CUSTOMIZATION — Full App vs Hardware (Chat-Driven)

## OVERVIEW

```
┌─────────────────────────────────────────────────────────────┐
│      AGENT CONFIGS: 2 OPCIONES, 100% CONFIGURABLES        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  OPCIÓN 1: FULL APP (Cloud - Racha servers)                │
│  ├─ Agent corre en OpenClaw infrastructure                 │
│  ├─ Configuración: vía chat de app                         │
│  ├─ Precio: $30-50/mes por agent                           │
│  └─ Setup: 2 minutos (botón + confirmar)                   │
│                                                             │
│  OPCIÓN 2: HARDWARE (User's VPS/home/raspberry)            │
│  ├─ Agent corre en máquina del trader                      │
│  ├─ Configuración: vía chat app O canal Telegram/Discord  │
│  ├─ Precio: $0/mes (user's electricity/bandwidth)          │
│  └─ Setup: 5 minutos (pairing code + OpenClaw agent SW)   │
│                                                             │
│  → TODO configurado desde conversación natural             │
│  → User nunca toca terminal (si no quiere)                 │
│  → Chat entiende intención y auto-configura               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## DATABASE: agent_configs (Revised)

```sql
CREATE TABLE agent_configs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Owner
  strategy_id UUID NOT NULL REFERENCES strategies(id),
  user_id UUID NOT NULL REFERENCES users(id),
  
  -- Agent Identity
  agent_name VARCHAR(255),
  agent_version INT DEFAULT 1,
  
  ┌──────────────────────────────────────────────────┐
  │  DEPLOYMENT CONFIG (The key field)               │
  └──────────────────────────────────────────────────┘
  
  deployment_config JSONB NOT NULL,
    -- ESTRUCTURA UNIFICADA para ambas opciones:
    -- {
    --   deployment_type: 'cloud' | 'hardware',
    --   
    --   -- Si deployment_type = 'cloud':
    --   cloud_config: {
    --     region: 'us-east-1' (or eu-west-1, ap-southeast-1),
    --     launch_on_create: true,
    --     redundancy: 'single' | 'failover',
    --     monthly_cost_estimate: 45
    --   },
    --
    --   -- Si deployment_type = 'hardware':
    --   hardware_config: {
    --     hardware_type: 'vps' | 'home_server' | 'raspberry_pi' | 'macos' | 'windows',
    --     pairing_code: 'ABC123XYZ',  -- Generated, 1 time use
    --     pairing_expires_at: '2026-03-26T09:10:00Z',
    --     openclaw_agent_version: 'v1.2.3',
    --     system_requirements: {
    --       os: 'linux' | 'macos' | 'windows',
    --       cpu_min: 2,
    --       memory_min_gb: 4,
    --       storage_min_gb: 50,
    --       internet_speed_mbps_min: 5
    --     },
    --     download_url: 'https://cdn.racha.network/agents/v1.2.3/...',
    --     hardware_deployment_id: UUID (FK after pairing)
    --   },
    --
    --   -- Broker connection (same for both):
    --   broker: {
    --     type: 'alpaca' | 'binance' | 'interactive_brokers',
    --     api_credential_id: UUID,
    --     account_type: 'paper' | 'live',
    --     sandbox: true | false
    --   },
    --
    --   -- Strategy parameters (customizable):
    --   strategy: {
    --     [from strategy table]
    --     entry_offset: +0.0005,  -- User tweaks
    --     tp_offset: +0.0,
    --     sl_offset: +0.0,
    --     risk_percent_override: 1.5,
    --     [...]
    --   },
    --
    --   -- Monitoring & alerts:
    --   monitoring: {
    --     check_interval_seconds: 10,
    --     alert_on_entry: true,
    --     alert_on_exit: true,
    --     alert_on_error: true,
    --     notification_channels: ['push', 'email', 'sms']
    --   },
    --
    --   -- Advanced (si user quiere):
    --   advanced: {
    --     max_slippage_percent: 0.1,
    --     max_spread_points: 3,
    --     retry_failed_orders: true,
    --     auto_hedge: false,
    --     timezone_override: 'America/New_York'
    --   }
    -- }
  
  -- openClaw Agent ref
  openclaw_agent_id VARCHAR(255),  -- Assigned after deployment
  openclaw_session_id VARCHAR(255),  -- Current live session
  
  -- Status
  status VARCHAR(50) DEFAULT 'pending',
    -- 'pending' = created but not deployed
    -- 'deploying' = deployment in progress
    -- 'deployed' = ready to run
    -- 'initializing' = starting up
    -- 'monitoring' = live, waiting for signals
    -- 'executing' = actively trading
    -- 'paused' = user paused
    -- 'error' = something went wrong
    -- 'archived' = old config
  
  current_state JSONB,
    -- {
    --   positions_open: 1,
    --   last_price_check: '2026-03-19T09:10:15Z',
    --   monitoring_active: true,
    --   deployment_location: 'cloud' | 'hardware',
    --   hardware_online: true (if hardware),
    --   hardware_latency_ms: 25,
    --   trades_today: 3,
    --   pnl_today: 450
    -- }
  
  -- Error handling
  error_logs TEXT[],
  last_error TEXT,
  
  -- Metrics
  uptime_percent DECIMAL(5,2) DEFAULT 100,
  total_executions INT DEFAULT 0,
  total_pnl DECIMAL(15,2) DEFAULT 0,
  
  -- Chat/UI interactions
  created_via VARCHAR(50),  -- 'chat', 'marketplace_ui', 'api'
  created_via_conversation_id UUID REFERENCES conversations(id),  -- Link back to chat
  
  -- Timestamps
  created_at TIMESTAMP DEFAULT NOW(),
  deployed_at TIMESTAMP,
  updated_at TIMESTAMP DEFAULT NOW(),
  last_heartbeat TIMESTAMP,
  
  -- Indexes
  INDEX idx_strategy_id (strategy_id),
  INDEX idx_user_id (user_id),
  INDEX idx_status (status),
  INDEX idx_deployment_type ((deployment_config->>'deployment_type')),
  UNIQUE KEY unique_strategy_user (strategy_id, user_id)
);
```

---

## UX FLOW: USER CONFIGURES VIA CHAT

### Scenario 1: User wants CLOUD deployment

```
USER: "I want to activate this EUR/USD strategy 24/7"

CHAT INTERFACE (LLM response):
"Great! I can deploy this strategy for you.

Two options:

1️⃣ CLOUD (Racha servers)
   - Always on, no setup needed
   - $45/month for 24/7 execution
   - Fastest: ready in 1 minute
   
2️⃣ HARDWARE (Your own VPS/home)
   - Free (you pay host)
   - Full privacy, control
   - 5 minutes setup

Which prefer? Type 'cloud' or 'hardware'."

───────────────────────────────

USER: "cloud please, us-east-1"

CHAT RESPONSE:
"Perfect! Deploying to AWS us-east-1.

Configuration:
├─ Strategy: Soporte Bounce EUR/USD
├─ Broker: Alpaca paper trading
├─ Risk: 1.5% per trade
├─ Alerts: Push + Email
└─ Cost: $45/month

Ready? [CONFIRM] or customize >>

(If customize, can adjust risk, broker account type, etc)"

───────────────────────────────

USER: [CONFIRM]

SYSTEM CREATES:
├─ agent_configs row:
│  ├─ deployment_config.deployment_type = 'cloud'
│  ├─ deployment_config.cloud_config.region = 'us-east-1'
│  ├─ deployment_config.cloud_config.launch_on_create = true
│  └─ status = 'deploying'
│
├─ Calls OpenClaw API:
│  └─ "Deploy agent_config on us-east-1"
│
└─ Updates status → 'deployed' (in ~30 seconds)

NOTIFICATION:
"✅ Agent deployed! EUR/USD strategy now running 24/7.
 Current: Monitoring (waiting for entry signal)
 Dashboard: [View Live] [Pause] [Settings]"
```

---

### Scenario 2: User wants HARDWARE deployment

```
USER: "I want to run this on my home server"

CHAT RESPONSE:
"Smart choice! Running on your hardware = free & private.

Your home server specs:
├─ OS: ?
├─ CPU: ?
├─ Memory: ?
└─ Internet: ?

Tell me what you have (or just say 'linux', 'mac', 'windows')"

───────────────────────────────

USER: "I have Ubuntu 22.04 on AWS t3.medium"

CHAT RESPONSE:
"Perfect! Ubuntu t3.medium is plenty.

Here's what I'll do:

1. Generate pairing code (valid 24h)
2. Give you download + install script
3. You run it on your server
4. Auto-connects to Racha
5. Agent starts monitoring

Ready? [START SETUP]"

───────────────────────────────

USER: [START SETUP]

SYSTEM CREATES:
├─ agent_configs row:
│  ├─ deployment_config.deployment_type = 'hardware'
│  ├─ deployment_config.hardware_config.pairing_code = 'ABC-123-XYZ'
│  ├─ deployment_config.hardware_config.pairing_expires_at = +24h
│  ├─ deployment_config.hardware_config.download_url = 'https://...'
│  └─ status = 'pending'  (waiting for hardware to pair)
│
└─ Generates time-limited pairing code

CHAT RESPONSE:
"Setup instructions:

SSH into your server:
  ssh ubuntu@your-aws-instance

Run this:
  bash <(curl -s https://setup.racha.network/install.sh) \
    --pairing-code ABC-123-XYZ \
    --strategy-id abc123 \
    --user-token YOUR_TOKEN

Or download + run locally:
  [Download OpenClaw Agent v1.2.3]
  [Instructions PDF]

Pairing code expires in 24 hours.
Questions? [Chat with support]"

───────────────────────────────

USER: (Runs on their server)
└─ OpenClaw agent starts
   ├─ Reads pairing code
   ├─ Pairs with Racha
   ├─ Loads strategy config
   ├─ Connects broker API
   └─ Starts monitoring EUR/USD

RACHA DETECTS:
├─ hardware_deployment created
├─ agent_configs.status = 'deployed'
├─ agent_configs.current_state.deployment_location = 'hardware'
└─ agent_configs.current_state.hardware_online = true

NOTIFICATION TO USER:
"✅ Hardware paired! Your agent is now live on your server.
 Status: Monitoring (latency: 24ms)
 Dashboard: [View Live] [Settings] [Failover to Cloud]"
```

---

### Scenario 3: Configuration via TELEGRAM

```
User in private Telegram group "My Trading Bots":

USER: "@racha_bot activate EUR strategy on hardware"

RACHA BOT RESPONDS:
"Got it! I'll set up your EUR/USD strategy on hardware.

1. What's your server? (VPS/home/etc)
2. OS? (linux/mac/windows)
3. Confirm broker: Alpaca paper trading OK?

Just reply here or go to app for full setup."

───────────────────────────────

USER: "AWS Ubuntu, yes Alpaca paper"

RACHA BOT:
"Perfect! Pairing code: XYZ-789-DEF (24h valid)

[Get Installation Script]
[Full Setup in App]
[Help]

Once paired, I'll confirm here ✅"

───────────────────────────────

SAME FLOW:
├─ OpenClaw agent installed & paired
├─ agent_configs.created_via = 'telegram'
├─ agent_configs.created_via_channel = 'My Trading Bots'
└─ Status: deployed
```

---

## CHAT COMMANDS (LLM parsing)

The chat LLM understands natural language + commands:

```
User inputs → LLM interprets:

"Activate EUR strategy"
  → Intent: deploy agent
  → Strategy: find EUR/USD
  → Ask: cloud or hardware?

"Run this on my server"
  → Intent: hardware deployment
  → Ask: OS/specs?

"Use cloud, US region, max 2% risk"
  → Intent: cloud deployment
  → Config: { region: 'us-east-1', risk_percent: 2.0 }
  → Action: Deploy immediately

"Pause all agents"
  → Intent: pause all
  → Action: Update all agent_configs.status = 'paused'

"Show earnings from EUR strategy"
  → Intent: analytics
  → Query: creator_earnings for that strategy

"I want to monetize this strategy"
  → Intent: list on marketplace
  → Action: strategies.is_monetizable = true
```

---

## DEPLOYMENT_CONFIG Structure (Deep Dive)

### Cloud Deployment

```json
{
  "deployment_type": "cloud",
  "cloud_config": {
    "region": "us-east-1",
    "regions_available": [
      "us-east-1",
      "us-west-2",
      "eu-west-1",
      "ap-southeast-1"
    ],
    "launch_on_create": true,
    "redundancy": "single",
    "failover_to_hardware": false,
    "monthly_cost_estimate": 45,
    "included": ["24/7 monitoring", "auto-restarts", "support"]
  },
  "broker": {
    "type": "alpaca",
    "api_credential_id": "cred_xyz",
    "account_type": "paper",
    "sandbox": true
  },
  "strategy": {
    "entry_offset": 0.0005,
    "tp_offset": 0.0,
    "sl_offset": 0.0,
    "risk_percent": 1.5
  },
  "monitoring": {
    "check_interval_seconds": 10,
    "alert_on_entry": true,
    "alert_on_exit": true,
    "notification_channels": ["push", "email"]
  },
  "advanced": {
    "max_slippage_percent": 0.1,
    "timezone": "America/New_York"
  }
}
```

### Hardware Deployment

```json
{
  "deployment_type": "hardware",
  "hardware_config": {
    "hardware_type": "vps",
    "hardware_name": "AWS t3.medium",
    "os": "ubuntu",
    "os_version": "22.04",
    "pairing_code": "ABC-123-XYZ",
    "pairing_code_expires_at": "2026-03-20T09:10:00Z",
    "pairing_code_used": false,
    "openclaw_agent_version": "1.2.3",
    "download_url": "https://cdn.racha.network/agents/v1.2.3/linux/amd64",
    "system_requirements": {
      "os": ["linux", "macos", "windows"],
      "cpu_min": 2,
      "memory_min_gb": 4,
      "storage_min_gb": 50,
      "internet_speed_mbps_min": 5
    },
    "install_guide": "https://docs.racha.network/hardware-setup",
    "support_chat": true
  },
  "broker": {
    "type": "binance",
    "api_credential_id": "cred_abc",
    "account_type": "live",
    "sandbox": false
  },
  "strategy": {
    "entry_offset": 0.0,
    "tp_offset": 0.0,
    "sl_offset": 0.0,
    "risk_percent": 2.0
  },
  "monitoring": {
    "check_interval_seconds": 5,
    "alert_on_entry": true,
    "alert_on_exit": true,
    "alert_on_hardware_offline": true,
    "notification_channels": ["push", "email", "telegram"]
  },
  "advanced": {
    "max_slippage_percent": 0.15,
    "timezone": "Europe/Madrid",
    "failover_to_cloud": true
  }
}
```

---

## API ENDPOINTS: Configuration via Chat

```
POST /api/chat/parse-intent
├─ Input: user_message (text)
├─ LLM parses intent
└─ Response: {intent, strategy_id, deployment_type, params}

POST /api/agents/deploy-from-chat
├─ Input: {intent_parsed, conversation_id}
├─ Creates: agent_configs with deployment_config
├─ Deploys: to cloud OR waits for hardware pairing
└─ Response: {agent_id, pairing_code_if_hardware}

POST /api/agents/pair-hardware
├─ Input: {pairing_code, agent_id}
├─ Action: Links hardware to agent_configs
├─ Response: {hardware_deployment_id, status}

GET /api/agents/pairing-status/:pairing_code
├─ Check if hardware has paired yet
└─ Real-time polling from app

POST /api/agents/customize
├─ Input: {agent_id, updates}
├─ Updates: deployment_config.strategy / monitoring / advanced
├─ Response: {updated_config, needs_restart}

POST /api/telegram/setup-agent
├─ For @racha_bot commands
├─ Same flow as chat, but from Telegram
└─ Confirmation posted back to Telegram
```

---

## DATABASE DELTA from V0

### New in agent_configs:

```sql
-- Removed: specific columns
-- deployment_type VARCHAR(50)
-- hardware_location VARCHAR(255)
-- hardware_ip_address VARCHAR(50)
-- cpu_usage DECIMAL(5,2)
-- memory_usage DECIMAL(5,2)

-- Added: unified config
deployment_config JSONB NOT NULL  -- EVERYTHING in here

-- Added: chat tracking
created_via VARCHAR(50)
created_via_conversation_id UUID

-- Simplified: these are now in deployment_config JSON
-- openclaw_agent_id (same)
-- status (same)
-- current_state (same)
```

---

## SUMMARY FOR USER

```
WHAT CHANGED:

V0: Agent config = manual database entry
DEPLOYMENT V1: Agent config = conversational UI

USER EXPERIENCE:

"I want to run this strategy"
  ↓
Chat asks: "Cloud or hardware?"
  ↓
User replies naturally
  ↓
System auto-deploys + configures
  ↓
Agent running in < 5 minutes
  ↓
No terminal needed, no manual config
  ↓
Everything trackable from app/chat

TECHNICAL:

deployment_config = JSON blob
  ├─ Cloud: launch immediately
  ├─ Hardware: generate pairing code
  └─ Both: customizable from chat

Chat → LLM intent parsing
  → agent_configs created
  → OpenClaw deployed
  → User notified
```

---

## EXAMPLES OF CUSTOMIZATION VIA CHAT

```
"Use 2x risk on this"
  → deployment_config.strategy.risk_percent = 3.0

"Only trade NY session"
  → deployment_config.advanced.timezone = 'America/New_York'
  → deployment_config.monitoring.check_interval_seconds = 30

"Alert me on Telegram too"
  → deployment_config.monitoring.notification_channels.push('telegram')

"Pair with my AWS server in Tokyo"
  → deployment_config.hardware_config.hardware_config = {...}
  → deployment_config.hardware_config.region = 'ap-northeast-1'

"Use live Binance, not demo"
  → deployment_config.broker.account_type = 'live'
  → deployment_config.broker.sandbox = false
  → (REQUIRES: confirmation + 2FA)

All without leaving chat interface.
```
