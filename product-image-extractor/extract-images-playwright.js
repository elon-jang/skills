#!/usr/bin/env node
/**
 * Product Image Extractor Skill - Playwright Version
 *
 * Playwright를 사용하여 JavaScript 렌더링이 필요하거나 봇 차단이 있는 사이트를 지원합니다.
 * UGG, Nike 등 고급 보안이 적용된 e-commerce 사이트에서 사용합니다.
 *
 * 사용법:
 *   node extract-images-playwright.js <product-url>
 *   PRODUCT_URL=<url> node extract-images-playwright.js
 *
 * 특징:
 *   - 실제 브라우저로 JavaScript 렌더링
 *   - 봇 차단 우회 (User-Agent, 화면 크기 등)
 *   - 이미지 타입별 자동 분류
 *   - 고해상도 이미지 자동 추천
 */

const { chromium } = require('playwright');

// 환경 변수나 인자로 URL 받기 (직접 실행 시)
const productUrl = process.env.PRODUCT_URL || process.argv[2];

async function extractProductImages(url) {
  let browser;
  try {
    console.log('\n📦 상품 이미지 추출 시작 (Playwright)\n');
    console.log(`🔗 URL: ${url}\n`);
    console.log('브라우저 시작 중...');

    // 브라우저 시작
    browser = await chromium.launch({
      headless: true,
      args: [
        '--disable-blink-features=AutomationControlled',
        '--disable-dev-shm-usage',
        '--no-sandbox'
      ]
    });

    const context = await browser.newContext({
      userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      viewport: { width: 1920, height: 1080 },
      locale: 'en-US'
    });

    const page = await context.newPage();

    // 페이지 로드
    console.log('페이지 로딩 중...');
    try {
      await page.goto(url, {
        waitUntil: 'domcontentloaded',
        timeout: 30000
      });
    } catch (error) {
      console.log('⚠️  페이지 로드 중 타임아웃, 계속 진행...');
    }

    // JavaScript 실행 대기
    await page.waitForTimeout(5000);

    console.log('HTML 파싱 중...');

    // HTML 가져오기 및 엔티티 디코딩
    const rawHtml = await page.content();
    const html = rawHtml
      .replace(/&amp;/g, '&')
      .replace(/&quot;/g, '"')
      .replace(/&apos;/g, "'")
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>');

    // 상품 이미지만 필터링하는 패턴
    const productKeywords = [
      'packshot',
      'product',
      'pdp',
      'image',
      'media',
      'item',
      'goods',
      'catalog',
      'zoom',
      'large',
      'swatch',
      'hero',
      'main',
      'primary'
    ];
    const excludeKeywords = [
      'wrapping',
      'banner',
      'favicon',
      'logo',
      'chanelmoi',
      'icon',
      'sprite',
      'bg',
      'background',
      'thumbnail',
      'thumb',
      'social',
      'facebook',
      'twitter',
      'instagram',
      'avatar',
      'badge'
    ];

    // 모든 이미지 URL 추출 (쿼리 파라미터 포함)
    const imageUrlPattern = /(https:\/\/[^"'\s]+\.(jpg|jpeg|png|webp|avif)(\?[^"'\s]*)?)/gi;
    const allUrls = html.match(imageUrlPattern) || [];

    // 중복 제거 및 필터링
    const imageUrls = new Set();
    const fallbackUrls = new Set();

    allUrls.forEach(url => {
      const urlLower = url.toLowerCase();

      // 제외 키워드가 포함된 이미지는 건너뛰기
      if (excludeKeywords.some(keyword => urlLower.includes(keyword))) {
        return;
      }

      // 상품 이미지 키워드가 포함된 경우 추가
      if (productKeywords.some(keyword => urlLower.includes(keyword))) {
        imageUrls.add(url);
        return;
      }

      // 키워드가 없지만 큰 이미지는 폴백으로 저장
      // 패턴: 1920x1080, w_1920, w=720, width=1024 등
      const sizeMatch = url.match(/(\d{3,4})[x_](\d{3,4})/i) ||
                       url.match(/[w|h]_?(\d{3,4})/i) ||
                       url.match(/[?&]w=(\d{3,4})/i) ||
                       url.match(/[?&]width=(\d{3,4})/i);
      if (sizeMatch) {
        const size = parseInt(sizeMatch[1]);
        if (size >= 320) { // 320px 이상이면 상품 이미지로 간주
          fallbackUrls.add(url);
        }
      }
    });

    // 상품 이미지를 찾지 못한 경우 폴백 사용
    if (imageUrls.size === 0 && fallbackUrls.size > 0) {
      console.log(`\n⚠️  상품 키워드를 찾지 못했습니다. 큰 이미지를 대신 사용합니다. (${fallbackUrls.size}개)\n`);
      fallbackUrls.forEach(url => imageUrls.add(url));
    }

    // 여전히 이미지를 찾지 못한 경우, 메타 태그에서 추출 시도
    if (imageUrls.size === 0) {
      console.log('\n⚠️  이미지를 찾지 못했습니다. 메타 태그에서 추출을 시도합니다...\n');

      const metaImages = await page.evaluate(() => {
        const ogImage = document.querySelector('meta[property="og:image"]');
        const twitterImage = document.querySelector('meta[name="twitter:image"]');
        const schemaImage = document.querySelector('meta[itemprop="image"]');

        const images = [];
        if (ogImage && ogImage.content) images.push(ogImage.content);
        if (twitterImage && twitterImage.content) images.push(twitterImage.content);
        if (schemaImage && schemaImage.content) images.push(schemaImage.content);

        return [...new Set(images)]; // 중복 제거
      });

      if (metaImages.length > 0) {
        console.log(`✅ 메타 태그에서 ${metaImages.length}개의 이미지를 찾았습니다.\n`);
        metaImages.forEach(url => imageUrls.add(url));
      }
    }

    // URL을 배열로 변환하고 정렬
    const sortedUrls = Array.from(imageUrls).sort((a, b) => {
      // hero, main, primary를 우선순위로
      if (a.includes('hero') || a.includes('main') || a.includes('primary')) return -1;
      if (b.includes('hero') || b.includes('main') || b.includes('primary')) return 1;

      // packshot-premium을 우선순위로
      if (a.includes('packshot-premium')) return -1;
      if (b.includes('packshot-premium')) return 1;

      // packshot-default를 다음 우선순위로
      if (a.includes('packshot-default')) return -1;
      if (b.includes('packshot-default')) return 1;

      return 0;
    });

    // 결과 출력
    console.log('\n' + '='.repeat(80));
    console.log('📸 추출된 상품 이미지 URL');
    console.log('='.repeat(80) + '\n');

    if (sortedUrls.length === 0) {
      console.log('❌ 상품 이미지를 찾을 수 없습니다.');
      await browser.close();
      return;
    }

    // 이미지 타입별로 그룹화
    const grouped = {
      hero: [],
      premium: [],
      default: [],
      alternative: [],
      other: []
    };

    sortedUrls.forEach(url => {
      if (url.includes('hero') || url.includes('main') || url.includes('primary')) {
        grouped.hero.push(url);
      } else if (url.includes('packshot-premium')) {
        grouped.premium.push(url);
      } else if (url.includes('packshot-default')) {
        grouped.default.push(url);
      } else if (url.includes('packshot-alternative')) {
        grouped.alternative.push(url);
      } else {
        grouped.other.push(url);
      }
    });

    let index = 1;

    if (grouped.hero.length > 0) {
      console.log('📸 대표 이미지:');
      grouped.hero.forEach(url => {
        console.log(`${index++}. ${url}`);
      });
      console.log('');
    }

    if (grouped.premium.length > 0) {
      console.log('📸 프리미엄 패키지샷:');
      grouped.premium.forEach(url => {
        console.log(`${index++}. ${url}`);
      });
      console.log('');
    }

    if (grouped.default.length > 0) {
      console.log('📸 기본 제품 이미지:');
      grouped.default.forEach(url => {
        console.log(`${index++}. ${url}`);
      });
      console.log('');
    }

    if (grouped.alternative.length > 0) {
      console.log('📸 대체 뷰:');
      grouped.alternative.forEach(url => {
        console.log(`${index++}. ${url}`);
      });
      console.log('');
    }

    if (grouped.other.length > 0) {
      console.log('📸 기타 제품 이미지:');
      grouped.other.forEach(url => {
        console.log(`${index++}. ${url}`);
      });
      console.log('');
    }

    console.log('='.repeat(80));
    console.log(`✅ 총 ${sortedUrls.length}개의 상품 이미지를 찾았습니다.`);
    console.log('='.repeat(80) + '\n');

    // 최고 해상도 이미지 추천
    const highestResUrls = sortedUrls.filter(url =>
      url.includes('w_1920') || url.includes('w_1240') ||
      url.match(/(\d{4})[x_](\d{4})/) || !url.match(/w_\d+/)
    );

    if (highestResUrls.length > 0) {
      console.log('✨ 추천 고해상도 이미지:');
      highestResUrls.slice(0, 3).forEach((url, i) => {
        console.log(`${i + 1}. ${url}`);
      });
      console.log('');
    }

    // 결과 객체 생성
    const result = {
      url: url,
      timestamp: new Date().toISOString(),
      total_images_count: sortedUrls.length,
      grouped: {
        hero: grouped.hero,
        premium: grouped.premium,
        default: grouped.default,
        alternative: grouped.alternative,
        other: grouped.other
      },
      high_resolution_recommended: highestResUrls.slice(0, 3),
      main_product_image: sortedUrls[0] || null,
      all_images: sortedUrls
    };

    // JSON 결과 출력
    console.log('\n--- RESULT START ---');
    console.log(JSON.stringify(result, null, 2));
    console.log('--- RESULT END ---\n');

    console.log('✅ 추출 완료!\n');

    if (sortedUrls.length > 0) {
      console.log(`🎯 대표 상품 이미지: ${sortedUrls[0]}\n`);
    }

    await browser.close();
    return result;

  } catch (error) {
    console.error('\n❌ 오류 발생:', error.message);
    console.error(error.stack);
    if (browser) {
      await browser.close();
    }
    process.exit(1);
  }
}

// 모듈로 사용 시 함수 export
module.exports = { extractProductImages };

// 직접 실행 시에만 실행
if (require.main === module) {
  if (!productUrl) {
    console.error('Error: 상품 URL이 필요합니다.');
    console.error('Usage: PRODUCT_URL=<url> node extract-images-playwright.js');
    console.error('   or: node extract-images-playwright.js <url>');
    process.exit(1);
  }

  extractProductImages(productUrl)
    .then(() => {
      process.exit(0);
    })
    .catch(err => {
      console.error('\n❌ 프로세스 실패:', err);
      process.exit(1);
    });
}
