# YouTube Subtitle Extractor Skill

Apify API를 사용하여 YouTube 동영상의 자막과 메타데이터를 추출하는 Claude Skill입니다.

## 기능

- YouTube 동영상 URL에서 자막/트랜스크립트 추출
- 동영상 메타데이터 수집 (제목, 설명, 조회수, 좋아요 등)
- 다국어 자막 지원
- Apify의 `streamers/youtube-scraper` actor 사용

## 설치

### 1. 디렉토리 구조

```
youtube-subtitle-extractor/
├── skill.md
├── README.md
└── scripts/
    └── extract_subtitles.py
```

### 2. 환경 설정

`.env` 파일에 Apify API 키를 추가하세요:

```bash
APIFY=apify_api_YOUR_API_KEY_HERE
```

### 3. 의존성

스크립트는 필요한 패키지를 자동으로 설치합니다:
- `requests` - HTTP 요청용

## 사용법

### 명령줄에서 직접 실행

```bash
# 기본 사용
python youtube-subtitle-extractor/scripts/extract_subtitles.py "https://www.youtube.com/watch?v=VIDEO_ID"

# 언어 지정
python youtube-subtitle-extractor/scripts/extract_subtitles.py "https://www.youtube.com/watch?v=VIDEO_ID" --language ko

# JSON 출력
python youtube-subtitle-extractor/scripts/extract_subtitles.py "https://www.youtube.com/watch?v=VIDEO_ID" --json
```

### Claude에서 사용

Claude Code에서 이 스킬을 사용하려면:

1. 스킬 디렉토리를 Claude의 skills 폴더에 배치
2. Claude에게 요청:

```
유튜브 영상 자막 추출해줘: https://www.youtube.com/watch?v=VIDEO_ID
```

## 출력 예시

```
======================================================================
✅ YouTube Subtitle Extraction Successful!
======================================================================
Video ID: dQw4w9WgXcQ
Video URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Actor used: streamers/youtube-scraper

======================================================================
Subtitle Item #1
======================================================================
Available fields: title, type, id, url, viewCount, date, likes, ...

TITLE: Rick Astley - Never Gonna Give You Up (Official Video)

TEXT:
------------------------------------------------------------
The official video for "Never Gonna Give You Up" by Rick Astley...

duration: 00:03:33
```

## 지원하는 입력 형식

- 전체 YouTube URL: `https://www.youtube.com/watch?v=VIDEO_ID`
- 짧은 URL: `https://youtu.be/VIDEO_ID`
- Video ID만: `VIDEO_ID`

## 제한사항

- Apify API 크레딧이 필요합니다 (무료 플랜: 월 $5 크레딧)
- 일부 동영상은 자막이 없을 수 있습니다
- 비공개 동영상은 추출할 수 없습니다
- API 응답 시간: 약 2-10초

## 문제 해결

### "actor-is-not-rented" 에러
- Apify Console에서 해당 actor를 렌트(rent)해야 합니다
- 또는 무료 크레딧이 소진되었을 수 있습니다

### "No subtitles found"
- 해당 동영상에 자막이 없는 경우
- 자막이 비활성화되어 있는 경우

### API 키 오류
- `.env` 파일에 올바른 `APIFY` 키가 있는지 확인
- 키 형식: `apify_api_XXXXXXXXXXXXX`

## 라이센스

이 스킬은 교육 및 개인 사용 목적으로 제공됩니다.
