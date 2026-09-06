/**
 * Превью-кадры (JPG) для каждой версии ролика.
 * Запуск: node scripts/render-stills.mjs
 */
import {spawnSync} from 'child_process';
import fs from 'fs';
import path from 'path';
import {fileURLToPath} from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
fs.mkdirSync(path.join(ROOT, 'out/previews'), {recursive: true});
const CHROME = findChrome();

// кадр финальной сцены (лого + CTA) — узнаваемое превью
const stills = [
  {id: 'MainLandscape', frame: 862, out: 'out/previews/preview_1920x1080.jpg'},
  {id: 'MainLandscape', frame: 470, out: 'out/previews/preview_1920x1080_3d.jpg'},
  {id: 'MainVertical', frame: 862, out: 'out/previews/preview_1080x1920.jpg'},
  {id: 'MainSquare', frame: 862, out: 'out/previews/preview_1080x1080.jpg'},
  {id: 'ShortLandscape', frame: 330, out: 'out/previews/preview_short_1920x1080.jpg'},
];

for (const s of stills) {
  console.log(`\nПревью ${s.id} @${s.frame} → ${s.out}`);
  // путь к Chrome берётся из remotion.config.ts (setBrowserExecutable)
  const args = ['remotion', 'still', s.id, s.out, `--frame=${s.frame}`, '--image-format=jpeg', '--jpeg-quality=92', '--log=error'];
  spawnSync('npx', args, {cwd: ROOT, stdio: 'inherit', shell: true});
}
console.log('\nПревью готовы в out/previews/');

function findChrome() {
  const cands = [
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
  ];
  return cands.find((p) => fs.existsSync(p)) || '';
}
