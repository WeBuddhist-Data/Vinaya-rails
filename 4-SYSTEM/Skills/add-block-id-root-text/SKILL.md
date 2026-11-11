---
name: add-block-id-root-text
description: Apply block IDs to Pali Abhidhamma root-text files (mātikā/kaṇḍa prose) in 1-SOURCES/Text/. Derives IDs from headings + leading N. numbers. Sole run → ^book-N; multiple runs → principal run stays ^book-N, others get ^book-k-N. Headings numbered by sibling position, may be longer.
profile: vault-local
---

# Add Block ID — Pali Mātikā/Kaṇḍa Texts

> Shared address space: `4-SYSTEM/Guidelines/block-id-spec.md` is the authoritative spec for ID grammar, the reserved-character registry, and cross-skill invariants. Register any new marker there before using it.

Apply block IDs to Pali Abhidhamma prose whose source prints paragraph numbers (`1.`, `2.`, `58.`…) that sometimes restart. **Ignore every existing `^…` ID in the file.** Rebuild from two signals only:

1. **Headings** (`#` … `#####`) — sibling order under each parent
2. **Leading verse numbers** — the integer before the first `.` on a content line, e.g. `1. (Ka) hetū dhammā.` → `1`

---

## Inputs (what counts)

| Signal | Use | Ignore |
|---|---|---|
| `N. text…` at start of a content line | `N` is the content address | Any trailing `^old-id` |
| `#` / `##` / `###` / `####` / `#####` title lines | Heading hierarchy + sibling counters | Any trailing `^old-id` |
| Homage / plain lines strictly before the file's first `#` heading of any level | Pre-title blocks (`^T-N`) | — |
| Unnumbered continuation lines | Same block as the preceding `N.` | Do not invent a new `N` |

Example (Dukamātikā):

```text
1. (Ka) hetū dhammā.        → take 1
2. (Ka) sahetukā dhammā.    → take 2
```

---

## Content IDs — choose `n-n` or `n-n-n`

Content IDs use **at most 3** segments. Prefer the **shortest form that stays unambiguous**.

### Step A — find numbering runs

Walk the file in order. A **run** is one unbroken sequence of leading numbers (`N.`).

- A new run starts at the first `N.` in the file.
- Another new run starts whenever the leading number returns to `1` after a previous number that was not `1`.
- Most headings do **not** start a run — a run often continues across many `####` / `#####` headings.

### Step B — the zone is a collision-breaker, nothing more

**Do not classify runs by genre or position.** Earlier versions of this skill used Roman numerals for "front matter" and reserved other vocabularies for "body" / "back matter". That was a mistake: those labels claimed to describe *what content is* (matrix, intro, closing) when they actually only recorded *where a counter happened to reset*. The two come apart constantly — a mātikā can sit mid-body, an `Uddesa` can be numerically fused to the body, matrix content can be indistinguishable from prose by numbering alone.

The middle segment exists for exactly one reason: **to stop two blocks with the same printed `N` from colliding inside one book.** Nothing else. It carries no meaning about genre, position, or importance.

It follows that:

- A book whose printed numbers are already unique book-wide (one single run) needs **no** middle segment at all.
- A book with several runs needs one only for the runs that would otherwise collide.

### Step C — pick the ID shape (do not hard-code book-specific patterns)

For each run, build the content ID from `book` + optional middle label + source `N`:

```
book  = Abhidhammapiṭaka order of this file (1…7), from ## title
N     = the printed leading number on that paragraph (never recomputed)
```

| Condition | Content ID | Shape |
|---|---|---|
| **Exactly one** run in the whole file | `^{book}-{N}` | `n-n` — **omit** the middle segment |
| **Two or more** runs | principal run `^{book}-{N}`; every other run `^{book}-{1}-{N}`, `^{book}-{2}-{N}`, … | `n-n` / `n-n-n` |

**Which run is "principal"?** The one you want cheapest to cite — normally the main body, which is usually also the longest. It keeps the bare `^{book}-{N}` namespace. Every *other* run takes the next sequential Arabic label in document order (`1`, `2`, …). Because those labels are pure collision-breakers, they are assigned by position, not by what the run contains.

When a book's runs are all conceptually peer/co-equal sections (e.g. book 6's ten yamakas, or a book split into many resetting zones with no single run that dominates), prefer **uniform positional numbering for every run, including the first** (`^{book}-1-{N}`, `^{book}-2-{N}`, …) over carving out a bare-namespace exception for one of them. Reserve the bare-principal-run form for books that genuinely have one dominant body run and only incidental smaller runs elsewhere. This also keeps IDs reliably searchable/predictable across a whole book when the number of zones is large — a stated design goal for these files.

