# DATABASE V0 — SUPABASE SCHEMA (Sin OpenClaw)

## VISIÓN GENERAL

```
┌─────────────────────────────────────────────────────┐
│         SUPABASE (PostgreSQL)                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  TIER 1: IDENTITY & CONFIG                         │
│  ├─ users                                           │
│  ├─ user_preferences                                │
│  └─ api_credentials (encrypted)                     │
│                                                     │
│  TIER 2: DATA IMPORT & STORAGE                      │
│  ├─ csv_imports (uploaded files)                    │
│  ├─ csv_rows (parsed data)                          │
│  └─ swipe_actions (like/dislike)                    │
│                                                     │
│  TIER 3: CONVERSATION & QUERIES                     │
│  ├─ conversations (chat history)                    │
│  ├─ chat_messages                                   │
│  └─ queries_log (all API calls)                     │
│                                                     │
│  TIER 4: BOT CONFIGURATION & EXECUTION              │
│  ├─ bot_configs (user bots)                         │
│  ├─ bot_backtests (historical tests)                │
│  ├─ bot_queries (LLM analysis for bots)             │
│  └─ bot_executions (simulation results)             │
│                                                     │
│  TIER 5: ANALYTICS & FEEDBACK                       │
│  ├─ action_log (all user actions)                   │
│  ├─ mlm_feedback (for future OpenClaw)              │
│  └─ audit_logs (security events)                    │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## TABLAS DETALLADAS

### TIER 1: IDENTITY & CONFIG

#### 1.1 users

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Auth (via Supabase Auth)
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  -- Profile
  display_name VARCHAR(255),
  avatar_url VARCHAR(510),
  bio TEXT,
  
  -- Settings
  timezone VARCHAR(50) DEFAULT 'UTC',
  language VARCHAR(10) DEFAULT 'es',
  currency VARCHAR(10) DEFAULT 'USD',
  
  -- Preferences
  risk_default DECIMAL(3,1) DEFAULT 1.5,  -- % per trade
  auto_backtest BOOLEAN DEFAULT true,
  notifications_enabled BOOLEAN DEFAULT true,
  
  -- Broker
  primary_broker VARCHAR(50),  -- 'tradingview', 'binance', 'investing'
  
  -- Metadata
  last_login_at TIMESTAMP,
  total_bots_created INT DEFAULT 0,
  total_queries INT DEFAULT 0,
  
  -- Indexes
  INDEX idx_email (email),
  INDEX idx_created_at (created_at)
);

-- Add updated_at trigger
CREATE TRIGGER update_users_timestamp
BEFORE UPDATE ON users
FOR EACH ROW
SET updated_at = NOW();
```

#### 1.2 user_preferences

```sql
CREATE TABLE user_preferences (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  -- Trading Preferences
  risk_percent DECIMAL(3,1) DEFAULT 1.5,
  max_daily_loss DECIMAL(5,2) DEFAULT 5.0,
  max_positions INT DEFAULT 3,
  
  -- UI Preferences
  theme VARCHAR(50) DEFAULT 'dark',  -- 'light', 'dark', 'auto'
  compact_mode BOOLEAN DEFAULT false,
  show_charts BOOLEAN DEFAULT true,
  
  -- Notification Preferences
  notify_on_bot_trigger BOOLEAN DEFAULT true,
  notify_on_tp_hit BOOLEAN DEFAULT true,
  notify_on_sl_hit BOOLEAN DEFAULT true,
  notify_on_query_complete BOOLEAN DEFAULT true,
  
  -- Data Preferences
  export_format VARCHAR(20) DEFAULT 'json',  -- 'json', 'csv', 'xlsx'
  auto_archive_after_days INT DEFAULT 30,
  keep_backtest_history BOOLEAN DEFAULT true,
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_user_id (user_id)
);
```

#### 1.3 api_credentials

