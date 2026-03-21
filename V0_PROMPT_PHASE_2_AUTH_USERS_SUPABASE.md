# V0 PHASE 2 PROMPT - AUTHENTICATION + USERS + SUPABASE
**Context**: You already generated Phase 1 app (Leads, Trading, Settings). Now add auth layer + user management + database.
**Date**: 2026-03-20 14:01 UTC
**Target**: Production-ready Next.js + Supabase + NextAuth.js

---

## 🎯 PHASE 2 OBJECTIVES

Add these 3 critical pieces:
1. **Authentication** - Login/Signup with Supabase Auth
2. **User Management** - User profiles, roles, sessions
3. **Database Integration** - Persist all data to Supabase

---

## 📊 SUPABASE SCHEMA (REQUIRED)

Create these tables in Supabase:

```sql
-- 1. USERS (Supabase Auth creates this, but extend it)
CREATE TABLE IF NOT EXISTS users_extended (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  avatar_url TEXT,
  role TEXT DEFAULT 'user', -- 'admin' | 'user' | 'trader'
  status TEXT DEFAULT 'active', -- 'active' | 'suspended' | 'deleted'
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- 2. SESSIONS
CREATE TABLE IF NOT EXISTS sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users_extended(id) ON DELETE CASCADE,
  token TEXT UNIQUE,
  expires_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);

-- 3. LEADS (USER-SCOPED)
CREATE TABLE IF NOT EXISTS leads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users_extended(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  title TEXT,
  signal_type TEXT, -- 'BULLISH' | 'BEARISH' | 'NEUTRAL'
  confidence INT,
  source TEXT, -- 'YouTube' | 'RSS' | 'Direct'
  description TEXT,
  link TEXT,
  status TEXT DEFAULT 'new', -- 'new' | 'reviewed' | 'acted' | 'dismissed'
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- 4. TRADING_ACCOUNTS (USER-SCOPED)
CREATE TABLE IF NOT EXISTS trading_accounts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users_extended(id) ON DELETE CASCADE,
  account_id TEXT, -- Alpaca account ID
  account_name TEXT,
  api_key_encrypted TEXT, -- Store encrypted
  api_secret_encrypted TEXT, -- Store encrypted
  current_equity DECIMAL(15,2),
  buying_power DECIMAL(15,2),
  status TEXT DEFAULT 'connected', -- 'connected' | 'error' | 'inactive'
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- 5. BATCH_DEPLOYMENTS (USER-SCOPED)
CREATE TABLE IF NOT EXISTS batch_deployments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users_extended(id) ON DELETE CASCADE,
  batch_num INT,
  deployment_time TIMESTAMP,
  strategy TEXT,
  orders_count INT,
  fill_rate_percent DECIMAL(5,2),
  actual_gain DECIMAL(15,2),
  equity_before DECIMAL(15,2),
  equity_after DECIMAL(15,2),
  status TEXT DEFAULT 'pending', -- 'pending' | 'completed' | 'failed'
  created_at TIMESTAMP DEFAULT NOW()
);

-- 6. USER_SETTINGS
CREATE TABLE IF NOT EXISTS user_settings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users_extended(id) ON DELETE CASCADE UNIQUE,
  daily_loss_halt DECIMAL(5,2) DEFAULT -1.0,
  position_stop_loss DECIMAL(5,2) DEFAULT -0.5,
  min_buying_power DECIMAL(15,2) DEFAULT 15000,
  target_fill_rate INT DEFAULT 80,
  batch_interval_minutes INT DEFAULT 15,
  theme TEXT DEFAULT 'dark', -- 'dark' | 'light'
  notifications_enabled BOOLEAN DEFAULT TRUE,
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_leads_user ON leads(user_id);
CREATE INDEX idx_trading_accounts_user ON trading_accounts(user_id);
CREATE INDEX idx_batch_deployments_user ON batch_deployments(user_id);
CREATE INDEX idx_sessions_user ON sessions(user_id);
```

---

## 🔐 AUTHENTICATION SETUP

### Use NextAuth.js + Supabase

Install:
```bash
npm install next-auth @supabase/supabase-js
```

Create `lib/auth.ts`:

