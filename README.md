# ayfar

Portfolio and web studio of **Ziya Azizov (ayfar)**, an engineer from Baku, Azerbaijan, working in programming, cybersecurity and AI.

**Live site: https://ayfar.dev**

Business websites and online shops, the Metro Tycoon game, and AI security research, in one place, in Azerbaijani, English and Russian. The Services section includes a free website check powered by [SaytYoxla](https://saytyoxla.vercel.app).

## Projects on the site

| Project | What it is |
|---|---|
| [Metro Tycoon](https://siloveu.itch.io/metro-tycoon) | Train-driving tycoon game on the Baku metro |
| [ProvGuard](https://github.com/ziko-asm/provguard) | Python library that stops prompt injection in AI agents by tracking where each tool argument came from |
| [Prompt Injection Detector Benchmark](https://github.com/ziko-asm/prompt-injection-detector) | How detectors fail on data from a different source |
| [GraphGuard IoT](https://github.com/ziko-asm/gnn-nids-robustt) | Adversarial robustness of GNN intrusion detection |
| [AI-NIDS Robustness Lab](https://github.com/ziko-asm/ai-nids-adversarial-benchmark) | Adversarial attacks on neural network intrusion detectors |
| [SaytYoxla](https://github.com/ziko-asm/saytyoxla) | Free website security check for businesses in Azerbaijan |
| bathshop.az, MANSIA, lathe workshop | Business websites and online shops in Baku |

## Build

The site is static. `build.py` generates every page in three languages, each at its own URL with `hreflang` links between them:

| Language | Home | Project pages | Articles |
|---|---|---|---|
| Azerbaijani (default) | `/` | `/p/<slug>.html` | `/yazilar/<slug>.html` |
| English | `/en/` | `/en/p/<slug>.html` | `/en/yazilar/<slug>.html` |
| Russian | `/ru/` | `/ru/p/<slug>.html` | `/ru/yazilar/<slug>.html` |

JavaScript is written in `assets/src/` and minified into `assets/` by the build (`pip install rjsmin==1.2.4`), so comments never reach the browser. It also writes `sitemap.xml` (with language alternates), `robots.txt`, `llms.txt`, `404.html` and `vercel.json` (security headers; the CSP allows the inline script and the inline `<style>` blocks by their hashes, so neither needs `'unsafe-inline'`; cross-origin isolation with COOP/COEP/CORP). Russian text lives in `ru.py`; the build stops and lists the gaps in `ru_missing.txt` if a string has no translation.

```bash
python build.py
```

Every push to `main` deploys to Vercel.

## Checks

Every push to `main` and every pull request runs [CI](.github/workflows/ci.yml):

1. **Build**: `python build.py` must succeed (it stops if a Russian translation is missing), and its output must match the committed pages.
2. **Static checks** (`python scripts/check_site.py`): every internal link, image and `hreflang` target exists, hreflang sets are complete and reciprocal, JSON-LD is valid, sitemap URLs exist, and the CSP hashes in `vercel.json` match the inline scripts.
3. **Browser tests** (`cd tests && npm ci && npm test`): every page in all three languages on desktop and phone, served with the real Vercel headers. No console errors or CSP violations, correct language, no sideways scroll, no WCAG 2.2 AA violations (axe-core), keyboard play of the mini game, readable site-check errors, and the 404 page.

To look at the site locally with production headers: `python scripts/serve.py` and open http://127.0.0.1:8765/.

## Fonts and images

Unbounded, Space Grotesk and JetBrains Mono are served from `/fonts` (SIL Open Font License, see [fonts/LICENSE.md](fonts/LICENSE.md)), so no request goes to a third party and the CSP stays `'self'` only.

The font files are cut down to the characters the site uses (the Azerbaijani letters took a 115 KB file; they now take 3 KB). The originals live in `fonts/src/`. After adding text with new letters:

```bash
python build.py && python scripts/subset_fonts.py && python build.py   # needs: pip install fonttools brotli
```

CI fails with a clear message if a page uses a letter that is missing from the subsets.

Gallery screenshots come in three widths: 720 px for phones (`python scripts/resize_images.py`, needs Pillow), 960 px and 1920 px. Page images carry `?v=` and are cached for a year, so bump `V` in `build.py` when replacing one.

## Contact

WhatsApp +994 77 217 23 58 · [LinkedIn](https://www.linkedin.com/in/ziya-azizov-91bba638a) · [Instagram](https://www.instagram.com/ayfar.web/)
