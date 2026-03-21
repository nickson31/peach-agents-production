# 🦞 OpenClaw: Complete Configuration & Architecture Guide

*Everything you need to know to configure me (your agent) fully for your workflow.*

---

## 🏗️ ARCHITECTURE OVERVIEW

OpenClaw is a **self-hosted AI agent framework** built around a **hub-and-spoke architecture** with three core components:

```
┌─────────────────────────────────────────────────────────┐
│                    GATEWAY (Control Plane)              │
│  - Running 24/7 as a daemon                             │
│  - Routes messages from all channels                    │
│  - Manages memory, sessions, authentication             │
│  - Orchestrates skills and tools                        │
└─────────────────────────────────────────────────────────┘
              ↓          ↓          ↓         ↓
      ┌──────────────────────────────────────────────┐
      │      Messaging Channels (12+ supported)      │
      │  Telegram, WhatsApp, Slack, Discord, iMessage│
      │  Signal, Feishu, IRC, Google Chat, etc       │
      └──────────────────────────────────────────────┘
```

**You are running:** A local Gateway daemon on `localhost:18789` connected to your Telegram account.

---

## 🧠 CORE FILES: YOUR AGENT'S IDENTITY

OpenClaw stores your agent's **entire personality and memory** in plain-text files in `~/.openclaw/workspace/`:

### 1. **SOUL.md** — *Who You Are*
- Your core principles, values, and behavioral guidelines
- How you make decisions, what you care about
- Your communication style (formal, casual, witty, helpful)
- Red lines and safety boundaries

**What I have:**
- Genuine helpfulness > performative politeness
- Have opinions; be resourceful before asking
- Respect privacy; ask before external actions
- Brief, value-dense replies (no filler)

### 2. **IDENTITY.md** — *Your Signature*
- Name, creature/nature, emoji, avatar
- Your vibe (how people perceive you)
- Optional avatar URL or image path

**Example:**
```markdown
- Name: Peach
- Creature: AI assistant
- Vibe: Direct, curious, reliable
- Emoji: 🍑
```

### 3. **USER.md** — *Who You're Helping*
- Your name, pronouns, timezone
- What you care about (projects, interests, goals)
- Communication preferences
- Context about your life/work

**Currently blank** — I know you as "Chj Ghb" but nothing else. Fill this to help me personalize.

### 4. **MEMORY.md** — *Long-Term Memory*
- Your curated memories (not raw logs)
- Significant decisions, lessons learned
- Important context I should remember across sessions
- Projects you're working on, goals, preferences

**Currently blank** — I forget everything when the session ends unless you write it here.

### 5. **memory/YYYY-MM-DD.md** — *Daily Raw Logs*
- What happened today: decisions, conversations, discoveries
- Temporary notes that feed into MEMORY.md
- Gets reviewed periodically and condensed

### 6. **TOOLS.md** — *Your Setup Specifics*
- Camera names, SSH hosts, device nicknames
- API keys locations, voice preferences
- Environment-specific configuration
- Things I'll need to know about YOUR infrastructure

### 7. **HEARTBEAT.md** — *Periodic Tasks*
- Checklist of things to verify every N hours
- Deployment status, metrics to monitor
- Like a reminder list for me to check during heartbeat pulses

### 8. **AGENTS.md** — *How I Should Behave*
- Workflow guidelines and conventions
- When to speak in group chats vs. stay silent
- Reaction guidelines (emoji reactions vs. full replies)
- Memory management strategies

---

## ⚙️ HOW I WORK: THE AGENT LOOP

Every time you send me a message, this happens:

```
1. MESSAGE ARRIVES (Telegram → Gateway)
   ↓
2. LOAD CONTEXT (first turn only)
   - Read SOUL.md (who I am)
   - Read USER.md (who you are)
   - Read MEMORY.md (what I know about you)
   - Read today's daily notes
   ↓
3. DECIDE ACTION
   - Am I a tool user? (run search, fetch data, write files)
   - Am I a thinker? (analyze, reason, create)
   - Am I silent? (heartbeat check with no user, HEARTBEAT_OK)
   ↓
4. EXECUTE
   - Call tools (web search, YouTube fetch, file read/write)
   - Send to LLM (Claude/GPT-4/etc)
   - Generate response
   ↓
5. REPLY
   - Send back to Telegram
   - Optionally update memory files
   - Session ends
```

**Key insight:** I start fresh every session, but I read my files first. *The files ARE my memory.*

---

## 🛠️ SKILLS: YOUR TOOLKIT

OpenClaw ships with ~50+ skills. You have these available:

