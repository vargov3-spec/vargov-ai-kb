# -*- coding: utf-8 -*-
"""Assembles the EN promo: browser takes + real-ceiling photography + end card."""
import json, os, subprocess, sys
from PIL import Image

REC = 'V:/Vargov Design в ИИ/promo-video/out/promo-rec-en'
WORK = 'C:/Users/PC/AppData/Local/Temp/claude/V--Vargov-Design-----/42630be1-02bb-43ed-bd05-f305fb27839a/scratchpad/promo-build'
OUT = 'V:/Vargov Design в ИИ/promo-video/out/configurator-promo-en-1080p.mp4'
PHOTOS_DIR = 'V:/vargov.design/фото с выставки 2025'
FONT = 'V:/Vargov Design в ИИ/promo-video/public/fonts/Montserrat-Light.ttf'
FONT_MED = 'V:/Vargov Design в ИИ/promo-video/public/fonts/Montserrat-Medium.ttf'
LOGO = 'V:/Vargov Design в ИИ/video-studio/backend/var/storage/brand/logo_white.png'
os.makedirs(WORK, exist_ok=True)


def run(args):
    r = subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode:
        print(' '.join(args[:12]), '...')
        print(r.stderr[-2500:])
        sys.exit(1)


takes = {t['name']: t['video'].replace('\\', '/') for t in json.load(open(f'{REC}/marks.json', encoding='utf-8'))}

# ── 1. browser takes → mp4 segments ──────────────────────────────────────────
SEGS = [
    ('a', takes['A-shapes'], 1.60, 31.50),   # hero → dimensions → 8 shapes
    ('b', takes['B-density'], 3.90, 17.00),  # airy → medium → dense
    ('c', takes['C-ar'], 3.90, 7.00),        # AR tap
]
parts = []
for name, src, ss, dur in SEGS:
    dst = f'{WORK}/seg_{name}.mp4'
    run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-t', str(dur), '-i', src,
         '-vf', 'fps=25,scale=1920:1080,format=yuv420p', '-c:v', 'libx264', '-crf', '17',
         '-preset', 'medium', '-an', dst])
    parts.append((dst, dur))

# ── 2. real-ceiling photography ─────────────────────────────────────────────
# DSC05193 — a phone held up to the installation: the literal bridge from AR
# to the room. Then texture, scale and craft.
PHOTOS = [('DSC05193', 'in'), ('DSC05015', 'out'), ('DSC05165', 'in'), ('DSC04773', 'out')]
PHOTO_DUR = 3.2

# подпись на первом кадре фотоблока — тем же шрифтом и в той же позиции,
# что и подписи внутри интерфейса
from PIL import ImageDraw, ImageFont

def caption_png(path, kicker, line):
    im = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    def tracked(text, y, size, color, spacing, font_path):
        f = ImageFont.truetype(font_path, size)
        widths = [d.textlength(ch, font=f) for ch in text]
        total = sum(widths) + spacing * (len(text) - 1)
        x = (1920 - total) / 2
        for ch, w in zip(text, widths):
            d.text((x, y), ch, font=f, fill=color)
            x += w + spacing

    tracked(kicker.upper(), 928, 15, (201, 162, 107, 255), 3.4, FONT_MED)
    tracked(line, 958, 33, (242, 239, 233, 255), 0.4, FONT)
    im.save(path)


CAP1 = f'{WORK}/cap_photo.png'
caption_png(CAP1, 'hand-blown glass', 'From the browser to a real ceiling')

