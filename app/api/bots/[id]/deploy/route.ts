/**
 * POST /api/bots/[id]/deploy - Deploy bot to Alpaca
 */

import { getCurrentUser, updateBot, getBotTrades, saveBotStats } from '@/lib/supabase'
import { NextRequest, NextResponse } from 'next/server'
import axios from 'axios'

const ALPACA_API = process.env.ALPACA_API || 'https://paper-api.alpaca.markets/v2'
const ALPACA_KEY = process.env.ALPACA_KEY
const ALPACA_SECRET = process.env.ALPACA_SECRET

interface RouteParams {
  params: { id: string }
}

export async function POST(req: NextRequest, { params }: RouteParams) {
  try {
    const user = await getCurrentUser()
    if (!user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const botId = params.id
    const body = await req.json()

    // Update bot status to deploying
    await updateBot(botId, { status: 'deploying' })

    // Deploy orders to Alpaca (wave system)
    const orders = await deployWavesToAlpaca(body, botId, user.id)

    // Calculate stats
    const stats = {
      bot_id: botId,
      user_id: user.id,
      orders_deployed: orders.length,
      orders_filled: orders.filter((o: any) => o.filled_qty > 0).length,
      fill_rate: (orders.filter((o: any) => o.filled_qty > 0).length / orders.length) * 100,
      pnl: 0, // Will be calculated from trades
    }

    // Save stats
    await saveBotStats(stats as any)

    // Update bot status to monitoring
    await updateBot(botId, { status: 'monitoring', is_active: true })

    return NextResponse.json({
      success: true,
      botId,
      orders,
      stats,
    })
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }
}

async function deployWavesToAlpaca(
  config: any,
  botId: string,
  userId: string
): Promise<any[]> {
  const orders: any[] = []
  const { symbols, allocation, config: botConfig } = config

  const headers = {
    'APCA-API-KEY-ID': ALPACA_KEY,
    'APCA-API-SECRET-KEY': ALPACA_SECRET,
  }

  try {
    // Get account data
    const accountRes = await axios.get(`${ALPACA_API}/account`, { headers })
    const buying_power = accountRes.data.buying_power

    // Deploy orders for each symbol
    for (const symbol of symbols) {
      const alloc = allocation[symbol] || 0.1
      const order_qty = Math.floor((parseFloat(buying_power) * alloc) / 100)

      if (order_qty === 0) continue

      // Place order
      const orderRes = await axios.post(
        `${ALPACA_API}/orders`,
        {
          symbol,
          qty: order_qty,
          side: 'buy',
          type: 'market',
          time_in_force: 'day',
        },
        { headers }
      )

      orders.push(orderRes.data)

      // Wave interval (90 seconds default)
      await new Promise(resolve => setTimeout(resolve, botConfig.waveInterval * 1000))
    }

    return orders
  } catch (error: any) {
    console.error('Alpaca deployment error:', error.response?.data || error.message)
    throw error
  }
}
