#!/usr/bin/env python3
"""
AGENT: Order Generator
Generates orders from validated signals and user config
"""

from typing import List, Dict, Any
from datetime import datetime

class OrderGenerator:
    """Generate Alpaca orders from signals"""
    
    def __init__(self, learnings_db: Dict):
        """
        Initialize with learnings database
        learnings_db: Historical performance data
        """
        self.learnings_db = learnings_db
    
    def generate_batch(self, 
                      config: Dict[str, Any], 
                      signals: List[Dict]) -> List[Dict]:
        """
        Generate batch of orders from config and signals
        
        config = {
            'creators': ['ForexMentor'],
            'symbols': {'ETHE': 0.5, 'GBTC': 0.4, 'FXA': 0.1},
            'entry_stagger': {'ETHE': -0.02, 'GBTC': -0.01},
            'batch_size': 100,
            'take_profit': 0.03,
            'stop_loss': -0.01
        }
        """
        
        orders = []
        signals_filtered = self._filter_signals_by_config(signals, config)
        
        # Calculate allocation per symbol
        allocation = self._calculate_allocation(
            signals_filtered, 
            config['symbols'],
            config['batch_size']
        )
        
        # Generate orders
        for symbol, qty in allocation.items():
            for i in range(qty):
                order = self._create_order(
                    symbol,
                    config,
                    signals_filtered
                )
                if order:
                    orders.append(order)
        
        return orders[:config['batch_size']]  # Respect batch size limit
    
    def _filter_signals_by_config(self, signals: List[Dict], config: Dict) -> List[Dict]:
        """Filter signals to match config requirements"""
        
        filtered = []
        
        for signal in signals:
            # Check: Creator in allowed list?
            creator = signal.get('creator')
            if creator not in config.get('creators', []):
                continue
            
            # Check: Symbol in allowed list?
            symbol = signal.get('symbol')
            if symbol not in config.get('symbols', {}):
                continue
            
            # Check: Confidence above threshold?
            if signal.get('confidence', 0) < config.get('min_confidence', 70):
                continue
            
            filtered.append(signal)
        
        return filtered
    
    def _calculate_allocation(self, 
                             signals: List[Dict], 
                             symbol_weights: Dict[str, float],
                             batch_size: int) -> Dict[str, int]:
        """Calculate how many orders per symbol"""
        
        allocation = {}
        
        for symbol, weight in symbol_weights.items():
            qty = int(batch_size * weight)
            allocation[symbol] = max(qty, 1)  # At least 1
        
        return allocation
    
    def _create_order(self, symbol: str, config: Dict, signals: List[Dict]) -> Dict or None:
        """Create single order"""
        
        # Find signal for this symbol
        signal = next((s for s in signals if s['symbol'] == symbol), None)
        if not signal:
            return None
        
        entry_price = signal.get('entry')
        if not entry_price:
            return None
        
        # Get stagger from config
        stagger = config['entry_stagger'].get(symbol, -0.02)
        
        # Calculate entry with stagger
        entry_with_stagger = entry_price * (1 + stagger)
        
        # Calculate exit (take profit)
        take_profit_pct = config.get('take_profit', 0.03)
        exit_price = entry_price * (1 + take_profit_pct)
        
        # Calculate stop loss
        stop_loss_pct = config.get('stop_loss', -0.01)
        stop_loss = entry_price * (1 + stop_loss_pct)
        
        return {
            'symbol': symbol,
            'qty': config.get('order_qty', 12),
            'entry': round(entry_with_stagger, 4),
            'exit': round(exit_price, 4),
            'stop_loss': round(stop_loss, 4),
            'side': 'buy',
            'type': 'limit',
            'time_in_force': 'day',
            'signal_id': signal.get('source'),
            'creator': signal.get('creator'),
            'confidence': signal.get('confidence'),
            'created_at': datetime.now().isoformat()
        }
