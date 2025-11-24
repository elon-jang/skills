# YouTube Summarizer Skill 생성 프롬프트

```
Claude Code용 YouTube Summarizer 스킬을 만들어줘.

## 스킬 개요
- 이름: youtube-summarizer
- 목적: YouTube 자막을 교육용 구조화 요약으로 자동 변환
- 사용 시나리오: 사용자가 "유튜브 영상 요약해줘", "이 영상 정리해줘" 등으로 요청할 때

## 핵심 기능
1. YouTube URL만 입력하면 자막 추출부터 요약 생성까지 완전 자동화
2. Claude API 사용하여 고품질 AI 요약 생성
3. 구간별 상세 요약 (타임스탬프 및 바로가기 링크)
4. 핵심 인사이트와 탐구형 질문 생성
5. Markdown 파일로 저장
6. Discord 자동 전송 지원 (선택)

## 기술 요구사항
- Python 스크립트 (scripts/ 디렉토리)
- Claude API 연동
- 환경 변수: ANTHROPIC_API_KEY
- youtube-subtitle-extractor 스킬과 연계
- CLI 인터페이스

## 사용 예시

**입력:**
```bash
python scripts/summarize_youtube.py "https://youtube.com/watch?v=VIDEO_ID"
```

**출력 (Markdown):**
```markdown
# 제목: {영상 제목}
**전체 재생시간:** {mm:ss}

## 전체요약
{핵심 요약}

## 구간별 요약
### 구간1: {제목} (⏱️ 00:00-05:30)
{내용}
[바로가기](링크)

## 핵심 인사이트
- {인사이트 1}

## 탐구 질문
1. {질문 1}
```

## 문서 작성
- skill.md: 영문으로 스킬 정의 및 워크플로우
- README.md: 한글로 설치, API 키 설정, 사용 예제
- references/summary_guide.md: 요약 가이드라인

나머지 구현 세부사항은 최선의 방법으로 구현해줘.
```
