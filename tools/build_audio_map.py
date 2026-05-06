"""
Generate audio-map.csv skeleton.

For each page in inventory.csv, create one row to be filled in during conversion:
  page_id, sound_symbol, source_file, format, mapped_via, notes

The 'sound_symbol' column will be populated when each FLA's library is opened
in Adobe Animate (during M1/M2). The 'source_file' column gets matched against
files in source/audio/{mp3,wav}/.

Initial pass: write one placeholder row per page so the file structure exists.
A second pass (during M1 pilot) will fill SS2-1's real symbols.
"""
import csv
from pathlib import Path

INVENTORY = Path(r"D:/SingularityShuttle/docs/inventory.csv")
AUDIO_DIR = Path(r"D:/SingularityShuttle/source/audio")
OUT = Path(r"D:/SingularityShuttle/docs/audio-map.csv")


def main():
    rows = []
    with open(INVENTORY, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append({
                "page_id": r["page_id"],
                "sound_symbol": "<TO FILL FROM FLA LIBRARY>",
                "source_file": "",
                "format": "",
                "mapped_via": "",
                "notes": "",
            })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["page_id", "sound_symbol", "source_file", "format", "mapped_via", "notes"])
        w.writeheader()
        for r in rows:
            w.writerow(r)

    # also dump the available audio file list for cross-reference during mapping
    files_index = Path(r"D:/SingularityShuttle/docs/audio-files-index.txt")
    with open(files_index, "w", encoding="utf-8") as f:
        f.write("# Available audio assets in source/audio/\n\n")
        f.write("## MP3\n")
        for p in sorted((AUDIO_DIR / "mp3").glob("*.mp3")):
            f.write(p.name + "\n")
        f.write("\n## WAV\n")
        for p in sorted((AUDIO_DIR / "wav").glob("*.wav")):
            f.write(p.name + "\n")

    print(f"audio-map.csv: {len(rows)} placeholder rows")
    print(f"audio-files-index.txt: index of all source audio")


if __name__ == "__main__":
    main()
