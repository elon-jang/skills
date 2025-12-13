# Product Image Extractor Skill v3.1

상품 페이지에서 **실제 상품 이미지만** 정확하게 추출하는 Claude Skill입니다.

## Description

Use this skill when the user asks to extract product images, get image URLs from a product page, or scrape product photos from e-commerce websites. This skill automatically detects the website and selects the optimal extraction method (curl for speed or Playwright for bot-resistant sites). Returns main_product_image field for easy integration. (user)

## 주요 기능

- 🎯 **정확한 필터링**: 11개 키워드 기반으로 상품 이미지만 추출
- 📊 **자동 분류**: 대표/프리미엄/기본/대체 이미지로 자동 분류
- ⚡ **이중 모드**: curl (빠름, 1-2초) + Playwright (봇 차단 우회, 10초)
- 🚀 **광범위 지원**: Chanel, UGG, Weverse Shop 등 다양한 e-commerce 사이트
- 📸 **고해상도 추천**: 가장 높은 해상도 이미지 자동 추천
- 🔧 **스마트 제외**: 14개 키워드로 배경/배너/로고/썸네일 자동 필터링
- 🔄 **3단계 폴백**: 키워드 → 크기 → 메타 태그 순으로 자동 시도
- 🏷️ **메타 태그 지원**: og:image, twitter:image 등에서 최소 1개 이미지 보장

## v3.1 주요 개선사항 (NEW!)

- ✅ **메인 이미지 자동 선정**: `main_product_image` 필드로 최적 대표 이미지 자동 선택
- ✅ **Chanel 최적화**: 제품 클로즈업 이미지 우선순위 (9543169 ID 기반)
- ✅ **스마트 정렬**: 제품 이미지 > 컬렉션/모델 이미지 자동 분류

## v3.0 주요 개선사항

- ✅ **자동 사이트 감지**: URL 도메인 분석으로 최적 추출 방식 자동 선택
- ✅ **통합 엔트리포인트**: `node index.js <URL>` 하나로 모든 사이트 지원
- ✅ **스마트 폴백**: 알 수 없는 사이트는 curl 먼저 시도, 실패 시 Playwright 자동 전환
- ✅ **사이트별 전략 매핑**: UGG→Playwright, Chanel/Weverse→curl

## 사이트별 전략

| 사이트 | 도메인 | 모드 | 이유 |
|--------|--------|------|------|
| UGG | `ugg.com` | Playwright | 봇 차단 우회 |
| Chanel | `chanel.com` | curl | 빠르고 안정적 |
| Weverse Shop | `weverse.io`, `shop.weverse.com` | curl | 빠르고 안정적 |
| 기타 | * | curl → Playwright | curl 먼저 시도, 실패 시 Playwright |

## v2.3 주요 개선사항

- ✅ **메타 태그 폴백**: 이미지 추출 실패 시 og:image, twitter:image 자동 추출
- ✅ **쿼리 파라미터 지원**: `?w=720&q=95` 형식 URL 정확히 추출
- ✅ **HTML 엔티티 디코딩**: `&amp;` → `&` 자동 변환
- ✅ **320px 폴백**: 더 낮은 해상도부터 상품 이미지로 인식

## v2.2 주요 개선사항

| 항목 | curl 모드 | Playwright 모드 |
|------|----------|----------------|
| 속도 | 빠름 (1-2초) | 보통 (8-10초) |
| 봇 차단 | ❌ 차단됨 | ✅ 우회 가능 |
| JavaScript | ❌ 미지원 | ✅ 완전 지원 |
| 지원 사이트 | Chanel 등 | UGG, Nike 등 |
| HTTP2 에러 | ✅ 해결 | ✅ 해결 |

## 사용 시나리오

다음과 같은 경우에 이 스킬을 자동으로 사용합니다:

