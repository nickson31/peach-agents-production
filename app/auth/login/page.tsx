/**
 * LOGIN PAGE
 */

'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { signInWithEmail, signInWithGoogle, signInWithGitHub } from '@/lib/auth'
import Link from 'next/link'

export default function LoginPage() {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleEmailLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await signInWithEmail(email, password)
      router.push('/dashboard')
    } catch (err: any) {
      setError(err.message || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  const handleGoogleLogin = async () => {
    setError('')
    setLoading(true)
    try {
      const { data } = await signInWithGoogle()
      if (data?.url) {
        window.location.href = data.url
      }
    } catch (err: any) {
      setError(err.message || 'Google login failed')
      setLoading(false)
    }
  }

  const handleGitHubLogin = async () => {
    setError('')
    setLoading(true)
    try {
      const { data } = await signInWithGitHub()
      if (data?.url) {
        window.location.href = data.url
      }
    } catch (err: any) {
      setError(err.message || 'GitHub login failed')
      setLoading(false)
    }
  }

  return (
    <div className="flex h-screen items-center justify-center bg-slate-950">
      <div className="w-full max-w-md space-y-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-white mb-2">PEACH&AGENTS</h1>
          <p className="text-slate-400">Trading Bot Management Platform</p>
        </div>

        <form onSubmit={handleEmailLogin} className="space-y-4">
          {error && <div className="p-3 bg-red-950 text-red-200 rounded">{error}</div>}

          <div>
            <label className="block text-sm font-medium text-white mb-1">Email</label>
            <input
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              required
              className="w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded text-white"
              placeholder="you@example.com"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-white mb-1">Password</label>
            <input
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
              className="w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded text-white"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2 bg-pink-600 hover:bg-pink-700 text-white font-semibold rounded disabled:opacity-50"
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-slate-700"></div>
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-2 bg-slate-950 text-slate-400">Or continue with</span>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <button
            onClick={handleGoogleLogin}
            disabled={loading}
            className="py-2 bg-slate-900 hover:bg-slate-800 text-white rounded font-semibold disabled:opacity-50"
          >
            Google
          </button>
          <button
            onClick={handleGitHubLogin}
            disabled={loading}
            className="py-2 bg-slate-900 hover:bg-slate-800 text-white rounded font-semibold disabled:opacity-50"
          >
            GitHub
          </button>
        </div>

        <p className="text-center text-slate-400">
          Don't have an account?{' '}
          <Link href="/auth/signup" className="text-pink-600 hover:text-pink-500">
            Sign up
          </Link>
        </p>
      </div>
    </div>
  )
}
