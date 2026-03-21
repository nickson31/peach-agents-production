#!/usr/bin/env python3
"""
YouTube Transcript Extractor - OpenClaw Skill
Extracts transcripts from YouTube videos using TranscriptAPI.com
"""

import os
import json
import sys
import urllib.request
import urllib.parse
from typing import Dict, List, Optional

class YouTubeTranscriptSkill:
    def __init__(self, api_key: str = None):
        """Initialize with TranscriptAPI key"""
        self.api_key = api_key or os.environ.get("TRANSCRIPT_API_KEY")
        self.base_url = "https://transcriptapi.com"
        self.videos_to_extract = [
            ("CEJ_R5226xE", "NEW OpenClaw AI Good For Trading"),
            ("Oh94XVXkZPM", "How I'm Using OpenClaw for Automated Trading"),
            ("QehqUyBuZMk", "I Tried the 100K/Month AI Side Hustle"),
            ("yg6MmR_9ed8", "How I Built a Profitable Trading Strategy"),
            ("YknxNkTgNWk", "+1,560% ROI With OpenClaw Polymarket Trading"),
            ("OdZj4NY2ibU", "Everyone's Using OpenClaw Wrong"),
            ("i13XK-uUOLQ", "Making $$$ with OpenClaw"),
            ("NKVBQath_sU", "Watching My OpenClaw Make Money In Real Time"),
            ("GansiD6Mk5Y", "I Gave 3 AI Agents $1,000 Each"),
            ("LCkGVCfmtzo", "My AI Agents Made Money in 7 Days"),
            ("rv6p9R_lNxc", "OPENCLAW FULL COURSE 3 HOURS"),
            ("ewOpudu8Cjc", "Build a Trading Bot With AI using OpenClaw"),
            ("2IZGViOIdcM", "Reich durch 1 Trade am Tag mit OpenClaw"),
            ("MaH6_I4NP0k", "These OpenClaw Hacks Will Make You Money"),
            ("nSBKCZQkmYw", "Use OpenClaw to Build a Business That Runs Itself"),
        ]
    
    def extract_via_transcriptapi(self, video_id: str) -> Optional[Dict]:
        """Extract using TranscriptAPI.com - CORRECT ENDPOINT: /api/v2/youtube/transcript"""
        if not self.api_key:
            return None
        
        try:
            # CORRECT ENDPOINT from Brave Search documentation
            endpoint = f"{self.base_url}/api/v2/youtube/transcript"
            
            # Build request with video_url parameter (not video_id)
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            params = urllib.parse.urlencode({"video_url": video_url})
            url = f"{endpoint}?{params}"
            
            req = urllib.request.Request(
                url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Accept": "application/json"
                }
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                # Extract transcript from response
                transcript_text = data.get("content", "") or data.get("transcript", "")
                
                return {
                    "video_id": video_id,
                    "title": data.get("title", ""),
                    "author": data.get("author", ""),
                    "transcript": transcript_text,
                    "length": len(transcript_text),
                    "source": "transcriptapi_v2",
                    "status": "success"
                }
            
        except urllib.error.HTTPError as e:
            return None
        except Exception as e:
            return None
    
    def extract_via_youtube_api(self, video_id: str) -> Optional[Dict]:
        """Extract using YouTube Data API (requires authentication)"""
        # This requires YOUTUBE_API_KEY environment variable
        api_key = os.environ.get("YOUTUBE_API_KEY")
        if not api_key:
            return None
        
        try:
            # YouTube Data API endpoint for captions
            url = "https://www.googleapis.com/youtube/v3/captions"
            params = urllib.parse.urlencode({
                "videoId": video_id,
                "key": api_key
            })
            
            req = urllib.request.Request(
                f"{url}?{params}",
                headers={"Accept": "application/json"}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                return {
                    "video_id": video_id,
                    "captions_available": len(data.get("items", [])) > 0,
                    "source": "youtube_api"
                }
        except Exception as e:
            return None
    
    def extract_all(self) -> List[Dict]:
        """Extract transcripts from all videos"""
        results = []
        
        print("🎬 EXTRAYENDO TRANSCRIPCIONES CON OPENCLAW SKILL")
        print("=" * 70)
        print(f"Videos a procesar: {len(self.videos_to_extract)}")
        print(f"API Key: {'✅ Presente' if self.api_key else '❌ No configurada'}")
        print("=" * 70)
        
        for i, (video_id, title) in enumerate(self.videos_to_extract, 1):
            print(f"\n[{i}/{len(self.videos_to_extract)}] 🎬 {title[:50]}...")
            
            result = {
                "video_id": video_id,
                "title": title,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "transcript": None,
                "status": "pending"
            }
            
            # Try TranscriptAPI first
            transcript_result = self.extract_via_transcriptapi(video_id)
            if transcript_result:
                result.update(transcript_result)
                result["status"] = "success"
                print(f"   ✅ Éxito: {len(result['transcript'])} caracteres")
            else:
                # Try YouTube API
                yt_result = self.extract_via_youtube_api(video_id)
                if yt_result and yt_result.get("captions_available"):
                    result["status"] = "captions_available"
                    print(f"   ⚠️ Captions disponibles (no extraído)")
                else:
                    result["status"] = "no_transcript"
                    print(f"   ❌ No se pudo extraer")
            
            results.append(result)
        
        return results
    
    def save_results(self, results: List[Dict], output_file: str = "youtube_transcripts.json"):
        """Save results to JSON file"""
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n✅ Resultados guardados: {output_file}")
    
    def print_summary(self, results: List[Dict]):
        """Print extraction summary"""
        print("\n" + "=" * 70)
        print("📊 RESUMEN DE EXTRACCIÓN")
        print("=" * 70)
        
        success = sum(1 for r in results if r["status"] == "success")
        captions = sum(1 for r in results if r["status"] == "captions_available")
        failed = sum(1 for r in results if r["status"] == "no_transcript")
        
        print(f"\n✅ Transcripciones extraídas: {success}/{len(results)}")
        print(f"⚠️ Captions disponibles (no extraídas): {captions}")
        print(f"❌ Sin acceso: {failed}")
        
        if success > 0:
            print(f"\n📝 Transcripciones completas:")
            for result in results:
                if result["status"] == "success":
                    chars = len(result.get("transcript", ""))
                    print(f"   ✅ {result['title'][:40]}: {chars} caracteres")

def main():
    """Main execution"""
    import sys
    
    # Get API key from argument or environment
    api_key = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("TRANSCRIPT_API_KEY")
    
    if not api_key:
        print("❌ No API key provided")
        print("Usage: python3 youtube_transcript_extractor.py <API_KEY>")
        print("Or set TRANSCRIPT_API_KEY environment variable")
        sys.exit(1)
    
    # Extract transcripts
    skill = YouTubeTranscriptSkill(api_key=api_key)
    results = skill.extract_all()
    
    # Save results
    output_file = "/home/ubuntu/.openclaw/workspace/youtube_transcripts_extracted.json"
    skill.save_results(results, output_file)
    
    # Print summary
    skill.print_summary(results)
    
    return results

if __name__ == "__main__":
    main()
