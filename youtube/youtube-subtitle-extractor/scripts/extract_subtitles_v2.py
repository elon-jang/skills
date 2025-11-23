#!/usr/bin/env python3
"""
Improved YouTube Subtitle Extractor using youtube-transcript-api
This version directly fetches YouTube's official subtitles without needing API keys.
"""

import sys
import json
import re
from typing import Optional, List, Dict


def extract_video_id(url: str) -> str:
    """Extract video ID from YouTube URL"""
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


def get_subtitles(youtube_url: str, languages: Optional[List[str]] = None) -> Dict:
    """
    Extract subtitles using youtube-transcript-api

    Args:
        youtube_url: YouTube video URL or ID
        languages: List of language codes to try (e.g., ['ko', 'en'])

    Returns:
        Dictionary with success status, video info, and subtitle data
    """
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        from youtube_transcript_api._errors import (
            TranscriptsDisabled,
            NoTranscriptFound,
            VideoUnavailable
        )
    except ImportError:
        return {
            'success': False,
            'error': 'youtube-transcript-api not installed. Run: pip install youtube-transcript-api'
        }

    try:
        video_id = extract_video_id(youtube_url)
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        # Try to fetch transcript in preferred languages
        if languages is None:
            languages = ['ko', 'en']

        print(f"🔍 Attempting to fetch transcript for video: {video_id}", file=sys.stderr)
        print(f"🔍 Preferred languages: {', '.join(languages)}", file=sys.stderr)

        # Create API instance
        api = YouTubeTranscriptApi()

        # Try to fetch with preferred languages
        try:
            fetched_transcript = api.fetch(video_id, languages=languages, preserve_formatting=False)
            used_language = fetched_transcript.language_code
            is_generated = fetched_transcript.is_generated
            print(f"✅ Successfully fetched transcript in language: {used_language} (auto-generated: {is_generated})", file=sys.stderr)
            print(f"✅ Total snippets: {len(fetched_transcript.snippets)}", file=sys.stderr)
        except Exception as e:
            print(f"❌ Failed to fetch transcript: {e}", file=sys.stderr)
            return {
                'success': False,
                'video_id': video_id,
                'video_url': video_url,
                'error': f'Failed to fetch transcript: {str(e)}'
            }

        # Try to get list of available languages for informational purposes
        available_languages = []
        try:
            transcript_list = api.list(video_id)
            for transcript in transcript_list:
                available_languages.append({
                    'code': transcript.language_code,
                    'language': transcript.language,
                    'is_generated': transcript.is_generated,
                    'is_translatable': transcript.is_translatable
                })
        except:
            # If we can't get the list, just note the language we used
            available_languages = [{'code': used_language, 'language': used_language}]

        # Format the transcript
        formatted_transcript = []
        full_text = []

        for snippet in fetched_transcript.snippets:
            formatted_transcript.append({
                'text': snippet.text,
                'start': snippet.start,
                'duration': snippet.duration
            })
            full_text.append(snippet.text)

        merged_text = ' '.join(full_text)

        return {
            'success': True,
            'video_id': video_id,
            'video_url': video_url,
            'language_used': used_language,
            'available_languages': available_languages,
            'transcript': formatted_transcript,
            'transcript_merged': merged_text,
            'total_entries': len(formatted_transcript),
            'total_characters': len(merged_text)
        }

    except TranscriptsDisabled:
        return {
            'success': False,
            'video_id': video_id if 'video_id' in locals() else None,
            'error': 'Subtitles are disabled for this video'
        }
    except NoTranscriptFound:
        return {
            'success': False,
            'video_id': video_id if 'video_id' in locals() else None,
            'error': 'No transcripts found for this video'
        }
    except VideoUnavailable:
        return {
            'success': False,
            'video_id': video_id if 'video_id' in locals() else None,
            'error': 'Video is unavailable'
        }
    except Exception as e:
        return {
            'success': False,
            'video_id': video_id if 'video_id' in locals() else None,
            'error': str(e)
        }


def format_output(result: Dict, show_full: bool = False) -> str:
    """Format the result for display"""

    lines = []
    lines.append("=" * 70)

    if result['success']:
        lines.append("✅ YouTube Subtitle Extraction Successful!")
        lines.append("=" * 70)
        lines.append(f"Video ID: {result['video_id']}")
        lines.append(f"Video URL: {result['video_url']}")
        lines.append(f"Language Used: {result['language_used']}")
        lines.append(f"Total Entries: {result['total_entries']}")
        lines.append(f"Total Characters: {result['total_characters']}")
        lines.append("")

        lines.append("📋 Available Languages:")
        for lang_info in result['available_languages']:
            status = "auto-generated" if lang_info['is_generated'] else "manual"
            lines.append(f"  - {lang_info['code']}: {lang_info['language']} ({status})")

        lines.append("")
        lines.append("=" * 70)
        lines.append("📝 Subtitle Text (First 2000 characters):")
        lines.append("=" * 70)

        merged = result['transcript_merged']
        if len(merged) > 2000 and not show_full:
            lines.append(merged[:2000])
            lines.append(f"\n... (truncated, {len(merged) - 2000} more characters)")
            lines.append("\nUse --full flag to see complete text")
        else:
            lines.append(merged)

        if show_full:
            lines.append("")
            lines.append("=" * 70)
            lines.append("⏱️  Timestamped Entries (First 10):")
            lines.append("=" * 70)
            for i, entry in enumerate(result['transcript'][:10], 1):
                start = entry['start']
                minutes = int(start // 60)
                seconds = int(start % 60)
                lines.append(f"[{minutes:02d}:{seconds:02d}] {entry['text']}")

            if len(result['transcript']) > 10:
                lines.append(f"\n... and {len(result['transcript']) - 10} more entries")

    else:
        lines.append("❌ Subtitle Extraction Failed")
        lines.append("=" * 70)
        lines.append(f"Error: {result['error']}")

        if result.get('video_id'):
            lines.append(f"Video ID: {result['video_id']}")

        if result.get('available_languages'):
            lines.append("\n📋 Available Languages:")
            for lang_info in result['available_languages']:
                status = "auto-generated" if lang_info['is_generated'] else "manual"
                lines.append(f"  - {lang_info['code']}: {lang_info['language']} ({status})")

    lines.append("=" * 70)
    return '\n'.join(lines)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Extract YouTube subtitles using youtube-transcript-api'
    )
    parser.add_argument('url', help='YouTube video URL or ID')
    parser.add_argument(
        '--language',
        action='append',
        help='Preferred language codes (can be used multiple times, e.g., --language ko --language en)'
    )
    parser.add_argument('--json', action='store_true', help='Output raw JSON')
    parser.add_argument('--full', action='store_true', help='Show full text without truncation')

    args = parser.parse_args()

    # Use provided languages or default to Korean and English
    languages = args.language if args.language else ['ko', 'en']

    try:
        result = get_subtitles(args.url, languages)

        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_output(result, show_full=args.full))

        sys.exit(0 if result['success'] else 1)

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
