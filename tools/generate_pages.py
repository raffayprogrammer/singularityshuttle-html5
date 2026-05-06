"""
Generate one HTML wrapper per page from inventory.csv.

Each wrapper:
  - embeds Ruffle.js from CDN
  - loads the corresponding .swf
  - rewrites any old singularityshuttle.com URLs in the SWF's getURL calls
    to point at our local /pages/* paths
  - shows a small footer with Home + Contents links
"""
import csv
from pathlib import Path

ROOT = Path(r"D:/SingularityShuttle")
INVENTORY = ROOT / "docs" / "inventory.csv"
PAGES_DIR = ROOT / "pages"

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<title>Singularity Shuttle — {page_id}</title>
<style>
  html, body {{
    margin: 0;
    padding: 0;
    background: #0d0d0d;
    font-family: system-ui, -apple-system, sans-serif;
    min-height: 100vh;
  }}
  #stageWrap {{
    width: 100%;
    display: flex;
    justify-content: center;
    padding: 20px 0 60px;
    box-sizing: border-box;
  }}
  #player {{
    width: 100%;
    max-width: {stage_w}px;
    aspect-ratio: {stage_w} / {stage_h};
    background: #000;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
  }}
  nav.bottombar {{
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 10px 16px;
    background: rgba(0,0,0,0.85);
    color: #aaa;
    text-align: center;
    font-size: 12px;
    z-index: 100;
    backdrop-filter: blur(6px);
  }}
  nav.bottombar a {{
    color: #ed1515;
    text-decoration: none;
    margin: 0 10px;
    font-weight: 600;
  }}
  nav.bottombar a:hover {{ text-decoration: underline; }}
  .badge {{
    display: inline-block;
    padding: 2px 8px;
    background: #ed1515;
    color: #fff;
    font-size: 10px;
    letter-spacing: 1px;
    text-transform: uppercase;
    border-radius: 4px;
    margin-right: 8px;
  }}
</style>
</head>
<body>

<script>
  // ===== URL rewriting =====
  // The original SWFs reference http://www.singularityshuttle.com/SS2-X.html
  // for cross-page navigation. Intercept those calls and redirect to local paths.
  (function () {{
    var origOpen = window.open.bind(window);
    function remap(u) {{
      if (typeof u !== "string") return u;
      var m = u.match(/^https?:\\/\\/(www\\.)?singularityshuttle\\.com\\/(.*)$/i);
      if (!m) return u;
      var path = m[2];
      if (path === "" || path.toLowerCase() === "index.html") return "/";
      // SS2-X.html or any other file
      return "/pages/" + path;
    }}
    window.open = function (url, name, features) {{
      return origOpen(remap(url), name, features);
    }};
    // Cover Ruffle's location.assign / replace / href setter paths too
    try {{
      var loc = window.location;
      var ass = loc.assign && loc.assign.bind(loc);
      if (ass) loc.assign = function (u) {{ return ass(remap(u)); }};
      var rep = loc.replace && loc.replace.bind(loc);
      if (rep) loc.replace = function (u) {{ return rep(remap(u)); }};
    }} catch (e) {{ /* read-only on some browsers; window.open is the main path anyway */ }}
  }})();
</script>

<div id="stageWrap">
  <div id="player"></div>
</div>

<nav class="bottombar">
  <span class="badge">{page_id}</span>
  Singularity Shuttle &middot; {stage_w} &times; {stage_h}
  &nbsp;|&nbsp;
  <a href="/">Home</a>
  &nbsp;|&nbsp;
  <a href="/pages/SS2-J.html">Contents</a>
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

    PAGES_DIR.mkdir(exist_ok=True)
    for r in rows:
        page_id = r["page_id"]
        try:
            stage_w = int(r["stage_w"])
            stage_h = int(r["stage_h"])
        except ValueError:
            print(f"!! skipping {page_id}: missing dimensions")
            continue

        out = PAGES_DIR / f"{page_id}.html"
        out.write_text(
            TEMPLATE.format(page_id=page_id, stage_w=stage_w, stage_h=stage_h),
            encoding="utf-8",
        )

    print(f"wrote {len(rows)} HTML pages to {PAGES_DIR}")


if __name__ == "__main__":
    main()
