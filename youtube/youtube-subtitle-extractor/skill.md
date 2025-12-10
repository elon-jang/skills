---
name: youtube-subtitle-extractor
description: YouTube 영상의 자막/메타데이터를 JSON 형식으로 추출하는 스킬입니다. youtube-transcript-api(권장) 또는 Apify API를 사용합니다. 추출된 결과는 youtube-summarizer 등 후속 스킬의 입력으로 사용됩니다.
version: 2.0.0
dependencies:
  - python >= 3.10
  - youtube-transcript-api (권장)
  - requests
---

# YouTube Subtitle Extractor

> skill-creator 양식에 맞춘 SKILL 문서입니다. 유튜브 링크만 있으면 자막/메타데이터를 안전하게 꺼내 다른 스킬(youtube-summarizer, discord-sender 등)에 전달할 수 있습니다.

## 언제 사용하나요?
- 사용자가 "유튜브 자막/트랜스크립트 뽑아줘"라고 요청할 때
- 요약, 번역, 검색 등 후속 스킬이 필요로 하는 원문 텍스트가 없을 때
- 여러 URL을 한 번에 처리하거나, 특정 언어/포맷으로 저장해야 할 때

## 입력 파라미터
| 이름 | 필수 | 설명 |
| --- | --- | --- |
| `youtube_url` | ✅ | 전체 URL 또는 11자 Video ID |
| `language` | ⛔ | `ko`, `en` 등 원하는 자막 언어 코드 |
| `raw_json` | ⛔ | true일 경우 JSON 원본을 그대로 반환 (`--json` 플래그) |

## 출력
- 영상 메타데이터: 제목, duration, channel, viewCount 등
- 자막/트랜스크립트 텍스트(필드명: `transcriptMerged`, `text`, `captions` 등)
- 사용된 배우(actor) 정보 및 요청 URL
- 오류/경고 메시지(자막 부재, API 제한 등)

## 실행 스크립트

### 방법 1: youtube-transcript-api (권장, API 키 불필요)
| 목적 | 명령 |
| --- | --- |
| 한국어 자막 추출 (JSON) | `python youtube-subtitle-extractor/scripts/extract_subtitles_v2.py "<YOUTUBE_URL>" --language ko --json` |
| 영어 자막 추출 | `python youtube-subtitle-extractor/scripts/extract_subtitles_v2.py "<YOUTUBE_URL>" --language en` |
| 전체 텍스트 보기 | `python youtube-subtitle-extractor/scripts/extract_subtitles_v2.py "<YOUTUBE_URL>" --language ko --full` |
| 여러 언어 우선순위 지정 | `python youtube-subtitle-extractor/scripts/extract_subtitles_v2.py "<YOUTUBE_URL>" --language ko --language en --json` |

**장점:**
- API 키 불필요 (무료)
- 빠르고 안정적
- YouTube의 공식 자막 직접 접근
- 타임스탬프 포함된 자막 지원

**설치:**
```bash
pip install youtube-transcript-api
```

### 방법 2: Apify API (대체 방법, 메타데이터 풍부)
| 목적 | 명령 |
| --- | --- |
| 자막 + 메타데이터 추출 | `python youtube-subtitle-extractor/scripts/extract_subtitles.py "<YOUTUBE_URL>" --language ko --json` |

**장점:**
- 조회수, 좋아요, 댓글 수 등 풍부한 메타데이터
- 여러 영상 배치 처리 가능

**.env 설정 (필수):**
```
APIFY=apify_api_token
```
- 파일 위치: `ai/skills/youtube/.env` (루트 `.env` 공유 가능)
- Git에 올리지 말 것

## 워크플로
1. **요청 분석**: URL/ID 추출, 원하는 언어 파악.
2. **스크립트 선택**:
   - 자막만 필요: `extract_subtitles_v2.py` (권장)
   - 메타데이터도 필요: `extract_subtitles.py` (Apify)
3. **스크립트 실행**: 언어 및 JSON 옵션을 포함하여 실행.
4. **결과 구조화**: JSON 결과를 후속 스킬이 읽기 쉬운 형태로 전달.
5. **오류 처리**:
   - URL 파싱 실패 → 사용자에게 올바른 링크 포맷 안내
   - 자막 미존재 → "해당 영상에 공개 자막 없음" 메시지 반환
   - API 오류 → 대체 방법 시도 또는 에러 메시지 반환

## 사용 예시
- "Extract subtitles from https://www.youtube.com/watch?v=VIDEO_ID"
- "유튜브 영상 자막 추출해줘: [URL], 한국어 자막만 필요해"
- "Download subtitles (JSON) from [YouTube URL]"

## skill-creator 프롬프트 예시
```
skill-creator야, youtube-subtitle-extractor 스킬로 다음 URL의 자막을 한국어 기준 JSON으로 받아줘.
- URL: https://youtu.be/VIDEO_ID1
- 언어: ko
```

## 연계 스킬
1. `youtube-summarizer` — 추출된 자막을 구조화 요약에 사용
2. `discord-sender` — 결과물을 팀 채널에 즉시 공유
3. 기타 텍스트 분석/번역 스킬

## 도구 승인
아래 명령을 Claude Skill 허용 목록에 미리 등록하면 skill-creator가 자동으로 실행합니다.
```
Bash(python youtube-subtitle-extractor/scripts/extract_subtitles_v2.py:*)
Bash(python youtube-subtitle-extractor/scripts/extract_subtitles.py:*)
```

## 참고 파일
- `scripts/extract_subtitles_v2.py` — youtube-transcript-api 사용 (권장, API 키 불필요)
- `scripts/extract_subtitles.py` — Apify HTTP API 사용 (메타데이터 풍부)
- `README.md` — 한글 설정/사용 가이드

## 출력 예시

### extract_subtitles_v2.py (JSON 출력)
```json
{
  "success": true,
  "video_id": "a1a9wV88MSM",
  "video_url": "https://www.youtube.com/watch?v=a1a9wV88MSM",
  "language_used": "ko",
  "available_languages": [
    {
      "code": "ko",
      "language": "Korean (auto-generated)",
      "is_generated": true,
      "is_translatable": false
    }
  ],
  "transcript": [
    {
      "text": "안녕하세요. 코드 팩토리입니다.",
      "start": 0.08,
      "duration": 4.36
    }
  ],
  "transcript_merged": "안녕하세요. 코드 팩토리입니다. ...",
  "total_entries": 557,
  "total_characters": 10728
}
```
