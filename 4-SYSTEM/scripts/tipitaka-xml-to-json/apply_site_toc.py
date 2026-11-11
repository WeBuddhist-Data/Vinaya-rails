#!/usr/bin/env python3
"""Set a root text's heading levels from the tipitaka.app contents tree.

The Abhidhamma vault checked its root-text TOCs against tipitaka.app's
contents sidebar; this applies that reference directly. The vault's ###-and-
deeper headings and the site's nodes are aligned in order by title (leading
numbers ignored); each matched heading takes the site's depth as its '#'
count. Unmatched headings keep their level and are reported.

Run after the converter and before heading_ids.py (heading IDs are reassigned
from the new levels).

Usage: apply_site_toc.py <root.md> <site-toc.json>
"""
import difflib
import json
import re
import sys
from pathlib import Path

HEADING = re.compile(r"^(#{3,})\s+(.*?)(\s+\^\S+)?\s*$")
NUM = re.compile(r"^\s*\d+(?:-\d+)*\.\s*")


NOTE = re.compile(r"\s*(\[.*\])\s*$")


def norm(t):
    return NUM.sub("", t.replace("**", "")).strip()


def key(t):
    """Matching key: title without a trailing CST editorial note '[…]'."""
    return NOTE.sub("", norm(t))


def main(md_path, toc_path):
    p = Path(md_path)
    lines = p.read_text(encoding="utf-8").split("\n")
    site = json.loads(Path(toc_path).read_text(encoding="utf-8"))
    idx, mine = [], []
    for i, line in enumerate(lines):
        m = HEADING.match(line)
        if m:
            idx.append(i)
            mine.append(key(m.group(2)))
    theirs = [key(n["title"]) for n in site]
    notes = {}  # line index -> editorial note moved out of a heading
    sm = difflib.SequenceMatcher(None, mine, theirs, autojunk=False)
    ops = sm.get_opcodes()
    # A file that holds one part of a larger work (a ṭīkā split per root
    # book) matches a slice of the site tree: shift depths so the part's
    # top headings land at ###.
    eq = [b for op, a1, a2, b1, b2 in ops if op == "equal" for b in range(b1, b2)]
    offset = 3 - min(site[b]["depth"] for b in eq) if eq else 0
    first_b, last_b = (eq[0], eq[-1]) if eq else (0, -1)
    changed, matched, unmatched_vault, unmatched_site = 0, 0, [], []
    for op, a1, a2, b1, b2 in ops:
        if op == "equal":
            for a, b in zip(range(a1, a2), range(b1, b2)):
                matched += 1
                depth = site[b]["depth"] + offset
                m = HEADING.match(lines[idx[a]])
                text = norm(m.group(2))
                nm = NOTE.search(text)
                if nm:
                    # A long CST note inside a heading title: keep the note
                    # as its own block right under the heading.
                    notes[idx[a]] = nm.group(1)
                    text = NOTE.sub("", text)
                title = f"**{text}**" if depth > 6 else text
                new = f"{'#' * depth} {title}" + (m.group(3) or "")
                if new != lines[idx[a]]:
                    changed += 1
                    lines[idx[a]] = new
        else:
            unmatched_vault += [mine[a] for a in range(a1, a2)]
            # only site nodes inside this file's span count as missing
            unmatched_site += [theirs[b] for b in range(b1, b2) if first_b <= b <= last_b]
    # Heading levels must not skip (linter rule, and the block-ID skills
    # number headings by sibling position): clamp each heading to at most
    # one level below the heading before it.
    prev, clamped = 1, 0
    any_heading = re.compile(r"^(#+)\s+(.*)$")
    for i, line in enumerate(lines):
        m = any_heading.match(line)
        if not m:
            continue
        lvl = len(m.group(1))
        if lvl > prev + 1:
            lvl = prev + 1
            text = m.group(2).replace("**", "")
            body = f"**{text}**" if lvl > 6 and not text.startswith("**") else text
            lines[i] = f"{'#' * lvl} {body}" if lvl > 6 else f"{'#' * lvl} {text}"
            clamped += 1
        prev = lvl
    if clamped:
        print(f"  clamped {clamped} heading(s) that skipped a level")
    for i in sorted(notes, reverse=True):
        lines[i + 1:i + 1] = ["", notes[i]]
    p.write_text("\n".join(lines), encoding="utf-8")
    if notes:
        print(f"  moved {len(notes)} editorial note(s) out of heading titles")
    print(f"{p.name}: {matched}/{len(mine)} headings matched to tipitaka.app, {changed} levels changed" + (f", depth offset {offset}" if offset else ""))
    for t in unmatched_vault:
        print(f"  vault only: {t}")
    for t in unmatched_site:
        print(f"  site only:  {t}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
