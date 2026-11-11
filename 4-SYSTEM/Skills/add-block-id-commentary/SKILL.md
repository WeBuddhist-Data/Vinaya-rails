---
name: add-block-id-commentary
description: Apply block IDs to Pali Aṭṭhakathā/Ṭīkā commentary files in 1-SOURCES/Commentaries/. Book number matches the root text it comments on (same 1–7 table as add-block-id-root-text). Content IDs are an internal continuous per-file counter ^book-N — not the source's own printed digits, which are citation markers back to the root verse, not a paragraph count. Headings get a hierarchical ^book-path-0 scheme, numbered by sibling position, Arabic by default (same as add-block-id-root-text) — except an optional, manually-named front-matter heading and its whole subtree (--frontmatter "<heading text>"), which gets Roman numerals instead, in its own counter namespace, the same way add-block-id-root-text's M-zone works.
profile: vault-local
---

# Add Block ID — Commentary (Aṭṭhakathā / Ṭīkā)

> Shared address space: `4-SYSTEM/Guidelines/block-id-spec.md` is the authoritative spec for ID grammar, the reserved-character registry, and cross-skill invariants — see its §11 for the commentary content-ID carve-out and §11a for the front-matter (Roman numeral) heading carve-out this skill relies on. Register any new marker there before using it.

Apply block IDs to Pali commentary/sub-commentary prose in `1-SOURCES/Commentaries/` (Aṭṭhakathā, Mūlaṭīkā, Anuṭīkā, …). Unlike `add-block-id-root-text`, these sources carry **no reliable per-paragraph counter of their own**:

- Aṭṭhakathā prose is mostly unnumbered — pure continuous exposition.
- Ṭīkā (sub-commentary) paragraphs sometimes *do* start with a printed digit (`3.`, `7.`, `8.`…), but that digit is a **citation back to the root-text verse being glossed**, not a running paragraph count — it does not increment 1, 2, 3… and must **not** be treated as source-N the way `add-block-id-root-text` treats it. Leave it exactly as printed in the rendered text.

So content IDs here are a single **internal, continuous, document-order counter**, one unbroken run for the whole file — never reset by a heading, never derived from a printed digit. This is a deliberate, spec-registered exception to block-id-spec.md's "N is verbatim from the source" invariant (§11 explains why).

Because there is no run/zone ambiguity to resolve and nothing to verify against a printed number, `apply.py` for this skill assigns every ID in one pass — content *and* headings — with no manual `--zones` step. The one optional flag is `--frontmatter "<heading text>"` (see "Front matter" below), which names a single heading to treat specially; everything else is fully automatic.

---

## Book number

Same table as `add-block-id-root-text` (Abhidhammapiṭaka order 1–7). Derived automatically from the commentary file's own frontmatter:

```yaml
root_text: 1-SOURCES/Text/pi-dhammasangani.md   # → book 1
```

| `book` | Treatise |
|---|---|
| `1` | Dhammasaṅgaṇīpāḷi |
| `2` | Vibhaṅgapāḷi |
| `3` | Dhātukathāpāḷi |
| `4` | Puggalapaññattipāḷi |
| `5` | Kathāvatthupāḷi |
| `6` | Yamakapāḷi |
| `7` | Paṭṭhānapāḷi |

A commentary's book number is the book it comments on, not a separate slot — the Aṭṭhasālinī (Dhammasaṅgaṇī-aṭṭhakathā), its Mūlaṭīkā, and its Anuṭīkā are all `book 1`, each in its own file, each with its own independent bare `^1-N` counter. This does not collide with the root text's own `^1-N` addresses: block IDs are always resolved as `file#^id` (Obsidian block references), so the same digits in two different files address two different things by design, exactly as the root text's own `^1-N` and a `2` and `3`-tier commentary's `^1-N` already coexist in this vault today.

---

## ID shapes

| Kind | Shape | Notes |
|---|---|---|
| Pre-title prose (homage) | `^T-{k}` | document order, before the first `#` |
| `#` collection heading | `^0` | one per file |
| `##` book heading | `^{book}-0` | |
| `###`/`####`/`#####` heading, ordinary | `^{book}-{path}-0` | each segment = 1-based sibling position under its parent, **Arabic** — same rule as `add-block-id-root-text`; counters are independent per level and reset under each new parent |
| `###`/`####`/`#####` heading, inside the named front-matter subtree | `^{book}-{path}-0` | each segment = 1-based sibling position under its parent, **Roman numeral** (`I`, `II`, `III`, …), in its own counter namespace — see "Front matter" below |
| Content block | `^{book}-{N}` | `N` = internal continuous counter, **always Arabic**, 1 at the first content block after the book heading, incrementing by 1 for every subsequent content block for the rest of the file — headings (front matter or not) do **not** reset or advance it |

No `M`-zone, no `x`-duplicate, no `U`-unnumbered marker — those exist in `add-block-id-root-text` to reconcile IDs against the source's own printed numbers. Commentary content has no printed numbering to reconcile against, so none of those markers apply here.

### Front matter (optional, opt-in — Roman numerals)

Some commentary files open with a section that is genuinely separate from the substantive commentary body — e.g. an editorial preface or opening narrative (Sumedhakathā-type material) that precedes the commentary's actual first kaṇḍa. When such a section exists, pass its exact heading text via `--frontmatter`:

```bash
python "<this-skill-dir>/apply.py" apply "<path-to-file.md>" --frontmatter "Sumedhakathāvaṇṇanā"
```

Effect, exactly mirroring `add-block-id-root-text`'s `M`-zone (block-id-spec.md §6):

