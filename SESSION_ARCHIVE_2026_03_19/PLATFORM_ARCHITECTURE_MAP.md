# RACHA V0 PLATFORM - TECHNICAL ARCHITECTURE MAP

## PHASE 0: UNDERSTAND THE PLATFORM STRUCTURE

```
┌─────────────────────────────────────────────────────────────┐
│              RACHA V0 TRADING PLATFORM                      │
└─────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────┐
    │         USER INTERFACE                               │
    │                                                      │
    │  ┌──────────────────┐  ┌──────────────────────┐    │
    │  │  Chat Page       │  │ Trading Page         │    │
    │  │                  │  │                      │    │
    │  │ - Messages       │  │ ┌────────────────┐  │    │
    │  │ - Notifications  │  │ │ Research Agent │  │    │
    │  │ - History        │  │ └────────────────┘  │    │
    │  │                  │  │ ┌────────────────┐  │    │
    │  │                  │  │ │ Agent          │  │    │
    │  │                  │  │ │ (Configure Bot)│  │    │
    │  │                  │  │ └────────────────┘  │    │
    │  └──────────────────┘  └──────────────────────┘    │
    │                                                      │
    └──────────────────────────────────────────────────────┘
    
    ┌──────────────────────────────────────────────────────┐
    │         BACKEND AGENTS                               │
    │                                                      │
    │  ┌────────────────────┐    ┌────────────────────┐   │
    │  │ RESEARCH AGENT     │    │ AGENT (Bot Config) │   │
    │  │                    │    │                    │   │
    │  │ - YouTube API      │    │ - User Config      │   │
    │  │ - Transcript parse │    │ - Symbol selection │   │
    │  │ - Signal extract   │    │ - Entry/exit setup │   │
    │  │ - Creator tier     │    │ - Deployment      │   │
    │  │ - Problem learning │    │ - Monitoring      │   │
    │  └────────────────────┘    │ - Results         │   │
    │                            └────────────────────┘   │
    │                                                      │
    └──────────────────────────────────────────────────────┘
    
    ┌──────────────────────────────────────────────────────┐
    │         EXECUTION LAYER                              │
    │                                                      │
    │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │
    │  │ Batch    │ │ Wave     │ │ Auto-    │ │Monitor │ │
    │  │ Deploy   │ │ Deploy   │ │ Profit   │ │Real-   │ │
    │  │          │ │          │ │ System   │ │ time   │ │
    │  └──────────┘ └──────────┘ └──────────┘ └────────┘ │
    │       ↓            ↓             ↓           ↓       │
    │  ┌────────────────────────────────────────────────┐ │
    │  │         ALPACA PAPER TRADING API              │ │
    │  │  (Real account, paper orders, live data)      │ │
    │  └────────────────────────────────────────────────┘ │
    │                                                      │
    └──────────────────────────────────────────────────────┘
    
    ┌──────────────────────────────────────────────────────┐
    │         DATA STORAGE & STATE                         │
    │                                                      │
    │  ┌────────────┐ ┌────────────┐ ┌──────────────┐    │
    │  │ Bot Config │ │ Deployments│ │ Creator Lib  │    │
    │  │ (per user) │ │ (history)  │ │ (metadata)   │    │
    │  └────────────┘ └────────────┘ └──────────────┘    │
    │                                                      │
    │  ┌─────────────────────────────────────────────┐    │
    │  │ Real-time Monitoring State (Redis/WebSocket)   │
    │  │ - Current orders                               │
    │  │ - Fills                                         │
    │  │ - P&L                                           │
    │  └─────────────────────────────────────────────┘    │
    │                                                      │
    └──────────────────────────────────────────────────────┘
```

---

## HOW RESEARCH AGENT WORKS

```
USER INPUT (Trading Page → Research Panel):
  "Analyze ForexMentor YouTube channel for trading signals"
  
    ↓
    
RESEARCH AGENT EXECUTES:

1. SEARCH PHASE
   ├─ Query YouTube API: "ForexMentor recent trading videos"
   ├─ Filter: Last 30 days, trading strategy content
   └─ Result: [Video 1, Video 2, Video 3, ...]

2. EXTRACT PHASE
   ├─ For each video:
   │  ├─ Get transcript (TranscriptAPI)
   │  ├─ Parse for: "buy at", "entry", "target", "stop"
   │  ├─ Extract: Symbols ($ETHE, $GBTC), prices, timeframes
   │  └─ Assign confidence score (0-100)
   
3. VALIDATE PHASE
   ├─ Check symbol in Alpaca (13,472 available)
   ├─ Normalize prices (decimal places, currency)
   ├─ Group duplicates from other sources
   └─ Tier creator (Tier 1/2/3)

4. OUTPUT TO USER (Research Panel)
   ├─ Creator profile: Name, tier, success rate
   ├─ Signals: [Signal 1, Signal 2, ...]
   │  ├─ Symbol
   │  ├─ Entry price
   │  ├─ Exit price
   │  ├─ Confidence
   │  └─ Timeframe
   ├─ Recommendation: "95% confidence, allocate 40%"
   └─ YouTube learnings: "3 videos confirm this pattern"

RESULT: User sees curated, validated signals ready for bot config
```

