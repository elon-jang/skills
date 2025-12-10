#!/usr/bin/env python3
"""
YouTube Video Information Fetcher

This script fetches detailed information about a YouTube video using the YouTube Data API v3.
It supports both video URLs and video IDs as input.

Usage:
    python get_video_info.py <video_url_or_id> [--env-file PATH]

Example:
    python get_video_info.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    python get_video_info.py "dQw4w9WgXcQ"
    python get_video_info.py "dQw4w9WgXcQ" --env-file /path/to/.env
"""

import os
import sys
import json
import argparse
import re
from urllib.parse import urlparse, parse_qs
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: 'requests' library is not installed.", file=sys.stderr)
    print("Please install it using: pip install requests", file=sys.stderr)
    sys.exit(1)


def load_env_file(env_path=None):
    """Load environment variables from .env file"""
    if env_path is None:
        # Try to find .env in common locations
        possible_paths = [
            Path.cwd() / '.env',
            Path.home() / '.env',
            Path(__file__).parent.parent.parent / '.env',  # Go up to parent directories
        ]

        for path in possible_paths:
            if path.exists():
                env_path = path
                break
    else:
        env_path = Path(env_path)

    if env_path is None or not env_path.exists():
        return None

    env_vars = {}
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()

    return env_vars


def extract_video_id(url_or_id):
    """
    Extract video ID from YouTube URL or return the ID if already provided.

    Supports formats:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - VIDEO_ID (direct ID)
    """
    # If it's already a video ID (11 characters, alphanumeric with - and _)
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url_or_id):
        return url_or_id

    # Try to parse as URL
    try:
        parsed_url = urlparse(url_or_id)

        # youtube.com/watch?v=VIDEO_ID
        if 'youtube.com' in parsed_url.netloc:
            query_params = parse_qs(parsed_url.query)
            if 'v' in query_params:
                return query_params['v'][0]

        # youtu.be/VIDEO_ID
        elif 'youtu.be' in parsed_url.netloc:
            return parsed_url.path.lstrip('/')

    except Exception:
        pass

    return None


def get_video_info(video_id, api_key):
    """
    Fetch video information from YouTube Data API v3

    Returns:
        dict: Video information including title, description, statistics, etc.
    """
    base_url = "https://www.googleapis.com/youtube/v3/videos"

    params = {
        'part': 'snippet,statistics,contentDetails,status',
        'id': video_id,
        'key': api_key
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()

        data = response.json()

        if 'items' not in data or len(data['items']) == 0:
            return {'error': 'Video not found or API key is invalid'}

        video = data['items'][0]
        snippet = video.get('snippet', {})
        statistics = video.get('statistics', {})
        content_details = video.get('content_details', {})
        status = video.get('status', {})

        # Format the output
        result = {
            'video_id': video_id,
            'url': f"https://www.youtube.com/watch?v={video_id}",
            'title': snippet.get('title', 'N/A'),
            'description': snippet.get('description', 'N/A'),
            'channel': {
                'name': snippet.get('channelTitle', 'N/A'),
                'id': snippet.get('channelId', 'N/A')
            },
            'published_at': snippet.get('publishedAt', 'N/A'),
            'duration': content_details.get('duration', 'N/A'),
            'statistics': {
                'view_count': int(statistics.get('viewCount', 0)),
                'like_count': int(statistics.get('likeCount', 0)),
                'comment_count': int(statistics.get('commentCount', 0))
            },
            'tags': snippet.get('tags', []),
            'category_id': snippet.get('categoryId', 'N/A'),
            'privacy_status': status.get('privacyStatus', 'N/A'),
            'thumbnails': snippet.get('thumbnails', {})
        }

        return result

    except requests.exceptions.RequestException as e:
        return {'error': f'API request failed: {str(e)}'}


def format_output(video_info):
    """Format video information for display"""
    if 'error' in video_info:
        return f"Error: {video_info['error']}"

    output = []
    output.append(f"Title: {video_info['title']}")
    output.append(f"Channel: {video_info['channel']['name']}")
    output.append(f"Video URL: {video_info['url']}")
    output.append(f"Published: {video_info['published_at']}")
    output.append(f"Duration: {video_info['duration']}")
    output.append(f"\nStatistics:")
    output.append(f"  Views: {video_info['statistics']['view_count']:,}")
    output.append(f"  Likes: {video_info['statistics']['like_count']:,}")
    output.append(f"  Comments: {video_info['statistics']['comment_count']:,}")

    if video_info.get('tags'):
        output.append(f"\nTags: {', '.join(video_info['tags'][:10])}")  # Show first 10 tags

    output.append(f"\nDescription:")
    # Truncate long descriptions
    description = video_info['description']
    if len(description) > 300:
        description = description[:300] + "..."
    output.append(description)

    return '\n'.join(output)


def main():
    parser = argparse.ArgumentParser(
        description='Fetch YouTube video information using YouTube Data API v3',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  %(prog)s "dQw4w9WgXcQ"
  %(prog)s "dQw4w9WgXcQ" --env-file /path/to/.env
  %(prog)s "dQw4w9WgXcQ" --json
        """
    )

    parser.add_argument(
        'video',
        help='YouTube video URL or video ID'
    )

    parser.add_argument(
        '--env-file',
        help='Path to .env file containing GOOGLE_API_KEY'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Output in JSON format'
    )

    parser.add_argument(
        '--api-key',
        help='Google API key (alternative to .env file)'
    )

    args = parser.parse_args()

    # Get API key
    api_key = args.api_key

    if not api_key:
        # Try to load from .env file
        env_vars = load_env_file(args.env_file)

        if env_vars and 'GOOGLE_API_KEY' in env_vars:
            api_key = env_vars['GOOGLE_API_KEY']
        else:
            # Try environment variable
            api_key = os.environ.get('GOOGLE_API_KEY')

    if not api_key:
        print("Error: GOOGLE_API_KEY not found.", file=sys.stderr)
        print("Please provide API key via:", file=sys.stderr)
        print("  1. --api-key argument", file=sys.stderr)
        print("  2. GOOGLE_API_KEY in .env file", file=sys.stderr)
        print("  3. GOOGLE_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    # Extract video ID
    video_id = extract_video_id(args.video)

    if not video_id:
        print(f"Error: Could not extract video ID from: {args.video}", file=sys.stderr)
        print("Please provide a valid YouTube URL or video ID.", file=sys.stderr)
        sys.exit(1)

    # Fetch video information
    video_info = get_video_info(video_id, api_key)

    # Output
    if args.json:
        print(json.dumps(video_info, indent=2, ensure_ascii=False))
    else:
        print(format_output(video_info))


if __name__ == '__main__':
    main()
