import { chromium } from 'playwright';

const options = [
  {
    name: 'option1_fraunces',
    label: 'Option 1 — Fraunces + DM Sans',
    headingFont: 'Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,700;1,9..144,300;1,9..144,700',
    bodyFont: 'DM+Sans:wght@300;400;500',
    headingCSS: "'Fraunces', serif",
    bodyCSS: "'DM Sans', sans-serif",
  },
  {
    name: 'option2_cormorant',
    label: 'Option 2 — Cormorant Garamond + Inter',
    headingFont: 'Cormorant+Garamond:ital,wght@0,400;0,700;1,400;1,700',
    bodyFont: 'Inter:wght@300;400;500',
    headingCSS: "'Cormorant Garamond', serif",
    bodyCSS: "'Inter', sans-serif",
  },
  {
    name: 'option3_dm_serif',
    label: 'Option 3 — DM Serif Display + Nunito',
    headingFont: 'DM+Serif+Display:ital@0;1',
    bodyFont: 'Nunito:wght@300;400;500',
    headingCSS: "'DM Serif Display', serif",
    bodyCSS: "'Nunito', sans-serif",
  },
  {
    name: 'option4_lora',
    label: 'Option 4 — Lora + Outfit (warm & rounded)',
    headingFont: 'Lora:ital,wght@0,400;0,700;1,400;1,700',
    bodyFont: 'Outfit:wght@300;400;500',
    headingCSS: "'Lora', serif",
    bodyCSS: "'Outfit', sans-serif",
  },
];

const browser = await chromium.launch({
  executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  args: ['--no-sandbox', '--disable-setuid-sandbox']
});

for (const opt of options) {
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1440, height: 900 });

  const html = `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8"/>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="https://fonts.googleapis.com/css2?family=${opt.headingFont}&family=${opt.bodyFont}&display=swap" rel="stylesheet"/>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: radial-gradient(ellipse at 50% 0%, #4a1942 0%, #1a0a2e 40%, #0d0d1a 100%);
      min-height: 100vh; display: flex; flex-direction: column; align-items: center;
      justify-content: center; text-align: center; padding: 3rem 2rem; color: white;
      font-family: ${opt.bodyCSS};
      overflow: hidden;
    }
    .blob1 { position:absolute; width:420px; height:420px; background:#ec4899; border-radius:50%; filter:blur(90px); opacity:0.22; top:-80px; left:-60px; }
    .blob2 { position:absolute; width:500px; height:500px; background:#7c3aed; border-radius:50%; filter:blur(90px); opacity:0.18; top:-100px; right:-80px; }
    .option-tag {
      position: absolute; top: 20px; left: 50%; transform: translateX(-50%);
      background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.2);
      border-radius: 999px; padding: 0.4rem 1.2rem;
      font-size: 0.8rem; letter-spacing: 0.05em; color: rgba(255,255,255,0.8);
      font-family: ${opt.bodyCSS};
    }
    .tag {
      font-size: 0.7rem; letter-spacing: 0.3em; text-transform: uppercase;
      color: rgba(180,150,220,0.7); margin-bottom: 1.5rem;
      font-family: ${opt.bodyCSS};
    }
    .line1 {
      font-family: ${opt.headingCSS};
      font-size: 5rem; font-weight: 700; color: white; display: block; line-height: 1.1;
    }
    .line2 {
      font-family: ${opt.headingCSS};
      font-size: 5.5rem; font-style: italic; font-weight: 400; display: block; line-height: 1.1;
      background: linear-gradient(135deg, #ec4899, #a855f7);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
      margin-bottom: 1.8rem;
    }
    .sub {
      font-family: ${opt.bodyCSS};
      font-size: 1.1rem; color: rgba(220,200,255,0.85); line-height: 1.8;
      max-width: 600px; margin: 0 auto 1.5rem;
    }
    .sub em { color: #ec4899; font-style: italic; }
    .signed {
      font-family: ${opt.bodyCSS};
      font-size: 0.9rem; color: rgba(200,170,240,0.6); letter-spacing: 0.1em;
    }
    .counter-row {
      display: flex; gap: 1.2rem; justify-content: center; margin: 2.5rem 0 1rem;
    }
    .c-card {
      background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.09);
      border-radius: 14px; padding: 1.5rem 1.8rem; min-width: 110px;
      backdrop-filter: blur(16px);
    }
    .c-num {
      font-family: ${opt.headingCSS};
      font-size: 3rem; font-weight: 700; display: block;
      background: linear-gradient(135deg, #ec4899, #a855f7);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }
    .c-label {
      font-family: ${opt.bodyCSS};
      font-size: 0.6rem; letter-spacing: 0.25em; text-transform: uppercase;
      color: rgba(180,150,220,0.6);
    }
    .reason-row {
      display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; max-width: 700px;
      margin: 1rem auto 0;
    }
    .r-card {
      background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
      border-radius: 12px; padding: 1.2rem 1.4rem; text-align: left;
      backdrop-filter: blur(12px);
    }
    .r-num { font-family: ${opt.headingCSS}; font-size: 1.4rem; color: #ec4899; display: block; margin-bottom: 0.3rem; }
    .r-text { font-family: ${opt.bodyCSS}; font-size: 0.9rem; color: rgba(215,195,250,0.85); line-height: 1.6; }
  </style>
</head>
<body>
  <div class="blob1"></div>
  <div class="blob2"></div>
  <div class="option-tag">${opt.label}</div>
  <p class="tag">Since we said yes</p>
  <span class="line1">Happy Birthday,</span>
  <span class="line2">my Adi bear</span>
  <p class="sub">I couldn't fly to you this year, so I built you a tiny world instead. Scroll slowly — there's six months of us in here, and a lifetime of <em>more to come.</em></p>
  <p class="signed">With ❤️, Aishwarya</p>
  <div class="counter-row">
    <div class="c-card"><span class="c-num">175</span><span class="c-label">Days</span></div>
    <div class="c-card"><span class="c-num">14</span><span class="c-label">Hours</span></div>
    <div class="c-card"><span class="c-num">32</span><span class="c-label">Minutes</span></div>
    <div class="c-card"><span class="c-num">07</span><span class="c-label">Seconds</span></div>
  </div>
  <div class="reason-row">
    <div class="r-card"><span class="r-num">01</span><p class="r-text">You turn even my crying into laughter.</p></div>
    <div class="r-card"><span class="r-num">02</span><p class="r-text">You are my respite, my safe place, my shoulder.</p></div>
  </div>
</body>
</html>`;

  await page.setContent(html, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: `/home/user/personal_v1/font_${opt.name}.png`, fullPage: false });
  console.log(`captured ${opt.name}`);
  await page.close();
}

await browser.close();
console.log('done');
