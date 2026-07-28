// EN promo, no voiceover. Three takes, each its own webm:
//   A: hero + setup + 8 composition shapes  (LC0601 — sculpted birds)
//   B: density airy → medium → dense        (LC0036 — 605 → 857 → 1500 pcs)
//   C: AR button press on the dense cloud
// Post (ffmpeg) adds: real-ceiling photography, end card, music.
import { createRequire } from 'node:module';
import { mkdirSync, writeFileSync } from 'node:fs';
const require = createRequire('V:/Vargov Design в ИИ/proposal-generator/package.json');
const { chromium } = require('playwright');

const OUT = 'V:/Vargov Design в ИИ/promo-video/out/promo-rec-en';
mkdirSync(OUT, { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const HOST = 'http://localhost:5177';

// ВАЖНО: без --use-angle=d3d11 headless-Chromium рисует через SwiftShader —
// плотное облако даёт 0.9 fps и ролик выходит слайд-шоу. С d3d11 — 58 fps.
const browser = await chromium.launch({
  headless: true,
  args: ['--enable-gpu', '--ignore-gpu-blocklist', '--use-angle=d3d11'],
});
const ctx = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  deviceScaleFactor: 1,
  recordVideo: { dir: OUT, size: { width: 1920, height: 1080 } },
});

const takes = [];
const newTake = async (url, name) => {
  const page = await ctx.newPage();
  const T0 = Date.now();
  const marks = [];
  page.__mark = (m) => { const t = (Date.now() - T0) / 1000; marks.push({ name: m, t }); console.log(`[${name}] ${m} ${t.toFixed(2)}`); };
  page.__marks = marks;
  page.__name = name;
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  await sleep(2600);
  await page.evaluate(() => {
    const s = document.createElement('style');
    s.textContent = `
    #__cap{position:fixed;left:0;right:0;bottom:70px;z-index:99998;text-align:center;
      font-family:Montserrat,'Segoe UI',sans-serif;color:#f2efe9;opacity:0;transition:opacity .45s ease;
      text-shadow:0 2px 20px rgba(0,0,0,.9);pointer-events:none}
    #__cap .l1{font-size:32px;letter-spacing:.01em;font-weight:300}
    #__cap .l2{font-size:14px;letter-spacing:.24em;text-transform:uppercase;color:#c9a26b;margin-bottom:14px}
    #__cur{position:fixed;z-index:99999;width:24px;height:24px;margin:-12px 0 0 -12px;border-radius:50%;
      background:rgba(242,239,233,.92);box-shadow:0 0 0 8px rgba(242,239,233,.14),0 4px 18px rgba(0,0,0,.6);
      opacity:0;transition:opacity .3s,transform .12s;pointer-events:none;left:960px;top:980px}
    #__cur.press{transform:scale(.6)}
    #__ring{position:fixed;z-index:99997;width:44px;height:44px;margin:-22px 0 0 -22px;border-radius:50%;
      border:2px solid rgba(210,130,0,.95);opacity:0;pointer-events:none}
    @keyframes __rr{from{transform:scale(.45);opacity:.95}to{transform:scale(2.8);opacity:0}}
    #__ring.go{animation:__rr .9s ease-out}`;
    document.head.appendChild(s);
    const c = document.createElement('div'); c.id = '__cap';
    c.innerHTML = '<div class="l2"></div><div class="l1"></div>';
    document.body.appendChild(c);
    for (const id of ['__cur', '__ring']) { const d = document.createElement('div'); d.id = id; document.body.appendChild(d); }
  });
  return page;
};
const cap = (page, kicker, line) => page.evaluate(([k, l]) => {
  const el = document.getElementById('__cap');
  el.style.opacity = '0';
  setTimeout(() => {
    el.querySelector('.l2').textContent = k;
    el.querySelector('.l1').innerHTML = l;
    el.style.opacity = '1';
  }, 440);
}, [kicker, line]);
const capOff = (page) => page.evaluate(() => { document.getElementById('__cap').style.opacity = '0'; });
const centerPanel = (page) => page.evaluate(() => {
  const p = document.querySelector('.view3d-panel');
  const b = p.getBoundingClientRect();
  window.scrollBy(0, b.top - (window.innerHeight - b.height) / 2);
});
const waitGen = async (page, maxMs = 25000) => {
  const t = Date.now();
  await sleep(220);
  while (Date.now() - t < maxMs) {
    if (!(await page.evaluate(() => !!document.querySelector('.gen-overlay')))) return;
    await sleep(120);
  }
};
const clickForm = (page, l) => page.evaluate((n) => {
  [...document.querySelectorAll('.formcard')].find((x) => x.textContent.trim() === n)?.click();
}, l);
const clickDens = (page, l) => page.evaluate((n) => {
  [...document.querySelectorAll('.seg button')].find((x) => x.textContent.trim() === n)?.click();
}, l);
const count = (page) => page.evaluate(() => document.querySelector('.metrics .spec b')?.textContent.trim().replace(' pcs', '') || '');
// медленный доворот камеры во время выдержки кадра — «поворотный стол»
const orbit = async (page, dx, ms) => {
  const b = await page.locator('.view3d-panel canvas').boundingBox();
  if (!b) { await sleep(ms); return; }
  const cx = b.x + b.width / 2, cy = b.y + b.height * 0.45;
  await page.mouse.move(cx, cy);
  await page.mouse.down();
  const n = Math.max(4, Math.round(ms / 40));
  for (let i = 1; i <= n; i++) { await page.mouse.move(cx + (dx * i) / n, cy); await sleep(40); }
  await page.mouse.up();
};
const toWhite = async (page) => {
  await page.evaluate(() => {
    document.querySelector('.el-color.white')?.click();
    const gold = document.querySelector('.el-color.gold.on');
    if (gold) setTimeout(() => gold.click(), 150);
  });
  await sleep(800);
};
const closeTake = async (page) => {
  const path = await page.video().path();
  await page.close();
  takes.push({ name: page.__name, video: path, marks: page.__marks });
};

