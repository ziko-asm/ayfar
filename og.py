"""Renders 1200x630 share images into img/og/. Needs Pillow.

Run:  python og.py <fonts_dir>
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import IMG_SLUG, P  # noqa: E402

ROOT = os.path.dirname(os.path.abspath(__file__))
FONTS = sys.argv[1]
OUT = os.path.join(ROOT, "img", "og")
W, H = 1200, 630
BG = (5, 7, 11)


def font(name, size, weight):
    f = ImageFont.truetype(os.path.join(FONTS, name), size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def backdrop(c1, c2):
    im = Image.new("RGB", (W, H), BG)
    glow = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(glow)
    d.ellipse((-200, -260, 520, 420), fill=tuple(int(v * .45) for v in hexrgb(c1)))
    d.ellipse((760, 260, 1500, 900), fill=tuple(int(v * .4) for v in hexrgb(c2)))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    im = Image.blend(im, glow, 1)
    d = ImageDraw.Draw(im)
    for x in range(0, W, 60):
        d.line([(x, 0), (x, H)], fill=(14, 18, 26))
    for y in range(0, H, 60):
        d.line([(0, y), (W, y)], fill=(14, 18, 26))
    return im


def gradient_text(im, xy, text, fnt, c1, c2):
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).text(xy, text, font=fnt, fill=255)
    bbox = mask.getbbox() or (0, 0, 1, 1)
    grad = Image.new("RGB", im.size)
    gd = ImageDraw.Draw(grad)
    a, b = hexrgb(c1), hexrgb(c2)
    x0, x1 = bbox[0], max(bbox[2], bbox[0] + 1)
    for x in range(im.size[0]):
        t = min(1, max(0, (x - x0) / (x1 - x0)))
        gd.line([(x, 0), (x, im.size[1])], fill=tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3)))
    im.paste(grad, (0, 0), mask)


def rounded(img, r):
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, img.size[0] - 1, img.size[1] - 1), r, fill=255)
    img.putalpha(m)
    return img


def window(shot_path, w):
    shot = Image.open(shot_path).convert("RGB")
    h = int(shot.size[1] * w / shot.size[0])
    shot = shot.resize((w, h), Image.LANCZOS)
    bar = 30
    win = Image.new("RGB", (w, h + bar), (8, 11, 17))
    d = ImageDraw.Draw(win)
    for i, c in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
        d.ellipse((14 + i * 16, 11, 23 + i * 16, 20), fill=c)
    win.paste(shot, (0, bar))
    return rounded(win.convert("RGBA"), 16)


def paste_shadow(im, obj, xy, angle=0):
    if angle:
        obj = obj.rotate(angle, resample=Image.BICUBIC, expand=True)
    sh = Image.new("RGBA", (obj.size[0] + 80, obj.size[1] + 80), (0, 0, 0, 0))
    sh.paste((0, 0, 0, 170), (40, 50), obj.split()[3])
    sh = sh.filter(ImageFilter.GaussianBlur(24))
    im.paste(sh, (xy[0] - 40, xy[1] - 40), sh)
    im.paste(obj, xy, obj)


def scene_art(kind, c1):
    art = Image.new("RGBA", (560, 380), (0, 0, 0, 0))
    d = ImageDraw.Draw(art)
    d.rounded_rectangle((0, 0, 559, 379), 18, fill=(12, 10, 22, 255), outline=(60, 60, 80))
    mono = font("JetBrainsMono.ttf", 15, 600)
    if kind == "metro":
        pts = [(80, 290), (180, 290), (240, 220), (350, 220), (410, 150), (500, 150)]
        d.line(pts, fill=(229, 57, 74), width=9, joint="curve")
        for (x, y), n, dy in zip(pts, ["İçərişəhər", "28 May", "Nərimanov", "Koroğlu", "Əhmədli", "H. Aslanov"], [30, 30, -30, 30, -30, -30]):
            d.ellipse((x - 10, y - 10, x + 10, y + 10), fill=(7, 8, 13), outline=(255, 255, 255), width=3)
            d.text((x, y + dy), n, font=mono, fill=(207, 214, 224), anchor="mm")
        d.rounded_rectangle((268, 205, 328, 235), 9, fill=(255, 255, 255))
        d.rectangle((268, 222, 328, 228), fill=(229, 57, 74))
        for x, y in [(130, 290), (210, 255), (455, 150)]:
            d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=(255, 201, 77))
        d.text((30, 30), "₼ 1 250 000", font=font("Unbounded.ttf", 22, 700), fill=(255, 201, 77))
    elif kind == "nids":
        d.text((30, 26), "DETECTION RATE · PGD ε=0.5", font=mono, fill=(141, 153, 168))
        for i, (a, b) in enumerate([(.96, .07), (.95, .02), (.89, .02), (.9, .17)]):
            x = 40 + i * 125
            d.rounded_rectangle((x, 330 - int(260 * a), x + 50, 330), 6, fill=(52, 245, 176))
            d.rounded_rectangle((x + 56, 330 - int(260 * b) - 4, x + 106, 330), 6, fill=(255, 122, 69))
        d.line([(30, 331), (530, 331)], fill=(60, 70, 85), width=2)
    else:
        d.arc((60, 90, 260, 290), -90, 270, fill=(40, 46, 60), width=16)
        d.arc((60, 90, 260, 290), -90, 230, fill=(52, 245, 176), width=16)
        d.text((160, 180), "A", font=font("Unbounded.ttf", 76, 900), fill=(52, 245, 176), anchor="mm")
        d.text((160, 240), "87 / 100", font=mono, fill=(141, 153, 168), anchor="mm")
        for i, (t, ok) in enumerate([("HTTPS", 1), ("SSL", 1), ("HSTS", 1), ("DMARC", 0), ("Mobile", 1)]):
            y = 80 + i * 48
            d.rounded_rectangle((300, y, 520, y + 36), 10, fill=(20, 26, 36), outline=(40, 48, 60))
            d.text((320, y + 18), ("✓ " if ok else "! ") + t, font=mono, fill=(52, 245, 176) if ok else (255, 201, 77), anchor="lm")
    return art


def wrap_text(text, fnt, maxw, draw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def brand(d):
    d.ellipse((60, 52, 84, 76), outline=(52, 245, 176), width=4)
    d.ellipse((67, 59, 77, 69), fill=(255, 79, 216))
    d.text((96, 64), "ayfar.az", font=font("Unbounded.ttf", 24, 900), fill=(238, 243, 248), anchor="lm")


def home():
    im = backdrop("#34f5b0", "#ff4fd8").convert("RGBA")
    shots = ["mexaniki-1.webp", "bathshop-1.webp", "provguard-1.webp"]
    for i, s in enumerate(shots):
        win = window(os.path.join(ROOT, "img", s), 430)
        paste_shadow(im, win, (650 + i * 70, 70 + i * 120), angle=-6 + i * 3)
    d = ImageDraw.Draw(im)
    brand(d)
    gradient_text(im, (54, 150), "ayfar", font("Unbounded.ttf", 170, 900), "#ffffff", "#34f5b0")
    d.text((62, 400), "Saytlar · Oyunlar · Layihələr", font=font("SpaceGrotesk.ttf", 40, 700), fill=(238, 243, 248))
    d.text((62, 456), "Ziya Əzizovun bütün işləri bir yerdə", font=font("SpaceGrotesk.ttf", 28, 500), fill=(141, 153, 168))
    d.text((62, 548), f"{len(P)} CANLI LAYİHƏ · BAKI", font=font("JetBrainsMono.ttf", 20, 700), fill=(52, 245, 176))
    im.convert("RGB").save(os.path.join(OUT, "home.png"), optimize=True)


def project(p):
    im = backdrop(p["c1"], p["c2"]).convert("RGBA")
    kind, val = p["media"]
    if kind == "reel":
        obj = window(os.path.join(ROOT, "img", f"{IMG_SLUG[p['slug']]}-1.webp"), 560)
    else:
        obj = rounded(scene_art(val, p["c1"]).convert("RGBA"), 18)
    paste_shadow(im, obj, (600, 120), angle=-4)
    d = ImageDraw.Draw(im)
    brand(d)
    tag = p["tag"][0].upper()
    tf = font("JetBrainsMono.ttf", 18, 700)
    tw = d.textlength(tag, font=tf)
    d.rounded_rectangle((60, 130, 60 + tw + 32, 168), 19, outline=hexrgb(p["c1"]), width=2)
    d.text((76, 149), tag, font=tf, fill=hexrgb(p["c1"]), anchor="lm")
    name = p["name"][0]
    size = 72 if len(name) <= 14 else 54 if len(name) <= 22 else 44
    tf2 = font("Unbounded.ttf", size, 900)
    lines = wrap_text(name, tf2, 520, d)
    y = 196
    for ln in lines[:3]:
        gradient_text(im, (58, y), ln, tf2, "#ffffff", p["c1"])
        y += int(size * 1.12)
    d = ImageDraw.Draw(im)
    sf = font("SpaceGrotesk.ttf", 24, 500)
    first = p["summary"][0].split(". ")[0].split(": ")[0].rstrip(".") + "."
    for ln in wrap_text(first, sf, 500, d)[:3]:
        y += 0
        d.text((62, y + 14), ln, font=sf, fill=(196, 204, 214))
        y += 34
    d.text((62, 560), p["metric"][0], font=font("Unbounded.ttf", 30, 900), fill=hexrgb(p["c2"]))
    im.convert("RGB").save(os.path.join(OUT, f"{p['slug']}.png"), optimize=True)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    home()
    for p in P:
        project(p)
    print("og images:", len(P) + 1)
