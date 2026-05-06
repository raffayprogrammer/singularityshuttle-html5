"""
Parse SWF files to extract stage width and height.
SWF format spec: https://www.adobe.com/content/dam/acom/en/devnet/pdf/swf-file-format-spec.pdf
Header: signature(3) + version(1) + length(4), then RECT (variable bits) for stage size.
RECT is in twips (1/20 px). FWS=uncompressed, CWS=zlib, ZWS=lzma.
"""
import os
import sys
import csv
import zlib
import struct
from pathlib import Path

SWF_DIR = Path(r"D:/SingularityShuttle/source/swf")
FLA_DIR = Path(r"D:/SingularityShuttle/source/fla")
HTML_DIR = Path(r"D:/SingularityShuttle/source/html-original")
OUT_CSV = Path(r"D:/SingularityShuttle/docs/inventory.csv")


def read_rect(stream):
    """Read a SWF RECT structure starting from current byte. Return (xmin,xmax,ymin,ymax) in twips."""
    nbits = (stream[0] >> 3) & 0x1F
    total_bits = 5 + 4 * nbits
    total_bytes = (total_bits + 7) // 8
    bits = ""
    for b in stream[:total_bytes]:
        bits += format(b, "08b")
    bits = bits[5:]  # skip nbits header
    fields = []
    for i in range(4):
        chunk = bits[i * nbits:(i + 1) * nbits]
        v = int(chunk, 2) if chunk else 0
        if chunk and chunk[0] == "1":
            v -= 1 << nbits
        fields.append(v)
    return fields  # xmin, xmax, ymin, ymax


def parse_swf(path):
    with open(path, "rb") as f:
        data = f.read()
    sig = data[:3]
    body = data[8:]
    if sig == b"CWS":
        body = zlib.decompress(body)
    elif sig == b"ZWS":
        return None, None  # LZMA — skip, not in this project
    elif sig != b"FWS":
        return None, None
    xmin, xmax, ymin, ymax = read_rect(body)
    width_px = (xmax - xmin) // 20
    height_px = (ymax - ymin) // 20
    return width_px, height_px


def classify(page_id):
    """Return (type, sort_key) for a page id like SS2-3atext."""
    base = page_id.replace("SS2-", "")
    if base == "J":
        return "jump", (99, 0, 0)
    is_text = base.endswith("text")
    if is_text:
        base = base[:-4]
    # base now like "1", "3a", "7b"
    num_part = ""
    suffix = ""
    for ch in base:
        if ch.isdigit():
            num_part += ch
        else:
            suffix += ch
    num = int(num_part) if num_part else 99
    sub_order = ord(suffix[0]) - ord("a") + 1 if suffix else 0
    if is_text and suffix:
        t = "text-sub"
    elif is_text:
        t = "text"
    elif suffix:
        t = "full-sub"
    else:
        t = "full"
    return t, (num, sub_order, 1 if is_text else 0)


def main():
    rows = []
    for swf in sorted(SWF_DIR.glob("*.swf")):
        page_id = swf.stem
        fla = FLA_DIR / f"{page_id}.fla"
        html = HTML_DIR / f"{page_id}.html"
        try:
            w, h = parse_swf(swf)
        except Exception as e:
            print(f"!! {swf.name}: {e}", file=sys.stderr)
            w, h = None, None
        ptype, sort_key = classify(page_id)
        rows.append({
            "page_id": page_id,
            "fla_file": fla.name if fla.exists() else "MISSING",
            "swf_file": swf.name,
            "original_html": html.name if html.exists() else "MISSING",
            "stage_w": w if w is not None else "?",
            "stage_h": h if h is not None else "?",
            "type": ptype,
            "status": "pending",
            "_sort": sort_key,
        })

    rows.sort(key=lambda r: r["_sort"])
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["page_id", "fla_file", "swf_file", "original_html", "stage_w", "stage_h", "type", "status"])
        w.writeheader()
        for r in rows:
            r.pop("_sort")
            w.writerow(r)
    print(f"wrote {len(rows)} rows to {OUT_CSV}")


if __name__ == "__main__":
    main()
