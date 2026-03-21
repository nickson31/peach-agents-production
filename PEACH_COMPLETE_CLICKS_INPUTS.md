# 🍑 PEACH: COMPLETE CLICKS & INPUTS SPECIFICATION
## Every Button, Every Field, Every Interaction

**Date**: 2026-03-21  
**Scope**: 100% exhaustive mapping of all clicks and inputs across 10 pages  
**Total**: ~150+ clicks, ~80+ inputs identified with exact behavior

---

## PAGE 1: DASHBOARD (HOME)

### HEADER (Top Navigation Bar)
```
┌─────────────────────────────────────────────────┐
│ [LOGO] PEACH | [Nav] Settings Logout            │
└─────────────────────────────────────────────────┘
```

**Clicks:**
1. **Logo click** → Refresh page / Return to dashboard
   - Action: Navigate to `/dashboard`
   - State: Clears all filters, resets to default view
   - Behavior: Smooth scroll to top

2. **"Settings" link** → Open settings page
   - Action: Navigate to `/settings`
   - State: Preserve current portfolio state
   - Behavior: Opens in same tab

3. **"Logout" link** → Sign out
   - Action: Clear session token
   - Navigate to `/login`
   - Behavior: Show confirmation before logout
   - Recovery: Can go back if clicked by accident

---

### ACCOUNT OVERVIEW SECTION

```
📊 ACCOUNT OVERVIEW
├─ Equity: $100,000 [+$8,200 this month]
├─ Daily P&L: +$1,200 (+1.2%) ↑ [Green]
├─ Monthly Return: +8.2% [vs S&P 6%]
├─ Buying Power: $158,000
└─ [Deposit] [Withdraw]
```

**Inputs/Clicks:**

4. **"Equity" display** (read-only)
   - Type: Display (not editable)
   - Value: Real-time from Alpaca API
   - Update frequency: Every 30 seconds
   - Format: USD with 2 decimals
   - Color logic: Green if >0, red if <0

5. **"[+$8,200 this month]" badge** (clickable)
   - Action: Opens profit breakdown modal
   - Shows: Gross profit, fees, commissions
   - Modal has close button (X) in top right
   - Can also close by clicking outside modal

6. **"Daily P&L" display**
   - Type: Real-time metric
   - Value: (Today's closes - Today's opens) + Unrealized
   - Color: Green if positive, red if negative
   - Arrow: ↑ if gain, ↓ if loss
   - Updates: Every 5 seconds

7. **"Monthly Return" percentage**
   - Type: Calculate vs S&P 500
   - Comparison: Shows vs benchmark
   - Clickable: Shows breakdown of returns by strategy
   - Modal shows: RSI, Copy trading, Arbitrage splits

8. **"Buying Power" number**
   - Type: Real-time from broker
   - Source: Alpaca `GET /v2/account`
   - Updates: Every 10 seconds
   - Tooltip on hover: "Cash available to buy more"

9. **[Deposit] button**
   - Type: Primary button (blue)
   - Action: Opens deposit flow
   - Steps: 
     - Select amount
     - Select method (ACH, wire, etc.)
     - Confirm
   - Behavior: Window or modal, 50/50
   - Success: "Deposit initiated, arrives in 1-3 days"

10. **[Withdraw] button**
    - Type: Secondary button (outline)
    - Action: Opens withdrawal flow
    - Steps:
      - Select amount (max = available cash)
      - Select destination (linked bank)
      - Confirm
    - Behavior: Requires 2FA verification
    - Success: "Withdrawal pending, 3-5 business days"

---

### BOT STATUS SECTION

```
🤖 BOT STATUS
├─ Status: [RUNNING] (paper trading)
├─ Last trade: 2m ago (BUY ETHE)
├─ Win rate: 72% (18/25 trades)
├─ Avg win: $850 | Avg loss: -$350
└─ [Pause] [Resume] [EMERGENCY STOP]
```

**Clicks/Inputs:**

11. **"Status: [RUNNING]" indicator**
    - Type: Display + clickable
    - Click action: Shows bot details modal
    - Modal includes:
      - Bot name
      - Start time
      - Current strategy
      - Active positions count
      - Last action taken (timestamp)
    - Close: X button or click outside

12. **"(paper trading)" text**
    - Type: Badge/label indicating demo mode
    - Clickable: Shows explanation of paper trading
    - Info displayed: "Trades don't require real money, but results are real"

13. **"Last trade: 2m ago (BUY ETHE)"** link
    - Type: Clickable text
    - Action: Navigate to Trade History page
    - Pre-filter: Show only this trade
    - Scroll: Auto-scroll to this trade in list

14. **"Win rate: 72% (18/25 trades)"** display
    - Type: Metric display, clickable
    - Action: Opens analytics modal
    - Shows:
      - Win distribution (by asset)
      - Win distribution (by strategy)
      - Win distribution (by time)
      - Breakdown of wins

15. **"Avg win: $850"** display
    - Type: Clickable metric
    - Action: Shows all winning trades
    - Filter: Only trades with P&L > 0
    - Sort: By size (descending)

16. **"Avg loss: -$350"** display
    - Type: Clickable metric
    - Action: Shows all losing trades
    - Filter: Only trades with P&L < 0
    - Sort: By size (ascending, most negative first)

17. **[Pause] button**
    - Type: Secondary button (yellow/warning color)
    - Action: Pause bot (stop generating new signals)
    - Behavior: Existing positions stay open
    - Confirmation: "Are you sure? Positions stay open."
    - State change: Button becomes [Resume]
    - Tooltip: "Bot will not generate new trades, but will not close existing ones"

