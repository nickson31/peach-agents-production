/**
 * DASHBOARD PAGE - Main app hub
 */

'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { getCurrentSession, getCurrentUser, signOut } from '@/lib/auth'
import { getUserBots } from '@/lib/supabase'
import Link from 'next/link'

interface Bot {
  id: string
  name: string
  strategy: string
  status: string
  symbols: string[]
}

export default function DashboardPage() {
  const router = useRouter()
  const [user, setUser] = useState<any>(null)
  const [bots, setBots] = useState<Bot[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadData() {
      try {
        const session = await getCurrentSession()
        if (!session) {
          router.push('/auth/login')
          return
        }

        const currentUser = await getCurrentUser()
        setUser(currentUser)

        if (currentUser) {
          const userBots = await getUserBots(currentUser.id)
          setBots(userBots || [])
        }
      } catch (error) {
        console.error('Failed to load data:', error)
      } finally {
        setLoading(false)
      }
    }

    loadData()
  }, [router])

  const handleLogout = async () => {
    try {
      await signOut()
      router.push('/auth/login')
    } catch (error) {
      console.error('Logout failed:', error)
    }
  }

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center bg-slate-950">
        <p className="text-slate-400">Loading...</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold">PEACH&AGENTS Dashboard</h1>
          <div className="flex items-center gap-4">
            <span className="text-slate-400">{user?.email}</span>
            <button
              onClick={handleLogout}
              className="px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded font-semibold"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Navigation */}
        <div className="mb-8 flex gap-4">
          <Link
            href="/dashboard/bots"
            className="px-4 py-2 bg-pink-600 hover:bg-pink-700 rounded font-semibold"
          >
            Manage Bots
          </Link>
          <Link
            href="/dashboard/research"
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded font-semibold"
          >
            Research
          </Link>
          <Link
            href="/dashboard/analytics"
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded font-semibold"
          >
            Analytics
          </Link>
        </div>

        {/* Bots Summary */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="p-6 bg-slate-900 border border-slate-800 rounded-lg">
            <h3 className="text-slate-400 text-sm font-medium mb-2">Total Bots</h3>
            <p className="text-4xl font-bold">{bots.length}</p>
          </div>
          <div className="p-6 bg-slate-900 border border-slate-800 rounded-lg">
            <h3 className="text-slate-400 text-sm font-medium mb-2">Active Bots</h3>
            <p className="text-4xl font-bold">{bots.filter(b => b.status === 'monitoring').length}</p>
          </div>
          <div className="p-6 bg-slate-900 border border-slate-800 rounded-lg">
            <h3 className="text-slate-400 text-sm font-medium mb-2">Total P&L</h3>
            <p className="text-4xl font-bold text-green-400">$0.00</p>
          </div>
        </div>

        {/* Bots List */}
        <div className="bg-slate-900 border border-slate-800 rounded-lg">
          <div className="p-6 border-b border-slate-800">
            <h2 className="text-xl font-bold">Your Bots</h2>
          </div>
          <div className="divide-y divide-slate-800">
            {bots.length === 0 ? (
              <div className="p-6 text-center text-slate-400">
                <p>No bots yet.</p>
                <Link
                  href="/dashboard/bots"
                  className="text-pink-600 hover:text-pink-500 font-semibold"
                >
                  Create your first bot
                </Link>
              </div>
            ) : (
              bots.map(bot => (
                <div key={bot.id} className="p-6 hover:bg-slate-800 transition">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-semibold text-lg">{bot.name}</h3>
                      <p className="text-slate-400 text-sm">Strategy: {bot.strategy}</p>
                      <p className="text-slate-400 text-sm">Symbols: {bot.symbols.join(', ')}</p>
                    </div>
                    <div className="text-right">
                      <span
                        className={`px-3 py-1 rounded text-sm font-semibold ${
                          bot.status === 'monitoring'
                            ? 'bg-green-950 text-green-200'
                            : 'bg-slate-800 text-slate-200'
                        }`}
                      >
                        {bot.status}
                      </span>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </main>
    </div>
  )
}
