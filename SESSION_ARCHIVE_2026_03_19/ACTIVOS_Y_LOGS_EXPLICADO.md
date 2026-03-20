# ACTIVOS & LOGS DE ALPACA - EXPLICACIÓN COMPLETA

## 🏦 ACTIVOS EN LOS QUE OPERAMOS

### 1. ETHE (Ethereum Trust - ETF)
```
¿QUÉ ES?
├─ Fondo de inversión que replica el precio de Ethereum
├─ Símbolo: ETHE (en Alpaca)
├─ Ethereum real: ETH (blockchain crypto)
└─ ETHE = forma de tradear ETH sin tener crypto directo

VENTAJAS:
├─ Baja volatilidad vs. ETH puro
├─ Altamente líquido (fácil de comprar/vender)
├─ Sin comisiones de wallet
├─ Trading tradicional (como acciones)

CARACTERÍSTICAS:
├─ Rango de precio: $2,000-4,000+
├─ Fill rate en Batch 5: 93% (EXCELENTE)
├─ Volumen: Alto (institucional)
├─ Spreads: Bajos (fácil llenar órdenes)

DATOS 2026:
├─ Predicción bullish: $3,500-4,000+
├─ Flujos institucionales: +$6.2B año-a-fecha
├─ BlackRock ETHA: 60-70% del volumen
└─ Tendencia: FUERTE AL ALZA
```

### 2. GBTC (Grayscale Bitcoin Trust - ETF)
```
¿QUÉ ES?
├─ Fondo que replica el precio de Bitcoin
├─ Símbolo: GBTC (en Alpaca)
├─ Bitcoin real: BTC (blockchain)
└─ GBTC = forma de tradear BTC sin wallet

VENTAJAS:
├─ Estable y predecible
├─ Muy alta liquidez
├─ Spreads pequeños
├─ Confiable para swing trading

CARACTERÍSTICAS:
├─ Rango de precio: $50-100+
├─ Fill rate en Batch 5: 90% (EXCELENTE)
├─ Volumen: ALTÍSIMO (más que ETHE)
├─ Spreads: MUY bajos

DATOS 2026:
├─ Inflows consistentes
├─ Tendencia: Bullish
├─ Proyección 2040: $150+
└─ Confiabilidad: MÁXIMA
```

### 3. FXA (Currency ETF - Dólar Australiano)
```
¿QUÉ ES?
├─ ETF que replica AUD/USD
├─ Símbolo: FXA (en Alpaca)
├─ Permite tradear divisas como acciones
└─ Menor volatilidad que crypto

CARACTERÍSTICAS:
├─ Rango de precio: $60-70
├─ Fill rate en Batch 5: media (~50%)
├─ Volumen: Medio (menos que GBTC/ETHE)
├─ Spreads: Más anchos (más difícil llenar)

USO EN BATCHES:
├─ Batch 5: 10% allocation
├─ Razón: Diversificación
├─ Ventaja: No correlaciona con crypto
└─ Desventaja: Menos líquido
```

### 4. OTROS SÍMBOLOS (Problemáticos - NO USAR)

#### FXB (Bank ETF - INVÁLIDO)
```
❌ PROBLEMA: No existe en Alpaca
└─ Fill rate Batch 1-5: 0% (nunca se llenó)
```

#### EUO (Euro Currency - ERRORES)
```
❌ PROBLEMAS: 
├─ Validation errors (422)
├─ API format issues
└─ Fill rate: Muy bajo

ACCIÓN: REMOVIDO de Batch 6+
```

#### GLD (Gold ETF - UNPROVEN)
```
❌ PROBLEMA:
├─ No probado en nuestros batches
├─ Histórico desconocido
└─ Mejor usar ETHE/GBTC (proven)
```

---

## 📊 LOGS DE ALPACA - TODAS LAS COLUMNAS EXPLICADAS

### Estructura de una ORDEN (Order Object)

```json
{
  "id": "12345678-1234-1234-1234-123456789012",
  "client_order_id": "BATCH_6_ETHE_1711123200",
  "created_at": "2026-03-19T21:00:00Z",
  "updated_at": "2026-03-19T21:00:05Z",
  "submitted_at": "2026-03-19T21:00:00Z",
  "filled_at": "2026-03-19T21:00:02Z",
  "expired_at": null,
  "canceled_at": null,
  "failed_at": null,
  
  "asset_id": "b0b6dd9d-8b9b-48a9-ba46-b9d54906e592",
  "symbol": "ETHE",
  "asset_class": "us_equity",
  
  "qty": 10,
  "filled_qty": 8,
  "filled_avg_price": 2450.50,
  
  "order_class": "simple",
  "order_type": "limit",
  "type": "limit",
  
  "side": "buy",
  "time_in_force": "day",
  "limit_price": 2450.00,
  "stop_price": null,
  "trail_price": null,
  "trail_percent": null,
  
  "extended_hours": false,
  "legs": null,
  "status": "partially_filled",
  
  "commission": 0,
  "legs": null,
  "source": "welltrade"
}
```

