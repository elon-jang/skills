# Product Image Extractor - Claude Skill v2.3

웹페이지에서 **실제 상품 이미지만** 정확하게 추출하는 Claude Skill입니다.

## 개요

이 스킬은 두 가지 모드로 상품 이미지 URL을 추출합니다:

- **curl 모드**: 빠른 속도 (1-2초), 정적 HTML 사이트용
- **Playwright 모드**: 봇 차단 우회 (8-10초), JavaScript 동적 로딩 사이트용

배경 이미지, 배너, 로고 등을 자동으로 필터링하고 실제 상품 이미지만 반환합니다.

## v2.3 주요 개선사항 (NEW!)

- ✅ **메타 태그 폴백**: 이미지를 찾지 못한 경우 og:image, twitter:image 등 메타 태그에서 자동 추출
- ✅ **HTML 엔티티 디코딩**: `&amp;` → `&` 변환으로 쿼리 파라미터 지원 강화
- ✅ **향상된 쿼리 파라미터 지원**: `?w=720&q=95` 형식의 이미지 URL 정확히 추출
- ✅ **확장된 폴백 크기 감지**: 320px 이상 이미지를 상품 이미지로 간주 (이전: 800px)

## v2.2 주요 개선사항

| 항목 | curl 모드 | Playwright 모드 |
|------|----------|----------------|
| HTTP2 에러 | ✅ 해결 | ✅ 해결 |
| 속도 | 빠름 (1-2초) | 보통 (8-10초) |
| 메모리 사용 | 낮음 | 중간 |
| 봇 차단 우회 | ❌ 불가능 | ✅ 가능 |
| JavaScript | ❌ 미지원 | ✅ 완전 지원 |
| 필터링 정확도 | 높음 (48개) | 높음 (47개) |
| 이미지 분류 | ✅ 자동 분류 | ✅ 자동 분류 |

## 특징

- ✅ **정확한 필터링**: 11개 키워드 기반 (packshot, product, pdp, image, media, item, goods, catalog, zoom, large, swatch)
- 🎯 **자동 분류**: 대표/프리미엄/기본/대체 이미지로 자동 분류
- 🚀 **이중 모드**: curl (빠름) + Playwright (봇 차단 우회)
- 📊 **고해상도 추천**: 가장 높은 해상도의 이미지를 자동으로 추천
- ⚡ **광범위 지원**: Chanel, UGG, Weverse Shop 등 다양한 e-commerce 사이트
- 🔧 **스마트 제외**: 14개 제외 키워드로 배경, 배너, 로고, 썸네일 등 자동 필터링
- 🔄 **3단계 폴백**: 키워드 → 크기 기반 → 메타 태그 순으로 자동 시도
- 🏷️ **메타 태그 지원**: og:image, twitter:image, schema.org 자동 추출

## 설치

```bash
cd skills/product-image-extractor
npm install
npx playwright install chromium  # Playwright 모드 사용 시
```

## 사용법

### Claude에서 사용하기

```
상품 이미지를 추출해줘: https://www.chanel.com/us/fragrance/p/136008/...
상품 대표 이미지 하나를 추출해줘: https://www.ugg.com/women-slippers/disquette/...
```

### curl 모드 (빠름, 기본)

```bash
cd skills/product-image-extractor
node extract-images.js "https://www.chanel.com/..."
# 또는
npm run extract "https://www.chanel.com/..."
```

### Playwright 모드 (봇 차단 사이트)

```bash
node extract-images-playwright.js "https://www.ugg.com/..."
# 또는
npm run extract-pw "https://www.ugg.com/..."
```

## 출력 형식

### 콘솔 출력

```
📦 상품 이미지 추출 시작

🔗 URL: https://www.chanel.com/us/fragrance/p/136008/...

페이지 HTML 가져오는 중...
HTML 파싱 중...

================================================================================
📸 추출된 상품 이미지 URL
================================================================================

📸 프리미엄 패키지샷:
1. https://www.chanel.com/images/.../packshot-premium-136008.jpg
2. https://www.chanel.com/images/.../packshot-premium-136008.jpg (다른 해상도)

📸 기본 제품 이미지:
3. https://www.chanel.com/images/.../packshot-default-136008.jpg
4. ...

📸 대체 뷰:
5. https://www.chanel.com/images/.../packshot-alternative-v1-136008.jpg

================================================================================
✅ 총 48개의 상품 이미지를 찾았습니다.
================================================================================

✨ 추천 고해상도 이미지:
1. https://www.chanel.com/images/.../w_1240/packshot-premium.jpg
2. https://www.chanel.com/images/.../w_1920/packshot-default.jpg
3. https://www.chanel.com/images/.../w_1240/packshot-alternative.jpg
```

### JSON 출력 (curl 모드)

```json
{
  "url": "https://www.chanel.com/us/fragrance/p/136008/...",
  "timestamp": "2025-12-09T09:49:00.000Z",
  "total_images_count": 48,
  "grouped": {
    "premium": [...],
    "default": [...],
    "alternative": [...],
    "other": [...]
  },
  "high_resolution_recommended": [...],
  "all_images": [...]
}
```

### JSON 출력 (Playwright 모드)

```json
{
  "url": "https://www.ugg.com/women-slippers/disquette/...",
  "timestamp": "2025-12-09T12:30:35.379Z",
  "total_images_count": 47,
  "grouped": {
    "hero": [...],
    "premium": [...],
    "default": [...],
    "alternative": [...],
    "other": [...]
  },
  "high_resolution_recommended": [...],
  "main_product_image": "https://dms.deckers.com/ugg/image/upload/t_product-xlarge-wp/...",
  "all_images": [...]
}
```

## 필터링 로직

