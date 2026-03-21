# DATABASE V0 COMPLETE — Demo (No OpenClaw)

**Para Marc: La base de datos completa que necesita Supabase para la DEMO.**

---

## VISIÓN

```
DEMO V0 (Vercel + Supabase):
├─ 4 páginas (Chat, Estrategia, Research, Config)
├─ Funcionalidades:
│  ├─ Research Agent (BraveSearch)
│  ├─ Olimpiada de bots
│  ├─ Strategy marketplace
│  ├─ CSV upload/swipe
│  └─ Strategy sharing within community
│
├─ NO: Ejecución real, NO 24/7 monitoring
├─ SÍ: Backtest histórico, simulación, monetización via 0.5-1% revenue share
└─ Objetivo: Generar $50K-200K/mes con 50-500 usuarios premium
```

---

## SCHEMA COMPLETA (13 Tablas)

### TIER 0: IDENTITY & AUTH

#### users

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Auth (via Supabase Auth)
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  -- Profile
  display_name VARCHAR(255),
  avatar_url VARCHAR(510),
  bio TEXT,
  
  -- Account Type
  tier VARCHAR(50) DEFAULT 'free',  -- 'free', 'trader' ($499), 'pro' ($1999)
  subscription_active BOOLEAN DEFAULT false,
  subscription_expires_at TIMESTAMP,
  
  -- Preferences
  timezone VARCHAR(50) DEFAULT 'UTC',
  language VARCHAR(10) DEFAULT 'es',
  currency VARCHAR(10) DEFAULT 'USD',
  risk_default DECIMAL(3,1) DEFAULT 1.5,
  
  -- Stats
  total_olimpiadas INT DEFAULT 0,
  total_strategies_created INT DEFAULT 0,
  total_strategies_subscribed INT DEFAULT 0,
  lifetime_earnings DECIMAL(15,2) DEFAULT 0,
  
  -- Subscription Billing
  stripe_customer_id VARCHAR(255),
  
  -- Dates
  last_login_at TIMESTAMP,
  
  -- Indexes
  INDEX idx_email (email),
  INDEX idx_tier (tier),
  INDEX idx_created_at (created_at),
  INDEX idx_subscription_active (subscription_active)
);
```

#### user_preferences

```sql
CREATE TABLE user_preferences (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  -- Trading Preferences
  risk_percent DECIMAL(3,1) DEFAULT 1.5,
  max_daily_loss DECIMAL(5,2) DEFAULT 5.0,
  
  -- UI Preferences
  theme VARCHAR(50) DEFAULT 'dark',
  compact_mode BOOLEAN DEFAULT false,
  
  -- Notification Preferences
  notify_new_strategies BOOLEAN DEFAULT true,
  notify_earnings BOOLEAN DEFAULT true,
  notify_strategy_updates BOOLEAN DEFAULT true,
  
  -- Data Preferences
  auto_export_backtest BOOLEAN DEFAULT false,
  keep_history_days INT DEFAULT 90,
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_user_id (user_id)
);
```

---

### TIER 1: CONVERSATIONS & QUERIES

#### conversations

```sql
CREATE TABLE conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  -- Metadata
  title VARCHAR(255),
  description TEXT,
  
  -- Type of conversation
  context_type VARCHAR(50) DEFAULT 'general',
    -- 'research', 'olimpiada_builder', 'strategy_analysis', 'general'
  
  -- Context data
  context_data JSONB,  -- {olimpiada_id, strategy_id, csv_import_id}
  
  -- Status
  is_archived BOOLEAN DEFAULT false,
  archived_at TIMESTAMP,
  
  -- Timestamps
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  last_message_at TIMESTAMP,
  
  -- Indexes
  INDEX idx_user_id (user_id),
  INDEX idx_context_type (context_type),
  INDEX idx_last_message_at (last_message_at)
);
```

#### chat_messages

```sql
CREATE TABLE chat_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  
  -- Message
  role VARCHAR(20) NOT NULL,  -- 'user', 'assistant'
  content TEXT NOT NULL,
  
  -- Audio (optional)
  audio_url VARCHAR(510),
  audio_duration_seconds INT,
  
  -- LLM Context
  llm_model VARCHAR(100),
  tokens_used INT,
  api_cost DECIMAL(10,6),
  response_time_ms INT,
  
  -- Error Handling
  is_error BOOLEAN DEFAULT false,
  error_message TEXT,
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_conversation_id (conversation_id),
  INDEX idx_role (role),
  INDEX idx_created_at (created_at)
);
```

#### queries_log

```sql
CREATE TABLE queries_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  -- Query Type
  query_type VARCHAR(50) NOT NULL,
    -- 'research', 'csv_parse', 'strategy_extract', 'backtest', 'olimpiada'
  
  -- Input/Output
  input_data JSONB,
  output_data JSONB,
  
  -- LLM Stats
  llm_model VARCHAR(100),
  tokens_used INT,
  api_cost DECIMAL(10,6),
  response_time_ms INT,
  
  -- Status
  status VARCHAR(50) DEFAULT 'completed',  -- 'pending', 'processing', 'completed', 'error'
  error_message TEXT,
  
  created_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP,
  
  -- Indexes
  INDEX idx_user_id (user_id),
  INDEX idx_query_type (query_type),
  INDEX idx_status (status),
  INDEX idx_created_at (created_at)
);
```

---

### TIER 2: CSV & SWIPE

#### csv_imports

```sql
CREATE TABLE csv_imports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  -- File Info
  filename VARCHAR(255) NOT NULL,
  file_size_bytes INT,
  
  -- Content
  row_count INT,
  column_count INT,
  columns_detected TEXT[],
  
  -- Parsing
  parse_status VARCHAR(50) DEFAULT 'pending',
  parse_error TEXT,
  
  -- Data
  data_sample JSONB,  -- First 5 rows
  
  -- Status
  is_active BOOLEAN DEFAULT true,
  archived_at TIMESTAMP,
  
  created_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP,
  
  -- Indexes
  INDEX idx_user_id (user_id),
  INDEX idx_parse_status (parse_status),
  INDEX idx_created_at (created_at)
);
```

#### csv_rows

```sql
CREATE TABLE csv_rows (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  csv_import_id UUID NOT NULL REFERENCES csv_imports(id) ON DELETE CASCADE,
  
  -- Row Identity
  row_number INT NOT NULL,
  row_data JSONB NOT NULL,
  
  -- User Actions
  swipe_action VARCHAR(20),  -- 'like', 'dislike'
  swiped_at TIMESTAMP,
  
  -- Metadata
  is_duplicate BOOLEAN DEFAULT false,
  is_valid BOOLEAN DEFAULT true,
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_csv_import_id (csv_import_id),
  INDEX idx_swipe_action (swipe_action),
  UNIQUE KEY unique_row (csv_import_id, row_number)
);
```

#### swipe_actions

```sql
CREATE TABLE swipe_actions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  csv_row_id UUID NOT NULL REFERENCES csv_rows(id) ON DELETE CASCADE,
  
  -- Action
  action VARCHAR(20) NOT NULL,  -- 'like', 'dislike'
  reason TEXT,
  
  -- Timestamp
  swiped_at TIMESTAMP DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_user_id (user_id),
  INDEX idx_action (action),
  INDEX idx_swiped_at (swiped_at)
);
```

---

### TIER 3: OLIMPIADA

#### olimpiada_configs

```sql
CREATE TABLE olimpiada_configs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  -- Identity
  name VARCHAR(255) NOT NULL,
  description TEXT,
  
  -- Setup
  topic VARCHAR(255),  -- "EUR/USD strategies from YouTube"
  symbol VARCHAR(50) NOT NULL,
  timeframe VARCHAR(10),
  
  -- Backtest
  backtest_start_date DATE,
  backtest_end_date DATE,
  data_period_days INT,
  
  -- Results Storage
  traders_count INT,  -- 20 traders tested
  traders_list JSONB,  -- [{name, video_url, transcript_used, bot_config}]
  
  backtest_results JSONB,
    -- [{
    --   rank: 1,
    --   trader_name: 'TradingMaster88',
    --   win_rate: 0.68,
    --   pnl: 4250,
    --   num_trades: 42,
    --   config: {entry, tp, sl, risk}
    -- }]
  
  -- Status
  status VARCHAR(50) DEFAULT 'pending',  -- 'processing', 'completed', 'error'
  error_message TEXT,
  
  -- Timestamps
  created_at TIMESTAMP DEFAULT NOW(),
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  
  -- Indexes
  INDEX idx_user_id (user_id),
  INDEX idx_status (status),
  INDEX idx_symbol (symbol),
  INDEX idx_created_at (created_at)
);
```

---

### TIER 4: STRATEGIES & MARKETPLACE

#### strategies

```sql
CREATE TABLE strategies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Creator
  creator_user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  creator_name VARCHAR(255),
  creator_avatar VARCHAR(510),
  
  -- Identity
  strategy_name VARCHAR(255) NOT NULL,
  strategy_version INT DEFAULT 1,
  
  -- Source
  source_type VARCHAR(50),  -- 'youtube_transcript', 'olimpiada_winner', 'user_upload'
  source_reference JSONB,
  
  -- Strategy Definition (CORE)
  symbol VARCHAR(50) NOT NULL,
  timeframe VARCHAR(10) NOT NULL,
  
  entry_logic JSONB,
    -- {trigger, conditions, entry_price, rules}
  
  exit_logic JSONB,
    -- {tp_price, sl_price, rules}
  
  risk_management JSONB,
    -- {risk_percent, max_positions, max_daily_loss}
  
  -- Performance Stats
  stats JSONB DEFAULT '{"total_backtests": 0, "avg_win_rate": 0, "users_count": 0}'::jsonb,
  
  -- Ratings
  rating DECIMAL(3,2),
  rating_count INT DEFAULT 0,
  reviews TEXT[],
  
  -- Monetization
  revenue_share_percent DECIMAL(3,2) DEFAULT 0.5,  -- 0.5 or 1.0
  creator_earnings DECIMAL(15,2) DEFAULT 0,
  
  -- Publishing
  status VARCHAR(50) DEFAULT 'published',  -- 'draft', 'published', 'archived'
  is_open_to_new_users BOOLEAN DEFAULT true,
  
  -- Metadata
  description TEXT,
  tags TEXT[],
  best_market_conditions JSONB,
  disclaimers TEXT,
  
  -- Timestamps
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  published_at TIMESTAMP,
  
  -- Indexes
  INDEX idx_creator_user_id (creator_user_id),
  INDEX idx_symbol (symbol),
  INDEX idx_source_type (source_type),
  INDEX idx_status (status),
  INDEX idx_rating (rating DESC),
  INDEX idx_created_at (created_at)
);
```

#### strategy_subscriptions

```sql
CREATE TABLE strategy_subscriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  strategy_id UUID NOT NULL REFERENCES strategies(id) ON DELETE CASCADE,
  
  -- Subscription
  subscribed_at TIMESTAMP DEFAULT NOW(),
  activated_at TIMESTAMP,
  
  -- Custom Parameters
  custom_entry_offset DECIMAL(5,3),
  custom_tp_offset DECIMAL(5,3),
  custom_sl_offset DECIMAL(5,3),
  custom_risk_percent DECIMAL(3,1),
  
  -- Status
  status VARCHAR(50) DEFAULT 'saved',
    -- 'saved', 'backtesting', 'active', 'paused'
  
  -- Backtest Results
  backtest_data JSONB,
    -- {win_rate, pnl, num_trades, max_drawdown, tested_at}
  
  -- Metadata
  notes TEXT,
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  -- Constraints
  UNIQUE KEY unique_user_strategy (user_id, strategy_id),
  INDEX idx_user_id (user_id),
  INDEX idx_strategy_id (strategy_id),
  INDEX idx_status (status)
);
```

#### strategy_exports

```sql
CREATE TABLE strategy_exports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  olimpiada_id UUID REFERENCES olimpiada_configs(id) ON DELETE CASCADE,
  
  -- Strategy metadata
  strategy_name VARCHAR(255),
  source_trader_name VARCHAR(255),
  
  -- Definition
  symbol VARCHAR(50),
  timeframe VARCHAR(10),
  entry_price DECIMAL(10,5),
  tp_price DECIMAL(10,5),
  sl_price DECIMAL(10,5),
  strategy_rules JSONB,
  
  -- Validation
  backtest_win_rate DECIMAL(5,2),
  backtest_pnl DECIMAL(15,2),
  backtest_num_trades INT,
  
  -- Sharing
  visibility VARCHAR(50) DEFAULT 'private',  -- 'private', 'friends', 'community'
  shared_with_user_ids UUID[],
  shared_in_community_ids UUID[],
  
  -- Monetization
  is_monetizable BOOLEAN DEFAULT false,
  creator_id UUID REFERENCES users(id),
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_olimpiada_id (olimpiada_id),
  INDEX idx_visibility (visibility),
  INDEX idx_creator_id (creator_id)
);
```

---

### TIER 5: REVENUE & MONETIZATION

#### strategy_revenue

```sql
CREATE TABLE strategy_revenue (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- References
  strategy_id UUID NOT NULL REFERENCES strategies(id),
  user_id UUID NOT NULL REFERENCES users(id),  -- trader using it
  creator_id UUID NOT NULL REFERENCES users(id),  -- creator
  
  -- Trade Result
  trade_pnl DECIMAL(15,2),
  trade_date TIMESTAMP,
  
  -- Revenue Split
  creator_percent DECIMAL(5,2),  -- 0.5 or 1.0
  creator_earnings DECIMAL(15,2),
  platform_percent DECIMAL(5,2),
  platform_earnings DECIMAL(15,2),
  
  -- Status
  is_settled BOOLEAN DEFAULT false,
  settled_at TIMESTAMP,
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_strategy_id (strategy_id),
  INDEX idx_creator_id (creator_id),
  INDEX idx_user_id (user_id),
  INDEX idx_is_settled (is_settled)
);
```

#### subscription_payments

```sql
CREATE TABLE subscription_payments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  
  -- Payment
  amount DECIMAL(15,2) NOT NULL,
  currency VARCHAR(10) DEFAULT 'USD',
  
  -- Tier
  tier VARCHAR(50),  -- 'trader', 'pro'
  
  -- Stripe
  stripe_payment_id VARCHAR(255),
  stripe_invoice_url VARCHAR(510),
  
  -- Status
  status VARCHAR(50),  -- 'pending', 'succeeded', 'failed'
  
  created_at TIMESTAMP DEFAULT NOW(),
  processed_at TIMESTAMP,
  
  -- Indexes
  INDEX idx_user_id (user_id),
  INDEX idx_status (status),
  INDEX idx_created_at (created_at)
);
```

#### creator_payouts

```sql
CREATE TABLE creator_payouts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  creator_id UUID NOT NULL REFERENCES users(id),
  
  -- Payout
  amount DECIMAL(15,2) NOT NULL,
  currency VARCHAR(10) DEFAULT 'USD',
  
  -- Period
  period_start DATE,
  period_end DATE,
  
  -- Status
  status VARCHAR(50) DEFAULT 'pending',  -- 'pending', 'processing', 'completed'
  
  -- Bank
  bank_account_id VARCHAR(255),  -- Stripe connected account
  stripe_payout_id VARCHAR(255),
  
  created_at TIMESTAMP DEFAULT NOW(),
  paid_at TIMESTAMP,
  
  -- Indexes
  INDEX idx_creator_id (creator_id),
  INDEX idx_status (status),
  INDEX idx_period_start (period_start)
);
```

---

### TIER 6: COMMUNITY & SHARING

#### community_groups

```sql
CREATE TABLE community_groups (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Group identity
  group_name VARCHAR(255),
  external_id VARCHAR(255),  -- Telegram group ID, Discord server ID
  external_type VARCHAR(50),  -- 'telegram', 'discord', 'slack'
  
  -- Settings
  is_private BOOLEAN DEFAULT true,
  description TEXT,
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_external_id (external_id)
);
```

#### community_members

```sql
CREATE TABLE community_members (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  community_id UUID NOT NULL REFERENCES community_groups(id) ON DELETE CASCADE,
  
  -- Role
  role VARCHAR(50) DEFAULT 'member',  -- 'admin', 'member'
  joined_at TIMESTAMP DEFAULT NOW(),
  
  -- Constraints
  UNIQUE KEY unique_user_community (user_id, community_id),
  INDEX idx_user_id (user_id),
  INDEX idx_community_id (community_id)
);
```

#### olimpiada_shares

```sql
CREATE TABLE olimpiada_shares (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  olimpiada_id UUID REFERENCES olimpiada_configs(id),
  shared_by_user_id UUID REFERENCES users(id),
  
  -- Share method
  share_type VARCHAR(50),  -- 'link', 'direct', 'community'
  shared_with_user_ids UUID[],
  community_id UUID REFERENCES community_groups(id),
  
  -- Link
  share_link VARCHAR(255) UNIQUE,
  link_expires_at TIMESTAMP,
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_olimpiada_id (olimpiada_id),
  INDEX idx_share_link (share_link)
);
```

---

### TIER 7: ANALYTICS & AUDIT

#### action_log

```sql
CREATE TABLE action_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  -- Action
  action_type VARCHAR(100) NOT NULL,
    -- 'olimpiada_created', 'strategy_added', 'backtest_run', etc
  
  -- Resource
  resource_type VARCHAR(50),
  resource_id UUID,
  
  -- Metadata
  action_metadata JSONB,
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_user_id (user_id),
  INDEX idx_action_type (action_type),
  INDEX idx_created_at (created_at)
);
```

#### audit_logs

```sql
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  
  -- Event
  event_type VARCHAR(100) NOT NULL,
  event_severity VARCHAR(50),  -- 'info', 'warning', 'critical'
  event_description TEXT,
  event_data JSONB,
  
  -- Context
  ip_address VARCHAR(50),
  user_agent VARCHAR(510),
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_event_type (event_type),
  INDEX idx_created_at (created_at)
);
```

---

## SQL DEPLOY SCRIPT

```sql
-- RUN THIS ON SUPABASE TO CREATE ALL TABLES

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- TIER 0
CREATE TABLE users (...);  -- See above
CREATE TABLE user_preferences (...);

