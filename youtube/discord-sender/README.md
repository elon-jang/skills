# Discord Message Sender Skill

Discord 채널에 메시지를 전송하는 Claude 스킬입니다.

## 기능

- Discord Bot API(v10)를 사용한 메시지 전송
- `.env` 자동 탐색(스킬 폴더, 저장소 루트, 홈 디렉토리) 및 환경 변수 병합
- 2,000자 이상의 본문을 자동으로 분할하여 순차 전송
- HTTP 429 발생 시 `Retry-After` 헤더 기반 지연 후 재시도
- 유튜브 워크플로와의 통합 지원

## 설치

### 필수 라이브러리

```bash
pip install requests
```

### Claude Code에 스킬 등록

```bash
ln -s /Users/elon/Downloads/tpm/ai/skills/youtube/discord-sender /Users/elon/.claude/skills/discord-sender
```

## 환경 설정

`.env` 파일에 다음 정보를 추가하세요:

```env
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_CHANNEL_ID=your_channel_id_here
DISCORD_SERVER_ID=your_server_id_here
```

## Discord Bot 생성 방법

1. [Discord Developer Portal](https://discord.com/developers/applications)에 접속
2. "New Application" 클릭하여 새 애플리케이션 생성
3. 좌측 메뉴에서 "Bot" 선택
4. "Add Bot" 클릭
5. "Reset Token" 클릭하여 Bot Token 생성 및 복사
6. "MESSAGE CONTENT INTENT" 활성화 (필요시)
7. 좌측 메뉴에서 "OAuth2" > "URL Generator" 선택
8. Scopes에서 "bot" 선택
9. Bot Permissions에서 "Send Messages" 선택
10. 생성된 URL로 Bot을 서버에 초대

## 사용 방법

### 기본 사용

```bash
python discord-sender/scripts/send_message.py "메시지 내용"
```

### 특정 채널에 전송

```bash
python discord-sender/scripts/send_message.py "메시지" "채널_ID" "봇_토큰"
```

### Claude Code에서 사용

```
Discord에 "테스트 메시지"를 전송해줘
```

## 워크플로 예제

### 유튜브 요약 → Discord 전송

```bash
# 1단계: 유튜브 자막 추출
python youtube-subtitle-extractor/scripts/extract_subtitles.py "https://www.youtube.com/watch?v=vqLONWXfMsI"

# 2단계: 자막 요약 (Claude Code에서)
# "위 자막을 youtube-summarizer로 요약해줘"

# 3단계: Discord로 전송 (Claude Code에서)
# "위 요약을 Discord에 전송해줘"
```

## 출력 예제

```
======================================================================
🚀 Discord Message Sender
======================================================================
Message: 안녕하세요! Claude에서 보내는 메시지입니다.
----------------------------------------------------------------------
✅ SUCCESS!
Message ID: 1234567890123456789
Channel ID: 1439908670552150140
Timestamp: 2025-11-17T12:00:00.000000+00:00
======================================================================
```

## 제한사항

- API 정책상 단일 메시지는 2,000자를 넘을 수 없으므로 자동 분할 전송이 이루어집니다.
- Rate Limit: Discord API는 요청량을 제한합니다. 스크립트가 최대 3회까지 자동 재시도하지만, 반복적인 초과 시 수동 대기가 필요할 수 있습니다.
- Bot은 초대된 서버/채널에서만 메시지를 전송할 수 있습니다.

## 보안

- `.env` 파일은 절대 Git에 커밋하지 마세요
- Bot 토큰은 외부에 노출되지 않도록 주의하세요
- `.gitignore`에 `.env` 추가 권장

## 연관 스킬

- **youtube-subtitle-extractor**: 유튜브 자막 추출
- **youtube-summarizer**: 유튜브 영상 요약
- **youtube-video-info**: 유튜브 영상 정보 조회

## 라이선스

MIT
