# PEACH&AGENTS - DEPLOYMENT INSTRUCTIONS

## 🎯 COMPLETE DEPLOYMENT GUIDE

Your application is ready to deploy. Follow these steps exactly.

---

## STEP 1: CREATE GITHUB REPOSITORY

1. Go to [github.com/new](https://github.com/new)
2. Fill in:
   - **Repository name**: `peach-agents`
   - **Description**: "Trading Bot Platform with Multi-Source AI"
   - **Privacy**: Public or Private (your choice)
3. Click "Create repository"
4. Copy the HTTPS URL (you'll need this)

---

## STEP 2: PUSH TO GITHUB

### On your machine:

```bash
cd /home/ubuntu/.openclaw/workspace/peach-agents-platform

# Configure git (if not done)
git config user.name "Your Name"
git config user.email "your@email.com"

# Add remote (replace with YOUR GitHub URL)
git remote add origin https://github.com/YOUR-USERNAME/peach-agents.git

# Rename branch and push
git branch -M main
git push -u origin main
```

**Done!** Your code is now on GitHub.

---

## STEP 3: DEPLOY TO VERCEL

### Via GitHub (Recommended):

1. Go to [vercel.com](https://vercel.com)
2. Login with GitHub
3. Click "New Project"
4. Click "Import Git Repository"
5. Find `peach-agents` in your GitHub repos
6. Click "Import"

Vercel will:
- Detect it's Next.js ✓
- Suggest framework settings ✓
- Show environment variable form

### Continue on Vercel dashboard:

1. **Add Environment Variables** (critical step):

   ```
   JWT_SECRET = peach-agents-ultra-secure-key-2026-only-you
   PEACH_EMAIL = you@peach-agents.local
   PEACH_PASSWORD = PeachAgents2026!Secure
   
   ALPACA_API = https://paper-api.alpaca.markets/v2
   ALPACA_KEY = (your key from alpaca.markets)
   ALPACA_SECRET = (your secret from alpaca.markets)
   
   BRAVE_SEARCH_API_KEY = (from search.brave.com)
   YOUTUBE_API_KEY = (from console.cloud.google.com)
   TWITTER_BEARER_TOKEN = (from developer.twitter.com)
   ```

2. Click "Deploy"

**Wait 2-3 minutes** for deployment...

---

## STEP 4: CONFIGURE ENVIRONMENT VARIABLES

### Get Your API Keys:

#### Alpaca (Paper Trading)
1. Go to [app.alpaca.markets](https://app.alpaca.markets)
2. Sign up for free (paper trading account)
3. Go to Settings → API Keys
4. Copy `API Key` and `Secret Key`

#### Brave Search (Google Alternative)
1. Go to [search.brave.com/api](https://www.search.brave.com/api/)
2. Sign up
3. Create API key
4. Copy it

#### YouTube API
1. Go to [console.cloud.google.com](https://console.cloud.google.com/)
2. Create new project
3. Enable YouTube Data API v3
4. Create API key
5. Copy it

#### Twitter (Optional)
1. Go to [developer.twitter.com](https://developer.twitter.com/)
2. Create app
3. Get Bearer Token
4. Copy it

### Add to Vercel:

1. Go to your Vercel project
2. Click Settings → Environment Variables
3. Add each variable from above
4. Click "Save"
5. Redeploy: Click "Deployments" → Latest → "Redeploy"

---

## STEP 5: CUSTOM DOMAIN (Optional)

1. Go to Vercel project → Settings → Domains
2. Add your custom domain
3. Follow DNS configuration
4. Update `NEXT_PUBLIC_APP_URL` env var if using custom domain

---

## STEP 6: FIRST LOGIN

1. Visit your Vercel URL: `https://peach-agents.vercel.app`
2. Login with:
   - **Username**: `peach`
   - **Password**: `PeachAgents2026!Secure`
3. You're in! 🎉

---

## STEP 7: CREATE FIRST BOT

1. Go to "Management" page (Tab 4)
2. Click "Create Bot"
3. Fill in:
   - **Name**: "My First Bot"
   - **Strategy**: "Trend Following"
   - **Symbols**: ETHE, GBTC
   - **Allocation**: ETHE 60%, GBTC 40%
4. Click "Deploy"
5. Watch the waves deploy! 🌊

---

## TROUBLESHOOTING

### ❌ Deployment Failed

**Error**: `pnpm install failed`
- Solution: Check Node.js version (must be 18+)
- Vercel auto-handles this, usually works

**Error**: `Build failed - TypeScript error`
- Solution: Check `tsconfig.json` in repo
- Likely permission issue, verify all files pushed

**Error**: `Environment variable not found`
- Solution: Make sure ALL env vars are set in Vercel
- Missing even one will fail some features
- Set blanks if you don't have all APIs yet

### ❌ Login Failed

**Error**: `Invalid credentials`
- Solution: Check PEACH_PASSWORD in Vercel env vars
- Default is: `PeachAgents2026!Secure`
- Make sure no extra spaces

**Error**: `JWT error`
- Solution: Check JWT_SECRET in Vercel env vars
- Make sure it matches value you set

### ❌ Bot Deployment Failed

**Error**: `Alpaca API error`
- Solution: Check ALPACA_KEY and ALPACA_SECRET
- Make sure they're for PAPER TRADING account
- Verify at [app.alpaca.markets](https://app.alpaca.markets)

**Error**: `Search not working`
- Solution: Add missing API keys:
  - `BRAVE_SEARCH_API_KEY`
  - `YOUTUBE_API_KEY`
  - Works without Twitter key (optional)

---

## 📊 MONITORING DEPLOYMENT

### Check Deployment Status:

1. Go to Vercel dashboard
2. Click "Deployments"
3. Green checkmark = Success ✅
4. Red X = Failed ❌

### View Logs:

1. Click on failed deployment
2. Click "Build Logs" tab
3. Scroll to see error

### Redeploy:

1. Go to Deployments
2. Click on latest successful deploy
3. Click "Redeploy"

---

## 🔒 SECURITY BEST PRACTICES

1. **Never share your JWT_SECRET** - Keep it private
2. **Rotate API keys** - Do monthly
3. **Use strong PEACH_PASSWORD** - No default passwords in prod
4. **Monitor Vercel logs** - Check for unusual activity
5. **Keep GitHub private** - Contains sensitive config

---

## 📞 PRODUCTION READINESS CHECKLIST

- [ ] GitHub repository created and pushed
- [ ] Vercel project created
- [ ] All environment variables configured
- [ ] Custom domain set (optional)
- [ ] SSL/TLS enabled (automatic on Vercel)
- [ ] First bot created and deployed successfully
- [ ] Alpaca paper trading account verified
- [ ] API keys tested and working

---

## 🎉 YOU'RE LIVE!

Your trading platform is now live at: `https://your-domain.vercel.app`

Next steps:
1. Create multiple bots
2. Search for trading strategies
3. Deploy to Alpaca
4. Monitor performance
5. Optimize allocations
6. Scale deployment

---

## 📚 DOCUMENTATION

- **README.md** - Overview and features
- **README_IMPLEMENTATION.md** - Technical details
- **.env.example** - All environment variables
- This file - Deployment guide

---

**PEACH&AGENTS is now deployed and ready to trade!** 🍑
