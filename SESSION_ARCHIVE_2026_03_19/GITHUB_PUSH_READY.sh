#!/bin/bash

# PEACH&AGENTS - GitHub Push Script
# Run this when GitHub repo is created

GITHUB_URL="$1"  # Pass as argument: ./script.sh https://github.com/nickson31/peach-agents-production.git

if [ -z "$GITHUB_URL" ]; then
    echo "Usage: ./GITHUB_PUSH_READY.sh https://github.com/nickson31/peach-agents-production.git"
    exit 1
fi

echo "🚀 PUSHING PEACH&AGENTS TO GITHUB..."
echo "URL: $GITHUB_URL"

cd /home/ubuntu/.openclaw/workspace/peach-agents-production

# Configure git
echo "📝 Configuring git..."
git config user.name "nickson31"
git config user.email "willmnadarin@gmail.com"

# Add remote
echo "🔗 Adding remote..."
git remote add origin "$GITHUB_URL" 2>/dev/null || git remote set-url origin "$GITHUB_URL"

# Rename branch to main
echo "🏷️ Renaming branch to main..."
git branch -M main

# Push to GitHub
echo "📤 Pushing code to GitHub..."
git push -u origin main --force

echo "✅ DONE! Your code is now on GitHub"
echo "URL: $GITHUB_URL"
echo ""
echo "Next steps:"
echo "1. Go to Supabase and create project"
echo "2. Run schema.sql in SQL Editor"
echo "3. Get API keys"
echo "4. Deploy on Vercel"
