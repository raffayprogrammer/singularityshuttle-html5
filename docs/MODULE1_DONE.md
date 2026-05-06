# Module 1 — Environment & Pipeline Setup

**Status:** 🟢 9 of 10 outputs complete &nbsp;|&nbsp; ⏸ 1 blocked on Adobe Animate license

---

## Definition of Done — Checklist

| # | Output | Status | Evidence |
|---|---|---|---|
| 1 | Folder structure scaffolded | ✅ | `source/`, `build/`, `docs/`, `tests/`, `tools/` exist |
| 2 | 31 FLA in `source/fla/` | ✅ | `ls source/fla/ \| wc -l` → 31 |
| 3 | 31 SWF in `source/swf/` | ✅ | `ls source/swf/ \| wc -l` → 31 |
| 4 | 31 HTML in `source/html-original/` | ✅ | `ls source/html-original/ \| wc -l` → 31 |
| 5 | 43 MP3 + 138 WAV + 78 SFK organised | ✅ | `source/audio/{mp3,wav,sfk-archive}/` populated |
| 6 | `inventory.csv` with stage dimensions | ✅ | [docs/inventory.csv](inventory.csv) — 31 rows, all dimensions filled |
| 7 | `audio-map.csv` skeleton | ✅ | [docs/audio-map.csv](audio-map.csv) — 31 placeholder rows |
| 8 | `audio-files-index.txt` | ✅ | [docs/audio-files-index.txt](audio-files-index.txt) — full list of MP3 + WAV |
| 9 | CreateJS library | ✅ | `build/lib/createjs.min.js` (242 KB, v1.0.0) |
| 10 | Shared wrapper template + JS scaler | ✅ | [docs/wrapper-template.html](wrapper-template.html), [build/lib/wrapper.js](../build/lib/wrapper.js) |
| 11 | Mobile audio gate (tap-to-begin) | ✅ | `mountAudioGate()` in `wrapper.js` |
| 12 | Ruffle SWF emulator installed | ✅ | `tools/ruffle/ruffle.exe` |
| 13 | Ruffle plays SS2-1.swf | ⏳ | Manual verification — see "How to Validate" below |
| 14 | Adobe Animate opens SS2-1.fla | ⏸ | **Blocked on license — start free trial then verify** |
| 15 | Git repo initialized + .gitignore | ✅ | This commit |
| 16 | GitHub repo + Pages staging URL | ⏳ | See "Push to GitHub" below |

---

## Findings from Inventory

### Page structure (different from proposal description)

The proposal described the 15 full pages as *"Pages 1 through 15."* The actual source is:

| Group | Pages | Count |
|---|---|---|
| Main numbered | SS2-1, SS2-2, SS2-3, SS2-4, SS2-5, SS2-6, SS2-7, SS2-8 | 8 |
| Sub-pages | SS2-3a, SS2-4a, SS2-5a, SS2-6a, SS2-7a, **SS2-7b**, SS2-8a | 7 |
| **Subtotal full** | | **15** |
| Text-only counterparts (one per full page) | SS2-Xtext / SS2-Xatext / SS2-7btext | 15 |
| Jump / contents | SS2-J | 1 |
| **Total deliverable** | | **31** ✓ |

**Total deliverable count matches the proposal (31).** Only the structure description differs. **Surface this to the project lead before M1 sign-off.**

### Stage dimensions

- All pages share the same width (**684 px**) — matches proposal.
- Heights vary from **570 px** (`SS2-J`, the jump hub) to **2850 px** (`SS2-7a`).
- The proposal called `SS2-5` the "largest page" — that was true for the *sample* set reviewed. The actual largest page is `SS2-7a` (684 × 2850). Worth noting; not material to scope.

### Audio assets

- 43 MP3 + 138 WAV = **181 unique audio assets** for 31 pages (~5–6 sounds per page).
- Names are sound-design labels (`ARCUS 1`, `BOOMS 022`, `ASTRAL DAWN`, `Machine hum with heartbeat`), with **no direct mapping to pages**. Mapping must be derived during conversion by opening each FLA's library in Animate and matching symbol names against `docs/audio-files-index.txt`.

---

## How to Validate Module 1

Run these checks yourself to confirm everything is wired up:

### 1. File counts

```bash
cd D:/SingularityShuttle
ls source/fla/ | wc -l                  # → 31
ls source/swf/ | wc -l                  # → 31
ls source/html-original/ | wc -l        # → 31
ls source/audio/mp3/ | wc -l            # → 43
ls source/audio/wav/ | wc -l            # → 138
wc -l docs/inventory.csv                # → 32 (1 header + 31 rows)
wc -l docs/audio-map.csv                # → 32
```

### 2. Inventory has real numbers (not "?" placeholders)

```bash
grep "?" docs/inventory.csv             # → no matches in stage_w/stage_h columns
```

### 3. CreateJS loads in browser

Open `build/index.html` directly in Chrome — should display the placeholder landing page with no console errors. Then in DevTools Console:
```js
typeof createjs    // → "object"  (not "undefined")
```

### 4. Ruffle plays an SWF locally

```bash
# Launch Ruffle and open SS2-1.swf
"D:/SingularityShuttle/tools/ruffle/ruffle.exe" "D:/SingularityShuttle/source/swf/SS2-1.swf"
```
Expected: Ruffle window opens, SWF starts playing with audio. If audio is silent or animation freezes, note which page/timestamp — important for parity reference later.

### 5. Adobe Animate opens a FLA (after license is active)

- Launch Adobe Animate
- File → Open → `D:/SingularityShuttle/source/fla/SS2-1.fla`
- Expected: file opens, prompts to upgrade legacy format → accept
- Confirm stage shows **684 × 1795 px** in the bottom-right of the timeline panel
- Save screenshot to `tests/animate-opens-ss2-1.png`

### 6. Git is clean

```bash
git status                              # → "working tree clean" after first commit
git log --oneline                       # → 1 commit (initial Module 1)
```

---

## Push to GitHub

```bash
# Create empty repo on github.com first (no README, no .gitignore — we have ours)
# Repo name suggestion: singularityshuttle-html5

cd D:/SingularityShuttle
git remote add origin https://github.com/<your-username>/singularityshuttle-html5.git
git push -u origin main
```

### Enable GitHub Pages

1. Repo → Settings → Pages
2. Source: **Deploy from branch**
3. Branch: **main** &nbsp;|&nbsp; Folder: **`/build`**
4. Save → wait ~1 minute → Pages URL appears at top of Settings → Pages

The build is then live at `https://<your-username>.github.io/singularityshuttle-html5/` — this is your **staging URL** for client review. As you convert pages and commit them to `build/pages/`, GitHub Pages auto-deploys on push.

### What gets pushed to GitHub vs stays local

| Pushed | Stays local (.gitignored) |
|---|---|
| `build/` (the deliverable) | `source/fla/` |
| `docs/` | `source/swf/` |
| `tools/*.py` | `source/audio/wav/` |
| `README.md`, `.gitignore` | `source/audio/sfk-archive/` |
|  | `tools/ruffle/` |

`source/audio/mp3/` is currently *not* gitignored — keep it small (or move it out if total MP3 size goes >100 MB).

---

## Outstanding Items Before M1 Pilot Can Start

1. ⏸ **Adobe Animate license / trial** — the only remaining blocker
2. 🟡 **Ruffle parity playback test** — manual, ~5 min
3. 🟡 **Project-lead acknowledgement** of the page-structure clarification (sub-pages vs. linear 1-15)

Once the Animate trial is active and Ruffle is verified, M1 conversion of `SS2-1` can begin immediately.