- "이 상품 페이지에서 이미지 URL을 추출해줘"
- "상품 이미지 URL을 가져와줘: [URL]"
- "이 링크의 상품 사진들을 모두 추출해줘"
- "제품 이미지 URL 목록을 만들어줘"
- "상품 이미지를 추출해줘: [URL]"

## 작동 방식

### curl 모드 (기본, 빠름)

1. curl로 HTML을 가져옵니다 (HTTP2 에러 회피)
2. 정규식으로 모든 이미지 URL 추출
3. 11개 포함 키워드 + 14개 제외 키워드로 필터링
4. 폴백: 키워드 실패 시 800px+ 큰 이미지 자동 선택
5. 이미지 타입별 자동 분류 및 JSON 반환

### Playwright 모드 (봇 차단 사이트용)

1. Chromium 브라우저로 JavaScript 렌더링
2. 봇 감지 우회 (User-Agent, viewport 설정)
3. 동적 로드 대기 (5초)
4. 동일한 필터링 + 분류 로직 적용
5. 대표 이미지 자동 선택

## 요구사항

- Node.js 14.0 이상
- curl (시스템 기본 설치)
- Playwright (선택, 봇 차단 사이트 지원용)

## 출력 형식

```json
{
  "url": "https://example.com/product",
  "timestamp": "2025-12-13T11:37:00.000Z",
  "main_product_image": "https://example.com/images/main-product.jpg",
  "total_images_count": 9,
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

**주요 필드:**

- `main_product_image`: 자동 선정된 최적 대표 이미지 (NEW in v3.1)
- `total_images_count`: 추출된 총 이미지 개수
- `all_images`: 모든 이미지 URL 배열 (우선순위 정렬됨)

## 실행 명령어

### 자동 모드 (권장)

```bash
cd skills/product-image-extractor
node index.js "<URL>"
# 또는
npm run extract "<URL>"
```

사이트를 자동 감지하여 최적 방식을 선택합니다:
- UGG → Playwright (봇 차단 우회)
- Chanel → curl (빠름)
- Weverse → curl (빠름)
- 기타 → curl 먼저 시도, 실패 시 Playwright

### 수동 모드 (특정 방식 강제)

```bash
# curl 모드 강제
node extract-images.js "<URL>"
npm run extract-curl "<URL>"

# Playwright 모드 강제
node extract-images-playwright.js "<URL>"
npm run extract-pw "<URL>"
```

## 예시 결과

### Chanel 향수 (curl 모드)

- **입력**: `https://www.chanel.com/us/fragrance/p/136008/...`
- **결과**: 48개의 상품 이미지 (1-2초)
  - 5개 프리미엄 패키지샷
  - 38개 기본 제품 이미지
  - 5개 대체 뷰

### UGG 슬리퍼 (Playwright 모드)

- **입력**: `https://www.ugg.com/women-slippers/disquette/1122550.html`
- **결과**: 47개의 상품 이미지 (8-10초)
  - 대표 이미지 자동 선택
  - 다양한 각도 및 해상도

## 지원 사이트

- ✅ **Chanel**: curl 모드, packshot 키워드 (48-55개)
- ✅ **UGG**: Playwright 모드, 봇 차단 우회 (47개)
- ✅ **Weverse Shop**: curl 모드, 쿼리 파라미터 (4개)
- ✅ **일반 e-commerce**: curl 모드, product/pdp/image 키워드
- ✅ **메타 태그 사이트**: 최소 1개 대표 이미지 보장

## 주의사항

- 웹 스크래핑은 해당 웹사이트의 이용약관을 준수해야 합니다
- 과도한 요청은 IP 차단을 유발할 수 있습니다
- 봇 차단이 강한 사이트는 Playwright 모드를 사용하세요

## 버전 정보

- **현재 버전**: v3.1
- **릴리스**: 2025-12-13
- **변경사항**: 메인 이미지 자동 선정 (`main_product_image`), Chanel 제품 클로즈업 우선순위, 브랜드 무관 최적 이미지 선택
