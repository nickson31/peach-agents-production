/**
 * SIGNUP PAGE
 */

'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { signUpWithEmail } from '@/lib/auth'
import Link from 'next/link'

export default function SignupPage() {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [fullName, setFullName] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await signUpWithEmail(email, password, fullName)
      setSuccess(true)
      setTimeout(() => {
        router.push('/auth/login')
      }, 2000)
    } catch (err: any) {
      setError(err.message || 'Signup failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex h-screen items-center justify-center bg-slate-950">
      <div className="w-full max-w-md space-y-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-white mb-2">PEACH&AGENTS</h1>
          <p className="text-slate-400">Create your account</p>
        </div>

        {success ? (
          <div className="text-center p-4 bg-green-950 text-green-200 rounded">
            <p className="font-semibold">Account created successfully!</p>
            <p className="text-sm">Redirecting to login...</p>
          </div>
        ) : (
          <form onSubmit={handleSignup} className="space-y-4">
            {error && <div className="p-3 bg-red-950 text-red-200 rounded">{error}</div>}

            <div>
              <label className="block text-sm font-medium text-white mb-1">Full Name</label>
              <input
                type="text"
                value={fullName}
                onChange={e => setFullName(e.target.value)}
                className="w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded text-white"
                placeholder="Your name"
              />
            </div>

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
              <p className="text-xs text-slate-400 mt-1">At least 8 characters recommended</p>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2 bg-pink-600 hover:bg-pink-700 text-white font-semibold rounded disabled:opacity-50"
            >
              {loading ? 'Creating account...' : 'Sign Up'}
            </button>
          </form>
        )}

        <p className="text-center text-slate-400">
          Already have an account?{' '}
          <Link href="/auth/login" className="text-pink-600 hover:text-pink-500">
            Login
          </Link>
        </p>
      </div>
    </div>
  )
}
