"""
apply.py — helper script for the add-block-id-commentary skill.

Unlike add-block-id-root-text, commentary sources carry **no reliable
per-paragraph source numbering** to preserve verbatim — a printed digit
inside a commentary paragraph (e.g. "3. Tatthāpi ...") is a citation back to
the ROOT TEXT verse being glossed, not a running paragraph counter, and it
is left untouched in the rendered text. So content IDs here are an
**internal, continuous, document-order counter** — one unbroken run for the
whole file, never reset by headings, never derived from printed digits.
This is a deliberate, spec-registered exception to block-id-spec.md's
"N is verbatim from the source" invariant — see block-id-spec.md §11.

Headings default to plain Arabic sibling-position numbering, same logic as
add-block-id-root-text. The ONE exception: a single, manually-identified
front-matter heading (and its whole descendant subtree) — a section that
structurally precedes and is separate from the substantive commentary body,
analogous to add-block-id-root-text's `M`-zone — gets Roman-numeral sibling
IDs instead, in its own counter namespace that does not consume a slot in
the body's Arabic counter. See block-id-spec.md §11a. This is a judgment
call, exactly like M-zone detection in add-block-id-root-text: pass
--frontmatter "<exact heading text>" naming the heading that opens it. Omit
the flag and every heading in the file is plain Arabic — the front-matter
exception is opt-in, not a default.

Usage
-----
audit   python apply.py audit <file.md> [--frontmatter "<heading text>"]
            Detects the book number (from frontmatter `root_text:`), lists
            pre-title blocks, the heading tree, and how many content blocks
            will receive ^{book}-{N}. Makes no changes. With --frontmatter,
            flags which heading (if found) would become the Roman-numbered
            front-matter root.

apply   python apply.py apply <file.md> [--frontmatter "<heading text>"]
            Strips every pre-existing ^id, then assigns:
              - ^T-{k} to each pre-title block (homage etc.), doc order
              - ^0 to the single `#` collection heading
              - ^{book}-0 to the `##` book heading
              - ^{book}-{path}-0 to every other heading, each segment being
                that heading's 1-based sibling position under its parent —
                Arabic by default; Roman ONLY for the heading matching
                --frontmatter (if given) and everything nested under it
                (###, ####, ##### each keep their own sibling counter within
                whichever numeral system applies to them)
              - ^{book}-{N} to every content block, N counting up by 1
                across the WHOLE file in document order (continuation, not
                reset, across every heading, including inside the
                front-matter subtree). Content is ALWAYS Arabic — the
                front-matter distinction never touches content IDs.
            Re-running is always safe — all existing ^ids are stripped first.

What this script does NOT do:
            - It never invents or edits prose.
            - It does not auto-detect the front-matter heading. Exactly one
              heading may be named via --frontmatter per run; deciding
              whether a section qualifies (does it genuinely precede and
              stand apart from the body, the way a root-text mātikā that
              opens the book's first counter does?) is an LLM/editorial
              judgment call outside this script's scope, not something the
              script infers from headings or content.
"""

import re
import sys
from pathlib import Path

HEADING = re.compile(r"^(#+)\s+(.*)$")
EXISTING_ID = re.compile(r"\s*\^[\w-]+\s*$")
ROOT_TEXT_FM = re.compile(r"^root_text:\s*.*?([A-Za-z0-9_-]+)\.md\s*$")
TRANSCLUSION_ONLY = re.compile(r"^\s*!\[\[[^\]]+\]\]\s*$")

_ROMAN_TABLE = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]


def to_roman(n: int) -> str:
    """1-based sibling index -> uppercase Roman numeral (I, II, III, IV, ...).
    Every heading path segment in a commentary file uses this instead of a
    plain Arabic sibling index — block-id-spec.md §11a."""
    if n <= 0:
        raise ValueError(f"to_roman expects a positive index, got {n}")
    out = []
    for val, sym in _ROMAN_TABLE:
        while n >= val:
            out.append(sym)
            n -= val
    return "".join(out)

