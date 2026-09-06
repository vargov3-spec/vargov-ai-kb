// Вырезает реальные фрагменты из скриншотов конфигуратора в public/.
// Запуск: node scripts/crop-assets.mjs
import Jimp from 'jimp';
import path from 'path';
import {fileURLToPath} from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SHOTS = path.resolve(__dirname, '../../..', 'защита контента/configurator/shots');
const OUT = path.resolve(__dirname, '../public/shots');

const jobs = [
  // LC0536 — хрустальный каскад (шаг 01)
  {src: 'live-final.png', box: [142, 436, 298, 302], out: 'product-crop.png'},
  // изометрический 3D-рендер (запасной вариант / текстура)
  {src: 'designer-full.png', box: [150, 1780, 950, 800], out: '3d-iso.png'},
  // вид сверху + сбоку (технические проекции)
  {src: 'v4-views-crop.png', box: [40, 10, 1160, 620], out: 'views.png'},
];

for (const j of jobs) {
  try {
    const img = await Jimp.read(path.join(SHOTS, j.src));
    const [x, y, w, h] = j.box;
    img.crop(x, y, Math.min(w, img.bitmap.width - x), Math.min(h, img.bitmap.height - y));
    await img.writeAsync(path.join(OUT, j.out));
    console.log('ok', j.out, img.bitmap.width + 'x' + img.bitmap.height);
  } catch (e) {
    console.error('fail', j.out, e.message);
  }
}
