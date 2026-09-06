/**
 * Генерация ОРИГИНАЛЬНОЙ музыки и звуковых эффектов (синтез).
 * Всё создаётся программно → права принадлежат проекту, коммерческое
 * использование разрешено (см. LICENSES.md).
 * Запуск: node scripts/gen-audio.mjs
 */
import fs from 'fs';
import path from 'path';
import {fileURLToPath} from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(__dirname, '../public/audio');
fs.mkdirSync(OUT, {recursive: true});

const SR = 44100;

function writeWav(name, left, right) {
  const n = left.length;
  const buf = Buffer.alloc(44 + n * 4);
  buf.write('RIFF', 0);
  buf.writeUInt32LE(36 + n * 4, 4);
  buf.write('WAVE', 8);
  buf.write('fmt ', 12);
  buf.writeUInt32LE(16, 16);
  buf.writeUInt16LE(1, 20); // PCM
  buf.writeUInt16LE(2, 22); // stereo
  buf.writeUInt32LE(SR, 24);
  buf.writeUInt32LE(SR * 4, 28);
  buf.writeUInt16LE(4, 32);
  buf.writeUInt16LE(16, 34);
  buf.write('data', 36);
  buf.writeUInt32LE(n * 4, 40);
  for (let i = 0; i < n; i++) {
    const l = Math.max(-1, Math.min(1, left[i]));
    const r = Math.max(-1, Math.min(1, right[i]));
    buf.writeInt16LE((l * 32767) | 0, 44 + i * 4);
    buf.writeInt16LE((r * 32767) | 0, 46 + i * 4);
  }
  fs.writeFileSync(path.join(OUT, name), buf);
  console.log('ok', name, (buf.length / 1024 / 1024).toFixed(2) + 'MB', (n / SR).toFixed(1) + 's');
}

const silence = (sec) => new Float32Array(Math.ceil(sec * SR));
const note = (n) => 440 * Math.pow(2, (n - 69) / 12); // midi→Hz

/* ---------------- МУЗЫКА: атмосферный технологичный эмбиент ---------------- */
function music(seconds = 31) {
  const N = Math.ceil(seconds * SR);
  const L = new Float32Array(N);
  const R = new Float32Array(N);

  // аккордовая основа Amaj9 (A C# E G# B), спокойная, «архитектурная»
  const roots = [note(45), note(52)]; // A2, E3 — дрон-квинта
  const pad = [note(57), note(61), note(64), note(68), note(71)]; // A3 C#4 E4 G#4 B4

  // мягкое стерео-хорус-расстроение
  const detune = 1.003;

  for (let i = 0; i < N; i++) {
    const t = i / SR;
    // общая огибающая: вход 0-2с, набор к 16с, ровно, деликатный спад в конце
    const intro = Math.min(1, t / 2);
    const build = 0.55 + 0.45 * Math.min(1, t / 16);
    const outro = t > seconds - 3 ? Math.max(0, (seconds - t) / 3) : 1;
    const env = intro * build * outro;

    let l = 0;
    let r = 0;

    // дрон
    for (const f of roots) {
      l += 0.12 * Math.sin(2 * Math.PI * f * t);
      r += 0.12 * Math.sin(2 * Math.PI * f * detune * t);
    }
    // пад с медленной амплитудной модуляцией на каждый голос
    pad.forEach((f, k) => {
      const lfo = 0.5 + 0.5 * Math.sin(2 * Math.PI * (0.05 + k * 0.017) * t + k);
      const amp = 0.05 * lfo;
      l += amp * Math.sin(2 * Math.PI * f * t + k);
      r += amp * Math.sin(2 * Math.PI * f * detune * t + k + 0.3);
    });
    // мерцающий верх (входит после 6с)
    if (t > 6) {
      const shimT = Math.min(1, (t - 6) / 6);
      const sh = 0.03 * shimT * (0.5 + 0.5 * Math.sin(2 * Math.PI * 0.2 * t));
      l += sh * Math.sin(2 * Math.PI * note(76) * t);
      r += sh * Math.sin(2 * Math.PI * note(83) * t);
    }
    // мягкое цифровое арпеджио (входит после 4с) — деликатные «капли»
    if (t > 4) {
      const seq = [note(69), note(73), note(76), note(71), note(80)];
      const step = 0.75; // сек
      const idx = Math.floor(t / step);
      const local = t - idx * step;
      const f = seq[idx % seq.length];
      const pluck = Math.exp(-local * 6) * 0.09 * Math.min(1, (t - 4) / 4);
      const v = pluck * (Math.sin(2 * Math.PI * f * t) + 0.4 * Math.sin(2 * Math.PI * 2 * f * t));
      // панорама по шагам
      const pan = (idx % 2) * 0.6 - 0.3;
      l += v * (0.5 - pan * 0.5);
      r += v * (0.5 + pan * 0.5);
    }

    L[i] = l * env;
    R[i] = r * env;
  }

  // нормализация к ~-3 dBFS
  let peak = 0;
  for (let i = 0; i < N; i++) peak = Math.max(peak, Math.abs(L[i]), Math.abs(R[i]));
  const g = peak > 0 ? 0.7 / peak : 1;
  for (let i = 0; i < N; i++) {
    L[i] *= g;
    R[i] *= g;
  }
  writeWav('music.wav', L, R);
}

