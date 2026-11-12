#!/usr/bin/env python3
"""Give a built Vinaya file the printed form of its source (tipitaka-xml, as
tipitaka.app shows it).

The converters and the block-ID skills drop some of what the source prints, as
the Abhidhamma vault's format does. The Vinaya files keep the source's body and
structure, so this step, run last in the build, puts it back:

  1. printed numbers on headings      "Pārājikakaṇḍaṃ"       -> "1. Pārājikakaṇḍaṃ"
  2. printed numbers on root paragraphs "Tena samayena …"    -> "1. Tena samayena …"
     (the block ID stays ^1-1; the number is now in the text too)
  3. the piṭaka heading as printed    "Vinayapiṭake (ṭīkā)"  -> "Vinayapiṭake"
  4. variant-reading notes as on the site  "[… (sī.)]"       -> "{… (sī.)}"

Each heading and text line is matched, in order, to the JSON segment it was
built from (one line per segment), and the missing leading number is taken
from that segment verbatim. Block IDs, heading IDs, levels and transclusions
are untouched.

In the Vinaya XML every square bracket comes from a <note> element (vin02m2,
the Mahāvagga root, has one literal bracket: check it by hand when building
pi-3), so all brackets in text lines are notes.

Usage: source_form.py <file.md> <source.json>
"""
import difflib
import json
import re
import sys
from pathlib import Path

ID = re.compile(r"\s+\^([A-Za-z0-9-]+)\s*$")
HEAD = re.compile(r"^(#+)\s+(.*?)\s*$")
NUM = re.compile(r"^\s*(?:\d+(?:-\d+)*|\(\d+\))\.\s*")
LABEL = re.compile(r"^(Vinayapiṭake) \((?:aṭṭhakathā|ṭīkā)\)$")


def key(t):
    t = NUM.sub("", t.replace("**", "")).strip()
    t = LABEL.sub(r"\1", t)
    return re.sub(r"\s+", "", t).replace("{", "[").replace("}", "]")  # matching only


def braces(t):
    """A note's outer brackets become braces; brackets inside the note's own
    text stay, as the site shows them (pi-1: {[ ] etthantare pāṭhā …}).
    A <note> always closes in its own paragraph, so a '[' that is never
    closed on the line is the source's own bracket and stays as printed
    (pi-3, vin02m2: '… āgatā} [ Evaṃ vutte bhagavā …')."""
    out, i, notes = [], 0, 0
    while i < len(t):
        if t[i] == "[":
            depth, j = 0, i
            while j < len(t):
                depth += (t[j] == "[") - (t[j] == "]")
                if depth == 0:
                    break
                j += 1
            if j < len(t):          # closed on this line: a note
                out.append("{" + t[i + 1:j] + "}"); notes += 1; i = j + 1
                continue
        out.append(t[i]); i += 1
    return "".join(out), notes


def main(md_path, json_path):
    p = Path(md_path)
    text = p.read_text(encoding="utf-8")
    m = re.match(r"^---\n.*?\n---\n", text, re.S)
    head, body = (m.group(0), text[m.end():]) if m else ("", text)
    lines = body.split("\n")
    segs = [s["content"] for s in json.loads(Path(json_path).read_text(encoding="utf-8"))["segments"]]

    items = []  # (line index, is_heading, hashes, title/text, id)
    for i, ln in enumerate(lines):
        if not ln.strip() or ln.lstrip().startswith("![["):
            continue
        idm = ID.search(ln)
        core = ID.sub("", ln) if idm else ln
        h = HEAD.match(core)
        if h:
            items.append((i, True, h.group(1), h.group(2), idm.group(1) if idm else None))
        else:
            items.append((i, False, "", core, idm.group(1) if idm else None))

    sm = difflib.SequenceMatcher(None, [key(it[3]) for it in items], [key(s) for s in segs], autojunk=False)
    counts = {"heading numbers": 0, "paragraph numbers": 0, "piṭaka label": 0, "notes": 0}
    unmatched = []
    for op, a1, a2, b1, b2 in sm.get_opcodes():
        if op != "equal":
            unmatched += [items[a][3][:60] for a in range(a1, a2)]
            continue
        for a, b in zip(range(a1, a2), range(b1, b2)):
            i, is_head, hashes, t, bid = items[a]
            src = segs[b]
            bold = is_head and t.startswith("**") and t.endswith("**")
            bare = t[2:-2] if bold else t
            new = bare
            lm = LABEL.match(new)
            if is_head and lm:
                new = lm.group(1); counts["piṭaka label"] += 1
            sp = NUM.match(src)
            if sp and not NUM.match(new):
                new = src[:sp.end()] + new
                counts["heading numbers" if is_head else "paragraph numbers"] += 1
            new, n_notes = braces(new); counts["notes"] += n_notes
            if new == bare:
                continue
            new = f"**{new}**" if bold else new
            lines[i] = (f"{hashes} {new}" if is_head else new) + (f" ^{bid}" if bid else "")
    p.write_text(head + "\n".join(lines), encoding="utf-8")
    print(f"{p.name}: " + ", ".join(f"{k} {v}" for k, v in counts.items())
          + f"; lines not matched to the source: {len(unmatched)}")
    for u in unmatched[:10]:
        print("   not matched:", u)
    return 1 if unmatched else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
