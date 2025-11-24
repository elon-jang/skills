# YouTube Summarizer Skill 생성 프롬프트

```
Claude Code용 YouTube Summarizer 스킬을 만들어줘.

## 스킬 개요
- 이름: youtube-summarizer
- 목적: YouTube 자막을 교육용으로 활용 가능한 구조화된 요약으로 변환
- 사용 시나리오: 사용자가 "유튜브 영상 요약해줘", "이 영상 정리해줘" 등으로 요청할 때

## 핵심 기능
1. YouTube URL → 자막 추출 → AI 요약 → 파일 저장까지 완전 자동화
2. Claude API를 사용한 고품질 AI 요약 생성
3. 구간별 상세 요약 (타임스탬프 및 바로가기 링크 포함)
4. 핵심 주제, 논리 전개, 데이터 인사이트 분석
5. 탐구형 질문 생성
6. Discord 자동 전송 지원 (선택)
7. Markdown 형식으로 구조화된 출력

## 기술 요구사항
- Python 스크립트 2개:
  - scripts/summarize_youtube.py (완전 자동화 워크플로우)
  - scripts/generate_summary.py (자막 JSON → AI 요약)
- Claude API 사용 (Anthropic SDK)
- 환경 변수: ANTHROPIC_API_KEY
- youtube-subtitle-extractor 스킬 통합
- discord-sender 스킬 통합 (선택)

## 사용 예시

**완전 자동화:**
```bash
python scripts/summarize_youtube.py "https://youtube.com/watch?v=VIDEO_ID"
```

**옵션:**
```bash
# Discord 전송 없이
python scripts/summarize_youtube.py "VIDEO_URL" --no-discord

# 영어 자막으로
python scripts/summarize_youtube.py "VIDEO_URL" --language en

# 출력 파일 지정
python scripts/summarize_youtube.py "VIDEO_URL" -o summary.md

# Claude Opus 모델 사용
python scripts/summarize_youtube.py "VIDEO_URL" --model claude-opus-4-20250514
```

**단계별 실행:**
```bash
# 1. 자막 추출 (별도)
python ../youtube-subtitle-extractor/scripts/extract_subtitles_v2.py "VIDEO_URL" --language ko --json > transcript.json

# 2. AI 요약 생성
python scripts/generate_summary.py transcript.json -o summary.md
```

## 출력 형식 (Markdown)

```markdown
# 제목: {영상 제목}
**전체 재생시간:** {mm:ss}

## 전체요약
{3-5줄 핵심 요약}

## 구간별 요약

### 구간1: {구간 제목} (⏱️ 00:00-05:30)
{구간 내용 요약}
[바로가기](https://youtube.com/watch?v=VIDEO_ID&t=0s)

### 구간2: {구간 제목} (⏱️ 05:30-12:00)
{구간 내용 요약}
[바로가기](https://youtube.com/watch?v=VIDEO_ID&t=330s)

## 핵심 인사이트
- {데이터 기반 인사이트 1}
- {데이터 기반 인사이트 2}

## 탐구 질문
1. {비판적 사고 질문}
2. {확장 가능성 질문}
3. {실제 적용 질문}
```

## 워크플로우
1. YouTube URL 입력 받기
2. youtube-subtitle-extractor 자동 호출하여 자막 추출
3. (선택) youtube-video-info 호출하여 메타데이터 수집
4. Claude API로 구조화된 요약 생성
5. Markdown 파일로 저장
6. (선택) discord-sender로 팀 채널에 공유

## 문서 작성
- skill.md: 영문으로 스킬 정의 및 워크플로우
- README.md: 한글로 상세 가이드
  - Claude API 키 발급 방법
  - 완전 자동화 vs 단계별 실행 비교
  - 출력 템플릿 상세 설명
  - references/summary_guide.md 참조
- references/summary_guide.md: 요약 작성 가이드라인

나머지 구현 세부사항(Claude API 프롬프트, 구간 분할 로직, 타임스탬프 변환 등)은 최선의 방법으로 구현해줘.
```
