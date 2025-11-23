# URL Shortener Skill

Claude Code 스킬로, 텍스트 내의 모든 URL을 Bitly API를 사용하여 자동으로 단축합니다.

## 특징

- 텍스트 내의 모든 HTTP/HTTPS URL 자동 감지
- Bitly API를 통한 URL 단축
- 원본 텍스트 포맷 유지
- 여러 URL 동시 처리
- Verbose 모드로 상세 진행 상황 확인

## 설치

### 1. 의존성 패키지 설치

```bash
pip install requests python-dotenv
```

### 2. Bitly API 토큰 설정

Bitly API 토큰을 환경 변수나 `.env` 파일로 설정해야 합니다.

작업 디렉토리에 `.env` 파일을 생성하고 다음과 같이 작성:

```bash
BITLY_TOKEN=your_bitly_api_token_here
```

#### Bitly 토큰 발급 방법

1. [Bitly 회원가입](https://bitly.com/a/sign_up)
2. Settings → Developer Settings → API로 이동
3. Access Token 생성
4. 생성된 토큰을 `.env` 파일에 저장

### 3. Claude Code에 스킬 등록

```bash
# 심볼릭 링크 생성
ln -s ~/elon/tpm/ai/skills/url-shorten/url-shortener ~/.claude/skills/url-shortener
```

## 사용 방법

### 기본 사용

```bash
python scripts/shorten_urls.py "Check out this article: https://www.example.com/very/long/path/to/article"
```

### Verbose 모드

URL 단축 과정과 매핑 정보를 확인하려면:

```bash
python scripts/shorten_urls.py --verbose "Your text with URLs here"
# 또는
python scripts/shorten_urls.py -v "Your text with URLs here"
```

### Claude Code에서 사용

Claude Code 대화에서 직접 URL 단축 요청:

```
사용자: 이 텍스트의 URL을 짧게 만들어줘:
Visit https://www.example.com/blog/2024/article and
https://docs.example.com/getting-started/installation/guide
```

## 사용 예제

### 예제 1: 단일 URL 단축

**입력:**
```
Check out this article: https://www.example.com/very/long/path/to/article
```

**출력:**
```
Check out this article: https://bit.ly/3xYz123
```

### 예제 2: 여러 URL 단축

**입력:**
```
Visit our website at https://www.example.com/blog/2024/article and
documentation at https://docs.example.com/getting-started/installation/guide
```

**출력:**
```
Visit our website at https://bit.ly/3xYz123 and
documentation at https://bit.ly/4aBc789
```

### 예제 3: 파일의 URL 단축

```bash
# 파일에서 읽어서 URL을 단축하고 새 파일로 저장
python scripts/shorten_urls.py "$(cat input.txt)" > output.txt
```

## 스킬 구조

```
url-shortener/
├── README.md                    # 이 파일
├── SKILL.md                     # Claude Code 스킬 정의
└── scripts/
    └── shorten_urls.py          # URL 단축 스크립트
```

### 핵심 컴포넌트

#### `shorten_urls.py`

Python 스크립트로 다음 기능 제공:

1. **URL 추출**: 정규식을 사용하여 텍스트에서 모든 HTTP/HTTPS URL 추출
2. **Bitly API 호출**: 각 URL을 Bitly API로 단축
3. **텍스트 대체**: 원본 URL을 단축된 URL로 교체
4. **결과 반환**: 수정된 텍스트 출력

#### 주요 함수

- `load_bitly_token()`: 환경 변수나 .env 파일에서 Bitly 토큰 로드
- `shorten_url(url, token)`: 단일 URL을 Bitly API로 단축
- `shorten_urls_in_text(text, token, verbose)`: 텍스트 내 모든 URL 처리

## Python 모듈로 사용

스크립트를 다른 Python 코드에서 모듈로 import하여 사용 가능:

```python
from scripts.shorten_urls import shorten_urls_in_text, load_bitly_token

# Bitly 토큰 로드
token = load_bitly_token()

# 텍스트의 URL 단축
modified_text, url_mapping = shorten_urls_in_text("Your text with URLs here", token)

print(modified_text)
print(url_mapping)  # 원본 URL -> 단축 URL 매핑 딕셔너리
```

## 트러블슈팅

### "BITLY_TOKEN not found"

**원인**: `BITLY_TOKEN` 환경 변수가 설정되지 않음

**해결 방법**:
1. 작업 디렉토리에 `.env` 파일 생성
2. `BITLY_TOKEN=your_token_here` 추가
3. `python-dotenv` 설치 확인: `pip install python-dotenv`

### "Invalid BITLY_TOKEN or insufficient permissions"

**원인**: 토큰이 유효하지 않거나 만료됨

**해결 방법**:
1. 토큰이 정확한지 확인 (공백이나 따옴표 없이)
2. https://bitly.com/a/settings/api 에서 새 토큰 생성
3. `.env` 파일에 새 토큰으로 업데이트

### "requests library not found"

**원인**: `requests` 패키지가 설치되지 않음

**해결 방법**:
```bash
pip install requests
```

### "Failed to shorten URL"

**원인**: 네트워크 문제 또는 Bitly API 오류

**해결 방법**:
1. 인터넷 연결 확인
2. URL이 유효하고 접근 가능한지 확인
3. 잠시 후 재시도 (rate limiting)
4. `--verbose` 플래그로 자세한 오류 메시지 확인

### "No URLs found"

URL이 발견되지 않으면 다음을 확인:
- URL이 `http://` 또는 `https://`로 시작하는지
- URL이 특수 문자로 감싸져 있지 않은지
- 텍스트에 유효한 URL 패턴이 포함되어 있는지

## 참고사항

- Bitly 계정과 API 토큰 필요 (무료 tier 사용 가능)
- 이미 단축된 URL도 bit.ly 링크로 재변환됨
- 생성된 단축 URL은 영구적이며 Bitly 대시보드에서 관리 가능
- Bitly 계정 tier에 따라 API rate limit 적용

## 라이선스

This skill is part of the personal skills collection.

## 기여

이슈나 개선 사항은 [GitHub Repository](https://github.com/elon-jang/skills)에 제보해주세요.
