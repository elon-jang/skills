---
name: youtube-summarizer
description: YouTube 자막과 메타데이터를 입력받아 교육용으로 활용 가능한 구조화 요약(핵심 주제, 논리 전개, 데이터 인사이트, 탐구 질문 포함)을 Markdown 템플릿으로 만들어 주는 스킬입니다. Claude API를 사용한 자동 요약 생성 지원.
version: 2.0.0
dependencies:
  - python >= 3.10
  - anthropic (Claude API SDK)
---

# YouTube Video Summarizer

> skill-creator 기본 템플릿을 따르며, 자막 분석 후 구조화된 학습용 요약을 생성합니다.

## 참고 문서
- 모든 상세 지침과 출력 템플릿의 공식 버전은 `./references/summary_guide.md`에 정의되어 있습니다.
- 이 SKILL 문서는 요약된 개요만 제공하며, 세부 규칙이 변경되면 `summary_guide.md`를 최신 기준으로 삼습니다.
- Claude/skill-creator 워크플로에서는 `summary_guide.md`를 함께 로드하거나 콘텐츠를 인라인으로 전달하세요.

## 언제 이 스킬을 호출하나요?
- 사용자가 유튜브 영상을 학습·리포트용으로 요약해 달라고 요청할 때
- 이미 추출된 자막(JSON, SRT, TXT 등)과 기본 영상 정보(제목, 재생시간, URL)가 제공될 때
- 요약 결과를 다른 워크플로(예: Discord 전송, 문서 작성)에 즉시 활용해야 할 때

## 입력 요구사항
1. `transcript`: 시간 정보가 포함된 자막. 문단별 또는 타임스탬프 기반 JSON을 권장합니다.
2. `video_metadata`: 제목, 전체 재생시간(mm:ss), YouTube URL, 주요 인물/장르 등.
3. (선택) `analysis_focus`: 사용자가 강조해 달라는 포인트(예: "데이터 관점 위주", "교육 사례 강조").

## 출력 규칙
- 자막 문장을 그대로 복사하지 말고 의미를 재구성합니다.
- 외부 지식이나 추정 내용을 임의로 추가하지 않습니다.
- [mm:ss] 포맷으로 전체 재생시간·구간 시간을 표기합니다.
- direct link는 `https://www.youtube.com/watch?v=VIDEO_ID&t=000s` 형태를 유지합니다(초 단위).
- 전 섹션은 Markdown으로 출력하며, 이모지는 예시 수준에서만 사용합니다.

## 필수 섹션 템플릿
`summary_guide.md`의 "📄 출력 형식" 절에 명시된 Markdown 템플릿을 그대로 사용합니다. (상대 경로: `./references/summary_guide.md`)
````markdown
1. 제목 : { title }
2. 전체 재생시간 : { total_playback_time }
3. 전체요약
{ total_summary }

4. 구간별 요약
 - 구간1: {interval1_title}  (⏱️{time_interval1})
   {interval1_concise_summary}
   [바로가기] {direct_url_link1}

 - 구간2: {interval2_title}  (⏱️{time_interval2})
   {interval2_concise_summary}
   [바로가기] {direct_url_link2}

 - 구간3: {interval3_title}  (⏱️{time_interval3})
   {interval3_concise_summary}
   [바로가기] {direct_url_link3}
   ...
````
※ 템플릿 업데이트가 필요할 경우 `summary_guide.md`를 우선 수정한 뒤 이 문서를 보강하세요.

## 작성 가이드
1. **핵심 주제/내용**: 영상의 중심 메시지, 주요 주장·사례를 요약합니다.
2. **논리 전개**: 문제 제기 → 분석 → 결론 흐름을 명확히 밝힙니다.
3. **맥락 연결**: 배경, 인용, 산업/학습적 함의를 덧붙입니다.
4. **데이터 기반 인사이트**: 제시된 수치·비율·연도를 찾아 의미를 해석합니다.
5. **탐구형 질문 3개**:
   - 핵심 주장에 대한 비판적 사고를 유도
   - 다른 도메인으로 확장 가능성 탐색
   - 실제 적용, 한계, 향후 실험 방향 제시

## 실행 스크립트

### 방법 1: 완전 자동화 (권장) - YouTube URL → 요약 완성
```bash
# 기본 사용 (자막 추출 + AI 요약 + Discord 전송)
python youtube-summarizer/scripts/summarize_youtube.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Discord 전송 없이 요약만 생성
python youtube-summarizer/scripts/summarize_youtube.py "VIDEO_URL" --no-discord

# 영어 자막으로 요약
python youtube-summarizer/scripts/summarize_youtube.py "VIDEO_URL" --language en

# 출력 파일 지정
python youtube-summarizer/scripts/summarize_youtube.py "VIDEO_URL" -o my_summary.md

# 다른 Claude 모델 사용 (Opus)
python youtube-summarizer/scripts/summarize_youtube.py "VIDEO_URL" --model claude-opus-4-20250514
```

