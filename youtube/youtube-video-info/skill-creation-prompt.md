# YouTube Video Info Skill 생성 프롬프트

```
Claude Code용 YouTube Video Info 스킬을 만들어줘.

## 스킬 개요
- 이름: youtube-video-info
- 목적: YouTube Data API v3를 사용하여 영상의 상세 정보 조회
- 사용 시나리오: 사용자가 "유튜브 영상 정보 알려줘", "조회수 몇인지 확인해줘" 등으로 요청할 때

## 핵심 기능
1. YouTube URL 또는 Video ID로부터 영상 메타데이터 조회
2. 영상 기본 정보 (제목, 설명, 재생시간, 게시일)
3. 통계 정보 (조회수, 좋아요 수, 댓글 수)
4. 채널 정보 (채널명, 채널 ID)
5. 추가 정보 (태그, 카테고리, 썸네일 URL)
6. JSON 또는 사람이 읽기 쉬운 형식 출력

## 기술 요구사항
- Python 스크립트: scripts/get_video_info.py
- Google YouTube Data API v3 사용
- 환경 변수: GOOGLE_API_KEY
- CLI 인터페이스 제공 (--json, --api-key 플래그)

## 사용 예시

**기본 사용:**
```bash
python scripts/get_video_info.py "https://youtube.com/watch?v=VIDEO_ID"
```

**JSON 출력:**
```bash
python scripts/get_video_info.py "VIDEO_ID" --json
```

**API 키 직접 지정:**
```bash
python scripts/get_video_info.py "VIDEO_ID" --api-key "YOUR_API_KEY"
```

**출력 예시 (사람이 읽기 쉬운 형식):**
```
Title: 영상 제목
Channel: 채널명
Published: 2024-01-15
Duration: PT10M30S (10분 30초)
Views: 1,234,567
Likes: 12,345
Comments: 890
Description: 영상 설명 (처음 300자)...
```

**출력 예시 (JSON):**
```json
{
  "video_id": "VIDEO_ID",
  "title": "영상 제목",
  "description": "영상 설명",
  "channel_name": "채널명",
  "channel_id": "CHANNEL_ID",
  "published_at": "2024-01-15T10:30:00Z",
  "duration": "PT10M30S",
  "view_count": 1234567,
  "like_count": 12345,
  "comment_count": 890,
  "tags": ["tag1", "tag2"],
  "thumbnails": {
    "default": "https://...",
    "medium": "https://...",
    "high": "https://..."
  }
}
```

## API 키 설정
.env 파일 또는 환경 변수로 설정:
```bash
GOOGLE_API_KEY=your_google_api_key_here
```

## 지원 URL 형식
- 전체 URL: https://www.youtube.com/watch?v=VIDEO_ID
- 짧은 URL: https://youtu.be/VIDEO_ID
- Video ID만: VIDEO_ID (11자)

## 문서 작성
- SKILL.md: 영문으로 스킬 정의 및 사용법
  - API 키 발급 방법 (Google Cloud Console)
  - YouTube Data API v3 활성화 방법
  - 사용 예제
  - 출력 정보 상세 설명
  - 에러 처리 (잘못된 Video ID, API 할당량 초과 등)

나머지 구현 세부사항(URL 파싱, API 호출, 응답 포맷팅 등)은 최선의 방법으로 구현해줘.
```
