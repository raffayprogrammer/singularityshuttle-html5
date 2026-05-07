# Browser Compatibility Matrix

Cross-browser test results for the Singularity Shuttle restoration.

**Live URL:** https://singularityshuttle-html5.vercel.app
**Last automated validation:** see [`DEPLOYMENT_VALIDATION.md`](DEPLOYMENT_VALIDATION.md) — 70/70 URLs returning 200

---

## Test methodology

Each row below represents one test environment. For each, we verify:

1. **Landing page loads** — `/` renders the hero, card grid, and SS2-J embed
2. **Page wrapper loads** — at least 3 pages tested: `SS2-1`, `SS2-J`, `SS2-7a` (largest)
3. **Ruffle.js initializes** — the embedded player appears, no console errors
4. **Animation plays** — visual content moves as expected
5. **Audio plays** — narration / sound effects audible
6. **Cross-page navigation** — clicking buttons inside SS2-J navigates to other pages
7. **Modern card grid navigation** — clicking cards on `/` navigates correctly
8. **Native HTML5 build** — `/pages/SS2-1-native.html` renders, audio plays, buttons work

---

## Test status legend

- ✅ **Pass** — works as expected
- ⚠️ **Partial** — works with caveats (note in comments)
- ❌ **Fail** — does not work, blocking
- ⏳ **Pending** — not yet tested
- N/A **Not applicable**

---

## Desktop browsers

| Browser | Version | Landing | Page load | Ruffle init | Animation | Audio | Nav (SWF) | Nav (cards) | Native HTML5 | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Chrome | latest | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | |
| Firefox | latest | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | |
| Safari (macOS) | latest | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | |
| Edge | latest | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | |

## Mobile browsers

| Browser | Device | Landing | Page load | Ruffle init | Animation | Audio | Nav (SWF) | Nav (cards) | Native HTML5 | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Safari | iPhone (latest iOS) | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | |
| Chrome | Android (latest) | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | |

---

## How to populate this doc

1. Open the live URL in each browser/device
2. Click through the test methodology checklist (1-8 above)
3. Mark the cell ✅ / ⚠️ / ❌
4. Add notes for any partial or failed cells (e.g. "audio silent until tap" is a ⚠️ caveat, not a fail)
5. Commit + push the updated matrix

---

## Known caveats (apply to all browsers)

- **First-load delay:** Ruffle.js downloads ~3 MB of WebAssembly on first visit. Subsequent visits are cached. Expect 2-3 seconds before the player appears.
- **Audio autoplay block:** All modern browsers block audio playback until a user gesture. Ruffle's `unmuteOverlay` config shows a "Click to unmute" overlay. This is expected behavior, not a bug — note it as ⚠️ if testing requires explicit click.
- **Tall pages on narrow phones:** Pages like SS2-7a (684×2850) scale to viewport width — content stays legible but may require scrolling. This is by design (preserves aspect ratio).
- **CDN dependency:** Ruffle.js loads from `unpkg.com`. If unpkg goes down, all pages break. To mitigate: self-host Ruffle (see `DEVELOPER_GUIDE.md` §6.4).

---

## Lighthouse audit (pending)

To run, with Chrome installed:

```bash
npx lighthouse https://singularityshuttle-html5.vercel.app --output html --output-path docs/lighthouse-landing.html
npx lighthouse https://singularityshuttle-html5.vercel.app/pages/SS2-1.html --output html --output-path docs/lighthouse-ss2-1.html
```

Target scores:
- **Performance:** ≥ 80 (acceptable for image-heavy / WASM-loading pages)
- **Accessibility:** ≥ 90
- **Best Practices:** ≥ 90
- **SEO:** ≥ 90

Findings will be summarized here once the audit runs.

---

## Test owner

Testing performed by: _[name]_
Date completed: _[YYYY-MM-DD]_
Sign-off: _[name + date]_
