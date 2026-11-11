"""
apply.py — helper script for the add-block-id-root-text skill.

Two modes
---------
audit   python apply.py audit <file.md>
            Detects the book number, splits the file into blocks (blank-line
            / heading separated), finds every content block whose first line
            starts with "N. text", and groups them into numbering *runs* (a
            run starts wherever N resets to 1, or at the first numbered
            block in the file). For each run it lists every heading between
            the end of the previous run and the start of this one — several
            sub-headings often sit back-to-back, so the LLM must pick which
            (if any) is the run's real opening heading, not just the closest
            one. Also flags non-sequential jumps that aren't a clean reset
            or a repeated same N (duplicates become Nx1/Nx2 on apply).
            Makes no changes.

apply   python apply.py apply <file.md> --zones "1=1@25,2=2@116,3=3@588"
            Re-detects the same runs and, using the run-index -> run-label
            (+ optional chosen heading line) mapping, assigns:
              - temporary ^{book}-{run}-0 on the chosen opening heading
                (LLM replaces with full hierarchy afterward)
              - ^{book}-{run}-{n} on the LAST line of each numbered block
                (or ^{book}-{n} when label is empty: --zones "1=")
                n = printed leading number; prefix stripped from FIRST line
                repeated n in the same run → …nx1, …nx2, …
              - ^{book}-U{k} on standalone unnumbered content blocks inside a
                run (U = Unnumbered; k in document order). Stray blocks
                before the first run are left for ^T-N.
            Every pre-existing ^ID is stripped first — re-running is safe.
            Non-opener headings left bare for the LLM hierarchy pass.

What the script cannot do (requires LLM judgment):
            - which heading candidate opens a run
            - full hierarchical IDs for every heading (^0, ^T-1, h3/h4/h5…)
            - genuine reset vs interpolation / OCR when ANOMALY is flagged
"""

import argparse
import re
import sys
from pathlib import Path

NUM_PREFIX = re.compile(r"^(\d+)\.\s*(.*)$")
HEADING = re.compile(r"^(#+)\s+(.*)$")
EXISTING_ID = re.compile(r"\s*\^[\w-]+\s*$")


def read_file(path: Path):
    content = path.read_bytes().replace(b"\x00", b"").decode("utf-8")
    # Normalize CRLF/CR so Windows sources don't leave bare \r on lines
    # (rstrip on ID lines would otherwise create mixed endings / phantom blanks).
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    return content.split("\n")


def is_blank(line: str) -> bool:
    return line.strip() == ""


def is_heading(line: str) -> bool:
    return bool(HEADING.match(line))


def strip_id(line: str) -> str:
    """Remove a trailing block ID (and the space before it) if present."""
    return EXISTING_ID.sub("", line)


# ---------------------------------------------------------------------------
# Book number detection
# ---------------------------------------------------------------------------

BOOK_TITLES = {
    # Vinayapiṭaka
    "pārājikapāḷi": 1,
    "parajika": 1,
    "pācittiyapāḷi": 2,
    "pacittiya": 2,
    "mahāvaggapāḷi": 3,
    "mahavagga": 3,
    "cūḷavaggapāḷi": 4,
    "culavagga": 4,
    "parivārapāḷi": 5,
    "parivara": 5,
    "dhammasaṅgaṇīpāḷi": 1,
    "dhammasangani": 1,
    "vibhaṅgapāḷi": 2,
    "vibhanga": 2,
    "dhātukathāpāḷi": 3,
    "dhatukatha": 3,
    "puggalapaññattipāḷi": 4,
    "puggalapannatti": 4,
    "kathāvatthupāḷi": 5,
    "kathavatthu": 5,
    "yamakapāḷi": 6,
    "yamaka": 6,
    "paṭṭhānapāḷi": 7,
    "patthana": 7,
}


