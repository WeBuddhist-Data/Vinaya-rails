"""List spaces before punctuation that are present in the source XML itself
(and therefore stay in the vault), typed A/B/C/D.

usage: python kept_spaces.py <vault.md> <out.md> <xml1> [xml2 ...]
"""
import re, sys, collections
import xml.etree.ElementTree as ET
sys.stdout.reconfigure(encoding="utf-8")
md_path, out_path, xml_paths = sys.argv[1], sys.argv[2], sys.argv[3:]
PB = "¶"

def inner(el):
    s = el.text or ""
    for ch in el:
        if ch.tag == "note":
            s += "{" + inner(ch).strip() + "}"
        elif ch.tag == "pb":
            s += PB + ch.get("ed") + " " + ch.get("n") + PB
        else:
            s += inner(ch)
        s += ch.tail or ""
    return s

X, pending = [], [""]
def walk(el):
    for ch in el:
        if ch.tag == "div":
            walk(ch)
        elif ch.tag in ("head", "p", "trailer"):
            if ch.tag == "head" or ch.get("rend") in ("title", "subhead", "nikaya"):
                notes = [n for n in ch if n.tag == "note"]
                if notes:   # vault emits a heading's note as its own block after the heading
                    h = (ch.text or "") + "".join((inner(c) if c.tag not in ("note", "pb") else "") + (c.tail or "") for c in ch)
                    X.append(re.sub(r"\s+", " ", h).strip())
                    for n in notes:
                        X.append(re.sub(r"\s+", " ", "{" + inner(n).strip() + "}").replace("‘‘", '"').replace("’’", '"'))
                    continue
            t = re.sub(r"\s+", " ", inner(ch).replace("‘‘", '"').replace("’’", '"')).strip()
            t = re.sub(r"^(\d+(?:-\d+)?) \.", r"\1.", t)   # "199 ." markup quirk, normalised in the vault
            if ch.get("rend") == "hangnum":
                pending[0] = t + " "; continue
            if not t:   # empty <p>: no vault line
                continue
            X.append(pending[0] + t); pending[0] = ""
        else:
            walk(ch)
for xp in xml_paths:
    walk(ET.parse(xp).getroot().find(".//body"))

L = open(md_path, encoding="utf-8").read().split("\n")
fm = L.index("---", 1) + 1
idx = [i for i in range(fm, len(L)) if L[i].strip() and not re.match(r"^!\[\[[^\]]+\]\]\s*$", L[i])]
assert len(idx) == len(X), (len(idx), len(X))

rows = []
pat = re.compile(r"(\S)((?:\s*" + PB + "[^" + PB + "]+" + PB + r")*\s+(?:" + PB + "[^" + PB + "]+" + PB + r"\s*)*)([.,;:!?…])")
for k, raw in enumerate(X):
    for r in pat.finditer(raw):
        g = r.group(2)
        if " " not in g:
            continue
        if PB not in g:
            cat = "D"
        elif r.group(3) != "…":
            cat = "C"
        elif re.search(PB + r"\s+$", g):
            cat = "B"
        else:
            cat = "A"
        x = re.sub(PB + r"(\w) ([\d.]+)" + PB, r"<pb \1 \2/>", raw[max(0, r.start() - 30):r.end() + 10])
        rows.append((cat, idx[k] + 1, x))

name = md_path.replace("\\", "/").split("/")[-1]
cnt = collections.Counter(r[0] for r in rows)
print(name, dict(cnt))
for r in rows:
    if r[0] in "CD":
        print(f"  {r[0]} line {r[1]}: …{r[2]}…")
out = [f"# {name} — spaces before punctuation that are in the source (kept)", "",
       "Present in " + ", ".join("`" + p.replace("\\", "/").split("/")[-1] + "`" for p in xml_paths) +
       " itself; they stay in the vault (decision of 2026-11-13).", "",
       "- **A** `word <pb/>…` · **B** `word <pb/> …pe…` · **C** `word <pb/>,` / `.` · **D** plain source space", "",
       f"Counts: {dict(cnt)}", "",
       "| # | Type | Vault line | Source XML |", "|---|---|---|---|"]
for n, (c, ln, x) in enumerate(rows, 1):
    out.append(f"| {n} | {c} | [{ln}](../../1-SOURCES/Text/{name}:{ln}) | `…{x.replace('|', '/')}…` |")
open(out_path, "w", encoding="utf-8").write("\n".join(out) + "\n")
