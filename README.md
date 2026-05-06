# Singularity Shuttle — Flash to HTML5 Conversion

Restoration of the 31-page **Singularity Shuttle** interactive Flash experience (originally published 2004), rebuilt for the modern web with full preservation of animations, sound, and interactivity.

## Status

Module 1 (Environment & Pipeline Setup) — see [`docs/MODULE1_DONE.md`](docs/MODULE1_DONE.md).

## Repo Layout

```
SingularityShuttle/
├── source/              Original FLA / SWF / HTML / audio (NOT in git — too large)
├── build/               Final HTML5 output (deployable)
│   ├── pages/           One .html + .js per page (31 total)
│   ├── assets/          Re-organised audio + extracted images
│   └── lib/             Shared CreateJS + responsive scaler
├── docs/                inventory.csv, audio-map.csv, handover docs
├── tests/               Per-page parity screenshots
└── tools/               Ruffle, FLA/SWF parser scripts
```

## Tech Stack

- **Adobe Animate** (latest) — sole supported tool to open legacy `.fla` source
- **CreateJS** (EaselJS, TweenJS, SoundJS, PreloadJS) — runtime
- **HTML5 Canvas + ES2020** — output target
- **Ruffle** — SWF playback for parity reference

## Local Setup

```bash
# 1. Place SS Files.zip and SS Audio.zip alongside this repo
# 2. Run extraction (one-time)
python tools/parse_swf.py        # rebuild inventory.csv
python tools/build_audio_map.py  # rebuild audio-map skeleton
```

## Deployment

The `build/` folder is fully self-contained static — deploy to any static host:

- **GitHub Pages** (this repo's default — auto-deploys `build/`)
- **Cloudflare Pages / Netlify / Vercel** — drag-drop `build/` zip
- **Any cPanel / FTP host** — upload `build/` contents

No server-side code, no build step, no DB.

## License / Credits

Original content © Singularity Shuttle (2004).
Restoration by Redstone Catalyst.
