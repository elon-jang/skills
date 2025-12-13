#!/usr/bin/env node
/**
 * Product Image Extractor Skill
 *
 * 이 스크립트는 상품 페이지 URL에서 실제 상품 이미지만 정확하게 추출합니다.
 * 배경 이미지, 배너, 로고 등은 자동으로 필터링됩니다.
 *
 * 사용법:
 *   node extract-images.js <product-url>
 *   PRODUCT_URL=<url> node extract-images.js
 *
 * 특징:
 *   - curl 기반으로 HTTP2 프로토콜 에러 회피
 *   - packshot, product 키워드 기반 필터링
 *   - 이미지 타입별 자동 분류 (premium, default, alternative)
 *   - 고해상도 이미지 자동 추천
 */

const { exec } = require('child_process');
const { promisify } = require('util');
const execAsync = promisify(exec);

// 환경 변수나 인자로 URL 받기 (직접 실행 시)
const productUrl = process.env.PRODUCT_URL || process.argv[2];

async function extractProductImages(url) {
  try {
    console.log('\n📦 상품 이미지 추출 시작\n');
    console.log(`🔗 URL: ${url}\n`);
    console.log('페이지 HTML 가져오는 중...');

    // curl로 HTML 가져오기 (maxBuffer 증가)
    const userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';
    const { stdout: html } = await execAsync(
      `curl -s -L -H "User-Agent: ${userAgent}" -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8" -H "Accept-Language: en-US,en;q=0.5" "${url}"`,
      { maxBuffer: 10 * 1024 * 1024 } // 10MB
    );

    console.log('HTML 파싱 중...');

    // HTML 엔티티 디코딩 (&amp; → &, &quot; → " 등)
    const decodedHtml = html
      .replace(/&amp;/g, '&')
      .replace(/&quot;/g, '"')
      .replace(/&apos;/g, "'")
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>');

    // 상품 이미지만 필터링하는 패턴
    const productKeywords = [
      'packshot',
      'product',
      'pdp',           // Product Detail Page
      'image',
      'media',
      'item',
      'goods',
      'catalog',
      'zoom',
      'large',
      'swatch'
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
      'instagram'
    ];

    // 모든 이미지 URL 추출 (쿼리 파라미터 포함)
    const imageUrlPattern = /(https:\/\/[^"'\s]+\.(jpg|jpeg|png|webp|avif)(\?[^"'\s]*)?)/gi;
    const allUrls = decodedHtml.match(imageUrlPattern) || [];

    // 중복 제거 및 필터링
    const imageUrls = new Set();
    const fallbackUrls = new Set(); // 폴백용 이미지 (큰 사이즈)

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

      // 키워드가 없지만 큰 이미지는 폴백으로 저장 (해상도 기준)
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

      // og:image, twitter:image, itemprop="image" 메타 태그 추출
      const metaImagePattern = /<meta[^>]*(?:property="og:image"|name="twitter:image"|itemprop="image")[^>]*content="([^"]+)"/gi;
      let match;
      const metaImages = new Set();

      while ((match = metaImagePattern.exec(decodedHtml)) !== null) {
        const imageUrl = match[1];
        if (imageUrl && imageUrl.startsWith('http')) {
          metaImages.add(imageUrl);
        }
      }

      if (metaImages.size > 0) {
        console.log(`✅ 메타 태그에서 ${metaImages.size}개의 이미지를 찾았습니다.\n`);
        metaImages.forEach(url => imageUrls.add(url));
      }
    }

    // Chanel 사이트 특화 이미지 필터링 및 우선순위
    const optimizeForChanel = (urls) => {
      const urlArray = Array.from(urls);

      // 제품 ID 패턴 추출 (예: -9543169179678)
      const productIdPattern = /-\d{13}\.jpg/;
      const styleIds = new Set();
      const groupedByStyle = new Map();

      urlArray.forEach(url => {
        const match = url.match(productIdPattern);
        if (match) {
          const idMatch = url.match(/-(\d{13})\.jpg/);
          if (idMatch) {
            const styleId = idMatch[1];
            styleIds.add(styleId);
            if (!groupedByStyle.has(styleId)) {
              groupedByStyle.set(styleId, []);
            }
            groupedByStyle.get(styleId).push(url);
          }
        }
      });

      // 각 스타일 ID별로 최적 해상도 선택 (1600px 우선, 없으면 3200px)
      const optimizedUrls = [];
      const seenStyles = new Set();

      // 스타일 ID를 배열로 변환하고 정렬
      // 954316... (제품 클로즈업) > 기타 ID (컬렉션/모델 착용)
      const sortedStyleIds = Array.from(groupedByStyle.keys()).sort((a, b) => {
        // 9543169로 시작하는 ID를 우선순위로 (제품 클로즈업 이미지)
        const aIsProduct = a.startsWith('9543169');
        const bIsProduct = b.startsWith('9543169');

        if (aIsProduct && !bIsProduct) return -1;
        if (!aIsProduct && bIsProduct) return 1;

        // 둘 다 제품 이미지이거나 둘 다 아닌 경우 ID 내림차순 (큰 번호가 더 중요)
        return b.localeCompare(a);
      });

      sortedStyleIds.forEach(styleId => {
        const urls = groupedByStyle.get(styleId);

        // w_1600 버전 찾기
        const w1600 = urls.find(u => u.includes('w_1600'));
        const w3200 = urls.find(u => u.includes('w_3200'));

        // 우선순위: w_1600 > w_3200 > 기타
        if (w1600) {
          optimizedUrls.push(w1600);
          seenStyles.add(styleId);
        } else if (w3200) {
          optimizedUrls.push(w3200);
          seenStyles.add(styleId);
        }
      });

      return optimizedUrls;
    };

    // Chanel 사이트 감지
    const isChanelSite = url.toLowerCase().includes('chanel.com');

    // URL을 배열로 변환하고 정렬
    let sortedUrls;

    if (isChanelSite) {
      // Chanel 사이트는 특화 로직 사용
      const optimized = optimizeForChanel(imageUrls);

      // 최적화된 결과가 있으면 사용, 없으면 원본 사용
      if (optimized.length > 0) {
        sortedUrls = optimized;
      } else {
        sortedUrls = Array.from(imageUrls).sort((a, b) => {
          // packshot-premium을 우선순위로
          if (a.includes('packshot-premium')) return -1;
          if (b.includes('packshot-premium')) return 1;

          // packshot-default를 다음 우선순위로
          if (a.includes('packshot-default')) return -1;
          if (b.includes('packshot-default')) return 1;

          // packshot-alternative를 다음 우선순위로
          if (a.includes('packshot-alternative')) return -1;
          if (b.includes('packshot-alternative')) return 1;

          return 0;
        });
      }
    } else {
      // 기타 사이트는 기존 로직 사용
      sortedUrls = Array.from(imageUrls).sort((a, b) => {
        // packshot-premium을 우선순위로
        if (a.includes('packshot-premium')) return -1;
        if (b.includes('packshot-premium')) return 1;

        // packshot-default를 다음 우선순위로
        if (a.includes('packshot-default')) return -1;
        if (b.includes('packshot-default')) return 1;

        // packshot-alternative를 다음 우선순위로
        if (a.includes('packshot-alternative')) return -1;
        if (b.includes('packshot-alternative')) return 1;

        return 0;
      });
    }

    // 결과 출력
    console.log('\n' + '='.repeat(80));
    console.log('📸 추출된 상품 이미지 URL');
    console.log('='.repeat(80) + '\n');

    if (sortedUrls.length === 0) {
      console.log('❌ 상품 이미지를 찾을 수 없습니다.');
      return;
    }

    // 이미지 타입별로 그룹화
    const grouped = {
      premium: [],
      default: [],
      alternative: [],
      other: []
    };

    sortedUrls.forEach(url => {
      if (url.includes('packshot-premium')) {
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

    // 메인 제품 이미지 자동 선정
    const selectMainImage = (urls, grouped) => {
      // 우선순위: premium > default > alternative > other 첫 번째
      if (grouped.premium.length > 0) return grouped.premium[0];
      if (grouped.default.length > 0) return grouped.default[0];
      if (grouped.alternative.length > 0) return grouped.alternative[0];
      if (grouped.other.length > 0) return grouped.other[0];
      return urls[0] || null;
    };

    const mainProductImage = selectMainImage(sortedUrls, grouped);

    if (mainProductImage) {
      console.log('⭐ 메인 제품 이미지:');
      console.log(`${mainProductImage}\n`);
    }

    // 최고 해상도 이미지 추천
    const highestResUrls = sortedUrls.filter(url =>
      url.includes('w_1920') || url.includes('w_1240') || !url.match(/w_\d+/)
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
      main_product_image: mainProductImage,
      total_images_count: sortedUrls.length,
      grouped: {
        premium: grouped.premium,
        default: grouped.default,
        alternative: grouped.alternative,
        other: grouped.other
      },
      high_resolution_recommended: highestResUrls.slice(0, 3),
      all_images: sortedUrls
    };

    // JSON 결과 출력 (Claude가 파싱 가능)
    console.log('\n--- RESULT START ---');
    console.log(JSON.stringify(result, null, 2));
    console.log('--- RESULT END ---\n');

    console.log('✅ 추출 완료!\n');

    return result;

  } catch (error) {
    console.error('\n❌ 오류 발생:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

// 모듈로 사용 시 함수 export
module.exports = { extractProductImages };

// 직접 실행 시에만 실행
if (require.main === module) {
  if (!productUrl) {
    console.error('Error: 상품 URL이 필요합니다.');
    console.error('Usage: PRODUCT_URL=<url> node extract-images.js');
    console.error('   or: node extract-images.js <url>');
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