for i, (name, direction) in enumerate(PHOTOS):
    crop = f'{WORK}/photo_{i}.png'
    im = Image.open(f'{PHOTOS_DIR}/{name}.jpg')
    w, h = im.size
    th = int(w * 9 / 16)
    top = max(0, (h - th) // 2)
    im.crop((0, top, w, top + th)).resize((3840, 2160), Image.LANCZOS).save(crop)
    frames = int(PHOTO_DUR * 25)
    z = (f"'min(1+0.00095*on,1.08)'" if direction == 'in' else f"'max(1.08-0.00095*on,1)'")
    dst = f'{WORK}/photo_{i}.mp4'
    pan = (f"zoompan=z={z}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
           f"d={frames}:s=1920x1080:fps=25")
    if i == 0:
        run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-t', str(PHOTO_DUR), '-i', crop,
             '-loop', '1', '-t', str(PHOTO_DUR), '-i', CAP1,
             '-filter_complex',
             f"[0:v]{pan}[bg];"
             "[1:v]fps=25,format=rgba,fade=t=in:st=0.25:d=0.6:alpha=1,"
             f"fade=t=out:st={PHOTO_DUR - 0.7:.2f}:d=0.6:alpha=1[cap];"
             "[bg][cap]overlay=0:0,format=yuv420p[o]",
             '-map', '[o]', '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-an', dst])
    else:
        run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-t', str(PHOTO_DUR), '-i', crop,
             '-vf', f'{pan},format=yuv420p', '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-an', dst])
    parts.append((dst, PHOTO_DUR))

# ── 3. end card ─────────────────────────────────────────────────────────────
# Собирается картинкой в PIL, а не drawtext: у ffmpeg двоеточие в пути к шрифту
# ломает парсер фильтров, а трекинг букв он всё равно не умеет.
from PIL import ImageDraw, ImageFont

END_DUR = 4.6
card = Image.new('RGB', (1920, 1080), (12, 12, 14))
logo = Image.open(LOGO).convert('RGBA')
lw = 430
logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
card.paste(logo, ((1920 - lw) // 2, 1080 // 2 - 70 - logo.height // 2), logo)
d = ImageDraw.Draw(card)


def track(text, y, size, color, spacing, font_path=FONT):
    f = ImageFont.truetype(font_path, size)
    widths = [d.textlength(ch, font=f) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = (1920 - total) / 2
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=f, fill=color)
        x += w + spacing


track('vargov.design', 1080 // 2 + 112, 30, (210, 130, 0), 3.5)
track('GENERATIVE 3D CONFIGURATOR', 1080 // 2 + 172, 18, (138, 131, 119), 5.5, FONT_MED)
card_png = f'{WORK}/endcard.png'
card.save(card_png)
end = f'{WORK}/end.mp4'
run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-t', str(END_DUR), '-i', card_png,
     '-vf', 'fps=25,format=yuv420p', '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-an', end])
parts.append((end, END_DUR))

# ── 4. chain with cross-dissolves ───────────────────────────────────────────
XF = 0.6
inputs = []
for p, _ in parts:
    inputs += ['-i', p]
chain, cur = [], parts[0][1]
label = '0:v'
for i in range(1, len(parts)):
    off = cur - XF
    out = f'x{i}'
    chain.append(f'[{label}][{i}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}[{out}]')
    label = out
    cur = off + XF + parts[i][1] - 0.0
    cur = off + parts[i][1]
total = cur
chain.append(f'[{label}]fade=t=in:st=0:d=0.7,fade=t=out:st={total - 0.9:.3f}:d=0.9,format=yuv420p[v]')
# немой звуковой трек: часть площадок (LinkedIn, Instagram) капризничает на
# файлах вообще без аудиодорожки
run(['ffmpeg', '-v', 'error', '-y'] + inputs +
    ['-f', 'lavfi', '-t', f'{total:.3f}', '-i', 'anullsrc=channel_layout=stereo:sample_rate=48000',
     '-filter_complex', ';'.join(chain),
     '-map', '[v]', '-map', f'{len(parts)}:a', '-c:v', 'libx264', '-crf', '18', '-preset', 'slow',
     '-c:a', 'aac', '-b:a', '96k', '-shortest',
     '-pix_fmt', 'yuv420p', '-movflags', '+faststart', OUT])
print('OK', OUT, f'{total:.1f}s')
