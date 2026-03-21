# TELEGRAM OPERATIONS ALERTS - Setup Guide

## Overview

Sistema automático que detecta operaciones cerradas en Alpaca y envía alertas formateadas a Telegram.

---

## Scripts Disponibles

### 1. `alert_closed_operations.py`
**Propósito**: Monitoreo básico de operaciones cerradas

```bash
# Single check
python3 alert_closed_operations.py

# Continuous monitoring
python3 alert_closed_operations.py --continuous
```

**Output**:
- Tabla columnar con operaciones cerradas
- P&L por operación
- Formato: Columnas o párrafos

**Uso**: Testing y verificación manual

---

### 2. `telegram_operations_alerts.py`
**Propósito**: Alertas formateadas para Telegram

```bash
# Check and generate message
python3 telegram_operations_alerts.py
```

**Output**:
- Mensaje Telegram-compatible
- Agrupado por YouTuber
- P&L total
- Estado de ejecución

**Uso**: Producción (ejecutar vía cron)

---

### 3. `operations_telegram_bridge.py`
**Propósito**: Bridge integrado con OpenClaw message system

```bash
# Single check
python3 operations_telegram_bridge.py

# Continuous (recomendado)
python3 operations_telegram_bridge.py --continuous
```

**Features**:
- ✅ Auto-detección de operaciones cerradas
- ✅ Integración nativa OpenClaw
- ✅ Estado persistente (no duplica alertas)
- ✅ Mensajes formateados

---

## Configuración Automática

### Opción A: Cron Job (cada 5 minutos)

```bash
# Agregar cron job
(crontab -l 2>/dev/null || true; echo "*/5 * * * * python3 /home/ubuntu/.openclaw/workspace/telegram_operations_alerts.py >> /home/ubuntu/.openclaw/workspace/alerts.log 2>&1") | crontab -

# Verificar
crontab -l | grep operations
```

### Opción B: Systemd Service (recomendado para producción)

```bash
# Crear service file
cat > /tmp/operations-alerts.service << 'EOF'
[Unit]
Description=Alpaca Operations Telegram Alerts
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/ubuntu/.openclaw/workspace/operations_telegram_bridge.py --continuous
Restart=always
RestartSec=10
User=ubuntu
WorkingDirectory=/home/ubuntu/.openclaw/workspace
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Instalar (requiere sudo)
sudo cp /tmp/operations-alerts.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable operations-alerts
sudo systemctl start operations-alerts

# Verificar status
sudo systemctl status operations-alerts
```

### Opción C: Background Process (simple)

```bash
# Terminal 1: Start monitoring
cd /home/ubuntu/.openclaw/workspace
nohup python3 operations_telegram_bridge.py --continuous > alerts.log 2>&1 &

# Check if running
ps aux | grep operations_telegram_bridge

# View logs
tail -f alerts.log
```

---

## Mensaje Telegram - Formato

### Ejemplo: Batch Summary

```
📊 OPERACIONES EJECUTADAS

Resumen:
├─ Total cerradas: 62
├─ Ejecutadas: 62 ✅
└─ P&L Total: +$1,250

════════════════════════════

🎯 ForexMentor - 15 órdenes
   ✅ EUO
   ✅ GBTC
   ✅ ETHE
   ... +12 más

🎯 CryptoBob - 12 órdenes
   ✅ ETHE
   ✅ GBTC
   ... +10 más

════════════════════════════
💰 Total: +$1,250
⏱️ 13:39 UTC
```

### Ejemplo: Individual Alert

```
✅ ForexMentor → EUO
FILLED
Qty: 10 @ $108.48
Target: $108.50
P&L: +$20
```

---

## Columns Disponibles

```
| Campo | Contenido | Ejemplo |
|-------|-----------|---------|
| YouTuber | Creator de estrategia | ForexMentor |
| Symbol | Instrumento Alpaca | EUO, GBTC, ETHE |
| Status | Estado orden | FILLED, PARTIAL, CANCELED |
| Qty | Cantidad ejecutada | 10 |
| Price | Precio ejecución | $108.48 |
| Target | Precio limit original | $108.50 |
| P&L | Ganancia/Pérdida | +$20 ó -$15 |
| Time | Hora de ejecución | 13:39 UTC |
```

---

## Data Persistence

### State File: `bridge_state.json`

```json
{
  "reported": {
    "order-id-1": "2026-03-19T13:30:00",
    "order-id-2": "2026-03-19T13:35:00"
  },
  "last_summary": "2026-03-19T13:39:00"
}
```

**Propósito**: 
- Evita alertas duplicadas
- Rastrea qué órdenes ya fueron reportadas
- Persiste entre ejecuciones

---

## Troubleshooting

### Problema: No recibe alertas

