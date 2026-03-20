#!/usr/bin/env python3
"""
RESEARCH AGENT: Signal Extractor
Extracts trading signals from YouTube transcripts
"""

import re
from typing import List, Dict, Any

class SignalExtractor:
    """Extract trading signals from transcript text"""
    
    ENTRY_KEYWORDS = [
        r"buy at|long entry|go long|buy|entry price is|support at",
        r"comprar en|entrada en|nivel de entrada"
    ]
    
    EXIT_KEYWORDS = [
        r"take profit at|target|exit|sell at|profit target",
        r"tomar ganancias en|objetivo|salida"
    ]
    
    STOP_KEYWORDS = [
        r"stop loss|sl|break below|below",
        r"stop en|pérdida máxima"
    ]
    
    SYMBOL_PATTERN = r"\$?([A-Z]{1,6})\b|BTC|ETH|EUR|GBP|USD"
    PRICE_PATTERN = r"\$?([\d,]+\.?\d*)"
    TIMEFRAME_PATTERN = r"(1m|5m|15m|30m|1h|4h|daily|weekly|monthly)"
    
    def extract_signals(self, transcript: str, video_metadata: Dict[str, Any]) -> List[Dict]:
        """Extract trading signals from transcript"""
        
        signals = []
        
        # Split transcript into chunks (roughly paragraph-level)
        chunks = transcript.split('\n\n')
        
        for chunk in chunks:
            if self._has_trading_content(chunk):
                signal = self._parse_chunk(chunk, video_metadata)
                if signal:
                    signals.append(signal)
        
        return signals
    
    def _has_trading_content(self, text: str) -> bool:
        """Check if chunk contains trading-related keywords"""
        trading_keywords = [
            'buy', 'sell', 'entry', 'exit', 'target', 'stop loss',
            'long', 'short', 'support', 'resistance', 'price',
            'compra', 'venta', 'entrada', 'salida', 'objetivo'
        ]
        return any(kw.lower() in text.lower() for kw in trading_keywords)
    
    def _parse_chunk(self, chunk: str, metadata: Dict) -> Dict or None:
        """Parse a chunk of text for signal"""
        
        # Find entry price
        entry = self._extract_price(chunk, self.ENTRY_KEYWORDS)
        if not entry:
            return None
        
        # Find exit/target
        exit_price = self._extract_price(chunk, self.EXIT_KEYWORDS)
        
        # Find stop loss
        stop_loss = self._extract_price(chunk, self.STOP_KEYWORDS)
        
        # Find symbol
        symbol = self._extract_symbol(chunk)
        if not symbol:
            return None
        
        # Find timeframe
        timeframe = self._extract_timeframe(chunk)
        
        return {
            'symbol': symbol,
            'entry': entry,
            'exit': exit_price,
            'stop_loss': stop_loss,
            'timeframe': timeframe or '4h',
            'source': metadata.get('video_url'),
            'creator': metadata.get('creator'),
            'timestamp': metadata.get('timestamp'),
            'confidence': self._calculate_confidence(chunk, entry, exit_price)
        }
    
    def _extract_price(self, text: str, keywords: List[str]) -> float or None:
        """Extract price from text using keywords"""
        for keyword in keywords:
            match = re.search(f"{keyword}.*?({self.PRICE_PATTERN})", text, re.IGNORECASE)
            if match:
                try:
                    price_str = match.group(2).replace(',', '')
                    return float(price_str)
                except:
                    pass
        return None
    
    def _extract_symbol(self, text: str) -> str or None:
        """Extract symbol from text"""
        match = re.search(self.SYMBOL_PATTERN, text, re.IGNORECASE)
        if match:
            return match.group(1).upper()
        return None
    
    def _extract_timeframe(self, text: str) -> str or None:
        """Extract timeframe from text"""
        match = re.search(self.TIMEFRAME_PATTERN, text, re.IGNORECASE)
        if match:
            return match.group(1).lower()
        return None
    
    def _calculate_confidence(self, text: str, entry: float, exit_price: float) -> int:
        """Calculate confidence score (0-100)"""
        
        confidence = 50  # Base
        
        # Check for specific keywords
        strong_keywords = ['strong', 'setup', 'high probability', 'key level']
        if any(kw in text.lower() for kw in strong_keywords):
            confidence += 15
        
        # Check for historical context
        if 'last time' in text.lower() or 'previously' in text.lower():
            confidence += 10
        
        # Check for multiple confirmations
        if text.count('entry') > 1 or text.count('target') > 1:
            confidence += 10
        
        # Check entry/exit ratio
        if entry and exit_price:
            ratio = exit_price / entry
            if 1.02 < ratio < 1.06:  # 2-6% target
                confidence += 10
        
        return min(confidence, 100)
