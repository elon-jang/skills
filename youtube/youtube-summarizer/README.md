# YouTube Video Summarizer Skill

유튜브 영상의 자막을 분석하여 학습용으로 구조화된 요약을 생성하는 Claude 스킬입니다.

## 기능

- 유튜브 영상 자막을 논리적이고 통찰적으로 요약
- 핵심 주제, 핵심 내용, 논리 전개, 맥락 연결 분석
- 숫자 기반 인사이트 추출
- 탐구형 질문 생성
- 구간별 요약 및 타임스탬프 링크 제공

## 설치 방법

### Claude Code에서 설치

```bash
# 스킬 디렉토리로 이동
cd /Users/elon/.claude/skills

# 현재 디렉토리를 심볼릭 링크로 연결
ln -s /Users/elon/Downloads/tpm/ai/skills/youtube/youtube-summarizer youtube-summarizer
```

또는 skill.md 파일을 직접 복사:

```bash
cp /Users/elon/Downloads/tpm/ai/skills/youtube/youtube-summarizer/skill.md /Users/elon/.claude/skills/youtube-summarizer/skill.md
```

### Claude Web에서 설치

1. Claude Web에 접속
2. 설정 > 스킬 메뉴로 이동
3. "커스텀 스킬 추가" 클릭
4. skill.md의 내용을 복사하여 붙여넣기

## 사용 방법

### 기본 사용법

```
유튜브 영상 https://www.youtube.com/watch?v=VIDEO_ID를 요약해줘
```

### 워크플로 사용법

1. 자막 추출:
```
python youtube-subtitle-extractor/scripts/extract_subtitles.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

2. 요약 생성:
```
위에서 추출한 자막을 youtube-summarizer 스킬을 사용해서 요약해줘
```

## 출력 형식

요약 결과는 다음 형식으로 제공됩니다:

1. **제목**: 영상 제목
2. **전체 재생시간**: [mm:ss] 형식
3. **전체요약**:
   - 🎯 핵심 주제
   - 💡 핵심 내용
   - 🔍 논리 전개
   - 🧩 맥락 연결
   - 🔢 숫자 기반 인사이트
   - 🧠 탐구형 질문
4. **구간별 요약**: 타임스탬프 링크와 함께 제공

## 연관 스킬

- **youtube-subtitle-extractor**: 유튜브 영상의 자막을 추출
- **youtube-video-info**: 유튜브 영상의 메타데이터를 추출

## 요구사항

- Claude Code 또는 Claude Web
- youtube-subtitle-extractor 스킬 (자막 추출용)

## 라이선스

MIT