def detect_book(lines):
    """Book number from ## title text (preferred) or legacy ^N-0; else 1."""
    for line in lines:
        if not re.match(r"^##\s", line):
            continue
        clean = strip_id(line)
        title = re.sub(r"^##\s+", "", clean).strip().lower()
        for key, num in BOOK_TITLES.items():
            if key in title or title in key:
                return num
        m = re.search(r"\^(\d+)(?:-0)?\s*$", line)
        if m:
            return int(m.group(1))
        break
    return 1


# ---------------------------------------------------------------------------
# Block segmentation
# ---------------------------------------------------------------------------

def segment_blocks(lines):
    """
    Split lines into blocks: each heading is its own block; runs of
    consecutive non-blank, non-heading lines form a content block bounded
    by blank lines or headings. Returns a list of (kind, start, end)
    0-indexed, kind in {"heading", "content"}.
    """
    blocks = []
    current = []
    for i, line in enumerate(lines):
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


# ---------------------------------------------------------------------------
# Run detection
# ---------------------------------------------------------------------------

def detect_runs(lines):
    """
    Walk blocks in order. A numbered content block is one whose first line
    matches "N. text". A run starts at the first numbered block, and again
    every time N resets to 1 while the previous N was NOT 1. Returns a list
    of dicts:
      { first_n, last_n,
        heading_candidates: [(line_idx, level, text)],
        items: [(start_line, end_line, n)],
        anomalies: [(start_line, expected, got)],
        unnumbered: [(start_line, end_line)]  # content blocks with no N.
      }
    heading_candidates holds EVERY heading between the end of the previous
    run (or start of file) and this run's first item — the LLM must choose
    which one (if any) is the zone's actual opening heading.
    """
    blocks = segment_blocks(lines)
    runs = []
    current = None
    pending_headings = []
    prev_n = None
    stray_unnumbered = []  # content blocks outside any run (before first run, or between — shouldn't normally happen)

    for (kind, start, end) in blocks:
        if kind == "heading":
            m = HEADING.match(lines[start])
            level = len(m.group(1))
            text = strip_id(lines[start]).strip()
            pending_headings.append((start, level, text))
            continue

        # content block
        first_line = strip_id(lines[start]).strip()
        m = NUM_PREFIX.match(first_line)
        if not m:
            if current is not None:
                current.setdefault("unnumbered", []).append((start, end))
            else:
                stray_unnumbered.append((start, end))
            pending_headings = []
            continue

        n = int(m.group(1))
        starts_new_run = (current is None) or (n == 1 and prev_n != 1)

        if starts_new_run:
            if current is not None:
                runs.append(current)
            current = {
                "first_n": n,
                "last_n": n,
                "heading_candidates": pending_headings,
                "items": [(start, end, n)],
                "anomalies": [],
                "unnumbered": [],
            }
            pending_headings = []
        else:
            current["last_n"] = n
            current["items"].append((start, end, n))
            # Same printed N twice in a row → handled as Nx1/Nx2 on apply, not an anomaly.
            # Other jumps (skip or go backwards without reset-to-1) need LLM review.
            if n != prev_n and n != prev_n + 1:
                current["anomalies"].append((start, prev_n + 1, n))
            pending_headings = []
        prev_n = n

    if current is not None:
        runs.append(current)
    return runs, stray_unnumbered


# ---------------------------------------------------------------------------
# AUDIT
# ---------------------------------------------------------------------------

