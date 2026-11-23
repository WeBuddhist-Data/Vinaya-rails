"""Compare a vault root-text .md against its CST tipitaka-xml source(s).

usage: python compare_vin.py <vault.md> <out_report.md> <xml1> [xml2 ...]

Content: every XML <p>/<trailer> is one line; every vault line is one line.
The two line streams are diffed in order, so text moved across block
boundaries is not a difference, but changed, missing, extra or re-broken
lines are.
"""
import re, sys, difflib
import xml.etree.ElementTree as ET

md_path, out_path, xml_paths = sys.argv[1], sys.argv[2], sys.argv[3:]

# ---------------------------------------------------------------- XML side
def inner(el):
    s = el.text or ""
    for ch in el:
        if ch.tag == "note":
            s += "{" + inner(ch) + "}"
        elif ch.tag != "pb":
            s += inner(ch)
        s += ch.tail or ""
    return s

xml_heads = []   # (level, rend, text, file)
xml_lines = []   # (kind, text, file, rend)
paranums = []

def walk(el, depth, fname):
    for ch in el:
        if ch.tag == "div":
            walk(ch, depth + 1, fname)
        elif ch.tag == "head":
            t = inner(ch).strip()
            xml_heads.append((depth, ch.get("rend"), t, fname))
            xml_lines.append(("H", t, fname, ch.get("rend")))
        elif ch.tag in ("p", "trailer"):
            rend = ch.get("rend")
            t = inner(ch).strip()
            if ch.tag == "p" and rend in ("nikaya", "title", "subhead"):
                lvl = {"nikaya": 0, "title": depth + 1, "subhead": depth + 2}[rend]
                xml_heads.append((lvl, rend, t, fname))
                xml_lines.append(("H", t, fname, rend))
            else:
                if ch.find("hi[@rend='paranum']") is not None:
                    paranums.append(ch.find("hi[@rend='paranum']").text)
                xml_lines.append(("P", t, fname, rend))
        else:
            walk(ch, depth, fname)

for xp in xml_paths:
    root = ET.parse(xp).getroot()
    walk(root.find(".//body"), 0, xp.split("\\")[-1])

# ---------------------------------------------------------------- vault side
md_all = open(md_path, encoding="utf-8").read()
fm = re.match(r"\A---\n.*?\n---\n", md_all, flags=re.S)
offset = md_all[:fm.end()].count("\n") if fm else 0
md = md_all[fm.end():] if fm else md_all

vault_heads = []   # (level, text, id, lineno)
vault_lines = []   # (kind, text, lineno, blockid)
id_problems = []
blocks = []        # (bid, first_line, text)
lineno = offset + 1
for raw in re.split(r"(\n\s*\n)", md):
    if not raw.strip():
        lineno += raw.count("\n"); continue
    b = raw.strip("\n")
    lead = len(raw) - len(raw.lstrip("\n"))
    start = lineno + lead
    m = re.match(r"^(#+)\s+(.*?)\s*(\^[\w-]+)?\s*$", b)
    if m and "\n" not in b:
        htext = re.sub(r"^\*\*(.*)\*\*$", r"\1", m.group(2))   # headings deeper than ###### carry **bold** (CLAUDE.md §5a)
        vault_heads.append((len(m.group(1)) - 1, htext, m.group(3) or "", start))
        vault_lines.append(("H", htext, start, m.group(3) or ""))
    else:
        mid = re.search(r"\s*\^([\w-]+)\s*$", b)
        bid = mid.group(1) if mid else None
        text = b[:mid.start()] if mid else b
        if bid is None:
            id_problems.append(f"line {start}: block without block ID: {b[:80]!r}")
        mn = re.match(r"^(\d+(?:-\d+)?)\.\s", text)
        if bid and mn and bid.split("-")[-1] != mn.group(1).split("-")[0]:
            id_problems.append(f"line {start}: ^{bid} but paragraph number {mn.group(1)}")
        blocks.append((bid, start, text))
        for i, ln in enumerate(text.split("\n")):
            vault_lines.append(("P", ln, start + i, bid))
    lineno += raw.count("\n")

