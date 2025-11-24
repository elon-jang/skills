# Claude Code Skills Collection

Claude Code에서 사용할 수 있는 커스텀 스킬 모음입니다. 각 스킬은 특정 작업을 자동화하고 Claude의 기능을 확장합니다.

## 스킬 목록

### 📌 URL Shortener

텍스트 내의 모든 URL을 Bitly API를 사용하여 자동으로 단축합니다.

**주요 기능:**
- HTTP/HTTPS URL 자동 감지 및 단축
- 여러 URL 동시 처리
- 원본 텍스트 포맷 유지
- Verbose 모드로 상세 진행 상황 확인

**사용 예시:**
```bash
python url-shortener/scripts/shorten_urls.py "Visit https://www.example.com/blog/2024/article"
```

**상세 문서:** [url-shortener/README.md](./url-shortener/README.md)

---

### 🎥 YouTube 관련 스킬

YouTube 영상의 자막 추출, 요약, 메타데이터 조회, Discord 공유를 지원하는 통합 워크플로우입니다.

#### 1. YouTube Subtitle Extractor

YouTube 영상의 자막과 메타데이터를 JSON 형식으로 추출합니다.

**주요 기능:**
- youtube-transcript-api 사용 (권장, API 키 불필요)
- Apify API 대체 지원 (풍부한 메타데이터)
- 다국어 자막 지원 (한국어, 영어 등)
- 타임스탬프 포함 자막 추출

**사용 예시:**
```bash
python youtube/youtube-subtitle-extractor/scripts/extract_subtitles_v2.py "https://youtube.com/watch?v=VIDEO_ID" --language ko --json
```

**상세 문서:** [youtube/youtube-subtitle-extractor/README.md](./youtube/youtube-subtitle-extractor/README.md)

---

#### 2. YouTube Summarizer

YouTube 자막을 교육용으로 활용 가능한 구조화된 요약으로 변환합니다.

**주요 기능:**
- Claude API를 사용한 AI 기반 요약 생성
- 구간별 상세 요약 (타임스탬프 포함)
- 핵심 주제, 논리 전개, 데이터 인사이트 분석
- 탐구형 질문 생성
- 완전 자동화 워크플로우 (자막 추출 → AI 요약 → Discord 전송)

**사용 예시:**
```bash
# 완전 자동화
python youtube/youtube-summarizer/scripts/summarize_youtube.py "https://youtube.com/watch?v=VIDEO_ID"

# 단계별 실행
python youtube/youtube-summarizer/scripts/generate_summary.py transcript.json
```

**상세 문서:** [youtube/youtube-summarizer/README.md](./youtube/youtube-summarizer/README.md)

---

#### 3. YouTube Video Info

YouTube Data API v3를 사용하여 영상의 상세 정보를 조회합니다.

**주요 기능:**
- 영상 메타데이터 조회 (제목, 설명, 재생시간)
- 통계 정보 (조회수, 좋아요, 댓글 수)
- 채널 정보 조회
- JSON 또는 사람이 읽기 쉬운 형식 출력

**사용 예시:**
```bash
python youtube/youtube-video-info/scripts/get_video_info.py "VIDEO_ID" --json
```

**상세 문서:** [youtube/youtube-video-info/SKILL.md](./youtube/youtube-video-info/SKILL.md)

---

#### 4. Discord Sender

Discord Bot API를 사용하여 지정된 채널에 메시지를 전송합니다.

**주요 기능:**
- Discord REST API를 통한 메시지 전송
- 2,000자 초과 메시지 자동 분할 전송
- HTTP 429 레이트 리밋 자동 재시도
- YouTube 워크플로우 결과 실시간 공유

**사용 예시:**
```bash
python youtube/discord-sender/scripts/send_message.py "메시지 내용"
```

**상세 문서:** [youtube/discord-sender/README.md](./youtube/discord-sender/README.md)

---

## 스킬 생성 프롬프트