BOOK_SLUGS = {
    "pi-dhammasangani": 1, "pi-1": 1,
    "pi-vibhanga": 2, "pi-2": 2,
    "pi-dhatukatha": 3, "pi-3": 3,
    "pi-puggalapannatti": 4, "pi-4": 4,
    "pi-kathavatthu": 5, "pi-5": 5,
    "pi-yamaka": 6, "pi-6": 6,
    "pi-patthana": 7, "pi-7": 7,
}


def read_file(path: Path):
    content = path.read_bytes().replace(b"\x00", b"").decode("utf-8")
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    return content.split("\n")


def is_blank(line: str) -> bool:
    return line.strip() == ""


def is_heading(line: str) -> bool:
    return bool(HEADING.match(line))


def strip_id(line: str) -> str:
    return EXISTING_ID.sub("", line)


def detect_book(lines):
    """Book number from frontmatter `root_text: 1-SOURCES/Text/pi-xxx.md`."""
    in_fm = False
    for i, line in enumerate(lines):
        if line.strip() == "---":
            if i == 0:
                in_fm = True
                continue
            if in_fm:
                break
        if in_fm:
            m = ROOT_TEXT_FM.match(line.strip())
            if m:
                slug = m.group(1).lower()
                if slug in BOOK_SLUGS:
                    return BOOK_SLUGS[slug]
    return 1


def frontmatter_span(lines):
    """(start, end) 0-indexed, inclusive, of the YAML frontmatter block
    (both '---' delimiters), or None if the file has none. Per
    block-id-spec.md invariant #8, these lines are never tagged."""
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return (0, i)
    return None


def segment_blocks(lines):
    """
    Same segmentation as add-block-id-root-text: headings are their own
    block; blank/heading-bounded runs of lines form content blocks.
    Frontmatter (if present) is skipped entirely — never a block.
    Returns list of (kind, start, end) 0-indexed.
    """
    fm = frontmatter_span(lines)
    fm_end = fm[1] if fm else -1
    blocks = []
    current = []
    for i, line in enumerate(lines):
        if i <= fm_end:
            continue
        if is_heading(line):
            if current:
                blocks.append(("content", current[0], current[-1]))
                current = []
            blocks.append(("heading", i, i))
            continue
        if is_blank(line):
            if current:
                blocks.append(("content", current[0], current[-1]))
                current = []
            continue
        current.append(i)
    if current:
        blocks.append(("content", current[0], current[-1]))
    return blocks


def parse_frontmatter_arg(argv):
    """Pulls --frontmatter "<text>" out of the tail args, if present."""
    args = list(argv)
    fm_text = None
    if "--frontmatter" in args:
        i = args.index("--frontmatter")
        if i + 1 >= len(args):
            print('Usage: --frontmatter requires a heading-text argument')
            sys.exit(1)
        fm_text = args[i + 1].strip()
        del args[i:i + 2]
    return fm_text, args


def bold_heading_warnings(lines):
    """Headings of level 1-6 that carry `**`.

    Obsidian renders six heading levels, so bold inside one of them is
    redundant and ends up in the TOC title.
    """
    found = []
    for i, line in enumerate(lines):
        m = HEADING.match(line)
        if m and len(m.group(1)) <= 6 and "**" in m.group(2):
            found.append((i + 1, strip_id(line).strip()))
    return found


def print_bold_heading_warnings(lines):
    for lineno, text in bold_heading_warnings(lines):
        print(f'  WARN L{lineno}: heading contains ** — "{text[:70]}"')