**Why keep the body bare (when there is a real principal run)?** If the body is a single continuous counter, `^{book}-{N}` already cites it uniquely, and it is the text people cite most. Adding a redundant middle segment only lengthens the IDs that matter most.

### The `M` zone — a matrix that opens the book's first counter

One narrow exception to "zones are sequential and meaningless". When a **mātikā/matrix section is what starts the book's first numbering run** — i.e. it precedes the body and owns its own counter(s) — it is genuinely introductory material, and gets the `M` vocabulary instead of a plain sequential number:

| Track | Shape | Example (book 1) |
|---|---|---|
| Heading — the matrix parent | `^{book}-M-0` | `### Mātikā ^1-M-0` |
| Heading — its children | `^{book}-M-{Roman}-0` | `#### Tikamātikā ^1-M-I-0`, `#### Dukamātikā ^1-M-II-0` |
| Heading — deeper levels | Roman all the way down | `##### Hetugocchakaṃ ^1-M-II-I-0` … `^1-M-II-XIV-0` |
| Content of a matrix run | `^{book}-M{Roman}-{N}` | `^1-MI-1`…`^1-MI-22`, `^1-MII-1`…`^1-MII-142` |

Heading and content use the **same Roman label** for the same object — heading `^1-M-I-0` ↔ content `^1-MI-{N}`; heading `^1-M-II-0` ↔ content `^1-MII-{N}`. The only difference is that the heading track keeps its segments separated (and may nest deeper), while content fuses `M` + Roman into a single token so it stays within 3 segments.

Body `###` numbering then starts at `1` **after** the `M` section (`### Cittuppādakaṇḍaṃ ^1-1-0`), since `M` occupies its own slot rather than a numeric one.

**The test is counter behaviour, not the word "mātikā".** Matrices are common and recur throughout these books — book 1 has a second `#### Mātikā` inside Rūpakaṇḍaṃ, book 2 has 23 mātikā headings and *no* opening matrix at all, book 3 has five inside its `Uddesa`. None of those get `M`, because none of them starts the first counter: their numbers continue the surrounding run, so they are ordinary content under ordinary zones. Only a matrix that **opens** the book's numbering qualifies.

### Splitting one detected run into two zones at a chosen heading