```sql
CREATE TABLE api_credentials (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  -- Broker Identity
  broker VARCHAR(50) NOT NULL,  -- 'tradingview', 'binance', 'investing'
  broker_username VARCHAR(255),
  
  -- Encrypted Credentials
  api_key TEXT,  -- ENCRYPTED before insert (via Supabase pgcrypto)
  api_secret TEXT,  -- ENCRYPTED
  passphrase TEXT,  -- ENCRYPTED (if needed)
  
  -- Session
  session_token TEXT ENCRYPTED,  -- for browser-based auth
  token_expires_at TIMESTAMP,
  refresh_token TEXT ENCRYPTED,
  
  -- Status
  is_active BOOLEAN DEFAULT true,
  is_verified BOOLEAN DEFAULT false,
  last_verified_at TIMESTAMP,
  
  -- Audit
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  last_used_at TIMESTAMP,
  
  -- Constraints
  UNIQUE KEY unique_user_broker (user_id, broker),
  INDEX idx_user_id (user_id),
  INDEX idx_broker (broker),
  INDEX idx_active (is_active)
);

-- Note: Use pgcrypto extension for encryption
-- CREATE EXTENSION IF NOT EXISTS pgcrypto;
-- INSERT usage: api_key = pgp_sym_encrypt(api_key, 'secret_key')
-- SELECT usage: api_key = pgp_sym_decrypt(api_key, 'secret_key')
```

---

### TIER 2: DATA IMPORT & STORAGE

#### 2.1 csv_imports

```sql
CREATE TABLE csv_imports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  -- File Info
  filename VARCHAR(255) NOT NULL,
  original_filename VARCHAR(255),
  file_type VARCHAR(20),  -- 'csv', 'json', 'xlsx'
  file_size_bytes INT,
  
  -- Content Metadata
  row_count INT,
  column_count INT,
  columns_detected TEXT[],  -- Array: ['name', 'email', 'company']
  
  -- Parsing
  parse_status VARCHAR(50) DEFAULT 'pending',  -- 'pending', 'parsing', 'complete', 'error'
  parse_error TEXT,
  
  -- Content
  data_sample JSONB,  -- First 5 rows (for preview)
  data_full JSONB,    -- Full data (if small) or NULL if large
  data_storage_path VARCHAR(255),  -- If stored in S3: 's3://bucket/path'
  
  -- Processing
  llm_classification JSONB,  -- {columns: {name: 'person_name', email: 'email_address'}}
  processing_mode VARCHAR(50) DEFAULT 'auto',  -- 'auto', 'manual'
  
  -- Status
  is_active BOOLEAN DEFAULT true,
  archived_at TIMESTAMP,
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP,
  
  -- Indexes
  INDEX idx_user_id (user_id),
  INDEX idx_parse_status (parse_status),
  INDEX idx_created_at (created_at)
);
```

#### 2.2 csv_rows

```sql
CREATE TABLE csv_rows (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  csv_import_id UUID NOT NULL REFERENCES csv_imports(id) ON DELETE CASCADE,
  
  -- Row Identity
  row_number INT NOT NULL,
  row_hash VARCHAR(64),  -- SHA256 of row content (for dedup)
  
  -- Row Data
  row_data JSONB NOT NULL,  -- {name: 'John', email: 'john@...', company: 'Acme'}
  
  -- User Actions
  swipe_action VARCHAR(20),  -- 'like', 'dislike', null (not swiped yet)
  swipe_at TIMESTAMP,
  
  -- Metadata
  is_duplicate BOOLEAN DEFAULT false,
  is_valid BOOLEAN DEFAULT true,
  validation_errors TEXT[],
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_csv_import_id (csv_import_id),
  INDEX idx_row_number (csv_import_id, row_number),
  INDEX idx_swipe_action (swipe_action),
  UNIQUE KEY unique_row (csv_import_id, row_number)
);
```

#### 2.3 swipe_actions