---

## 🔍 EXPLICACIÓN DE CADA CAMPO

### IDENTIFICADORES

#### `id`
```
¿QUÉ ES? UUID único de la orden en Alpaca
EJEMPLO: "12345678-1234-1234-1234-123456789012"
USO: Referencia interna de Alpaca
IMPORTANTE: Guardarlo para reconciliación
```

#### `client_order_id`
```
¿QUÉ ES? ID que TÚ asignas (nosotros lo hacemos)
FORMATO: "BATCH_6_ETHE_1711123200"
│         └─ Batch ID
│            └─ Symbol
│               └─ Timestamp Unix

USO: Conectar tu sistema con Alpaca
VENTAJA: Identificar órdenes por batch
IMPORTANTE: El que usamos para tracking
```

#### `symbol`
```
¿QUÉ ES? El asset que se está comprando/vendiendo
VALORES NUESTROS:
├─ ETHE (Ethereum ETF)
├─ GBTC (Bitcoin ETF)
├─ FXA (Dólar Australiano)
└─ EUUSD (Euro - problemático)

USO: Identificar qué se compró
```

---

### PRECIO & ENTRADA

#### `limit_price`
```
¿QUÉ ES? El precio máximo que pagamos por la orden
EJEMPLO: 2450.00 (por ETHE)

CÓMO FUNCIONA:
├─ Si precio actual < limit_price → SE LLENA INMEDIATAMENTE
├─ Si precio actual > limit_price → QUEDAN PENDIENTE
└─ Si precio cae a limit_price → SE LLENA

ENTRY POINT EXPLICADO:
├─ Nosotros decimos: "Compra ETHE máximo a 2450"
├─ Market price ahora: 2460
├─ → Orden PEND, esperando que caiga a 2450
├─ Si cae a 2450 → SE LLENA a 2450
├─ Si sube → No se llena nunca

FÓRMULA NUESTRO:
entry_price = current_price × (1 - stagger%)
└─ Ejemplo: 2500 × (1 - 0.02) = 2450
```

#### `filled_avg_price`
```
¿QUÉ ES? Precio promedio al que se llenó la orden
EJEMPLO: 2450.50 (vs limit_price 2450.00)

INTERPRETACIÓN:
├─ Si filled_avg_price < limit_price → Excelente entrada ✓
├─ Si filled_avg_price = limit_price → Entrada OK ➳
├─ Si filled_avg_price > limit_price → Mejor entrada que esperado ❌

EN NUESTRO CASO:
├─ Limit: 2450
├─ Filled: 2450.50
└─ Interpretación: Se llenó un poco arriba (mercado subió mientras se procesaba)
```

#### `current_price` vs `entry_price` vs `limit_price`

```
DIFERENCIAS IMPORTANTES:

CURRENT PRICE (Precio de mercado AHORA):
├─ Precio al que se puede comprar/vender AHORA
├─ En tiempo real, cambia constantemente
├─ Lo que ves en Yahoo Finance, Bloomberg, etc.
└─ EJEMPLO: $2,460 para ETHE

LIMIT_PRICE (Precio de la orden):
├─ Precio máximo que estamos dispuestos a pagar
├─ LO QUE NOSOTROS ESPECIFICAMOS
├─ Si current > limit → orden queda pendiente
└─ EJEMPLO: "Compra máximo a $2,450"

ENTRY_PRICE (Precio de entrada que calculamos):
├─ Lo que esperamos que sea filled_price
├─ Lo calculamos NOSOTROS antes de hacer orden
├─ Basado en stagger (% por debajo de current)
└─ EJEMPLO: current=$2,460 - 2% stagger = $2,450

FILLED_AVG_PRICE (Precio real al que se llenó):
├─ Lo que REALMENTE pagamos
├─ Puede variar ligeramente de limit_price
├─ Si mercado se movió mientras se llenaba
└─ EJEMPLO: Se llenó a $2,450.50 (no exacto 2,450)
```

---

### CANTIDAD

#### `qty`
```
¿QUÉ ES? Cantidad de acciones/shares que pedimos
EJEMPLO: 10 shares de ETHE

EN BATCH 6:
├─ ~15 órdenes por onda
├─ Cada orden: x shares (depende del símbolo)
└─ Total: 120 órdenes x múltiples shares

CÁLCULO:
qty = (total_orders / num_symbols) × symbol_allocation
└─ ETHE (50%): qty más alto
└─ GBTC (40%): qty medio
└─ FXA (10%): qty más bajo
```

