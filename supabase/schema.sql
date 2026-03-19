-- PEACH&AGENTS - SUPABASE SCHEMA
-- Run this in Supabase SQL Editor

-- ============================================================================
-- USERS TABLE (for authentication)
-- ============================================================================
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT UNIQUE NOT NULL,
  full_name TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================================
-- BOTS TABLE (Trading bot configurations)
-- ============================================================================
CREATE TABLE IF NOT EXISTS bots (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  strategy TEXT NOT NULL,
  symbols TEXT[] NOT NULL,
  allocation JSONB NOT NULL,
  config JSONB NOT NULL DEFAULT '{
    "takeProfit": 0.03,
    "stopLoss": -0.01,
    "batchSize": 100,
    "waveInterval": 90
  }'::jsonb,
  status TEXT NOT NULL DEFAULT 'idle',
  is_active BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  created_by TEXT,
  updated_by TEXT
);

-- ============================================================================
-- BOT STATISTICS (Performance tracking)
-- ============================================================================
CREATE TABLE IF NOT EXISTS bot_stats (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  bot_id UUID NOT NULL REFERENCES bots(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  orders_deployed INT DEFAULT 0,
  orders_filled INT DEFAULT 0,
  fill_rate FLOAT DEFAULT 0.0,
  pnl FLOAT DEFAULT 0.0,
  equity FLOAT,
  cash FLOAT,
  buying_power FLOAT,
  timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================================
-- TRADES TABLE (Individual trade records)
-- ============================================================================
CREATE TABLE IF NOT EXISTS trades (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  bot_id UUID NOT NULL REFERENCES bots(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  alpaca_order_id TEXT UNIQUE,
  symbol TEXT NOT NULL,
  side TEXT NOT NULL,
  qty INT NOT NULL,
  entry_price FLOAT,
  exit_price FLOAT,
  entry_time TIMESTAMP WITH TIME ZONE,
  exit_time TIMESTAMP WITH TIME ZONE,
  pnl FLOAT,
  status TEXT NOT NULL DEFAULT 'pending',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================================
-- BOT FOLDERS (Organization)
-- ============================================================================
CREATE TABLE IF NOT EXISTS bot_folders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, name)
);

-- ============================================================================
-- BOT FOLDER MAPPING (Many-to-many)
-- ============================================================================
CREATE TABLE IF NOT EXISTS bot_folder_mapping (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  bot_id UUID NOT NULL REFERENCES bots(id) ON DELETE CASCADE,
  folder_id UUID NOT NULL REFERENCES bot_folders(id) ON DELETE CASCADE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(bot_id, folder_id)
);

-- ============================================================================
-- LEADS TABLE (Trading leads/signals)
-- ============================================================================
CREATE TABLE IF NOT EXISTS leads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  source TEXT NOT NULL,
  title TEXT,
  description TEXT,
  data JSONB NOT NULL,
  status TEXT NOT NULL DEFAULT 'new',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================================
-- STRATEGIES TABLE (Pre-built or custom)
-- ============================================================================
CREATE TABLE IF NOT EXISTS strategies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  config JSONB NOT NULL,
  is_public BOOLEAN DEFAULT FALSE,
  is_template BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, name)
);

-- ============================================================================
-- EXECUTION LOG (Audit trail)
-- ============================================================================
CREATE TABLE IF NOT EXISTS execution_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  bot_id UUID REFERENCES bots(id) ON DELETE SET NULL,
  action TEXT NOT NULL,
  details JSONB,
  status TEXT NOT NULL DEFAULT 'success',
  error_message TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================================