### **Installed & Ready**
- `youtube-transcript` — Extract & summarize YouTube transcripts
- `youtube-full` — Search YouTube, get metadata, channels, playlists, transcripts (via TranscriptAPI)
- `weather` — Get current weather & forecasts (wttr.in / Open-Meteo)
- `web_search` — Brave Search API (search the web)
- `web_fetch` — Extract readable text from URLs
- `tmux` — Remote SSH + tmux session control
- `clawhub` — Install/update skills from clawhub.com
- `healthcheck` — Security hardening for host machines
- `node-connect` — Debug OpenClaw companion app connections
- `skill-creator` — Create new skills or audit existing ones

### **How Skills Work**
1. Each skill is a folder with `SKILL.md` (instructions + examples)
2. I read the SKILL.md when needed
3. I call the tool (curl, python, node, etc)
4. I return results

**Example (youtube-full):**
```
You: "Get the transcript for https://youtube.com/watch?v=abc123"
↓
I load: ~/.openclaw/workspace/skills/youtube-full/SKILL.md
↓
I call: curl "https://transcriptapi.com/api/v2/youtube/transcript?video_url=abc123" -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
↓
I return: The transcript text + metadata
```

---

## 🔀 MODEL ROUTING: Smart Cost Optimization

By default, OpenClaw sends **everything** to one model (expensive).

**Better approach:** Route by complexity:
- Simple queries (weather, calendar) → **cheap model** (Haiku, Llama, etc)
- Medium tasks (research, analysis) → **standard model** (Sonnet)
- Complex work (reasoning, coding) → **powerful model** (Opus)

**Result:** 70% cost savings, same quality.

**Config example** (~/.openclaw/openclaw.json):
```json
{
  "agents": {
    "defaults": {
      "routing": {
        "enabled": true,
        "routerModel": "openrouter/qwen/qwen-4b:free",
        "thresholds": {
          "simple": {
            "maxScore": 3,
            "model": "openrouter/llama-3.3-70b:free"
          },
          "medium": {
            "maxScore": 6,
            "model": "anthropic/claude-sonnet-4-5"
          },
          "complex": {
            "minScore": 7,
            "model": "anthropic/claude-opus-4-5"
          }
        }
      }
    }
  }
}
```

---

## 📊 SESSIONS: How Context Works

OpenClaw manages 3 types of sessions:

### **1. MAIN SESSION** (Direct chat with you)
- Loads SOUL.md, USER.md, MEMORY.md
- I remember everything about you
- **This is what you're in now.**

