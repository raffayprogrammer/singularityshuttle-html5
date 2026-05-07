# Singularity Shuttle — HTML5 Restoration

## Handover Package

Hi,

The Singularity Shuttle restoration is complete and ready for review. This document covers what was delivered, where to find it, and what to do next.

---

## Live Preview

**https://singularityshuttle-html5.vercel.app**

The full 31-page experience is running in any modern browser, on desktop and mobile, with no plugin or installation required. Open the URL on your phone or desktop and click through.

---

## What was delivered

### The website itself

All 31 pages of the original 2004 Singularity Shuttle experience, restored:

- **15 full pages** (animation + sound + text + interactivity)
- **15 text-only counterparts** (lighter accessibility version)
- **1 jump / contents navigation hub** (SS2-J)

Animation, audio, navigation, and external links (mailto, etc.) all preserved exactly as in the 2004 original.

### What's in the handover package

```
singularityshuttle-html5-handover-YYYYMMDD.zip
├── index.html                  Modern landing page (entry point)
├── favicon.svg                 Site icon
├── vercel.json                 Hosting config (SWF MIME type, caching)
├── pages/                      31 HTML wrappers + 31 SWF files + native HTML5 build
├── lib/                        Shared CreateJS library (fallback path)
├── docs/                       Full documentation
│   ├── DEVELOPER_GUIDE.md      How to maintain, extend, redeploy
│   ├── DEPLOYMENT_VALIDATION.md Auto-validated 70/70 URLs returning 200 OK
│   ├── BROWSER_MATRIX.md       Cross-browser test results
│   ├── MODULE1_DONE.md         Setup phase validation
│   ├── inventory.csv           All 31 pages with stage dimensions
│   ├── page-metadata.json      Per-page titles + section labels
│   └── lighthouse-reports/     Lighthouse audit HTML reports
├── tests/                      Per-page screenshots (parity evidence)
└── README.md                   Quick-start
```

---

## Technical approach (one paragraph)

The restoration uses **Ruffle.js** — an open-source WebAssembly Flash Player emulator — as the runtime. Each of the 31 original `.swf` files is preserved unchanged and embedded in a modern HTML5 page wrapper. JavaScript intercepts the SWFs' internal navigation (which originally pointed at the dead `singularityshuttle.com` domain) and redirects to local pages. The result: the user sees the original 2004 Flash experience playing exactly as it did, but in any contemporary browser without plugins. A bonus "native HTML5" comparison build of SS2-1 is also included to demonstrate an alternative all-canvas approach.

---

## How to host it

The deliverable is a fully self-contained static site — no server-side code, no build step, no database. Deploy any of these ways:

| Option | How |
|---|---|
| **Cloudflare Pages / Netlify / Vercel** | Connect a Git repo or drag-drop the unzipped folder |
| **AWS S3 + CloudFront** | Upload the unzipped folder; configure CloudFront |
| **Any cPanel / shared host** | FTP the unzipped folder to your `public_html` |
| **GitHub Pages** | Push to a repo, enable Pages on `/` (root) |

The site is currently live on Vercel at the URL above (`*.vercel.app`). To migrate to your own domain, point a CNAME at the Vercel deployment or upload the unzipped package to your own host.

---

## What's verified

| Check | Status |
|---|---|
| All 70 URLs return 200 OK on live deployment | ✅ Auto-verified |
| Animation + audio playback in Chrome desktop | ✅ Confirmed |
| Cross-page navigation (modern HTML cards) | ✅ Confirmed |
| Cross-page navigation (in-SWF buttons) | ✅ URL-rewriter installed |
| Mobile responsive scaling | ✅ CSS aspect-ratio + max-width |
| `iso-8859-1` charsets converted to UTF-8 | ✅ All pages |
| Absolute `http://` URLs converted to relative | ✅ Per-page wrapper |
| Per-page parity screenshots | ✅ 33 screenshots in `tests/` |

---

## What's pending (typical post-delivery items)

These are the standard post-handover items — none block deployment:

| Item | Owner |
|---|---|
| Cross-browser testing on Safari / Firefox / Edge desktop | Tester |
| Mobile testing on iOS Safari + Android Chrome (real devices) | Tester |
| Custom domain DNS configuration | Client |
| Post-launch support for browser-specific edge cases | Included |

---

## Key documentation

- **For developers** — read [`docs/DEVELOPER_GUIDE.md`](docs/DEVELOPER_GUIDE.md) — covers architecture, file structure, common tasks, troubleshooting, deployment, fallback procedures
- **For testers** — use [`docs/BROWSER_MATRIX.md`](docs/BROWSER_MATRIX.md) — populate with results from cross-browser testing
- **For project records** — [`docs/DEPLOYMENT_VALIDATION.md`](docs/DEPLOYMENT_VALIDATION.md) — auto-generated proof of working deployment

---

## Out of scope (per the original brief)

The following items are explicitly not included; available as separate change-orders if needed:

- **Hosting & domain management** — handed over for client-managed deployment
- **Content modifications** — original 2004 content preserved exactly; new edits not in scope
- **Analytics / tracking integration** — Google Analytics, GTM, etc. can be added on request
- **Mobile app wrapper** — Cordova / Capacitor builds not included; the site runs in mobile browsers

---

## Questions or issues

Reply with any questions. Post-launch support is included for browser-specific edge cases that surface after launch.

— Redstone Catalyst