각 스킬을 처음부터 직접 만들고 싶다면 아래 프롬프트를 참고하세요. 프롬프트를 Claude Code에 입력하면 해당 스킬을 자동으로 생성할 수 있습니다.

### 📝 URL Shortener
**프롬프트 파일:** [url-shortener/skill-creation-prompt.md](./url-shortener/skill-creation-prompt.md)

텍스트 내 모든 URL을 Bitly API로 자동 단축하는 스킬을 생성하는 프롬프트입니다. 핵심 요구사항과 기대 동작만 명시하고, 구현 세부사항은 Claude에게 위임하는 방식으로 작성되었습니다.

### 🎥 YouTube 관련 스킬 (예정)
YouTube 워크플로우 스킬들의 생성 프롬프트도 순차적으로 추가될 예정입니다.

---

## 설치 및 설정

### 1. 스킬 디렉토리 구조

```
skills/
├── README.md                    # 이 파일
├── url-shortener/               # URL 단축 스킬
│   ├── README.md
│   ├── SKILL.md
│   ├── .env
│   └── scripts/
│       └── shorten_urls.py
└── youtube/                     # YouTube 관련 스킬
    ├── discord-sender/
    │   ├── README.md
    │   ├── skill.md
    │   └── scripts/
    │       └── send_message.py
    ├── youtube-subtitle-extractor/
    │   ├── README.md
    │   ├── skill.md
    │   └── scripts/
    │       ├── extract_subtitles.py
    │       └── extract_subtitles_v2.py
    ├── youtube-summarizer/
    │   ├── README.md
    │   ├── skill.md
    │   ├── references/
    │   │   └── summary_guide.md
    │   └── scripts/
    │       ├── generate_summary.py
    │       └── summarize_youtube.py
    └── youtube-video-info/
        ├── SKILL.md
        └── scripts/
            └── get_video_info.py
```

### 2. 의존성 패키지 설치

각 스킬별로 필요한 Python 패키지를 설치합니다:

```bash
# URL Shortener
pip install requests python-dotenv

# YouTube Subtitle Extractor
pip install youtube-transcript-api requests python-dotenv

# YouTube Summarizer
pip install anthropic python-dotenv

# YouTube Video Info
pip install requests python-dotenv

# Discord Sender
pip install requests python-dotenv
```

또는 모든 패키지를 한 번에 설치:

```bash
pip install requests python-dotenv youtube-transcript-api anthropic
```

### 3. 환경 변수 설정

각 스킬 디렉토리 또는 상위 디렉토리에 `.env` 파일을 생성하고 필요한 API 키를 설정합니다:

#### URL Shortener (.env)
```bash
BITLY_TOKEN=your_bitly_api_token_here
```

#### YouTube Subtitle Extractor - Apify 사용 시 (.env)
```bash
APIFY=apify_api_token
```

#### YouTube Summarizer (.env)
```bash
ANTHROPIC_API_KEY=sk-ant-api03-...
```

#### YouTube Video Info (.env)
```bash
GOOGLE_API_KEY=your_google_api_key_here
```

#### Discord Sender (.env)
```bash
DISCORD_BOT_TOKEN=your_bot_token
DISCORD_CHANNEL_ID=your_channel_id
DISCORD_SERVER_ID=optional_server_id
```

### 4. Claude Code에 스킬 등록

각 스킬을 Claude Code에서 사용할 수 있도록 심볼릭 링크를 생성합니다:

```bash
# URL Shortener
ln -s ~/elon/tpm/ai/skills/url-shortener ~/.claude/skills/url-shortener

# YouTube 스킬들
ln -s ~/elon/tpm/ai/skills/youtube/discord-sender ~/.claude/skills/discord-sender
ln -s ~/elon/tpm/ai/skills/youtube/youtube-subtitle-extractor ~/.claude/skills/youtube-subtitle-extractor
ln -s ~/elon/tpm/ai/skills/youtube/youtube-summarizer ~/.claude/skills/youtube-summarizer
ln -s ~/elon/tpm/ai/skills/youtube/youtube-video-info ~/.claude/skills/youtube-video-info
```

