"""Fetch the tipitaka.app contents tree (Mūla by default; pass other keys, e.g. atta-vp-prj, as arguments).
Writes 0-INBOX/tipitaka-app/<key>.json (list of nodes in document order)."""
import json, urllib.request
from pathlib import Path
V = "7d17987e5be3e268"
OUT = Path("0-INBOX/tipitaka-app")
def children(key):
    req = urllib.request.Request(f"https://tipitaka.app/api/children?key={key}&v={V}", headers={"User-Agent": "rails-toc-check"})
    return json.load(urllib.request.urlopen(req, timeout=30))
def walk(key, acc):
    for k in children(key):
        acc.append({x: k.get(x) for x in ("key", "depth", "rend", "start", "end", "title")})
        if k.get("children"):
            walk(k["key"], acc)
import sys
KEYS = sys.argv[1:] or ["vp-prj", "vp-pct", "vp-mv", "vp-cv", "vp-pv"]
for b in KEYS:
    acc = []; walk(b, acc)
    (OUT / f"{b}.json").write_text(json.dumps(acc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(b, len(acc))
