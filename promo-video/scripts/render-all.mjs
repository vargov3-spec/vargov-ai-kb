/**
 * Последовательный рендер всех версий ролика в MP4 (H.264).
 * Запуск: node scripts/render-all.mjs [id1 id2 ...]
 * Без аргументов рендерит полный набор.
 */
import {spawnSync} from 'child_process';
import fs from 'fs';
import path from 'path';
import {fileURLToPath} from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
fs.mkdirSync(path.join(ROOT, 'out'), {recursive: true});

const CHROME = findChrome();

const ALL = [
  {id: 'MainLandscape', out: 'out/vargov-configurator_1920x1080.mp4'},
  {id: 'MainVertical', out: 'out/vargov-configurator_1080x1920.mp4'},
  {id: 'MainSquare', out: 'out/vargov-configurator_1080x1080.mp4'},
  {id: 'ShortLandscape', out: 'out/vargov-configurator_short_1920x1080.mp4'},
  {id: 'ShortVertical', out: 'out/vargov-configurator_short_1080x1920.mp4'},
  {id: 'MainLandscapeVoice', out: 'out/vargov-configurator_1920x1080_voice.mp4'},
];

const wanted = process.argv.slice(2);
const jobs = wanted.length ? ALL.filter((j) => wanted.includes(j.id)) : ALL;

for (const job of jobs) {
  console.log(`\n===== Рендер ${job.id} → ${job.out} =====`);
  // путь к Chrome берётся из remotion.config.ts (setBrowserExecutable),
  // чтобы пробел в "Program Files" не ломал аргумент командной строки.
  const args = ['remotion', 'render', job.id, job.out, '--log=info'];
  const r = spawnSync('npx', args, {cwd: ROOT, stdio: 'inherit', shell: true});
  if (r.status !== 0) {
    console.error(`!!! Ошибка рендера ${job.id} (код ${r.status})`);
  } else {
    console.log(`+++ Готово: ${job.out}`);
  }
}
console.log('\nВсе задания завершены.');

function findChrome() {
  const cands = [
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
  ];
  return cands.find((p) => fs.existsSync(p)) || '';
}