def cmd_audit(path: Path, frontmatter_text=None):
    lines = read_file(path)
    book = detect_book(lines)
    blocks = segment_blocks(lines)

    print(f"=== AUDIT: {path.name} ({len(lines)} lines) ===")
    print(f"Detected book number: {book} (from frontmatter root_text:)\n")

    legacy_count = sum(1 for l in lines if re.search(r"\^[\w-]+\s*$", l))
    print(f"{legacy_count} line(s) currently carry a block ID (stripped and reassigned on apply)\n")

    first_heading_seen = False
    pre_title = 0
    content_blocks = 0
    heading_blocks = 0
    fm_matched = False
    for (kind, start, end) in blocks:
        if kind == "heading":
            first_heading_seen = True
            heading_blocks += 1
            hm = HEADING.match(lines[start])
            level = len(hm.group(1))
            text = strip_id(lines[start]).strip()
            bare_text = strip_id(hm.group(2)).strip()
            flag = ""
            if frontmatter_text and bare_text == frontmatter_text:
                flag = "  <-- front-matter root (Roman numerals from here down)"
                fm_matched = True
            print(f"  {'#' * level} L{start + 1}: \"{text[:70]}\"{flag}")
        else:
            block_lines = [lines[i] for i in range(start, end + 1)]
            is_pure_transclusion = all(
                is_blank(l) or TRANSCLUSION_ONLY.match(l) for l in block_lines
            ) and any(TRANSCLUSION_ONLY.match(l) for l in block_lines)
            if is_pure_transclusion:
                continue
            if not first_heading_seen:
                pre_title += 1
            else:
                content_blocks += 1

    print()
    print(f"Pre-title blocks (→ ^T-1, ^T-2, …): {pre_title}")
    if frontmatter_text:
        status = "found above" if fm_matched else "NOT FOUND — check exact heading text"
        print(f"Front-matter heading requested: \"{frontmatter_text}\" ({status})")
        print(f"Heading blocks (→ Roman inside front matter, Arabic elsewhere, hierarchical ^{book}-…-0): {heading_blocks}")
    else:
        print(f"Heading blocks (→ hierarchical ^{book}-…-0, plain Arabic — no --frontmatter given): {heading_blocks}")
    print(f"Content blocks (→ continuous ^{book}-N, always Arabic): {content_blocks}")

    bold = bold_heading_warnings(lines)
    if bold:
        print()
        print(f"Bold in headings of level 1-6 ({len(bold)}) — bold is redundant there "
              "and ends up in the TOC title:")
        print_bold_heading_warnings(lines)
    print()
    print(f'>>> python apply.py apply "{path}"' + (f' --frontmatter "{frontmatter_text}"' if frontmatter_text else ""))


def _next_sibling(path_stack, sibling_counters, level, depth, numeral_fn):
    """Advance the sibling counter for `level` under the current parent
    path, returning the new path_stack, updated counters, and the rendered
    (numeral_fn-applied) path segments."""
    path_key = tuple(path_stack[: depth - 1])
    idx = sibling_counters.get((level, path_key), 0) + 1
    sibling_counters[(level, path_key)] = idx
    # reset deeper levels' counters when a shallower sibling advances
    sibling_counters = {
        k: v for k, v in sibling_counters.items()
        if not (k[0] > level and k[1][: depth - 1] == path_key and len(k[1]) >= depth)
    }
    new_path_stack = path_stack[: depth - 1] + [idx]
    rendered = [numeral_fn(p) for p in new_path_stack]
    return new_path_stack, sibling_counters, rendered


