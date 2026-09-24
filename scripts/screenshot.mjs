// Screenshots a site draft at phone and desktop size and runs quick layout checks.
// Usage: node scripts/screenshot.mjs sites/<slug>/index.html   (a local draft)
//        node scripts/screenshot.mjs https://example.co.uk/      (a live site)
// Writes sites/<slug>/screenshots/{mobile,desktop}.png (or screenshots/live-<host>/ for a URL)
// and prints a short report.
import { chromium } from 'playwright';
import { mkdirSync, existsSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const file = process.argv[2];
const isUrl = /^https?:\/\//i.test(file || '');
if (!file || (!isUrl && !existsSync(file))) {
  console.error('Usage: node scripts/screenshot.mjs sites/<slug>/index.html  |  https://example.co.uk/');
  process.exit(1);
}

const outDir = isUrl ? join('screenshots', 'live-' + new URL(file).host) : join(dirname(file), 'screenshots');
mkdirSync(outDir, { recursive: true });
const url = isUrl ? file : pathToFileURL(resolve(file)).href;

const viewports = [
  { name: 'mobile', width: 390, height: 844, isMobile: true, hasTouch: true, deviceScaleFactor: 2 },
  { name: 'desktop', width: 1280, height: 800, isMobile: false, hasTouch: false, deviceScaleFactor: 1 },
];

const browser = await chromium.launch();
const problems = [];

for (const vp of viewports) {
  const page = await browser.newPage({
    viewport: { width: vp.width, height: vp.height },
    isMobile: vp.isMobile,
    hasTouch: vp.hasTouch,
    deviceScaleFactor: vp.deviceScaleFactor,
  });
  const failed = [];
  page.on('requestfailed', (req) => {
    const u = req.url();
    if (u.startsWith('file:') || (isUrl && new URL(u).host === new URL(url).host)) failed.push(u.replace(/^.*\//, '') || u);
  });
  await page.goto(url, { waitUntil: 'load', timeout: 20000 }).catch(() => {});
  await page.waitForTimeout(500);

  const report = await page.evaluate(() => {
    const doc = document.documentElement;
    const wide = [...document.querySelectorAll('body *')]
      .filter((el) => el.getBoundingClientRect().right > window.innerWidth + 1 && getComputedStyle(el).position !== 'fixed')
      .filter((el) => !el.closest('.site-nav'))
      .slice(0, 5)
      .map((el) => `<${el.tagName.toLowerCase()} class="${el.className}">`);
    const badAnchors = [...document.querySelectorAll('a[href^="#"]')]
      .map((a) => a.getAttribute('href'))
      .filter((h) => h.length > 1 && !document.getElementById(h.slice(1)));
    const brokenImgs = [...document.images].filter((i) => i.complete && i.naturalWidth === 0).map((i) => i.getAttribute('src'));
    const noAlt = [...document.images].filter((i) => !i.hasAttribute('alt')).map((i) => i.getAttribute('src'));
    const placeholders = (document.documentElement.outerHTML.match(/\[PLACEHOLDER/g) || []).length;
    const smallTargets = [...document.querySelectorAll('a, button')]
      .filter((el) => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0 && r.height < 40 && !el.classList.contains('skip-link'); })
      .slice(0, 5)
      .map((el) => el.textContent.trim().slice(0, 30));
    return { overflow: doc.scrollWidth > window.innerWidth, scrollWidth: doc.scrollWidth, wide, badAnchors, brokenImgs, noAlt, placeholders, smallTargets };
  });

  const shot = join(outDir, `${vp.name}.png`);
  await page.screenshot({ path: shot, fullPage: true });
  console.log(`\n[${vp.name} ${vp.width}px] ${shot}`);
  if (report.overflow) problems.push(`${vp.name}: page scrolls sideways (${report.scrollWidth}px wide). Culprits: ${report.wide.join(', ') || 'unknown'}`);
  if (report.badAnchors.length) problems.push(`${vp.name}: nav links to missing sections: ${[...new Set(report.badAnchors)].join(', ')}`);
  if (report.brokenImgs.length || failed.length) problems.push(`${vp.name}: images/files that failed to load: ${[...new Set([...report.brokenImgs, ...failed])].join(', ')}`);
  if (report.noAlt.length) problems.push(`${vp.name}: images with no alt text: ${report.noAlt.join(', ')}`);
  if (vp.isMobile && report.smallTargets.length) problems.push(`mobile: tap targets under 40px tall: ${report.smallTargets.map((t) => `"${t}"`).join(', ')}`);
  if (vp.name === 'desktop') console.log(`Placeholders left: ${report.placeholders}`);
  await page.close();
}

await browser.close();
console.log(problems.length ? `\nProblems found:\n- ${problems.join('\n- ')}` : '\nNo layout problems found.');
