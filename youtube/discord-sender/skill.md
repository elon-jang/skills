---
name: discord-sender
description: Discord Bot API를 이용해 지정된 채널로 텍스트 메시지를 전송하고, YouTube 워크플로 결과를 실시간으로 공유하는 스킬입니다.
version: 1.0.0
dependencies:
  - python >= 3.9
  - requests
---

# Discord Message Sender

> skill-creator 규격으로 정리된 스킬입니다. 자막 추출·요약 결과를 팀 Discord 채널에 자동 알림으로 보낼 때 사용하세요.

## 기능 요약
- Discord REST API(v10) 호출로 텍스트 메시지 전송
- `.env` 자동 탐색(스킬 디렉토리/루트/홈 디렉토리) 및 CLI 인자 지원
- 2,000자 초과 본문 자동 분할 전송(구간별 진행 로그 출력)
- HTTP 429 발생 시 `Retry-After` 헤더를 읽어 재시도

## 환경 변수(.env)
```
DISCORD_BOT_TOKEN=your_bot_token
DISCORD_CHANNEL_ID=your_channel_id
DISCORD_SERVER_ID=optional_server_id
```
- 위치: `ai/skills/youtube/.env`
- Git 추적 금지, 최소 권한(Bot: Send Messages)만 부여

## 호출 방법
| 시나리오 | 명령 |
| --- | --- |
| 기본 사용 | `python discord-sender/scripts/send_message.py "메시지 내용"` |
| 채널/토큰 수동 지정 | `python discord-sender/scripts/send_message.py "메시지" "<CHANNEL_ID>" "<BOT_TOKEN>"` |
| 파일에 있는 요약 전송 | `python discord-sender/scripts/send_message.py "$(cat summary.md)"` |

> 멀티라인 메시지는 작은따옴표 또는 히어독(`cat <<'EOF'`)으로 감싸 전송하세요.

## skill-creator 예시 프롬프트
```
skill-creator야, youtube-summarizer 결과물을 discord-sender 스킬로 #daily-video 채널에 올리는 단계를 추가해줘.
- env: DISCORD_BOT_TOKEN, DISCORD_CHANNEL_ID
- 메시지: 요약 제목 + 전체요약
```

## 워크플로 통합
1. `youtube-subtitle-extractor` → 자막 수집
2. `youtube-summarizer` → 구조화 요약 생성
3. `discord-sender` → 팀 채널에 요약·링크 공유

추가로 빌드/배포, 경고 알림, 일일 리포트에도 재사용할 수 있습니다.

## 오류 및 레이트 리밋 대응
- HTTP 401 → 토큰 불일치. 재발급 후 `.env` 갱신.
- HTTP 403 → Bot 권한 부족. Send Messages 권한 확인.
- HTTP 429 → 스크립트가 `Retry-After`(없으면 기본 2초)를 대기 후 자동 재시도(최대 3회).
- 메시지 2,000자 초과 → 자동 분할 전송. 실패 시 어떤 청크가 문제였는지 로그로 확인 가능.

## 보안 수칙
- `.env`는 저장소에 커밋하지 말 것.
- 토큰은 최소 권한 원칙 적용, 노출 시 즉시 재발급.
- 채널 ID·서버 ID는 필요 시에만 공유.

## 필수 도구 승인
```
Bash(python discord-sender/scripts/send_message.py:*)
```
skill-creator 구성에서 위 명령을 허용하면 Claude가 자동으로 메시지를 발송할 수 있습니다.
