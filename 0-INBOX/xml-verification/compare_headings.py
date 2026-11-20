"""Check a commentary's heading tree against the CST XML.

The commentary XML marks headings as <head> (inside <div>s) or as
<p rend="nikaya|book|chapter|title|subhead|subsubhead">. Their ranks have gaps,
so instead of comparing absolute levels this script compares PARENTS: for each
heading, the expected parent is the nearest earlier XML heading of a higher rank
(smaller number); the actual parent is the nearest earlier vault heading with
fewer '#'. A mismatch means the vault nests that heading differently.

usage: python compare_headings.py <vault.md> <out.md> <xml1> [xml2 ...] [--from "heading"] [--to "heading"]
  --from/--to  restrict the XML to the stretch starting at the first heading
               with that exact text and ending before the --to heading
               (for files that hold several books' commentaries)
"""
import re, sys, difflib
import xml.etree.ElementTree as ET
sys.stdout.reconfigure(encoding="utf-8")

args, opts, i = [], {}, 1
while i < len(sys.argv):
    if sys.argv[i] in ("--from", "--to"):
        opts[sys.argv[i]] = sys.argv[i + 1]; i += 2
    else:
        args.append(sys.argv[i]); i += 1
md_path, out_path, xml_paths = args[0], args[1], args[2:]
P_RANK = {"nikaya": 0, "book": 1, "chapter": 2, "title": 3, "subhead": 4, "subsubhead": 5}
HEAD_RANK = {"book": 1, "chapter": 2, "title": 3}

def txt(el):
    s = el.text or ""
    for c in el:
        if c.tag not in ("note", "pb"):
            s += txt(c)
        s += c.tail or ""
    return re.sub(r"\s+", " ", s).strip()

X = []
def walk(el, depth):
    for ch in el:
        if ch.tag == "div":
            walk(ch, depth + 1)
        elif ch.tag == "head":
            X.append((HEAD_RANK.get(ch.get("rend"), depth), "head/" + str(ch.get("rend")), txt(ch)))
        elif ch.tag == "p" and ch.get("rend") in P_RANK:
            X.append((P_RANK[ch.get("rend")], ch.get("rend"), txt(ch)))
        elif ch.tag not in ("p", "trailer"):
            walk(ch, depth)
for xp in xml_paths:
    walk(ET.parse(xp).getroot().find(".//body"), 0)
if "--from" in opts:
    X = X[next(k for k, h in enumerate(X) if h[2] == opts["--from"]):]
if "--to" in opts:
    X = X[:next(k for k, h in enumerate(X) if h[2] == opts["--to"])]

L = open(md_path, encoding="utf-8").read().split("\n")
V, plain = [], {}
for n, line in enumerate(L, 1):
    m = re.match(r"^(#+)\s+(.*?)(?:\s+(\^[\w-]+))?\s*$", line)
    if m:
        t = re.sub(r"^\*\*(.*)\*\*$", r"\1", m.group(2))
        V.append((len(m.group(1)), t, m.group(3) or "", n))
    else:
        s = re.sub(r"\s+\^[\w-]+\s*$", "", line).strip()
        if s:
            plain.setdefault(s, n)

norm = lambda s: s.replace("‘‘", '"').replace("’’", '"')
sm = difflib.SequenceMatcher(None, [norm(h[2]) for h in X], [h[1] for h in V], autojunk=False)
pairs, only_x, only_v = [], [], []
for op, a1, a2, b1, b2 in sm.get_opcodes():
    if op == "equal":
        pairs += [(a1 + k, b1 + k) for k in range(a2 - a1)]
    else:
        only_x += list(range(a1, a2)); only_v += list(range(b1, b2))

def parents(levels):
    out, stack = [], []
    for lv in levels:
        while stack and stack[-1][0] >= lv:
            stack.pop()
        out.append(stack[-1][1] if stack else None)
        stack.append((lv, len(out) - 1))
    return out
px = parents([h[0] for h in X])
pv = parents([h[0] for h in V])
xi_of_v = {b: a for a, b in pairs}
bad = []
for a, b in pairs:
    exp = px[a]
    act = pv[b]
    act_x = xi_of_v.get(act) if act is not None else None
    if exp != act_x:
        bad.append((V[b], X[a], X[exp][2] if exp is not None else "—", V[act][1] if act is not None else "—"))

name = md_path.replace("\\", "/").split("/")[-1]
o = [f"# Heading check: `{name}`", "", "Sources: " + ", ".join(p.replace("\\", "/").split("/")[-1] for p in xml_paths), ""]
o += [f"- XML headings: {len(X)}; vault headings: {len(V)}; matched by text: {len(pairs)}", ""]
o += ["## XML headings with no vault heading", ""]
for a in only_x:
    where = plain.get(norm(X[a][2]))
    o.append(f"- `{X[a][2]}` ({X[a][1]})" + (f" → plain text at vault line {where}" if where else " → not found as a line"))
o += ["", "## Vault headings with no XML heading", ""]
o += [f"- line {V[b][3]}: `{V[b][1]}` {V[b][2]}" for b in only_v]
o += ["", f"## Parent mismatches ({len(bad)})", "",
      "| Vault line | Heading | ID | XML tag | Parent by XML | Parent in vault |", "|---|---|---|---|---|---|"]
for v, x, e, a in bad:
    o.append(f"| {v[3]} | {'#' * v[0]} {v[1]} | `{v[2]}` | {x[1]} | {e} | {a} |")
o += ["", "## Tag → vault depth", ""]
from collections import Counter
c = Counter((X[a][1], V[b][0]) for a, b in pairs)
o += [f"- {t} → {'#' * d}: {n}" for (t, d), n in sorted(c.items(), key=lambda z: (z[0][1], z[0][0]))]
open(out_path, "w", encoding="utf-8").write("\n".join(o) + "\n")
print(f"{name}: xmlHeads={len(X)} vaultHeads={len(V)} matched={len(pairs)} onlyXml={len(only_x)} onlyVault={len(only_v)} parentMismatch={len(bad)}")