# duplicate ids
seen = {}
for bid, ln, _ in blocks:
    if bid in seen:
        id_problems.append(f"line {ln}: duplicate block ID ^{bid} (first at line {seen[bid]})")
    seen[bid] = ln
for lvl, t, hid, ln in vault_heads:
    if hid and hid[1:] in seen:
        id_problems.append(f"line {ln}: heading ID {hid} also used by a block")

# ---------------------------------------------------------------- normalise
def norm(s, xml):
    if xml:
        s = s.replace("‘‘", '"').replace("’’", '"')
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([.,;:!?…])", r"\1", s)
    return s

def strict(s, xml):
    if xml:
        s = s.replace("‘‘", '"').replace("’’", '"')
    return re.sub(r"\s+", " ", s).strip()

xa = [norm(t, True) for k, t, f, r in xml_lines]
va = [norm(t, False) for k, t, ln, b in vault_lines]

out = []
P = out.append
P(f"# Comparison report: `{md_path.split(chr(92))[-1]}`\n")
P("Sources: " + ", ".join(p.split("\\")[-1] for p in xml_paths) + "\n")

P("## 1. Counts\n")
P(f"- XML: {len(xml_lines)} lines ({len(xml_heads)} headings, {len(paranums)} numbered paragraphs, first ¶{paranums[0] if paranums else '-'}, last ¶{paranums[-1] if paranums else '-'})")
P(f"- Vault: {len(vault_lines)} lines ({len(vault_heads)} headings, {len(blocks)} blocks)")
num_blocks = [b for b in blocks if re.match(r"^\d", b[2])]
unnum = [b for b in blocks if not re.match(r"^\d", b[2])]
P(f"- Vault blocks starting with a paragraph number: {len(num_blocks)}; other blocks: {len(unnum)} → " + ", ".join(f"^{b[0]} (line {b[1]})" for b in unnum))
P("")

P("## 2. Block ID problems\n")
P("\n".join("- " + p for p in id_problems) if id_problems else "- none")
P("")

sm = difflib.SequenceMatcher(None, xa, va, autojunk=False)
diffs = [op for op in sm.get_opcodes() if op[0] != "equal"]
eq_lines = sum(i2 - i1 for t, i1, i2, j1, j2 in sm.get_opcodes() if t == "equal")
space_only = sum(1 for t, i1, i2, j1, j2 in sm.get_opcodes() if t == "equal"
                 for d in range(i2 - i1)
                 if strict(xml_lines[i1 + d][1], True) != strict(vault_lines[j1 + d][1], False))

P("## 3. Content (line by line, after ‘‘/’’ → \" and whitespace-before-punctuation normalisation)\n")
P(f"- Identical lines: {eq_lines} of {len(xa)} XML / {len(va)} vault")
P(f"- Lines identical except spacing before punctuation: {space_only}")
P(f"- Difference hunks: {len(diffs)}\n")
for t, i1, i2, j1, j2 in diffs:
    vl = vault_lines[j1][2] if j1 < len(vault_lines) else vault_lines[-1][2]
    P(f"### {t} — vault line {vl}")
    if t == "replace" and (i2 - i1) == (j2 - j1):
        for d in range(i2 - i1):
            aw, bw = xa[i1 + d].split(" "), va[j1 + d].split(" ")
            s2 = difflib.SequenceMatcher(None, aw, bw, autojunk=False)
            for tt, a1, a2, b1, b2 in s2.get_opcodes():
                if tt != "equal":
                    P(f"- line {vault_lines[j1+d][2]}: {tt}: XML `{' '.join(aw[max(0,a1-2):a2+2])}` → vault `{' '.join(bw[max(0,b1-2):b2+2])}`")
    else:
        for i in range(i1, i2):
            P(f"- XML  [{xml_lines[i][0]}/{xml_lines[i][3]}]: `{xa[i][:220]}`")
        for j in range(j1, j2):
            P(f"- vault line {vault_lines[j][2]} [{vault_lines[j][0]}]: `{va[j][:220]}`")
    P("")