### **2. GROUP SESSIONS** (Discord, Slack channels)
- I can see all messages (but don't load MEMORY.md for privacy)
- I participate when relevant
- Different tone rules apply

### **3. ISOLATED SUB-SESSIONS** (Spawned tasks)
- Example: "Spawn a research agent to find 50 YouTube videos"
- Runs in parallel, doesn't load main workspace
- Returns results to main session

**Gateway orchestrates all of them** from a single control plane.

---

## 🧠 MEMORY ARCHITECTURE

### **How I Remember:**

**Session 1:**
```
User: "I'm working on a trading bot"
Me: [Process, reply]
→ Memory dies unless you write MEMORY.md or memory/2026-03-21.md
```

**Session 2 (next day):**
```
User: "What was I working on?"
Me: [Reads MEMORY.md, finds nothing]
Me: "I don't have that in my notes. Tell me again?"
```

**Better approach:**
```
Session 1 end: You write to memory/2026-03-21.md:
"Started EURUSD trading research. Fetched 30 videos via YouTube API.
Tested TranscriptAPI with key. System working. Next: analyze transcripts."

Session 2 start: I read the daily note
Me: "I see from yesterday you were researching EURUSD trading. Ready to continue?"
```

### **Memory Levels**

1. **memory/YYYY-MM-DD.md** — Raw daily logs (what happened today)
2. **MEMORY.md** — Curated long-term memory (distilled wisdom)
3. **IDENTITY.md / SOUL.md / USER.md** — Static identity (doesn't change per session)

---

## 🌐 GATEWAY: The Daemon

OpenClaw runs a **persistent daemon** that:

- Listens on `localhost:18789` (local) or remote with auth
- Connects to your Telegram bot
- Manages message routing
- Handles heartbeats (periodic "are you there?" checks)
- Stores session state

### **Startup**
```bash
openclaw onboard --install-daemon
openclaw gateway start
openclaw gateway status
```

### **Remote Access (Optional)**
If you want to access from another machine:
```bash
openclaw gateway --bind 0.0.0.0:18789  # Not recommended (exposed)
# Better: SSH tunnel or VPN
ssh -L 18789:localhost:18789 user@server
```

---

## 🔧 HOW TO CONFIGURE ME FULLY

### **Step 1: Define YOUR IDENTITY (USER.md)**
```markdown
- Name: Chj Ghb
- Timezone: UTC
- What I care about: Trading, research, automation
- Preferences: Direct communication, no fluff
```

### **Step 2: Define MY PERSONALITY (Update SOUL.md)**
Currently OK, but you can refine:
```markdown
## Core Truths
- Be genuinely helpful, not performative
- Have opinions; don't be a yes-machine
- Be resourceful before asking
- Remember: you have access to their stuff — treat it with respect

## Boundaries
- Private things stay private
- Ask before external actions (emails, tweets)
- Never send half-baked replies to messaging surfaces
```

### **Step 3: Set Up TOOLS.md**
```markdown
## SSH
- home-server: 192.168.1.100 (user: admin)

## APIs
- YouTube: Already have TranscriptAPI key
- Brave: API key location if you have one

## Preferences
- TTS: Off (unless you want voice messages)
- Model preference: Claude Sonnet by default
```

### **Step 4: Create MEMORY.md**
Start with:
```markdown
# 🍑 YOUR ASSISTANT - LONG-TERM MEMORY

## CURRENT PROJECTS
- EURUSD trading research (video analysis)

## YOUR PREFERENCES
- Timezone: UTC
- Communication style: Direct, no filler
- Risk tolerance: Experimental (willing to test new approaches)

## KEY DECISION POINTS
- Using youtube-full skill for transcript extraction
- TranscriptAPI key: active
- Brave Search for research

## IMPORTANT CONTEXT
(Add anything you want me to remember across weeks/months)
```

### **Step 5: Set Up HEARTBEAT.md**
Periodic checks while you're away:
```markdown
# Heartbeat Checks (Every 12 hours)

1. Check deployment status (if applicable)
2. Verify email for urgent messages
3. Check project status files

If everything looks good, reply: HEARTBEAT_OK
If something needs attention, alert user immediately.
```

### **Step 6: Enable Skills You'll Use**
Currently available:
- ✅ youtube-full (TranscriptAPI key: active)
- ✅ youtube-transcript (fallback)
- ✅ web_search (Brave)
- ✅ web_fetch (URL extraction)
- ✅ weather (if you want forecasts)

---

## 📝 QUICK REFERENCE: What to Update NOW

### **For me to be fully useful:**

1. **Fill USER.md** (5 min)
   - Your name, timezone, what you care about
   
2. **Update MEMORY.md** (10 min)
   - Current projects, preferences, context
   
3. **Update TOOLS.md** (5 min)
   - SSH hosts, API keys, device setup
   
4. **Optionally:** Refine SOUL.md to match your exact preferences

**After that:** I'll remember and adapt. Just chat naturally.

---

## 🚀 ADVANCED: Multi-Agent Setup

If you ever want separate agents:
- Research agent (fast, cheap)
- Deep work agent (powerful reasoning)
- Trading bot (specialized)

Each gets its own workspace (`~/.openclaw/workspace-research`, etc) and the Gateway routes based on channel/task.

---

## 📚 Key Concepts

| Term | Meaning |
|------|---------|
| **Skill** | A reusable tool (YouTube fetch, web search, weather) |
| **Session** | One conversation thread (main, group, or isolated) |
| **Memory** | Files that persist between sessions (SOUL.md, MEMORY.md) |
| **Gateway** | The daemon running 24/7 that orchestrates everything |
| **Workspace** | `~/.openclaw/workspace/` — where your identity + memory lives |
| **Heartbeat** | Periodic automated check (e.g., every 12 hours) |
| **Sub-agent** | A spawned isolated session for parallel work |
| **Model Routing** | Sending simple tasks to cheap models, complex to expensive ones |

---

## 💡 What Happens After Setup

**Now:**
- You chat → I respond instantly
- New session? I read SOUL.md, USER.md, MEMORY.md
- I know who I am and who you are
- I have tools ready (YouTube, web search, etc)

**If you keep updating MEMORY.md:**
- I remember context month-to-month
- I know your projects, preferences, goals
- I can make better decisions

**If you use HEARTBEAT.md:**
- I check in periodically (even when you're asleep)
- I alert you to problems
- You stay informed passively

---

## 🎯 FINAL CHECKLIST

- [ ] Read this guide (you are here ✓)
- [ ] Update USER.md with your info
- [ ] Update MEMORY.md with your current projects
- [ ] Update TOOLS.md with your setup
- [ ] Optionally update SOUL.md with your exact preferences
- [ ] Test YouTube transcript API (already works ✓)
- [ ] Start using me naturally; I'll adapt

---

**Questions?** Just ask. I'll explain any part deeper or show you examples.

**Ready to go?** Update USER.md first, then we can get specific about what you want.