18. **[Resume] button**
    - Type: Primary button (blue)
    - Appears after pause
    - Action: Resume bot signal generation
    - Confirmation: None (quick action)
    - State change: Button becomes [Pause]

19. **[EMERGENCY STOP] button**
    - Type: Danger button (red)
    - Action: CLOSES ALL POSITIONS IMMEDIATELY
    - Behavior: Does not wait for confirms
    - Speed: <2 seconds execution
    - Confirmation: "EMERGENCY STOP - Close all positions now?"
    - Post-action: 
      - All positions closed
      - Bot status becomes [STOPPED]
      - Cannot resume without manual action
    - Tooltip: "Use only in emergency. Closes all open trades immediately."

---

### ACTIVE POSITIONS SECTION

```
📈 ACTIVE POSITIONS (3)
├─ [+] ETHE: 0.5 @ $2,400 (R:R 1:2)
│   └─ Unrealized: +$250 [Status: Winning]
├─ [+] BTC: 0.1 @ $65,000 (SL: $63K)
│   └─ Unrealized: +$800 [Status: Winning]
├─ [-] Polymarket: "Trump" at 60% odds
│   └─ Unrealized: -$100 [Status: Losing]
└─ [CLOSE ALL] [REBALANCE]
```

**Clicks/Inputs:**

20. **Position row (expand/collapse toggle)**
    - Type: Clickable row
    - Action: Expand to show full details
    - Details include:
      - Entry price & date
      - Current price (real-time)
      - Target price
      - Stop loss
      - Time held
      - Confidence
      - Reason for trade (AI analysis)
    - Behavior: Smooth expand animation

21. **"[+]" symbol (long indicator)**
    - Type: Visual indicator (non-clickable)
    - Meaning: Long position (bullish)
    - Color: Green background

22. **"[-]" symbol (short indicator)**
    - Type: Visual indicator (non-clickable)
    - Meaning: Short position or bearish bet
    - Color: Red background

23. **Asset name (ETHE, BTC, etc.)** - Clickable
    - Type: Link
    - Action: Opens detailed position page
    - Page shows:
      - Full trade details
      - Chart of asset
      - News related to asset
      - Trading history for this asset

24. **Position size "0.5 @ $2,400"**
    - Type: Display (text)
    - Shows: quantity @ entry price
    - Clickable: Opens entry confirmation details

25. **"(R:R 1:2)" ratio** - Clickable
    - Type: Risk/Reward indicator
    - Click: Explains what R:R means
    - Shows: 
      - Potential profit ($2,000)
      - Potential loss ($1,000)
      - Expected value calculation

26. **"Unrealized: +$250"** - Clickable
    - Type: Current P&L metric
    - Action: Shows breakdown
      - Entry → Current
      - High → Low during hold
      - Fees paid
    - Real-time updates

27. **"[Status: Winning]" badge**
    - Type: Status indicator
    - Color: Green
    - Clickable: Shows why (probability of hit)

28. **[CLOSE ALL] button**
    - Type: Secondary button
    - Action: Close all positions at market price
    - Confirmation: "Close all positions? This cannot be undone."
    - Execution: ~5-10 seconds
    - Result: All positions closed, new trade window opens
    - Note: Different from EMERGENCY STOP (slower, more control)

29. **[REBALANCE] button**
    - Type: Secondary button
    - Action: Opens rebalancing modal
    - Modal includes:
      - Current allocation %
      - Target allocation %
      - Suggested rebalance trades
      - Execute button
    - Behavior: Can adjust target% before saving

---

### TODAY'S TRADES SECTION

```
💰 TODAY'S TRADES (4)
├─ 09:30 [✅] Sold GBTC (+$280)
├─ 10:15 [⏳] Buy ETHE (PENDING YOUR OK)
│        └─ [APPROVE] [REJECT]
├─ 11:20 [❌] Arbitrage (REJECTED by you)
└─ 14:45 [PROPOSED] BUY SOL @ $185
         └─ Confidence: 68%
```

**Clicks/Inputs:**

30. **Trade row (any status)**
    - Type: Clickable row
    - Action: Expands to full trade details
    - Shows: Entry, target, stop loss, reason, etc.

31. **"09:30" timestamp**
    - Type: Clickable text
    - Action: Filters Trade History to this time period
    - Also shows: How long ago (2m, 1h, etc.)

32. **"[✅]" completed status**
    - Type: Visual indicator
    - Color: Green checkmark
    - Means: Trade filled and closed
    - Clickable: Shows execution details

33. **"[⏳]" pending status**
    - Type: Visual indicator
    - Color: Yellow/orange hourglass
    - Means: Waiting for user approval
    - Clickable: Jumps to Trade Approval page

34. **"[❌]" rejected status**
    - Type: Visual indicator
    - Color: Red X
    - Means: User rejected this trade
    - Clickable: Shows rejection reason

35. **"[PROPOSED]" status badge**
    - Type: Visual indicator
    - Color: Blue
    - Means: AI just proposed this
    - Time indicator: "30 seconds to decide"
    - Clickable: Goes to Trade Approval

36. **"Sold GBTC (+$280)" text**
    - Type: Clickable link
    - Action: Show full trade card
    - Card includes:
      - Entry price & time
      - Exit price & time
      - P&L calculation
      - Commission
      - Net profit

