"""
Build the final handover zip package for client delivery.

Contents:
  - All deployable files (index.html, pages/, lib/, favicon.svg, vercel.json)
  - All documentation (docs/)
  - All test artifacts (tests/)
  - README with quick-start
  - Excludes: source/, tools/, node_modules/, .git/

Output: handover/singularityshuttle-html5-handover-YYYYMMDD.zip
"""
import zipfile
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:/SingularityShuttle")
OUT_DIR = ROOT / "handover"
DATE = datetime.now().strftime("%Y%m%d")
OUT_FILE = OUT_DIR / f"singularityshuttle-html5-handover-{DATE}.zip"

INCLUDE = [
    "index.html",
    "favicon.svg",
    "vercel.json",
    "README.md",
    "pages/",
    "lib/",
    "docs/",
    "tests/",
]

EXCLUDE_DIRS = {"node_modules", ".git", "source", "tools", "handover"}
EXCLUDE_FILES = {".DS_Store", "Thumbs.db", "package.json", "package-lock.json"}


def should_skip(p: Path) -> bool:
    parts = set(p.parts)
    if parts & EXCLUDE_DIRS:
        return True
    if p.name in EXCLUDE_FILES:
        return True
    return False


def main():
    OUT_DIR.mkdir(exist_ok=True)
    if OUT_FILE.exists():
        OUT_FILE.unlink()

    files_added = 0
    total_size = 0

    with zipfile.ZipFile(OUT_FILE, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for item in INCLUDE:
            src = ROOT / item
            if not src.exists():
                print(f"!! missing: {item}")
                continue
            if src.is_file():
                arcname = src.relative_to(ROOT).as_posix()
                z.write(src, arcname)
                files_added += 1
                total_size += src.stat().st_size
            elif src.is_dir():
                for f in src.rglob("*"):
                    if f.is_file() and not should_skip(f.relative_to(ROOT)):
                        arcname = f.relative_to(ROOT).as_posix()
                        z.write(f, arcname)
                        files_added += 1
                        total_size += f.stat().st_size

    zip_size = OUT_FILE.stat().st_size
    print(f"Created: {OUT_FILE}")
    print(f"Files: {files_added}")
    print(f"Source size: {total_size / 1024 / 1024:.1f} MB")
    print(f"Zip size:    {zip_size / 1024 / 1024:.1f} MB")
    print(f"Compression: {(1 - zip_size / total_size) * 100:.0f}%")


if __name__ == "__main__":
    main()
