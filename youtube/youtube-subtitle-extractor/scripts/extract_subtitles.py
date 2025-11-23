#!/usr/bin/env python3
"""
Simplified YouTube Subtitle Extractor using Apify API
"""

import os
import sys
import json
import requests
from pathlib import Path

def load_api_key() -> str:
    """Load Apify API key from .env file"""
    env_path = Path(__file__).parent.parent.parent / '.env'

    if not env_path.exists():
        raise ValueError(f".env file not found at {env_path}")

    with open(env_path) as f:
        for line in f:
            if line.startswith('APIFY='):
                api_key = line.split('=', 1)[1].strip()
                return api_key

    raise ValueError("APIFY key not found in .env file")


def extract_video_id(url: str) -> str:
    """Extract video ID from YouTube URL"""
    import re

    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
        r'youtube\.com\/embed\/([^&\n?#]+)',
        r'youtube\.com\/v\/([^&\n?#]+)'
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    # Assume it's already a video ID
    if len(url) == 11:
        return url

    raise ValueError(f"Could not extract video ID from: {url}")


def extract_subtitles(youtube_url: str, language: str = None):
    """Extract subtitles using Apify API directly"""

    api_key = load_api_key()
    video_id = extract_video_id(youtube_url)

    # Use the streamers/youtube-scraper actor
    # This actor can extract captions and transcripts
    actors = [
        "streamers/youtube-scraper",  # Primary actor
        "visita/youtube-scraper",     # Backup
    ]

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    for actor in actors:
        print(f"🔍 Trying actor: {actor}", file=sys.stderr)

        # Prepare input based on actor
        if actor == "streamers/youtube-scraper":
            actor_input = {
                "startUrls": [{"url": youtube_url}],
                "maxResults": 1,
                "subtitlesLanguage": language if language else "en",
                "captions": True,
                "extendOutputFunction": "",
                "customMapFunction": ""
            }
        else:
            # Generic input for other actors
            actor_input = {
                "videoIds": [video_id]
            }
            if language:
                actor_input["language"] = language

        try:
            # Start the actor run
            # Format: username~actorname for URL encoding
            actor_id_encoded = actor.replace('/', '~')
            run_url = f"https://api.apify.com/v2/acts/{actor_id_encoded}/runs"
            response = requests.post(
                run_url,
                headers=headers,
                json=actor_input,
                params={'token': api_key, 'waitForFinish': 120}
            )

            if response.status_code != 201:
                print(f"❌ Failed to start actor: {response.text}", file=sys.stderr)
                continue

            run_data = response.json()
            run_id = run_data['data']['id']
            dataset_id = run_data['data']['defaultDatasetId']

            print(f"⏳ Actor started. Run ID: {run_id}", file=sys.stderr)
            print(f"⏳ Waiting for completion...", file=sys.stderr)

            # Wait for the run to complete
            import time
            max_wait = 60  # 60 seconds max
            waited = 0

            while waited < max_wait:
                time.sleep(2)
                waited += 2

                status_url = f"https://api.apify.com/v2/acts/{actor_id_encoded}/runs/{run_id}"
                status_response = requests.get(
                    status_url,
                    params={'token': api_key}
                )

                if status_response.status_code == 200:
                    status_data = status_response.json()
                    status = status_data['data']['status']

                    print(f"⏳ Status: {status} ({waited}s)", file=sys.stderr)

                    if status == 'SUCCEEDED':
                        break
                    elif status in ['FAILED', 'ABORTED', 'TIMED-OUT']:
                        raise Exception(f"Actor run {status}")

            # Get results from dataset
            dataset_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items"
            dataset_response = requests.get(
                dataset_url,
                params={'token': api_key}
            )

            if dataset_response.status_code == 200:
                items = dataset_response.json()

                if items:
                    return {
                        'success': True,
                        'video_id': video_id,
                        'video_url': youtube_url,
                        'actor': actor,
                        'data': items
                    }
                else:
                    print(f"⚠️  No data returned from {actor}", file=sys.stderr)

        except Exception as e:
            print(f"❌ Error with {actor}: {e}", file=sys.stderr)
            continue

    return {
        'success': False,
        'error': 'All actors failed or no subtitles available'
    }


def format_subtitles(result):
    """Format subtitle results for display"""

    if not result.get('success'):
        return f"❌ Error: {result.get('error', 'Unknown error')}"

    output = []
    output.append("="*70)
    output.append("✅ YouTube Subtitle Extraction Successful!")
    output.append("="*70)
    output.append(f"Video ID: {result['video_id']}")
    output.append(f"Video URL: {result['video_url']}")
    output.append(f"Actor used: {result['actor']}")
    output.append("")

    data = result.get('data', [])

    if not data:
        output.append("⚠️  No subtitle data found")
        return "\n".join(output)

    for idx, item in enumerate(data, 1):
        output.append(f"\n{'='*70}")
        output.append(f"Subtitle Item #{idx}")
        output.append(f"{'='*70}")

        if isinstance(item, dict):
            # Show available keys
            output.append(f"Available fields: {', '.join(item.keys())}")
            output.append("")

            # Try to find subtitle/caption text
            text_fields = ['transcriptMerged', 'captions', 'text', 'subtitle', 'transcript', 'content', 'subtitles']

            for field in text_fields:
                if field in item:
                    value = item[field]

                    if isinstance(value, str):
                        # Show first 2000 characters
                        if len(value) > 2000:
                            output.append(f"\n{field.upper()}:")
                            output.append("-" * 60)
                            output.append(value[:2000])
                            output.append(f"\n... (truncated, total length: {len(value)} characters)")
                        else:
                            output.append(f"\n{field.upper()}:")
                            output.append("-" * 60)
                            output.append(value)
                    elif isinstance(value, list):
                        output.append(f"\n{field.upper()} (list with {len(value)} items):")
                        output.append("-" * 60)
                        # Show first few items
                        for i, sub_item in enumerate(value[:5]):
                            if isinstance(sub_item, dict):
                                output.append(f"  [{i+1}] {sub_item}")
                            else:
                                output.append(f"  [{i+1}] {str(sub_item)[:200]}")
                        if len(value) > 5:
                            output.append(f"  ... and {len(value) - 5} more items")
                    else:
                        output.append(f"{field}: {value}")

                    output.append("")

            # Show other metadata
            metadata_fields = ['language', 'languageCode', 'title', 'duration', 'author']
            for field in metadata_fields:
                if field in item:
                    output.append(f"{field}: {item[field]}")
        else:
            output.append(str(item)[:1000])

    output.append("\n" + "="*70)

    return "\n".join(output)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Extract YouTube subtitles')
    parser.add_argument('url', help='YouTube video URL or ID')
    parser.add_argument('--language', help='Preferred language (e.g., ko, en)')
    parser.add_argument('--json', action='store_true', help='Output raw JSON')

    args = parser.parse_args()

    try:
        result = extract_subtitles(args.url, args.language)

        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_subtitles(result))

        sys.exit(0 if result.get('success') else 1)

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
