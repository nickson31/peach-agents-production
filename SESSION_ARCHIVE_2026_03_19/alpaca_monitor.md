# Alpaca Background Monitor - OpenClaw Persistent Agent

## Overview
Este monitor corre 24/7 en background checkeando tus órdenes en Alpaca y enviando updates a Telegram.

## Configuration

```yaml
ALPACA_KEY: PKW445AWAOSGU2WJYCCFUZ47PR
ALPACA_SECRET: 7tmQ6gY5c4hdmqwEN3UAgv4to78WsGkWPmxUox4G7x4X
TELEGRAM_USER: 7540076919
CHECK_INTERVAL: 30 seconds
```

## Features

- ✅ Monitorea órdenes en tiempo real
- ✅ Detecta cambios: new → pending → filled → canceled
- ✅ Envía alerts a Telegram (entry, TP hit, SL hit)
- ✅ Calcula P&L automáticamente
- ✅ Persiste estado en JSON
- ✅ Detecta duplicados automáticamente

## Deployment

```bash
openclaw cron add alpaca-monitor \
  --task "Monitor Alpaca orders 24/7" \
  --script "/home/ubuntu/.openclaw/workspace/monitor.py" \
  --interval "*/1 * * * *"  # Cada minuto
```

## Alerts Enviados

1. **Order Placed** → "✅ Orden creada: EUO 100 @ $24.99"
2. **Order Filled** → "🎯 Orden ejecutada: EUO 100 @ $24.95 | P&L: +$40"
3. **Order Partial Fill** → "⚠️ Ejecución parcial: EUO 50/100 @ $24.95"
4. **Order Canceled** → "❌ Orden cancelada: EUO (100 @ $24.99)"
5. **Position Update** → "📊 Posición: EUO +100 units | P&L: +$2,450"

## State File

```json
{
  "last_check": "2026-03-19T13:06:00Z",
  "orders_tracked": {
    "46e2c64f-4df7-406b-9417-233d3092649d": {
      "symbol": "GLD",
      "qty": 100,
      "entry_price": 191.1,
      "current_price": 191.15,
      "status": "new",
      "filled_qty": 0,
      "pnl": 5,
      "last_alert": "2026-03-19T13:02:00Z"
    }
  },
  "alerts_sent": 3
}
```

## Manual Commands

```bash
# Check status
python3 /home/ubuntu/.openclaw/workspace/monitor.py --status

# Force check now
python3 /home/ubuntu/.openclaw/workspace/monitor.py --check-now

# View alerts history
python3 /home/ubuntu/.openclaw/workspace/monitor.py --history

# Pause monitoring
python3 /home/ubuntu/.openclaw/workspace/monitor.py --pause

# Resume monitoring
python3 /home/ubuntu/.openclaw/workspace/monitor.py --resume
```