#### `filled_qty`
```
¿QUÉ ES? Cantidad de acciones que REALMENTE se llenaron
EJEMPLO: 8 de 10 (solo 80% llenado)

INTERPRETACIONES:
├─ filled_qty = qty → TOTALMENTE LLENADA ✓
├─ filled_qty < qty → PARCIALMENTE LLENADA ⚠️
├─ filled_qty = 0 → SIN LLENAR ✗

CAUSAS DE LLENADO PARCIAL:
├─ Mercado no bajó lo suficiente
├─ Orden expiró (end of day)
├─ Cancelada manualmente
├─ Mercado dividido (múltiples rellenos)
```

---

### ESTADO

#### `status`
```
POSIBLES VALORES:

1. "pending_new"
   ├─ Acaba de ser enviada
   ├─ Alpaca aún procesando
   └─ Durará < 1 segundo (normal)

2. "accepted"
   ├─ Alpaca aceptó la orden
   ├─ En camino al mercado
   └─ Durará segundos

3. "partially_filled"
   ├─ Se llenó PARTE solamente
   ├─ filled_qty < qty
   ├─ Ejemplo: Pidamos 10, se llenaron 8
   └─ MÁS COMÚN EN ÓRDENES DE BAJO VOLUMEN

4. "filled"
   ├─ 100% LLENADA
   ├─ filled_qty = qty
   ├─ Se puede cerrar/vender
   └─ ESTADO IDEAL NUESTRO

5. "done_for_day"
   ├─ No se llenó antes de EOD
   ├─ Fue cancelada automáticamente
   ├─ time_in_force: "day" hizo esto
   └─ APRENDIZAJE: Revisamos porqué no se llenó

6. "canceled"
   ├─ Cancelada manualmente
   ├─ O por otro razón
   └─ No se llenó en absoluto

7. "expired"
   ├─ Orden expiró (muy raro en nuestro setup)
   └─ No se llenó

8. "replaced"
   ├─ Fue reemplazada por nueva orden
   ├─ Nosotros no hacemos esto
   └─ Raro

9. "pending_cancel"
   ├─ Cancelación en progreso
   └─ Durará segundos

10. "rejected"
    ├─ Alpaca rechazó la orden
    ├─ Razones: Símbolo inválido, qty cero, etc.
    └─ ERROR - Revisar
```

#### `time_in_force`
```
¿QUÉ ES? Cuánto tiempo la orden es válida

NUESTRO VALOR: "day"
├─ Válida por todo el DÍA DE TRADING
├─ Si no se llena → Auto-cancela al cierre de mercado (16:00 EDT)
├─ Perfecta para swing trading
└─ Evita órdenes fantasma al día siguiente

OTROS VALORES (NO USAMOS):
├─ "gtc" (Good Till Canceled) - espera días
├─ "opg" (At Open) - solo apertura
├─ "ioc" (Immediate or Cancel) - rápido
```

---

### TIPO DE ORDEN

#### `order_type` / `type`
```
NUESTRO VALOR: "limit"

¿QUÉ ES?
├─ Especificamos PRECIO MÁXIMO
├─ Alpaca intenta llenar a ese precio o MEJOR
├─ Si no puede → queda pendiente
└─ VENTAJA: Control de precio

OTROS TIPOS (NO USAMOS):
├─ "market" - compra al precio actual (riesgo)
├─ "stop" - Trigger cuando precio cae
├─ "stop_limit" - Combinado
```

#### `side`
```
NUESTRO VALOR: "buy" (siempre compramos)

¿QUÉ ES?
├─ "buy" = Compramos
├─ "sell" = Vendemos
└─ NUESTRO SETUP: Solo buy (paper trading, long-only)
```

---

### TIEMPOS

#### `created_at`
```
¿QUÉ ES? Cuándo creamos la orden
FORMATO: ISO 8601 (2026-03-19T21:00:00Z)
PRECISIÓN: Al segundo
IMPORTANTE: Primer timestamp de la orden
```

#### `submitted_at`
```
¿QUÉ ES? Cuándo la enviamos a Alpaca
TÍPICAMENTE: Casi igual a created_at
DIFERENCIA: < 1 segundo normal
```

#### `filled_at`
```
¿QUÉ ES? Cuándo se llenó la orden
VACÍO (null): Si no se llenó
CON VALOR: Se llenó a esa hora exacta

IMPORTANTE PARA APRENDIZAJE:
├─ Diferencia entre created_at y filled_at = TIEMPO HASTA LLENAR
├─ Ejemplo: Creada 21:00:00, llenada 21:00:02 = 2 segundos
├─ Si > 30 seg = entrada no tan agresiva (menos demanda)
```

