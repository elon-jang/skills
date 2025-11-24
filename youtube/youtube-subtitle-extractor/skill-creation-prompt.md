# YouTube Subtitle Extractor Skill 생성 프롬프트

```
Claude Code용 YouTube Subtitle Extractor 스킬을 만들어줘.

## 스킬 개요
- 이름: youtube-subtitle-extractor
- 목적: YouTube 영상의 자막을 JSON 형식으로 추출
- 사용 시나리오: 사용자가 "유튜브 자막 뽑아줘", "자막 추출해줘" 등으로 요청할 때

## 핵심 기능
1. YouTube URL 또는 Video ID로부터 자막 추출
2. 다국어 자막 지원 (언어 우선순위 지정 가능)
3. 타임스탬프 포함 자막 데이터 제공
4. JSON 형식으로 구조화된 출력
5. 자막이 없는 경우 명확한 안내

## 기술 요구사항
- Python 스크립트 (scripts/ 디렉토리)
- youtube-transcript-api 사용 (권장, API 키 불필요)
- CLI 인터페이스 (언어 선택, JSON 출력 등)

## 사용 예시

**입력:**
```bash
python scripts/extract_subtitles_v2.py "https://youtube.com/watch?v=VIDEO_ID" --language ko --json
```

**출력:**
```json
{
  "success": true,
  "video_id": "VIDEO_ID",
  "transcript": [...],
  "transcript_merged": "전체 자막 텍스트..."
}
```

## 문서 작성
- skill.md: 영문으로 스킬 정의 및 사용법
- README.md: 한글로 설치, 환경 설정, 사용 예제, 트러블슈팅

나머지 구현 세부사항은 최선의 방법으로 구현해줘.
```
