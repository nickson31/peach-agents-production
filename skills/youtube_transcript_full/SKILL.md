# YouTube Transcript Extractor Skill

## Overview
Extracts full transcripts from YouTube videos using multiple methods and APIs.

## Purpose
- Extract video transcripts automatically
- Analyze trading video content
- Support research analysis

## Input
```json
{
  "video_id": "CEJ_R5226xE",
  "video_url": "https://www.youtube.com/watch?v=CEJ_R5226xE",
  "methods": ["transcript_api", "youtube_api", "manual_captions"]
}
```

## Output
```json
{
  "video_id": "CEJ_R5226xE",
  "title": "NEW OpenClaw AI Good For Trading",
  "transcript": "full text of transcript...",
  "length_chars": 15234,
  "language": "en",
  "captions_available": true,
  "source_method": "transcript_api"
}
```

## Available Methods

### Method 1: TranscriptAPI.com (Primary)
```bash
curl -X GET https://transcriptapi.com/api/v1/transcript \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d "videoId=CEJ_R5226xE"
```

### Method 2: YouTube-Transcript-API (Python)
```python
from youtube_transcript_api import YouTubeTranscriptApi
transcript = YouTubeTranscriptApi.get_transcript("CEJ_R5226xE")
```

### Method 3: YouTube Captions API (Official)
Requires YouTube Data API v3

## Implementation
Run the skill with:
```bash
openclaw skill youtube_transcript_full --input "{\"video_id\": \"CEJ_R5226xE\"}"
```

## Configuration
Set environment variables:
- TRANSCRIPT_API_KEY: Your TranscriptAPI.com key
- YOUTUBE_API_KEY: Your YouTube Data API key
