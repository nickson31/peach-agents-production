# ¿QUÉ SIGNIFICA QUE UNA ORDEN ESTÉ "STUCK" (PARADA)?

## Definición Técnica

**Order Stuck** = Orden que está en estado PENDING (no ejecutada) sin razón técnica clara

### Estados Posibles de una Orden

```
PENDING (Esperando)
├─ Normal: Aguarda match en el mercado (0-5 seg típico)
├─ Partial fill: Se llenó parcialmente, espera resto
└─ ❌ STUCK: Lleva >10 minutos sin llenar = PROBLEMA

FILLED (Ejecutada)
├─ Total: 100% de la orden se ejecutó
└─ Partial: Parte se ejecutó, resto fue cancelado

CANCELED (Cancelada)
└─ Order fue cancelada (manual o timeout)

REJECTED (Rechazada)
└─ El exchange rechazó la orden (invalid price, etc)
```

## Por Qué las Órdenes se Quedan Stuck

### Razón 1: Spreads Demasiado Grandes
```
Example:
- ETHE bid: $3,440
- ETHE ask: $3,450
- Tu orden: BUY @ $3,445 (límite price)
- Market está:
  - Si subió: Tu orden no se llena (stuck porque el market subió)
  - Si bajó: Tu orden se llena (buyer agresivo)

Si spreads amplios: Orden espera MUCHO tiempo
```

### Razón 2: Baja Liquidez
```
Example:
- Quieres comprar 1,000 shares ETHE
- Market tiene solo 100 disponibles @ tu precio
- Parte se llena (100)
- Resto (900) espera eternamente = STUCK
```

### Razón 3: Orden Demasiado Agresiva (Nuestro Caso Hoy)
```
Hoy pasó:
- Lanzamos 100+ órdenes en 30 minutos
- Mercado bajando (vendedores agresivos, compradores pocos)
- Nuestras órdenes: "Queremos comprar @ $3,445"
- Pero el market está @ $3,400 y cayendo
- Órdenes nunca se llenan = STUCK
```

### Razón 4: Error de Alpaca / Red
```
Muy raro, pero posible:
- Orden se queda en limbo
- API no responde
- Genera orden "fantasma"
```

## Timing Crítico: ¿Cuándo Cancelar?

### Opción A: Cancelar Rápido (1 min)
```
Ventaja: Capital libre rápido
Desventaja: Órdenes legítimas se cancelan prematuramente

Caso de uso: Market en crash, necesitas capital
```

### Opción B: Cancelar Normal (5-10 min)
```
Ventaja: Deja tiempo a órdenes buenas a llenarse
Desventaja: Capital bloqueado más tiempo

Caso de uso: Condiciones normales
```

### Opción C: Cancelar Lento (30+ min)
```
Ventaja: Máximo tiempo para llenar
Desventaja: Capital bloqueado demasiado tiempo

Caso de uso: NO RECOMENDADO
```

## Nuestra Configuración Actual

```
ORDER_ANALYZER corre CADA 60 SEGUNDOS

Chequea:
├─ ¿Órdenes > 10 minutos old?
├─ ¿Completamente unfilled (filled_qty = 0)?
└─ SI ambas: CANCEL INMEDIATAMENTE

Resultado:
├─ Capital bloqueado máximo: 10 minutos
├─ BP preservado: Recuperado cada ciclo
└─ Buying power siempre disponible

This es AGGRESSIVE pero CORRECTO para:
- High-frequency deployments (30 min batches)
- Market crashes where liquidity disappears
```

## Ejemplo Real: HOY

```
10:15 UTC: Deploy orden ETHE @ $3,445 (pending)
10:16-10:24 UTC: Orden espera (mercado bajando)
10:25 UTC: ORDER_ANALYZER corre
├─ Order age: 10+ minutos
├─ filled_qty: 0
└─ DECISION: CANCEL

10:26 UTC: Orden cancelada, BP liberado

TIMING: Capital bloqueado solo 10 minutos
        En lugar de 1+ hora
        
RESULTADO: +$300K capital recuperado
```

## Configuración Recomendada (3 opciones)

### OPTION 1: AGGRESSIVE (30-min batches)
```
Cancel timeout: 5 minutos
When: High-frequency trading
Justification: Need capital freed fast for next batch

Risk: Some good orders get canceled early
Benefit: Never starve buying power
```

### OPTION 2: BALANCED (Daily orders)
```
Cancel timeout: 10 minutos
When: Standard swing trading
Justification: Normal time for order to fill

Risk: Some capital blocked 10 min
Benefit: Better fill rates, less cancellations
```

### OPTION 3: CONSERVATIVE (Weekly holds)
```
Cancel timeout: 30+ minutos
When: Long-term investing
Justification: Patient, want fills

Risk: Capital blocked too long
Benefit: Higher fill rates
```

## DECISION REQUIRED

Which timeout should we use?

A) 5 minutes (AGGRESSIVE - for 30-min batches)
B) 10 minutes (BALANCED - for daily orders)
C) Something else?

This changes ORDER_ANALYZER behavior dramatically.