```typescript
import { NextAuthOptions } from 'next-auth'
import CredentialsProvider from 'next-auth/providers/credentials'
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
)

export const authOptions: NextAuthOptions = {
  providers: [
    CredentialsProvider({
      name: 'Email',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' }
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) return null

        try {
          // Sign in with Supabase Auth
          const { data, error } = await supabase.auth.signInWithPassword({
            email: credentials.email,
            password: credentials.password
          })

          if (error || !data.user) return null

          // Get user profile
          const { data: profile } = await supabase
            .from('users_extended')
            .select('*')
            .eq('id', data.user.id)
            .single()

          return {
            id: data.user.id,
            email: data.user.email,
            name: profile?.name,
            role: profile?.role,
            image: profile?.avatar_url
          }
        } catch (error) {
          console.error('Auth error:', error)
          return null
        }
      }
    })
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id
        token.role = user.role
      }
      return token
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string
        session.user.role = token.role as string
      }
      return session
    }
  },
  pages: {
    signIn: '/login',
    signOut: '/logout',
    error: '/auth/error'
  },
  session: {
    strategy: 'jwt',
    maxAge: 30 * 24 * 60 * 60 // 30 days
  }
}
```

---

## 👤 USER PAGES TO ADD

### 1. LOGIN PAGE (`app/login/page.tsx`)

```typescript
'use client'

import { useState } from 'react'
import { signIn } from 'next-auth/react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Alert } from '@/components/ui/alert'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const router = useRouter()

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError('')

    const result = await signIn('credentials', {
      email,
      password,
      redirect: false
    })

    if (result?.error) {
      setError(result.error)
    } else if (result?.ok) {
      router.push('/dashboard')
    }
    setLoading(false)
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="w-full max-w-md space-y-6">
        <h1 className="text-3xl font-bold text-center">🍑 Peach Agents</h1>
        <form onSubmit={handleLogin} className="space-y-4">
          {error && <Alert className="bg-red-100 text-red-700">{error}</Alert>}

          <div>
            <label className="text-sm font-medium">Email</label>
            <Input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
            />
          </div>

          <div>
            <label className="text-sm font-medium">Password</label>
            <Input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
            />
          </div>

          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? 'Signing in...' : 'Sign In'}
          </Button>
        </form>

        <p className="text-center text-sm">
          Don't have an account? <a href="/signup" className="text-primary underline">Sign up</a>
        </p>
      </div>
    </div>
  )
}
```

### 2. SIGNUP PAGE (`app/signup/page.tsx`)

Similar but with:
- Email, password, password confirm, name
- Call `supabase.auth.signUp()`
- Then redirect to verify email page

### 3. DASHBOARD PAGE (`app/dashboard/page.tsx`)

```typescript
'use client'

import { useSession } from 'next-auth/react'
import { redirect } from 'next/navigation'
import { MainApp } from '@/components/main-app'

export default function DashboardPage() {
  const { data: session, status } = useSession()

  if (status === 'loading') return <div>Loading...</div>
  if (!session) redirect('/login')

  return (
    <div>
      <nav className="flex justify-between p-4 bg-secondary">
        <h1>Welcome, {session.user?.name || session.user?.email}!</h1>
        <button onClick={() => signOut()}>Logout</button>
      </nav>
      
      <MainApp userId={session.user?.id} />
    </div>
  )
}
```

---

## 🔗 USER-SCOPED DATA FETCHING

Update your components to include `user_id`:

### Leads Component Update

```typescript
'use client'

import { useSession } from 'next-auth/react'
import { useEffect, useState } from 'react'
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)

export function LeadsScreen() {
  const { data: session } = useSession()
  const [leads, setLeads] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!session?.user?.id) return

    async function fetchLeads() {
      const { data, error } = await supabase
        .from('leads')
        .select('*')
        .eq('user_id', session.user.id)
        .order('created_at', { ascending: false })

      if (!error) setLeads(data || [])
      setLoading(false)
    }

    fetchLeads()
  }, [session?.user?.id])

  async function saveLead(lead: any) {
    if (!session?.user?.id) return

    await supabase
      .from('leads')
      .insert([
        {
          ...lead,
          user_id: session.user.id
        }
      ])
  }

  // ... rest of component
}
```

---

## 🔒 API ROUTES WITH AUTH

Create protected API routes:

### `app/api/leads/route.ts`

```typescript
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { createClient } from '@supabase/supabase-js'
import { NextRequest, NextResponse } from 'next/server'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
)

export async function GET(req: NextRequest) {
  const session = await getServerSession(authOptions)
  if (!session?.user?.id) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })

  const { data, error } = await supabase
    .from('leads')
    .select('*')
    .eq('user_id', session.user.id)

  if (error) return NextResponse.json({ error: error.message }, { status: 500 })
  return NextResponse.json(data)
}

export async function POST(req: NextRequest) {
  const session = await getServerSession(authOptions)
  if (!session?.user?.id) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })

  const body = await req.json()
  const { data, error } = await supabase
    .from('leads')
    .insert([{ ...body, user_id: session.user.id }])

  if (error) return NextResponse.json({ error: error.message }, { status: 500 })
  return NextResponse.json(data)
}
```