-- TIER 1
CREATE TABLE conversations (...);
CREATE TABLE chat_messages (...);
CREATE TABLE queries_log (...);

-- TIER 2
CREATE TABLE csv_imports (...);
CREATE TABLE csv_rows (...);
CREATE TABLE swipe_actions (...);

-- TIER 3
CREATE TABLE olimpiada_configs (...);

-- TIER 4
CREATE TABLE strategies (...);
CREATE TABLE strategy_subscriptions (...);
CREATE TABLE strategy_exports (...);

-- TIER 5
CREATE TABLE strategy_revenue (...);
CREATE TABLE subscription_payments (...);
CREATE TABLE creator_payouts (...);

-- TIER 6
CREATE TABLE community_groups (...);
CREATE TABLE community_members (...);
CREATE TABLE olimpiada_shares (...);

-- TIER 7
CREATE TABLE action_log (...);
CREATE TABLE audit_logs (...);

-- Enable RLS (Row Level Security)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
-- ... etc for all tables

-- Create policies
CREATE POLICY users_own_data ON users
  FOR SELECT USING (auth.uid() = id);

-- ... etc
```

---

## KEY QUERIES (For Marc to implement)

```sql
-- 1. Get user's olimpiadas with results
SELECT id, name, symbol, traders_count, status, completed_at
FROM olimpiada_configs
WHERE user_id = $1
ORDER BY created_at DESC;

