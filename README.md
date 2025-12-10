# Claude Code Skills Collection

Claude Code에서 사용할 수 있는 커스텀 스킬 모음입니다. 각 스킬은 특정 작업을 자동화하고 Claude의 기능을 확장합니다.

## 스킬 목록

### 📌 [URL Shortener](./url-shortener/README.md)

Bitly API로 텍스트 내 모든 URL을 자동 단축하는 스킬입니다.

- HTTP/HTTPS URL 자동 감지 및 단축
- 원본 텍스트 포맷 유지

### 🎥 YouTube 워크플로우 스킬

YouTube 영상 자막 추출부터 AI 요약, Discord 공유까지 완전 자동화된 통합 워크플로우를 제공합니다.

#### [YouTube Subtitle Extractor](./youtube/youtube-subtitle-extractor/README.md)

YouTube 영상의 자막과 메타데이터를 JSON으로 추출합니다.

- youtube-transcript-api 또는 Apify API 지원
- 다국어 자막, 타임스탬프 포함

#### [YouTube Summarizer](./youtube/youtube-summarizer/README.md)

YouTube 자막을 교육용 구조화 요약으로 변환합니다.

- Claude API 기반 AI 요약 생성
- 구간별 상세 요약, 탐구형 질문 생성
- 완전 자동화 워크플로우

#### [YouTube Video Info](./youtube/youtube-video-info/SKILL.md)

YouTube Data API v3로 영상 상세 정보를 조회합니다.

- 메타데이터, 통계 정보, 채널 정보 조회

#### [Discord Sender](./youtube/discord-sender/README.md)

Discord Bot API로 메시지를 자동 전송합니다.

- 2,000자 초과 자동 분할, 레이트 리밋 재시도

---

## 빠른 시작

### 설치

```bash
# 의존성 설치
pip install requests python-dotenv youtube-transcript-api anthropic

# Claude Code에 스킬 등록 (심볼릭 링크)
ln -s ~/path/to/ai/skills/url-shortener ~/.claude/skills/url-shortener
ln -s ~/path/to/ai/skills/youtube/youtube-subtitle-extractor ~/.claude/skills/youtube-subtitle-extractor
ln -s ~/path/to/ai/skills/youtube/youtube-summarizer ~/.claude/skills/youtube-summarizer
ln -s ~/path/to/ai/skills/youtube/youtube-video-info ~/.claude/skills/youtube-video-info
ln -s ~/path/to/ai/skills/youtube/discord-sender ~/.claude/skills/discord-sender
```

### 환경 변수 설정

각 스킬 디렉토리에 `.env` 파일을 생성하고 필요한 API 키를 설정하세요.

```bash
# URL Shortener
BITLY_TOKEN=your_token

# YouTube Summarizer
ANTHROPIC_API_KEY=sk-ant-api03-...

# YouTube Video Info
GOOGLE_API_KEY=your_key

# Discord Sender
DISCORD_BOT_TOKEN=your_token
DISCORD_CHANNEL_ID=your_channel_id
```

### 통합 워크플로우 예시

**YouTube 영상 완전 자동 요약:**

```bash
python youtube/youtube-summarizer/scripts/summarize_youtube.py "https://youtube.com/watch?v=VIDEO_ID"
```

자막 추출 → AI 요약 → Discord 전송 → Markdown 저장까지 자동 처리됩니다.

## API 키 발급

- **Bitly:** [bitly.com/a/sign_up](https://bitly.com/a/sign_up)
- **Anthropic (Claude):** [console.anthropic.com](https://console.anthropic.com/)
- **Google (YouTube):** [console.cloud.google.com](https://console.cloud.google.com/)
- **Discord Bot:** [discord.com/developers/applications](https://discord.com/developers/applications)

자세한 설정 방법은 각 스킬의 README.md를 참고하세요.

## 보안 주의

- `.env` 파일을 Git에 커밋하지 마세요
- `.gitignore`에 `.env` 추가
- API 키는 주기적으로 갱신하세요