- The named heading and every heading nested under it get Roman-numeral sibling IDs, in their own counter namespace (`^1-I-0`, `^1-I-I-0`, `^1-I-II-0`, …).
- That subtree does **not** consume a slot in the body's Arabic counter — the next ordinary `###` sibling after it starts fresh at `^{book}-1-0`, not `^{book}-2-0`.
- Content-block IDs are unaffected either way — always the plain continuous Arabic counter (§ above), whether the content sits inside or outside the front-matter subtree.
- Omit `--frontmatter` entirely and every heading in the file is plain Arabic, same as `add-block-id-root-text`'s default.

**This is a judgment call, not something `apply.py` detects automatically** — exactly like deciding whether a root-text mātikā "opens the book's first counter" and therefore qualifies for `M` (block-id-spec.md §6's "test is counter behaviour, not the word 'mātikā'"). Ask: does this section genuinely precede and stand apart from the substantive commentary body, the way an opening narrative or editorial preface does — not just "does it read as introductory"? A false positive here creates exactly the genre-classification problem `add-block-id-root-text`'s SKILL.md warns against (§8 there: "Earlier versions of this skill used Roman numerals for 'front matter'... That was a mistake"). At most one such heading per file; `apply.py` does not support multiple disjoint front-matter sections.

If `--frontmatter` is given but the exact text doesn't match any heading (check diacritics/spelling), `apply.py` prints a warning and falls back to all-Arabic — it never silently no-ops.

Transclusions (`![[...]]`) are never tagged, per block-id-spec.md invariant #7 — `apply.py` skips any content block that is purely a transclusion line.

YAML frontmatter delimiters and body are never tagged, per invariant #8.

---

## Workflow

Helper: `apply.py` next to this `SKILL.md`.

### 1 — Audit

```bash
python "<this-skill-dir>/apply.py" audit "<path-to-file.md>" [--frontmatter "<heading text>"]
```

Prints (no writes): detected book number, the full heading tree, counts of pre-title / heading / content blocks, and a warning for every heading of level 1–6 that contains `**` (with its line number) — bold is redundant at those levels and ends up in the TOC title. The same warning is printed on apply. Ignore existing `^` IDs — they are stripped and fully reassigned on apply. If a section of the file looks like genuine front matter (see above), re-run audit with `--frontmatter "<exact heading text>"` to preview which heading it would attach to before committing to it in apply — the audit output flags the matched heading, or warns if the text didn't match anything.

### 2 — Apply

```bash
python "<this-skill-dir>/apply.py" apply "<path-to-file.md>" [--frontmatter "<heading text>"]
```

One pass, fully automatic — strips every existing `^id`, then assigns pre-title `^T-k`, the heading hierarchy (Arabic, or Roman inside the named front-matter subtree), and the continuous Arabic content counter. Re-running is always safe, including with a different (or no) `--frontmatter` value — every existing `^id` is stripped and regenerated from scratch each time.

### 3 — Spot-check

After applying, confirm:

- Homage line (if present) carries `^T-1` (and `^T-2`, … for any further pre-title blocks).
- The `#` collection heading is bare `^0`.
- If `--frontmatter` was used: the named heading and its whole subtree carry **Roman numerals** (`I`, `II`, `III`, …), and the next ordinary `###` sibling after that subtree starts its own Arabic counter at `1` (not continuing/skipping past the front-matter subtree).
- Every other heading's sibling numbers are **Arabic** and increment correctly under each parent, restarting under a new parent, at every level (`###`, `####`, `#####` each keep independent counters).
- Content IDs are **always Arabic** (front matter or not) and increment by exactly 1 across the whole file, including across heading boundaries — no resets, no gaps except where a transclusion was correctly skipped.
- Printed digits inside commentary paragraphs (root-verse citation markers) are untouched — never confused with the block ID.

---

## Dos and Don'ts

- **DO** derive the book number from the file's own `root_text:` frontmatter.
- **DO** treat content numbering as an internal continuous counter — never derive it from a printed digit in the source.
- **DON'T** reset the content counter at any heading boundary, front matter or not.
- **DO** number ordinary headings by 1-based sibling position under their parent, independently per level, in **Arabic** — same rule as `add-block-id-root-text`.
- **DO** use `--frontmatter "<exact heading text>"` only for a heading that genuinely precedes and stands apart from the substantive commentary body — never to mark a section merely because it reads as introductory. This is a judgment call, the same one `add-block-id-root-text` makes for its `M`-zone (block-id-spec.md §6) — not something the script infers on its own.
- **DON'T** render content-block IDs as Roman — content stays Arabic always, front matter or not.
- **DON'T** leave `**` inside a heading of level 1–6 — the heading already renders as a heading, and the bold ends up in the parser's TOC title. Only headings deeper than level 6 need it, and the parser strips it there.
- **DON'T** mark more than one front-matter section per file — `apply.py` supports exactly zero or one.
- **DON'T** assign IDs to `![[...]]` transclusions or to YAML frontmatter.
- **DO** re-run freely — every existing `^id` is stripped and regenerated from scratch each time.

## Vinaya vault note

In this vault the book numbers are the Vinayapiṭaka order: `1` Pārājikapāḷi, `2` Pācittiyapāḷi (with the Bhikkhunīvibhaṅga), `3` Mahāvaggapāḷi, `4` Cūḷavaggapāḷi, `5` Parivārapāḷi. The book-7 and `M`-zone notes above are Abhidhamma-specific; no Vinaya book has a mātikā or more than one numbering run. The end-to-end Vinaya build (XML → JSON → markdown → these IDs → checks) is `0-INBOX/raw-data/build_all.sh`, using `4-SYSTEM/scripts/tipitaka-xml-to-json/`.
