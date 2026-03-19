# PEACH&AGENTS - DEPLOYMENT STEPS (ACTUAL)

## 👤 CREDENCIALES

```
GitHub: nickson31
Email: willmnadarin@gmail.com

Supabase Project:
- Email: willmnadarin@gmail.com
- Project: peach-agents-production

Vercel:
- Email: willmnadarin@gmail.com

Alpaca:
- Account: PA320EPZBPGV
- Key: PKW445AWAOSGU2WJYCCFUZ47PR
- Secret: 7tmQ6gY5c4hdmqwEN3UAgv4to78WsGkWPmxUox4G7x4X
```

---

## STEP 1: CREATE GITHUB REPO (Manual)

### What you do:
1. Open: https://github.com/new
2. Repository name: `peach-agents-production`
3. Description: `Trading Bot Platform with Supabase`
4. Visibility: `Public`
5. Click: "Create repository"

### After creation:
- Copy the URL: `https://github.com/nickson31/peach-agents-production`
- Send URL to me

---

## STEP 2: PUSH CODE (I do this)

```bash
cd /home/ubuntu/.openclaw/workspace/peach-agents-production
git remote add origin https://github.com/nickson31/peach-agents-production.git
git branch -M main
git push -u origin main
```

This will:
- ✅ Upload all source code
- ✅ Push database schema
- ✅ Push API routes
- ✅ Push authentication code

---

## STEP 3: SUPABASE SETUP (Manual + Automated)

### 3a. Create Supabase Project
1. Go to: https://supabase.com
2. Click: "New project"
3. Organization: "Personal" (default)
4. Project name: `peach-agents-production`
5. Database password: (let it auto-generate)
6. Region: Choose closest to you
7. Click: "Create new project"

Wait 2-3 minutes for project to initialize...

### 3b. Run Database Schema
1. In Supabase dashboard, go to: SQL Editor
2. Click: "New Query"
3. Name: "PEACH SCHEMA"
4. Open file: `supabase/schema.sql`
5. Copy ALL SQL
6. Paste into Supabase
7. Click: "Execute"

Wait for completion...

### 3c. Get API Keys
1. Go to: Settings → API
2. Copy these:
   - `NEXT_PUBLIC_SUPABASE_URL` = Project URL
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY` = anon public key
   - `SUPABASE_SERVICE_ROLE_KEY` = service_role key

Save these - need for Vercel

### 3d. Enable OAuth (Optional but Recommended)
1. Go to: Auth → Providers
2. Google:
   - Click "Enable"
   - Use Google Cloud credentials (or skip for now)
3. GitHub:
   - Click "Enable"
   - Use GitHub OAuth (or skip for now)

---

## STEP 4: VERCEL DEPLOYMENT (Automated)

### 4a. Connect GitHub
1. Go to: https://vercel.com
2. Sign in with GitHub
3. Click: "New Project"
4. Click: "Import Git Repository"
5. Find: `peach-agents-production` (your repo)
6. Click: "Import"

### 4b. Add Environment Variables
In Vercel, go to: Settings → Environment Variables

Add these (from Supabase Step 3c):
```
NEXT_PUBLIC_SUPABASE_URL = [from Supabase Settings]
NEXT_PUBLIC_SUPABASE_ANON_KEY = [from Supabase Settings]
SUPABASE_SERVICE_ROLE_KEY = [from Supabase Settings]

ALPACA_API = https://paper-api.alpaca.markets/v2
ALPACA_KEY = PKW445AWAOSGU2WJYCCFUZ47PR
ALPACA_SECRET = 7tmQ6gY5c4hdmqwEN3UAgv4to78WsGkWPmxUox4G7x4X

NEXT_PUBLIC_APP_URL = https://peach-agents-production.vercel.app
```

### 4c. Deploy
1. In Vercel, click: "Deploy"
2. Wait 2-3 minutes
3. See: "Deployment complete" ✅

---

## STEP 5: TEST DEPLOYMENT

### Test URL
Visit: `https://peach-agents-production.vercel.app`

You should see:
1. "PEACH&AGENTS" title
2. Login page

### Test Login
1. Go to: Signup page
2. Email: test@example.com
3. Password: TestPass123!
4. Click: "Sign Up"

You should get confirmation and redirect to login.

### Test Alpaca Integration
1. Login with test account
2. Go to: Dashboard
3. Click: "Manage Bots"
4. Create bot:
   - Name: "Test Bot"
   - Strategy: "Trend Following"
   - Symbols: ETHE, GBTC
   - Allocation: 60% / 40%
5. Click: "Deploy"

Should connect to Alpaca and show results.

---

## TIMELINE

| Step | Time | Who |
|------|------|-----|
| 1. GitHub repo | 2 min | You |
| 2. Push code | 5 min | Me (automated) |
| 3a. Supabase create | 5 min | You |
| 3b. Run schema | 2 min | You |
| 3c. Get keys | 3 min | You |
| 3d. OAuth (optional) | 5 min | You (skip ok) |
| 4. Vercel deploy | 10 min | You |
| 5. Test | 5 min | You |
| **TOTAL** | **~37 min** | **Both** |

---

## QUICK SUMMARY

### What I'm doing (automated):
- ✅ Configure git locally
- ✅ Push to GitHub
- ✅ Verify uploads

### What you're doing (manual):
1. Create GitHub repo
2. Create Supabase project
3. Run SQL schema in Supabase
4. Get Supabase keys
5. Add keys to Vercel
6. Deploy on Vercel
7. Test the live URL

---

## SUPPORT

If something fails:

**GitHub push fails:**
- Check URL is correct
- Verify repo exists

**Supabase schema fails:**
- Check SQL syntax
- Verify all text copied
- Try one table at a time

**Vercel deploy fails:**
- Check env vars are set
- Check no typos in keys
- See build logs in Vercel

**Login fails:**
- Check Supabase project is running
- Check env vars in Vercel
- Check network logs in browser

---

## AFTER DEPLOYMENT

You now have:
- ✅ Live production URL
- ✅ User authentication working
- ✅ Database connected
- ✅ Alpaca integration ready
- ✅ Full ownership of code

### Next: Users
Share URL with users and they can:
1. Signup/login
2. Create trading bots
3. Deploy to Alpaca
4. Monitor performance

---

**Ready to start?** 🍑
