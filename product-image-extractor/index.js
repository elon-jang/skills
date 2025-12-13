#!/usr/bin/env node
/**
 * Product Image Extractor - Unified Entry Point
 *
 * URL 도메인을 자동 감지하여 최적의 추출 방식을 선택합니다.
 * - UGG: Playwright (봇 차단 우회)
 * - Chanel: curl (빠름)
 * - Weverse: curl (빠름)
 * - 기타: curl 먼저 시도, 실패 시 Playwright 폴백
 *
 * 사용법:
 *   node index.js <product-url>
 *   npm run extract "<product-url>"
 */

const { extractProductImages: extractWithCurl } = require('./extract-images.js');
const { extractProductImages: extractWithPlaywright } = require('./extract-images-playwright.js');

// 사이트별 전략 매핑
const SITE_STRATEGIES = {
  'ugg.com': { mode: 'playwright', name: 'UGG' },
  'chanel.com': { mode: 'curl', name: 'Chanel' },
  'weverse.io': { mode: 'curl', name: 'Weverse Shop' },
  'shop.weverse.com': { mode: 'curl', name: 'Weverse Shop' }
};

/**
 * URL에서 도메인 추출
 */
function extractDomain(url) {
  try {
    const urlObj = new URL(url);
    return urlObj.hostname.replace(/^www\./, '');
  } catch {
    return null;
  }
}

/**
 * 도메인에 맞는 전략 찾기
 */
function getStrategy(url) {
  const domain = extractDomain(url);
  if (!domain) return null;

  // 정확한 도메인 매칭
  for (const [siteDomain, strategy] of Object.entries(SITE_STRATEGIES)) {
    if (domain === siteDomain || domain.endsWith('.' + siteDomain)) {
      return strategy;
    }
  }

  return null; // 알 수 없는 사이트
}

/**
 * 통합 추출 함수
 */
async function extract(url) {
  const strategy = getStrategy(url);

  if (strategy) {
    console.log(`\n🎯 사이트 감지: ${strategy.name}`);
    console.log(`📋 전략: ${strategy.mode === 'playwright' ? 'Playwright (봇 차단 우회)' : 'curl (빠름)'}\n`);

    if (strategy.mode === 'playwright') {
      return await extractWithPlaywright(url);
    } else {
      return await extractWithCurl(url);
    }
  }

  // 알 수 없는 사이트: curl 먼저 시도, 실패 시 Playwright
  console.log('\n🔍 알 수 없는 사이트 - curl 먼저 시도\n');

  try {
    const result = await extractWithCurl(url);
    if (result && result.total_images_count > 0) {
      return result;
    }
    throw new Error('이미지를 찾지 못함');
  } catch (error) {
    console.log('\n⚠️  curl 실패, Playwright로 재시도...\n');
    return await extractWithPlaywright(url);
  }
}

// 환경 변수나 인자로 URL 받기
const productUrl = process.env.PRODUCT_URL || process.argv[2];

if (!productUrl) {
  console.error('Error: 상품 URL이 필요합니다.');
  console.error('Usage: node index.js <url>');
  console.error('   or: npm run extract "<url>"');
  console.error('\n지원 사이트:');
  for (const [domain, strategy] of Object.entries(SITE_STRATEGIES)) {
    console.error(`  - ${strategy.name} (${domain}) → ${strategy.mode}`);
  }
  console.error('  - 기타 → curl 먼저 시도, 실패 시 Playwright');
  process.exit(1);
}

// 실행
extract(productUrl)
  .then(() => {
    process.exit(0);
  })
  .catch(err => {
    console.error('\n❌ 추출 실패:', err.message);
    process.exit(1);
  });
