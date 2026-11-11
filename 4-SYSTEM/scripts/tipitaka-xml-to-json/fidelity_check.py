#!/usr/bin/env python3
"""Check that a converted markdown file carries every word of its source JSON,
in order (headings' leading numbers, ^block IDs and transclusions ignored).
Usage: fidelity_check.py <source.json> <file.md>"""
import json, re, sys
from pathlib import Path

def words(s):
    return re.findall(r"[^\s\"‘’“”–—\-\[\]().,;:?!*]+", s)

def main(jp, mp):
    segs = json.loads(Path(jp).read_text(encoding="utf-8"))["segments"]
    src = []
    for s in segs:
        c = s["content"]
        if s["css_class"] in ("chapter", "title", "subhead", "subsubhead"):
            c = re.sub(r"^\s*\d+(-\d+)*\.\s*", "", c)
        else:
            c = re.sub(r"^\s*\d+(-\d+)*\.\s*", "", c)
        src += words(c)
    text = Path(mp).read_text(encoding="utf-8")
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
    out = []
    for line in text.split("\n"):
        if line.startswith("![["):
            continue
        line = re.sub(r"\s\^\S+\s*$", "", line)
        # The '#' piṭaka line carries an editorial layer label, e.g.
        # "# Vinayapiṭake (aṭṭhakathā)" — not source text.
        line = re.sub(r"^(# .*?)\s*\((aṭṭhakathā|ṭīkā|anuṭīkā|[^)]*ṭīkā)\)\s*$", r"\1", line)
        line = re.sub(r"^#+\s+", "", line).replace("**", "")
        line = re.sub(r"^\s*\d+(-\d+)*\.\s*", "", line)
        out += words(line)
    i = 0
    for k, w in enumerate(src):
        if i < len(out) and out[i] == w:
            i += 1
            continue
        print(f"MISMATCH at source word {k}: {' '.join(src[max(0,k-5):k+5])!r} vs md {' '.join(out[max(0,i-5):i+5])!r}")
        return 1
    extra = len(out) - i
    print(f"{Path(mp).name}: {len(src)} source words, {len(out)} md words, all in order" + (f", {extra} extra md words" if extra else ""))
    return 0 if extra == 0 else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