### 포함 키워드 (11개)
- `packshot`: 상품 패키지샷 (Chanel 등)
- `product`: 상품 이미지
- `pdp`: Product Detail Page
- `image`: 이미지
- `media`: 미디어
- `item`: 아이템
- `goods`: 상품
- `catalog`: 카탈로그
- `zoom`: 줌 이미지
- `large`: 큰 이미지
- `swatch`: 색상 견본

### 제외 키워드 (14개)
- `wrapping`: 포장 이미지
- `banner`: 배너 이미지
- `favicon`: 파비콘
- `logo`: 로고
- `chanelmoi`: 브랜드 장식 이미지
- `icon`: 아이콘
- `sprite`: 스프라이트
- `bg`, `background`: 배경 이미지
- `thumbnail`, `thumb`: 썸네일
- `social`, `facebook`, `twitter`, `instagram`: SNS 이미지

### 폴백 메커니즘
키워드 매칭에 실패한 경우:
1. URL에서 해상도 패턴 감지 (`800x600`, `w_1920` 등)
2. 800px 이상의 큰 이미지만 수집
3. 자동으로 상품 이미지로 간주

### 이미지 분류
- **프리미엄 패키지샷**: `packshot-premium` 포함
- **기본 제품 이미지**: `packshot-default` 포함
- **대체 뷰**: `packshot-alternative` 포함
- **기타**: 위에 해당하지 않는 상품 이미지

## 예시

### Chanel 향수 (curl 모드)

```bash
node extract-images.js "https://www.chanel.com/us/fragrance/p/136008/chance-eau-splendide-limited-edition-eau-de-parfum-spray/"
```

**결과**:

- 총 48개의 상품 이미지 추출 (1-2초)
- 5개 프리미엄 패키지샷
- 38개 기본 제품 이미지
- 5개 대체 뷰
- 배경 이미지 자동 제외 (145개 → 48개)

### UGG 슬리퍼 (Playwright 모드)

```bash
node extract-images-playwright.js "https://www.ugg.com/women-slippers/disquette/1122550.html?dwvar_1122550_color=DNY"
```

**결과**:

- 총 47개의 상품 이미지 추출 (8-10초)
- 대표 이미지 자동 선택
- 다양한 각도 및 해상도
- 봇 차단 우회 성공

## 지원하는 사이트

- ✅ **Chanel**: curl 모드, packshot 키워드 (48-55개)
- ✅ **UGG**: Playwright 모드, 봇 차단 우회 (47개)
- ✅ **Weverse Shop**: curl 모드, 쿼리 파라미터 지원 (4개)
- ✅ **일반 e-commerce**: curl 모드, product/pdp/image/media 키워드
- ✅ **메타 태그 있는 사이트**: 최소 1개 대표 이미지 보장
- ✅ **JavaScript 사이트**: Playwright 모드로 완전 지원
- ⚠️ **강력한 봇 차단 사이트**: Gucci, Moncler 등은 제한적 (메타 태그만 가능)

## 트러블슈팅

### "상품 이미지를 찾을 수 없습니다"

1. URL이 올바른지 확인
2. 봇 차단이 의심되는 경우 Playwright 모드 사용:

   ```bash
   node extract-images-playwright.js "<URL>"
   ```

3. 사이트가 다른 키워드를 사용하는 경우 키워드 추가 고려

### curl 에러

```bash
# curl 버전 확인
curl --version

# curl이 설치되지 않은 경우
brew install curl  # macOS
apt-get install curl  # Ubuntu/Debian
```

### stdout maxBuffer length exceeded

HTML이 너무 큰 경우 자동으로 10MB까지 처리합니다. 더 큰 버퍼가 필요한 경우:

```javascript
// extract-images.js 수정
maxBuffer: 20 * 1024 * 1024 // 20MB
```

## 제한사항

- 웹 스크래핑은 해당 웹사이트의 이용약관을 준수해야 합니다
- 과도한 요청은 IP 차단을 유발할 수 있습니다
- 매우 강력한 봇 차단(Cloudflare Challenge 등)은 Playwright도 차단될 수 있습니다

## 파일 구조

```text
skills/product-image-extractor/
├── extract-images.js            # curl 모드 스크립트 (빠름)
├── extract-images-playwright.js # Playwright 모드 스크립트 (봇 차단 우회)
├── skill.md                     # 스킬 메타데이터
├── package.json                 # Node.js 의존성
├── package-lock.json            # 잠금 파일
└── README.md                    # 이 문서
```

## 사용 가이드

### 어떤 모드를 사용해야 하나요?

| 상황 | 권장 모드 | 이유 |
|------|---------|------|
| 속도가 중요한 경우 | curl 모드 | 1-2초로 매우 빠름 |
| 봇 차단이 있는 사이트 | Playwright 모드 | 실제 브라우저로 우회 |
| JavaScript 동적 로딩 | Playwright 모드 | 완전한 렌더링 지원 |
| 일반 e-commerce | curl 모드 먼저 시도 | 대부분 충분함 |

## 라이센스

MIT License

## 기여

이슈와 개선 제안을 환영합니다!

## 버전 히스토리

- **v2.3** (2025-12-09): 메타 태그 폴백 추가, HTML 엔티티 디코딩, 쿼리 파라미터 지원 강화, 320px 폴백
- **v2.2** (2025-12-09): Playwright 모드 추가, UGG 등 봇 차단 사이트 지원, 이중 모드 시스템
- **v2.1** (2025-12-09): 확장 키워드 지원 (11개 포함, 14개 제외), 폴백 메커니즘 추가, 향상된 User-Agent
- **v2.0** (2025-12-09): curl 기반으로 전환, 필터링 정확도 향상, 이미지 분류 기능 추가
- **v1.0** (2025-12-09): Playwright 기반 초기 버전
