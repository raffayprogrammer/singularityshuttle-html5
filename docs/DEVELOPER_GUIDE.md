# Singularity Shuttle — Developer Guide

> The handover document. Everything a developer needs to maintain, extend, or rebuild this site.

**Live URL:** https://singularityshuttle-html5.vercel.app
**Repo:** https://github.com/raffayprogrammer/singularityshuttle-html5

---

## 1. What this project is

A modern HTML5 restoration of the **31-page Singularity Shuttle** interactive Flash experience originally published in 2004. The original `.fla` and `.swf` source files were preserved by the client; this project wraps them in modern HTML pages so they can be viewed in any contemporary browser without the discontinued Adobe Flash Player.

**Total assets:** 31 pages = 15 main + 15 text-only counterparts + 1 jump/contents hub.

---

## 2. Architecture decision — why Ruffle.js instead of Adobe Animate

The original brief (`02-Developer-Implementation-Guide.md`) assumed an Adobe Animate workflow — opening each `.fla` in Animate, converting to HTML5 Canvas, manually porting ActionScript to JavaScript, and re-publishing via CreateJS. That's a viable path but expensive: ~$23/month for Animate plus 3-4 weeks of conversion labor.

We chose a different path:

### Path A — Ruffle.js runtime (what's deployed)

[Ruffle](https://ruffle.rs) is an open-source Flash Player emulator written in Rust, compiled to WebAssembly. It runs in any modern browser, plays `.swf` files natively, and requires no plugins.

**The pipeline:**
1. Each `.swf` file is served as a static asset.
2. A thin HTML wrapper embeds Ruffle.js from CDN and loads the SWF.
3. JavaScript intercepts navigation calls (the SWFs hardcode `http://www.singularityshuttle.com/SS2-X.html` URLs) and rewrites them to point at our local pages.

**Trade-offs vs Adobe Animate path:**

| Dimension | Ruffle.js (Path A) | Adobe Animate (Path D) |
|---|---|---|
| Software cost | $0 | ~$23/mo |
| Time to deliver | ~1 day | 3-4 weeks |
| Animation fidelity | 100% (original SWF unchanged) | ~95% (depends on Animate's exporter) |
| Audio fidelity | 100% (embedded in SWF) | Variable (re-encoded) |
| Mobile performance | Good (WebAssembly) | Better (native canvas) |
| "Pure HTML5"? | Debate-able (WASM Flash interpreter) | Yes (native Canvas) |
| Future content edits | Need original FLA + Animate | Edit JS directly |

The end-user experience is functionally identical between the two paths.

### Path B — JPEXS extract + manual CreateJS rebuild (fallback)

If a specific page has Ruffle.js compatibility issues, that page can be rebuilt manually using [JPEXS FFDec](https://github.com/jindrapetrik/jpexs-decompiler) to extract assets and decompile ActionScript, then rebuilt by hand using CreateJS. This is currently **not used** for any page. Kept as a documented fallback.

---

## 3. Repository layout

```
singularityshuttle-html5/
├── index.html              — Landing page (hero + 31-card grid + SS2-J embed)
├── vercel.json             — SWF MIME type + cache headers
├── pages/                  — 31 SWFs + 31 HTML wrappers
│   ├── SS2-1.html
│   ├── SS2-1.swf
│   ├── SS2-1text.html
│   ├── SS2-1text.swf
│   ├── ...
│   └── SS2-J.swf
├── lib/                    — Path B fallback assets (CreateJS, scaler) — currently unused
│   ├── createjs.min.js
│   └── wrapper.js
├── docs/                   — Documentation + project metadata
│   ├── DEVELOPER_GUIDE.md  — (this file)
│   ├── MODULE1_DONE.md     — Setup phase validation
│   ├── inventory.csv       — All 31 pages with stage dimensions, type
│   ├── page-metadata.json  — Page titles + section labels
│   ├── audio-map.csv       — Audio asset → page mapping (Path B prep)
│   ├── audio-files-index.txt — Index of all 181 audio files
│   └── wrapper-template.html — Path B template (CreateJS, unused)
├── tools/                  — Build/automation scripts
│   ├── generate_pages.py   — Regenerates all 31 page wrappers
│   ├── parse_swf.py        — Rebuilds inventory.csv from SWF binaries
│   └── build_audio_map.py  — Rebuilds audio-map skeleton
├── source/                 — Original assets (NOT committed — too large)
│   ├── fla/                — Adobe Flash source files (CFB binary)
│   ├── swf/                — Compiled Flash output
│   ├── html-original/      — Original 2004 HTML wrappers (reference only)
│   └── audio/              — All MP3/WAV/SFK audio
├── tests/                  — Per-page parity screenshots (populated during QA)
├── README.md
└── .gitignore              — Excludes source/* binaries and tools/ruffle
```

### Files NOT in git (gitignored, kept locally)

- `source/fla/` — pre-CS5 binary FLA files (~126 MB)
- `source/swf/` — compiled SWFs (the deployed copies are in `pages/`)
- `source/audio/wav/` — uncompressed WAV (~600 MB)
- `source/audio/sfk-archive/` — Sound Forge cache files (ignore)
- `tools/ruffle/` — desktop Ruffle binary for local SWF testing

If you clone the repo fresh, these directories will be empty. To populate them, either request the original `SS Files.zip` and `SS Audio.zip` from the project owner, or rely on the SWFs that are already in `pages/`.

---

## 4. Local setup

### Prerequisites
- **Git** (any version)
- **Python 3.8+** (for the build/regen scripts)
- **Node.js** (only if you want to run a local static server; not strictly required)

### Steps

```bash
git clone https://github.com/raffayprogrammer/singularityshuttle-html5.git
cd singularityshuttle-html5
```

That's it. The site is fully static — no `npm install`, no build step.

### Test locally

Open `index.html` directly in a browser, OR run a static server for proper relative URL handling:

```bash
python -m http.server 8000
# Visit http://localhost:8000
```

(Direct `file://` opens may have CORS issues with Ruffle.js. The static server is safer.)

---

## 5. How it works in detail

### 5.1 The page wrapper

Every `pages/SS2-X.html` is generated from a template (`tools/generate_pages.py`) and looks like this in essence:

```html
<head> ...title, viewport, dark-themed CSS... </head>
<body>

  <!-- 1. URL-rewriting script (runs first) -->
  <script>
    // Override window.open, location.assign, location.replace,
    // and Location.prototype.href setter — to remap any
    // http://www.singularityshuttle.com/* URL the SWF tries to
    // navigate to into our local /pages/* paths.
  </script>

  <!-- 2. Page header with breadcrumb, title, section -->
  <header> ... </header>

  <!-- 3. The Ruffle player container -->
  <div id="player"></div>

  <!-- 4. Bottom nav bar with prev/next/home/contents -->
  <nav class="bottombar"> ... </nav>

  <!-- 5. Load Ruffle.js from CDN, attach to #player, load the SWF -->
  <script src="https://unpkg.com/@ruffle-rs/ruffle"></script>
  <script>
    var player = window.RufflePlayer.newest().createPlayer();
    document.getElementById("player").appendChild(player);
    player.load({ url: "SS2-X.swf", autoplay: "auto", scale: "showAll" });
  </script>

</body>
```

### 5.2 URL rewriting (the trickiest part)

The original SWFs were authored when the site lived at `singularityshuttle.com`. Buttons inside the SWF call `getURL("http://www.singularityshuttle.com/SS2-2.html")` to navigate. On our deployment, those URLs are dead.

Ruffle, when it processes a `getURL()` call, can navigate via three different JavaScript pathways depending on the AS target:

1. `getURL("...", "_blank")` → `window.open(url, "_blank")`
2. `getURL("...", "_self")` (default) → `window.location.href = url`
3. Programmatic redirects → `location.assign(url)` or `location.replace(url)`

The page wrapper installs three independent overrides covering all three paths:

```js
// 1. window.open
var origOpen = window.open.bind(window);
window.open = function (url, name, features) {
  return origOpen(remap(url), name, features);
};

// 2. location.assign / replace
window.location.assign = function (u) { return origAssign(remap(u)); };
window.location.replace = function (u) { return origReplace(remap(u)); };

// 3. Location.prototype.href setter (the key one for _self nav)
Object.defineProperty(Location.prototype, "href", {
  set: function (v) { return origSet.call(this, remap(v)); }
});

function remap(u) {
  // http://www.singularityshuttle.com/SS2-2.html  →  /pages/SS2-2.html
  // http://www.singularityshuttle.com/index.html  →  /
  // mailto:..., other domains                     →  unchanged
}
```

This is duplicated in every page wrapper so the override happens before Ruffle initializes.

### 5.3 The landing page

`index.html` is a hand-built modern landing with:
- Hero section (badge, title, primary CTA, stats row)
- Visible card grid linking to all 31 pages (regular `<a>` tags — bulletproof)
- Embedded SS2-J SWF below as the "Original 2004 Navigation Hub"

The card grid is the primary navigation; SS2-J is supplementary. Even if Ruffle's URL-rewrite path fails for any reason, users can always navigate via the cards.

### 5.4 Vercel configuration

`vercel.json` sets:
- `Content-Type: application/x-shockwave-flash` for `.swf` files (some hosts default to `application/octet-stream`, which Ruffle handles but isn't ideal)
- `Cache-Control: public, max-age=86400` for SWFs (24h cache)
- `X-Frame-Options: SAMEORIGIN` for `/pages/*` (prevents embedding in 3rd-party iframes)

---

## 6. Common tasks

### 6.1 Update a single page wrapper

Don't edit `pages/SS2-X.html` directly — those are generated. Edit:

```bash
# 1. Update the template or metadata
edit tools/generate_pages.py     # if changing the template
edit docs/page-metadata.json     # if changing titles or sections

# 2. Regenerate all 31 pages
python tools/generate_pages.py

# 3. Commit and push
git add pages/ docs/page-metadata.json tools/generate_pages.py
git commit -m "Update page metadata"
git push   # auto-deploys to Vercel in ~30s
```

### 6.2 Replace a SWF (e.g. fix a corrupt page)

```bash
# 1. Drop the new SWF into pages/
cp /path/to/new/SS2-5.swf pages/SS2-5.swf

# 2. If dimensions changed, rebuild inventory + regenerate wrappers
python tools/parse_swf.py
python tools/generate_pages.py

# 3. Commit and push
git add pages/SS2-5.swf docs/inventory.csv pages/SS2-5.html
git commit -m "Replace SS2-5 with corrected version"
git push
```

### 6.3 Add a new page (if scope grows)

```bash
# 1. Drop SS2-X.swf into pages/
# 2. Add a row to docs/inventory.csv (or rerun parse_swf.py to detect it)
# 3. Add an entry to docs/page-metadata.json with title + section
# 4. Add the ID to the ORDER list in tools/generate_pages.py for prev/next
# 5. Add a card to index.html
# 6. Regenerate
python tools/generate_pages.py
```

### 6.4 Pin Ruffle.js to a specific version

Currently we load from `https://unpkg.com/@ruffle-rs/ruffle` (latest). To pin:

```html
<script src="https://unpkg.com/@ruffle-rs/ruffle@0.1.0-nightly.2024.10.15"></script>
```

Or self-host — download the npm package, copy `dist/` into `lib/ruffle/`, and reference locally. Self-hosting is more reliable for long-term archival but increases the repo size.

### 6.5 Deploy

Push to `main` on GitHub. Vercel auto-deploys within 30 seconds.

```bash
git push origin main
```

To trigger a manual redeploy without code changes, use the Vercel dashboard's "Redeploy" button.

---

## 7. Troubleshooting

### Page loads but the player area is just a black box

- **Cause:** Ruffle.js failed to load from CDN, or browser is blocking `<script>` from `unpkg.com`.
- **Check:** DevTools Console for CSP/CORS errors.
- **Fix:** Self-host Ruffle (see 6.4).

### Audio is silent

- **Cause:** Browser autoplay policy. Modern browsers block audio on first page load until a user gesture.
- **Fix:** Ruffle's `unmuteOverlay: "visible"` config (already set) shows a "Click to unmute" prompt. User just needs to click.

### Clicking a button inside the SWF goes to the dead `singularityshuttle.com` domain

- **Cause:** URL rewriting didn't fire. Check DevTools Console for errors.
- **Likely culprit:** Ruffle navigated via a path the rewriter doesn't cover (rare).
- **Workaround:** Users can always navigate via the bottom navbar (Prev/Home/Contents/Next) or the card grid on the landing page.

### A specific page renders incorrectly (e.g., missing animation, broken transition)

- **Cause:** Ruffle's AS2 implementation has a gap on that specific SWF feature.
- **Diagnosis:** Compare against the desktop Ruffle player (`tools/ruffle/ruffle.exe`) to confirm it's a Ruffle issue, not a Vercel/CDN issue.
- **Fix path A:** Wait for a future Ruffle release; pin once fixed.
- **Fix path B:** Rebuild that one page using JPEXS extraction + CreateJS (see `docs/wrapper-template.html` for the CreateJS template).

### Vercel build fails

This site has no build step — Vercel should always succeed. If it doesn't:
- Check `vercel.json` syntax (must be valid JSON).
- Check that `index.html` exists at repo root.

### Repo is too large

The `source/` folder is gitignored to keep the repo small. If `pages/*.swf` totals ever push past 100 MB:
- Move SWFs to GitHub LFS, or
- Move SWFs to a separate CDN (e.g., R2, S3) and update the `url:` in each wrapper.

---

## 8. Path B fallback procedure (per-page rebuild)

Use only if a specific page is unsolvable in Ruffle.js. Steps:

1. **Install JPEXS FFDec**: https://github.com/jindrapetrik/jpexs-decompiler/releases
2. **Open the problem SWF** in JPEXS:
   ```
   File → Open → source/swf/SS2-X.swf
   ```
3. **Export assets**:
   - `File → Export selection` → choose Images, Sounds, Shapes (SVG), Texts
   - `File → Export ActionScript` for the AS source code
4. **Rebuild in CreateJS** using `docs/wrapper-template.html` as starting point:
   - Author HTML5 Canvas drawing code that reproduces the timeline
   - Use `lib/createjs.min.js` (already in repo) for animation primitives
   - Re-link audio via SoundJS to files in `source/audio/`
5. **Replace** `pages/SS2-X.html` with the new CreateJS-driven version
6. **Test** side-by-side against `source/swf/SS2-X.swf` in desktop Ruffle for parity

This is documented for completeness; the entire site currently uses Path A and no page has needed Path B treatment.

---

## 9. Open items / known issues

| Item | Severity | Notes |
|---|---|---|
| Cross-browser QA matrix not yet completed | 🟡 Medium | Path A confirmed working in Chrome desktop; Safari, Firefox, Edge, iOS Safari, Android Chrome to verify |
| Lighthouse audits not yet run | 🟢 Low | Static site, expected to score well; verify before final handover |
| Per-page parity screenshots not captured | 🟢 Low | Capture during QA pass; store in `tests/` |
| Some `source/*` files accidentally committed (HTML originals + MP3s) | 🟢 Low | Pages still work; cleanup is cosmetic |
| Audio mapping (`audio-map.csv`) is skeleton | 🟢 Low | Only relevant if Path B fallback is ever used |

---

## 10. Project metadata

- **Original publication:** 2004
- **Removed from web:** 2018 (Adobe Flash Player end-of-life)
- **Restoration delivered:** 2026
- **Total runtime:** 60+ minutes across 31 pages
- **Source authoring tool:** Adobe Flash CS3/CS4 (pre-CS5 binary FLA format)
- **Restoration runtime:** Ruffle 0.1.0-nightly (latest unpkg)
- **Hosting:** Vercel (free tier)
- **Deploy URL:** https://singularityshuttle-html5.vercel.app

---

## 11. Contacts

- **Project lead:** Redstone Catalyst
- **Original content owner:** Singularity Shuttle (2004)
- **Issue tracker:** https://github.com/raffayprogrammer/singularityshuttle-html5/issues

---

*End of Developer Guide.*
