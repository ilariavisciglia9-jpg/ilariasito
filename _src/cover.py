#!/usr/bin/env python3
"""Crea l'immagine di copertina (1200x630) per gli articoli del blog che non ne hanno una.
Uso:  python3 _src/cover.py          (crea solo quelle mancanti)
      python3 _src/cover.py --tutte  (le rigenera tutte)
Per usare una foto tua: salvala come images/blog/<slug>.jpg (1200x630) e non verrà sovrascritta."""
import glob, hashlib, json, math, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD = os.path.join(ROOT, '_src', 'cover-fonts')
W, H = 1200, 630
CYAN, PINK, LIME, AMBER = (56, 242, 255), (255, 63, 209), (184, 255, 60), (255, 194, 61)
PALETTES = [(CYAN, PINK, LIME), (PINK, CYAN, AMBER), (LIME, CYAN, PINK), (AMBER, PINK, CYAN)]

def font(name, size): return ImageFont.truetype(os.path.join(FD, name + '.ttf'), size)

def wrap(draw, text, fnt, maxw):
    lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if draw.textlength(t, font=fnt) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur)
    return lines

def glow(size, xy, r, col, a):
    lay = Image.new('RGBA', size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).ellipse([xy[0] - r, xy[1] - r, xy[0] + r, xy[1] + r], fill=col + (a,))
    return lay.filter(ImageFilter.GaussianBlur(r / 2.2))

def make(p, out):
    h = int(hashlib.md5(p['slug'].encode()).hexdigest(), 16)
    c1, c2, c3 = PALETTES[h % len(PALETTES)]
    im = Image.new('RGBA', (W, H), (5, 6, 11, 255))
    im.alpha_composite(glow((W, H), (1050, 40), 420, c1, 70))
    im.alpha_composite(glow((W, H), (80, 600), 380, c2, 55))
    gr = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gr)
    for x in range(0, W, 56): gd.line([(x, 0), (x, H)], fill=(120, 210, 255, 22))
    for y in range(0, H, 56): gd.line([(0, y), (W, y)], fill=(120, 210, 255, 22))
    im.alpha_composite(gr)
    d = ImageDraw.Draw(im)
    # pavimento in prospettiva (come il banner del sito)
    fl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(fl)
    hy = 470
    for i in range(-14, 15):
        fd.line([(W / 2 + i * 22, hy), (W / 2 + i * 150, H)], fill=c2 + (55,), width=1)
    y, step = hy, 6
    while y < H: fd.line([(0, y), (W, y)], fill=c2 + (60,), width=1); step *= 1.35; y += step
    im.alpha_composite(fl)
    # monitor stilizzato a destra
    mx, my, mw, mh = 790, 120, 330, 230
    d.rounded_rectangle([mx, my, mx + mw, my + mh], 16, fill=(10, 13, 24, 255), outline=c1 + (255,), width=3)
    d.rectangle([mx + 3, my + 3, mx + mw - 3, my + 30], fill=(14, 20, 40, 255))
    for i, c in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
        d.ellipse([mx + 16 + i * 18, my + 11, mx + 26 + i * 18, my + 21], fill=c + (255,))
    mono = font('jetbrains-mono-latin-600-normal', 15)
    codes = ['> ' + p.get('category', 'blog').lower().replace(' ', '_') + '.init()', '  domanda: true,', '  risposta: "chiara",', '  cliente: felice', '> pronto_', ]
    for i, s in enumerate(codes):
        d.text((mx + 18, my + 48 + i * 32), s, font=mono, fill=(c1, (217, 225, 245), (217, 225, 245), c3, c1)[i] + (255,))
    d.rectangle([mx + mw / 2 - 40, my + mh, mx + mw / 2 + 40, my + mh + 34], fill=(20, 26, 46, 255))
    d.rounded_rectangle([mx + mw / 2 - 95, my + mh + 34, mx + mw / 2 + 95, my + mh + 46], 6, fill=(20, 26, 46, 255), outline=c1 + (120,))
    # testi
    pix = font('press-start-2p-latin-400-normal', 16)
    d.rectangle([64, 74, 76, 86], fill=c3 + (255,))
    d.text((92, 72), ('BLOG · ' + p.get('category', '')).upper(), font=pix, fill=c1 + (255,))
    size = 64
    while True:
        tf = font('chakra-petch-latin-700-normal', size)
        lines = wrap(d, p['title'].upper(), tf, 680)
        if len(lines) <= 4 or size <= 40: break
        size -= 4
    y = 130
    for ln in lines:
        d.text((64, y), ln, font=tf, fill=(255, 255, 255, 255)); y += int(size * 1.08)
    bar = Image.new('RGBA', (260, 6))
    for x in range(260):
        t = x / 259
        a, b = (c1, c2) if t < .6 else (c2, c3); tt = t / .6 if t < .6 else (t - .6) / .4
        ImageDraw.Draw(bar).line([(x, 0), (x, 6)], fill=tuple(int(a[k] + (b[k] - a[k]) * tt) for k in range(3)) + (255,))
    im.alpha_composite(bar, (64, y + 18))
    d.text((64, H - 70), 'ilariavisciglia.it', font=font('jetbrains-mono-latin-600-normal', 22), fill=(159, 171, 200, 255))
    im.convert('RGB').save(out, 'JPEG', quality=86, optimize=True, progressive=True)

if __name__ == '__main__':
    allf = '--tutte' in sys.argv
    os.makedirs(os.path.join(ROOT, 'images', 'blog'), exist_ok=True)
    for f in sorted(glob.glob(os.path.join(ROOT, '_src', 'blog', '*.json'))):
        p = json.load(open(f, encoding='utf-8'))
        out = os.path.join(ROOT, 'images', 'blog', p['slug'] + '.jpg')
        if allf or not os.path.exists(out):
            make(p, out); print('copertina:', os.path.relpath(out, ROOT))
