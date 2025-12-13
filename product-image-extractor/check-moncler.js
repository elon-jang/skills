const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  // 네트워크 요청 모니터링
  const imageUrls = [];
  page.on('response', async (response) => {
    const url = response.url();
    if (url.match(/\.(jpg|jpeg|png|webp|avif)/i)) {
      imageUrls.push(url);
    }
  });

  await page.goto('https://www.moncler.com/ko-kr/women/outerwear/short-down-jackets/virieu-boucle-hooded-short-down-jacket-white-K20931A0021389B6S21I.html', {
    waitUntil: 'networkidle',
    timeout: 60000
  });

  // 페이지가 완전히 로드될 때까지 대기
  await page.waitForTimeout(10000);

  console.log('\n=== Network images loaded:', imageUrls.length, '===');
  imageUrls.forEach((url, idx) => {
    console.log(`${idx + 1}. ${url}`);
  });

  // 페이지의 모든 img 태그 검사
  const images = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('img')).map(img => ({
      src: img.src,
      srcset: img.srcset,
      dataSrc: img.getAttribute('data-src')
    }));
  });

  console.log('\n=== IMG tags found:', images.length, '===');
  images.forEach((img, idx) => {
    console.log(`\n${idx + 1}.`);
    console.log('  src:', img.src);
    if (img.srcset) console.log('  srcset:', img.srcset);
    if (img.dataSrc) console.log('  data-src:', img.dataSrc);
  });

  await browser.close();
})();
