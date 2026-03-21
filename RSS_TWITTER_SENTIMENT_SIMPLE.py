#!/usr/bin/env python3
"""
RSS TWITTER SENTIMENT LIVE - NO EXTERNAL DEPENDENCIES
Pure Python implementation for free sentiment analysis
Uses requests (built-in via urllib) + manual RSS parsing
"""

import urllib.request
import xml.etree.ElementTree as ET
import json
from datetime import datetime
from collections import Counter
import re

class RSSTwitterSentimentRadar:
    def __init__(self):
        """Initialize with RSS feeds (no external libraries needed)"""
        
        self.feeds = {
            # Public RSS feeds with crypto/market data
            "CoinDesk": "https://feeds.coindesk.com/news",
            "Bloomberg Crypto": "https://feeds.bloomberg.com/markets/cryptocurrency.rss",
            "Cointelegraph": "https://cointelegraph.com/feed",
            "The Block": "https://www.theblockcrypto.com/feed",
        }
        
        self.bullish_keywords = [
            "buy", "long", "bullish", "pump", "moon", "bull", 
            "breakout", "surge", "spike", "rally", "recovery",
            "accumulate", "dip", "discount", "opportunity", "rise",
            "gain", "growth", "jump"
        ]
        
        self.bearish_keywords = [
            "sell", "short", "bearish", "dump", "crash", "collapse",
            "drop", "decline", "downtrend", "pullback", "loss",
            "liquidation", "negative", "fear", "warning", "fall",
            "plunge", "decline", "loss"
        ]
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of text (no external libraries)"""
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
    
    def fetch_rss_feed(self, url):
        """Fetch and parse RSS feed using only standard library"""
        items = []
        
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                content = response.read()
                root = ET.fromstring(content)
                
                # Parse RSS items
                for item in root.findall(".//item"):
                    title_elem = item.find("title")
                    desc_elem = item.find("description")
                    link_elem = item.find("link")
                    pubdate_elem = item.find("pubDate")
                    
                    title = title_elem.text if title_elem is not None else ""
                    description = desc_elem.text if desc_elem is not None else ""
                    link = link_elem.text if link_elem is not None else ""
                    pubdate = pubdate_elem.text if pubdate_elem is not None else ""
                    
                    # Clean HTML from description
                    description = re.sub(r'<[^>]+>', '', description)
                    
                    if title:
                        items.append({
                            "title": title,
                            "description": description,
                            "link": link,
                            "pubdate": pubdate
                        })
            
            return items
        
        except Exception as e:
            return []
    
    def fetch_all_feeds(self):
        """Fetch all RSS feeds"""
        all_items = []
        feed_status = {}
        
        print(f"\n[{self._get_ts()}] 📡 FETCHING RSS FEEDS (NO API KEYS NEEDED):")
        
        for feed_name, feed_url in self.feeds.items():
            try:
                items = self.fetch_rss_feed(feed_url)
                
                if items:
                    print(f"  ✓ {feed_name}: {len(items)} items fetched")
                    feed_status[feed_name] = "✓"
                    
                    for item in items[:20]:  # Take latest 20 from each
                        combined_text = f"{item['title']} {item['description']}"
                        sentiment = self.analyze_sentiment(combined_text)
                        
                        all_items.append({
                            "source": feed_name,
                            "title": item['title'],
                            "sentiment": sentiment,
                            "link": item['link']
                        })
                else:
                    print(f"  ⚠ {feed_name}: Empty or timeout")
                    feed_status[feed_name] = "empty"
            
            except Exception as e:
                print(f"  ❌ {feed_name}: {str(e)[:40]}")
                feed_status[feed_name] = "error"
        
        return all_items, feed_status
    
    def calculate_market_consensus(self, items):
        """Calculate overall market sentiment"""
        
        if not items:
            return {
                "sentiment": "NEUTRAL",
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
            overall = "🔴 BEARISH"
        elif bullish > bearish:
            overall = "🟢 BULLISH"
        else:
            overall = "🟡 NEUTRAL"
        
        # Calculate confidence
        max_count = max(bullish, bearish, neutral)
        confidence = int((max_count / total) * 100) if total > 0 else 0
        
        return {
            "sentiment": overall,
            "bullish_count": bullish,
            "bearish_count": bearish,
            "neutral_count": neutral,
            "total_items": total,
            "confidence": confidence,
            "ratio": f"{bullish}B:{bearish}Be:{neutral}N"
        }
    
    def get_top_signals(self, items, count=5):
        """Get top signals"""
        
        bullish_items = [i for i in items if i["sentiment"] == "bullish"]
        bearish_items = [i for i in items if i["sentiment"] == "bearish"]
        
        return {
            "top_bullish": bullish_items[:count],
            "top_bearish": bearish_items[:count]
        }
    
    def _get_ts(self):
        return datetime.now().strftime("%H:%M:%S")
    
    def run_full_analysis(self):
        """Run complete analysis"""
        
        print("\n" + "="*70)
        print("🔄 RSS TWITTER SENTIMENT RADAR - LIVE (NO API KEYS NEEDED)")
        print("="*70)
        print("✓ Using public RSS feeds (100% FREE)")
        print("✓ No API restrictions")
        print("✓ No rate limits")
        print("✓ Real-time data")
        
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

def print_results(results):
    """Pretty print results"""
    
    consensus = results["consensus"]
    ts = datetime.now().strftime("%H:%M:%S")
    
    print(f"\n[{ts}] 📊 MARKET CONSENSUS FROM RSS FEEDS:")
    print(f"  Sentiment: {consensus['sentiment']}")
    print(f"  Confidence: {consensus['confidence']}%")
    print(f"  Bullish: {consensus['bullish_count']}")
    print(f"  Bearish: {consensus['bearish_count']}")
    print(f"  Neutral: {consensus['neutral_count']}")
    print(f"  Total items: {consensus['total_items']}")
    print(f"  Ratio: {consensus['ratio']}")
    
    print(f"\n[{ts}] 📈 TOP BULLISH SIGNALS:")
    for i, signal in enumerate(results['top_signals']['top_bullish'][:3], 1):
        print(f"  {i}. {signal['source']}: {signal['title'][:60]}...")
    
    print(f"\n[{ts}] 📉 TOP BEARISH SIGNALS:")
    for i, signal in enumerate(results['top_signals']['top_bearish'][:3], 1):
        print(f"  {i}. {signal['source']}: {signal['title'][:60]}...")
    
    # Trading recommendation
    sentiment = consensus['sentiment']
    if "BEARISH" in sentiment:
        print(f"\n🔴 TRADING DECISION: SHORT MODE")
        print(f"   ├─ Deploy SHORT orders")
        print(f"   ├─ Add DCA buys on dips")
        print(f"   └─ Exit at +2-3% target")
    elif "BULLISH" in sentiment:
        print(f"\n🟢 TRADING DECISION: BUY MODE")
        print(f"   ├─ Deploy BUY orders")
        print(f"   ├─ Scale with momentum")
        print(f"   └─ Exit at +3-4% target")
    else:
        print(f"\n🟡 TRADING DECISION: DCA MODE")
        print(f"   ├─ Deploy balanced DCA")
        print(f"   ├─ Mix buys + shorts")
        print(f"   └─ Exit at +2-3% target")
    
    print("\n" + "="*70)
    print("💾 Results saved to: rss_sentiment_latest.json")
    print("="*70)

def main():
    """Main execution"""
    
    radar = RSSTwitterSentimentRadar()
    results, items = radar.run_full_analysis()
    
    print_results(results)
    
    # Save results for integration with trading system
    with open("rss_sentiment_latest.json", "w") as f:
        json.dump(results, f, indent=2)
    
    return results

if __name__ == "__main__":
    main()
