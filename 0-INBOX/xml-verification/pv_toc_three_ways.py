"""Print the Parivāra chapter-1 heading tree three ways: tipitaka.app's contents
tree, the tipitaka-xml source, and the vault (pi-5.md). Down to vāra level;
kaṇḍas and vaggas are counted, not listed.  usage: python pv_toc_three_ways.py
"""
import re, sys, json
import xml.etree.ElementTree as ET
sys.stdout.reconfigure(encoding="utf-8")
KEEP = re.compile(r"vār|vibhaṅg|Soḷasa|Samuṭṭhānasīsa|Parivār", re.I)
SKIP = re.compile(r"kaṇḍ|vagg", re.I)
STOP = "Antarapeyyālaṃ"

def show(rows):
    """rows: (level, label). Print kept rows; count the skipped ones under each."""
    out, hidden = [], 0
    for lvl, label in rows + [(0, None)]:
        if label is None or (KEEP.search(label) and not SKIP.search(label)):
            if hidden and out:
                out[-1] += f"   (+{hidden} kaṇḍa/vagga headings)"
            hidden = 0
            if label:
                out.append("    " * lvl + label)
        else:
            hidden += 1
    print("\n".join(out))

# 1. website contents tree
site = json.load(open("0-INBOX/tipitaka-app/vp-pv.json", encoding="utf-8"))
rows, base = [], min(n["depth"] for n in site)
for n in site:
    if n["title"] == STOP: break
    rows.append((n["depth"] - base + 1, f"{n['title']}   [{n['key']}]"))
print("=== 1. tipitaka.app contents tree (vp-pv)\nParivārapāḷi   [book root]")
show(rows)

# 2. tipitaka-xml
root = ET.parse(r"D:\Work\OpenPecha\tipitaka-xml\romn\vin02m4.mul.xml").getroot()
rows = []
RANK = {"book": 0, "chapter": 1, "title": 2, "subhead": 3, "subsubhead": 4}
def walk(el, divs):
    for ch in el:
        if ch.tag == "div":
            if walk(ch, divs + [ch.get("id")]): return True
        elif (ch.tag == "head") or (ch.tag == "p" and ch.get("rend") in RANK):
            t = "".join(ch.itertext()).strip()
            if t == STOP: return True
            r = ch.get("rend")
            where = f"<{ch.tag} rend={r}> in div {divs[-1]}"
            lvl = RANK[r] if not (ch.tag == "head" and r == "title") else 1
            rows.append((lvl, f"{t}   [{where}]"))
        else:
            if walk(ch, divs): return True
walk(root.find(".//body"), ["body"])
print("\n=== 2. tipitaka-xml romn/vin02m4.mul.xml (indent = tag rank; the XML itself is flat inside the chapter div)")
show(rows)

# 3. vault
rows = []
for line in open("1-SOURCES/Text/pi-5.md", encoding="utf-8"):
    m = re.match(r"^(#+)\s+(.*?)\s*(\^[\w-]+)\s*$", line)
    if m:
        t = re.sub(r"^\*\*(.*)\*\*$", r"\1", m.group(2))
        if t == STOP: break
        if len(m.group(1)) >= 2:
            rows.append((len(m.group(1)) - 2, f"{t}   {m.group(3)}"))
    elif line.startswith("1. Bhikkhuvibhaṅgo"):
        rows.append((1, "(text line, not a heading) 1. Bhikkhuvibhaṅgo   ^5-U1"))
print("\n=== 3. vault pi-5.md now (my suggestion: keep this)")
show(rows)