---

## HOW AGENT (BOT CONFIG) WORKS

```
USER INPUT (Trading Page → Agent Panel):
  "Create bot: ForexMentor signals, ETHE 50%, GBTC 40%, 4-hour holds"
  
    ↓
    
AGENT PROCESSES CONFIG:

1. PARSE USER CONFIG
   ├─ Creator: ForexMentor (Tier 1, 95% score)
   ├─ Symbols: ETHE (50%), GBTC (40%), FXA (10%)
   ├─ Entry: -0.02 stagger (default for crypto)
   ├─ Exit: +3% take profit, -1% stop loss
   ├─ Time: 4+ hour holds (day trading)
   ├─ Deployment: Wave-based (90 sec intervals)
   └─ Batch size: 100 orders

2. VALIDATE AGAINST LEARNINGS
   ├─ Check: "ETHE 93% fill rate? YES ✅"
   ├─ Check: "GBTC 90% fill rate? YES ✅"
   ├─ Check: "Avoid FXB? YES (0% fills) ✅"
   ├─ Check: "Entry stagger correct? YES ✅"
   └─ Result: "Config validated, ready to deploy"

3. PREPARE DEPLOYMENT
   ├─ Generate 100 orders with:
   │  ├─ Symbol allocation (ETHE 50 orders, GBTC 40, FXA 10)
   │  ├─ Entry prices (calculated with stagger)
   │  ├─ Exit prices (+3%, -1%)
   │  └─ Metadata (creator, signal ID, confidence)
   
4. READY FOR DEPLOY BUTTON
   ├─ Summary shown to user:
   │  ├─ "Deploy 100 orders"
   │  ├─ "Capital: $120K"
   │  ├─ "Expected fill rate: 85%"
   │  ├─ "ROI target: +3-5%"
   │  └─ "Duration: 4 hours"
   ├─ User clicks: "DEPLOY"
   
    ↓
    
5. EXECUTION PHASE (Backend)
   ├─ Wave 1: Deploy 10 orders
   ├─ Wait 90 seconds
   ├─ Wave 2: Deploy 10 orders (adapted based on Wave 1)
   ├─ ... continue 8 more waves ...
   ├─ Real-time feedback on fills
   └─ Auto-profit system monitoring

RESULT: Orders deployed, monitored, profits taken, next batch optimized
```

---

## DATA FLOW: Chat Page to Trading Page

```
CHAT PAGE (General Interface):
  ├─ User asks: "Show me trading insights"
  ├─ User uploads: YouTube video link
  └─ User says: "Create bot for this creator"
    
    ↓ Message to backend
    
BACKEND ROUTER:
  ├─ Parse intent from natural language
  ├─ Determine: Research task? Agent task? Chat history?
  └─ Route to appropriate agent
    
    ↓
    
RESEARCH AGENT (if "show insights"):
  ├─ Extract signals from message/video
  ├─ Return: Curated data to chat
  └─ User sees: Results in chat + link to Trading page
    
OR
    
AGENT (if "create bot"):
  ├─ Take config from chat natural language
  ├─ Pre-fill Trading page with config
  └─ User sees: Full bot setup ready in Trading page
    
    ↓
    
TRADING PAGE DISPLAYS:
  ├─ Research Panel: Signals
  └─ Agent Panel: Bot configuration
    
    ↓ (User clicks DEPLOY)
    
EXECUTION LAYER:
  ├─ Alpaca API calls
  ├─ Wave-based deployment
  ├─ Real-time monitoring
  └─ Results streamed back to UI
    
    ↓
    
CHAT PAGE NOTIFIED:
  ├─ "Bot deployed: 100 orders"
  ├─ "Fill rate: 85%"
  ├─ "P&L: +4.2%"
  └─ Link to detailed results
```

---

## WHAT EACH COMPONENT DOES

### RESEARCH AGENT Component (Backend)

**Input**: Creator name, YouTube link, or natural language query
**Process**:
  - YouTube API search
  - TranscriptAPI extraction
  - NLP parsing (identify trades, prices, symbols)
  - Alpaca symbol validation
  - Creator tier assignment
  - Confidence scoring (0-100)