```sql
CREATE TABLE swipe_actions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  csv_import_id UUID NOT NULL REFERENCES csv_imports(id) ON DELETE CASCADE,
  csv_row_id UUID NOT NULL REFERENCES csv_rows(id) ON DELETE CASCADE,
  
  -- Action
  action VARCHAR(20) NOT NULL,  -- 'like', 'dislike', 'undo'
  reason VARCHAR(255),  -- optional user note
  
  -- Context
  swiped_at TIMESTAMP DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_user_id (user_id),
  INDEX idx_csv_import_id (csv_import_id),
  INDEX idx_action (action),
  INDEX idx_swiped_at (swiped_at)
);

-- View: Liked rows
CREATE VIEW liked_rows AS
SELECT DISTINCT
  cr.id,
  cr.csv_import_id,
  cr.row_number,
  cr.row_data,
  MAX(sa.swiped_at) as last_swiped_at
FROM csv_rows cr
JOIN swipe_actions sa ON cr.id = sa.csv_row_id
WHERE sa.action = 'like'
GROUP BY cr.id, cr.csv_import_id, cr.row_number, cr.row_data
ORDER BY cr.row_number;

-- View: Disliked rows
CREATE VIEW disliked_rows AS
SELECT DISTINCT
  cr.id,
  cr.csv_import_id,
  cr.row_number,
  cr.row_data,
  MAX(sa.swiped_at) as last_swiped_at
FROM csv_rows cr
JOIN swipe_actions sa ON cr.id = sa.csv_row_id
WHERE sa.action = 'dislike'
GROUP BY cr.id, cr.csv_import_id, cr.row_number, cr.row_data
ORDER BY cr.row_number;
```

---

### TIER 3: CONVERSATION & QUERIES

#### 3.1 conversations

```sql
CREATE TABLE conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  -- Metadata
  title VARCHAR(255),  -- "CSV Upload - Prospects Q1"
  description TEXT,
  
  -- Context
  context_type VARCHAR(50),  -- 'csv_analysis', 'bot_config', 'market_analysis', 'general'
  context_data JSONB,  -- {csv_import_id: '...', bot_id: '...'}
  
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

#### 3.2 chat_messages

```sql
CREATE TABLE chat_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  
  -- Message
  role VARCHAR(20) NOT NULL,  -- 'user', 'assistant'
  content TEXT NOT NULL,
  
  -- Audio (if voice)
  audio_url VARCHAR(510),
  audio_duration_seconds INT,
  
  -- LLM Context
  llm_model VARCHAR(100),  -- 'gpt-4-turbo-mini', 'claude-3-haiku', etc
  tokens_used INT,
  api_cost DECIMAL(10,6),
  
  -- Response Metadata
  response_time_ms INT,
  is_error BOOLEAN DEFAULT false,
  error_message TEXT,
  
  -- References
  referenced_query_id UUID,  -- Link to queries_log if this is a response
  referenced_bot_id UUID,    -- Link to bot if this is about a specific bot
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_conversation_id (conversation_id),
  INDEX idx_role (role),
  INDEX idx_created_at (created_at),
  INDEX idx_referenced_query_id (referenced_query_id)
);
```

#### 3.3 queries_log

```sql
CREATE TABLE queries_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  conversation_id UUID REFERENCES conversations(id) ON DELETE SET NULL,
  
  -- Query Type
  query_type VARCHAR(50) NOT NULL,  -- 'csv_parse', 'csv_classify', 'market_analysis', 'bot_create', 'backtest'
  
  -- Input
  query_input JSONB,  -- {csv_import_id, csv_rows: [...], columns: [...]}
  
  -- LLM Call
  llm_model VARCHAR(100),
  prompt_tokens INT,
  completion_tokens INT,
  total_tokens INT,
  
  -- Output
  query_output JSONB,  -- {status, result, classification, analysis}
  api_response_time_ms INT,
  api_cost DECIMAL(10,6),
  
  -- Status
  status VARCHAR(50) DEFAULT 'pending',  -- 'pending', 'processing', 'complete', 'error'
  error_message TEXT,
  
  -- Correlation
  batch_id VARCHAR(100),  -- group related queries
  
  created_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP,
  
  -- Indexes
  INDEX idx_user_id (user_id),
  INDEX idx_query_type (query_type),
  INDEX idx_status (status),
  INDEX idx_created_at (created_at),
  INDEX idx_batch_id (batch_id)
);

-- View: Query Cost by Type
CREATE VIEW query_costs_by_type AS
SELECT
  query_type,
  COUNT(*) as query_count,
  SUM(api_cost) as total_cost,
  AVG(api_cost) as avg_cost,
  MAX(api_response_time_ms) as max_response_ms
