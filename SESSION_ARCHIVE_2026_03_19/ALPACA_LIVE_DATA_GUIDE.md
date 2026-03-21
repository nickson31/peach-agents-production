# Alpaca Live Data: Opciones, Costos, Implementación

## RESUMEN EJECUTIVO

```
PAPER TRADING (MVP):
├─ Acceso: 15-20 min delayed data (FREE)
├─ Real-time: NO
├─ Uso: Perfect for backtest + simulation
└─ Cost: $0

LIVE TRADING U.S. STOCKS:
├─ Market Data: SIP (real-time) vs UTP (real-time)
├─ Cost: FREE (Alpaca covers it for brokers)
├─ WebSocket: FREE, unlimited
└─ Best for: Stocks/ETFs

CRYPTO:
├─ Data: Coinbase websocket (real-time, FREE)
├─ Cost: $0
└─ Best for: Crypto traders

FOREX:
├─ Data: Need external provider (OANDA, FXCM, etc)
├─ Cost: $0-100/mo depending on provider
└─ Best for: Forex traders
```

---

## OPCIÓN 1: PAPER TRADING (15-20 min delayed)

### Qué es
```
Alpaca da precios delayed (15-20 minutos atrás)
├─ Totalmente GRATIS
├─ WebSocket NO incluido (polling only)
└─ Perfecto para backtest, NO para live trading
```

### Cómo acceder
```python
from alpaca_trade_api import REST

# Paper trading account
api = REST(
    base_url='https://paper-api.alpaca.markets',
    key_id='YOUR_API_KEY',
    secret_key='YOUR_SECRET_KEY'
)

# Get last bar (delayed 15-20 min)
barset = api.get_barset('EUR_USD', '1min', limit=100)
last_bar = barset['EUR_USD'][-1]

print(f"Price: {last_bar['c']} (delayed ~20 min)")
```

### Ventajas
- ✅ Completely FREE
- ✅ No signup for market data
- ✅ Unlimited API calls
- ✅ Works for MVP backtests

### Desventajas
- ❌ 15-20 min delayed (not real-time)
- ❌ No WebSocket
- ❌ Polling only (slower, less efficient)
- ❌ Can't use for live trading

### Costo: $0
### Mejor para: MVP, Backtesting

---

## OPCIÓN 2: LIVE TRADING U.S. STOCKS (Real-time, FREE)

### Qué es
```
Si tienes cuenta VIVA (linked to real money account):
├─ Alpaca te DA acceso gratis a SIP/UTP real-time data
├─ NO CUESTA NADA (Alpaca lo subsidia)
└─ WebSocket real-time incluido
```

### Requisitos
```
1. Broker relationship active (live account)
2. Account funding >= $500 (minimum to trade)
3. Alpaca covers SIP/UTP cost for active brokers
```

### Cómo acceder
```python
from alpaca.data.live import StockDataStream

# Live account (connected to live broker)
wss_client = StockDataStream(
    api_key='YOUR_API_KEY',
    secret_key='YOUR_SECRET_KEY',
    feed='SIP'  # Real-time, covered by Alpaca
)

async def handle_quote(quote):
    print(f"LIVE {quote.symbol}: {quote.ask_price}")

wss_client.subscribe_quotes(handle_quote, 'EUR/USD')
await wss_client.run()
```

### Ventajas
- ✅ Real-time (< 1 sec lag)
- ✅ WebSocket (efficient)
- ✅ FREE (Alpaca subsidizes)
- ✅ Unlimited subscriptions
- ✅ SIP = best quality data (NYSE)

### Desventajas
- ❌ Need live account ($0 commission but need funding)
- ❌ Only stocks/ETFs (not forex)
- ❌ User needs Alpaca account

### Costo: $0
### Mejor para: Live trading (stocks only)

---

## OPCIÓN 3: CRYPTO (Real-time, FREE)

### Qué es
```
Alpaca usa Coinbase websocket:
├─ Real-time crypto data (< 100ms)
├─ GRATIS (no data fees)
└─ Unlimited WebSocket subscriptions
```

### Cómo acceder
```python
from alpaca.data.live import CryptoDataStream

wss_client = CryptoDataStream(
    api_key='YOUR_API_KEY',
    secret_key='YOUR_SECRET_KEY'
)

async def handle_quote(quote):
    print(f"LIVE {quote.symbol}: {quote.ask_price}")

wss_client.subscribe_quotes(handle_quote, 'BTC/USD')
wss_client.subscribe_quotes(handle_quote, 'ETH/USD')
await wss_client.run()
```