37. **"PENDING YOUR OK" - urgent indicator**
    - Type: Text alert
    - Color: Highlighted (orange/red)
    - Blink: May blink to draw attention
    - Click: Goes to Trade Approval page

38. **[APPROVE] button (in inline row)**
    - Type: Primary button (small)
    - Action: Approve this specific trade
    - Shortcut: Can also use keyboard shortcut (e.g., "A")
    - Confirmation: None (quick)
    - Next: Execution happens immediately

39. **[REJECT] button (in inline row)**
    - Type: Secondary/danger button (small)
    - Action: Reject this specific trade
    - Confirmation: "Reject this trade?"
    - Effect: Trade is skipped, bot moves to next signal
    - Note: User can see it and change mind later (view rejected)

40. **"REJECTED by you" text**
    - Type: Label (non-clickable)
    - Means: This trade was manually rejected
    - Clickable: Shows why (timestamp, user note maybe)

---

### QUICK ACTIONS SECTION

```
⚡ QUICK ACTIONS
├─ [APPROVE PENDING TRADES]
├─ [VIEW FULL HISTORY]
├─ [TUNE STRATEGY]
└─ [CONTACT SUPPORT]
```

**Clicks:**

41. **[APPROVE PENDING TRADES] button**
    - Type: Primary button
    - Action: Approve all pending trades at once (bulk action)
    - Warning: "This will approve all pending trades. Continue?"
    - Result: 
      - All pending become executing
      - Redirect to trade history showing new trades
    - Risk: User can accidentally approve bad trades
    - Undo: Can manually close if bad

42. **[VIEW FULL HISTORY] button**
    - Type: Secondary button
    - Action: Navigate to Trade History page
    - Behavior: Shows all trades, filterable, sortable

43. **[TUNE STRATEGY] button**
    - Type: Secondary button (maybe highlight/prompt)
    - Action: Navigate to Bot Configuration page
    - Pre-selected: Last used strategy
    - Purpose: Quick access to tune parameters

44. **[CONTACT SUPPORT] button**
    - Type: Secondary button
    - Action: Opens support options:
      - Live chat (if available)
      - Email support form
      - Call Mark (schedule)
      - FAQ
    - Behavior: Modal or new tab, depends on implementation

---

## PAGE 2: TRADE APPROVAL (AI Proposes, You Decide)

### HEADER & TIMER

```
┌──────────────────────────────────────────────┐
│ 🤖 TRADE PROPOSAL (30 sec remaining) ⏱️      │
├──────────────────────────────────────────────┤
```

**Clicks/Inputs:**

45. **"30 sec remaining" timer**
    - Type: Live countdown (read-only display)
    - Behavior: 
      - Updates every 1 second
      - Color changes: Green → Yellow → Red
      - When hits 0: Auto-reject trade
    - Click: No action (display only)
    - Tooltip: "You have 30 seconds to approve or reject"

46. **"⏱️" icon (timer visual)**
    - Type: Animated icon
    - Animation: Spins or shrinks as time runs out
    - Purpose: Visual urgency indicator

---

### TRADE DETAILS

```
BUY 0.5 BTC @ $65,200

ANALYSIS:
├─ Reason: RSI oversold (28) + support hold
├─ Confidence: 78% ↑ [Good]
├─ Pattern: Last 7 similar trades = 4W-1L
└─ Timeframe: Last 4 hours
```

**Clicks/Inputs:**

47. **"BUY" action label**
    - Type: Display (non-clickable)
    - Shows: BUY or SELL
    - Color: Green = BUY, Red = SELL
    - Size: Large font for immediate grab

48. **"0.5 BTC" quantity**
    - Type: Editable input field (maybe)
    - Current: 0.5
    - Can modify: Yes or No (depends on design)
    - Constraints: 
      - Min: 0.01
      - Max: Account buying power / Price
    - Validation: Shows warnings if adjusted

49. **"@ $65,200" price**
    - Type: Current market price (display or editable)
    - Source: Real-time from exchange API
    - Clickable: Shows price history chart (last 1h)
    - Editable: User can set custom price (limit order) or accept current (market order)
    - Button: [MARKET] vs [LIMIT] selector

50. **"Reason: RSI oversold (28) + support hold"**
    - Type: Clickable explanation text
    - Action: Shows detailed analysis
    - Modal includes:
      - RSI explanation
      - Support level chart
      - Why this matters
      - Historical performance of this signal

51. **"Confidence: 78%"** percentage
    - Type: Metric display
    - Color: Green (high confidence)
    - Clickable: Shows breakdown of confidence
      - RSI weight: 40%
      - Pattern matching: 20%
      - Support level: 15%
      - Volume: 15%
      - Other: 10%

52. **"↑" confidence trend**
    - Type: Visual indicator
    - Arrow up = confidence increasing
    - Arrow down = confidence decreasing
    - Means: "This signal is getting stronger"

53. **"[Good]" confidence label**
    - Type: Assessment label
    - Color: Green
    - Possible values: Bad (<40%), Medium (40-70%), Good (70-85%), Excellent (85%+)
    - Clickable: Shows historical accuracy of this confidence level

54. **"Pattern: Last 7 similar trades = 4W-1L"**
    - Type: Historical performance metric
    - Clickable: Shows all 7 similar trades
    - Win rate: 4 wins / 5 total = 80%
    - Helps user decide

55. **"Timeframe: Last 4 hours"**
    - Type: Time period for analysis
    - Clickable: Shows chart zoomed to this timeframe
    - Can change: User might want to see 1h, 1d, 1w option

---

### EXECUTION DETAILS

