"""Pācittiya Yojanā: put the vaggas under their Pācittiya kaṇḍa.

The XML tags kaṇḍas and vaggas alike (`title`), so they came out as siblings.
After:
  ### Pācittiyayojanā
  #### 5. Pācittiyakaṇḍaṃ      -> the 1st vagga's rules (the yojanā has no
                                 "1. Musāvādavaggo" heading), then vaggas 2–9
  #### 6. Pāṭidesanīyakaṇḍaṃ, #### 7. Sekhiyakaṇḍaṃ   (unchanged)
  ### Bhikkhunīvibhaṅgo
  #### 1.–3. kaṇḍas            (unchanged)
  #### 4. Pācittiyakaṇḍaṃ      -> vaggas 1–9
  #### 5. Pāṭidesanīyasikkhāpada-atthayojanā   <- was inside the 9th vagga; the text
       closes the khuddaka part ("Bhikkhunivibhaṅge khuddakavaṇṇanāya / Yojanā
       samattā.") before it, so it is the 5th kaṇḍa.
  Also: bhikkhunī Andhakāravagga rule `5. Pañcamasikkhāpadaṃ` is tagged `subsubhead`
  in the XML (a tagging slip) and sat under rule 4; it becomes rule 5 again.

usage: python fix_pacittiya_yojana.py <file.md> [--write]
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from heading_tree import Tree
sys.stdout.reconfigure(encoding="utf-8")
T = Tree(sys.argv[1])
root = T.by_id("2-0")
isvagga = lambda n: "vagg" in n.title

PY = next(n for n in root.kids if n.title == "Pācittiyayojanā")
K5 = next(n for n in PY.kids if n.title == "5. Pācittiyakaṇḍaṃ")
for v in [n for n in PY.kids if isvagga(n)]:
    v.move_to(K5)

BV = next(n for n in root.kids if n.title == "Bhikkhunīvibhaṅgo")
BK4 = next(n for n in BV.kids if n.title == "4. Pācittiyakaṇḍaṃ")
for v in [n for n in BV.kids if isvagga(n)]:
    v.move_to(BK4)
pd = next(n for n in T.nodes if n.title.startswith("5. Pāṭidesanīyasikkhāpada"))
pd.move_to(BV)
# the XML tags this one rule `subsubhead` (all its siblings are `subhead`), so it
# landed under rule 4; it is rule 5 of the bhikkhunī Andhakāravagga
andh = next(n for n in BK4.kids if n.title == "2. Andhakāravaggo")
r5 = next(n for n in T.nodes if n.title == "5. Pañcamasikkhāpadaṃ" and n.parent.parent is andh)
r5.move_to(andh)

changes = T.apply(root, write="--write" in sys.argv)
coll = lambda n: isvagga(n) or (n.new_depth >= 4 and not isvagga(n) and n.kids and not any(isvagga(k) for k in n.kids))
print("\n".join(T.outline(root, coll)))
deep = [n for n in T.renumber(root) if n.new_depth > 6]
print(f"\nheadings changed: {len(changes)}; deepest: {max(n.new_depth for n in T.renumber(root))} '#'; non-heading lines unchanged: True")
for n in deep:
    print(f"  7th level (bold): {n.title} ^{n.new_id} (line {n.line + 1})")
print("written" if "--write" in sys.argv else "dry run; pass --write to save")