### Ventajas
- ✅ Real-time
- ✅ WebSocket (efficient)
- ✅ FREE
- ✅ 24/7 data
- ✅ Multiple crypto pairs

### Desventajas
- ❌ Crypto only (not stocks/forex)
- ❌ Need Alpaca account

### Costo: $0
### Mejor para: Crypto traders

---

## OPCIÓN 4: FOREX (Paid or Free depending)

### Problema
```
Alpaca NO ofrece forex directo.
Opciones:
├─ A. OANDA API (FREE for data, $0 commission for Algo trading)
├─ B. FXCM API (FREE data + trading)
├─ C. Interactive Brokers (FREE data if account funded)
└─ D. Manual: Scrape OANDA rates (webscraping)
```

### Opción A: OANDA (RECOMENDADO)
```python
import oandapyV20
from oandapyV20.endpoints import instruments, pricing

account_id = 'YOUR_OANDA_ACCOUNT_ID'
access_token = 'YOUR_OANDA_API_KEY'

# Real-time forex via streaming
api = oandapyV20.API(access_token=access_token)

params = {
    "instruments": "EUR_USD,GBP_USD,XAU_USD"
}

# Streaming prices (free)
streamer = pricing.PricingStream(
    accountID=account_id,
    params=params
)
streamer.connect()

for msg in streamer.response:
    print(msg)  # Real-time quotes
```

### Ventajas
- ✅ Real-time forex data (FREE)
- ✅ WebSocket streaming
- ✅ NO commission on API trades
- ✅ Excellent for EUR/USD, Gold

### Desventajas
- ❌ Need OANDA account
- ❌ Separate from Alpaca
- ❌ Different broker ecosystem

### Costo: $0 (data), $0 (trades via Algo)
### Mejor para: Forex traders (EUR/USD, Gold)

---

## OPCIÓN 5: POLYGON.IO (Premium data, PAID)

### Qué es
```
Polygon.io = aggregated market data:
├─ Real-time stocks
├─ Forex (forex data aggregation)
├─ Crypto
├─ Options
└─ $99-599/mo depending on tier
```

### Planes
```
STARTER: $99/mo
├─ Real-time stocks
├─ 2 year historical
└─ Good for MVP

PROFESSIONAL: $399/mo
├─ All assets (stocks + forex + crypto)
├─ Earlier data
└─ Better for scaling

ENTERPRISE: Custom pricing
```

### Cómo acceder
```python
from polygon import RESTClient

client = RESTClient(
    api_key='YOUR_POLYGON_API_KEY'
)

# Real-time quotes
quotes = client.get_last_quote('EUR/USD')
print(f"Bid: {quotes.bid}, Ask: {quotes.ask}")
```

### Ventajas
- ✅ All asset classes (stocks, forex, crypto)
- ✅ Real-time
- ✅ Aggregated data (multiple sources)
- ✅ Good documentation

### Desventajas
- ❌ PAID ($99-599/mo)
- ❌ Expensive for MVP
- ❌ Overkill if only need stocks or forex

### Costo: $99-599/mo
### Mejor para: Scaling (when free options not enough)

---

## COMPARATIVA: QUÉ USAR PARA CADA CASO

```
┌─────────────────────────────────────────────────────━━━━━━━━━┐
│ TRADER TYPE          │ DATA SOURCE    │ COST  │ LATENCY    │
├──────────────────────┼────────────────┼───────┼────────────┤
│ Backtest (Historical)│ Alpaca Paper   │ $0    │ 15-20min   │
│ Stocks Live          │ Alpaca SIP     │ $0    │ <1 sec     │
│ Crypto Live          │ Alpaca Crypto  │ $0    │ <100ms     │
│ Forex Live           │ OANDA Stream   │ $0    │ <500ms     │
│ Multi-asset Live     │ Polygon.io     │ $99   │ <500ms     │
│ Premium (best)       │ Polygon Prof   │ $399  │ <100ms     │
└──────────────────────┴────────────────┴───────┴────────────┘
```

---

## RECOMENDACIÓN PARA MVP V0

### Setup Mínimo (Gratuito)

**Para Stock/ETF Traders:**
```
1. Alpaca live account (free to open)
2. SIP real-time (FREE, included)
3. WebSocket streaming (FREE)
4. Backtest: Historical from Alpaca (FREE)
```

