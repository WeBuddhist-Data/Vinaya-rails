"""Rebuild the heading tree of pi-5's first chapter, `### Soḷasamahāvāro ^5-1-0`.

The chapter holds the 16 vāras of the Bhikkhuvibhaṅga, then `Bhikkhunīvibhaṅgo`
and the 16 vāras of the Bhikkhunīvibhaṅga. The converted file got this wrong in
three ways (see pi-5-verification.md §2b–d):
  - `Bhikkhunīvibhaṅgo` was an empty child of `8. Samuccayavāro`;
  - bhikkhunī vāras 3–8 and the 8 paccayavāras sat under `2. Katāpattivāro`;
  - vaggas were siblings of their kaṇḍa.

Every heading in the chapter is classified by its title and re-parented:
  vāra (…vāro)            -> child of the chapter (bhikkhu part) or of Bhikkhunīvibhaṅgo
  Bhikkhunīvibhaṅgo       -> child of the chapter
  kaṇḍa (…kaṇḍa…)         -> child of the last vāra
  vagga (…vagg…)          -> child of the last kaṇḍa
Heading IDs are then renumbered from the tree. Headings deeper than ###### get
their title wrapped in **bold** (4-SYSTEM/CLAUDE.md §5a). Line order, text and
paragraph IDs are not touched; the script asserts that before writing.

usage: python restructure_pi5_solasa.py <pi-5.md> [--write]
"""
import re, sys
sys.stdout.reconfigure(encoding="utf-8")
path = sys.argv[1]
WRITE = "--write" in sys.argv
HEAD = re.compile(r"^(#+)\s+(.*?)\s+\^([\w-]+)\s*$")

raw = open(path, "rb").read().decode("utf-8")
nl = "\r\n" if "\r\n" in raw else "\n"
L = raw.split(nl)
plain = lambda t: re.sub(r"^\*\*(.*)\*\*$", r"\1", t)

ch = next(i for i, l in enumerate(L) if (m := HEAD.match(l)) and m.group(3) == "5-1-0")
ch_depth = len(HEAD.match(L[ch]).group(1))

class Node:
    def __init__(self, line, title, parent):
        self.line, self.title, self.parent, self.kids = line, title, parent, []
        if parent: parent.kids.append(self)
root = Node(ch, "Soḷasamahāvāro", None)
group = root; last_vara = last_kanda = None; nodes = []
for i in range(ch + 1, len(L)):
    m = HEAD.match(L[i])
    if not m:
        continue
    if len(m.group(1)) <= ch_depth:
        break
    t = plain(m.group(2))
    if t == "Bhikkhunīvibhaṅgo":
        n = Node(i, t, root); group = n; last_vara = last_kanda = None
    elif t.endswith("vāro"):
        n = Node(i, t, group); last_vara, last_kanda = n, None
    elif "kaṇḍ" in t:
        n = Node(i, t, last_vara); last_kanda = n
    elif "vagg" in t:
        n = Node(i, t, last_kanda)
    else:
        raise SystemExit(f"unclassified heading at line {i + 1}: {t}")
    nodes.append(n)

def assign(n, prefix, depth):
    n.id, n.depth = prefix + "-0", depth
    for k, c in enumerate(n.kids, 1):
        assign(c, f"{prefix}-{k}", depth + 1)
assign(root, "5-1", ch_depth)

changes = 0
for n in nodes:
    title = f"**{n.title}**" if n.depth > 6 else n.title
    new = f"{'#' * n.depth} {title} ^{n.id}"
    if new != L[n.line]:
        changes += 1
        L[n.line] = new

before = [l for l in raw.split(nl) if not HEAD.match(l)]
after = [l for l in L if not HEAD.match(l)]
assert before == after, "non-heading lines changed"

def show(n, ind=0):
    if n.kids and all("vagg" in k.title for k in n.kids):
        print("  " * ind + f"{n.title}  ^{n.id}   [+ {len(n.kids)} vaggas ^{n.kids[0].id} … ^{n.kids[-1].id}]")
        return
    print("  " * ind + f"{n.title}  ^{n.id}" + ("" if n is root else f"   (line {n.line + 1})"))
    for c in n.kids:
        show(c, ind + 1)
show(root)
print(f"\nheadings in chapter: {len(nodes)}; changed: {changes}; deepest level: {max(n.depth for n in nodes)} '#'; non-heading lines unchanged: True")
if WRITE:
    open(path, "wb").write(nl.join(L).encode("utf-8"))
    print("written:", path)
else:
    print("dry run; pass --write to save")
