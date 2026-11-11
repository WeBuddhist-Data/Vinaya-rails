#!/usr/bin/env python3
"""Step 4 of add-block-id-root-text: heading IDs and pre-title IDs.

Per 4-SYSTEM/Guidelines/block-id-spec.md (Abhidhamma vault) §2–§5:
  - content strictly before the first heading -> ^T-N
  - '#'  -> ^0
  - '##' -> ^{book}-0
  - '###' and deeper -> ^{book}-{sibling path}-0, one continuous '###'
    counter across the whole book.
Existing heading IDs are stripped first; content IDs are left untouched.

Usage: heading_ids.py <file.md> <book>
"""
import re
import sys
from pathlib import Path

HEADING = re.compile(r"^(#+)\s+(.*?)\s*$")
TRAILING_ID = re.compile(r"\s+\^[^\s]+\s*$")


def main(path: str, book: int) -> None:
    p = Path(path)
    lines = p.read_text(encoding="utf-8").split("\n")
    # frontmatter span
    start = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                start = i + 1
                break
    seen_heading = False
    t_counter = 0
    counters: list[int] = []  # counters[k] = sibling count at depth k (### = 0)
    for i in range(start, len(lines)):
        line = lines[i]
        m = HEADING.match(line)
        if not m:
            if not seen_heading and line.strip() and not TRAILING_ID.search(line):
                t_counter += 1
                lines[i] = f"{line.rstrip()} ^T-{t_counter}"
            continue
        seen_heading = True
        hashes, title = m.group(1), TRAILING_ID.sub("", m.group(2)).strip()
        level = len(hashes)
        if level == 1:
            hid = "^0"
        elif level == 2:
            hid = f"^{book}-0"
            counters = []
        else:
            depth = level - 3
            counters = counters[: depth + 1]
            while len(counters) < depth + 1:
                counters.append(0)
            counters[depth] += 1
            hid = f"^{book}-" + "-".join(str(c) for c in counters) + "-0"
        lines[i] = f"{hashes} {title} {hid}"

    # Step 4.5: every content block after the first heading that still has
    # no ID is an unnumbered block -> ^{book}-U{k}. U is one global counter,
    # renumbered here in document order.
    u_re = re.compile(rf"\s\^{book}-U\d+\s*$")
    blocks, cur = [], []
    for i in range(start, len(lines)):
        line = lines[i]
        if not line.strip() or HEADING.match(line):
            if cur:
                blocks.append(cur)
                cur = []
            continue
        cur.append(i)
    if cur:
        blocks.append(cur)
    k = 0
    for b in blocks:
        last = b[-1]
        if all(lines[j].startswith("![[") for j in b):
            continue  # transclusion-only blocks take no ID
        if re.search(r"\s\^T-\d+\s*$", lines[last]):
            continue
        if u_re.search(lines[last]) or not TRAILING_ID.search(lines[last]):
            k += 1
            lines[last] = u_re.sub("", lines[last]).rstrip() + f" ^{book}-U{k}"
    p.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))