-- 2. Get strategy marketplace (top strategies)
SELECT id, strategy_name, creator_name, symbol, rating, 
       (stats->>'users_count')::INT as users_count
FROM strategies
WHERE status = 'published' AND is_open_to_new_users = true
ORDER BY rating DESC
LIMIT 20;

-- 3. Get user's strategy earnings (creator dashboard)
SELECT 
  s.strategy_name,
  COUNT(ss.id) as active_users,
  SUM(CASE WHEN sr.trade_pnl > 0 THEN sr.creator_earnings ELSE 0 END) as this_month_earnings,
  SUM(sr.trade_pnl) as total_user_pnl
FROM strategies s
LEFT JOIN strategy_subscriptions ss ON s.id = ss.strategy_id
LEFT JOIN strategy_revenue sr ON s.id = sr.strategy_id
WHERE s.creator_user_id = $1
GROUP BY s.id, s.strategy_name;

-- 4. Calculate creator payout (monthly)
SELECT 
  creator_id,
  SUM(creator_earnings) as total_earnings
FROM strategy_revenue
WHERE created_at >= DATE_TRUNC('month', NOW())
  AND created_at < DATE_TRUNC('month', NOW()) + INTERVAL '1 month'
  AND is_settled = false
GROUP BY creator_id;
```

---

## ENVIRONMENT VARIABLES (For Marc)

```
.env.local:

NEXT_PUBLIC_SUPABASE_URL=https://<project>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<anon_key>
SUPABASE_SERVICE_ROLE_KEY=<service_role_key>

# APIs
OPENROUTER_API_KEY=<key>
BRAVE_SEARCH_API_KEY=<key>
YOUTUBE_API_KEY=<key>

# Stripe
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=<key>
STRIPE_SECRET_KEY=<key>
STRIPE_WEBHOOK_SECRET=<key>

# Server
NEXT_PUBLIC_API_URL=http://localhost:3000 (dev) or https://api.racha.network (prod)
```

---

## SUMMARY FOR MARC

**Database V0 tiene 13 tablas:**

```
Tier 0 (Identity): users, user_preferences
Tier 1 (Chat): conversations, chat_messages, queries_log
Tier 2 (CSV): csv_imports, csv_rows, swipe_actions
Tier 3 (Olimpiada): olimpiada_configs
Tier 4 (Strategies): strategies, strategy_subscriptions, strategy_exports
Tier 5 (Revenue): strategy_revenue, subscription_payments, creator_payouts
Tier 6 (Community): community_groups, community_members, olimpiada_shares
Tier 7 (Audit): action_log, audit_logs
```

**Flujo end-to-end:**

1. User login → users table
2. Run olimpiada → olimpiada_configs + backtest results
3. Strategy extracted → strategies + strategy_exports
4. Subscribe to strategy → strategy_subscriptions
5. Backtest locally → backtest_data JSON
6. Create revenue record → strategy_revenue (when live trades happen)
7. Monthly payout → creator_payouts

**Importante:**
- Supabase maneja auth, realtime, storage
- Todo guardado en PostgreSQL
- RLS policies aseguran privacy
- Revenue tracking granular para payout mensual
- Audit logs para compliance