FROM queries_log
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY query_type
ORDER BY total_cost DESC;
```

---

### TIER 4: BOT CONFIGURATION & EXECUTION

#### 4.1 bot_configs

```sql
CREATE TABLE bot_configs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  -- Identity
  bot_name VARCHAR(255) NOT NULL,
  description TEXT,
  
  -- Broker Connection
  broker VARCHAR(50) NOT NULL,  -- 'tradingview', 'binance', 'investing'
  broker_account_id VARCHAR(255),  -- Account identifier
  api_credential_id UUID REFERENCES api_credentials(id) ON DELETE SET NULL,
  
  -- Trading Parameters
  symbol VARCHAR(50) NOT NULL,  -- EUR_USD, BTC_USD, etc
  timeframe VARCHAR(10),  -- 1m, 5m, 15m, 1h, 4h, daily
  
  -- Entry/Exit Levels
  entry_price DECIMAL(10,5),
  tp_price DECIMAL(10,5),
  sl_price DECIMAL(10,5),
  
  -- Risk Management
  risk_percent DECIMAL(3,1),
  position_size INT,  -- qty or amount
  max_positions INT DEFAULT 1,
  max_daily_loss DECIMAL(5,2),
  
  -- Strategy
  strategy_type VARCHAR(50),  -- 'manual', 'pattern_based', 'technical'
  strategy_rules JSONB,  -- {rule1: 'soporte', rule2: 'volumen'}
  
  -- Status
  is_active BOOLEAN DEFAULT false,
  is_paper_trading BOOLEAN DEFAULT true,  -- Paper vs Live
  
  -- Backtest Reference
  backtest_id UUID REFERENCES bot_backtests(id) ON DELETE SET NULL,
  
  -- Metadata
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  activated_at TIMESTAMP,
  
  -- Indexes
  INDEX idx_user_id (user_id),
  INDEX idx_is_active (is_active),
  INDEX idx_symbol (symbol),
  INDEX idx_created_at (created_at)
);
```

#### 4.2 bot_backtests

```sql
CREATE TABLE bot_backtests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  bot_config_id UUID NOT NULL REFERENCES bot_configs(id) ON DELETE CASCADE,
  
  -- Backtest Period
  backtest_start_date DATE,
  backtest_end_date DATE,
  data_points INT,
  
  -- Results
  total_trades INT,
  winning_trades INT,
  losing_trades INT,
  win_rate DECIMAL(5,2),
  
  -- P&L
  total_pnl DECIMAL(15,2),
  avg_win DECIMAL(15,2),
  avg_loss DECIMAL(15,2),
  profit_factor DECIMAL(5,2),
  
  -- Drawdown
  max_drawdown DECIMAL(5,2),
  max_drawdown_date DATE,
  
  -- Trade Details
  trades_detail JSONB,  -- [{entry: 1.0875, exit: 1.0750, pnl: 1250, duration_mins: 45}]
  
  -- Metadata
  llm_analysis JSONB,  -- {summary: '...', recommendation: '...', risk_assessment: '...'}
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_bot_config_id (bot_config_id),
  INDEX idx_created_at (created_at)
);
```

#### 4.3 bot_queries

```sql
CREATE TABLE bot_queries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  bot_config_id UUID NOT NULL REFERENCES bot_configs(id) ON DELETE CASCADE,
  
  -- Query
  query_type VARCHAR(50),  -- 'market_analysis', 'entry_suggestion', 'exit_analysis'
  query_text TEXT,
  
  -- LLM Analysis
  llm_model VARCHAR(100),
  llm_response JSONB,  -- {analysis, recommendation, confidence, entry_zones}
  tokens_used INT,
  api_cost DECIMAL(10,6),
  
  -- Confidence & Execution
  confidence_score INT,  -- 0-100
  was_executed BOOLEAN DEFAULT false,
  execution_date TIMESTAMP,
  
  -- Result Feedback
  predicted_pnl DECIMAL(15,2),
  actual_pnl DECIMAL(15,2),
  accuracy_percent INT,  -- % match between prediction and actual
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_user_id (user_id),
  INDEX idx_bot_config_id (bot_config_id),
  INDEX idx_was_executed (was_executed),
  INDEX idx_created_at (created_at)
);
```

#### 4.4 bot_executions

```sql
CREATE TABLE bot_executions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  bot_config_id UUID NOT NULL REFERENCES bot_configs(id) ON DELETE CASCADE,
  
  -- Execution
  execution_type VARCHAR(50),  -- 'simulation', 'paper_trade', 'live_trade'
  
  -- Order Details
  symbol VARCHAR(50),
  entry_price DECIMAL(10,5),
  exit_price DECIMAL(10,5),
  qty INT,
  
  -- Trigger
  trigger_source VARCHAR(50),  -- 'manual', 'price_hit', 'pattern_detected'
  trigger_time TIMESTAMP,
  
  -- Execution Result
  order_id VARCHAR(255),
  execution_status VARCHAR(50),  -- 'pending', 'executed', 'partial', 'error'
  
  -- P&L
  pnl DECIMAL(15,2),
  pnl_percent DECIMAL(5,2),
  
  -- Duration
  entry_time TIMESTAMP,
  exit_time TIMESTAMP,
  duration_minutes INT,
  
  -- Reason Closed
  close_reason VARCHAR(50),  -- 'tp_hit', 'sl_hit', 'manual', 'timeout'
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_bot_config_id (bot_config_id),
  INDEX idx_execution_status (execution_status),
  INDEX idx_symbol (symbol),
  INDEX idx_created_at (created_at)
);

