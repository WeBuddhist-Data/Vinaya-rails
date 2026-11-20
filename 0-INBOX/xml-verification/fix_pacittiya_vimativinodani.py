"""Pācittiya Vimativinodanī: make `Bhikkhunīvibhaṅgavaṇṇanā` the parent of the
five bhikkhunī kaṇḍas.

Before: an empty `#### Bhikkhunīvibhaṅgavaṇṇanā ^2-3-8-0` inside `7. Sekhiyakaṇḍaṃ`,
with the bhikkhunī kaṇḍas as `###` siblings of the bhikkhu ones.
After:  `### Bhikkhunīvibhaṅgavaṇṇanā ^2-4-0` (same rank as the kaṇḍas, as in the XML)
holding `#### 1. Pārājikakaṇḍaṃ` … `#### 5. Pāṭidesanīyakaṇḍaṃ`, the same shape as
pi-2 and the other Pācittiya commentaries.

usage: python fix_pacittiya_vimativinodani.py <file.md> [--write]
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from heading_tree import Tree
sys.stdout.reconfigure(encoding="utf-8")
T = Tree(sys.argv[1])
root = T.by_id("2-0")
BV = next(n for n in T.nodes if n.title == "Bhikkhunīvibhaṅgavaṇṇanā")
BV.move_to(root)
for k in [n for n in root.kids if n.line > BV.line]:
    k.move_to(BV)

changes = T.apply(root, write="--write" in sys.argv)
coll = lambda n: n.new_depth >= 4 and n.kids
print("\n".join(T.outline(root, coll)))
print(f"\nheadings changed: {len(changes)}; deepest: {max(n.new_depth for n in T.renumber(root))} '#'; non-heading lines unchanged: True")
print("written" if "--write" in sys.argv else "dry run; pass --write to save")
