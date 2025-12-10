#!/usr/bin/env python3
"""
YouTube to Summary - 통합 워크플로우
YouTube URL 하나로 자막 추출 → 요약 생성 → Discord 전송을 한 번에 처리
"""

import os
import sys
import json
import argparse
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Dict


def find_script(script_name: str, skill_name: str) -> Path:
    """Find a script in the skills directory"""

    # Try multiple possible locations
    locations = [
        Path.home() / '.claude' / 'skills' / skill_name / 'scripts' / script_name,
        Path(__file__).parent.parent.parent / skill_name / 'scripts' / script_name,
        Path.cwd() / skill_name / 'scripts' / script_name,
    ]

    for location in locations:
        if location.exists():
            return location

    raise FileNotFoundError(f"Could not find {script_name} in {skill_name}")


def extract_subtitles(youtube_url: str, language: str = 'ko') -> Dict:
    """Extract subtitles using extract_subtitles_v2.py"""

    print("=" * 70)
    print("📝 STEP 1: 자막 추출")
    print("=" * 70)

    script_path = find_script('extract_subtitles_v2.py', 'youtube-subtitle-extractor')

    cmd = [
        'python',
        str(script_path),
        youtube_url,
        '--language', language,
        '--json'
    ]

    print(f"🔍 실행: {' '.join(cmd)}")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"❌ 자막 추출 실패:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)

    # Parse JSON from stdout
    transcript_data = json.loads(result.stdout)

    if not transcript_data.get('success'):
        print(f"❌ 자막 추출 실패: {transcript_data.get('error')}", file=sys.stderr)
        sys.exit(1)

    print(f"✅ 자막 추출 성공!")
    print(f"   - Video ID: {transcript_data.get('video_id')}")
    print(f"   - Language: {transcript_data.get('language_used')}")
    print(f"   - Entries: {transcript_data.get('total_entries')}")
    print(f"   - Characters: {transcript_data.get('total_characters')}")

    return transcript_data


def get_video_info(youtube_url: str) -> Optional[Dict]:
    """Get video info using youtube-video-info (optional)"""

    try:
        script_path = find_script('get_video_info.py', 'youtube-video-info')

        cmd = [
            'python',
            str(script_path),
            youtube_url,
            '--json'
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return json.loads(result.stdout)
    except:
        pass

    return None


def generate_summary(
    transcript_data: Dict,
    video_info: Optional[Dict] = None,
    output_file: Optional[str] = None,
    model: str = 'claude-sonnet-4-20250514'
) -> str:
    """Generate summary using generate_summary.py"""

    print("\n" + "=" * 70)
    print("🤖 STEP 2: AI 요약 생성")
    print("=" * 70)

    script_path = find_script('generate_summary.py', 'youtube-summarizer')

    # Save transcript to temp file
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.json',
        delete=False,
        encoding='utf-8'
    ) as f:
        json.dump(transcript_data, f, ensure_ascii=False)
        transcript_file = f.name

    # Save video info to temp file if available
    video_info_file = None
    if video_info:
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False,
            encoding='utf-8'
        ) as f:
            json.dump(video_info, f, ensure_ascii=False)
            video_info_file = f.name

    # Build command
    cmd = [
        'python',
        str(script_path),
        transcript_file,
        '--model', model
    ]

    if video_info_file:
        cmd.extend(['--video-info', video_info_file])

    if output_file:
        cmd.extend(['--output', output_file])

    print(f"🔍 실행 중...")
    print(f"   - Model: {model}")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    # Cleanup temp files
    os.unlink(transcript_file)
    if video_info_file:
        os.unlink(video_info_file)

    if result.returncode != 0:
        print(f"❌ 요약 생성 실패:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)

    print(result.stderr)  # Print progress messages

    return result.stdout


def send_to_discord(summary_text: str) -> bool:
    """Send summary to Discord (optional)"""

    print("\n" + "=" * 70)
    print("📤 STEP 3: Discord 전송")
    print("=" * 70)

    try:
        script_path = find_script('send_message.py', 'discord-sender')

        cmd = [
            'python',
            str(script_path),
            summary_text
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("✅ Discord 전송 성공!")
            print(result.stdout)
            return True
        else:
            print(f"⚠️  Discord 전송 실패 (선택 사항이므로 계속 진행)", file=sys.stderr)
            return False

    except FileNotFoundError:
        print("⚠️  discord-sender 스킬을 찾을 수 없습니다 (건너뜀)", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description='YouTube 영상을 자동으로 자막 추출 → 요약 → Discord 전송',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  # 기본 사용 (자막 추출 + 요약)
  python summarize_youtube.py "https://www.youtube.com/watch?v=VIDEO_ID"

  # 요약만 생성하고 Discord는 전송하지 않음
  python summarize_youtube.py "VIDEO_URL" --no-discord

  # 영어 자막으로 요약
  python summarize_youtube.py "VIDEO_URL" --language en

  # 출력 파일 지정
  python summarize_youtube.py "VIDEO_URL" -o my_summary.md

  # 다른 Claude 모델 사용
  python summarize_youtube.py "VIDEO_URL" --model claude-opus-4-20250514
        """
    )
    parser.add_argument(
        'youtube_url',
        help='YouTube 영상 URL 또는 Video ID'
    )
    parser.add_argument(
        '--language', '-l',
        default='ko',
        help='자막 언어 (기본값: ko)'
    )
    parser.add_argument(
        '--output', '-o',
        help='요약 저장 경로 (기본값: summary_<video_id>.md)'
    )
    parser.add_argument(
        '--model', '-m',
        default='claude-sonnet-4-20250514',
        help='Claude 모델 (기본값: claude-sonnet-4-20250514)'
    )
    parser.add_argument(
        '--no-discord',
        action='store_true',
        help='Discord 전송 건너뛰기'
    )
    parser.add_argument(
        '--with-video-info',
        action='store_true',
        help='영상 정보(조회수, 좋아요 등)도 함께 수집 (youtube-video-info 필요)'
    )

    args = parser.parse_args()

    try:
        print("\n🎬 YouTube 자동 요약 워크플로우 시작")
        print(f"📺 URL: {args.youtube_url}")
        print(f"🌍 언어: {args.language}")
        print(f"🤖 모델: {args.model}\n")

        # Step 1: Extract subtitles
        transcript_data = extract_subtitles(args.youtube_url, args.language)

        # Optional: Get video info
        video_info = None
        if args.with_video_info:
            print("\n📊 영상 정보 수집 중...")
            video_info = get_video_info(args.youtube_url)
            if video_info:
                print("✅ 영상 정보 수집 완료")

        # Step 2: Generate summary
        summary_text = generate_summary(
            transcript_data,
            video_info,
            args.output,
            args.model
        )

        # Step 3: Send to Discord (optional)
        if not args.no_discord:
            send_to_discord(summary_text)
        else:
            print("\n⏭️  Discord 전송 건너뜀")

        print("\n" + "=" * 70)
        print("✅ 모든 작업 완료!")
        print("=" * 70)

        # Print summary to stdout for piping
        if not args.output:
            print("\n" + summary_text)

        sys.exit(0)

    except KeyboardInterrupt:
        print("\n\n⚠️  사용자가 중단했습니다.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