// ══ TAKE A — hero, setup, shapes ═════════════════════════════════════════
{
  const p = await newTake(`${HOST}/?sku=LC0601&w=2400&l=1800&h=1500&form=sphere&lang=en`, 'A-shapes');
  p.__mark('hero');
  await sleep(3400);

  await cap(p, 'step 01 – 02', 'Your element. Your ceiling.');
  await p.evaluate(async () => {
    const ease = (t) => (t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2);
    for (let i = 1; i <= 30; i++) { window.scrollTo(0, 380 * ease(i / 30)); await new Promise((r) => setTimeout(r, 16)); }
  });
  p.__mark('setup');
  await sleep(2800);

  await p.evaluate(() => [...document.querySelectorAll('button')].find((b) => /Show more options/i.test(b.textContent))?.click());
  await sleep(400);
  await toWhite(p);
  await capOff(p);
  await centerPanel(p);
  await waitGen(p);
  await sleep(500);
  p.__mark('shapes');
  await cap(p, 'composition shape', 'Twenty shapes, one engine');
  await sleep(2000);

  const SHAPES = ['Sphere', 'Cone', 'Wave', 'Spiral', 'Drop / paraboloid', 'Arc / ribbon', 'Helix', 'Tiers'];
  for (let i = 0; i < SHAPES.length; i++) {
    await clickForm(p, SHAPES[i]);
    await waitGen(p);
    await cap(p, `shape ${String(i + 1).padStart(2, '0')} of 20`, SHAPES[i]);
    p.__mark(`shape_${SHAPES[i]}`);
    await orbit(p, 34, 1500);
  }
  await capOff(p);
  await sleep(700);
  p.__mark('end');
  await closeTake(p);
}

// ══ TAKE B — density ═════════════════════════════════════════════════════
{
  const p = await newTake(`${HOST}/?sku=LC0036&w=2400&l=1800&h=1500&form=cone&density=airy&lang=en`, 'B-density');
  await toWhite(p);
  await centerPanel(p);
  await waitGen(p);
  await sleep(600);
  p.__mark('start');
  await cap(p, 'density', 'From airy to dense');
  await sleep(2000);
  for (const d of ['Airy', 'Medium', 'Dense']) {
    await clickDens(p, d);
    await waitGen(p);
    await sleep(350);
    const c = await count(p);
    await cap(p, d.toLowerCase(), `${c} elements — not one of them touching`);
    p.__mark(`dens_${d}`);
    await orbit(p, 30, 2400);
  }
  await capOff(p);
  await sleep(700);
  p.__mark('end');
  await closeTake(p);
}

// ══ TAKE C — AR ══════════════════════════════════════════════════════════
{
  const p = await newTake(`${HOST}/?sku=LC0036&w=2400&l=1800&h=1500&form=cone&density=dense&lang=en`, 'C-ar');
  await toWhite(p);
  await centerPanel(p);
  await waitGen(p);
  await sleep(700);
  p.__mark('start');
  await cap(p, 'augmented reality', 'One tap — and it hangs in your room');
  await sleep(1200);
  const box = await p.locator('.ar-btn').boundingBox();
  const cx = box.x + box.width / 2, cy = box.y + box.height / 2;
  await p.evaluate(async ([tx, ty]) => {
    const cur = document.getElementById('__cur');
    cur.style.opacity = '1';
    const sx = 900, sy = 950;
    const ease = (t) => 1 - Math.pow(1 - t, 3);
    for (let i = 1; i <= 34; i++) {
      const k = ease(i / 34);
      cur.style.left = `${sx + (tx - sx) * k}px`;
      cur.style.top = `${sy + (ty - sy) * k}px`;
      await new Promise((r) => setTimeout(r, 16));
    }
  }, [cx, cy]);
  await sleep(500);
  p.__mark('tap');
  await p.evaluate(([x, y]) => {
    const cur = document.getElementById('__cur');
    const ring = document.getElementById('__ring');
    ring.style.left = `${x}px`; ring.style.top = `${y}px`; ring.style.opacity = '1';
    cur.classList.add('press');
    ring.classList.remove('go'); void ring.offsetWidth; ring.classList.add('go');
    setTimeout(() => cur.classList.remove('press'), 240);
  }, [cx, cy]);
  await p.locator('.ar-btn').click();
  await sleep(2400);
  await capOff(p);
  await p.evaluate(() => { document.getElementById('__cur').style.opacity = '0'; });
  await sleep(900);
  p.__mark('end');
  await closeTake(p);
}

await ctx.close();
writeFileSync(`${OUT}/marks.json`, JSON.stringify(takes, null, 1));
console.log(JSON.stringify(takes.map((t) => ({ name: t.name, video: t.video })), null, 1));
await browser.close();
