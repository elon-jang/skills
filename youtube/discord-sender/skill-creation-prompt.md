# Discord Sender Skill 생성 프롬프트

```
Claude Code용 Discord Sender 스킬을 만들어줘.

## 스킬 개요
- 이름: discord-sender
- 목적: Discord Bot API를 사용하여 지정된 채널에 메시지 전송
- 사용 시나리오: YouTube 워크플로우 결과를 팀 Discord 채널에 자동 공유할 때

## 핵심 기능
1. Discord REST API v10을 통한 텍스트 메시지 전송
2. 2,000자 초과 메시지 자동 분할 전송
3. HTTP 429 레이트 리밋 자동 재시도 (Retry-After 헤더 처리)
4. 환경 변수 자동 탐색 (스킬 디렉토리/루트/홈 디렉토리)
5. CLI 인자로 채널 ID와 토큰 수동 지정 가능
6. 전송 진행 상황 로그 출력

## 기술 요구사항
- Python 스크립트: scripts/send_message.py
- Discord REST API 사용 (requests 라이브러리)
- 환경 변수:
  - DISCORD_BOT_TOKEN (필수)
  - DISCORD_CHANNEL_ID (필수)
  - DISCORD_SERVER_ID (선택)
- CLI 인터페이스

## 사용 예시

**기본 사용 (.env 파일 사용):**
```bash
python scripts/send_message.py "전송할 메시지 내용"
```

**채널/토큰 수동 지정:**
```bash
python scripts/send_message.py "메시지" "CHANNEL_ID" "BOT_TOKEN"
```

**파일 내용 전송:**
```bash
python scripts/send_message.py "$(cat summary.md)"
```

**멀티라인 메시지:**
```bash
python scripts/send_message.py "$(cat <<'EOF'
첫 번째 줄
두 번째 줄
세 번째 줄
EOF
)"
```

## 환경 변수 (.env)
```bash
DISCORD_BOT_TOKEN=your_bot_token
DISCORD_CHANNEL_ID=your_channel_id
DISCORD_SERVER_ID=optional_server_id
```

## Discord Bot 설정
1. Discord Developer Portal에서 애플리케이션 생성
2. Bot 메뉴에서 토큰 생성
3. Bot 권한에 "Send Messages" 활성화
4. OAuth2 URL Generator로 봇을 서버에 초대
5. 채널 ID 복사 (Discord 개발자 모드 활성화 필요)

## 에러 처리
- HTTP 401: 잘못된 토큰 → 재발급 안내
- HTTP 403: 권한 부족 → Send Messages 권한 확인 안내
- HTTP 429: 레이트 리밋 → Retry-After 대기 후 자동 재시도 (최대 3회)
- 2,000자 초과: 자동 분할 전송 (청크별 진행 로그)

## 통합 워크플로우
다른 스킬과의 연계:
1. youtube-subtitle-extractor → 자막 수집
2. youtube-summarizer → 구조화 요약 생성
3. discord-sender → 팀 채널에 요약·링크 공유

추가 활용:
- 빌드/배포 알림
- 일일 리포트 자동 전송
- 에러 경고 알림

## 문서 작성
- skill.md: 영문으로 스킬 정의 및 사용법
- README.md: 한글로 상세 가이드
  - Discord Bot 생성 및 설정 방법
  - 환경 변수 설정
  - 사용 예제
  - 레이트 리밋 및 에러 대응
  - 보안 주의사항 (토큰 관리)

나머지 구현 세부사항(메시지 분할 로직, API 재시도 로직, 환경 변수 탐색 등)은 최선의 방법으로 구현해줘.
```
