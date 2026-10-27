const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const htmlPath = 'file://' + path.resolve(__dirname, '../History/تاريخ العملات الرقمية — من الفكرة إلى الثورة المالية.html');
  console.log('Testing Crypto History HTML path:', htmlPath);

  const errors = [];
  
  // Test Desktop
  const pageDesk = await browser.newPage({ viewport: { width: 1200, height: 750 } });
  pageDesk.on('console', msg => {
    if (msg.type() === 'error') {
      console.error('Desktop Console Error:', msg.text());
      errors.push(msg.text());
    }
  });
  pageDesk.on('pageerror', err => {
    console.error('Desktop Page Error:', err.message);
    errors.push(err.message);
  });

  await pageDesk.goto(htmlPath);
  await pageDesk.waitForTimeout(1500);
  console.log('Desktop initial loaded (Scene 0)');
  await pageDesk.screenshot({ path: path.join(__dirname, 'shot_crypto_desk_s0.png') });

  const dots = await pageDesk.$$('#dots span');
  console.log('Found dots count:', dots.length);

  // Jump to Scene 2 (Pizza Day)
  if (dots.length > 2) {
    await dots[2].click();
    await pageDesk.waitForTimeout(1500);
    await pageDesk.screenshot({ path: path.join(__dirname, 'shot_crypto_desk_s2.png') });
  }

  // Jump to Scene 4 (Ethereum)
  if (dots.length > 4) {
    await dots[4].click();
    await pageDesk.waitForTimeout(1500);
    await pageDesk.screenshot({ path: path.join(__dirname, 'shot_crypto_desk_s4.png') });
  }

  // Jump to Scene 6 (ETF Approval)
  if (dots.length > 6) {
    await dots[6].click();
    await pageDesk.waitForTimeout(1500);
    await pageDesk.screenshot({ path: path.join(__dirname, 'shot_crypto_desk_s6.png') });
  }

  // Jump to Scene 8 (Full Timeline)
  if (dots.length > 8) {
    await dots[8].click();
    await pageDesk.waitForTimeout(1500);
    await pageDesk.screenshot({ path: path.join(__dirname, 'shot_crypto_desk_s8.png') });
  }

  // Test Mobile Viewport (390 x 844 - iPhone 14)
  const pageMobile = await browser.newPage({ viewport: { width: 390, height: 844 }, isMobile: true });
  pageMobile.on('console', msg => {
    if (msg.type() === 'error') {
      console.error('Mobile Console Error:', msg.text());
      errors.push(msg.text());
    }
  });
  pageMobile.on('pageerror', err => {
    console.error('Mobile Page Error:', err.message);
    errors.push(err.message);
  });

  await pageMobile.goto(htmlPath);
  await pageMobile.waitForTimeout(1500);
  await pageMobile.screenshot({ path: path.join(__dirname, 'shot_crypto_mobile_s0.png') });

  const mobileDots = await pageMobile.$$('#dots span');
  if (mobileDots.length > 7) {
    await mobileDots[7].click();
    await pageMobile.waitForTimeout(1500);
    await pageMobile.screenshot({ path: path.join(__dirname, 'shot_crypto_mobile_s7.png') });
  }

  await browser.close();

  if (errors.length > 0) {
    console.error('FAILED with errors:', errors);
    process.exit(1);
  } else {
    console.log('ALL CRYPTO TESTS PASSED! No console or page errors.');
  }
})();