-- View: Bot Performance Summary
CREATE VIEW bot_performance AS
SELECT
  bc.id as bot_id,
  bc.bot_name,
  bc.symbol,
  COUNT(*) as total_executions,
  ROUND(100.0 * SUM(CASE WHEN be.pnl > 0 THEN 1 ELSE 0 END) / COUNT(*), 2) as win_rate,
  SUM(be.pnl) as total_pnl,
  AVG(be.pnl) as avg_pnl,
  MAX(be.pnl) as best_trade,
  MIN(be.pnl) as worst_trade,
  AVG(be.duration_minutes) as avg_duration_minutes
FROM bot_configs bc
LEFT JOIN bot_executions be ON bc.id = be.bot_config_id
GROUP BY bc.id, bc.bot_name, bc.symbol
ORDER BY total_pnl DESC;
```

---

### TIER 5: ANALYTICS & FEEDBACK

#### 5.1 action_log

```sql
CREATE TABLE action_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  -- Action Type
  action_type VARCHAR(100) NOT NULL,  -- 'csv_upload', 'csv_swipe', 'bot_create', 'query_made', 'result_viewed'
  
  -- Resource
  resource_type VARCHAR(50),  -- 'csv', 'bot', 'chat', 'query'
  resource_id UUID,  -- csv_import_id, bot_id, etc
  
  -- Metadata
  action_metadata JSONB,  -- {file_size, row_count, query_type, result_status}
  
  -- Timing
  duration_ms INT,  -- Time spent on action
  
  -- Session
  session_id VARCHAR(255),  -- Browser session ID
  ip_address VARCHAR(50),
  user_agent VARCHAR(510),
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_user_id (user_id),
  INDEX idx_action_type (action_type),
  INDEX idx_resource_id (resource_id),
  INDEX idx_created_at (created_at)
);

-- View: Daily Active Users
CREATE VIEW dau_stats AS
SELECT
  DATE(created_at) as day,
  COUNT(DISTINCT user_id) as active_users,
  COUNT(DISTINCT action_type) as unique_actions,
  COUNT(*) as total_actions
FROM action_log
GROUP BY DATE(created_at)
ORDER BY day DESC;
```

#### 5.2 mlm_feedback

```sql
CREATE TABLE mlm_feedback (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  -- Query Reference
  query_id UUID REFERENCES queries_log(id) ON DELETE SET NULL,
  bot_query_id UUID REFERENCES bot_queries(id) ON DELETE SET NULL,
  
  -- Feedback
  feedback_type VARCHAR(50),  -- 'helpful', 'not_helpful', 'incorrect', 'needs_improvement'
  feedback_text TEXT,
  
  -- Rating
  rating INT,  -- 1-5
  
  -- Metadata (for future ML training)
  model_version VARCHAR(50),
  predicted_output JSONB,
  actual_outcome JSONB,
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_user_id (user_id),
  INDEX idx_query_id (query_id),
  INDEX idx_feedback_type (feedback_type)
);