```
EXECUTION DETAILS:
├─ Entry: $65,200
├─ Target: $67,000 (+2.8%)
├─ Stop Loss: $63,500 (-2.6%)
├─ Position Size: 1% account ($1,000)
├─ Time Limit: Close if not +2% in 24h
└─ Risk/Reward: 1:1.1 (acceptable)
```

**Clicks/Inputs:**

56. **"Entry: $65,200"** - Display
    - Type: Current market or proposed entry
    - Click: Shows entry method (market vs limit)
    - Editable: User can change to custom entry price

57. **"Target: $67,000"** - Editable input
    - Type: Take profit price (input field)
    - Default: $67,000
    - User can change
    - Validation: Must be > entry price
    - Button: [MARKET] / [TRAILING] / [LIMIT] options

58. **"(+2.8%)" profit calculation**
    - Type: Calculated percentage
    - Auto-updates: When user changes target
    - Formula: ((Target - Entry) / Entry) × 100

59. **"Stop Loss: $63,500"** - Editable
    - Type: Input field
    - Default: $63,500
    - User can change
    - Validation: Must be < entry price
    - Warning: If SL too tight, alert

60. **"(-2.6%)" loss calculation**
    - Type: Calculated percentage
    - Auto-updates: When user changes stop
    - Formula: ((Stop - Entry) / Entry) × 100

61. **"Position Size: 1% account ($1,000)"**
    - Type: Display (usually not editable to user)
    - Shows: Percentage and dollar amount
    - Determined by: Bot configuration (risk management)
    - Can override: Depends on settings

62. **"Time Limit: Close if not +2% in 24h"**
    - Type: Trade exit condition
    - Meaning: Automatically close if no 2% gain after 24 hours
    - Editable: User can change time or profit %
    - Options: [1h] [4h] [24h] [1 week] [None - hold indefinitely]

63. **"Risk/Reward: 1:1.1"** metric
    - Type: Display
    - Meaning: For every $1 risked, can make $1.10
    - Click: Shows all trades with this ratio
    - Color: Green if >1.0 (favorable), Red if <1.0

64. **"(acceptable)" assessment**
    - Type: Label
    - Possible values: Poor, Fair, Acceptable, Good, Excellent
    - Click: Explains what makes good R:R

---

### PAST PERFORMANCE

```
PAST PERFORMANCE:
├─ This strategy (RSI oversold): 80% win
├─ This asset (BTC): 72% win
├─ This hour (14:00-15:00): 3W-0L
└─ Recent trend: ↑ Up 3 days straight
```

**Clicks/Inputs:**

65. **"This strategy (RSI oversold): 80% win"**
    - Type: Performance metric, clickable
    - Action: Shows all RSI oversold trades
    - Filter: Only this strategy
    - Stats shown: Win rate, avg duration, avg profit

66. **"This asset (BTC): 72% win"**
    - Type: Asset-specific metric, clickable
    - Action: Shows all BTC trades
    - Stats: Total trades, win rate, avg profit

67. **"This hour (14:00-15:00): 3W-0L"**
    - Type: Time-period specific, clickable
    - Action: Shows all trades in this hour
    - Helps detect: "Good trading hour"

68. **"Recent trend: ↑ Up 3 days straight"**
    - Type: Trend indicator, clickable
    - Arrow: Up/Down/Neutral
    - Action: Shows last 3 days of P&L

---

### ACTION BUTTONS

```
[✅ APPROVE]  [❌ REJECT]  [❓ ASK MARK]

☐ Don't ask again for RSI oversold trades
```

**Clicks/Inputs:**

69. **[✅ APPROVE] button**
    - Type: Primary button (blue, prominent)
    - Action: Execute the trade
    - Behavior: 
      - Submits order to Alpaca
      - Waits for fill confirmation
      - Shows success message
      - Returns to dashboard
    - Keyboard shortcut: Green space bar or "A" key
    - Confirmation: None (immediate)
    - Error handling: Shows alert if order fails

70. **[❌ REJECT] button**
    - Type: Secondary/danger button (red outline)
    - Action: Skip this trade
    - Behavior:
      - Cancels this proposal
      - Bot moves to next signal
      - Shows summary: "Trade rejected. Next signal in 30s."
    - Keyboard shortcut: "R" key
    - Confirmation: None
    - Can undo: User can go to Trade History to see it

71. **[❓ ASK MARK] button**
    - Type: Secondary button (maybe Telegram-like icon)
    - Action: Send question to Mark
    - Behavior:
      - Opens input field: "Your question..."
      - Sends via Telegram/email
      - Mark can respond
      - User sees response in app
    - Time: Response not immediate (Mark might be sleeping)
    - Alternative: Could open live chat instead

72. **"☐ Don't ask again" checkbox**
    - Type: Checkbox input
    - Default: Unchecked
    - Action: If checked, auto-approve all RSI oversold trades
    - Warning: "You can change this in Settings"
    - Stored: Persists in user preferences
    - Risk: User might forget they checked it

---

## PAGE 3: PERFORMANCE ANALYTICS

### HEADER & QUICK STATS

```
📊 PERFORMANCE ANALYTICS (Last 30 Days)

QUICK STATS:
├─ Total Trades: 47
├─ Winning: 34 (72%)  Losing: 13 (28%)
├─ Avg Win: +$850    Avg Loss: -$350
├─ Best: +$3,200 (Apr 15)
├─ Worst: -$1,100 (Apr 8)
├─ Sharpe Ratio: 1.8 (good)
├─ Max Drawdown: -9.5%
└─ Win/Loss Ratio: 2.43x
```

