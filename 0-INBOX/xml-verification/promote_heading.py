"""Move one heading up one level: it becomes the next sibling of its current parent.

Used for a heading nested too deep, e.g. a kaṇḍa's closing `Nigamanavaṇṇanā`
that landed under the kaṇḍa's last sikkhāpada:

    ##### 13. Kuladūsakasikkhāpadavaṇṇanā   ^1-6-13-0
    ###### Nigamanavaṇṇanā                  ^1-6-13-1-0
  ->
    ###### Nigamanavaṇṇanā                  ^1-6-14-0   (now one '#' less)

The heading must be the LAST child of its parent, and must have no later sibling
at the new level inside the grandparent, so no other heading ID needs to change;
the script refuses otherwise. Its own descendants (if any) move with it.
Non-heading lines are untouched (asserted).

usage: python promote_heading.py <file.md> <heading-id> [--write]
"""
import re, sys
sys.stdout.reconfigure(encoding="utf-8")
path, hid = sys.argv[1], sys.argv[2].lstrip("^")
WRITE = "--write" in sys.argv
HEAD = re.compile(r"^(#+)\s+(.*?)\s+\^([\w-]+)\s*$")

raw = open(path, "rb").read().decode("utf-8")
nl = "\r\n" if "\r\n" in raw else "\n"
L = raw.split(nl)
heads = [(i, len(m.group(1)), m.group(2), m.group(3)) for i, l in enumerate(L) if (m := HEAD.match(l))]
k = next(n for n, h in enumerate(heads) if h[3] == hid)
i, depth, title, _ = heads[k]
segs = hid.split("-")[:-1]                       # path without the trailing 0
parent_path, grand_path = segs[:-1], segs[:-2]
# siblings of the parent inside the grandparent: find the parent's number and the highest number used
sib_nums = [int(h[3].split("-")[len(grand_path)]) for h in heads
            if h[1] == depth - 1 and h[3].split("-")[:len(grand_path)] == grand_path]
parent_num = int(parent_path[-1])
assert parent_num == max(sib_nums), f"parent {parent_path} is not the grandparent's last child; later IDs would shift"
# it must be the parent's last child
later_kids = [h for h in heads[k + 1:] if h[1] == depth and h[3].split("-")[:len(parent_path)] == parent_path]
assert not later_kids, f"not the last child of its parent: {later_kids[0]}"
new_prefix = "-".join(grand_path + [str(parent_num + 1)])
old_prefix = "-".join(segs)

changes = []
for n in range(k, len(heads)):
    j, d, t, h = heads[n]
    if n > k and d <= depth:
        break
    new_id = new_prefix + h[len(old_prefix):]
    new = f"{'#' * (d - 1)} {re.sub(r'^\*\*(.*)\*\*$', r'\1', t) if d - 1 <= 6 else t} ^{new_id}"
    changes.append((j + 1, L[j], new))
    L[j] = new
assert [l for l in raw.split(nl) if not HEAD.match(l)] == [l for l in L if not HEAD.match(l)]
for ln, a, b in changes:
    print(f"{ln:6}: {a}\n        → {b}")
print(f"headings changed: {len(changes)}; non-heading lines unchanged: True")
if WRITE:
    open(path, "wb").write(nl.join(L).encode("utf-8"))
    print("written:", path)
else:
    print("dry run; pass --write to save")