**Para Crypto Traders:**
```
1. Alpaca Crypto account
2. Real-time via Coinbase websocket (FREE)
3. WebSocket streaming (FREE)
4. Backtest: Historical from Alpaca (FREE)
```

**Para Forex Traders:**
```
1. OANDA account (free to open)
2. Real-time streaming (FREE)
3. No commission on algo trades
4. Backtest: Download OHLCV from OANDA (FREE)
```

**Costo Total: $0**

---

## ARQUITECTURA RECOMENDADA (MVP)

### Múltiples Brokers (Flexible)

```javascript
// Bot executes on user's chosen broker

if (user.broker === 'stocks') {
  // Alpaca SIP real-time
  // WebSocket: StockDataStream
  // Order execution: Alpaca API
  
} else if (user.broker === 'crypto') {
  // Alpaca Crypto
  // WebSocket: CryptoDataStream
  // Order execution: Alpaca API
  
} else if (user.broker === 'forex') {
  // OANDA streaming
  // WebSocket: OANDA REST streaming
  // Order execution: OANDA API
}
```

### Ventajas
- ✅ User picks their broker
- ✅ We support all major (Alpaca, OANDA, etc)
- ✅ No vendor lock-in
- ✅ Cost: $0 (user pays what they want)

---

## IMPLEMENTACIÓN: WebSocket Monitoring Loop

```python
import asyncio
from alpaca.data.live import StockDataStream

class BotMonitor:
    def __init__(self, bot_config, alpaca_api):
        self.bot = bot_config
        self.api = alpaca_api
        self.wss = StockDataStream(
            api_key=alpaca_api.key_id,
            secret_key=alpaca_api.secret_key,
            feed='SIP'  # Real-time
        )
    
    async def handle_quote(self, quote):
        """Called on every price update (real-time)"""
        
        # Check if entry triggered
        if (quote.ask_price <= self.bot.entry_price and 
            not self.bot.order_placed):
            
            # Place order
            await self.place_order()
        
        # Check if TP/SL hit
        if self.bot.position_open:
            if quote.bid_price >= self.bot.tp_price:
                await self.close_position('tp_hit', quote.bid_price)
            elif quote.ask_price <= self.bot.sl_price:
                await self.close_position('sl_hit', quote.ask_price)
    
    async def place_order(self):
        """Place limit order at entry price"""
        order = self.api.submit_order(
            symbol=self.bot.symbol,
            qty=self.bot.qty,
            side='buy',
            order_type='limit',
            limit_price=self.bot.entry_price
        )
        self.bot.order_placed = True
    
    async def close_position(self, reason, price):
        """Close position, log P&L"""
        order = self.api.submit_order(
            symbol=self.bot.symbol,
            qty=self.bot.qty,
            side='sell',
            order_type='market'
        )
        
        # Calculate P&L and log
        pnl = (price - self.bot.entry_price) * self.bot.qty
        self.log_execution(reason, price, pnl)
    
    async def run(self):
        """Subscribe to real-time quotes"""
        self.wss.subscribe_quotes(
            self.handle_quote,
            self.bot.symbol
        )
        await self.wss.run()
```

### Ventajas de este approach
- ✅ Real-time event-driven (not polling)
- ✅ Fast response (<100ms)
- ✅ WebSocket efficient (one connection)
- ✅ Auto-scales to 1000+ bots

---

## COSTO FINAL CON DATOS REALES

```
MVP V0 (Real-time bots):
├─ Alpaca SIP: $0 (subsidized)
├─ OANDA Forex: $0 (free streaming)
├─ Alpaca Crypto: $0 (Coinbase websocket)
├─ BackTest data: $0 (historical free)
└─ TOTAL COST: $0 for data

At scale (1000 users):
├─ Still $0 (Alpaca, OANDA, Coinbase don't charge per connection)
└─ Only cost: Your infrastructure (Vercel, DB)
```

---

## RESUMEN

| Feature | MVP | Scale |
|---------|-----|-------|
| Live Stock Data | Alpaca SIP ($0) | Alpaca SIP ($0) |
| Live Crypto Data | Alpaca Crypto ($0) | Alpaca Crypto ($0) |
| Live Forex Data | OANDA ($0) | OANDA ($0) |
| WebSocket | FREE | FREE |
| Backtest Data | Alpaca free | Alpaca free |
| **Total Data Cost** | **$0** | **$0** |

**Conclusion: Real-time data is FREE. No hidden costs.**

