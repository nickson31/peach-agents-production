# PEACH&AGENTS - QUICK START CHECKLISTS

## FOR DEVELOPER (You)

### ✅ Pre-Deployment Checklist

**GitHub Setup (30 min)**
- [ ] Create GitHub repo: `peach-agents`
- [ ] Configure git locally
- [ ] Push all code: `git push -u origin main`
- [ ] Verify on GitHub dashboard

**Vercel Deployment (45 min)**
- [ ] Sign up to vercel.com
- [ ] Connect GitHub account
- [ ] Import peach-agents repository
- [ ] Vercel auto-detects Next.js ✓

**API Keys (2 hours)**
- [ ] Get Alpaca keys (alpaca.markets)
  - API Key: `____________________`
  - Secret: `____________________`
- [ ] Get Brave Search key (search.brave.com)
  - Key: `____________________`
- [ ] Get YouTube API key (console.cloud.google.com)
  - Key: `____________________`
- [ ] Get Twitter Bearer Token (developer.twitter.com) - Optional
  - Token: `____________________`

**Vercel Environment Variables (30 min)**
- [ ] Add to Vercel dashboard:
  ```
  JWT_SECRET = (generate random 32+ chars)
  PEACH_EMAIL = you@peach-agents.local
  PEACH_PASSWORD = (strong password you'll give users)
  ALPACA_API = https://paper-api.alpaca.markets/v2
  ALPACA_KEY = (from above)
  ALPACA_SECRET = (from above)
  BRAVE_SEARCH_API_KEY = (from above)
  YOUTUBE_API_KEY = (from above)
  TWITTER_BEARER_TOKEN = (optional)
  NEXT_PUBLIC_APP_URL = https://your-deployed-url.vercel.app
  ```

**First Deployment (5 min)**
- [ ] Click "Deploy" on Vercel
- [ ] Wait 2-3 minutes
- [ ] Green checkmark appears = Success ✓

**Test Deployment (10 min)**
- [ ] Visit deployed URL
- [ ] Login: username=`peach`, password=`(your PEACH_PASSWORD)`
- [ ] Can you see dashboard? If no → check Vercel logs

**Document Your Setup (15 min)**
- [ ] Save master password somewhere safe
- [ ] Save JWT_SECRET somewhere safe
- [ ] Document which API keys are active
- [ ] Share deployment URL with authorized users

---

## FOR USERS (Your Customers)

### ✅ First Time Setup Checklist

**Get Access (5 min)**
- [ ] Receive deployment URL from developer
- [ ] Receive login credentials:
  - Username: `peach`
  - Password: `__________________` (from developer)

**First Login (5 min)**
- [ ] Visit deployment URL
- [ ] Login with provided credentials
- [ ] You see dashboard = Success ✓

**Create First Bot (15 min)**
- [ ] Go to "Management" tab
- [ ] Click "Create Bot"
- [ ] Fill in:
  ```
  Name: "My First Bot"
  Strategy: "Trend Following"
  Symbols: Select ETHE, GBTC
  Allocation: ETHE 60%, GBTC 40%
  Take Profit: 3%
  Stop Loss: 1%
  ```
- [ ] Click "Deploy"
- [ ] Watch waves deploy on screen

**Monitor First Bot (5 min)**
- [ ] Go to "Management" → "Bots" tab
- [ ] See your bot with live stats:
  - Fill rate %
  - Orders deployed
  - P&L $
- [ ] Understand what you see

**Optional: Try Search (10 min)**
- [ ] Go to "Research" tab
- [ ] Search for: "Best scalping strategy"
- [ ] Click on YouTube videos
- [ ] Extract signals for next bot

---

## 🚀 TIME ESTIMATES

| Task | Time | Who |
|------|------|-----|
| GitHub setup | 30 min | Developer |
| Vercel deployment | 45 min | Developer |
| API keys collection | 2 hours | Developer |
| Vercel config | 30 min | Developer |
| First deploy | 5 min | Developer |
| Testing | 10 min | Developer |
| **Total Developer** | **~4 hours** | Developer |
| User first login | 5 min | User |
| Create first bot | 15 min | User |
| Monitor bot | 5 min | User |
| Try search | 10 min | User |
| **Total User** | **~35 min** | User |

---

## 🔑 CREDENTIALS TO SHARE WITH USERS

**What to give users:**
```
Login Portal: https://your-deployed-url.vercel.app
Username: peach
Password: [your PEACH_PASSWORD from .env]
```

**What NOT to share:**
- JWT_SECRET
- API keys
- GitHub password
- Vercel admin access
- Database credentials (none yet)

---

## 🆘 IF SOMETHING FAILS

### Deploy failed?
- Check Vercel logs → Deployments → [latest] → Build Logs
- Look for error message
- Usually: missing env var or syntax error

### Login failed?
- Verify PEACH_PASSWORD in Vercel env vars
- Check no extra spaces
- Restart browser (clear cache)

### Bot deploy failed?
- Verify ALPACA_KEY and ALPACA_SECRET
- Ensure paper trading account is active at alpaca.markets
- Check Vercel function logs

### Search not working?
- Add missing API keys (Brave, YouTube, Twitter)
- Verify keys are valid
- Check rate limits not exceeded

---

## 📞 QUICK LINKS

**For Developer:**
- GitHub: https://github.com
- Vercel: https://vercel.com
- Alpaca: https://app.alpaca.markets
- Brave Search: https://www.search.brave.com/api/
- YouTube API: https://console.cloud.google.com/
- Twitter API: https://developer.twitter.com/

**For Users:**
- [Your deployment URL]
- Documentation: README.md
- Help: [Support email/channel]

---

## ✅ SUCCESS CRITERIA

**Developer is done when:**
- ✅ Deployment URL works
- ✅ Can login with credentials
- ✅ Can create a bot
- ✅ Bot deploys to Alpaca
- ✅ All API keys working
- ✅ Dashboard shows live data

**Users are happy when:**
- ✅ Can login easily
- ✅ Can create bots in <15 min
- ✅ Can see real-time performance
- ✅ Orders deploy to Alpaca
- ✅ Dashboard is intuitive
- ✅ Search finds strategies

---

**PEACH&AGENTS ready to launch!** 🍑
