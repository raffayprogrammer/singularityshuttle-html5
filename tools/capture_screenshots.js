/**
 * Capture full-page screenshots of every Singularity Shuttle page
 * for the parity / handover deliverable.
 *
 * Output: tests/screenshots/<page_id>.png  (full-page, 684px viewport width)
 *
 * Usage:
 *   node tools/capture_screenshots.js
 */
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

const BASE = "https://singularityshuttle-html5.vercel.app";
const OUT_DIR = path.join(__dirname, "..", "tests", "screenshots");

// All 31 pages + landing + native comparison
const targets = [
  { id: "_landing", url: BASE + "/" },
  { id: "_native-SS2-1", url: BASE + "/pages/SS2-1-native.html" },
];

// Read inventory.csv for the 31 page IDs
const inventory = fs.readFileSync(
  path.join(__dirname, "..", "docs", "inventory.csv"),
  "utf8"
);
inventory.split("\n").slice(1).forEach((line) => {
  const cols = line.split(",");
  if (cols[0]) {
    targets.push({ id: cols[0], url: `${BASE}/pages/${cols[0]}.html` });
  }
});

(async () => {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 720, height: 900 },
    deviceScaleFactor: 1,
  });

  let pass = 0;
  let fail = 0;
  const results = [];

  for (const t of targets) {
    const page = await context.newPage();
    try {
      await page.goto(t.url, { waitUntil: "networkidle", timeout: 30000 });
      // Wait for Ruffle to initialize
      await page.waitForTimeout(3500);
      // Try to programmatically dismiss Ruffle's autoplay gate by calling
      // play() on the player element (it lives inside #player as a child).
      try {
        await page.evaluate(async () => {
          const container = document.getElementById("player");
          if (!container) return;
          // Ruffle creates a <ruffle-player> or similar element inside the container
          for (const el of container.querySelectorAll("*")) {
            if (typeof el.play === "function") {
              try { await el.play(); } catch (e) { /* ok */ }
            }
          }
        });
        await page.waitForTimeout(3000); // let animation begin
      } catch (clickErr) { /* fallthrough */ }

      const out = path.join(OUT_DIR, `${t.id}.png`);
      await page.screenshot({ path: out, fullPage: true });
      console.log(`OK  ${t.id}  -> ${out}`);
      pass++;
      results.push({ id: t.id, url: t.url, status: "ok", file: out });
    } catch (e) {
      console.error(`FAIL ${t.id}: ${e.message}`);
      fail++;
      results.push({ id: t.id, url: t.url, status: "fail", error: e.message });
    } finally {
      await page.close();
    }
  }

  await browser.close();

  const summary = `# Screenshot capture summary\n\n` +
    `Run at: ${new Date().toISOString()}\n` +
    `Total: ${targets.length}\n` +
    `Passed: ${pass}\n` +
    `Failed: ${fail}\n\n` +
    `## Per-page\n\n` +
    `| Page | Status | File |\n|---|---|---|\n` +
    results.map(r =>
      `| ${r.id} | ${r.status} | ${r.status === "ok" ? path.relative(path.join(__dirname, ".."), r.file) : (r.error || "")} |`
    ).join("\n") + "\n";

  fs.writeFileSync(path.join(OUT_DIR, "..", "SCREENSHOTS_SUMMARY.md"), summary);
  console.log(`\nDone: ${pass} passed, ${fail} failed`);
  console.log(`Summary: tests/SCREENSHOTS_SUMMARY.md`);
})();
