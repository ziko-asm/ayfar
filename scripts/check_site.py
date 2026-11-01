"""Static checks on the built site (no browser needed). Exits non-zero on any problem.

- every internal link, image, srcset entry and hreflang target points to a file that exists
- every page has <html lang>, a <title>, a description, and (except 404) a canonical URL
- hreflang alternates are complete (az, en, ru, x-default) and reciprocal
- every JSON-LD block is valid JSON
- every sitemap URL exists
- the CSP in vercel.json allows exactly the inline scripts the pages contain

Run:  python scripts/check_site.py
"""
import base64
import glob
import hashlib
import json
import os
import re
import sys
from urllib.parse import urljoin, urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://ayfar.vercel.app"
LANGS = {"az", "en", "ru", "x-default"}
errors = []


def err(page, msg):
    errors.append(f"{page}: {msg}")


def target_exists(path):
    full = os.path.join(ROOT, path.lstrip("/"))
    if path.endswith("/"):
        full = os.path.join(full, "index.html")
    return os.path.isfile(full)


def url_path(page):
    """URL path a page is served at: /index.html -> /, /en/index.html -> /en/."""
    return page[: -len("index.html")] if page.endswith("index.html") else page


pages = sorted("/" + os.path.relpath(f, ROOT).replace(os.sep, "/")
               for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)
               if not os.path.relpath(f, ROOT).startswith(("content", "node_modules", "tests")))
alternates = {}
inline_hashes = set()
links = 0

for page in pages:
    with open(os.path.join(ROOT, page.lstrip("/")), encoding="utf-8") as f:
        html = f.read()
    base = "http://local" + url_path(page)

    # links and images
    for attr, val in re.findall(r'\s(href|src|srcset|data-zoom)="([^"]*)"', html):
        for v in ([x.strip().split(" ")[0] for x in val.split(",")] if attr == "srcset" else [val]):
            if v.startswith(SITE):
                v = v[len(SITE):] or "/"
            if not v or v.startswith(("#", "mailto:", "tel:", "data:")):
                continue
            u = urlparse(urljoin(base, v))
            if u.netloc != "local":
                continue
            links += 1
            if not target_exists(u.path):
                err(page, f"broken link {v}")

    # head basics
    m = re.search(r'<html lang="([a-z]{2})"', html)
    if not m:
        err(page, "missing <html lang>")
    if not re.search(r"<title>[^<]+</title>", html):
        err(page, "missing <title>")
    if not re.search(r'<meta name="description" content="[^"]+">', html):
        err(page, "missing meta description")
    if page != "/404.html" and not re.search(r'<link rel="canonical" href="https://[^"]+">', html):
        err(page, "missing canonical")
    if html.count("<h1") != 1:
        err(page, f"expected one <h1>, found {html.count('<h1')}")

    # hreflang
    alts = dict(re.findall(r'<link rel="alternate" hreflang="([a-z-]+)" href="([^"]+)">', html))
    if alts:
        if set(alts) != LANGS:
            err(page, f"hreflang set is {sorted(alts)}, expected {sorted(LANGS)}")
        alternates[SITE + url_path(page)] = alts

    # JSON-LD
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            json.loads(block)
        except ValueError as e:
            err(page, f"invalid JSON-LD: {e}")

    # inline scripts that the CSP has to allow
    for body in re.findall(r"<script>(.*?)</script>", html, re.S):
        inline_hashes.add("'sha256-" + base64.b64encode(hashlib.sha256(body.encode()).digest()).decode() + "'")

# hreflang must be reciprocal: every alternate lists the same set back
for url, alts in alternates.items():
    for lang, href in alts.items():
        if href not in alternates:
            err(url, f"hreflang {lang} -> {href} is not a page with alternates")
        elif alternates[href] != alts:
            err(url, f"hreflang set differs on {href}")

# sitemap
with open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8") as f:
    locs = re.findall(r"<loc>([^<]+)</loc>", f.read())
for loc in locs:
    if loc.startswith(SITE) and not loc.endswith((".jpg", ".png", ".webp")) and not target_exists(loc[len(SITE):] or "/"):
        err("sitemap.xml", f"{loc} does not exist")

# CSP
with open(os.path.join(ROOT, "vercel.json"), encoding="utf-8") as f:
    cfg = json.load(f)
csp = next(h["value"] for r in cfg["headers"] for h in r["headers"] if h["key"] == "Content-Security-Policy")
script_src = re.search(r"script-src ([^;]+)", csp).group(1).split()
allowed = {s for s in script_src if s.startswith("'sha256-")}
if allowed != inline_hashes:
    err("vercel.json", f"CSP script hashes {sorted(allowed)} do not match inline scripts {sorted(inline_hashes)}")
if "'unsafe-inline'" in script_src:
    err("vercel.json", "script-src must not allow 'unsafe-inline'")

print(f"{len(pages)} pages, {links} internal links, {len(locs)} sitemap URLs checked")
if errors:
    print(f"{len(errors)} problem(s):")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print("all good")