/* ---------------- ЗВУКОВЫЕ ЭФФЕКТЫ ---------------- */
function tick() {
  const N = Math.ceil(0.06 * SR);
  const L = new Float32Array(N);
  const R = new Float32Array(N);
  for (let i = 0; i < N; i++) {
    const t = i / SR;
    const e = Math.exp(-t * 90);
    const s = e * (Math.sin(2 * Math.PI * 2100 * t) * 0.6 + (Math.random() * 2 - 1) * 0.15 * Math.exp(-t * 300));
    L[i] = R[i] = s * 0.5;
  }
  writeWav('sfx_tick.wav', L, R);
}

function whoosh() {
  const N = Math.ceil(0.5 * SR);
  const L = new Float32Array(N);
  const R = new Float32Array(N);
  let lp = 0;
  for (let i = 0; i < N; i++) {
    const t = i / SR;
    const env = Math.sin(Math.PI * (t / 0.5)); // колокол
    const noise = Math.random() * 2 - 1;
    lp += (noise - lp) * (0.02 + 0.15 * (t / 0.5)); // растущий lowpass
    const swept = 0.2 * Math.sin(2 * Math.PI * (200 + 600 * t / 0.5) * t);
    const s = (lp * 0.8 + swept) * env * 0.4;
    L[i] = s * (0.6 + 0.4 * (1 - t / 0.5));
    R[i] = s * (0.6 + 0.4 * (t / 0.5));
  }
  writeWav('sfx_whoosh.wav', L, R);
}

function impact() {
  const N = Math.ceil(1.6 * SR);
  const L = new Float32Array(N);
  const R = new Float32Array(N);
  for (let i = 0; i < N; i++) {
    const t = i / SR;
    const sub = Math.exp(-t * 3.2) * Math.sin(2 * Math.PI * (70 - 25 * Math.min(1, t)) * t);
    const body = Math.exp(-t * 5) * Math.sin(2 * Math.PI * 160 * t) * 0.4;
    const shimmer = Math.exp(-t * 1.6) * 0.14 * (Math.sin(2 * Math.PI * note(76) * t) + Math.sin(2 * Math.PI * note(83) * t));
    const click = Math.exp(-t * 200) * (Math.random() * 2 - 1) * 0.2;
    const s = (sub * 0.8 + body + shimmer + click) * 0.7;
    L[i] = R[i] = s;
  }
  writeWav('sfx_impact.wav', L, R);
}

/* озвучка-заглушка (тишина 31с) — заменяется реальной начиткой */
function voicePlaceholder() {
  const s = silence(31);
  writeWav('voiceover_ru.wav', s, s);
}

music();
tick();
whoosh();
impact();
voicePlaceholder();
console.log('\nАудио сгенерировано в public/audio/');
