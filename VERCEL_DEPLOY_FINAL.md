# VERCEL DEPLOYMENT - FINAL STEPS

## 📋 Environment Variables (Ready to Paste)

Copy these EXACTLY and add to Vercel:

```
NEXT_PUBLIC_SUPABASE_URL=https://xhdwqtsyhkztriqjnmzz.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sb_publishable_1Pi-yqgBYKvJybA0np6ZnQ_UFc4XY3t
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhoZHdxdHN5aGt6dHJpcWpubXp6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3Mzk0MzQxMiwiZXhwIjoyMDg5NTE5NDEyfQ.WOKdQcpX7TMlIjamhemSRjnWtvFXEo7b-u4uUCzjSXw

ALPACA_API=https://paper-api.alpaca.markets/v2
ALPACA_KEY=PKW445AWAOSGU2WJYCCFUZ47PR
ALPACA_SECRET=7tmQ6gY5c4hdmqwEN3UAgv4to78WsGkWPmxUox4G7x4X

NEXT_PUBLIC_APP_URL=https://peach-agents-production.vercel.app
NODE_ENV=production
```

---

## 🚀 VERCEL DEPLOYMENT STEPS

### STEP 1: Go to Vercel

1. Open: https://vercel.com/dashboard
2. Login (use GitHub account)

### STEP 2: Import Repository

1. Click: "Add New..." → "Project"
2. Click: "Import Git Repository"
3. Find: `peach-agents-production`
4. Click: "Import"

### STEP 3: Configure Project

Vercel will auto-detect:
- Framework: **Next.js** ✓
- Build Command: `pnpm build` ✓
- Output Directory: `.next` ✓

**Do NOT change these - they're correct**

### STEP 4: Add Environment Variables

1. In Vercel project setup page:
2. Scroll to: "Environment Variables"
3. Add each variable from above:

```
Key: NEXT_PUBLIC_SUPABASE_URL
Value: https://xhdwqtsyhkztriqjnmzz.supabase.co

Key: NEXT_PUBLIC_SUPABASE_ANON_KEY
Value: sb_publishable_1Pi-yqgBYKvJybA0np6ZnQ_UFc4XY3t

Key: SUPABASE_SERVICE_ROLE_KEY
Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Key: ALPACA_API
Value: https://paper-api.alpaca.markets/v2

Key: ALPACA_KEY
Value: PKW445AWAOSGU2WJYCCFUZ47PR

Key: ALPACA_SECRET
Value: 7tmQ6gY5c4hdmqwEN3UAgv4to78WsGkWPmxUox4G7x4X

Key: NEXT_PUBLIC_APP_URL
Value: https://peach-agents-production.vercel.app

Key: NODE_ENV
Value: production
```

### STEP 5: Deploy

1. Click: "Deploy"
2. Wait 2-3 minutes
3. See: "Congratulations! Your site is live"

### STEP 6: Get Live URL

After deployment completes:
```
https://peach-agents-production.vercel.app
```

---

## ✅ TESTING AFTER DEPLOYMENT

### Test 1: App Loads
1. Visit: https://peach-agents-production.vercel.app
2. Should see: Login page with "PEACH&AGENTS"

### Test 2: Signup
1. Click: "Sign up"
2. Email: test@example.com
3. Password: Test@12345
4. Click: "Sign Up"
5. Should see: Success message

### Test 3: Login
1. After signup, go to Login
2. Email: test@example.com
3. Password: Test@12345
4. Click: "Login"
5. Should see: Dashboard

### Test 4: Create Bot
1. On Dashboard, click: "Manage Bots"
2. Click: "Create Bot"
3. Fill:
   - Name: "Test Bot"
   - Strategy: "Trend Following"
   - Symbols: ETHE, GBTC
   - Allocation: 60% / 40%
4. Click: "Deploy"
5. Should connect to Alpaca

---

## 🎯 FINAL SUMMARY

| Step | Status | Time |
|------|--------|------|
| GitHub repo | ✅ DONE | 2026-03-19 18:22 |
| Code pushed | ✅ DONE | 2026-03-19 18:22 |
| Supabase project | ✅ DONE | Now |
| Schema executed | ⏳ WAITING | (you) |
| Vercel deploy | ⏳ NEXT | (you) |
| Testing | ⏳ AFTER | (you) |

---

## 🚨 IF SOMETHING FAILS

### Build fails on Vercel
- Check all env vars are set (no typos)
- See: Vercel Deployments → Logs
- Common: Missing env var

### App won't load
- Check Supabase project is running
- Verify all 3 Supabase keys are correct
- Check browser console for errors

### Login fails
- Verify Supabase is connected
- Check auth is enabled
- See Supabase logs

### Bot deployment fails
- Check Alpaca keys are correct
- Verify paper trading account active
- See Vercel logs

---

**Ready? Do Supabase schema first, then Vercel.** 🍑
