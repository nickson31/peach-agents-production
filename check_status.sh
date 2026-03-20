#!/bin/bash

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║        OPERATIONS ALERTS - STATUS CHECK                        ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

echo "🔍 PROCESS STATUS:"
if pgrep -f "operations_telegram_bridge.py" > /dev/null; then
    PID=$(pgrep -f "operations_telegram_bridge.py")
    echo "   ✅ RUNNING (PID: $PID)"
    UPTIME=$(ps -p $PID -o etime= | tr -d ' ')
    echo "   Uptime: $UPTIME"
else
    echo "   ❌ NOT RUNNING"
fi

echo ""
echo "📊 RECENT ALERTS:"
if [ -f "/home/ubuntu/.openclaw/workspace/alerts_monitor.log" ]; then
    LINES=$(wc -l < /home/ubuntu/.openclaw/workspace/alerts_monitor.log)
    echo "   Log lines: $LINES"
    echo ""
    echo "   Last 5 checks:"
    tail -5 /home/ubuntu/.openclaw/workspace/alerts_monitor.log | sed 's/^/   /'
else
    echo "   No log file yet"
fi

echo ""
echo "📁 STATE FILE:"
if [ -f "/home/ubuntu/.openclaw/workspace/bridge_state.json" ]; then
    REPORTED=$(cat /home/ubuntu/.openclaw/workspace/bridge_state.json | grep -o '"reported"' | wc -l)
    echo "   ✅ Exists"
    # Count reported orders
    python3 -c "
import json
with open('/home/ubuntu/.openclaw/workspace/bridge_state.json') as f:
    data = json.load(f)
    reported = len(data.get('reported', {}))
    print(f'   Reported orders: {reported}')
" 2>/dev/null || echo "   (parsing...)"
else
    echo "   ⚠️  Not created yet"
fi

echo ""
echo "🔗 ALPACA CONNECTION:"
python3 -c "
import requests, base64
key = 'PKW445AWAOSGU2WJYCCFUZ47PR'
secret = '7tmQ6gY5c4hdmqwEN3UAgv4to78WsGkWPmxUox4G7x4X'
auth = base64.b64encode(f'{key}:{secret}'.encode()).decode()
try:
    resp = requests.get(
        'https://paper-api.alpaca.markets/v2/account',
        headers={'Authorization': f'Basic {auth}'},
        timeout=5
    )
    if resp.status_code == 200:
        account = resp.json()
        print(f'   ✅ Connected')
        print(f'   Buying Power: \${float(account.get(\"buying_power\", 0)):,.2f}')
        print(f'   Cash: \${float(account.get(\"cash\", 0)):,.2f}')
    else:
        print(f'   ❌ Error: {resp.status_code}')
except Exception as e:
    print(f'   ❌ Connection failed: {str(e)[:40]}')
" 2>/dev/null || echo "   (checking...)"

echo ""
echo "🎯 ORDERS STATUS:"
python3 -c "
import requests, base64
key = 'PKW445AWAOSGU2WJYCCFUZ47PR'
secret = '7tmQ6gY5c4hdmqwEN3UAgv4to78WsGkWPmxUox4G7x4X'
auth = base64.b64encode(f'{key}:{secret}'.encode()).decode()
try:
    resp = requests.get(
        'https://paper-api.alpaca.markets/v2/orders?status=all&limit=500',
        headers={'Authorization': f'Basic {auth}'},
        timeout=5
    )
    orders = resp.json()
    status_count = {}
    for o in orders:
        s = o.get('status', 'unknown')
        status_count[s] = status_count.get(s, 0) + 1
    
    print(f'   Total orders: {len(orders)}')
    for status in sorted(status_count.keys()):
        print(f'   - {status.upper()}: {status_count[status]}')
except Exception as e:
    print(f'   ❌ Failed: {str(e)[:40]}')
" 2>/dev/null || echo "   (fetching...)"

echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "Commands:"
echo "  View logs:      tail -f /home/ubuntu/.openclaw/workspace/alerts_monitor.log"
echo "  Stop monitor:   killall python3 operations_telegram_bridge.py"
echo "  Restart:        cd /home/ubuntu/.openclaw/workspace && nohup python3 operations_telegram_bridge.py --continuous > alerts_monitor.log 2>&1 &"
echo "  Check status:   bash check_status.sh"
echo ""
