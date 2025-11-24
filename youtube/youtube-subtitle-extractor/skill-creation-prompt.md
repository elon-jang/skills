# YouTube Subtitle Extractor Skill 생성 프롬프트

```
Claude Code용 YouTube Subtitle Extractor 스킬을 만들어줘.

## 스킬 개요
- 이름: youtube-subtitle-extractor
- 목적: YouTube 영상의 자막과 메타데이터를 JSON 형식으로 추출
- 사용 시나리오: 사용자가 "유튜브 자막 뽑아줘", "자막 추출해줘" 등으로 요청할 때

## 핵심 기능
1. YouTube URL 또는 Video ID로부터 자막 추출
2. youtube-transcript-api 사용 (권장, API 키 불필요)
3. 다국어 자막 지원 (한국어, 영어 등 우선순위 지정 가능)
4. 타임스탬프 포함 자막 데이터 제공
5. JSON 형식으로 구조화된 출력
6. Apify API 대체 지원 (풍부한 메타데이터 필요 시)

## 기술 요구사항
- Python 스크립트 2개:
  - scripts/extract_subtitles_v2.py (youtube-transcript-api 사용, 권장)
  - scripts/extract_subtitles.py (Apify API 사용, 대체)
- 환경 변수: APIFY (Apify API 사용 시만 필수)
- CLI 인터페이스 제공 (--language, --json, --full 플래그)

## 사용 예시

**기본 사용 (youtube-transcript-api):**
```bash
python scripts/extract_subtitles_v2.py "https://youtube.com/watch?v=VIDEO_ID" --language ko --json
```

**출력 형식:**
```json
{
  "success": true,
  "video_id": "VIDEO_ID",
  "video_url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "language_used": "ko",
  "transcript": [
    {
      "text": "안녕하세요",
      "start": 0.08,
      "duration": 4.36
    }
  ],
  "transcript_merged": "전체 자막 텍스트...",
  "total_entries": 557,
  "total_characters": 10728
}
```

**CLI 옵션:**
```bash
# 한국어 자막
python scripts/extract_subtitles_v2.py "VIDEO_URL" --language ko --json

# 영어 자막
python scripts/extract_subtitles_v2.py "VIDEO_URL" --language en --json

# 여러 언어 우선순위
python scripts/extract_subtitles_v2.py "VIDEO_URL" --language ko --language en --json

# 전체 텍스트만 출력
python scripts/extract_subtitles_v2.py "VIDEO_URL" --full
```

## 문서 작성
- skill.md: 영문으로 스킬 정의 및 사용법
- README.md: 한글로 상세 가이드
  - youtube-transcript-api vs Apify 비교
  - 설치 방법 (pip install youtube-transcript-api)
  - 환경 변수 설정 (Apify 사용 시)
  - 사용 예제
  - 출력 형식 설명
  - 트러블슈팅 (자막 없음, API 오류 등)

## 에러 처리
- YouTube URL 파싱 실패 시 명확한 오류 메시지
- 자막이 없는 영상의 경우 "자막 없음" 메시지
- 요청한 언어의 자막이 없을 때 사용 가능한 언어 목록 표시
- API 오류 핸들링

나머지 구현 세부사항(URL 파싱, API 호출, 데이터 구조화 등)은 최선의 방법으로 구현해줘.
```
