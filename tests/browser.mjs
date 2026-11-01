// Browser checks on the built site, served with the real Vercel headers (CSP included).
// Run:  cd tests && npm ci && node browser.mjs        (starts scripts/serve.py itself)
import { spawn } from "node:child_process";
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import { chromium } from "playwright";

const require = createRequire(import.meta.url);
const AXE = readFileSync(require.resolve("axe-core/axe.min.js"), "utf8");
const PORT = 8790;
const BASE = `http://127.0.0.1:${PORT}`;
const PAGES = ["/", "/p/metro-tycoon.html", "/p/provguard.html", "/p/saytyoxla.html", "/yazilar/provguard.html"];
const LANGS = { az: "", en: "/en", ru: "/ru" };
const VIEWPORTS = { desktop: { width: 1440, height: 900 }, phone: { width: 360, height: 740 } };

const failures = [];
let passed = 0;
function check(ok, name, detail = "") {
  if (ok) passed++;
  else failures.push(`${name}${detail ? ": " + detail : ""}`);
}

const server = spawn("python3", ["../scripts/serve.py", String(PORT)], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
for (let i = 0; i < 50; i++) {
  try { if ((await fetch(BASE + "/")).ok) break; } catch {}
  await sleep(100);
}

const browser = await chromium.launch();
try {
  // 1. every page in every language and viewport: no errors or CSP violations, right language, no sideways scroll
  for (const [vpName, viewport] of Object.entries(VIEWPORTS)) {
    const ctx = await browser.newContext({ viewport, reducedMotion: "reduce" });
    for (const [lang, prefix] of Object.entries(LANGS)) {
      for (const path of PAGES) {
        const url = prefix + path, name = `${vpName} ${url}`;
        const page = await ctx.newPage();
        const errors = [];
        page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
        page.on("pageerror", (e) => errors.push(e.message));
        const res = await page.goto(BASE + url, { waitUntil: "load" });
        await page.waitForTimeout(400);
        check(res.status() === 200, name, `status ${res.status()}`);
        check(errors.length === 0, name + " console", errors.join(" | "));
        const info = await page.evaluate(() => ({
          lang: document.documentElement.lang,
          overflow: document.documentElement.scrollWidth - innerWidth,
          current: document.querySelector('.lang a[aria-current="page"]')?.getAttribute("hreflang"),
          article: document.querySelector(".art-body")?.offsetHeight ?? null,
        }));
        check(info.lang === lang, name + " <html lang>", info.lang);
        check(info.current === lang, name + " language switch", String(info.current));
        check(info.overflow <= 0, name + " horizontal scroll", `${info.overflow}px`);
        if (info.article !== null) check(info.article > 1000, name + " article text visible", `${info.article}px`);

        // accessibility (WCAG 2.2 AA rules from axe-core), with animations settled; CSP is bypassed only to inject axe
        if (path === "/" || path.startsWith("/yazilar")) {
          const ap = await browser.newPage({ viewport, reducedMotion: "reduce", bypassCSP: true });
          await ap.goto(BASE + url, { waitUntil: "load" });
          await ap.evaluate(() => document.querySelectorAll(".reveal,.slide").forEach((e) => e.classList.add("in", "seen")));
          await ap.addStyleTag({ content: "*,*::before,*::after{transition:none!important;animation:none!important}" });
          await ap.addScriptTag({ content: AXE });
          const violations = await ap.evaluate(async () =>
            (await axe.run(document, { runOnly: ["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"] })).violations
              .map((v) => `${v.id} (${v.nodes.length}): ${v.nodes[0].target.join(" ")}`));
          check(violations.length === 0, name + " axe", violations.join("; "));
          await ap.close();
        }
        await page.close();
      }
    }
    await ctx.close();
  }

  const page = await browser.newPage({ viewport: VIEWPORTS.desktop });

  // 2. the language switch opens the same page in the other language
  await page.goto(BASE + "/p/provguard.html");
  await page.click('.lang a[hreflang="ru"]');
  await page.waitForURL("**/ru/p/provguard.html", { timeout: 5000 }).catch(() => {});
  check(page.url().endsWith("/ru/p/provguard.html"), "language switch keeps the page", page.url());

  // 3. the mini game can be played from the keyboard
  await page.goto(BASE + "/");
  await page.waitForTimeout(500);
  await page.focus("#gStart");
  await page.keyboard.down("Space");
  await page.waitForTimeout(1000);
  const speed = +(await page.textContent("#gSpd"));
  await page.keyboard.up("Space");
  check(speed > 0, "game: Space on the start button drives the train", `speed ${speed}`);
  check(await page.evaluate(() => document.activeElement.id) === "game", "game: focus moves to the canvas");

  // 4. the site check shows readable errors whatever shape the API error has
  for (const [body, want] of [[{ detail: [{ msg: "Field required" }] }, "Field required"], [{ detail: "Custom" }, "Custom"], [{}, "Yoxlamaq alınmadı"]]) {
    await page.unroute("**/api/scan").catch(() => {});
    await page.route("**/api/scan", (r) => r.fulfill({ status: 422, contentType: "application/json", body: JSON.stringify(body) }));
    await page.fill("#scanUrl", "example.az");
    await page.click("#scanForm button");
    await page.waitForTimeout(300);
    const text = await page.textContent("#scanOut");
    check(text.includes(want) && !text.includes("[object"), "site check error message", text);
  }

  // 5. unknown pages return 404 with the 404 page
  const res = await page.goto(BASE + "/en/does-not-exist");
  check(res.status() === 404 && (await page.title()).includes("tapılmadı"), "404 page", String(res.status()));
} finally {
  await browser.close();
  server.kill();
}

console.log(`${passed} checks passed`);
if (failures.length) {
  console.log(`${failures.length} failed:`);
  for (const f of failures) console.log("  - " + f);
  process.exit(1);
}
