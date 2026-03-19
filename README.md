# PEACH&AGENTS - Production Ready

**Trading Bot Management Platform with Supabase Backend**

> ⚠️ **THIS IS A REAL PRODUCTION SETUP** - Not a demo. Full authentication, database, and deployment ready.

## 🎯 What's Different From The Demo

The original ZIP was a **static demo** with localStorage only. This version is **fully functional** with:

- ✅ **Supabase PostgreSQL Backend** - Persistent data storage
- ✅ **Real Authentication** - Email/password + Google + GitHub OAuth
- ✅ **Multi-user Support** - Each user has their own data
- ✅ **Real API Endpoints** - Connected to database
- ✅ **Alpaca Integration** - Actual trading deployment
- ✅ **Production Ready** - Deploy to Vercel immediately

## 🚀 Quick Start

### 1. Set Up Supabase

```bash
# Go to supabase.com
# Create new project
# Go to SQL Editor and run:
```

Copy all SQL from `supabase/schema.sql` and run it in Supabase.

### 2. Install & Configure

```bash
# Install dependencies
npm install
# or
pnpm install

# Copy env file
cp .env.example .env.local

# Add your credentials
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
ALPACA_KEY=your-alpaca-key
ALPACA_SECRET=your-alpaca-secret
```

### 3. Run Locally

```bash
npm run dev
# Visit http://localhost:3000
```

### 4. Deploy to Vercel

```bash
# Push to GitHub
git add .
git commit -m "Initial commit"
git push

# Go to vercel.com
# Import your GitHub repo
# Add environment variables
# Deploy
```

## 📁 Project Structure

```
peach-agents-production/
├── app/
│   ├── api/              # API routes (connected to DB)
│   │   ├── bots/        # Bot CRUD operations
│   │   ├── bots/[id]/deploy/  # Alpaca deployment
│   │   └── ...
│   ├── auth/            # Login/signup pages
│   │   ├── login/
│   │   └── signup/
│   ├── dashboard/       # Main dashboard
│   └── layout.tsx
├── lib/
│   ├── supabase.ts      # Database client + functions
│   ├── auth.ts          # Authentication
│   └── ...
├── supabase/
│   └── schema.sql       # Database schema (RUN THIS!)
├── .env.example         # Environment template
└── package.json
```

## 🔐 Authentication

Users can login with:
- 📧 **Email/Password** - Traditional login
- 🔵 **Google** - OAuth
- 🐙 **GitHub** - OAuth

Each user gets their own isolated workspace with RLS (Row Level Security).

## 💾 Database

**Supabase PostgreSQL** with full schema:
- `users` - User accounts
- `bots` - Trading bot configs
- `bot_stats` - Performance history
- `trades` - Individual trade records
- `leads` - Trading signals/leads
- `strategies` - Pre-built strategies
- `execution_logs` - Audit trail

**Row Level Security (RLS)** - Users can ONLY see their own data.

## 🤖 Bot Management

```typescript
// Create a bot
POST /api/bots
{
  name: "My Bot",
  strategy: "trend-following",
  symbols: ["ETHE", "GBTC"],
  allocation: { ETHE: 0.6, GBTC: 0.4 },
  config: {
    takeProfit: 0.03,
    stopLoss: -0.01,
    batchSize: 100,
    waveInterval: 90
  }
}

// Deploy bot to Alpaca
POST /api/bots/[id]/deploy

// Get all bots
GET /api/bots

// Update bot
PUT /api/bots/[id]

// Delete bot
DELETE /api/bots/[id]
```

## 📊 Features

- ✅ Multi-user authentication
- ✅ Bot creation & management
- ✅ Real-time deployment to Alpaca
- ✅ Performance tracking
- ✅ Trade history
- ✅ Lead management
- ✅ Strategy templates
- ✅ Audit trails
- ✅ Portfolio analytics
- ✅ Responsive UI

## 🔄 Real-Time Data

All bots are synced with Alpaca in real-time:
- Live order status
- Fill rates
- P&L calculations
- Account equity tracking

## 🚨 Important

1. **Supabase Schema** - Must run `supabase/schema.sql` first!
2. **API Keys** - Add to `.env.local` before running
3. **Alpaca Account** - Create paper trading account at alpaca.markets
4. **Vercel Secrets** - Add all env vars when deploying

## 🛠️ What You Need To Do

As the developer (you have full authority):

1. ✅ Set up Supabase project
2. ✅ Run the SQL schema
3. ✅ Configure environment variables
4. ✅ Test locally
5. ✅ Deploy to Vercel
6. ✅ Add any custom features (you own this code)

## ⚙️ Customization Points

All files are yours to modify:

```
- lib/supabase.ts → Database queries
- lib/auth.ts → Authentication logic
- app/api/ → API endpoints
- app/dashboard/ → UI pages
```

You have full permission to extend, modify, and deploy.

## 🎓 Learning Resources

- [Supabase Docs](https://supabase.com/docs)
- [Next.js Docs](https://nextjs.org/docs)
- [Alpaca API](https://alpaca.markets/docs)

---

**This is production-ready code. Deploy with confidence.** 🍑