**Output**: Structured signals array
```json
{
  "creator": "ForexMentor",
  "tier": 1,
  "confidence": 95,
  "signals": [
    {
      "symbol": "ETHE",
      "entry": 3450.00,
      "exit": 3555.00,
      "stagger": -0.02,
      "timeframe": "4h",
      "source_video": "https://youtube.com/...",
      "confidence": 97
    }
  ],
  "recommendation": "Allocate 40% to this creator"
}
```

### AGENT Component (Backend)

**Input**: User config (creator, symbols, amounts, entry/exit, deployment mode)
**Process**:
  - Parse config from natural language or UI form
  - Validate against historical learnings
  - Generate batch orders
  - Calculate allocations
  - Prepare wave schedule

**Output**: Deployment plan ready for execution
```json
{
  "batch_id": "batch_5_20260319",
  "config": {
    "creators": ["ForexMentor"],
    "symbols": ["ETHE", "GBTC", "FXA"],
    "allocation": {"ETHE": 0.5, "GBTC": 0.4, "FXA": 0.1}
  },
  "deployment": {
    "mode": "wave-based",
    "waves": 10,
    "orders_per_wave": 10,
    "wave_interval": 90,
    "total_orders": 100
  },
  "orders": [
    {
      "symbol": "ETHE",
      "qty": 12,
      "entry": 3449.98,
      "exit": 3555.00,
      "stop_loss": 3416.50
    }
  ]
}
```

### Wave Deployment Component

**Input**: Batch deployment plan
**Process**: 
  - Deploy Wave 1 (10 orders)
  - Wait 90 seconds
  - Analyze Wave 1 fills
  - Adapt Wave 2 allocation
  - Deploy Wave 2
  - ... repeat 8 more times ...

**Output**: Real-time monitoring stream (WebSocket)
```json
{
  "wave": 1,
  "status": "completed",
  "deployed": 10,
  "filled": 9,
  "fill_rate": 90,
  "timestamp": "2026-03-19T15:13:00Z",
  "next_wave_allocation": {"ETHE": 8, "GBTC": 4, "FXA": 1}
}
```

### Auto-Profit System

**Input**: Real-time position data from Alpaca
**Process**:
  - Monitor every filled order
  - Check if +3% profit reached → Auto-sell
  - Check if -1% loss reached → Auto-exit
  - Reinvest proceeds

**Output**: P&L updates, closed positions log

### Monitoring Component

**Input**: All live orders
**Process**:
  - Query Alpaca every 5 seconds
  - Track fills, prices, P&L
  - Detect problems
  - Stream to UI real-time

**Output**: Live dashboard data
```json
{
  "account": {
    "equity": 104230.50,
    "cash": 45918.24,
    "profit": 4230.50
  },
  "positions": {
    "ETHE": {"qty": 1838, "value": 31705.50},
    "GBTC": {"qty": 150, "value": 8109.00}
  },
  "orders": {
    "filled": 181,
    "pending": 36,
    "total": 417
  }
}
```

---

## LEARNING LOOP INTEGRATION

```
After each batch deploys:

1. COLLECT RESULTS
   ├─ All fills, prices, P&L
   ├─ By symbol, by creator, by timeframe
   └─ Store in database

2. IDENTIFY PROBLEMS (Automatic)
   ├─ Low fill rate on symbol X?
   ├─ Format errors on symbol Y?
   ├─ API throttling?
   └─ Group into categories

3. YOUTUBE LEARNING (Optional, user-triggered)
   ├─ Generate 25-40 searches per problem
   ├─ Suggest videos to user
   ├─ User can review or skip

4. EXTRACT INSIGHTS
   ├─ "ETHE 93% fill rate → allocate more"
   ├─ "FXB 0% fill rate → eliminate"
   ├─ "FXA needs wider stagger → try -0.05"
   └─ Store in "learnings" database

5. APPLY TO NEXT BATCH
   ├─ When user creates new bot:
   │  ├─ Check learnings database
   │  ├─ Pre-populate config with best practices
   │  ├─ Suggest allocations based on history
   │  └─ Warn about known problems
   └─ "Based on 417 orders: ETHE recommended 50%, FXB disabled"
```

---

## STATE MANAGEMENT (Real-time)

```
SHARED STATE (Real-time sync across Chat + Trading):

1. User State
   ├─ Current creator selection
   ├─ Active bot configs
   ├─ Deployment history
   └─ P&L tracking

2. Bot State (Per bot)
   ├─ Current status (idle, deploying, monitoring, closed)
   ├─ Current batch ID
   ├─ Active orders (by wave)
   ├─ Real-time metrics
   └─ Last update timestamp

3. Creator State
   ├─ Library of creators (21 researched)
   ├─ Performance history
   ├─ Tier and scores
   ├─ YouTube videos analyzed
   └─ Signals extracted

4. Learnings State
   ├─ Symbol performance
   ├─ Problem history
   ├─ YouTube research conducted
   ├─ Optimization suggestions
   └─ Best practices learned

UPDATE MECHANISM: WebSocket (real-time) + REST API (backup)
  ├─ Chat page listens: For notifications
  ├─ Trading page listens: For monitoring updates
  ├─ Both: Can trigger state changes
  └─ Sync: Automatic across both pages
```

