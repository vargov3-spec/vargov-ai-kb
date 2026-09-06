/**
 * Генерация русской озвучки диктора локальным голосом Windows (Microsoft Irina),
 * с автоподгонкой темпа под длительность ролика и нормализацией громкости.
 * Запуск: node scripts/gen-voice.mjs
 *
 * Премиальный нейросетевой голос (seed_audio/ElevenLabs) можно подставить
 * вручную: положите файл как public/audio/voiceover_ru.wav (или .mp3) и
 * обновите AUDIO.voiceover в video.config.ts. См. NARRATION.md.
 */
import {spawnSync} from 'child_process';
import fs from 'fs';
import path from 'path';
import {fileURLToPath} from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const AUDIO = path.join(ROOT, 'public/audio');
const RAW = path.join(AUDIO, 'voiceover_ru_sapi.wav');
const OUT = path.join(AUDIO, 'voiceover_ru.wav');
const TARGET_SEC = 27.5; // целевая длительность речи (ролик 30 c)
const VOICE = 'Microsoft Irina Desktop';

const TEXT =
  'Представляем первый генеративный 3D-конфигуратор подвесных световых и декоративных ' +
  'композиций Vargov Design. Выберите дизайн, задайте размеры, количество элементов и геометрию. ' +
  'Создайте индивидуальную композицию для конкретного пространства и оцените результат в реальном ' +
  'времени. Создавайте композиции, которых ещё не существовало. Vargov Design.';

// 1) SAPI → сырой wav
const ps = `Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; $s.SelectVoice('${VOICE}'); $s.Rate = 0; $s.Volume = 100; $s.SetOutputToWaveFile('${RAW.replace(/\\/g, '\\\\')}'); $s.Speak([Console]::In.ReadToEnd()); $s.Dispose()`;
console.log('Синтез речи (Microsoft Irina)…');
const gen = spawnSync('powershell', ['-NoProfile', '-Command', ps], {input: TEXT, encoding: 'utf8'});
if (gen.status !== 0 || !fs.existsSync(RAW)) {
  console.error('Не удалось синтезировать речь.', gen.stderr);
  process.exit(1);
}

// 2) длительность сырого файла
const probe = spawnSync('npx', ['remotion', 'ffprobe', RAW], {cwd: ROOT, encoding: 'utf8', shell: true});
const m = (probe.stdout + probe.stderr).match(/Duration:\s*(\d+):(\d+):([\d.]+)/);
const rawSec = m ? +m[1] * 3600 + +m[2] * 60 + +m[3] : TARGET_SEC;
const tempo = Math.min(1.3, Math.max(0.9, rawSec / TARGET_SEC));
console.log(`Сырая длительность ${rawSec.toFixed(1)} c → темп ×${tempo.toFixed(3)} → ~${TARGET_SEC} c`);

// 3) темп + нормализация громкости → финальный wav (44.1k stereo)
const ff = spawnSync(
  'npx',
  ['remotion', 'ffmpeg', '-y', '-i', RAW, '-af', `atempo=${tempo.toFixed(3)},loudnorm=I=-19:TP=-2:LRA=11,aresample=44100`, '-ac', '2', OUT],
  {cwd: ROOT, encoding: 'utf8', shell: true},
);
if (ff.status !== 0 || !fs.existsSync(OUT)) {
  console.error('Ошибка обработки аудио.', ff.stderr);
  process.exit(1);
}
console.log('Готово:', path.relative(ROOT, OUT));
console.log('Теперь: npm run render:voice');