-- View: Feedback Summary
CREATE VIEW feedback_summary AS
SELECT
  feedback_type,
  COUNT(*) as count,
  ROUND(AVG(rating), 2) as avg_rating,
  DATE_TRUNC('month', created_at) as month
FROM mlm_feedback
WHERE rating IS NOT NULL
GROUP BY feedback_type, DATE_TRUNC('month', created_at)
ORDER BY month DESC, count DESC;
```

#### 5.3 audit_logs

```sql
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  
  -- Event
  event_type VARCHAR(100) NOT NULL,  -- 'login', 'api_key_added', 'bot_activated', 'data_exported'
  event_severity VARCHAR(50),  -- 'info', 'warning', 'critical'
  
  -- Details
  event_description TEXT,
  event_data JSONB,
  
  -- Context
  ip_address VARCHAR(50),
  user_agent VARCHAR(510),
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_user_id (user_id),
  INDEX idx_event_type (event_type),
  INDEX idx_created_at (created_at)
);
```

---

## EXAMPLE QUERIES (FOR DEVELOPMENT)

### 1. Upload CSV & Get Stats

```sql
-- Step 1: Insert import
INSERT INTO csv_imports (user_id, filename, file_type, row_count, columns_detected)
VALUES ('user_123', 'prospects.csv', 'csv', 342, ARRAY['name', 'email', 'company']);

-- Step 2: Get import with row preview
SELECT 
  id, filename, row_count, columns_detected,
  (SELECT json_agg(row_data) FROM csv_rows WHERE csv_import_id = csv_imports.id LIMIT 5) as preview
FROM csv_imports
WHERE user_id = 'user_123'
ORDER BY created_at DESC;
```

### 2. Analyze Swipe Pattern

```sql
-- Get swipe stats for specific import
SELECT 
  ci.filename,
  COUNT(*) as total_rows,
  SUM(CASE WHEN cr.swipe_action = 'like' THEN 1 ELSE 0 END) as liked,
  SUM(CASE WHEN cr.swipe_action = 'dislike' THEN 1 ELSE 0 END) as disliked,
  COUNT(*) - SUM(CASE WHEN cr.swipe_action IS NOT NULL THEN 1 ELSE 0 END) as pending,
  ROUND(100.0 * SUM(CASE WHEN cr.swipe_action = 'like' THEN 1 ELSE 0 END) / COUNT(*), 2) as like_rate
FROM csv_imports ci
LEFT JOIN csv_rows cr ON ci.id = cr.csv_import_id
WHERE ci.user_id = 'user_123'
GROUP BY ci.id, ci.filename;
```

### 3. Get Chat History with References

```sql
-- Get conversation with all messages and referenced queries
SELECT 
  c.id, c.title, c.context_type,
  json_agg(json_build_object(
    'id', cm.id,
    'role', cm.role,
    'content', cm.content,
    'created_at', cm.created_at,
    'referenced_query', ql.query_type,
    'query_result', ql.query_output
  ) ORDER BY cm.created_at) as messages
FROM conversations c
LEFT JOIN chat_messages cm ON c.id = cm.conversation_id
LEFT JOIN queries_log ql ON cm.referenced_query_id = ql.id
WHERE c.user_id = 'user_123' AND c.is_archived = false
GROUP BY c.id
ORDER BY c.last_message_at DESC;
```

### 4. Bot Performance Metrics

```sql
-- Get bot stats for user
SELECT 
  bc.bot_name,
  bc.symbol,
  COUNT(be.id) as total_executions,
  ROUND(100.0 * SUM(CASE WHEN be.pnl > 0 THEN 1 ELSE 0 END) / COUNT(be.id), 2) as win_rate,
  SUM(be.pnl) as total_pnl,
  AVG(be.pnl) as avg_pnl,
  MAX(be.duration_minutes) as longest_trade_minutes,
  bb.total_trades as backtest_trades,
  bb.win_rate as backtest_win_rate
