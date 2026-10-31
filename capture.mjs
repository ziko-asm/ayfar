// Captures sharp preview frames of each site through headless Chrome (DevTools protocol).
// Usage: node capture.mjs <chrome-debug-port>
import { writeFileSync, mkdirSync } from "node:fs";

const PORT = process.argv[2] || "9333";
const W = 1280, H = 800, DPR = 1.5;
const SITES = [
  ["provguard", "https://provguard.vercel.app", 3000, [0, 760, 1520, 2280]],
  ["detector", "https://prompt-injection-detector-snowy.vercel.app/", 3000, [0, 760, 1520]],
  ["graphguard", "https://graphguard-iot.vercel.app/", 4000, [0, 700, 1500]],
  ["agentaudit", "https://agent-audit-ten.vercel.app/", 2500, [0, 760, 1520]],
  ["bathshop", "https://bathshop-az-selling-site.vercel.app/", 4000, [0, 520, 1300]],
  ["mexaniki", "https://mexaniki-emal.vercel.app/", 9000, [0, 800, 1700]],
];
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const target = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: "PUT" })).json();
const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener("open", r, { once: true }));
let id = 0;
const pending = new Map();
ws.addEventListener("message", (e) => {
  const m = JSON.parse(e.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
});
const send = (method, params = {}) => new Promise((res, rej) => {
  const i = ++id;
  pending.set(i, (m) => (m.error ? rej(new Error(method + ": " + m.error.message)) : res(m.result)));
  ws.send(JSON.stringify({ id: i, method, params }));
});

await send("Page.enable");
await send("Emulation.setDeviceMetricsOverride", { width: W, height: H, deviceScaleFactor: DPR, mobile: false });
mkdirSync("img/raw", { recursive: true });
for (const [name, url, wait, ys] of SITES) {
  await send("Page.navigate", { url });
  await sleep(wait);
  for (let i = 0; i < ys.length; i++) {
    await send("Runtime.evaluate", { expression: `scrollTo(0, ${ys[i]})` });
    await sleep(1800);
    const { data } = await send("Page.captureScreenshot", { format: "png", captureBeyondViewport: false });
    writeFileSync(`img/raw/${name}-${i + 1}.png`, Buffer.from(data, "base64"));
    console.log("saved", name, i + 1);
  }
}
ws.close();