# ---------------------------------------------------------------- headings
P("## 4. Headings (XML structural level vs vault level)\n")
P("XML level: nikaya=0, div head = div depth, `title` = depth+1, `subhead` = depth+2. Vault level = number of `#` − 1.\n")
xh = [norm(t, True) for l, r, t, f in xml_heads]
vh = [norm(t, False) for l, t, i, ln in vault_heads]
hm = difflib.SequenceMatcher(None, xh, vh, autojunk=False)
lvl_mis, txt_mis = [], []
for t, i1, i2, j1, j2 in hm.get_opcodes():
    if t == "equal":
        for d in range(i2 - i1):
            if xml_heads[i1 + d][0] != vault_heads[j1 + d][0]:
                lvl_mis.append((xml_heads[i1 + d], vault_heads[j1 + d]))
    else:
        txt_mis.append((t, xml_heads[i1:i2], vault_heads[j1:j2]))
P(f"- XML headings: {len(xh)}; vault headings: {len(vh)}")
P(f"- Text mismatches: {len(txt_mis)}")
for t, a, b in txt_mis:
    P(f"  - {t}: XML {[(h[0], h[1], h[2]) for h in a]} → vault {[(h[0], h[1], h[2], 'line '+str(h[3])) for h in b]}")
P(f"- Level mismatches: {len(lvl_mis)}")
for xhd, vhd in lvl_mis:
    P(f"  - line {vhd[3]}: `{vhd[1]}` {vhd[2]}: XML level {xhd[0]} ({xhd[1]}), vault level {vhd[0]}")
P("")

P("## 5. Heading block-ID consistency\n")
bad = []
for lvl, t, hid, ln in vault_heads:
    if not hid:
        bad.append(f"line {ln}: `{t}` has no block ID"); continue
    segs = hid[1:].split("-")
    if hid == "^0":
        continue
    if segs[-1] != "0":
        bad.append(f"line {ln}: `{t}` {hid} does not end in -0")
    if len(segs) - 1 != lvl:
        bad.append(f"line {ln}: `{t}` {hid} path length {len(segs)-1} ≠ heading level {lvl}")
P("\n".join("- " + b for b in bad) if bad else "- all heading IDs agree with heading depth")
P("")

# ---------------------------------------------------------------- semantic hierarchy hints
P("## 6. Hierarchy hints (numbering restarts among siblings)\n")
hints = []
prev_by_level = {}
for idx, (lvl, t, hid, ln) in enumerate(vault_heads):
    m = re.match(r"^(\d+)\.", t)
    for k in list(prev_by_level):
        if k > lvl:
            del prev_by_level[k]
    if m:
        n = int(m.group(1))
        p = prev_by_level.get(lvl)
        if p is not None and n <= p[0]:
            hints.append(f"line {ln}: `{t}` {hid} restarts numbering at level {lvl} (previous sibling `{p[1]}`) — likely belongs one level deeper")
        prev_by_level[lvl] = (n, t)
    else:
        prev_by_level.pop(lvl, None)
P("\n".join("- " + h for h in hints) if hints else "- none")
P("")

P("## 7. Vault outline\n")
P("```")
for lvl, t, hid, ln in vault_heads:
    P("  " * lvl + f"{t}  {hid}   (line {ln})")
P("```")

open(out_path, "w", encoding="utf-8").write("\n".join(out))
print(f"xmlLines={len(xa)} vaultLines={len(va)} equal={eq_lines} spaceOnly={space_only} hunks={len(diffs)} "
      f"headsX={len(xh)} headsV={len(vh)} headTxtMis={len(txt_mis)} headLvlMis={len(lvl_mis)} "
      f"idProblems={len(id_problems)} headIdBad={len(bad)} hierarchyHints={len(hints)} unnumberedBlocks={len(unnum)}")
