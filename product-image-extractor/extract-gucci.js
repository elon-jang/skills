const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({
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
    locale: 'ko-KR'
  });

  const page = await context.newPage();

  console.log('페이지 로딩 중...');

  try {
    await page.goto('https://www.gucci.com/kr/ko/pr/women/shoes-for-women/pumps-for-women/mid-heels-for-women/womens-pump-with-horsebit-p-853460KY9809744', {
      waitUntil: 'domcontentloaded',
      timeout: 45000
    });
  } catch (error) {
    console.log('타임아웃 발생, 계속 진행...');
  }

  // 추가 대기
  console.log('JavaScript 실행 대기 중 (15초)...');
  await page.waitForTimeout(15000);

  // 메타 태그 확인
  const ogImage = await page.evaluate(() => {
    const meta = document.querySelector('meta[property="og:image"]');
    return meta ? meta.getAttribute('content') : null;
  });

  console.log('\nog:image:', ogImage);

  // 모든 img 태그 확인
  const images = await page.evaluate(() => {
    const imgs = Array.from(document.querySelectorAll('img'));
    return imgs.map(img => ({
      src: img.src,
      alt: img.alt,
      width: img.width,
      height: img.height
    })).filter(img => img.src && img.src.startsWith('http'));
  });

  console.log('\n이미지 태그 발견:', images.length, '개');

  // 상품 이미지로 보이는 것들만 필터링
  const productImages = images.filter(img =>
    (img.width > 300 || img.height > 300) &&
    !img.src.includes('logo') &&
    !img.src.includes('icon')
  );

  console.log('상품 이미지 후보:', productImages.length, '개\n');

  productImages.slice(0, 10).forEach((img, idx) => {
    console.log(`${idx + 1}. ${img.src}`);
    console.log(`   크기: ${img.width}x${img.height}, alt: ${img.alt}\n`);
  });

  await browser.close();
})();