Sometimes the printed numbers never reset at a real structural boundary — e.g. book 7's `paccayuddesa` / `paccayaniddesa` / `Pucchāvāro` runs straight into `1. Kusalattikaṃ`'s own exposition with no reset back to `1` (items 1–52 are the shared front matter, item 53 onward is Kusalattikaṃ's, but both are one auto-detected run). When a heading boundary like this clearly separates two conceptually distinct zones despite no number reset, split the run manually at that heading: everything before it becomes one zone, everything from it onward becomes the next, each keeping its own copy of the printed `N` verbatim. `apply.py`'s automatic run detection (reset-to-1 only) cannot do this split by itself — it has to be done by re-partitioning that run's item list at the chosen line before assigning zone labels.

### Duplicate printed `N` within one run

When the source repeats the same leading number without resetting the run (often consecutive):

```text
4. …
5. …
5. …
6. …
```

Keep the first as bare `N`; disambiguate later copies with an `x` suffix on the **last** segment:

| Printed | Content ID (sole body) | Content ID (zoned run) |
|---|---|---|
| first `5.` | `^{book}-5` | `^{book}-{zone}-5` |
| second `5.` | `^{book}-5x1` | `^{book}-{zone}-5x1` |
| third `5.` | `^{book}-5x2` | `^{book}-{zone}-5x2` |

`apply.py` does this automatically (occurrence order within each run). Do **not** invent a new run for a repeated `N` that is not a reset to `1`.

### Unnumbered body segments (`U` = Unnumbered)

Some body blocks have **no** leading `N.` and are **not** continuations of the previous numbered verse (blank-line separated units that must keep their own ID — e.g. an unlabelled matrix list under `##### Dukaṃ`).

Classify the gap first:

| Role | ID |
|---|---|
| Homage / any plain content **strictly before the file's first `#` heading of any level** | `^T-1`, `^T-2`… — Step 4, **not** `U` |
| Unnumbered content that falls **after** the first heading but **before the first numbering run starts** (e.g. an enumeration list under an intro subheading, before the body's own `1.` begins) | `^{book}-U{k}` — same treatment and same global counter as unnumbered blocks inside a run, **not** `^T-N` |
| Numbered block in a non-principal run | usual zone label from Step C (`^{book}-{zone}-{N}`) |
| Continuation of the previous `N.` (same verse) | merge into that block; one ID on the last line |
| Standalone unnumbered **body** segment (inside a run) | `^{book}-U{k}` |

`T-N` is reserved **only** for content that sits before the very first heading in the file — typically just the homage line (`Namo tassa…`). It is not a catch-all for "anything before the numbering starts": a book can have headings, sub-headings, and even whole unnumbered paragraphs (like an intro's enumeration list) before its first `N.` run begins, and none of that is pre-title. Once the file has its first heading, every subsequent stray unnumbered block is ordinary `U`-territory, whether or not a numbering run has technically started yet.

`U` means Unnumbered. Number `k` in **document order** across the **whole file** — this includes both the pre-run stray blocks described above and every standalone unnumbered block inside any run:

```text
^{book}-U1
^{book}-U2
…
```

Examples (`book=1`): `^1-U1`, `^1-U2`.

Prefer merging intro/outro lines into the adjacent numbered verse when they clearly belong to it. Use `U` only when the block must remain separate. Do **not** use `x` here (`x` = duplicate printed `N.` only). Do **not** use `^1-0U1` (collides conceptually with heading `^1-0`).

`apply.py` assigns `^{book}-U{k}` automatically to unnumbered content blocks **inside** a numbering run, and reports pre-first-run stray blocks separately in its audit output; the LLM must classify each stray block by the table above (pre-title → `T-N`, everything else → `U{k}` continuing the same global counter, positioned in its correct document-order slot before the in-run U-blocks that follow it).

### Step D — check your work

After labeling, verify:

- If there is only one run in the file, content IDs are `^{book}-{N}` with **no** middle segment.
- If there are several runs, either the principal run stays bare and every other run has its own sequential Arabic middle segment (`1`, `2`, …) in document order, **or** — when the runs are conceptually peer/co-equal and searchability across many zones matters more than a shorter body ID — every run including the first gets a positional label; no two runs share a label either way.
- Repeated printed `N` in one run → first `…-{N}`, then `…-{N}x1`, `…-{N}x2`, …
- Standalone unnumbered body blocks inside a run → `^{book}-U1`, `^{book}-U2`, … (not `^T-N`)
- Stray unnumbered blocks after the title but before the first run → also `^{book}-U{k}` (not `^T-N`); only content before the very first heading is `^T-N`.
- No content ID exceeds 3 hyphen-separated segments; headings may be longer and end in `-0` (except `^0`, `^T-N`). The `xK` / `U{k}` markers sit on the last segment (`5x1`, `U1`), not as an extra hyphen part.
- Stripped `N.` prefixes; ID on the last line of each numbered block.

After assigning the ID, **strip** the `N.` prefix from the rendered line. Put the ID on the **last** line of the block (continuations / closers stay in the same block).

### Abhidhammapiṭaka `book` numbers

| `book` | Treatise |
|---|---|
| `1` | Dhammasaṅgaṇīpāḷi |
| `2` | Vibhaṅgapāḷi |
| `3` | Dhātukathāpāḷi |
| `4` | Puggalapaññattipāḷi |
| `5` | Kathāvatthupāḷi |
| `6` | Yamakapāḷi |
| `7` | Paṭṭhānapāḷi |

---

## Heading IDs — may exceed `n-n-n`

Every heading gets an ID. Trailing `-0` marks a heading (never content).

**Headings are a separate track from content zones.** A heading's ID records *where it sits in the document tree*; a content zone records *which numbering run a paragraph belongs to*. Do not try to make one mirror the other — that is what forced the old Roman/front-matter scheme, and it does not survive contact with real books.

Each heading segment is its **sequential position among its siblings** under the same parent (Roman inside an `M` subtree, Arabic elsewhere).

Note that some headings *do* carry printed numbers — book 2 has ~170 `#####` headings like `##### (25. Ka) arati` and `##### (1) Rūpadukaṃ`. **Use sibling position anyway, not those printed numbers**: they collide (two different `(1) …` headings under the same parent would produce the same ID) and they desync wherever lettered sub-headings intervene (`(24. Kha)`, `(24. Ga)` push `(25. Ka)` to sibling 27). Verbatim-number preservation is a rule for *content* IDs only.

| Heading | ID | Example (`book=1`) |
|---|---|---|
| Homage / pre-`#` prose | `^T-1`, `^T-2`… | `Namo tassa… ^T-1` |
| `#` collection | `^0` | `# Abhidhammapiṭake ^0` |
| `##` book | `^{book}-0` | `## Dhammasaṅgaṇīpāḷi ^1-0` |
| `###` (any) | `^{book}-{h3}-0` | `### Mātikā ^1-1-0`, `### Cittuppādakaṇḍaṃ ^1-2-0` |
| `####` | `^{book}-{h3}-{h4}-0` | `#### Tikamātikā ^1-1-1-0`, `#### Dukamātikā ^1-1-2-0` |
| `#####` | `^{book}-{h3}-{h4}-{h5}-0` | `##### Hetugocchakaṃ ^1-1-2-1-0` |

`###` counters run straight through **all** `###` siblings in document order — Mātikā is simply the 1st, Cittuppādakaṇḍaṃ the 2nd, and so on. There is no separate counter for "front" vs "body" sections, because that distinction no longer exists.

Heading depth may produce **4+** segments. Content stays ≤3 segments. The heading's trailing `-0` keeps e.g. `### Cittuppādakaṇḍaṃ ^1-2-0` distinct from paragraph `^1-2`.

Because the two tracks are independent, the same digits can appear in both with different meanings — e.g. Dukamātikā's **content** is `^1-2-{N}` (2nd non-principal run) while its **heading** is `^1-1-2-0` (2nd `####` under the 1st `###`). No literal collision is possible, since content IDs never end in `-0`.

---

## Workflow

Helper: `apply.py` next to this `SKILL.md`.

### 1 — Audit

```bash
python "<this-skill-dir>/apply.py" audit "<path-to-file.md>"
```

Prints (no writes): detected `book`, each numbering run (lines, `first→last`, heading candidates), anomalies (non-sequential jumps that are not a clean reset to `1`), and any stray unnumbered blocks found before the first run.

**Ignore existing `^` IDs** when judging structure — treat them as noise to be stripped on apply.

**Also check for corrupted legacy IDs** before trusting any automatic stripping: some older sources use a lettering scheme that overflows past `z` into punctuation or control characters (e.g. `{`, `|`, `}`, `~`, `\xa0`, `\x7f`–`\x81`). A strict `\^[\w-]+\s*$` stripper silently fails to match these, leaving the stale ID in place and appending the new one after it, producing a line with two IDs. Scan for lines with more than one `^` after applying, and for any pre-apply line whose trailing `^`-token isn't fully `[\w-]` — strip those with a tolerant "caret to end of line" regex instead before running Step 3.

### 2 — Confirm runs and assign labels (follow Step C)

For each audited run:

1. Confirm the boundary is a real restart (not OCR / interpolation), or identify a heading-boundary split that the numbers themselves don't show (see "Splitting one detected run into two zones" above).
2. Decide whether one run is genuinely **principal** (bare `^{book}-{N}`) or whether the book's runs are peer/co-equal and should all get positional labels including the first (see Step C).
3. Choose `--zones` label from Step C accordingly.

### 3 — Apply content IDs

```bash
# Example: three runs, the third (body) is principal → its label is empty
python "<this-skill-dir>/apply.py" apply "<path>" --zones "1=1@25,2=2@116,3=@588"

# Entire file is one run → empty label
python "<this-skill-dir>/apply.py" apply "<path>" --zones "1="

# All runs peer/co-equal → every run gets a positional label, none bare
python "<this-skill-dir>/apply.py" apply "<path>" --zones "1=1,2=2,3=3"
```

`--zones "K=LABEL"` maps audit run index `K` → middle segment `LABEL`. Empty `LABEL` (`K=` or `K=@line`) yields `^{book}-{N}`.

The script strips all existing `^` IDs, tags numbered paragraphs, strips `N.` prefixes, normalises blanks. It may put a temporary ID on the chosen run-opening heading; Step 4 replaces heading IDs fully. When a run must be split at a heading with no number reset, or a book needs more zones than `--zones` can express cleanly (dozens of runs), write a short custom script that reuses `apply.py`'s `detect_runs`/`content_id`/`strip_id` helpers directly rather than fighting the CLI.

### 4 — Headings + leftovers

1. Content strictly before the file's first `#` heading of any level → `^T-N`
2. `#` → `^0`; `##` → `^{book}-0`
3. Every `###`/`####`/`#####` → hierarchical IDs by sibling position under each parent (one continuous `###` counter across the whole book)
4. Fix anomaly paragraphs the script skipped (e.g. `N.` not on the first line of a blank-line block — check whether the true numbered line is buried on a later line of the same block; if so, split the block with a blank line before re-running Step 3)
5. Any other stray unnumbered blocks — i.e. ones that come after the first heading but before the first numbering run — get `^{book}-U{k}` (same global counter as in-run `U` blocks), **not** `^T-N`

Confirm: no bare headings; every leading `N.` has a content ID; standalone unnumbered body blocks have `U{k}`; no content ID exceeds 3 hyphen segments; `T-N` appears only on content before the very first heading.

---

## Dos and Don'ts

- **DO** derive structure from headings + leading `N.` only — strip and ignore legacy `^` IDs.
- **DO** copy `N` verbatim into the last segment of the content ID.
- **DO** when the same printed `N` appears again in the same run, keep the first as `…-{N}` and use `…-{N}x1`, `…-{N}x2`, … for later copies.
- **DO** give standalone unnumbered body segments `^{book}-U{k}` (`U` = Unnumbered); reserve `^T-N` for content strictly before the file's first heading (normally just the homage line).
- **DO** start a new run only when the printed number resets to `1` (or at the first number in the file).
- **DON'T** start a new run at every heading — gocchakas and kaṇḍas often sit inside one run.
- **DON'T** classify runs by genre or position — the zone is a collision-breaker only, never a claim that content is "matrix", "intro" or "front matter".
- **DO** give the principal (normally body) run the bare `^{book}-{N}` namespace when one genuinely dominates; label every other run `1`, `2`, … in document order. When runs are peer/co-equal, label all of them positionally instead (no bare exception).
- **DO** collapse a **sole** run to `^{book}-{N}` — no middle segment at all.
- **DO** ID every heading; headings may be longer than 3 segments and are numbered by sibling position, independently of content zones.
- **DON'T** treat "before the first numbered run" as equivalent to "pre-title" — only content before the very first heading is pre-title; everything else unnumbered is `U`-territory.
- **DON'T** assign IDs to `![[...]]` transclusions.
- **DO** collapse multiple blank lines to one before parsing blocks.
- **DO** proactively scan for corrupted/overflowed legacy IDs (non-`[\w-]` characters right after a `^`) before stripping, especially in older or heavily-edited source files — a strict stripper can silently leave stale IDs in place.

---

## Book 7 (Paṭṭhānapāḷi) — resolved design notes

Book 7 exists in the workspace and has been fully processed. What was previously an open, provisional design question is now settled by real content:

- The `paccayuddesa` / `paccayaniddesa` / `Pucchāvāro` → `1. Kusalattikaṃ` boundary (items 1–52 vs. 53 onward) has no number reset, so it was split manually at the `### Kusalattikaṃ` heading per "Splitting one detected run into two zones" above, producing 74 total zones from the audit's 73 auto-detected runs.
- The book's runs are **peer/co-equal** (74 resetting sections, no single dominant body run), so it uses **plain sequential positional labels for every zone, including the first** (`^7-1-{N}` … `^7-74-{N}`) — no bare-principal exception. This was chosen specifically because it keeps every verse ID predictable and searchable across a very large number of zones, which matters more here than shortening the body's own IDs.
- The previously proposed descriptive vocabulary (`T{n}` for tikas, `D{n}` for dukas, fused `D{duka}T{tika}` / `T{tika}D{duka}` cross-reference tokens, and `{mode}{pairing}` stacked tokens) was evaluated against the real file and rejected: it produces systemic collisions — e.g. `T1` (Kusalattikaṃ's own primary exposition) collides with `T1` used again for a tika-led cross-reference section, and several `D{n}` anchors are reused across three different structural layers (primary duka groups, duka-led cross-refs, tika-led cross-refs), producing up to triple collisions on the same token. Plain sequential zoning has no such collisions by construction.
- Book 7 also surfaced two file-specific edge cases worth watching for in any future deeply-nested book: (a) a numbered item whose `N.` sits on a non-first line of its content block (an unnumbered intro/parenthetical line shares the block) — `apply.py`'s run-detector only checks the first line, so these get silently misclassified as unnumbered unless caught and split with a blank line first; (b) the legacy-ID overflow corruption described in the Workflow §1 audit note above, found in both book 6 and book 7.

## Vinaya vault note

In this vault the book numbers are the Vinayapiṭaka order: `1` Pārājikapāḷi, `2` Pācittiyapāḷi (with the Bhikkhunīvibhaṅga), `3` Mahāvaggapāḷi, `4` Cūḷavaggapāḷi, `5` Parivārapāḷi. The book-7 and `M`-zone notes above are Abhidhamma-specific; no Vinaya book has a mātikā or more than one numbering run. The end-to-end Vinaya build (XML → JSON → markdown → these IDs → checks) is `0-INBOX/raw-data/build_all.sh`, using `4-SYSTEM/scripts/tipitaka-xml-to-json/`.
