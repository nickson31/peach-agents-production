/**
 * Supabase Client Setup
 * Handles all database operations and authentication
 */

import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || ''
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || ''

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Missing Supabase environment variables')
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// ============================================================================
// TYPES
// ============================================================================

export interface Database {
  public: {
    Tables: {
      bots: {
        Row: {
          id: string
          user_id: string
          name: string
          strategy: string
          symbols: string[]
          allocation: Record<string, number>
          config: {
            takeProfit: number
            stopLoss: number
            batchSize: number
            waveInterval: number
          }
          status: 'idle' | 'deploying' | 'monitoring' | 'completed'
          is_active: boolean
          created_at: string
          updated_at: string
        }
        Insert: Omit<Database['public']['Tables']['bots']['Row'], 'id' | 'created_at' | 'updated_at'>
      }
      bot_stats: {
        Row: {
          id: string
          bot_id: string
          user_id: string
          orders_deployed: number
          orders_filled: number
          fill_rate: number
          pnl: number
          equity: number | null
          cash: number | null
          buying_power: number | null
          timestamp: string
        }
      }
      trades: {
        Row: {
          id: string
          bot_id: string
          user_id: string
          alpaca_order_id: string | null
          symbol: string
          side: 'buy' | 'sell'
          qty: number
          entry_price: number | null
          exit_price: number | null
          entry_time: string | null
          exit_time: string | null
          pnl: number | null
          status: string
          created_at: string
        }
      }
      leads: {
        Row: {
          id: string
          user_id: string
          source: string
          title: string | null
          description: string | null
          data: Record<string, any>
          status: string
          created_at: string
          updated_at: string
        }
      }
      strategies: {
        Row: {
          id: string
          user_id: string | null
          name: string
          description: string | null
          config: Record<string, any>
          is_public: boolean
          is_template: boolean
          created_at: string
        }
      }
    }
  }
}

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

export async function getCurrentUser() {
  const {
    data: { user },
  } = await supabase.auth.getUser()
  return user
}

export async function getUserBots(userId: string) {
  const { data, error } = await supabase
    .from('bots')
    .select('*')
    .eq('user_id', userId)
    .order('created_at', { ascending: false })

  if (error) throw error
  return data
}

export async function createBot(bot: Database['public']['Tables']['bots']['Insert']) {
  const { data, error } = await supabase
    .from('bots')
    .insert([bot])
    .select()
    .single()

  if (error) throw error
  return data
}

export async function updateBot(
  botId: string,
  updates: Partial<Database['public']['Tables']['bots']['Row']>
) {
  const { data, error } = await supabase
    .from('bots')
    .update(updates)
    .eq('id', botId)
    .select()
    .single()

  if (error) throw error
  return data
}

export async function deleteBot(botId: string) {
  const { error } = await supabase
    .from('bots')
    .delete()
    .eq('id', botId)

  if (error) throw error
}

export async function getBotStats(botId: string, days: number = 7) {
  const { data, error } = await supabase
    .from('bot_stats')
    .select('*')
    .eq('bot_id', botId)
    .gte('timestamp', new Date(Date.now() - days * 24 * 60 * 60 * 1000).toISOString())
    .order('timestamp', { ascending: true })

  if (error) throw error
  return data
}

export async function saveBotStats(stats: Database['public']['Tables']['bot_stats']['Row']) {
  const { data, error } = await supabase
    .from('bot_stats')
    .insert([stats])
    .select()
    .single()

  if (error) throw error
  return data
}

export async function getBotTrades(botId: string) {
  const { data, error } = await supabase
    .from('trades')
    .select('*')
    .eq('bot_id', botId)
    .order('created_at', { ascending: false })

  if (error) throw error
  return data
}

export async function createTrade(trade: Database['public']['Tables']['trades']['Row']) {
  const { data, error } = await supabase
    .from('trades')
    .insert([trade])
    .select()
    .single()

  if (error) throw error
  return data
}

export async function getUserLeads(userId: string) {
  const { data, error } = await supabase
    .from('leads')
    .select('*')
    .eq('user_id', userId)
    .order('created_at', { ascending: false })

  if (error) throw error
  return data
}

export async function saveLeads(leads: Database['public']['Tables']['leads']['Row'][]) {
  const { data, error } = await supabase
    .from('leads')
    .insert(leads)
    .select()

  if (error) throw error
  return data
}

export async function getStrategies(userId?: string) {
  let query = supabase
    .from('strategies')
    .select('*')
    .or(`is_public.eq.true${userId ? `,user_id.eq.${userId}` : ''}`)

  const { data, error } = await query

  if (error) throw error
  return data
}
