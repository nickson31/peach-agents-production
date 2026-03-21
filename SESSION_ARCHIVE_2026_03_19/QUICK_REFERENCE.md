# PEACH&AGENTS - QUICK REFERENCE

## 🔗 LINKS IMPORTANTES

### GitHub
- Create repo: https://github.com/new
- Your repos: https://github.com/nickson31
- Code location: https://github.com/nickson31/peach-agents-production

### Supabase
- Create project: https://supabase.com/dashboard/projects
- Dashboard: https://supabase.com/dashboard
- Your projects: https://supabase.com/dashboard/projects

### Vercel
- New project: https://vercel.com/new
- Dashboard: https://vercel.com/dashboard
- Live app: https://peach-agents-production.vercel.app

### Alpaca
- Account: https://app.alpaca.markets
- Paper trading: https://app.alpaca.markets/paper/dashboard

---

## 📋 CREDENCIALES

```
GitHub:
├─ Username: nickson31
├─ Email: willmnadarin@gmail.com
└─ Password: [yours]

Supabase:
├─ Email: willmnadarin@gmail.com
├─ Password: [same as GitHub or new]
└─ Project: peach-agents-production

Vercel:
├─ Email: willmnadarin@gmail.com
├─ Auth: Via GitHub (recommended)
└─ Project: peach-agents-production

Alpaca:
├─ Account ID: PA320EPZBPGV
├─ API Key: PKW445AWAOSGU2WJYCCFUZ47PR
├─ Secret: 7tmQ6gY5c4hdmqwEN3UAgv4to78WsGkWPmxUox4G7x4X
└─ Mode: Paper trading (no real money)
```

---

## ✅ DEPLOYMENT CHECKLIST

- [ ] GitHub repo created
- [ ] Code pushed to GitHub
- [ ] Supabase project created
- [ ] Database schema (schema.sql) executed
- [ ] API keys copied from Supabase
- [ ] Vercel environment variables set
- [ ] Vercel deployment complete
- [ ] App tested at live URL
- [ ] Users can signup
- [ ] Users can create bots
- [ ] Bots deploy to Alpaca

---

## 🔄 FILES YOU NEED

```
/home/ubuntu/.openclaw/workspace/

peach-agents-production/           ← SOURCE CODE
├── supabase/schema.sql            ← DATABASE SCHEMA (RUN THIS!)
├── .env.example                   ← ENV TEMPLATE
├── package.json                   ← DEPENDENCIES
└── README.md                       ← DOCUMENTATION

GITHUB_PUSH_READY.sh               ← RUN TO PUSH CODE

DEPLOY_STEPS_ACTUAL.md             ← FULL GUIDE

QUICK_REFERENCE.md                 ← THIS FILE
```

---

## 🎯 ENVIRONMENT VARIABLES (For Vercel)

```bash
# From Supabase Settings → API
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Alpaca (Paper Trading)
ALPACA_API=https://paper-api.alpaca.markets/v2
ALPACA_KEY=PKW445AWAOSGU2WJYCCFUZ47PR
ALPACA_SECRET=7tmQ6gY5c4hdmqwEN3UAgv4to78WsGkWPmxUox4G7x4X

# App URL
NEXT_PUBLIC_APP_URL=https://peach-agents-production.vercel.app
```

---

## 🚀 QUICK COMMANDS

### Push to GitHub (when repo exists)
```bash
cd /home/ubuntu/.openclaw/workspace
./GITHUB_PUSH_READY.sh https://github.com/nickson31/peach-agents-production.git
```

### Check git status
```bash
cd /home/ubuntu/.openclaw/workspace/peach-agents-production
git status
git log --oneline
```

### View source files
```bash
ls -la /home/ubuntu/.openclaw/workspace/peach-agents-production/

# Key files:
app/api/bots/route.ts              ← Bot API
app/api/bots/[id]/deploy/route.ts  ← Deployment
app/auth/login/page.tsx            ← Login page
app/dashboard/page.tsx             ← Dashboard
lib/supabase.ts                    ← Database
lib/auth.ts                        ← Authentication
supabase/schema.sql                ← Database schema
```

---

## 🔐 SECURITY NOTES

✅ DO:
- Add .env.local to .gitignore (already done)
- Use Vercel Secrets (not in code)
- Rotate API keys monthly
- Enable GitHub branch protection

❌ DON'T:
- Never commit .env files
- Never share API keys in public
- Never share Supabase service role key
- Never commit credentials

---

## 🆘 TROUBLESHOOTING

### GitHub push fails
```bash
# Check remote
git remote -v

# Fix if wrong
git remote set-url origin https://github.com/nickson31/peach-agents-production.git

# Try push again
git push -u origin main --force
```

### Supabase schema fails
- Go back to SQL editor
- Clear error
- Try one table at a time
- Check SQL syntax

### Vercel build fails
- Check all env vars are set
- No typos in keys
- Check Vercel build logs
- Ensure Node.js 18+ selected

### App not loading
- Verify Supabase project is running
- Check env vars in Vercel
- See deployment logs
- Test API endpoints locally

---

## 📞 SUPPORT STEPS

1. **Check logs**
   - GitHub: Commit history
   - Supabase: SQL errors
   - Vercel: Build & deployment logs
   - Browser console: JavaScript errors

2. **Verify config**
   - Env vars match Supabase keys
   - No extra spaces in keys
   - All required vars present

3. **Test locally**
   ```bash
   cd peach-agents-production
   npm install
   npm run dev
   ```

4. **Ask for help**
   - Share error message
   - Share log output
   - Share what you were doing

---

## 🎉 AFTER LAUNCH

Once everything is working:

### Share with users
- URL: https://peach-agents-production.vercel.app
- They can signup
- Create accounts
- Deploy trading bots

### Monitor
- Vercel dashboard → Logs
- Supabase → Database usage
- App → User activity

### Update code
```bash
# Make changes locally
git add .
git commit -m "Feature: ..."
git push origin main

# Auto-deploys to Vercel in 2-3 min
```

### Add features
- Modify API routes
- Add new pages
- Update database schema
- Deploy = automatic

---

**You're ready. Let's go! 🍑**