---

## API ENDPOINTS (Backend)

### Research Agent
```
POST /api/research/analyze-creator
  Input: { creator: "ForexMentor", videos: 5 }
  Output: Signals, tier, confidence
  
POST /api/research/parse-youtube-link
  Input: { url: "https://youtube.com/..." }
  Output: Extracted signals
  
POST /api/research/natural-language
  Input: { query: "Find trading signals for crypto" }
  Output: Curated signals + creator recommendations
```

### Agent (Bot Config)
```
POST /api/agent/validate-config
  Input: Bot configuration
  Output: Validation result + warnings
  
POST /api/agent/generate-orders
  Input: Validated config
  Output: Order list ready for deployment
  
POST /api/agent/deploy-batch
  Input: Order list
  Output: Batch ID + starts deployment
  
GET /api/agent/deployment-status/:batch_id
  Output: Real-time wave progress
  
POST /api/agent/stop-deployment/:batch_id
  Output: Stops and cancels pending
```

### Monitoring
```
GET /api/monitor/live-data
  Output: Real-time account metrics (WebSocket)
  
GET /api/monitor/batch-history
  Output: All past deployments
  
POST /api/monitor/get-learnings
  Output: Performance insights for next batch
```

---

## FOLDER STRUCTURE (What we'll create)

```
/racha-v0-platform/
├── /backend/
│   ├── /agents/
│   │   ├── /research-agent/
│   │   │   ├── youtube-search.py
│   │   │   ├── transcript-parser.py
│   │   │   ├── signal-extractor.py
│   │   │   ├── alpaca-validator.py
│   │   │   └── creator-tier.py
│   │   ├── /agent-bot-config/
│   │   │   ├── config-parser.py
│   │   │   ├── order-generator.py
│   │   │   ├── deployment-planner.py
│   │   │   └── validate-against-learnings.py
│   │   └── /shared/
│   │       ├── creator-library.py
│   │       ├── learnings-db.py
│   │       └── problem-detector.py
│   ├── /execution/
│   │   ├── wave-deployment.py
│   │   ├── auto-profit-system.py
│   │   ├── monitoring.py
│   │   └── real-time-streamer.py
│   ├── /api/
│   │   ├── research-routes.py
│   │   ├── agent-routes.py
│   │   ├── monitor-routes.py
│   │   └── websocket-handler.py
│   └── /db/
│       ├── creator-profiles.json
│       ├── deployment-history.json
│       ├── learnings.json
│       └── user-configs.json
├── /frontend/
│   ├── /pages/
│   │   ├── /chat-page/
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── MessageList.tsx
│   │   │   ├── InputBox.tsx
│   │   │   └── NotificationCenter.tsx
│   │   ├── /trading-page/
│   │   │   ├── TradingDashboard.tsx
│   │   │   ├── research-panel/
│   │   │   │   ├── ResearchPanel.tsx
│   │   │   │   ├── CreatorSearch.tsx
│   │   │   │   ├── SignalsList.tsx
│   │   │   │   └── RecommendationCard.tsx
│   │   │   ├── agent-panel/
│   │   │   │   ├── AgentPanel.tsx
│   │   │   │   ├── BotConfigForm.tsx
│   │   │   │   ├── DeploymentPreview.tsx
│   │   │   │   └── DeployButton.tsx
│   │   │   ├── monitoring-panel/
│   │   │   │   ├── LiveDashboard.tsx
│   │   │   │   ├── OrdersTable.tsx
│   │   │   │   ├── P&LChart.tsx
│   │   │   │   └── RealTimeMetrics.tsx
│   │   │   └── history-panel/
│   │   │       ├── DeploymentHistory.tsx
│   │   │       ├── PerformanceAnalysis.tsx
│   │   │       └── LearningsInsights.tsx
│   ├── /components/
│   │   ├── common/
│   │   ├── charts/
│   │   └── forms/
│   └── /state/
│       ├── userState.ts
│       ├── botState.ts
│       ├── creatorState.ts
│       └── learningsState.ts
└── /shared/
    ├── types.ts
    ├── constants.ts
    ├── utilities.ts
    └── alpaca-sdk-wrapper.ts
```

This is the technical blueprint mapping.
