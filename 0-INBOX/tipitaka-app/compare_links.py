"""Compare our commentary→root links with tipitaka.app's paranum links.

Ours: a commentary paragraph whose text opens with a printed number "N." or
"N-M." is linked to root paragraph(s) N..M (one transclusion each).
Site: /api/links entries with src == "paranum" between two layers.

Usage:
  compare_links.py mula-atta <root.json> <atta.json> <site-links-of-root.json>
  compare_links.py atta-tika <atta.json> <tika.json> <site-links-of-tika.json>
For atta-tika the check is that each site link joins two paragraphs carrying
the same printed number — the property our ṭīkā→root links rely on.
"""
import json, re, sys
from pathlib import Path

LEAD = re.compile(r"^\s*(\d+)(?:-(\d+))?\.\s")


HEADS = ("chapter", "title", "subhead", "subsubhead", "book", "nikaya")


def nums(seg):
    if seg.get("css_class") in HEADS:
        return []  # headings carry numbers but are never linked
    m = LEAD.match(seg["content"])
    if not m:
        return []
    a = int(m.group(1)); b = int(m.group(2)) if m.group(2) else a
    return list(range(a, b + 1)) if b >= a else [a]


def load(p):
    d = json.loads(Path(p).read_text(encoding="utf-8"))
    return d["segments"]


def mula_atta(root_p, att_p, links_p):
    root, att = load(root_p), load(att_p)
    site = {(root[x["i"]] and tuple(nums(root[x["i"]])), x["t"])
            for x in json.loads(Path(links_p).read_text(encoding="utf-8"))
            if x["src"] == "paranum" and x["kind"] == "mula-atta"}
    site_pairs = {(n, t) for ns, t in site for n in ns}
    ours = {(n, i) for i, s in enumerate(att) for n in nums(s)}
    only_site, only_ours = site_pairs - ours, ours - site_pairs
    print(f"mula-atta: site {len(site_pairs)} links, ours {len(ours)}, "
          f"shared {len(site_pairs & ours)}, only on site {len(only_site)}, only ours {len(only_ours)}")
    for n, t in sorted(only_site)[:20]:
        print(f"  only on site: root {n} <- commentary para #{t}: {att[t]['content'][:70]!r}")
    for n, t in sorted(only_ours)[:20]:
        print(f"  only ours:    root {n} <- commentary para #{t}: {att[t]['content'][:70]!r}")


def atta_tika(att_p, tika_p, links_p):
    att, tika = load(att_p), load(tika_p)
    L = [x for x in json.loads(Path(links_p).read_text(encoding="utf-8"))
         if x["src"] == "paranum" and x["kind"] == "atta-tika"]
    same = [x for x in L if set(nums(tika[x["i"]])) & set(nums(att[x["t"]]))]
    print(f"atta-tika: site {len(L)} paranum links, {len(same)} join paragraphs with the same printed number")
    for x in [x for x in L if x not in same][:20]:
        print(f"  differs: tika #{x['i']} {tika[x['i']]['content'][:50]!r}  atta #{x['t']} {att[x['t']]['content'][:50]!r}")
    cited = sum(1 for s in tika if nums(s))
    print(f"  ṭīkā paragraphs with a printed number (linked to the root by us): {cited}")


if __name__ == "__main__":
    {"mula-atta": mula_atta, "atta-tika": atta_tika}[sys.argv[1]](*sys.argv[2:])
