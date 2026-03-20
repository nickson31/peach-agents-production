#!/bin/bash
# TODAY AUTO-DEPLOYMENT - $40K TARGET
# Batch 1-8 (8 batches total, 2 hours)
# 11:40 UTC → 13:55 UTC
# SHORT_AGGRESSIVE strategy (Bearish market)
# Every 15 minutes

ALPACA_API="https://paper-api.alpaca.markets/v2"
ALPACA_KEY="PKW445AWAOSGU2WJYCCFUZ47PR"
ALPACA_SECRET="7tmQ6gY5c4hdmqwEN3UAgv4to78WsGkWPmxUox4G7x4X"

LOG_FILE="/home/ubuntu/.openclaw/workspace/TODAY_DEPLOYMENT_40K.log"

log_event() {
  TIMESTAMP=$(date -u +"%H:%M:%S UTC")
  echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

log_event "🚀 TODAY AUTO-DEPLOYMENT START - $40K TARGET"
log_event "   Time: $(date -u)"
log_event "   Target: 8 batches"
log_event "   Duration: ~2 hours"
log_event "   Interval: Every 15 minutes"
log_event "   Strategy: SHORT_AGGRESSIVE (Bearish)"
log_event ""

# Batch configuration
declare -a BATCH_SIZES=(200 210 220 230 240 250 260 270)
CURRENT_BATCH=1
WAVE_SIZE=20
WAVE_INTERVAL=3
ETHE_ENTRY=3445.00

# Deploy batches
for idx in "${!BATCH_SIZES[@]}"; do
  BATCH_NUM=$((CURRENT_BATCH + idx))
  BATCH_SIZE=${BATCH_SIZES[$idx]}
  NUM_WAVES=$(( (BATCH_SIZE + WAVE_SIZE - 1) / WAVE_SIZE ))
  
  log_event ""
  log_event "📤 BATCH $BATCH_NUM: $BATCH_SIZE orders ($NUM_WAVES waves)"
  log_event "   Strategy: SHORT_AGGRESSIVE"
  log_event "   ETHE entry: \$$ETHE_ENTRY"
  
  SUCCESSFUL=0
  FAILED=0
  
  # Deploy waves
  for wave in $(seq 1 $NUM_WAVES); do
    # SHORT orders (66% of batch)
    SHORT_COUNT=$((BATCH_SIZE * 66 / 100 / NUM_WAVES))
    for i in $(seq 1 $SHORT_COUNT); do
      RESPONSE=$(curl -s -X POST "$ALPACA_API/orders" \
        -H "APCA-API-KEY-ID: $ALPACA_KEY" \
        -H "APCA-API-SECRET-KEY: $ALPACA_SECRET" \
        -H "Content-Type: application/json" \
        -d "{
          \"symbol\": \"ETHE\",
          \"qty\": 1,
          \"side\": \"sell\",
          \"type\": \"market\",
          \"time_in_force\": \"day\",
          \"client_order_id\": \"BATCH_${BATCH_NUM}_SHORT_W${wave}_${i}\"
        }")
      
      STATUS=$(echo "$RESPONSE" | jq -r '.status // "error"' 2>/dev/null)
      if [[ "$STATUS" == "accepted" ]] || [[ "$STATUS" == "pending_new" ]]; then
        echo -n "✓"
        ((SUCCESSFUL++))
      else
        echo -n "✗"
        ((FAILED++))
      fi
    done
    
    # BUY orders (34% of batch - DCA)
    BUY_COUNT=$((BATCH_SIZE * 34 / 100 / NUM_WAVES))
    for i in $(seq 1 $BUY_COUNT); do
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
          \"client_order_id\": \"BATCH_${BATCH_NUM}_BUY_W${wave}_${i}\"
        }")
      
      STATUS=$(echo "$RESPONSE" | jq -r '.status // "error"' 2>/dev/null)
      if [[ "$STATUS" == "accepted" ]] || [[ "$STATUS" == "pending_new" ]]; then
        echo -n "✓"
        ((SUCCESSFUL++))
      else
        echo -n "✗"
        ((FAILED++))
      fi
    done
    
    echo " Wave $wave"
    
    # Wait between waves
    if [[ $wave -lt $NUM_WAVES ]]; then
      sleep $WAVE_INTERVAL
    fi
  done
  
  log_event "   ✓ Successful: $SUCCESSFUL | Failed: $FAILED"
  
  # Get account status
  ACCOUNT=$(curl -s "$ALPACA_API/account" \
    -H "APCA-API-KEY-ID: $ALPACA_KEY" \
    -H "APCA-API-SECRET-KEY: $ALPACA_SECRET")
  
  EQUITY=$(echo "$ACCOUNT" | jq -r '.equity // "N/A"')
  BP=$(echo "$ACCOUNT" | jq -r '.buying_power // "N/A"')
  
  log_event "   Account: Equity=$EQUITY | BP=$BP"
  
  # Escalate entry for next batch
  ETHE_ENTRY=$(echo "$ETHE_ENTRY * 0.99" | bc -l)
  
  # Wait 15 minutes before next batch (only if not last)
  if [[ $idx -lt $((${#BATCH_SIZES[@]} - 1)) ]]; then
    log_event "   ⏳ Next batch in 15 minutes..."
    sleep 900
  fi
done

log_event ""
log_event "✅ TODAY DEPLOYMENT COMPLETE"
log_event "   Time: $(date -u)"
log_event "   Total batches: 8"
log_event "   Total orders: $(echo "${BATCH_SIZES[@]}" | tr ' ' '+' | bc)"
log_event ""
