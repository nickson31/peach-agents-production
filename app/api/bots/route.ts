/**
 * GET /api/bots - List all bots for current user
 * POST /api/bots - Create new bot
 */

import { getCurrentUser, getUserBots, createBot } from '@/lib/supabase'
import { NextRequest, NextResponse } from 'next/server'

export async function GET(req: NextRequest) {
  try {
    const user = await getCurrentUser()
    if (!user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const bots = await getUserBots(user.id)
    return NextResponse.json(bots)
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }
}

export async function POST(req: NextRequest) {
  try {
    const user = await getCurrentUser()
    if (!user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const body = await req.json()
    const bot = await createBot({
      ...body,
      user_id: user.id,
      status: 'idle',
    })

    return NextResponse.json(bot, { status: 201 })
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }
}