**Clicks/Inputs:**

73. **"Last 30 Days" date range selector** - Clickable
    - Type: Dropdown/selector
    - Options: [Last 7] [Last 30] [Last 90] [YTD] [All time] [Custom]
    - Action: Updates all metrics
    - Custom: Opens date picker (from/to)
    - Behavior: Persists selection

74. **"Total Trades: 47"** - Clickable
    - Type: Metric, links to Trade History
    - Action: Shows all 47 trades in filterable list

75. **"Winning: 34 (72%)"** - Clickable badge
    - Type: Green badge
    - Action: Filters trades to only winners
    - Shows: All winning trades sorted by size

76. **"Losing: 13 (28%)"** - Clickable badge
    - Type: Red badge
    - Action: Filters trades to only losers

77. **"Avg Win: +$850"** - Clickable
    - Type: Average profit display
    - Action: Shows all winning trades with avg line
    - Distribution: Histogram of win sizes
    - Comparison: Benchmark comparison

78. **"Avg Loss: -$350"** - Clickable
    - Type: Red metric
    - Action: Shows all losing trades
    - Distribution: Histogram of loss sizes

79. **"Best: +$3,200 (Apr 15)"** - Clickable
    - Type: Link to specific trade
    - Click: Opens that trade details
    - Shows: What made it the best (entry, exit, timing)

80. **"Worst: -$1,100 (Apr 8)"** - Clickable
    - Type: Link to specific trade
    - Click: Opens that trade details
    - Question: What went wrong?

81. **"Sharpe Ratio: 1.8"** - Hover tooltip
    - Type: Advanced metric
    - Hover: Explains what Sharpe Ratio means
    - Interpretation: >1.0 is good, >2.0 is excellent
    - Click: Shows Sharpe trend over time

82. **"(good)" assessment label**
    - Type: Qualitative assessment
    - Color: Green
    - Possible: Bad, Fair, Good, Excellent

83. **"Max Drawdown: -9.5%"** - Clickable
    - Type: Risk metric
    - Meaning: Biggest decline from peak
    - Click: Shows drawdown chart over time
    - Risk: Shows when it happened

84. **"Win/Loss Ratio: 2.43x"** - Tooltip
    - Type: Profitability metric
    - Meaning: Average winner is 2.43x average loser
    - Formula: Avg Win / Abs(Avg Loss)
    - Click: Explains ratio

---

### MONTHLY RETURNS CHART

```
MONTHLY RETURNS:
┌──────────────────────────────────┐
│ March: +3.2% ▂▃▅▇█              │
│ April: +8.5% ▂▃▅▇███             │
│ May: +6.1% ▂▃▅▇██                │
└──────────────────────────────────┘
```

**Clicks/Inputs:**

85. **"March: +3.2%"** bar - Clickable
    - Type: Bar chart element
    - Action: Expands to show March trades detail
    - Shows: All trades in March, filtered

86. **"▂▃▅▇█" mini chart** - Hoverable
    - Type: Sparkline (trend within month)
    - Hover: Shows tooltip with daily breakdown
    - Color gradient: Green for gains, red for losses
    - Click: Goes to Trade History filtered to that month

87. **Chart title interaction**
    - Scroll: Can scroll months left/right
    - Zoom: Can click zoom buttons to see more/fewer months
    - Range selector: [3M] [6M] [1Y] [All]

---

### P&L BY STRATEGY

```
P&L BY STRATEGY:
├─ RSI Trading: +$5,200 (60%)
│  └─ 28 trades, 75% win
├─ Copy Trading: +$2,100 (25%)
│  └─ 12 trades, 67% win
├─ Arbitrage: +$1,200 (15%)
│  └─ 7 trades, 86% win
└─ [ADJUST WEIGHTS]
```

**Clicks/Inputs:**

88. **"RSI Trading: +$5,200"** - Clickable
    - Type: Strategy profit metric
    - Action: Filters Trade History to RSI trades only
    - Shows: All RSI trades in detail

89. **"(60%)" percentage** - Visual pie chart
    - Type: Percentage of total profit
    - Pie chart: Visual breakdown (maybe pie chart hover)
    - Hover: Tooltip showing exact USD amount

90. **"28 trades, 75% win"** stats - Clickable
    - Type: Trade count and win rate
    - Action: Shows all 28 RSI trades
    - Breakdown: 21 wins, 7 losses

91. **"Copy Trading: +$2,100"** - Clickable
    - Type: Strategy profit, clickable

92. **"Arbitrage: +$1,200"** - Clickable
    - Type: Strategy profit, clickable

93. **[ADJUST WEIGHTS] button**
    - Type: Secondary button (maybe orange/highlight)
    - Action: Opens strategy weight adjustment modal
    - Modal shows:
      - Current weights (RSI 60%, Copy 25%, Arb 15%)
      - Sliders for each
      - Must total 100%
      - [Save] button applies changes
    - Effect: Changes strategy mix going forward

---

### TRADES BY ASSET

```
TRADES BY ASSET:
├─ BTC: +$3,500 (50% of total)
├─ ETH: +$2,200 (31%)
├─ SOL: +$1,000 (14%)
├─ Polymarket: +$300 (5%)
└─ [ADD ASSET] [REMOVE ASSET]
```

**Clicks/Inputs:**

94. **"BTC: +$3,500"** - Clickable
    - Type: Asset profit, clickable
    - Action: Filters Trade History to BTC trades
    - Shows: All BTC trades, stats