---

## 🔐 ENCRYPT ALPACA KEYS

For `trading_accounts`, encrypt API keys before storing:

```typescript
import crypto from 'crypto'

const ENCRYPTION_KEY = process.env.ENCRYPTION_KEY! // 32-char hex string

export function encryptKey(key: string): string {
  const iv = crypto.randomBytes(16)
  const cipher = crypto.createCipheriv('aes-256-cbc', Buffer.from(ENCRYPTION_KEY, 'hex'), iv)
  let encrypted = cipher.update(key, 'utf-8', 'hex')
  encrypted += cipher.final('hex')
  return iv.toString('hex') + ':' + encrypted
}

export function decryptKey(encrypted: string): string {
  const [ivHex, encryptedHex] = encrypted.split(':')
  const iv = Buffer.from(ivHex, 'hex')
  const decipher = crypto.createDecipheriv('aes-256-cbc', Buffer.from(ENCRYPTION_KEY, 'hex'), iv)
  let decrypted = decipher.update(encryptedHex, 'hex', 'utf-8')
  decrypted += decipher.final('utf-8')
  return decrypted
}
```

---

## 📱 LAYOUT WITH SESSION PROVIDER

Update `app/layout.tsx`:

```typescript
import { SessionProvider } from 'next-auth/react'
import { ReactNode } from 'react'

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html>
      <body>
        <SessionProvider>
          {children}
        </SessionProvider>
      </body>
    </html>
  )
}
```

---

## 🎯 FILE STRUCTURE (PHASE 2)

```
app/
├── layout.tsx (add SessionProvider)
├── page.tsx (landing/redirect to login or dashboard)
├── login/
│   └── page.tsx (NEW)
├── signup/
│   └── page.tsx (NEW)
├── dashboard/
│   └── page.tsx (NEW - PeachScreen with auth)
├── api/
│   ├── auth/
│   │   └── [...nextauth]/route.ts (NEW)
│   ├── leads/
│   │   └── route.ts (NEW - user-scoped)
│   ├── trading-accounts/
│   │   └── route.ts (NEW - user-scoped)
│   └── batch-deployments/
│       └── route.ts (NEW - user-scoped)

lib/
├── auth.ts (NEW)
├── encryption.ts (NEW)
└── alpaca-client.ts (UPDATE - use session)

components/
├── main-app.tsx (NEW - wrapper for Leads/Trading/Settings)
└── (all existing components - update to use Supabase)
```

---

## 🌍 ENVIRONMENT VARIABLES

Add to `.env.local`:

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# NextAuth
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-generated-secret-key

# Encryption
ENCRYPTION_KEY=your-32-char-hex-key

# Alpaca (user provides via UI, stored encrypted)
# Not set here - input via Settings panel
```

---

## 🚀 SUPABASE SETUP STEPS

1. Create Supabase project
2. Run SQL schema above in SQL Editor
3. Enable Email Auth in Authentication settings
4. Get API keys (anon + service role)
5. Add to `.env.local`

---

## 📋 CHECKLIST FOR V0

- [ ] Add NextAuth.js + Supabase Auth
- [ ] Create login page with email/password
- [ ] Create signup page
- [ ] Create dashboard page (protected)
- [ ] Update all components to use `user_id`
- [ ] Add Supabase `.insert()` for user data
- [ ] Create API routes with auth middleware
- [ ] Encrypt Alpaca keys before storing
- [ ] Add SessionProvider to layout
- [ ] Update `main-app` to receive userId
- [ ] Add logout functionality
- [ ] Add user profile page (optional)
- [ ] Add theme preference to user_settings

---

## 🔗 OPENCLAW CONNECTION (LATER)

Once auth works, add OpenClaw integration:
- User provides OpenClaw URL in Settings
- Store encrypted in `user_settings.openclaw_url`
- Fetch batch status from: `{openclaw_url}/api/batches?user_id={user_id}`

---

## ✅ FINAL OUTPUT

After V0 generates:
1. Push to GitHub
2. Set env vars in Vercel
3. Deploy
4. Test: Sign up → Login → Dashboard → See leads + trading

You'll have:
✅ Multi-user platform
✅ Secure auth
✅ Data separated by user
✅ Ready for production

---

**END OF PROMPT**

**Next steps after V0 completes Phase 2**:
1. Supabase setup (tables + keys)
2. Deploy to Vercel
3. Test authentication flow
4. Phase 3: OpenClaw + Alpaca integration