#### `canceled_at`
```
¿QUÉ ES? Cuándo se canceló
VACÍO (null): Si no se canceló
CON VALOR: Cancelada a esa hora
RAZONES: EOD, manual, rechaza, etc.
```

---

## 📈 EJEMPLOS REALES DEL BATCH 5

### Ejemplo 1: ORDEN PERFECTA (100% LLENADA)

```json
{
  "client_order_id": "BATCH_5_ETHE_1711100000",
  "symbol": "ETHE",
  "qty": 10,
  "filled_qty": 10,
  "filled_avg_price": 2450.25,
  "limit_price": 2450.00,
  "status": "filled",
  "created_at": "2026-03-19T15:00:00Z",
  "filled_at": "2026-03-19T15:00:02Z",
  "side": "buy",
  "time_in_force": "day"
}

INTERPRETACIÓN:
├─ ✓ Status: "filled" (perfecta)
├─ ✓ filled_qty (10) = qty (10) (100%)
├─ ✓ filled_avg_price (2450.25) ≈ limit_price (2450)
├─ ✓ Tiempo: 2 segundos hasta llenar (demanda fuerte)
├─ ✓ Entry exitosa
└─ RESULTADO: Este fue UN ÉXITO ✓
```

### Ejemplo 2: ORDEN PARCIALMENTE LLENADA

```json
{
  "client_order_id": "BATCH_5_FXA_1711100090",
  "symbol": "FXA",
  "qty": 15,
  "filled_qty": 5,
  "filled_avg_price": 65.80,
  "limit_price": 65.75,
  "status": "partially_filled",
  "created_at": "2026-03-19T15:01:30Z",
  "filled_at": "2026-03-19T15:01:35Z",
  "canceled_at": "2026-03-19T16:00:00Z",
  "side": "buy",
  "time_in_force": "day"
}

INTERPRETACIÓN:
├─ ⚠️ Status: "partially_filled" (solo 33%)
├─ ⚠️ filled_qty (5) << qty (15) (66% NO SE LLENÓ)
├─ ⚠️ filled_avg_price (65.80) > limit_price (65.75) (menos demanda)
├─ ⚠️ Se llenó 5 segundos, luego esperó hasta EOD
├─ ❌ Cancelada al cierre (16:00) sin llenar resto
└─ APRENDIZAJE: FXA spread más grande, menos líquido
```

### Ejemplo 3: ORDEN SIN LLENAR

```json
{
  "client_order_id": "BATCH_5_GLD_1711100200",
  "symbol": "GLD",
  "qty": 20,
  "filled_qty": 0,
  "filled_avg_price": null,
  "limit_price": 180.00,
  "status": "done_for_day",
  "created_at": "2026-03-19T15:02:00Z",
  "filled_at": null,
  "canceled_at": "2026-03-19T16:00:00Z",
  "side": "buy",
  "time_in_force": "day"
}

INTERPRETACIÓN:
├─ ❌ Status: "done_for_day" (NO se llenó)
├─ ❌ filled_qty (0) = 0% LLENADA
├─ ❌ filled_avg_price: null (nunca se llenó)
├─ ❌ Mercado nunca bajó a 2450
├─ ❌ Cancelada EOD sin resultados
└─ APRENDIZAJE: GLD muy bajo volumen, NO USAR
```

---

## 🎯 RESUMEN: CÓMO INTERPRETAMOS LOGS

### Para aprender RÁPIDO:

```
PASO 1: Ver STATUS
├─ "filled" → ✓ Se llenó perfecto
├─ "partially_filled" → ⚠️ Revisar porqué
└─ "done_for_day" → ❌ Símbolo no bueno

PASO 2: Comparar FILLED vs QTY
├─ filled_qty = qty → Excelente
├─ filled_qty > 50% qty → OK
├─ filled_qty < 50% qty → Problema
└─ filled_qty = 0 → No usar símbolo

PASO 3: Ver FILLED_AVG_PRICE vs LIMIT_PRICE
├─ filled_avg_price < limit_price → Mejor entrada
├─ filled_avg_price ≈ limit_price → OK
└─ diferencia > 0.5% → Revisar spreads

PASO 4: TIEMPO hasta llenado
├─ < 5 segundos → Demanda fuerte
├─ 5-30 segundos → Normal
└─ > 30 segundos → Weak entry, no llenar luego
```

---

## 🍑 EN BATCH 6:

Cada 30 minutos vamos a revisar:
1. Symbol fill rates
2. Órdenes que NO se llenaron (aprender porqué)
3. Entry prices (qué símbolos se llenan mejor)
4. YouTube research (aplicar hallazgos)
5. Ajustes para Batch 7

**TODO BASADO EN ENTENDER ESTOS LOGS.** 📊