95. **"(50% of total)" pie slice**
    - Type: Percentage indicator
    - Hover: Shows exact P&L, trade count, win %

96. **[ADD ASSET] button**
    - Type: Secondary button
    - Action: Opens asset selector modal
    - Modal: Dropdown of available assets
    - Add: Enable trading for new asset
    - Effect: Bot can now trade this asset

97. **[REMOVE ASSET] button**
    - Type: Secondary button (maybe red outline)
    - Action: Select which asset to remove
    - Confirmation: "Stop trading [Asset]?"
    - Effect: Bot won't trade this asset anymore

---

### TRADES BY TIME

```
TRADES BY TIME:
├─ 09:00-12:00: +$4,200 (High activity)
├─ 12:00-15:00: +$2,100 (Medium)
├─ 15:00-20:00: +$1,500 (Lower)
├─ 20:00-09:00: +$400 (Slow)
└─ [VIEW HEATMAP]
```

**Clicks/Inputs:**

98. **"09:00-12:00: +$4,200"** - Clickable
    - Type: Time period profit
    - Action: Filters trades to this time period
    - Shows: Best trading hours

99. **"(High activity)" label** - Display (non-clickable)
    - Type: Activity level assessment
    - Helps: Understand when bot is active

100. **[VIEW HEATMAP] button**
     - Type: Secondary button
     - Action: Opens detailed heatmap visualization
     - Heatmap shows: Hour × Day grid with intensity
     - Color: Green = profits, Red = losses
     - Hover: Shows exact P&L for each cell
     - Purpose: Identify best trading times

101. **[EXPORT CSV] button**
     - Type: Secondary button
     - Action: Downloads performance data as CSV
     - File includes: All trades, stats, metrics

102. **[DOWNLOAD PDF] button**
     - Type: Secondary button
     - Action: Generates PDF report
     - Includes: Charts, tables, summary

103. **[SHARE] button**
     - Type: Secondary button
     - Action: Opens share options
     - Options: Copy link, email, social (if public profile)
     - Privacy: Can limit who sees

---

## PAGE 4: TRADE HISTORY

### HEADER & FILTERS

```
📜 TRADE HISTORY (Sortable, Filterable)

[Filters] ▼
├─ Asset: [All] [BTC] [ETH] [SOL] [Other]
├─ Status: [All] [Won] [Lost] [Pending]
├─ Strategy: [All] [RSI] [Copy] [Arb]
├─ Date range: [Last 7] [Last 30] [Custom]
└─ [Apply Filters]

[Sort by] ▼ Date | P&L | Win% | Risk
```

**Clicks/Inputs:**

104. **"Asset: [All]" dropdown** - Clickable
     - Type: Multi-select dropdown
     - Options: [All] [BTC] [ETH] [SOL] [Other]
     - Behavior: Can select multiple
     - Click [BTC]: Others uncheck, only BTC
     - "All": Re-selects all options
     - Updates: Trade list filters in real-time

105. **"Status: [All]" dropdown** - Clickable
     - Type: Single or multi-select
     - Options: [All] [Won] [Lost] [Pending] [Rejected by user] [Cancelled]
     - Effect: Shows only trades in selected status

106. **"Strategy: [All]" dropdown** - Clickable
     - Type: Single-select
     - Options: [All] [RSI] [Copy Trading] [Arbitrage] [Custom]
     - Effect: Filters by strategy

107. **"Date range: [Last 7]" dropdown** - Clickable
     - Type: Preset or custom date range
     - Presets: [Last 7] [Last 30] [Last 90] [YTD] [All time]
     - Custom: Opens date picker
     - Behavior: From/To dates

108. **[Apply Filters] button**
     - Type: Primary button
     - Action: Applies all filter selections
     - Behavior: May auto-apply on change, or require button click
     - Result: Trade list updates

109. **"[Sort by]" dropdown** - Clickable
     - Type: Single-select sort
     - Options: [Date] [P&L] [Win/Loss %] [Risk] [Duration] [Strategy]
     - Direction: Ascending/descending toggle
     - Click: Updates sort immediately
     - Default: Date (newest first)

110. **Sort direction toggle** (up/down arrow)
     - Type: Button to toggle ↑ ↓
     - Action: Reverses sort order

---

### TRADE LOG ROWS

```
Trade #47 (Today, 14:45)
├─ Action: BUY ETHE
├─ Entry: $2,400 | Exit: $2,520
├─ P&L: +$60 (2.5%) ✅
├─ Size: 0.5 ETH (1% account)
├─ Duration: 2h 15m
├─ Reason: RSI oversold + support
├─ Your decision: [APPROVED]
└─ [DETAILS] [EDIT NOTES]
```

**Clicks/Inputs:**

111. **Trade row (entire row)** - Clickable to expand
     - Type: Expandable row
     - Action: Shows full trade details
     - Animation: Smooth expand
     - Can collapse: Click again or [X]

112. **"Trade #47" ID** - Clickable
     - Type: Trade ID link
     - Action: Opens detailed trade view
     - Shows: Complete trade record

113. **"(Today, 14:45)" timestamp** - Clickable
     - Type: Time link
     - Action: Filters to trades around this time
     - Alternative: Shows timezone-converted time on hover

114. **"Action: BUY ETHE"** - Display
     - Type: Text (non-editable)
     - Shows: BUY or SELL
     - Color: Green = BUY, Red = SELL

115. **"Entry: $2,400"** - Display
     - Type: Entry price
     - Shows: Exact execution price

