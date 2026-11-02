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
style_hashes = set()
links = 0

for page in pages:
    with open(os.path.join(ROOT, page.lstrip("/")), encoding="utf-8") as f:
        html = f.read()
    base = "http://local" + url_path(page)

    # links and images
    for attr, val in re.findall(r'\s(href|src|srcset|data-src|data-srcset|data-zoom)="([^"]*)"', html):
        for v in ([x.strip().split(" ")[0] for x in val.split(",")] if attr.endswith("srcset") else [val]):
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

    # inline scripts and <style> blocks that the CSP has to allow by hash
    for body in re.findall(r"<script>(.*?)</script>", html, re.S):
        inline_hashes.add("'sha256-" + base64.b64encode(hashlib.sha256(body.encode()).digest()).decode() + "'")
    for body in re.findall(r"<style>(.*?)</style>", html, re.S):
        style_hashes.add("'sha256-" + base64.b64encode(hashlib.sha256(body.encode()).digest()).decode() + "'")
    # style="" attributes would need 'unsafe-inline' (colours are classes: .pc-<slug>)
    for m in re.finditer(r'\sstyle="', html):
        err(page, "style attribute (use a class; the CSP allows no inline style attributes)")
        break

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
style_src = re.search(r"style-src ([^;]+)", csp).group(1).split()
if {s for s in style_src if s.startswith("'sha256-")} != style_hashes:
    err("vercel.json", "CSP style hashes do not match the <style> blocks: run python build.py")
if "'unsafe-inline'" in style_src:
    err("vercel.json", "style-src must not allow 'unsafe-inline'")
headers = {h["key"]: h["value"] for r in cfg["headers"] for h in r["headers"] if r["source"] == "/(.*)"}
for key, want in (("Cross-Origin-Opener-Policy", "same-origin"), ("Cross-Origin-Embedder-Policy", "require-corp"),
                  ("Cross-Origin-Resource-Policy", "same-origin")):
    if headers.get(key) != want:
        err("vercel.json", f"{key} should be {want}")
if headers.get("Access-Control-Allow-Origin", "*") == "*":
    err("vercel.json", "Access-Control-Allow-Origin must not be *")

# served JavaScript is the minified build of assets/src (no comments shipped)
for src in glob.glob(os.path.join(ROOT, "assets", "src", "*.js")):
    out = os.path.join(ROOT, "assets", os.path.basename(src))
    with open(out, encoding="utf-8") as f:
        if "/*" in f.read():
            err("assets/" + os.path.basename(src), "contains comments: run python build.py")

# fonts: the -ext font files are cut down to the characters the site uses (scripts/subset_fonts.py);
# a new letter that is missing from them would fall back to a system font
with open(os.path.join(ROOT, "fonts", "src", "fonts.css"), encoding="utf-8") as f:
    src_css = f.read()
with open(os.path.join(ROOT, "fonts", "subset.json"), encoding="utf-8") as f:
    subsets = json.load(f)
used = set()
for f in [os.path.join(ROOT, p.lstrip("/")) for p in pages] + glob.glob(os.path.join(ROOT, "assets", "*.js")):
    with open(f, encoding="utf-8") as fh:
        used |= set(fh.read())
for name, info in subsets.items():
    block = next(b for b in re.findall(r"@font-face \{.*?\}", src_css, re.S) if f"/fonts/{name}" in b)
    rng = set()
    for part in re.search(r"unicode-range: ([^;]+);", block).group(1).split(","):
        a, _, b = part.strip()[2:].partition("-")
        rng |= {chr(c) for c in range(int(a, 16), int(b or a, 16) + 1)}
    missing = (used & rng) - set(info["chars"]) - set(info["unsupported"])
    if missing:
        err(f"fonts/{name}", f"pages use {''.join(sorted(missing))!r}, not in the subset: run python scripts/subset_fonts.py")

print(f"{len(pages)} pages, {links} internal links, {len(locs)} sitemap URLs checked")
if errors:
    print(f"{len(errors)} problem(s):")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print("all good")
