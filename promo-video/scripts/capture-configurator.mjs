/**
 * (Опционально) Автоматическая запись реального интерфейса конфигуратора
 * через Playwright — если нужна «настоящая» запись экрана вместо
 * код-рекреации.
 *
 * Требуется один раз установить:
 *   npm i -D playwright
 *   npx playwright install chromium
 *
 * Запуск:
 *   node scripts/capture-configurator.mjs
 *
 * Результат: public/interior/configurator-capture.webm (+ раскадровка PNG).
 * Затем этот ролик можно вставить через <Video> в нужную сцену Remotion.
 *
 * Скрипт «мягкий»: если селектор не найден — шаг пропускается, запись
 * продолжается. Настройте шаги под текущую вёрстку сайта при необходимости.
 */
import path from 'path';
import fs from 'fs';
import {fileURLToPath} from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(__dirname, '../public/interior');
fs.mkdirSync(OUT, {recursive: true});
const URL = 'https://configurator.vargov.ru/';

let chromium;
try {
  ({chromium} = await import('playwright'));
} catch {
  console.error('Playwright не установлен. Выполните:\n  npm i -D playwright\n  npx playwright install chromium');
  process.exit(1);
}

const browser = await chromium.launch({headless: true});
const context = await browser.newContext({
  viewport: {width: 1920, height: 1080},
  deviceScaleFactor: 2,
  recordVideo: {dir: OUT, size: {width: 1920, height: 1080}},
});
const page = await context.newPage();

// плавное движение мыши между точками
async function glide(x, y, steps = 40) {
  await page.mouse.move(x, y, {steps});
}
const wait = (ms) => page.waitForTimeout(ms);
async function shot(name) {
  try {
    await page.screenshot({path: path.join(OUT, `cap-${name}.png`)});
  } catch {}
}
async function tryDo(label, fn) {
  try {
    await fn();
  } catch (e) {
    console.warn(`пропущен шаг «${label}»: ${e.message}`);
  }
}

console.log('Открываю конфигуратор…');
await page.goto(URL, {waitUntil: 'networkidle', timeout: 60000});
await wait(1500);
await shot('home');

// 1) Артикул
await tryDo('ввод артикула', async () => {
  const input = page.locator('input').first();
  await input.scrollIntoViewIfNeeded();
  await input.click();
  await input.fill('');
  for (const ch of 'LC0536') {
    await input.type(ch, {delay: 90});
  }
  await wait(1200);
});
await shot('article');

// 2) Габариты — меняем несколько полей
await tryDo('габариты', async () => {
  const inputs = page.locator('input');
  const n = Math.min(await inputs.count(), 5);
  for (let i = 1; i < n; i++) {
    const el = inputs.nth(i);
    await el.scrollIntoViewIfNeeded();
    await el.click();
    await wait(400);
  }
});
await shot('dims');

// 3) Форма — кликаем карточки форм по тексту
for (const shape of ['Каскад', 'Шар', 'Полусфера']) {
  await tryDo(`форма ${shape}`, async () => {
    const card = page.getByText(shape, {exact: true}).first();
    await card.scrollIntoViewIfNeeded();
    const box = await card.boundingBox();
    if (box) await glide(box.x + box.width / 2, box.y + box.height / 2);
    await card.click();
    await wait(1400);
  });
}
await shot('shape');

// 4) Плотность
for (const d of ['Воздушная', 'Насыщенная', 'Средняя']) {
  await tryDo(`плотность ${d}`, async () => {
    const btn = page.getByText(d, {exact: true}).first();
    await btn.click();
    await wait(1200);
  });
}
await shot('density');

// 5) Прокрутка к 3D-виду
await tryDo('3D-вид', async () => {
  const v = page.getByText('3D-ВИД', {exact: false}).first();
  await v.scrollIntoViewIfNeeded();
  await wait(2500);
});
await shot('viewport');

await wait(1000);
await context.close(); // финализирует видео
await browser.close();
console.log('Готово. Видео и кадры — в public/interior/');
