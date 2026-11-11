#!/usr/bin/env python3
"""Structural heading pass for Vinaya root/commentary drafts.

Runs after tipitaka_org_book.py (or the commentary converter) and before
heading IDs are assigned. The CST source marks some groupings at the same
level as the items they group; this pass nests them, using the printed
numbers kept in the JSON (the markdown headings have them stripped).

Rules
  1. Vagga headings (title ends in -vaggo/-vagga) that sit at the same level
     as their neighbours:
       - if the next non-vagga sibling is numbered 1  -> the vagga is a
         parent: demote following siblings (and their subtree) by one level
         until the next vagga or a heading at a higher level;
       - otherwise the vagga is a child of the preceding sibling: demote the
         vagga by one level.
  2. A mid-file book title (e.g. Bhikkhunīvibhaṅgo) stays at ### and every
     later heading is demoted by one level, nesting the following kaṇḍas.
  3. A synthetic '### Section N' placeholder (chapter with no chapter title)
     is replaced by its first child heading, promoted to ###.

Usage: vinaya_structure.py <draft.md> <source.json>
"""
import json
import re
import sys
from pathlib import Path

HEADING = re.compile(r"^(#+)\s+(.*?)(\s+\^\S+)?\s*$")
NUM = re.compile(r"^\s*(\d+)(?:-\d+)?\.\s*")
VAGGA = re.compile(r"vagg[oa]$")


def strip_num(t):
    return NUM.sub("", t).strip()


def main(md_path, json_path):
    p = Path(md_path)
    lines = p.read_text(encoding="utf-8").split("\n")
    data = json.loads(Path(json_path).read_text(encoding="utf-8"))
    segs = data["segments"]
    book_titles = [s["content"] for s in segs if s["css_class"] == "book"]
    json_heads = [s["content"] for s in segs
                  if s["css_class"] in ("chapter", "title", "subhead", "subsubhead")]
    # Map markdown headings (### and deeper) to printed numbers by order.
    heads = []  # [line_idx, level, text, num]
    j = 0
    for i, line in enumerate(lines):
        m = HEADING.match(line)
        if not m or len(m.group(1)) < 3:
            continue
        text = m.group(2)
        num = None
        if not re.match(r"^Section \d+$", text):
            while j < len(json_heads) and strip_num(json_heads[j]) != text:
                j += 1
            if j < len(json_heads):
                n = NUM.match(json_heads[j])
                num = int(n.group(1)) if n else None
                j += 1
        heads.append([i, len(m.group(1)), text, num])

    # Rule 3: synthetic Section placeholder.
    for k, h in enumerate(heads):
        if re.match(r"^Section \d+$", h[2]) and k + 1 < len(heads) and heads[k + 1][1] > h[1]:
            child = heads[k + 1]
            lines[h[0]] = None
            child[1] = h[1]
            h[1] = None
    heads = [h for h in heads if h[1] is not None]

    # Rule 2: mid-file book title.
    # Headings already nested under it (deeper than it) stay as they are;
    # from the next heading at its own level onwards everything is demoted
    # by one, so the following kaṇḍas become its children. Volume breaks
    # ("… (dutiyo bhāgo)") are not divisions and stay flat.
    mid_books = set(book_titles[1:]) | {
        strip_num(s["content"]) for s in segs if s.get("mid_book")}
    mid_books = {t for t in mid_books if "bhāgo" not in t}
    # The Bhikkhunīvibhaṅga heading groups the bhikkhunī kaṇḍas/vāras that
    # follow it wherever it appears (root, commentaries, Parivāra).
    is_mid = lambda t: t in mid_books or re.match(r"^Bhikkhun[iī]vibhaṅg", t)
    for k, h in enumerate(heads):
        if is_mid(h[2]):
            level = h[1]
            m = k + 1
            while m < len(heads) and heads[m][1] > level:
                m += 1
            # demote following siblings (and their subtrees) until the
            # parent section ends or another grouping heading starts
            while m < len(heads) and heads[m][1] >= level and not is_mid(heads[m][2]):
                heads[m][1] += 1
                m += 1

    # Rule 1: vaggas.
    k = 0
    while k < len(heads):
        h = heads[k]
        if VAGGA.search(h[2]):
            level = h[1]
            nxt = next((x for x in heads[k + 1:] if x[1] <= level), None)
            if nxt is not None and nxt[1] == level and not VAGGA.search(nxt[2]) and nxt[3] == 1:
                # parent: demote following siblings until next vagga/higher
                m = k + 1
                while m < len(heads) and heads[m][1] >= level:
                    if heads[m][1] == level and VAGGA.search(heads[m][2]):
                        break
                    heads[m][1] += 1
                    m += 1
                k = m
                continue
            # Otherwise the vagga belongs to the preceding same-level sibling
            # (e.g. Parivāra: "4. Nissaggiyakaṇḍaṃ", "1. Kathinavaggo", …,
            # "5. Pācittiyakaṇḍaṃ"): demote it and its own subtree.
            prev = next((x for x in reversed(heads[:k]) if x[1] <= level), None)
            if prev is not None and prev[1] == level:
                h[1] += 1
                m = k + 1
                while m < len(heads) and heads[m][1] > level:
                    heads[m][1] += 1
                    m += 1
        k += 1

    for i, level, text, _ in heads:
        title = f"**{text}**" if level > 6 and not text.startswith("**") else text
        lines[i] = f"{'#' * level} {title}"
    out = [l for l in lines if l is not None]
    p.write_text("\n".join(out), encoding="utf-8")
    print(f"{md_path}: {len(heads)} headings, deepest {max(h[1] for h in heads)}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
