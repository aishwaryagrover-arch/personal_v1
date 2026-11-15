// Render the logo SVGs to transparent PNGs with the pre-installed Chromium,
// plus a contact sheet (preview.png) for a quick visual check.
// Usage: node render_png.js <logo_dir>
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const dir = process.argv[2];
const svgDir = path.join(dir, 'svg');
const pngDir = path.join(dir, 'png');
fs.mkdirSync(pngDir, { recursive: true });

// [svg file, output name, width px] — height follows the SVG's aspect ratio
const jobs = [
  ['ovelto-mark-light.svg', 'ovelto-mark-light-1024.png', 1024],
  ['ovelto-mark-light.svg', 'ovelto-mark-light-512.png', 512],
  ['ovelto-mark-dark.svg', 'ovelto-mark-dark-1024.png', 1024],
  ['ovelto-mark-mono-teal.svg', 'ovelto-mark-mono-teal-1024.png', 1024],
  ['ovelto-mark-mono-white.svg', 'ovelto-mark-mono-white-1024.png', 1024],
  ['ovelto-lockup-light.svg', 'ovelto-lockup-light-2000.png', 2000],
  ['ovelto-lockup-dark.svg', 'ovelto-lockup-dark-2000.png', 2000],
  ['ovelto-lockup-mono-teal.svg', 'ovelto-lockup-mono-teal-2000.png', 2000],
  ['ovelto-lockup-mono-white.svg', 'ovelto-lockup-mono-white-2000.png', 2000],
  ['ovelto-lockup-stacked-light.svg', 'ovelto-lockup-stacked-light-1000.png', 1000],
  ['ovelto-lockup-stacked-dark.svg', 'ovelto-lockup-stacked-dark-1000.png', 1000],
  ['ovelto-app-icon.svg', 'ovelto-app-icon-1024.png', 1024],
  ['ovelto-app-icon.svg', 'apple-touch-icon-180.png', 180],
  ['ovelto-mark-small.svg', 'favicon-48.png', 48],
  ['ovelto-mark-small.svg', 'favicon-32.png', 32],
  ['ovelto-mark-small.svg', 'favicon-16.png', 16],
];

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const [svg, out, w] of jobs) {
    const src = fs.readFileSync(path.join(svgDir, svg), 'utf8');
    const vb = src.match(/viewBox="([\d.\s-]+)"/)[1].split(/\s+/).map(Number);
    const h = Math.round((w * vb[3]) / vb[2]);
    await page.setViewportSize({ width: w, height: h });
    // Inline the SVG at the exact output size on a transparent page
    const sized = src.replace(/<\?xml[^>]*>/, '').replace(/width="[\d.]+" height="[\d.]+"/, `width="${w}" height="${h}"`);
    await page.setContent(`<html><body style="margin:0;background:transparent">${sized}</body></html>`);
    await page.screenshot({ path: path.join(pngDir, out), omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } });
  }

  // Contact sheet: each asset on the ground it is meant for
  const tile = (f, bg, w) => `<div style="background:${bg};padding:24px;border-radius:12px;display:flex;align-items:center;justify-content:center"><img src="data:image/svg+xml;base64,${Buffer.from(fs.readFileSync(path.join(svgDir, f))).toString('base64')}" style="width:${w}px"></div>`;
  const html = `<html><body style="margin:0;padding:24px;background:#EDF0F4;font-family:sans-serif;display:grid;grid-template-columns:repeat(3,1fr);gap:16px;width:1400px">
    ${tile('ovelto-lockup-light.svg', '#F3F7F1', 400)}${tile('ovelto-lockup-dark.svg', '#08303A', 400)}${tile('ovelto-lockup-mono-teal.svg', '#FFFFFF', 400)}
    ${tile('ovelto-lockup-stacked-light.svg', '#F3F7F1', 220)}${tile('ovelto-mark-light.svg', '#FFFFFF', 220)}${tile('ovelto-app-icon.svg', '#F3F7F1', 180)}
    ${tile('ovelto-lockup-mono-white.svg', '#08303A', 400)}${tile('ovelto-mark-dark.svg', '#08303A', 220)}
    <div style="background:#fff;padding:24px;border-radius:12px;display:flex;gap:20px;align-items:center;justify-content:center">
      <img src="png/favicon-48.png"><img src="png/favicon-32.png"><img src="png/favicon-16.png"></div>
  </body></html>`;
  fs.writeFileSync(path.join(dir, 'preview.html'), html);
  await page.setViewportSize({ width: 1448, height: 900 });
  await page.goto('file://' + path.join(dir, 'preview.html'));
  await page.screenshot({ path: path.join(dir, 'preview.png'), fullPage: true });
  await browser.close();
  console.log('PNGs:', fs.readdirSync(pngDir).length);
})();
