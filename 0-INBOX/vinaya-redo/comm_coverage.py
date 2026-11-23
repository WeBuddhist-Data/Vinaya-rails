"""Completeness of the Vinaya commentaries: does each CSCD commentary XML end up in the vault
in full, with nothing dropped (also at the joins where one XML file was cut into several
vault files) and nothing added?

For each layer, the XML file(s) are read in order and the vault files cut from them are read
in book order; the two line streams are aligned. Normalisation is the one compare_vin.py uses
(notes as { }, ‘‘ ’’ → ", spaces collapsed, no space before punctuation), plus: a `hangnum`
line (a bare paragraph number) is joined to the line after it, as the vault does; vault
transclusion lines are skipped; heading markers and **bold** around headings are dropped.

usage: python comm_coverage.py            (from the vault root)
"""
import re, sys, difflib
import xml.etree.ElementTree as ET
sys.stdout.reconfigure(encoding="utf-8")
X = r"D:\Work\OpenPecha\tipitaka-xml\romn"
C = "1-SOURCES/Commentaries"
BOOKS = ["parajika", "pacittiya", "mahavagga", "culavagga", "parivara"]
LAYERS = [
    ("atthakatha", ["vin01a.att"], ["parajika"]),
    ("atthakatha", ["vin02a1.att"], ["pacittiya"]),
    ("atthakatha", ["vin02a2.att"], ["mahavagga"]),
    ("atthakatha", ["vin02a3.att"], ["culavagga"]),
    ("atthakatha", ["vin02a4.att"], ["parivara"]),
    ("saratthadipani", ["vin01t1.tik", "vin01t2.tik"], ["parajika"]),
    ("saratthadipani", ["vin02t.tik"], ["pacittiya", "mahavagga", "culavagga", "parivara"]),
    ("vajirabuddhi", ["vin06t.nrf"], BOOKS),
    ("vimativinodani", ["vin07t.nrf"], BOOKS),
    ("yojana", ["vin12t.nrf"], ["pacittiya", "mahavagga", "culavagga", "parivara"]),
]

def inner(el):
    s = el.text or ""
    for ch in el:
        if ch.tag == "note":
            s += "{" + inner(ch) + "}"
        elif ch.tag != "pb":
            s += inner(ch)
        s += ch.tail or ""
    return s

def norm(s):
    s = s.replace("‘‘", '"').replace("’’", '"')
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\{\s+", "{", s); s = re.sub(r"\s+\}", "}", s)
    return re.sub(r"\s+([.,;:!?…])", r"\1", s)

def xml_lines(stems):
    out = []
    for st in stems:
        body = ET.parse(f"{X}\\{st}.xml").getroot().find(".//body")
        pend = ""
        for el in body.iter():
            if el.tag in ("head", "p", "trailer"):
                t = norm(inner(el))
                if not t:
                    continue
                if el.get("rend") == "hangnum":
                    pend = t + " "; continue
                out.append((st, pend + t)); pend = ""
    return out

def vault_lines(path):
    raw = open(path, encoding="utf-8").read().replace("\r\n", "\n")
    raw = re.sub(r"\A---\n.*?\n---\n", "", raw, flags=re.S)
    out = []
    for n, l in enumerate(raw.split("\n"), 1):
        if not l.strip() or l.startswith("![[") or re.match(r"^\[\^[\w-]+\]:", l):
            continue
        l = re.sub(r"\s*\^[\w-]+\s*$", "", l)
        m = re.match(r"^#+\s+(.*)$", l)
        if m:
            l = re.sub(r"^\*\*(.*)\*\*$", r"\1", m.group(1))
        out.append((path.split("/")[-1], n, norm(l)))
    return out

total_missing = total_extra = 0
for layer, stems, books in LAYERS:
    xl = xml_lines(stems)
    vl = []
    for b in books:
        vl += vault_lines(f"{C}/pi-{b}-{layer}.md")
    sm = difflib.SequenceMatcher(None, [t for s, t in xl], [t for f, n, t in vl], autojunk=False)
    miss, extra = [], []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op in ("delete", "replace"):
            miss += [xl[i] for i in range(i1, i2)]
        if op in ("insert", "replace"):
            extra += [vl[j] for j in range(j1, j2)]
    total_missing += len(miss); total_extra += len(extra)
    print(f"{layer:15} {'+'.join(stems):24} -> {len(books)} file(s): XML {len(xl):,} lines, vault {len(vl):,}; "
          f"XML lines not in vault: {len(miss)}; vault lines not in XML: {len(extra)}")
    for s, t in miss[:6]:
        print(f"      missing [{s}] {t[:150]}")
    for f, n, t in extra[:6]:
        print(f"      extra   {f}:{n} {t[:150]}")
print(f"\nTOTAL: XML lines not in vault {total_missing}; vault lines not in XML {total_extra}")
