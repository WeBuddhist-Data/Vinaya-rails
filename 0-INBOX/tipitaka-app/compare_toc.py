"""Compare the vault's root-text heading trees with tipitaka.app's.
Both are matched to source segments: tipitaka.app gives each node's start
segment; the vault headings are matched to JSON heading segments in order."""
import json, re, sys
from pathlib import Path
BOOKS = [(1, "vin01m", "vp-prj"), (2, "vin02m1", "vp-pct"), (3, "vin02m2", "vp-mv"),
         (4, "vin02m3", "vp-cv"), (5, "vin02m4", "vp-pv")]
NUM = re.compile(r"^\s*\d+(?:-\d+)*\.\s*")
HCLS = ("chapter", "title", "subhead", "subsubhead")
def norm(t): return re.sub(r"\s*\[.*\]\s*$", "", NUM.sub("", t)).strip()
total = 0
for b, stem, key in BOOKS:
    segs = json.loads(Path(f"0-INBOX/raw-data/{stem}.json").read_text(encoding="utf-8"))["segments"]
    site = json.loads(Path(f"0-INBOX/tipitaka-app/{key}.json").read_text(encoding="utf-8"))
    md = [l for l in Path(f"1-SOURCES/Text/pi-{b}.md").read_text(encoding="utf-8").split("\n") if re.match(r"^#{3,} ", l)]
    mine = []
    for l in md:
        lvl = len(l.split(" ")[0]); title = re.sub(r"\s\^\S+$", "", l[lvl + 1:]).replace("**", "")
        mine.append((lvl, title))
    # positions of JSON heading segments, in order
    jh = [(i, s["content"]) for i, s in enumerate(segs) if s["css_class"] in HCLS]
    pos, j = [], 0
    for lvl, t in mine:
        while j < len(jh) and norm(jh[j][1]) != t: j += 1
        pos.append(jh[j][0] if j < len(jh) else None); j += 1
    mine_by_pos = {p: (lvl, t) for p, (lvl, t) in zip(pos, mine) if p is not None}
    diffs = []
    site_pos = set()
    for n in site:
        p = n["start"]; site_pos.add(p)
        m = mine_by_pos.get(p)
        if m is None:
            diffs.append(f"  only on site   d{n['depth']} @{p} {n['title']}")
        elif m[0] != n["depth"] or m[1] != norm(n["title"]):
            diffs.append(f"  differs        @{p} site d{n['depth']} '{n['title']}'  vault d{m[0]} '{m[1]}'")
    for p, (lvl, t) in mine_by_pos.items():
        if p not in site_pos:
            diffs.append(f"  only in vault  d{lvl} @{p} {t}")
    unmatched = [t for p, (l, t) in zip(pos, mine) if p is None]
    print(f"pi-{b} ({key}): site {len(site)} nodes, vault {len(mine)} headings, {len(diffs)} differences" + (f", {len(unmatched)} vault headings not located" if unmatched else ""))
    for d in diffs: print(d)
    total += len(diffs)
print("TOTAL", total)
