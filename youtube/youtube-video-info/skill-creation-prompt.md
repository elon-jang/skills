# YouTube Video Info Skill 생성 프롬프트

```
Claude Code용 YouTube Video Info 스킬을 만들어줘.

## 스킬 개요
- 이름: youtube-video-info
- 목적: YouTube 영상의 메타데이터와 통계 정보 조회
- 사용 시나리오: 사용자가 "유튜브 영상 정보 알려줘", "조회수 확인해줘" 등으로 요청할 때

## 핵심 기능
1. YouTube URL 또는 Video ID로 영상 정보 조회
2. 기본 정보 (제목, 설명, 재생시간, 게시일)
3. 통계 정보 (조회수, 좋아요, 댓글 수)
4. 채널 정보 (채널명, 채널 ID)
5. JSON 또는 읽기 쉬운 형식으로 출력

## 기술 요구사항
- Python 스크립트 (scripts/ 디렉토리)
- YouTube Data API v3 사용
- 환경 변수: GOOGLE_API_KEY
- CLI 인터페이스

## 사용 예시

**입력:**
```bash
python scripts/get_video_info.py "https://youtube.com/watch?v=VIDEO_ID" --json
```

**출력:**
```json
{
  "title": "영상 제목",
  "channel_name": "채널명",
  "view_count": 1234567,
  "like_count": 12345,
  "duration": "PT10M30S"
}
```

## 문서 작성
- SKILL.md: 영문으로 스킬 정의, API 키 발급 방법, 사용 예제

나머지 구현 세부사항은 최선의 방법으로 구현해줘.
```
