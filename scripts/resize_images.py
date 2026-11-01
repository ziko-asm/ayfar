"""Makes the 640 px wide previews (img/<name>-<n>-m.webp) from the 1920 px screenshots.
Phones show a gallery image about 360 CSS px wide (~630 device px), so they get this size
instead of the 960 px one. Needs Pillow.

Run:  python scripts/resize_images.py      (only writes files that are missing or older than their source)
"""
import glob
import os
import re

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIDTH, QUALITY = 640, 78

made = 0
for src in sorted(glob.glob(os.path.join(ROOT, "img", "*.webp"))):
    if not re.search(r"-\d+\.webp$", src):  # only the full-size screenshots, e.g. provguard-1.webp
        continue
    dst = src[:-5] + "-m.webp"
    if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
        continue
    with Image.open(src) as im:
        h = round(im.height * WIDTH / im.width)
        im.convert("RGB").resize((WIDTH, h), Image.LANCZOS).save(dst, "WEBP", quality=QUALITY, method=6)
    made += 1
print(f"{made} preview(s) written")
