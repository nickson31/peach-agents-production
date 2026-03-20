/**
 * HOME PAGE
 * Redirects to login or dashboard based on auth state
 */

'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { getCurrentSession } from '@/lib/auth'

export default function Home() {
  const router = useRouter()
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function checkAuth() {
      const session = await getCurrentSession()
      if (session) {
        router.push('/dashboard')
      } else {
        router.push('/auth/login')
      }
      setLoading(false)
    }
    checkAuth()
  }, [router])

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center bg-slate-950">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-white mb-4">PEACH&AGENTS</h1>
          <p className="text-slate-400">Loading...</p>
        </div>
      </div>
    )
  }

  return null
}