def cmd_audit(path: Path):
    lines = read_file(path)
    book = detect_book(lines)
    runs, stray = detect_runs(lines)

    print(f"=== AUDIT: {path.name} ({len(lines)} lines) ===")
    print(f"Detected book number: {book}\n")

    print("--- Existing block IDs (all stripped and reassigned on apply) ---")
    legacy_count = sum(1 for l in lines if re.search(r"\^[\w-]+\s*$", l))
    print(f"  {legacy_count} line(s) currently carry a block ID")
    print()

    if stray:
        print(f"--- Content blocks with no number, outside any run: {len(stray)} ---")
        print("    (left for ^T-N on apply / Step 4 — not ^book-U{k})")
        for (s, e) in stray:
            preview = lines[s].strip()[:70].encode("unicode_escape").decode()
            print(f"  L{s + 1}-{e + 1}: \"{preview}\"")
        print()

    print(f"--- Numbering runs detected: {len(runs)} ---")
    for idx, r in enumerate(runs, 1):
        s0, e0, _ = r["items"][0]
        s1, e1, _ = r["items"][-1]
        print(
            f"  Run {idx}: lines {s0 + 1}-{e1 + 1} "
            f"({len(r['items'])} items, {r['first_n']}→{r['last_n']})"
        )
        if r["heading_candidates"]:
            print("      Heading candidates (choose which, if any, opens this zone):")
            for (i, level, text) in r["heading_candidates"]:
                print(f"        L{i + 1} ({'#' * level}): \"{text}\"")
        else:
            print("      (no heading between previous run and this one)")
        if r["unnumbered"]:
            print(f"      {len(r['unnumbered'])} unnumbered block(s) inside this run "
                  f"→ will get ^{book}-U{{k}} on apply "
                  f"(merge into prior verse first if they are continuations)")
        # Count repeated printed N within this run (first keeps bare; later → Nxk)
        n_counts = {}
        for (_s, _e, n) in r["items"]:
            n_counts[n] = n_counts.get(n, 0) + 1
        dups = sorted(n for n, c in n_counts.items() if c > 1)
        if dups:
            print(
                f"      Duplicate printed N in this run (will become Nx1, Nx2…): "
                + ", ".join(f"{n}×{n_counts[n]}" for n in dups)
            )
        if r["anomalies"]:
            for (i, expected, got) in r["anomalies"]:
                print(
                    f"      ANOMALY at L{i + 1}: expected {expected}, "
                    f"got {got} — needs LLM review (interpolation? OCR error? "
                    f"genuine second reset?)"
                )
    print()

    if runs:
        print(">>> Confirm run boundaries, then pick which run is PRINCIPAL (normally the body).")
        print(">>> --zones LABEL: principal run=empty (K=); every other run=1, 2, … in document order.")
        print(">>> Zone is a collision-breaker only — not a genre/position claim. Ignore existing ^IDs.")
        if len(runs) == 1:
            zones_example = "1="
        elif len(runs) == 3:
            zones_example = "1=1,2=2,3="
        else:
            zones_example = ",".join(f"{i}=?" for i in range(1, len(runs) + 1))
        print(f'    python apply.py apply "{path}" --zones "{zones_example}"')
    else:
        print(">>> No numbered paragraphs found — nothing to do.")


# ---------------------------------------------------------------------------
# APPLY
# ---------------------------------------------------------------------------

def parse_zones(spec: str, n_runs: int):
    """
    '1=1,2=2@116,3=3@588' ->
      {1: ('1', None), 2: ('2', 115), 3: ('3', 587)}
    '1=' or '1=@25' -> empty label => content IDs are book-n (2-segment).
    Value is (zone_label, heading_line_idx_or_None), 0-indexed internally.
    If the '@lineNo' is omitted, the run's sole heading candidate is used
    automatically (only valid when there is exactly one candidate).
    """
    mapping = {}
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "=" not in part:
            print(f"Bad --zones entry (expected N=LABEL, N=, or N=LABEL@lineNo): {part!r}")
            sys.exit(1)
        k, v = part.split("=", 1)
        k = k.strip()
        v = v.strip()
        if not k.isdigit():
            print(f"Bad run index in --zones: {k!r}")
            sys.exit(1)
        if "@" in v:
            label, lineno = v.split("@", 1)
            if not lineno.strip().isdigit():
                print(f"Bad line number in --zones entry: {v!r}")
                sys.exit(1)
            mapping[int(k)] = (label.strip(), int(lineno.strip()) - 1)
        else:
            mapping[int(k)] = (v, None)
    missing = [i for i in range(1, n_runs + 1) if i not in mapping]
    if missing:
        print(f"--zones is missing labels for run(s): {missing}")
        sys.exit(1)
    return mapping


