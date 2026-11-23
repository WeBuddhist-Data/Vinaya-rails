"""Check a commentary's block IDs and its root-verse transclusions.

- content block IDs (non-heading `^B-N`) must run 1..N with no gaps or duplicates;
- every run of transclusion lines `![[<root>#^B-N]]` must be followed by a paragraph
  whose printed number (or range, incl. CST's truncated '133-4.') expands to exactly
  those IDs;
- every target must exist as a block ID in the root file.

usage: python check_links.py <commentary.md> <root.md>
"""
import re, sys
sys.stdout.reconfigure(encoding="utf-8")
L = open(sys.argv[1], encoding="utf-8").read().split("\n")
root_ids = set(re.findall(r"\^([\w-]+)\s*$", open(sys.argv[2], encoding="utf-8").read(), re.M))

ids = [m.group(1) for l in L if not l.startswith("#") for m in [re.search(r"\s\^(\d+-\d+)\s*$", l)] if m]
nums = [int(i.split("-")[1]) for i in ids]
print(f"content IDs: {len(ids)} ({ids[0] if ids else ''} … {ids[-1] if ids else ''}); "
      f"sequential: {nums == list(range(1, len(nums) + 1))}; duplicates: {len(ids) - len(set(ids))}")

bad = missing = groups = n = 0
targets = set()
k = 0
while k < len(L):
    if not L[k].startswith("![["):
        k += 1; continue
    grp = []
    while k < len(L) and (L[k].startswith("![[") or not L[k].strip()):
        if L[k].strip():
            m = re.match(r"^!\[\[([^#]+)#\^([\w-]+)\]\]", L[k])
            targets.add(m.group(1)); grp.append(m.group(2))
        k += 1
    groups += 1; n += len(grp)
    for t in grp:
        if t not in root_ids:
            missing += 1; print("  target missing in root:", t)
    book = grp[0].split("-")[0]
    p = re.match(r"^(\d+)(?:-(\d+))?\.", L[k]) if k < len(L) else None
    if not p:
        bad += 1; print(f"  line {k + 1}: no printed number after links {grp}: {L[k][:50]!r}"); continue
    a, b = p.group(1), p.group(2)
    if b and len(b) < len(a):
        b = a[:len(a) - len(b)] + b
    want = [f"{book}-{i}" for i in range(int(a), int(b or a) + 1)]
    if grp != want:
        bad += 1; print(f"  line {k + 1}: links {grp} but paragraph starts {L[k][:14]!r}")
print(f"link targets: {sorted(targets)}")
print(f"transclusion groups: {groups}; links: {n}; groups not matching the printed number: {bad}; targets missing in root: {missing}")