## 통합 워크플로우 예시

### YouTube 영상 자동 요약 및 공유

YouTube 영상 URL 하나로 자막 추출, 요약 생성, Discord 공유까지 자동으로 처리:

```bash
# 완전 자동화 워크플로우
python youtube/youtube-summarizer/scripts/summarize_youtube.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

이 명령어는 다음 과정을 자동으로 수행합니다:
1. **자막 추출** (youtube-subtitle-extractor)
2. **영상 정보 수집** (youtube-video-info, 선택)
3. **AI 요약 생성** (youtube-summarizer + Claude API)
4. **Discord 전송** (discord-sender)
5. **Markdown 파일 저장**

### URL이 포함된 텍스트 단축 및 공유

```bash
# 1. URL 단축
python url-shortener/scripts/shorten_urls.py "$(cat document.txt)" > shortened.txt

# 2. Discord로 전송
python youtube/discord-sender/scripts/send_message.py "$(cat shortened.txt)"
```

## Claude Code에서 사용하기

Claude Code 대화에서 직접 스킬을 호출할 수 있습니다:

### URL 단축 예시
```
사용자: 이 텍스트의 URL을 짧게 만들어줘:
Visit https://www.example.com/blog/2024/article
```

### YouTube 요약 예시
```
사용자: 이 유튜브 영상을 요약해줘:
https://www.youtube.com/watch?v=VIDEO_ID
```

Claude가 자동으로 적절한 스킬을 선택하여 작업을 수행합니다.

## API 키 발급 방법

### Bitly API Token
1. [Bitly 회원가입](https://bitly.com/a/sign_up)
2. Settings → Developer Settings → API로 이동
3. Access Token 생성
4. `.env` 파일에 저장

### Anthropic API Key (Claude)
1. [Anthropic Console](https://console.anthropic.com/)에서 계정 생성
2. API Keys 메뉴에서 새 키 생성
3. `.env` 파일에 저장

### Google API Key (YouTube Data API)
1. [Google Cloud Console](https://console.cloud.google.com/)에서 프로젝트 생성
2. YouTube Data API v3 활성화
3. API 및 서비스 → 사용자 인증 정보에서 API 키 생성
4. `.env` 파일에 저장

### Discord Bot Token
1. [Discord Developer Portal](https://discord.com/developers/applications)에서 애플리케이션 생성
2. Bot 메뉴에서 토큰 생성
3. Bot 권한에서 "Send Messages" 권한 활성화
4. 봇을 Discord 서버에 초대
5. 채널 ID 복사 (개발자 모드 활성화 필요)
6. `.env` 파일에 저장

## 트러블슈팅

### "API Token not found" 오류
- `.env` 파일이 올바른 위치에 있는지 확인
- 환경 변수 이름이 정확한지 확인
- `python-dotenv` 패키지가 설치되어 있는지 확인

### "Module not found" 오류
```bash
pip install requests python-dotenv youtube-transcript-api anthropic
```

### Discord 메시지 전송 실패
- Bot 토큰과 채널 ID가 올바른지 확인
- Bot에게 "Send Messages" 권한이 부여되었는지 확인
- 봇이 해당 채널에 접근할 수 있는지 확인

### YouTube 자막 추출 실패
- 영상에 공개 자막이 있는지 확인
- URL 형식이 올바른지 확인
- 인터넷 연결 상태 확인

## 보안 주의사항

1. **`.env` 파일을 Git에 커밋하지 마세요**
   - `.gitignore`에 `.env` 추가
   - API 키가 노출되지 않도록 주의

2. **최소 권한 원칙 적용**
   - Discord Bot은 필요한 최소 권한만 부여
   - API 키는 필요한 서비스에만 접근 가능하도록 설정

3. **API 키 주기적 갱신**
   - 정기적으로 API 키를 재발급하여 보안 강화

## 기여 및 이슈

이슈나 개선 사항은 [GitHub Repository](https://github.com/elon-jang/skills)에 제보해주세요.

## 라이선스

This is a personal skills collection for Claude Code.