def cmd_apply(path: Path, frontmatter_text=None):
    lines = read_file(path)
    book = detect_book(lines)
    blocks = segment_blocks(lines)

    print_bold_heading_warnings(lines)

    ids = {}  # line_idx -> id string
    t_k = 0
    n = 0

    # Two independent heading counter namespaces. Arabic is the default,
    # used everywhere except inside the front-matter subtree (if any).
    arabic_path_stack, arabic_counters = [], {}
    roman_path_stack, roman_counters = [], {}

    fm_active = False   # currently inside the front-matter subtree
    fm_level = None      # heading level that opened it
    fm_matched = False   # did we ever find the requested heading

    first_heading_seen = False

    for (kind, start, end) in blocks:
        if kind == "heading":
            first_heading_seen = True
            m = HEADING.match(lines[start])
            level = len(m.group(1))  # 1..5
            text = strip_id(m.group(2)).strip()  # heading text only, no "#"s

            if level == 1:
                ids[start] = "0"
                arabic_path_stack, arabic_counters = [], {}
                roman_path_stack, roman_counters = [], {}
                fm_active = False
                continue

            if level == 2:
                ids[start] = f"{book}-0"
                arabic_path_stack, arabic_counters = [], {}
                roman_path_stack, roman_counters = [], {}
                fm_active = False
                continue

            depth = level - 2  # level3(###)=depth1, level4(####)=depth2, ...

            if fm_active and level <= fm_level:
                # A sibling (or higher) heading closes the front-matter
                # subtree; this heading and everything after it is
                # ordinary Arabic body content again.
                fm_active = False

            if not fm_active and frontmatter_text and text == frontmatter_text:
                # Opens the front-matter subtree. It gets its own Roman
                # counter namespace and does NOT consume a slot in the
                # Arabic body counter — same principle as add-block-id-
                # root-text's M-zone (block-id-spec.md §6, §11a).
                fm_active = True
                fm_level = level
                fm_matched = True
                roman_path_stack, roman_counters, rendered = _next_sibling(
                    roman_path_stack, roman_counters, level, depth, to_roman
                )
                ids[start] = f"{book}-" + "-".join(rendered) + "-0"
                continue

            if fm_active:
                roman_path_stack, roman_counters, rendered = _next_sibling(
                    roman_path_stack, roman_counters, level, depth, to_roman
                )
                ids[start] = f"{book}-" + "-".join(rendered) + "-0"
            else:
                arabic_path_stack, arabic_counters, rendered = _next_sibling(
                    arabic_path_stack, arabic_counters, level, depth, str
                )
                ids[start] = f"{book}-" + "-".join(rendered) + "-0"
            continue

        # content block
        block_lines = [lines[i] for i in range(start, end + 1)]
        is_pure_transclusion = all(
            is_blank(l) or TRANSCLUSION_ONLY.match(l) for l in block_lines
        ) and any(TRANSCLUSION_ONLY.match(l) for l in block_lines)
        if is_pure_transclusion:
            continue  # invariant: never assign IDs to ![[...]] transclusions

        if not first_heading_seen:
            t_k += 1
            ids[end] = f"T-{t_k}"
        else:
            n += 1
            ids[end] = f"{book}-{n}"  # always Arabic, front matter or not

    if frontmatter_text and not fm_matched:
        print(f'WARNING: --frontmatter "{frontmatter_text}" did not match any heading text — '
              f'no Roman numerals were assigned. Check exact spelling/diacritics.\n')

    result = []
    for i, line in enumerate(lines):
        clean = strip_id(line)
        if i in ids:
            result.append(f"{clean.rstrip()} ^{ids[i]}")
        else:
            result.append(clean)

    text = "\n".join(result)
    text = re.sub(r" {2,}(\^)", r" \1", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    path.write_text(text, encoding="utf-8", newline="\n")
    fm_note = f'; front matter "{frontmatter_text}" -> Roman' if frontmatter_text else "; no front matter (all headings Arabic)"
    print(f"Applied block IDs to {path.name} (book {book}{fm_note})\n")
    cmd_audit(path, frontmatter_text)


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("audit", "apply"):
        print('Usage: python apply.py audit|apply <file.md> [--frontmatter "<heading text>"]')
        sys.exit(1)
    mode = sys.argv[1]
    frontmatter_text, rest = parse_frontmatter_arg(sys.argv[2:])
    if not rest:
        print("Usage: missing <file.md>")
        sys.exit(1)
    p = Path(rest[0])
    if not p.exists():
        print(f"File not found: {p}")
        sys.exit(1)
    if mode == "audit":
        cmd_audit(p, frontmatter_text)
    else:
        cmd_apply(p, frontmatter_text)


if __name__ == "__main__":
    main()
