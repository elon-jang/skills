#!/usr/bin/env python3
"""
YouTube Video Summarizer with Claude API
자막과 영상 정보를 입력받아 구조화된 요약을 자동 생성합니다.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Optional


def load_api_key() -> str:
    """Load Anthropic API key from .env file or environment"""

    # Try environment variable first
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if api_key:
        return api_key

    # Try .env file
    env_locations = [
        Path.cwd() / '.env',
        Path.home() / '.env',
        Path(__file__).parent.parent.parent / '.env',
    ]

    for env_path in env_locations:
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    if line.startswith('ANTHROPIC_API_KEY='):
                        api_key = line.split('=', 1)[1].strip()
                        return api_key

    raise ValueError(
        "ANTHROPIC_API_KEY not found. Set it in .env file or as environment variable."
    )


def load_summary_guide() -> str:
    """Load the summary guide template"""
    guide_path = Path(__file__).parent.parent / 'references' / 'summary_guide.md'

    if not guide_path.exists():
        raise FileNotFoundError(f"Summary guide not found at {guide_path}")

    with open(guide_path, 'r', encoding='utf-8') as f:
        return f.read()


def format_transcript_for_prompt(transcript_data: Dict) -> str:
    """Format transcript data into a readable prompt"""

    lines = []

    # Add video metadata
    if 'video_id' in transcript_data:
        lines.append(f"Video ID: {transcript_data['video_id']}")
    if 'video_url' in transcript_data:
        lines.append(f"Video URL: {transcript_data['video_url']}")

    lines.append("")

    # Add transcript text
    if 'transcript_merged' in transcript_data:
        lines.append("=== 전체 자막 텍스트 ===")
        lines.append(transcript_data['transcript_merged'])
    elif 'transcript' in transcript_data:
        lines.append("=== 타임스탬프별 자막 ===")
        for entry in transcript_data['transcript']:
            start = entry.get('start', 0)
            text = entry.get('text', '')
            minutes = int(start // 60)
            seconds = int(start % 60)
            lines.append(f"[{minutes:02d}:{seconds:02d}] {text}")

    return '\n'.join(lines)


def format_video_info_for_prompt(video_info: Optional[Dict]) -> str:
    """Format video info into a readable prompt"""

    if not video_info:
        return ""

    lines = []
    lines.append("=== 영상 정보 ===")

    if 'title' in video_info:
        lines.append(f"제목: {video_info['title']}")
    if 'description' in video_info:
        lines.append(f"설명: {video_info['description'][:500]}...")
    if 'channel' in video_info:
        channel = video_info['channel']
        if isinstance(channel, dict):
            lines.append(f"채널: {channel.get('name', 'N/A')}")
        else:
            lines.append(f"채널: {channel}")
    if 'duration' in video_info:
        lines.append(f"재생시간: {video_info['duration']}")
    if 'statistics' in video_info:
        stats = video_info['statistics']
        lines.append(f"조회수: {stats.get('view_count', 'N/A'):,}")
        lines.append(f"좋아요: {stats.get('like_count', 'N/A'):,}")

    lines.append("")
    return '\n'.join(lines)


def generate_summary(
    transcript_data: Dict,
    video_info: Optional[Dict] = None,
    model: str = "claude-sonnet-4-20250514"
) -> str:
    """Generate summary using Claude API"""

    try:
        from anthropic import Anthropic
    except ImportError:
        raise ImportError(
            "anthropic package not installed. Run: pip install anthropic"
        )

    api_key = load_api_key()
    summary_guide = load_summary_guide()

    # Build the prompt
    prompt_parts = []

    # Add video info if available
    if video_info:
        prompt_parts.append(format_video_info_for_prompt(video_info))

    # Add transcript
    prompt_parts.append(format_transcript_for_prompt(transcript_data))

    prompt_parts.append("\n위 영상의 자막을 summary_guide.md의 지침에 따라 구조화된 요약으로 작성해주세요.")

    user_prompt = '\n'.join(prompt_parts)

    print("🤖 Claude API를 호출하여 요약을 생성하고 있습니다...", file=sys.stderr)
    print(f"📊 자막 길이: {len(transcript_data.get('transcript_merged', ''))} 문자", file=sys.stderr)
    print(f"🎯 모델: {model}", file=sys.stderr)

    # Call Claude API
    client = Anthropic(api_key=api_key)

    response = client.messages.create(
        model=model,
        max_tokens=8000,
        temperature=0.3,
        system=summary_guide,  # Use summary guide as system prompt
        messages=[
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    # Extract the summary text
    summary_text = response.content[0].text

    print("✅ 요약 생성 완료!", file=sys.stderr)
    print(f"📝 생성된 요약 길이: {len(summary_text)} 문자", file=sys.stderr)

    return summary_text


def main():
    parser = argparse.ArgumentParser(
        description='Generate structured YouTube video summary using Claude API'
    )
    parser.add_argument(
        'transcript_file',
        help='Path to transcript JSON file (from extract_subtitles_v2.py)'
    )
    parser.add_argument(
        '--video-info',
        help='Path to video info JSON file (from youtube-video-info)'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output file path (default: summary_<video_id>.md)'
    )
    parser.add_argument(
        '--model',
        default='claude-sonnet-4-20250514',
        help='Claude model to use (default: claude-sonnet-4-20250514)'
    )

    args = parser.parse_args()

    try:
        # Load transcript data
        print(f"📖 자막 파일 로딩: {args.transcript_file}", file=sys.stderr)
        with open(args.transcript_file, 'r', encoding='utf-8') as f:
            transcript_data = json.load(f)

        if not transcript_data.get('success'):
            print(f"❌ 자막 추출 실패: {transcript_data.get('error')}", file=sys.stderr)
            sys.exit(1)

        # Load video info if provided
        video_info = None
        if args.video_info:
            print(f"📖 영상 정보 로딩: {args.video_info}", file=sys.stderr)
            with open(args.video_info, 'r', encoding='utf-8') as f:
                video_info = json.load(f)

        # Generate summary
        summary = generate_summary(transcript_data, video_info, args.model)

        # Determine output file
        if args.output:
            output_path = Path(args.output)
        else:
            video_id = transcript_data.get('video_id', 'unknown')
            output_path = Path(f"summary_{video_id}.md")

        # Save summary
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(summary)

        print(f"✅ 요약이 저장되었습니다: {output_path}", file=sys.stderr)
        print(f"📄 파일 경로: {output_path.absolute()}", file=sys.stderr)

        # Also print to stdout for piping
        print(summary)

        sys.exit(0)

    except FileNotFoundError as e:
        print(f"❌ 파일을 찾을 수 없습니다: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ 오류 발생: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
