# Discord Sender Skill 생성 프롬프트

```
Claude Code용 Discord Sender 스킬을 만들어줘.

## 스킬 개요
- 이름: discord-sender
- 목적: Discord 채널에 메시지 자동 전송
- 사용 시나리오: YouTube 워크플로우 결과를 팀 Discord 채널에 자동 공유할 때

## 핵심 기능
1. Discord 채널에 텍스트 메시지 전송
2. 긴 메시지 자동 분할 전송 (2,000자 제한)
3. 레이트 리밋 자동 재시도
4. 파일 내용도 쉽게 전송 가능
5. 환경 변수 또는 CLI 인자로 설정

## 기술 요구사항
- Python 스크립트 (scripts/ 디렉토리)
- Discord Bot API 사용
- 환경 변수: DISCORD_BOT_TOKEN, DISCORD_CHANNEL_ID
- CLI 인터페이스

## 사용 예시

**입력:**
```bash
python scripts/send_message.py "전송할 메시지"
python scripts/send_message.py "$(cat summary.md)"
```

## 환경 변수
```bash
DISCORD_BOT_TOKEN=your_bot_token
DISCORD_CHANNEL_ID=your_channel_id
```

## 문서 작성
- skill.md: 영문으로 스킬 정의 및 사용법
- README.md: 한글로 Discord Bot 설정 방법, 환경 변수, 사용 예제

나머지 구현 세부사항은 최선의 방법으로 구현해줘.
```
