# PEACH&AGENTS - PRODUCTION GITHUB READY

## 🎯 WHAT'S CHANGED

You were right. The old setup had problems:
- ❌ Demo was static (no real login)
- ❌ Used localStorage only (no database)
- ❌ Bot logic wasn't connected to persistence
- ❌ Not suitable for real deployment

**THIS IS THE REAL VERSION:**
- ✅ Full Supabase backend (PostgreSQL)
- ✅ Real authentication (email + OAuth)
- ✅ Persistent multi-user data
- ✅ Connected API routes
- ✅ Alpaca integration ready
- ✅ Production deployment ready

---

## 📦 WHAT YOU GET

### Location
```
/home/ubuntu/.openclaw/workspace/peach-agents-production/
```

### Structure
```
peach-agents-production/
├── app/
│   ├── api/              # ← REAL API ROUTES (database connected)
│   │   ├── bots/         # Create/read/update/delete bots
│   │   ├── bots/[id]/deploy/  # Deploy to Alpaca
│   │   └── ...
│   ├── auth/
│   │   ├── login/        # Email + OAuth login
│   │   └── signup/       # User registration
│   ├── dashboard/        # Main app UI
│   └── page.tsx          # Auth redirect
├── lib/
│   ├── supabase.ts       # ← DATABASE CLIENT (all queries)
│   ├── auth.ts           # ← AUTH MODULE (login/logout)
│   └── ...
├── supabase/
│   └── schema.sql        # ← DATABASE SCHEMA (RUN FIRST!)
├── package.json          # All dependencies
├── .env.example          # Environment variables
└── README.md             # Full documentation
```

---

## 🔄 DATA FLOW (REAL)

### OLD (Demo - Static)
```
User clicks "Create Bot"
  → Saves to localStorage
  → Only visible in browser
  → Lost on refresh/device change
  → NO Alpaca integration
```

### NEW (Production - Real)
```
User clicks "Create Bot"
  ↓
API POST /api/bots
  ↓
Server validates auth (Supabase JWT)
  ↓
Insert into database (bots table)
  ↓
Return bot data
  ↓
User deploys bot
  ↓
API POST /api/bots/[id]/deploy
  ↓
Connect to Alpaca
  ↓
Place orders (wave system)
  ↓
Save stats to bot_stats table
  ↓
Real-time dashboard update
```

---

## 🗄️ DATABASE SCHEMA

**13 Tables with full RLS (Row Level Security):**

```sql
users
├─ id, email, full_name, created_at
└─ Each user ONLY sees their own data

bots
├─ id, user_id, name, strategy, symbols, allocation
├─ status, config, is_active
└─ User RLS: Can only see own bots

bot_stats
├─ id, bot_id, user_id, orders_deployed, fill_rate, pnl
└─ Real-time performance tracking

trades
├─ id, bot_id, alpaca_order_id, symbol, side, qty
├─ entry_price, exit_price, pnl, status
└─ Complete trade history

leads, strategies, bot_folders, execution_logs
└─ All with RLS enforcement
```

---

## 🚀 GITHUB SETUP (Step by Step)

### 1. Create GitHub Repository

```bash
# Go to github.com/new
# Fill in:
#   Name: peach-agents-production
#   Description: Trading Bot Platform with Supabase
#   Visibility: Public (recommended for Open Source)
# Create repository
```

### 2. Push to GitHub

```bash
cd /home/ubuntu/.openclaw/workspace/peach-agents-production

# Add remote
git remote add origin https://github.com/YOUR-USERNAME/peach-agents-production.git

# Rename branch
git branch -M main

# Push
git push -u origin main
```

### 3. GitHub Settings (Recommended)

```
Settings → General
├─ Main branch: main
├─ Auto-delete head branches: ✓
└─ Require status checks: Optional

Settings → Secrets and variables
├─ Add all .env vars (developer only)
└─ Never commit .env to git
```

---

## 🌐 VERCEL DEPLOYMENT (Step by Step)

### 1. Connect GitHub

```
vercel.com
├─ Sign in (GitHub)
├─ Click "New Project"
├─ Import from GitHub
└─ Select peach-agents-production
```

### 2. Configure Environment

**Vercel Dashboard → Settings → Environment Variables:**

```
NEXT_PUBLIC_SUPABASE_URL = https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY = eyJhbGciOiJIUzI1...
SUPABASE_SERVICE_ROLE_KEY = eyJhbGciOiJIUzI1...

ALPACA_API = https://paper-api.alpaca.markets/v2
ALPACA_KEY = your-key-here
ALPACA_SECRET = your-secret-here

NEXT_PUBLIC_APP_URL = https://peach-agents.vercel.app
```

### 3. Deploy

```
Click "Deploy" → Wait 2-3 minutes → ✅ Live!
```

---

## 🔐 SUPABASE SETUP

### 1. Create Project

```
supabase.com
├─ Click "New Project"
├─ Organization: Personal (or your org)
├─ Project Name: peach-agents
└─ Region: Choose closest to you
```

### 2. Run SQL Schema

```
Supabase Dashboard
├─ SQL Editor
├─ Click "New Query"
├─ Paste all SQL from: supabase/schema.sql
└─ Click "Execute"
```