116. **"Exit: $2,520"** - Display
     - Type: Exit price
     - Shows: Exact closing price

117. **"P&L: +$60 (2.5%)"** - Clickable
     - Type: Profit/loss metric
     - Color: Green (+), Red (-)
     - Click: Shows P&L breakdown

118. **"✅" status badge** - Visual (non-clickable)
     - Green checkmark = Trade closed profitably
     - Red X = Trade closed at loss
     - Yellow = Still pending

119. **"Size: 0.5 ETH"** - Display
     - Type: Quantity traded
     - Shows: Unit and count

120. **"(1% account)" note** - Display
     - Type: Position size as % of account
     - Helps: Understand risk management

121. **"Duration: 2h 15m"** - Display
     - Type: How long position was held
     - Useful: Identify scalps vs swing trades

122. **"Reason: RSI oversold + support"** - Clickable
     - Type: Trade rationale
     - Click: Shows full technical analysis
     - Helps: Understand why bot proposed

123. **"Your decision: [APPROVED]"** - Display badge
     - Type: User action
     - Shows: [APPROVED] [REJECTED] [AUTO-APPROVED] [CANCELLED]
     - Useful: Track user override rate

124. **[DETAILS] button**
     - Type: Secondary button (small)
     - Action: Opens full trade details page
     - Shows: Comments, charts, strategy breakdown

125. **[EDIT NOTES] button**
     - Type: Secondary button (small)
     - Action: Opens note editor for this trade
     - Allows: User to add comments
     - Saved: Persists for future reference

---

## PAGE 5: BOT CONFIGURATION

### STRATEGY MIX SLIDERS

```
STRATEGY MIX:
├─ [Slider] RSI Trading: 60% ◄──────      ─────►
├─ [Slider] Copy Trading: 30% ◄──────    ─────►
├─ [Slider] Arbitrage: 10% ◄───────    ─────►
└─ [RESET TO DEFAULT]
```

**Clicks/Inputs:**

126. **RSI Trading slider handle** - Draggable
     - Type: Range input slider
     - Range: 0-100%
     - Constraints: All sliders must total 100%
     - Behavior: When drag, others adjust proportionally
     - Feedback: Shows percentage in real-time
     - Visual: Fills bar showing selected %

127. **"60%" text value** - Editable input
     - Type: Text input field
     - Input: Type exact percentage (0-100)
     - Behavior: Updates slider visual
     - Validation: Must be number, total must equal 100

128. **Copy Trading slider handle** - Draggable
     - Type: Range input (similar to above)

129. **Arbitrage slider handle** - Draggable
     - Type: Range input (similar to above)

130. **[RESET TO DEFAULT] button**
     - Type: Secondary button (maybe warning color)
     - Action: Restores original strategy mix (maybe 50/30/20 or similar)
     - Confirmation: "Reset to default mix?"
     - Effect: All sliders reset, [SAVE] needed

---

### RSI PARAMETERS

```
RSI PARAMETERS:
├─ [Input] RSI Period: [14] (default)
├─ [Input] Oversold Threshold: [30] (0-50)
├─ [Input] Overbought Threshold: [70] (50-100)
├─ [Toggle] Use divergence: [ON]
└─ [SAVE]
```

**Clicks/Inputs:**

131. **"RSI Period: [14]" input field** - Text input
     - Type: Numeric input
     - Default: 14 (standard)
     - Range: 5-30
     - Behavior: Updates RSI calculation
     - Tooltip: "Higher = smoother, Lower = more responsive"

132. **"Oversold Threshold: [30]" slider** - Draggable
     - Type: Range slider
     - Range: 0-50
     - Meaning: RSI < 30 = oversold (buy signal)
     - Lower value = more aggressive
     - Feedback: Shows on chart

133. **"Overbought Threshold: [70]" slider** - Draggable
     - Type: Range slider
     - Range: 50-100
     - Meaning: RSI > 70 = overbought (sell signal)
     - Lower value = more aggressive
     - Linked: Overbought must be > Oversold

134. **"Use divergence" toggle** - ON/OFF
     - Type: Boolean toggle
     - ON: Include RSI divergence in analysis
     - OFF: Ignore divergence signals
     - Divergence: When price makes new high but RSI doesn't
     - Tooltip: Explains what divergence means

135. **[SAVE] button (RSI section)**
     - Type: Primary button
     - Action: Saves RSI parameters
     - Confirmation: "Save RSI settings?"
     - Effect: Bot uses new RSI settings immediately
     - Feedback: "Settings saved" toast message

---

### COPY TRADING CONFIGURATION

```
COPY TRADING:
├─ [Toggle] Enabled: [ON]
├─ [Input] Max traders to follow: [3]
├─ [Button] [SELECT TRADERS]
│  └─ Following: Trader1, Trader2, Trader3
├─ [Toggle] Mirror their exact sizing: [OFF]
├─ [Slider] Size scaling: 50% (0-200%)
└─ [SAVE]
```

**Clicks/Inputs:**

136. **"Enabled: [ON]" toggle**
     - Type: Boolean toggle
     - ON: Copy trading is active
     - OFF: Copy trading disabled
     - Effect: Immediate

137. **"Max traders to follow: [3]" input**
     - Type: Numeric input
     - Range: 1-20
     - Meaning: Max traders to copy signals from
     - Helps: Avoid spreading capital too thin