**Verificación:**
```bash
# 1. Check if script is running
ps aux | grep operations

# 2. Check logs
tail -f /home/ubuntu/.openclaw/workspace/alerts.log

# 3. Verify Alpaca connection
python3 -c "
import requests, base64
key = 'PKW445AWAOSGU2WJYCCFUZ47PR'
secret = '7tmQ6gY5c4hdmqwEN3UAgv4to78WsGkWPmxUox4G7x4X'
auth = base64.b64encode(f'{key}:{secret}'.encode()).decode()
resp = requests.get(
    'https://paper-api.alpaca.markets/v2/orders',
    headers={'Authorization': f'Basic {auth}'}
)
print(f'Status: {resp.status_code}')
print(f'Orders: {len(resp.json())}')
"

# 4. Check Telegram ID
echo "Telegram User: 7540076919"
```

### Problema: Alertas duplicadas

**Solución:**
```bash
# Reset state file
rm /home/ubuntu/.openclaw/workspace/bridge_state.json

# Restart script
killall python3 operations_telegram_bridge.py
python3 operations_telegram_bridge.py --continuous &
```

### Problema: Mensajes malformateados

**Verificación:**
```bash
# Test message format
python3 -c "
from telegram_operations_alerts import format_telegram_message
import requests, base64

key = 'PKW445AWAOSGU2WJYCCFUZ47PR'
secret = '7tmQ6gY5c4hdmqwEN3UAgv4to78WsGkWPmxUox4G7x4X'
auth = base64.b64encode(f'{key}:{secret}'.encode()).decode()

resp = requests.get(
    'https://paper-api.alpaca.markets/v2/orders?status=filled&limit=5',
    headers={'Authorization': f'Basic {auth}'}
)

orders = resp.json()
msg = format_telegram_message(orders)
print(msg)
"
```

---

## Integración Avanzada

### Webhook Alpaca (futuro)

```python
# Cuando Alpaca soporte webhooks:
@app.route('/alpaca/webhook', methods=['POST'])
def alpaca_webhook():
    order = request.json
    if order['status'] == 'filled':
        send_telegram_alert(order)
    return {'ok': True}
```

### Filtros Personalizados

Modificar `check_and_alert()` para:

```python
# Solo alertar si P&L > $50
if pnl > 50:
    send_alert(order)

# Solo alertar ciertos símbolos
if symbol in ['EUO', 'GBTC']:
    send_alert(order)

# Solo alertar YouTubers específicos
if youtuber in ['ForexMentor', 'CryptoBob']:
    send_alert(order)
```

---

## Monitoring Dashboard

Para ver estado en vivo:

```bash
# Ver últimas alertas
tail -100 /home/ubuntu/.openclaw/workspace/telegram_alerts.log

# Ver estado de órdenes
cat /home/ubuntu/.openclaw/workspace/bridge_state.json | jq '.reported | length'

# Ver log de errores
grep ERROR /home/ubuntu/.openclaw/workspace/alerts.log
```

---

## Parar/Reiniciar

### Si es Cron Job

```bash
# Ver cron
crontab -l

# Remover
crontab -r

# Reinstalar
crontab /tmp/cron_alerts.txt
```

### Si es Background Process

```bash
# Detener
killall python3 operations_telegram_bridge.py

# O específicamente
kill $(pgrep -f "operations_telegram_bridge.py")

# Reiniciar
python3 /home/ubuntu/.openclaw/workspace/operations_telegram_bridge.py --continuous &
```

### Si es Systemd

```bash
# Ver status
sudo systemctl status operations-alerts

# Detener
sudo systemctl stop operations-alerts

# Reiniciar
sudo systemctl restart operations-alerts

# Ver logs
sudo journalctl -u operations-alerts -f
```

---

## Status Checker Script

```bash
#!/bin/bash
echo "=== OPERATIONS ALERTS STATUS ==="
echo ""
echo "Process:"
ps aux | grep operations_telegram_bridge | grep -v grep || echo "  NOT RUNNING ❌"

echo ""
echo "Recent alerts:"
tail -3 /home/ubuntu/.openclaw/workspace/telegram_alerts.log

echo ""
echo "Reported orders:"
cat /home/ubuntu/.openclaw/workspace/bridge_state.json | jq '.reported | length' || echo "  0"
```

---

## Production Checklist

- [ ] Script configurado en cron o systemd
- [ ] State file creado (`bridge_state.json`)
- [ ] Telegram ID verificado (7540076919)
- [ ] Alpaca API keys válidas
- [ ] Logs siendo guardados
- [ ] Alertas siendo recibidas
- [ ] P&L siendo calculado correctamente
- [ ] No hay alertas duplicadas
- [ ] Mensajes están formateados correctamente
- [ ] Error handling funcionando

---

## Support

Para debugging:
```bash
# Enable verbose logging
DEBUG=1 python3 operations_telegram_bridge.py

# Test individual functions
python3 -c "
from operations_telegram_bridge import *
orders = get_all_orders()
print(f'Total orders: {len(orders)}')
print(f'Filled: {sum(1 for o in orders if o[\"status\"] == \"filled\")}')
"
```

---

**Status: ✅ Ready for Production**

Sistema completamente automatizado para alertas de operaciones cerradas a Telegram.
