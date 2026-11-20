"""Remove spaces that the XML->md conversion inserted where a <pb/> page-break
tag sat between a word and its punctuation (word<pb/>. -> "word ." -> "word.").

Only a space the source does not have is removed: every vault line is paired
with its XML line (same order, verified by compare_vin.py) and the space is
dropped only where the XML, with <pb> deleted and nothing put in its place,
has no space before that punctuation mark. Genuine source spaces stay.

usage: python fix_pb_spaces.py <vault.md> <xml1> [xml2 ...] [--write]
"""
import re, sys, difflib
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding="utf-8")
args = [a for a in sys.argv[1:] if a != "--write"]
WRITE = "--write" in sys.argv
md_path, xml_paths = args[0], args[1:]
PUNCT = set(".,;:!?…")

def inner(el):
    s = el.text or ""
    for ch in el:
        if ch.tag == "note":
            s += "{" + inner(ch).strip() + "}"
        elif ch.tag != "pb":
            s += inner(ch)
        s += ch.tail or ""
    return s

xml_lines = []
pending = [""]   # a <p rend="hangnum"> (bare paragraph number) is merged into the next line, as the vault does
def walk(el):
    for ch in el:
        if ch.tag == "div":
            walk(ch)
        elif ch.tag in ("head", "p", "trailer"):
            if ch.tag == "head" or ch.get("rend") in ("title", "subhead", "nikaya"):
                # a note inside a heading is emitted by the vault as its own block after the heading
                notes = [n for n in ch if n.tag == "note"]
                if notes:
                    h = (ch.text or "") + "".join((inner(c) if c.tag not in ("note", "pb") else "") + (c.tail or "") for c in ch)
                    xml_lines.append(re.sub(r"\s+", " ", h).strip())
                    for n in notes:
                        xml_lines.append(re.sub(r"\s+", " ", "{" + inner(n).strip() + "}").replace("‘‘", '"').replace("’’", '"'))
                    continue
            t = inner(ch).replace("‘‘", '"').replace("’’", '"')
            t = re.sub(r"\s+", " ", t).strip()
            t = re.sub(r"^(\d+(?:-\d+)?) \.", r"\1.", t)   # "199 ." markup quirk -> "199." as in the vault
            if ch.get("rend") == "hangnum":
                pending[0] = t + " "
                continue
            if not t:   # empty <p> (e.g. <p rend="centre"> </p>): the vault has no line for it
                continue
            xml_lines.append(pending[0] + t)
            pending[0] = ""
        else:
            walk(ch)
for xp in xml_paths:
    walk(ET.parse(xp).getroot().find(".//body"))

raw = open(md_path, "rb").read().decode("utf-8")
nl = "\r\n" if "\r\n" in raw else "\n"
lines = raw.split(nl)

# locate content lines (skip frontmatter and blank lines), strip heading marks and block IDs
fm_end = 0
if lines[0] == "---":
    fm_end = lines.index("---", 1) + 1
TRANSCLUSION = re.compile(r"^!\[\[[^\]]+\]\]\s*$")   # root-verse embeds added to commentaries; not in the XML
content_idx = [i for i in range(fm_end, len(lines)) if lines[i].strip() and not TRANSCLUSION.match(lines[i])]
assert len(content_idx) == len(xml_lines), (len(content_idx), len(xml_lines))

def split_line(s):
    m = re.match(r"^(#+\s+)?(.*?)(\s+\^[\w-]+)?$", s)
    return m.group(1) or "", m.group(2), m.group(3) or ""

changed_lines, removed, skipped = 0, 0, []
for k, i in enumerate(content_idx):
    pre, body, suf = split_line(lines[i])
    src = xml_lines[k]
    if body == src:
        continue
    if pre and re.sub(r"^\*\*(.*)\*\*$", r"\1", body) == src:
        continue   # heading deeper than ###### with its **bold** wrap (CLAUDE.md §5a)
    sm = difflib.SequenceMatcher(None, src, body, autojunk=False)
    out, ok, n = [], True, 0
    for op, a1, a2, b1, b2 in sm.get_opcodes():
        seg = body[b1:b2]
        if op == "equal":
            out.append(seg)
        elif op == "insert" and seg.strip() == "" and b2 < len(body) and body[b2] in PUNCT:
            n += 1          # conversion-inserted space before punctuation: drop it
        else:
            ok = False
            out.append(seg)
    if not ok:
        skipped.append((i + 1, lines[i][:120]))
        continue
    if n:
        lines[i] = pre + "".join(out) + suf
        changed_lines += 1
        removed += n

print(f"lines changed: {changed_lines}; spaces removed: {removed}; lines with other differences (left untouched): {len(skipped)}")
for ln, s in skipped[:20]:
    print(f"  untouched line {ln}: {s!r}")
if WRITE:
    open(md_path, "wb").write(nl.join(lines).encode("utf-8"))
    print("written:", md_path)
else:
    print("dry run; pass --write to save")