138. **[SELECT TRADERS] button**
     - Type: Primary button
     - Action: Opens Trader select modal
     - Behavior:
       - Shows leaderboard of traders
       - User selects up to [n] traders
       - Shows stats (win %, returns, etc.)
       - [Confirm selection] saves choices
     - Pre-selected: Shows who already following

139. **"Following: Trader1, Trader2, Trader3"** - Chips
     - Type: Tag/chip display
     - Click chip: Shows trader details
     - [X] on chip: Remove from follow list
     - Shows: Win %, returns, shares traded

140. **"Mirror their exact sizing: [OFF]" toggle**
     - Type: Boolean toggle
     - ON: Uses same position size as copied trader
     - OFF: Scales to your account
     - Risk: ON could over-leverage you
     - Tooltip: Explains both options

141. **"Size scaling: 50%" slider**
     - Type: Range slider
     - Range: 0-200%
     - Meaning: 50% = copy 50% of their size
     - Example: If they buy $10K, you buy $5K
     - 200% = Copy 200% (2x their size, risky!)

142. **[SAVE] button (Copy trading section)**
     - Type: Primary button
     - Saves copy trading settings

---

### ARBITRAGE CONFIGURATION

```
ARBITRAGE:
├─ [Toggle] Enabled: [ON]
├─ [Input] Min spread: [1.2%]
├─ [Select boxes] Markets:
│  ├─ ☑ Binance/Coinbase (USD pairs)
│  ├─ ☑ Crypto.com/Kraken (alt pairs)
│  ├─ ☑ Polymarket (prediction markets)
│  └─ ☐ (Reserve markets)
└─ [SAVE]
```

**Clicks/Inputs:**

143. **"Enabled: [ON]" toggle**
     - Type: Boolean toggle
     - ON: Arbitrage trading active
     - OFF: Disabled

144. **"Min spread: [1.2%]" input**
     - Type: Numeric input
     - Range: 0.1-10%
     - Meaning: Only trade if price spread > 1.2%
     - Lower = more trades (but less profit each)
     - Higher = fewer trades (but bigger profit)

145. **"Binance/Coinbase" checkbox** - ☑
     - Type: Boolean checkbox
     - ON: Include these exchanges
     - OFF: Exclude
     - Exchanges: USD pair trading

146. **"Crypto.com/Kraken" checkbox** - ☑
     - Type: Boolean checkbox
     - Alternative exchange pair

147. **"Polymarket" checkbox** - ☑
     - Type: Boolean checkbox
     - Prediction markets arbitrage

148. **[SAVE] button (Arbitrage)**
     - Type: Primary button
     - Saves arbitrage settings

---

### POSITION SIZING

```
POSITION SIZING:
├─ [Slider] % of account per trade: [1.5%]
│  (On $100K account = $1,500 max per trade)
├─ [Slider] Max concurrent trades: [5]
├─ [Slider] Max daily positions: [10]
└─ [SAVE]
```

**Clicks/Inputs:**

149. **"% of account per trade" slider**
     - Type: Range slider
     - Range: 0.1-5%
     - Shows: Dollar amount based on current equity
     - Risk management: Controls max loss per trade
     - Tooltip: "Lower = safer, Higher = aggressive"

150. **"Max concurrent trades" slider**
     - Type: Range slider
     - Range: 1-20
     - Meaning: How many open positions allowed
     - Risk: Spreads capital across multiple trades

151. **"Max daily positions" slider**
     - Type: Range slider
     - Range: 1-50
     - Meaning: Max trades per day
     - Helps: Prevent overtrading

152. **[SAVE] button (Position sizing)**
     - Type: Primary button

---

### RISK CONTROLS

```
RISK CONTROLS:
├─ [Slider] Daily loss limit: [-1.0%]
│  (Bot stops at -$1,000 per day)
├─ [Slider] Stop loss on all trades: [-2.5%]
├─ [Slider] Take profit auto-close: [+3.0%]
├─ [Input] Max trade duration: [24] hours
└─ [SAVE]
```

**Clicks/Inputs:**

153. **"Daily loss limit" slider**
     - Type: Range slider
     - Range: -0.1% to -10%
     - Shows: Dollar impact on $100K account
     - Meaning: Bot stops all trading at this daily loss
     - Safety: Prevents catastrophic losses

154. **"Stop loss on all trades" slider**
     - Type: Range slider
     - Range: -0.5% to -10%
     - Meaning: Every trade has automatic stop
     - Can't be turned off by user (mandatory)

155. **"Take profit auto-close" slider**
     - Type: Range slider
     - Range: +0.5% to +10%
     - Meaning: Close at this profit level automatically
     - Lock in gains

156. **"Max trade duration" input**
     - Type: Numeric input + dropdown
     - Values: Hours or days
     - Range: 1 hour to 30 days
     - Meaning: Trades close automatically after this time
     - Prevents: Holding winners too long

157. **[SAVE] button (Risk controls)**
     - Type: Primary button

---

## (CONTINUED IN PART 2 - TOKEN LIMIT)

---

## SUMMARY: COMPLETE CLICKS & INPUTS TALLY

**Total identified so far: 157 clicks/inputs**

**Remaining pages to detail:**
- PAGE 6: Positions & Portfolio (~25 clicks)
- PAGE 7: Watchlist & Alerts (~20 clicks)
- PAGE 8: Billing & Revenue Share (~15 clicks)
- PAGE 9: Community & Learning (~30 clicks)
- PAGE 10: Settings & Account (~30 clicks)

**Estimated total**: 250-300 clicks/inputs across all pages

All mapped with exact behaviors, state changes, validation rules, and user flows.
