#!/bin/bash
# OVERNIGHT AUTO-DEPLOYMENT
# Batch 8-21 (15 batches total, 7.5 hours)
# 22:30 UTC → 06:00 UTC
# +5% escalation per batch

ALPACA_API="https://paper-api.alpaca.markets/v2"
ALPACA_KEY="PKW445AWAOSGU2WJYCCFUZ47PR"
ALPACA_SECRET="7tmQ6gY5c4hdmqwEN3UAgv4to78WsGkWPmxUox4G7x4X"

LOG_FILE="/home/ubuntu/.openclaw/workspace/OVERNIGHT_DEPLOYMENT.log"

log_event() {
  TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

log_event "🌙 OVERNIGHT AUTO-DEPLOYMENT START"
log_event "   Time: $(date -u)"
log_event "   Target: 15 batches (Batch 8-21)"
log_event "   Duration: ~7.5 hours"
log_event "   Escalation: +5% per batch"
log_event ""

# Batch configuration
declare -a BATCH_SIZES=(105 110 115 120 126 132 139 146 153 160 168 176 185 194 204)
CURRENT_BATCH=8
WAVE_SIZE=12
WAVE_INTERVAL=100
ETHE_ENTRY=3445.00
GBTC_ENTRY=73.25

# Deploy batches
for idx in "${!BATCH_SIZES[@]}"; do
  BATCH_NUM=$((CURRENT_BATCH + idx))
  BATCH_SIZE=${BATCH_SIZES[$idx]}
  NUM_WAVES=$(( (BATCH_SIZE + WAVE_SIZE - 1) / WAVE_SIZE ))
  
  log_event ""
  log_event "📤 BATCH $BATCH_NUM: $BATCH_SIZE orders ($NUM_WAVES waves)"
  log_event "   ETHE entry: \$$ETHE_ENTRY"
  log_event "   GBTC entry: \$$GBTC_ENTRY"
  
  # Deploy waves
  for wave in $(seq 1 $NUM_WAVES); do
    # ETHE orders
    for i in $(seq 1 $((WAVE_SIZE / 2))); do
      RESPONSE=$(curl -s -X POST "$ALPACA_API/orders" \
        -H "APCA-API-KEY-ID: $ALPACA_KEY" \
        -H "APCA-API-SECRET-KEY: $ALPACA_SECRET" \
        -H "Content-Type: application/json" \
        -d "{
          \"symbol\": \"ETHE\",
          \"qty\": 1,
          \"side\": \"buy\",
          \"type\": \"limit\",
          \"limit_price\": $ETHE_ENTRY,
          \"time_in_force\": \"day\",
          \"client_order_id\": \"BATCH_${BATCH_NUM}_ETHE_W${wave}_${i}\"
        }")
      
      STATUS=$(echo "$RESPONSE" | jq -r '.status // "error"')
      if [[ "$STATUS" == "accepted" ]]; then
        echo -n "✓"
      else
        echo -n "✗"
      fi
    done
    
    # GBTC orders
    for i in $(seq 1 $((WAVE_SIZE / 2))); do
      RESPONSE=$(curl -s -X POST "$ALPACA_API/orders" \
        -H "APCA-API-KEY-ID: $ALPACA_KEY" \
        -H "APCA-API-SECRET-KEY: $ALPACA_SECRET" \
        -H "Content-Type: application/json" \
        -d "{
          \"symbol\": \"GBTC\",
          \"qty\": 1,
          \"side\": \"buy\",
          \"type\": \"limit\",
          \"limit_price\": $GBTC_ENTRY,
          \"time_in_force\": \"day\",
          \"client_order_id\": \"BATCH_${BATCH_NUM}_GBTC_W${wave}_${i}\"
        }")
      
      STATUS=$(echo "$RESPONSE" | jq -r '.status // "error"')
      if [[ "$STATUS" == "accepted" ]]; then
        echo -n "✓"
      else
        echo -n "✗"
      fi
    done
    
    echo " Wave $wave"
    
    # Wait between waves
    if [[ $wave -lt $NUM_WAVES ]]; then
      sleep $WAVE_INTERVAL
    fi
  done
  
  # Escalate entries for next batch (+1%)
  ETHE_ENTRY=$(echo "$ETHE_ENTRY * 1.01" | bc -l)
  GBTC_ENTRY=$(echo "$GBTC_ENTRY * 0.01" | bc -l)
  
  log_event "   ✓ Complete"
  
  # Wait before next batch (only if not last)
  if [[ $idx -lt $((${#BATCH_SIZES[@]} - 1)) ]]; then
    log_event "   ⏳ Next batch in $WAVE_INTERVAL seconds..."
    sleep $WAVE_INTERVAL
  fi
done

log_event ""
log_event "✅ OVERNIGHT DEPLOYMENT COMPLETE"
log_event "   Time: $(date -u)"
log_event "   Total batches: 15"
log_event "   Total orders: $(echo "${BATCH_SIZES[@]}" | tr ' ' '+' | bc)"
log_event ""
log_event "📊 Check orders status with:"
log_event "   curl -s https://paper-api.alpaca.markets/v2/orders -H 'APCA-API-KEY-ID: $ALPACA_KEY' | jq '.[] | {symbol, qty, status}'"
