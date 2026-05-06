"""
Generate one HTML wrapper per page from inventory.csv + page-metadata.json.

Each wrapper:
  - sleek dark page with header (page id badge, title, section)
  - centered player loading the SWF via Ruffle.js
  - URL-rewriting JS (3 override paths) so SWF nav lands on local pages
  - bottom navbar with Home + Contents + prev/next where applicable
"""
import csv
import json
from pathlib import Path

ROOT = Path(r"D:/SingularityShuttle")
INVENTORY = ROOT / "docs" / "inventory.csv"
METADATA = ROOT / "docs" / "page-metadata.json"
PAGES_DIR = ROOT / "pages"

# Linear sequence used for the bottom-bar prev/next
ORDER = [
    "SS2-1", "SS2-1text",
    "SS2-2", "SS2-2text",
    "SS2-3", "SS2-3text", "SS2-3a", "SS2-3atext",
    "SS2-4", "SS2-4text", "SS2-4a", "SS2-4atext",
    "SS2-5", "SS2-5text", "SS2-5a", "SS2-5atext",
    "SS2-6", "SS2-6text", "SS2-6a", "SS2-6atext",
    "SS2-7", "SS2-7text", "SS2-7a", "SS2-7atext", "SS2-7b", "SS2-7btext",
    "SS2-8", "SS2-8text", "SS2-8a", "SS2-8atext",
    "SS2-J",
]

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<title>{title} · Singularity Shuttle</title>
<meta name="description" content="Singularity Shuttle · {page_id} · {title}">
<style>
  *, *::before, *::after {{ box-sizing: border-box; }}
  html, body {{
    margin: 0; padding: 0;
    background:
      radial-gradient(ellipse at top, rgba(237,21,21,0.08) 0%, transparent 50%),
      radial-gradient(ellipse at bottom, rgba(50,80,200,0.06) 0%, transparent 60%),
      #0a0a0a;
    color: #f0f0f0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
    min-height: 100vh;
    -webkit-font-smoothing: antialiased;
  }}
  a {{ color: inherit; }}
  .page-header {{
    max-width: 720px;
    margin: 0 auto;
    padding: 32px 24px 16px;
    text-align: center;
  }}
  .breadcrumb {{
    font-size: 12px;
    color: #888;
    margin-bottom: 12px;
    letter-spacing: 0.4px;
  }}
  .breadcrumb a {{ color: #aaa; text-decoration: none; }}
  .breadcrumb a:hover {{ color: #ed1515; }}
  .breadcrumb span {{ color: #444; margin: 0 8px; }}
  .page-id {{
    display: inline-block;
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    background: rgba(237,21,21,0.15);
    border: 1px solid rgba(237,21,21,0.4);
    color: #ff6b6b;
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1px;
    margin-bottom: 12px;
  }}
  .page-title {{
    font-size: clamp(24px, 4vw, 34px);
    font-weight: 700;
    margin: 8px 0 6px;
    letter-spacing: -0.5px;
    line-height: 1.15;
  }}
  .page-section {{
    color: #888;
    font-size: 14px;
    margin-bottom: 8px;
  }}
  .page-meta {{
    color: #555;
    font-size: 11px;
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    letter-spacing: 0.5px;
  }}
  #stageWrap {{
    width: 100%;
    display: flex;
    justify-content: center;
    padding: 8px 12px 80px;
  }}
  #player {{
    width: 100%;
    max-width: {stage_w}px;
    aspect-ratio: {stage_w} / {stage_h};
    background: #000;
    border-radius: 8px;
    overflow: hidden;
    box-shadow:
      0 0 0 1px rgba(255,255,255,0.04),
      0 16px 48px rgba(0,0,0,0.5),
      0 0 80px rgba(237,21,21,0.06);
  }}
  nav.bottombar {{
    position: fixed;
    bottom: 0; left: 0; right: 0;
    padding: 10px 16px;
    background: rgba(10,10,10,0.92);
    border-top: 1px solid #1a1a1a;
    color: #888;
    text-align: center;
    font-size: 12px;
    z-index: 100;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
  }}
  nav.bottombar a {{
    color: #ddd;
    text-decoration: none;
    margin: 0 8px;
    font-weight: 500;
    transition: color 150ms;
  }}
  nav.bottombar a:hover {{ color: #ed1515; }}
  nav.bottombar .sep {{ color: #333; margin: 0 4px; }}
  nav.bottombar .ghost {{ color: #555; }}
</style>
</head>
<body>

<script>
  // URL rewriting — three independent overrides for Ruffle's navigation paths
  (function () {{
    function remap(u) {{
      if (typeof u !== "string") return u;
      var m = u.match(/^https?:\\/\\/(www\\.)?singularityshuttle\\.com\\/(.*)$/i);
      if (!m) return u;
      var path = m[2];
      if (path === "" || path.toLowerCase() === "index.html") return "/";
      return "/pages/" + path;
    }}

    var origOpen = window.open.bind(window);
    window.open = function (url, name, features) {{
      return origOpen(remap(url), name, features);
    }};

    try {{
      var loc = window.location;
      var ass = loc.assign && loc.assign.bind(loc);
      if (ass) loc.assign = function (u) {{ return ass(remap(u)); }};
      var rep = loc.replace && loc.replace.bind(loc);
      if (rep) loc.replace = function (u) {{ return rep(remap(u)); }};
    }} catch (e) {{ /* silent */ }}

    try {{
      var proto = Location.prototype;
      var d = Object.getOwnPropertyDescriptor(proto, "href");
      if (d && d.set) {{
        var origSet = d.set;
        Object.defineProperty(proto, "href", {{
          configurable: true, enumerable: true,
          get: d.get,
          set: function (v) {{ return origSet.call(this, remap(v)); }}
        }});
      }}
    }} catch (e) {{ /* silent */ }}
  }})();
</script>

<header class="page-header">
  <div class="breadcrumb">
    <a href="/">Singularity Shuttle</a>
    <span>›</span>
    <a href="/#contents">Pages</a>
    <span>›</span>
    {page_id}
  </div>
  <span class="page-id">{page_id}</span>
  <h1 class="page-title">{title}</h1>
  <div class="page-section">{section}</div>
  <div class="page-meta">{stage_w} × {stage_h} · Restored from original 2004 Flash via Ruffle.js</div>
</header>

<div id="stageWrap">
  <div id="player"></div>
</div>

<nav class="bottombar">
  {prev_link}
  <span class="sep">·</span>
  <a href="/">Home</a>
  <span class="sep">·</span>
  <a href="/pages/SS2-J.html">Contents</a>
  <span class="sep">·</span>
  {next_link}
</nav>

<script src="https://unpkg.com/@ruffle-rs/ruffle"></script>
<script>
  window.RufflePlayer = window.RufflePlayer || {{}};
  window.addEventListener("load", function () {{
    var ruffle = window.RufflePlayer.newest();
    var player = ruffle.createPlayer();
    var container = document.getElementById("player");
    container.appendChild(player);
    player.load({{
      url: "{page_id}.swf",
      autoplay: "auto",
      unmuteOverlay: "visible",
      letterbox: "on",
      scale: "showAll"
    }});
  }});
</script>

</body>
</html>
"""


def main():
    rows = []
    with open(INVENTORY, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    with open(METADATA, encoding="utf-8") as f:
        meta = json.load(f)

    PAGES_DIR.mkdir(exist_ok=True)
    for r in rows:
        page_id = r["page_id"]
        try:
            stage_w = int(r["stage_w"])
            stage_h = int(r["stage_h"])
        except ValueError:
            print(f"!! skipping {page_id}: missing dimensions")
            continue

        page_meta = meta.get(page_id, {"title": page_id, "section": ""})
        title = page_meta["title"]
        section = page_meta["section"]

        # prev / next from linear ORDER
        try:
            idx = ORDER.index(page_id)
            prev_id = ORDER[idx - 1] if idx > 0 else None
            next_id = ORDER[idx + 1] if idx < len(ORDER) - 1 else None
        except ValueError:
            prev_id = next_id = None

        if prev_id:
            prev_link = f'<a href="/pages/{prev_id}.html">‹ Previous</a>'
        else:
            prev_link = '<span class="ghost">‹ Previous</span>'

        if next_id:
            next_link = f'<a href="/pages/{next_id}.html">Next ›</a>'
        else:
            next_link = '<span class="ghost">Next ›</span>'

        out = PAGES_DIR / f"{page_id}.html"
        out.write_text(
            TEMPLATE.format(
                page_id=page_id,
                title=title,
                section=section,
                stage_w=stage_w,
                stage_h=stage_h,
                prev_link=prev_link,
                next_link=next_link,
            ),
            encoding="utf-8",
        )

    print(f"wrote {len(rows)} HTML pages to {PAGES_DIR}")


if __name__ == "__main__":
    main()
