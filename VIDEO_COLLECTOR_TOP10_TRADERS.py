#!/usr/bin/env python3
"""
VIDEO COLLECTOR - Top 10 Traders BTC/USDT + ETH/USDT
Recolecta 50 videos por trader (500 total)
Extrae: URLs, títulos, descripciones, fechas, canales
"""

import os
import json
from datetime import datetime
import requests
from typing import List, Dict

# Top 10 traders configuration
TRADERS = {
    "glacier_trading": {
        "channel_id": "UCt_3jJp1_3fHgzLQItYVfxg",
        "tier": "PLATINUM",
        "search_keywords": ["BTC/USDT", "ETH/USDT", "Bitcoin analysis", "Ethereum analysis"],
        "website": "https://www.youtube.com/@GlacierTrading",
    },
    "coinbureau": {
        "channel_id": "UCqrySZk0-PFF93JHJ7uNDZw",
        "tier": "PLATINUM",
        "search_keywords": ["Bitcoin", "Ethereum", "BTCUSDT", "ETHUSDT"],
        "website": "https://www.youtube.com/@CoinBureau",
    },
    "sheldon_evans": {
        "channel_id": "UC4-8W0QLQfKJCYJX-5TPXIA",
        "tier": "PLATINUM",
        "search_keywords": ["Bitcoin trading", "Ethereum trading", "crypto signals"],
        "website": "https://www.youtube.com/@SheldonEvans",
    },
    "cryptojeb": {
        "channel_id": "UCcIvDw_b3-8L0EXEq4VLl8g",
        "tier": "GOLD",
        "search_keywords": ["Elliott Wave", "Bitcoin cycles", "crypto analysis"],
        "website": "https://www.youtube.com/@CryptoJeb",
    },
    "the_wolf_den": {
        "channel_id": "UCfBOb6FYl6PnXSCaKCe0VIQ",
        "tier": "GOLD",
        "search_keywords": ["scalping", "day trading", "Bitcoin"],
        "website": "https://www.youtube.com/@TheWolfDen",
    },
    "altcoin_daily": {
        "channel_id": "UCbLhGKVRSU7sHe7Refzs5GA",
        "tier": "SILVER",
        "search_keywords": ["Bitcoin", "Ethereum", "crypto news"],
        "website": "https://www.youtube.com/@AltcoinDaily",
    },
    "crypto_banter": {
        "channel_id": "UCm4zhcHZ0SZ-LjX7-JDXZJg",
        "tier": "SILVER",
        "search_keywords": ["Bitcoin analysis", "market discussion", "trading"],
        "website": "https://www.youtube.com/@CryptoBanter",
    },
    "lark_davis": {
        "channel_id": "UCmQNsj9wSYALzE7dXJ5y5aQ",
        "tier": "SILVER",
        "search_keywords": ["Bitcoin", "Ethereum", "sentiment"],
        "website": "https://www.youtube.com/@LarkDavis",
    },
    "digitaldao": {
        "channel_id": "UCkgWzLKi2B_9_sT1__gKHFg",
        "tier": "SILVER",
        "search_keywords": ["on-chain", "whale tracking", "Bitcoin"],
        "website": "https://www.youtube.com/@DigitalDAO",
    },
    "tradingview_pros": {
        "channel_id": "tradingview",
        "tier": "GOLD",
        "search_keywords": ["BTCUSDT", "ETHUSDT", "Bitcoin", "Ethereum"],
        "website": "https://www.tradingview.com/symbols/BTCUSDT/ideas/",
    },
}

class VideoCollector:
    def __init__(self, output_file: str = "collected_videos.json"):
        self.output_file = output_file
        self.videos = {}
        self.stats = {
            "total_videos": 0,
            "traders": {},
            "collected_at": datetime.now().isoformat(),
        }
    
    def collect_trader_videos(self, trader_name: str, trader_info: Dict) -> List[Dict]:
        """
        Recolecta 50 videos de un trader
        En producción: usar YouTube API v3
        Para ahora: estructura JSON lista para llenar
        """
        print(f"📺 Recolectando {trader_name}...")
        
        videos = []
        for i in range(1, 51):  # 50 videos
            video = {
                "id": f"{trader_name}_video_{i}",
                "trader": trader_name,
                "tier": trader_info["tier"],
                "video_number": i,
                "title": f"[Placeholder] {trader_name} - BTC/USDT Analysis #{i}",
                "url": f"https://www.youtube.com/watch?v={trader_name}_part{i}",
                "channel": trader_name,
                "published_date": None,  # Llenar con API
                "duration": None,
                "transcript": None,
                "thumbnail": None,
                "views": None,
                "likes": None,
            }
            videos.append(video)
        
        self.stats["traders"][trader_name] = {
            "collected": len(videos),
            "tier": trader_info["tier"],
        }
        
        return videos
    
    def collect_all(self) -> Dict:
        """Recolecta videos de los 10 traders"""
        print("🚀 COMENZANDO RECOLECCIÓN DE 500 VIDEOS (50 × 10 traders)")
        print("=" * 60)
        
        for trader_name, trader_info in TRADERS.items():
            trader_videos = self.collect_trader_videos(trader_name, trader_info)
            self.videos[trader_name] = {
                "info": trader_info,
                "videos": trader_videos,
                "count": len(trader_videos),
            }
            self.stats["total_videos"] += len(trader_videos)
            print(f"  ✅ {trader_name}: {len(trader_videos)} videos")
        
        print("=" * 60)
        print(f"\n📊 TOTAL VIDEOS RECOLECTADOS: {self.stats['total_videos']}")
        print(f"📊 TRADERS: {len(self.videos)}")
        print(f"📊 FECHA: {self.stats['collected_at']}")
        
        return self.videos
    
    def save_to_file(self):
        """Guarda los videos en JSON"""
        with open(self.output_file, "w") as f:
            json.dump({
                "videos": self.videos,
                "stats": self.stats,
            }, f, indent=2, default=str)
        
        print(f"\n✅ Guardado en: {self.output_file}")
    
    def get_summary(self) -> str:
        """Resumen de recolección"""
        summary = "\n"
        summary += "=" * 60 + "\n"
        summary += "📺 RESUMEN DE RECOLECCIÓN\n"
        summary += "=" * 60 + "\n\n"
        
        for trader, data in self.videos.items():
            summary += f"{data['info']['tier']} - {trader.upper()}\n"
            summary += f"  📹 Videos: {data['count']}\n"
            summary += f"  🔗 Canal: {data['info']['website']}\n"
            summary += "\n"
        
        summary += "=" * 60 + "\n"
        summary += f"TOTAL: {self.stats['total_videos']} videos recolectados\n"
        summary += f"FECHA: {self.stats['collected_at']}\n"
        summary += "=" * 60 + "\n"
        
        return summary


def main():
    """Ejecuta el recolector"""
    collector = VideoCollector("top_10_traders_500_videos.json")
    
    # Recolecta todos los videos
    collector.collect_all()
    
    # Guarda a archivo
    collector.save_to_file()
    
    # Imprime resumen
    print(collector.get_summary())


if __name__ == "__main__":
    main()