**필요 사항:**
- ANTHROPIC_API_KEY 환경 변수 또는 .env 파일 설정
- `youtube-subtitle-extractor` 스킬 설치
- (선택) `discord-sender` 스킬 설치

### 방법 2: 단계별 실행 - 자막 JSON 파일로부터 요약 생성
```bash
# 1단계: 자막 추출 (별도 실행)
python youtube-subtitle-extractor/scripts/extract_subtitles_v2.py "VIDEO_URL" --language ko --json > transcript.json

# 2단계: 요약 생성
python youtube-summarizer/scripts/generate_summary.py transcript.json

# 영상 정보도 함께 사용
python youtube-summarizer/scripts/generate_summary.py transcript.json --video-info video_info.json

# 출력 파일 지정
python youtube-summarizer/scripts/generate_summary.py transcript.json -o summary.md
```

**장점:**
- 각 단계를 독립적으로 실행 가능
- 중간 결과물(자막 JSON) 재사용 가능
- 디버깅이 용이

### .env 설정 (필수)
```bash
# .env 파일에 추가
ANTHROPIC_API_KEY=sk-ant-api03-...
```

**설치:**
```bash
pip install anthropic
```

## 단계별 워크플로

### 자동화된 워크플로 (summarize_youtube.py 사용 시)
1. **자막 추출**: youtube-subtitle-extractor를 자동 호출
2. **영상 정보 수집** (선택): youtube-video-info를 자동 호출
3. **AI 요약 생성**: Claude API를 사용하여 구조화된 요약 생성
4. **Discord 전송** (선택): discord-sender를 자동 호출
5. **파일 저장**: Markdown 파일로 저장

### 수동 워크플로 (generate_summary.py 사용 시)
1. **자료 확인**: 자막·메타데이터 유효성 점검, 누락 시 사용자에게 재요청.
2. **구간 분할**: 영상 러닝타임과 주제 전환을 고려해 3~5개 구간으로 나눕니다.
3. **요약 작성**: 템플릿에 맞춰 전체 요약 → 구간 요약 순으로 작성.
4. **데이터/질문 삽입**: 숫자 인사이트와 탐구형 질문을 전체요약에 통합합니다.
5. **링크/시간 검증**: direct link, [mm:ss] 포맷 오류 여부를 재확인합니다.

## 예시 출력
샘플 결과는 `summary_guide.md` 하단 "출력 예시" 절을 참고하세요. (상대 경로: `./references/summary_guide.md`)

## 연결 워크플로
1. `youtube-subtitle-extractor`로 최신 자막 확보
2. (필요 시) `youtube-video-info`로 메타데이터 보강
3. 본 스킬로 구조화된 요약 작성
4. 결과를 `discord-sender`나 문서 자동화 파이프라인으로 전달

## 도구 및 권한
아래 명령을 Claude Skill 허용 목록에 미리 등록하면 자동으로 실행됩니다.
```
Bash(python youtube-summarizer/scripts/generate_summary.py:*)
Bash(python youtube-summarizer/scripts/summarize_youtube.py:*)
```

## 참고 파일
- `scripts/summarize_youtube.py` — 완전 자동화 워크플로우 (자막 추출 → AI 요약 → Discord 전송)
- `scripts/generate_summary.py` — Claude API를 사용한 AI 요약 생성
- `references/summary_guide.md` — 요약 작성 가이드라인 및 템플릿

## 사용 예시

### 완전 자동화 워크플로우
```bash
# 유튜브 URL만 제공하면 모든 과정 자동 실행
python youtube-summarizer/scripts/summarize_youtube.py \
  "https://www.youtube.com/watch?v=a1a9wV88MSM" \
  --language ko \
  -o claude_code_tips.md

# 출력:
# ✅ 자막 추출 성공 (557개 항목, 10,728자)
# ✅ AI 요약 생성 완료 (Claude Sonnet 4)
# ✅ Discord 전송 완료
# ✅ 파일 저장: claude_code_tips.md
```

### 단계별 실행
```bash
# 1. 자막 추출
python youtube-subtitle-extractor/scripts/extract_subtitles_v2.py \
  "https://www.youtube.com/watch?v=a1a9wV88MSM" \
  --language ko --json > transcript.json

# 2. AI 요약 생성
python youtube-summarizer/scripts/generate_summary.py \
  transcript.json \
  -o summary.md

# 3. Discord 전송 (선택)
python discord-sender/scripts/send_message.py "$(cat summary.md)"
```
