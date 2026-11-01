# ayfar

Portfolio and web studio of **Ziya Azizov (ayfar)**, an engineer from Baku, Azerbaijan, working in programming, cybersecurity and AI.

**Live site: https://ayfar.vercel.app**

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

It also writes `sitemap.xml` (with language alternates), `robots.txt`, `llms.txt`, `404.html` and `vercel.json` (security headers and a CSP that allows the one inline script by its hash). Russian text lives in `ru.py`; the build stops and lists the gaps in `ru_missing.txt` if a string has no translation.

```bash
python build.py
```

Every push to `main` deploys to Vercel.

## Contact

WhatsApp +994 77 217 23 58 · [LinkedIn](https://www.linkedin.com/in/ziya-azizov-91bba638a) · [Instagram](https://www.instagram.com/ayfar.web/)
