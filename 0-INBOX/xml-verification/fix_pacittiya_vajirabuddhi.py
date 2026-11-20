"""Pācittiya Vajirabuddhi: undo the XML's upside-down ranks (vagga above kaṇḍa).

After, under `## Pācittiyavaṇṇanā ^2-0` (same shape as pi-2 and the aṭṭhakathā):
  ### 5. Pācittiyakaṇḍo             -> its 9 vaggas -> their rules
  ### 6. Pāṭidesanīyakaṇḍo          -> its 2 rules
  ### 7. Sekhiyakaṇḍo               -> its 7 vaggas + Pakiṇṇakavaṇṇanā
  ### 8. Sattādhikaraṇasamathavaṇṇanā
  ### Bhikkhunīvibhaṅgavaṇṇanā
  #### 1. Pārājikakaṇḍavaṇṇanā       -> Ganthārambhavaṇṇanā + the 4 pārājikas
  #### 2. Saṅghādisesakaṇḍavaṇṇanā   -> its rules
  #### 3. Nissaggiyakaṇḍavaṇṇanā     -> its rules
  #### 4. Pācittiyakaṇḍavaṇṇanā      -> its 9 vaggas -> their rules, + Nigamanavaṇṇanā
Placement follows the text's own closing lines, e.g. Pakiṇṇakavaṇṇanā closes after
"Pādukavaggavaṇṇanā niṭṭhitā." and before "Sekhiyakaṇḍavaṇṇanā niṭṭhitā.", and
Nigamanavaṇṇanā after "Chattupāhanavaggavaṇṇanā niṭṭhitā." and before
"Pācittiyakaṇḍavaṇṇanā niṭṭhitā.". `Ganthārambhavaṇṇanā` comes after the
`1. Pārājikakaṇḍavaṇṇanā` title in the text, so it becomes that kaṇḍa's first section.

usage: python fix_pacittiya_vajirabuddhi.py <file.md> [--write]
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from heading_tree import Tree
sys.stdout.reconfigure(encoding="utf-8")
T = Tree(sys.argv[1])
root = T.by_id("2-0")
iskanda = lambda n: "kaṇḍ" in n.title and n.title[0].isdigit() or n.title.startswith("8. Sattādhikaraṇa")
isvagga = lambda n: "vagg" in n.title

# ---- bhikkhu part
K5 = next(n for n in root.kids if n.title == "5. Pācittiyakaṇḍo")
for v in [n for n in root.kids if isvagga(n)]:
    v.move_to(K5)
ratana = K5.kids[-1]
cur = None
for n in list(ratana.kids):
    if iskanda(n):
        n.move_to(root); cur = n
    elif cur is not None:
        n.move_to(cur)
sekhiya = next(n for n in root.kids if n.title == "7. Sekhiyakaṇḍo")
paduka = sekhiya.kids[-1]
for n in [k for k in paduka.kids if k.title == "Pakiṇṇakavaṇṇanā"]:
    n.move_to(sekhiya)

# ---- bhikkhunī part
BV = next(n for n in root.kids if n.title == "Bhikkhunīvibhaṅgavaṇṇanā")
BK1 = next(n for n in BV.kids if n.title == "1. Pārājikakaṇḍavaṇṇanā")
gantha = next(n for n in BV.kids if n.title == "Ganthārambhavaṇṇanā")
gantha.move_to(BK1)
cur = BK1
for n in list(gantha.kids):
    if iskanda(n):
        n.move_to(BV); cur = n
    else:
        n.move_to(cur)
BK4 = cur
assert BK4.title == "4. Pācittiyakaṇḍavaṇṇanā", BK4
for v in [n for n in BV.kids if isvagga(n)]:
    v.move_to(BK4)
for n in [x for x in T.nodes if x.title == "Nigamanavaṇṇanā" and x.line > BK4.line]:
    n.move_to(BK4)

changes = T.apply(root, write="--write" in sys.argv)
coll = lambda n: isvagga(n) or (iskanda(n) and n.title[0] in "1236" ) or n.title == "Ganthārambhavaṇṇanā"
print("\n".join(T.outline(root, coll)))
print(f"\nheadings changed: {len(changes)}; deepest: {max(n.new_depth for n in T.renumber(root))} '#'; non-heading lines unchanged: True")
print("written" if "--write" in sys.argv else "dry run; pass --write to save")
