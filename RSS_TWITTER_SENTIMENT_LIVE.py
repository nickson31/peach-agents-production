#!/usr/bin/env python3
"""
RSS TWITTER SENTIMENT LIVE - Free real-time crypto sentiment analyzer
Uses RSS feeds (100% FREE) - no API restrictions, no cost
"""

import feedparser
import json
from datetime import datetime
from collections import Counter

class RSSTwitterSentimentRadar:
    def __init__(self):
        """Initialize with popular crypto Twitter RSS feeds"""
        
        self.feeds = {
            # Major crypto accounts
            "Whale Alert": "https://rss.app/feeds/WJb6B9v0zPaEhXy1.xml",  # Big transactions
            "CoinDesk": "https://feeds.coindesk.com/news",  # Crypto news
            "Crypto News": "https://feeds.bloomberg.com/markets/cryptocurrency.rss",
            
            # Popular signals
            "Top Traders": "https://rss.app/feeds/crypto-traders.xml",
            "Market Signals": "https://rss.app/feeds/market-signals.xml",
            
            # Hashtags aggregated
            "ETH Sentiment": "https://rss.app/feeds/ETH-sentiment.xml",
            "Bitcoin": "https://rss.app/feeds/bitcoin-news.xml",
            "Crash Signals": "https://rss.app/feeds/crash-signals.xml",
        }
        
        self.bullish_keywords = [
            "buy", "long", "bullish", "pump", "moon", "bull run", 
            "breakout", "surge", "spike", "rally", "recovery",
            "accumulate", "dip", "discount", "opportunity"
        ]
        
        self.bearish_keywords = [
            "sell", "short", "bearish", "dump", "crash", "collapse",
            "bear", "drop", "dump", "decline", "downtrend", "pullback",
            "liquidation", "red", "negative", "fear", "warning"
        ]
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of text"""
        if not text:
            return "neutral"
        
        text_lower = text.lower()
        
        bearish_count = sum(1 for keyword in self.bearish_keywords if keyword in text_lower)
        bullish_count = sum(1 for keyword in self.bullish_keywords if keyword in text_lower)
        
        if bearish_count > bullish_count:
            return "bearish"
        elif bullish_count > bearish_count:
            return "bullish"
        else:
            return "neutral"
    
    def fetch_all_feeds(self):
        """Fetch and parse all RSS feeds"""
        all_items = []
        feed_status = {}
        
        print(f"\n[{self._get_ts()}] 📡 FETCHING ALL RSS FEEDS:")
        
        for feed_name, feed_url in self.feeds.items():
            try:
                feed = feedparser.parse(feed_url)
                
                if feed.entries:
                    count = len(feed.entries)
                    print(f"  ✓ {feed_name}: {count} items")
                    feed_status[feed_name] = "✓"
                    
                    # Get latest 30 items from this feed
                    for entry in feed.entries[:30]:
                        title = entry.get("title", "")
                        summary = entry.get("summary", "")
                        link = entry.get("link", "")
                        published = entry.get("published", "")
                        
                        combined_text = f"{title} {summary}"
                        sentiment = self.analyze_sentiment(combined_text)
                        
                        all_items.append({
                            "source": feed_name,
                            "title": title,
                            "sentiment": sentiment,
                            "link": link,
                            "timestamp": published
                        })
                else:
                    print(f"  ⚠ {feed_name}: No items")
                    feed_status[feed_name] = "empty"
            
            except Exception as e:
                print(f"  ❌ {feed_name}: Error - {str(e)[:50]}")
                feed_status[feed_name] = "error"
        
        return all_items, feed_status
    
    def calculate_market_consensus(self, items):
        """Calculate overall market sentiment from all items"""
        
        if not items:
            return {
                "sentiment": "neutral",
                "bullish_count": 0,
                "bearish_count": 0,
                "neutral_count": 0,
                "total_items": 0,
                "confidence": 0
            }
        
        sentiments = [item["sentiment"] for item in items]
        sentiment_counts = Counter(sentiments)
        
        bullish = sentiment_counts.get("bullish", 0)
        bearish = sentiment_counts.get("bearish", 0)
        neutral = sentiment_counts.get("neutral", 0)
        total = len(items)
        
        # Determine overall sentiment
        if bearish > bullish:
            overall = "BEARISH"
        elif bullish > bearish:
            overall = "BULLISH"
        else:
            overall = "NEUTRAL"
        
        # Calculate confidence (0-100)
        max_count = max(bullish, bearish, neutral)
        confidence = int((max_count / total) * 100) if total > 0 else 0
        
        return {
            "sentiment": overall,
            "bullish_count": bullish,
            "bearish_count": bearish,
            "neutral_count": neutral,
            "total_items": total,
            "confidence": confidence,
            "ratio": f"{bullish}B:{bearish}Ba:{neutral}N"
        }
    
    def get_top_signals(self, items, count=10):
        """Get top bullish and bearish signals"""
        
        bullish_items = [i for i in items if i["sentiment"] == "bullish"]
        bearish_items = [i for i in items if i["sentiment"] == "bearish"]
        
        return {
            "top_bullish": bullish_items[:count],
            "top_bearish": bearish_items[:count]
        }
    
    def _get_ts(self):
        return datetime.now().strftime("%H:%M:%S")
    
    def run_full_analysis(self):
        """Run complete sentiment analysis and return results"""
        
        print("\n" + "="*70)
        print("🔄 RSS TWITTER SENTIMENT RADAR - LIVE ANALYSIS")
        print("="*70)
        
        # Fetch all feeds
        items, feed_status = self.fetch_all_feeds()
        
        # Calculate consensus
        consensus = self.calculate_market_consensus(items)
        
        # Get top signals
        top_signals = self.get_top_signals(items, count=5)
        
        # Prepare results
        results = {
            "timestamp": datetime.now().isoformat(),
            "consensus": consensus,
            "top_signals": top_signals,
            "feed_status": feed_status,
            "total_items_analyzed": len(items)
        }
        
        return results, items

def print_results(results, items):
    """Pretty print results"""
    
    consensus = results["consensus"]
    ts = datetime.now().strftime("%H:%M:%S")
    
    print(f"\n[{ts}] 📊 MARKET CONSENSUS FROM RSS:")
    print(f"  Overall: {consensus['sentiment']}")
    print(f"  Confidence: {consensus['confidence']}%")
    print(f"  Bullish: {consensus['bullish_count']}")
    print(f"  Bearish: {consensus['bearish_count']}")
    print(f"  Neutral: {consensus['neutral_count']}")
    print(f"  Total analyzed: {consensus['total_items']}")
    print(f"  Ratio: {consensus['ratio']}")
    
    print(f"\n[{ts}] 📈 TOP BULLISH SIGNALS:")
    for i, signal in enumerate(results['top_signals']['top_bullish'][:3], 1):
        print(f"  {i}. {signal['source']}: {signal['title'][:60]}...")
    
    print(f"\n[{ts}] 📉 TOP BEARISH SIGNALS:")
    for i, signal in enumerate(results['top_signals']['top_bearish'][:3], 1):
        print(f"  {i}. {signal['source']}: {signal['title'][:60]}...")
    
    # Decision
    if consensus['sentiment'] == "BEARISH":
        print(f"\n🔴 RECOMMENDATION: SHORT MODE (bearish market)")
        print(f"   Action: Deploy SHORT orders + DCA buys")
    elif consensus['sentiment'] == "BULLISH":
        print(f"\n🟢 RECOMMENDATION: BUY MODE (bullish market)")
        print(f"   Action: Deploy BUY orders")
    else:
        print(f"\n🟡 RECOMMENDATION: DCA MODE (neutral market)")
        print(f"   Action: Deploy balanced DCA")
    
    print("\n" + "="*70)

def main():
    """Main execution"""
    
    radar = RSSTwitterSentimentRadar()
    results, items = radar.run_full_analysis()
    
    print_results(results, items)
    
    # Save results for integration
    with open("rss_sentiment_latest.json", "w") as f:
        json.dump(results, f, indent=2)
    
    return results

if __name__ == "__main__":
    main()
