"""pi-5: make `1. Bhikkhuvibhaṅgo` a heading, the sibling of `Bhikkhunīvibhaṅgo`
inside `Soḷasamahāvāro` (decided 2026-11-20).

Before:                                   After:
  ## Parivārapāḷi                           ## Parivārapāḷi
  1. Bhikkhuvibhaṅgo ^5-U1   (text line)    ### Soḷasamahāvāro ^5-1-0
  ### Soḷasamahāvāro ^5-1-0                 #### 1. Bhikkhuvibhaṅgo ^5-1-1-0
  #### 16 bhikkhu vāras                     ##### 16 bhikkhu vāras
  #### Bhikkhunīvibhaṅgo ^5-1-17-0          #### Bhikkhunīvibhaṅgo ^5-1-2-0
  ##### 16 bhikkhunī vāras                  ##### 16 bhikkhunī vāras

Evidence: the Vajirabuddhi closes the section "Mahāvibhaṅge ca bhikkhunivibhaṅge
soḷasamahāvāravaṇṇanā niṭṭhitā"; the XML chapter div vin5_1 (Soḷasamahāvāro)
holds both halves. The one line `1. Bhikkhuvibhaṅgo` moves below the chapter
heading (a tree cannot put a child before its parent); nothing else moves.

usage: python fix_pi5_bhikkhuvibhanga.py <pi-5.md> [--write]
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")
from heading_tree import Tree, HEAD

path = sys.argv[1]
raw = open(path, "rb").read().decode("utf-8")
nl = "\r\n"
old = f"1. Bhikkhuvibhaṅgo ^5-U1{nl}{nl}### Soḷasamahāvāro ^5-1-0{nl}"
new = f"### Soḷasamahāvāro ^5-1-0{nl}{nl}#### 1. Bhikkhuvibhaṅgo ^5-1-99-0{nl}"
assert raw.count(old) == 1, "expected block not found exactly once"
step1 = raw.replace(old, new)

tmp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp", "pi-5.bhikkhuvibhanga-step1.md")
open(tmp, "wb").write(step1.encode("utf-8"))

T = Tree(tmp)
S = T.by_id("5-1-0")
BV = next(n for n in S.kids if n.title == "1. Bhikkhuvibhaṅgo")
BN = next(n for n in S.kids if n.title == "Bhikkhunīvibhaṅgo")
vaaras = [n for n in S.kids if BV.line < n.line < BN.line]
assert len(vaaras) == 16, len(vaaras)
for v in vaaras:
    v.move_to(BV)
root = T.by_id("5-0")
changes = T.apply(root)

# the only non-heading change against the original: the U1 text line is gone
orig_body = [l for l in raw.split(nl) if not HEAD.match(l)]
new_body = [l for l in T.L if not HEAD.match(l)]
orig_body.remove("1. Bhikkhuvibhaṅgo ^5-U1")
assert orig_body == new_body, "non-heading lines changed"
assert len(raw.split(nl)) == len(T.L), "line count changed"

if "--write" in sys.argv:
    open(path, "wb").write(nl.join(T.L).encode("utf-8"))
os.remove(tmp)

coll = lambda n: n.new_depth >= 5
print("\n".join(T.outline(S, coll)))
deep = [n for n in T.renumber(root) if n.new_depth > 6]
print(f"\nheading lines changed: {len(changes)} (+1 line converted from text); "
      f"7-level (bold) headings: {len(deep)}; deepest: {max(n.new_depth for n in T.renumber(root))} '#'")
print("non-heading lines: unchanged except the removed `1. Bhikkhuvibhaṅgo ^5-U1`; line count unchanged")
print("written" if "--write" in sys.argv else "dry run; pass --write to save")