def content_id(book: int, zone: str, n: int, occurrence: int = 0) -> str:
    """book-n / book-zone-n; 2nd+ same printed N → …Nx1, …Nx2 (occurrence 1, 2…)."""
    if zone == "":
        base = f"{book}-{n}"
    else:
        base = f"{book}-{zone}-{n}"
    if occurrence <= 0:
        return base
    return f"{base}x{occurrence}"


def cmd_apply(path: Path, zones_spec: str):
    lines = read_file(path)
    book = detect_book(lines)
    runs, _stray = detect_runs(lines)

    if not runs:
        print("No numbered paragraphs found — nothing to do.")
        return

    zone_map = parse_zones(zones_spec, len(runs))

    heading_ids = {}     # line_idx -> temporary heading id (Step 4 replaces)
    id_target = {}        # end_line_idx -> content id
    prefix_strip = set()  # start_line_idx that need "N. " stripped

    for idx, r in enumerate(runs, 1):
        zone, heading_line = zone_map[idx]
        if heading_line is None:
            candidates = r["heading_candidates"]
            if len(candidates) == 1:
                heading_line = candidates[0][0]
            elif len(candidates) > 1:
                label_disp = zone if zone != "" else ""
                print(
                    f"Run {idx} has {len(candidates)} heading candidates — "
                    f"must specify which with {idx}={label_disp}@lineNo. Aborting."
                )
                sys.exit(1)
        if heading_line is not None:
            # Temporary only; LLM replaces with full hierarchy in Step 4.
            heading_ids[heading_line] = (
                f"{book}-{zone}-0" if zone != "" else f"{book}-0"
            )
        n_occurrence = {}  # printed N → how many times already assigned in this run
        for (start, end, n) in r["items"]:
            occ = n_occurrence.get(n, 0)
            n_occurrence[n] = occ + 1
            id_target[end] = content_id(book, zone, n, occurrence=occ)
            prefix_strip.add(start)

    # Standalone unnumbered body blocks inside runs → ^{book}-U{k} (document order).
    # Stray blocks before the first run are left for ^T-N in the LLM heading pass.
    u_k = 0
    for r in runs:
        for (start, end) in r.get("unnumbered", []):
            if end in id_target:
                continue
            u_k += 1
            id_target[end] = f"{book}-U{u_k}"

    result = []
    for i, line in enumerate(lines):
        clean = strip_id(line)  # strip ANY legacy ID everywhere, unconditionally

        if i in prefix_strip:
            m = NUM_PREFIX.match(clean.strip())
            clean = m.group(2) if m else clean.strip()

        if i in heading_ids:
            result.append(f"{clean.rstrip()} ^{heading_ids[i]}")
            continue
        if i in id_target:
            result.append(f"{clean.rstrip()} ^{id_target[i]}")
            continue
        result.append(clean)

    text = "\n".join(result)
    text = re.sub(r" {2,}(\^)", r" \1", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"Applied block IDs to {path.name} (book {book}, {len(runs)} run(s))\n")

    cmd_audit(path)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("mode", choices=["audit", "apply"])
    parser.add_argument("file")
    parser.add_argument("--zones", default=None)
    args = parser.parse_args()

    p = Path(args.file)
    if not p.exists():
        print(f"File not found: {p}")
        sys.exit(1)

    if args.mode == "audit":
        cmd_audit(p)
    else:
        if not args.zones:
            print("apply mode requires --zones \"1=I,2=II,...\" — run audit first.")
            sys.exit(1)
        cmd_apply(p, args.zones)


if __name__ == "__main__":
    main()