FROM bot_configs bc
LEFT JOIN bot_executions be ON bc.id = be.bot_config_id
LEFT JOIN bot_backtests bb ON bc.backtest_id = bb.id
WHERE bc.user_id = 'user_123' AND bc.is_active = true
GROUP BY bc.id, bc.bot_name, bc.symbol, bb.total_trades, bb.win_rate
ORDER BY total_pnl DESC;
```

### 5. Query Cost Analysis

```sql
-- Cost breakdown by query type and date
SELECT 
  DATE(created_at) as day,
  query_type,
  COUNT(*) as query_count,
  SUM(api_cost) as day_cost,
  AVG(api_cost) as avg_cost,
  AVG(total_tokens) as avg_tokens
FROM queries_log
WHERE user_id = 'user_123'
GROUP BY DATE(created_at), query_type
ORDER BY day DESC, day_cost DESC;
```

### 6. Liked Rows Export

```sql
-- Export all liked rows from specific import as JSON
SELECT json_agg(cr.row_data)
FROM csv_rows cr
JOIN swipe_actions sa ON cr.id = sa.csv_row_id
WHERE cr.csv_import_id = 'csv_123' AND sa.action = 'like'
ORDER BY cr.row_number;
```

---

## REAL-TIME SUBSCRIPTIONS (Supabase)

```typescript
// Subscribe to new chat messages
supabase
  .channel('chat:' + conversationId)
  .on('postgres_changes', 
    { event: 'INSERT', schema: 'public', table: 'chat_messages' },
    (payload) => {
      console.log('New message:', payload.new);
    }
  )
  .subscribe();

// Subscribe to bot execution updates
supabase
  .channel('bot:' + botId)
  .on('postgres_changes',
    { event: '*', schema: 'public', table: 'bot_executions' },
    (payload) => {
      console.log('Bot execution update:', payload);
    }
  )
  .subscribe();

// Subscribe to query results
supabase
  .channel('queries')
  .on('postgres_changes',
    { event: 'UPDATE', schema: 'public', table: 'queries_log', filter: `user_id=eq.${userId}` },
    (payload) => {
      console.log('Query completed:', payload.new);
    }
  )
  .subscribe();
```

---

## SECURITY & PRIVACY

```sql
-- Row Level Security (RLS) - Enable on all tables

-- users table: users can only see their own data
CREATE POLICY users_isolation ON users
  FOR SELECT
  USING (auth.uid() = id);

-- csv_imports: users can only see their own imports
ALTER TABLE csv_imports ENABLE ROW LEVEL SECURITY;
CREATE POLICY csv_own_data ON csv_imports
  FOR ALL
  USING (auth.uid() = user_id);

-- api_credentials: encrypted & user-specific
ALTER TABLE api_credentials ENABLE ROW LEVEL SECURITY;
CREATE POLICY api_credentials_own ON api_credentials
  FOR ALL
  USING (auth.uid() = user_id);

-- All other tables: apply same pattern (user_id-based isolation)
```

---

## DEPLOYMENT CHECKLIST

- [ ] Enable Row Level Security (RLS) on all tables
- [ ] Set up pgcrypto extension for encryption
- [ ] Create indexes for performance
- [ ] Set up real-time subscriptions
- [ ] Enable point-in-time recovery (PITR)
- [ ] Configure backups
- [ ] Set up monitoring & alerts
- [ ] Create roles for API calls
- [ ] Test all queries
- [ ] Performance test with 10K+ rows

---

## COST ESTIMATION (Supabase Free → Pro)

| Item | Free | Pro |
|------|------|-----|
| Database size | 500MB | Unlimited |
| Auth users | 50K | Unlimited |
| Real-time connections | 200 | 1K+ |
| API requests/month | Unlimited | Unlimited |
| Monthly cost | $0 | $25/mo |

**Start with Free, upgrade to Pro when users > 100 or storage > 500MB**
