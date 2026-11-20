"""Pārājika Vajirabuddhi: make each kaṇḍa the parent of its own rules.

Before (XML ranks followed): kaṇḍas 2–4 and all their rules sit inside
`4. Catutthapārājikaṃ`; `1. Pārājikakaṇḍo` is empty, its 4 pārājikas are its
siblings; the Nissaggiya vaggas are siblings of the 4 pārājikas.
After, under `### Pārājikavaṇṇanā ^1-7-0`:
  #### Verañjakaṇḍo         -> its 5 sections (Verañjakaṇḍavaṇṇanā … Upāsakatta…)
  #### 1. Pārājikakaṇḍo     -> the 4 pārājikas (each with its own sections)
  #### 2. Saṅghādisesakaṇḍo -> its 13 rules
  #### 3. Aniyatakaṇḍo      -> its 2 rules
  #### 4. Nissaggiyakaṇḍo   -> the 3 vaggas -> their rules
`Nigamanavaṇṇanā` stays under the 4th pārājika: the text itself closes it with
"Catutthapārājikavaṇṇanā niṭṭhitā." before "Pārājikakaṇḍavaṇṇanā niṭṭhitā.".

usage: python fix_parajika_vajirabuddhi.py <file.md> [--write]
"""
import sys
sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else __file__.rsplit("/", 1)[0])
from heading_tree import Tree
sys.stdout.reconfigure(encoding="utf-8")
T = Tree(sys.argv[1])
ch = T.by_id("1-7-0")
kids = list(ch.kids)
K1 = next(n for n in kids if n.title == "1. Pārājikakaṇḍo")
V = next(n for n in kids if n.title == "Verañjakaṇḍo")      # the Verañja sections belong to it too
for n in kids[kids.index(V) + 1:kids.index(K1)]:
    n.move_to(V)
P = [n for n in kids if n.title.endswith("pārājikaṃ")]
assert len(P) == 4
for p in P:
    p.move_to(K1)
P4 = P[3]
cur = None
for n in list(P4.kids):
    if n.title.endswith("kaṇḍo"):
        n.move_to(ch); cur = n
    elif cur is not None:
        n.move_to(cur)
K4 = cur
assert K4.title == "4. Nissaggiyakaṇḍo"
for v in [n for n in ch.kids if n.title.endswith("vaggo")]:
    v.move_to(K4)

changes = T.apply(ch, write="--write" in sys.argv)
coll = lambda n: n.title.endswith(("pārājikaṃ", "vaggo")) or (n.title.endswith("kaṇḍo") and not n.title.startswith("4."))
print("\n".join(T.outline(ch, coll)))
print(f"\nheadings changed: {len(changes)}; deepest: {max(n.new_depth for n in T.renumber(ch))} '#'; non-heading lines unchanged: True")
print("written" if "--write" in sys.argv else "dry run; pass --write to save")
