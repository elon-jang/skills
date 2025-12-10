# URL Shortener Skill 생성 프롬프트

```
Claude Code용 URL Shortener 스킬을 만들어줘.

## 스킬 개요
- 이름: url-shortener
- 목적: 텍스트 내의 모든 URL을 Bitly API로 자동 단축
- 사용 시나리오: 사용자가 "URL 짧게 만들어줘", "URL 단축해줘" 등으로 요청할 때

## 핵심 기능
1. 텍스트에서 HTTP/HTTPS URL 자동 감지
2. Bitly API를 사용하여 각 URL을 bit.ly 링크로 단축
3. 원본 텍스트 포맷은 유지하고 URL만 교체
4. 여러 URL 동시 처리 가능
5. Verbose 모드 지원 (URL 매핑 정보 출력)

## 기술 요구사항
- Python 스크립트 (scripts/shorten_urls.py)
- Bitly API 사용
- 환경 변수: BITLY_TOKEN
- CLI 인터페이스 제공

## 사용 예시

**입력:**
```
Visit https://www.example.com/blog/2024/article and
https://docs.example.com/getting-started/guide
```

**출력:**
```
Visit https://bit.ly/3xYz123 and
https://bit.ly/4aBc789
```

**CLI 사용:**
```bash
python scripts/shorten_urls.py "텍스트 내용"
python scripts/shorten_urls.py --verbose "텍스트 내용"
```

## 문서 작성
- SKILL.md: 영문으로 스킬 정의 및 사용법
- README.md: 한글로 상세 가이드 (설치, 환경 설정, Bitly API 토큰 발급, 예제, 트러블슈팅)
- .gitignore: .env 파일 제외

나머지 구현 세부사항(함수 구조, 에러 처리, API 호출 방법 등)은 최선의 방법으로 구현해줘.
```