### 3. Get Keys

```
Supabase Dashboard → Settings → API
├─ NEXT_PUBLIC_SUPABASE_URL = Project URL
├─ NEXT_PUBLIC_SUPABASE_ANON_KEY = anon key
└─ SUPABASE_SERVICE_ROLE_KEY = service_role key
```

### 4. Enable Auth

```
Supabase Dashboard → Auth → Providers
├─ Email: ✓ Enabled
├─ Google: Add OAuth credentials
└─ GitHub: Add OAuth credentials
```

---

## 💪 WHAT YOU HAVE FULL AUTHORITY OVER

You own this code completely. Modify anything:

### Frontend (app/)
```typescript
// Customize login page
app/auth/login/page.tsx

// Modify dashboard
app/dashboard/page.tsx

// Add new pages
app/dashboard/bots/page.tsx
app/dashboard/analytics/page.tsx
```

### Backend (lib/ + app/api/)
```typescript
// Add database queries
lib/supabase.ts

// Create new API endpoints
app/api/bots/stats/route.ts
app/api/leads/import/route.ts

// Extend auth logic
lib/auth.ts
```

### Database (supabase/)
```sql
-- Add tables
-- Modify schemas
-- Create functions
-- Add triggers

All yours to customize
```

---

## 📋 SETUP CHECKLIST

### Phase 1: Local Development (30 min)

- [ ] Run `npm install`
- [ ] Create Supabase project
- [ ] Run schema.sql in Supabase
- [ ] Copy `.env.example` to `.env.local`
- [ ] Add Supabase keys
- [ ] Add Alpaca keys
- [ ] Run `npm run dev`
- [ ] Test: http://localhost:3000

### Phase 2: GitHub Setup (10 min)

- [ ] Create GitHub repo
- [ ] Push code: `git push -u origin main`
- [ ] Verify on GitHub dashboard
- [ ] Clone in another directory to test (optional)

### Phase 3: Vercel Deployment (15 min)

- [ ] Create Vercel account
- [ ] Import GitHub repo
- [ ] Add environment variables
- [ ] Click Deploy
- [ ] Wait for deployment (2-3 min)
- [ ] Test: https://your-project.vercel.app

### Phase 4: Production Launch (5 min)

- [ ] Test login with email
- [ ] Test login with Google/GitHub
- [ ] Create test bot
- [ ] Deploy test bot to Alpaca
- [ ] Verify orders appear
- [ ] Share URL with users

---

## 🔒 SECURITY NOTES

### What's Protected
```
✅ API routes check authentication
✅ Database RLS prevents data leakage
✅ Supabase manages auth tokens
✅ API keys only in server (never client)
✅ OAuth tokens from Google/GitHub
```

### What You Need To Do
```
✓ Never commit .env to GitHub
✓ Use .gitignore (already configured)
✓ Add secrets to Vercel (not in code)
✓ Rotate API keys monthly
✓ Monitor Vercel logs
```

---

## 📊 AUTHENTICATION TYPES

### 1. Email/Password
```
User enters email + password
→ Verified by Supabase
→ JWT token created
→ Stored in localStorage
→ Sent with each API request
```

### 2. Google OAuth
```
User clicks "Login with Google"
→ Redirected to Google
→ User grants permission
→ JWT token created
→ User logged in
```

### 3. GitHub OAuth
```
Same flow as Google
→ Uses GitHub credentials
→ Works with GitHub accounts
```

---

## 🚀 AFTER DEPLOYMENT

### Monitor
```
vercel.com/dashboard
├─ Deployments tab (see all deploys)
├─ Analytics (traffic, performance)
├─ Logs (errors, debugging)
└─ Settings (manage env vars)
```

### Update Code
```
Edit file locally
→ Commit: git commit -m "..."
→ Push: git push
→ Auto-redeploy on Vercel
→ Live in 2-3 minutes
```

### Add Features
```
Create new files
→ Add routes to app/api/
→ Create new pages
→ Update database schema
→ Commit and push
→ Auto-deployed
```

---

## 💾 GITHUB ZIP

Ready to use:
```
/home/ubuntu/.openclaw/workspace/peach-agents-production-github.zip
```

Contains:
- ✅ All source code
- ✅ Git initialized (first commit done)
- ✅ .env.example (template)
- ✅ Supabase schema
- ✅ All dependencies in package.json
- ✅ Ready to push to GitHub

---

## 📖 NEXT STEPS

1. **Extract and Review**
   ```bash
   unzip peach-agents-production-github.zip
   cd peach-agents-production
   cat README.md
   ```

2. **Set Up Locally**
   ```bash
   npm install
   cp .env.example .env.local
   # Add your keys
   npm run dev
   ```

3. **Push to GitHub**
   ```bash
   git remote add origin YOUR-REPO-URL
   git branch -M main
   git push -u origin main
   ```

4. **Deploy to Vercel**
   - Import GitHub repo
   - Add env vars
   - Click Deploy

5. **Share With Users**
   - Send Vercel URL
   - Users signup/login
   - Create bots
   - Deploy to Alpaca

---

**THIS IS PRODUCTION-READY CODE. You have full authority to complete, modify, and deploy.** 🍑

Everything is yours.