-- PORTFOLIO VIEW (Aggregated)
-- ============================================================================
CREATE TABLE IF NOT EXISTS portfolio_summary (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
  total_bots INT DEFAULT 0,
  active_bots INT DEFAULT 0,
  total_equity FLOAT DEFAULT 0.0,
  total_cash FLOAT DEFAULT 0.0,
  total_pnl FLOAT DEFAULT 0.0,
  average_fill_rate FLOAT DEFAULT 0.0,
  last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================================
-- INDEXES (Performance optimization)
-- ============================================================================
CREATE INDEX idx_bots_user_id ON bots(user_id);
CREATE INDEX idx_bots_status ON bots(status);
CREATE INDEX idx_bots_created_at ON bots(created_at);
CREATE INDEX idx_bot_stats_bot_id ON bot_stats(bot_id);
CREATE INDEX idx_bot_stats_user_id ON bot_stats(user_id);
CREATE INDEX idx_bot_stats_timestamp ON bot_stats(timestamp);
CREATE INDEX idx_trades_bot_id ON trades(bot_id);
CREATE INDEX idx_trades_user_id ON trades(user_id);
CREATE INDEX idx_trades_symbol ON trades(symbol);
CREATE INDEX idx_leads_user_id ON leads(user_id);
CREATE INDEX idx_leads_status ON leads(status);
CREATE INDEX idx_execution_logs_user_id ON execution_logs(user_id);
CREATE INDEX idx_execution_logs_bot_id ON execution_logs(bot_id);

-- ============================================================================
-- ROW LEVEL SECURITY (RLS)
-- ============================================================================

-- Users can only see their own data
ALTER TABLE bots ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can only see their own bots"
  ON bots FOR SELECT
  USING (auth.uid() = user_id);
CREATE POLICY "Users can only modify their own bots"
  ON bots FOR UPDATE
  USING (auth.uid() = user_id);
CREATE POLICY "Users can only delete their own bots"
  ON bots FOR DELETE
  USING (auth.uid() = user_id);
CREATE POLICY "Users can insert their own bots"
  ON bots FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Bot stats security
ALTER TABLE bot_stats ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can only see their own bot stats"
  ON bot_stats FOR SELECT
  USING (auth.uid() = user_id);
CREATE POLICY "Users can insert their own bot stats"
  ON bot_stats FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Trades security
ALTER TABLE trades ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can only see their own trades"
  ON trades FOR SELECT
  USING (auth.uid() = user_id);
CREATE POLICY "Users can insert their own trades"
  ON trades FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Leads security
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can only see their own leads"
  ON leads FOR SELECT
  USING (auth.uid() = user_id);
CREATE POLICY "Users can modify their own leads"
  ON leads FOR UPDATE
  USING (auth.uid() = user_id);
CREATE POLICY "Users can delete their own leads"
  ON leads FOR DELETE
  USING (auth.uid() = user_id);
CREATE POLICY "Users can insert their own leads"
  ON leads FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- ============================================================================
-- FUNCTIONS
-- ============================================================================

-- Function to update portfolio summary
CREATE OR REPLACE FUNCTION update_portfolio_summary(p_user_id UUID)
RETURNS void AS $$
BEGIN
  INSERT INTO portfolio_summary (user_id, total_bots, active_bots, last_updated)
  SELECT
    p_user_id,
    COUNT(*)::INT as total_bots,
    COUNT(CASE WHEN is_active = TRUE THEN 1 END)::INT as active_bots,
    NOW()
  FROM bots
  WHERE user_id = p_user_id
  ON CONFLICT (user_id) DO UPDATE SET
    total_bots = EXCLUDED.total_bots,
    active_bots = EXCLUDED.active_bots,
    last_updated = NOW();
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- TRIGGERS
-- ============================================================================

-- Trigger to log bot creation
CREATE OR REPLACE FUNCTION log_bot_creation()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO execution_logs (user_id, bot_id, action, details, status)
  VALUES (NEW.user_id, NEW.id, 'BOT_CREATED', row_to_json(NEW), 'success');
  PERFORM update_portfolio_summary(NEW.user_id);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER bot_creation_trigger
AFTER INSERT ON bots
FOR EACH ROW
EXECUTE FUNCTION log_bot_creation();

-- Trigger to update portfolio on bot status change
CREATE OR REPLACE FUNCTION log_bot_update()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO execution_logs (user_id, bot_id, action, details, status)
  VALUES (
    NEW.user_id,
    NEW.id,
    'BOT_UPDATED',
    jsonb_build_object('old', row_to_json(OLD), 'new', row_to_json(NEW)),
    'success'
  );
  PERFORM update_portfolio_summary(NEW.user_id);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER bot_update_trigger
AFTER UPDATE ON bots
FOR EACH ROW
EXECUTE FUNCTION log_bot_update();

-- Handle new user creation
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.users (id, email, full_name)
  VALUES (new.id, new.email, new.user_metadata->>'full_name');
  PERFORM update_portfolio_summary(new.id);
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
