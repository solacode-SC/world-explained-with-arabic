const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const htmlPath = 'file://' + path.resolve(__dirname, '../How it works/كيف تُصنع الرقائق الإلكترونية؟ — أشباه الموصلات.html');
  console.log('Testing HTML path:', htmlPath);

  const errors = [];
  
  // Test Desktop
  const pageDesk = await browser.newPage({ viewport: { width: 1200, height: 750 } });
  pageDesk.on('console', msg => {
    if (msg.type() === 'error') {
      console.error('Console Error:', msg.text());
      errors.push(msg.text());
    }
  });
  pageDesk.on('pageerror', err => {
    console.error('Page Error:', err.message);
    errors.push(err.message);
  });

  await pageDesk.goto(htmlPath);
  await pageDesk.waitForTimeout(2000);
  console.log('Desktop initial loaded');
  await pageDesk.screenshot({ path: path.join(__dirname, 'shot_desk_s0.png') });

  // Jump to Scene 3 (EUV)
  const dots = await pageDesk.$$('#dots span');
  console.log('Found dots count:', dots.length);
  if (dots.length > 3) {
    await dots[3].click();
    await pageDesk.waitForTimeout(2000);
    await pageDesk.screenshot({ path: path.join(__dirname, 'shot_desk_s3.png') });
  }

  // Jump to Scene 5 (Transistor switch)
  if (dots.length > 5) {
    await dots[5].click();
    await pageDesk.waitForTimeout(2000);
    await pageDesk.screenshot({ path: path.join(__dirname, 'shot_desk_s5.png') });
  }

  // Jump to Scene 8 (Recap)
  if (dots.length > 8) {
    await dots[8].click();
    await pageDesk.waitForTimeout(2000);
    await pageDesk.screenshot({ path: path.join(__dirname, 'shot_desk_s8.png') });
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
  await pageMobile.waitForTimeout(2000);
  await pageMobile.screenshot({ path: path.join(__dirname, 'shot_mobile_s0.png') });

  const mobileDots = await pageMobile.$$('#dots span');
  if (mobileDots.length > 5) {
    await mobileDots[5].click();
    await pageMobile.waitForTimeout(2000);
    await pageMobile.screenshot({ path: path.join(__dirname, 'shot_mobile_s5.png') });
  }

  await browser.close();

  if (errors.length > 0) {
    console.error('FAILED with errors:', errors);
    process.exit(1);
  } else {
    console.log('ALL TESTS PASSED! No console or page errors.');
  }
})();

