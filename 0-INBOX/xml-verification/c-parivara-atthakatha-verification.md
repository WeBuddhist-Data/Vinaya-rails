# pi-parivara-atthakatha (Samantapāsādikā, Parivāra) vs tipitaka-xml — verification

- **Date:** 2026-11-17
- **Vault file:** `1-SOURCES/Commentaries/pi-parivara-atthakatha.md`
- **Source:** `tipitaka-xml/romn/vin02a4.att.xml` (the whole file). Root text: `pi-5.md`.
- **Method:** the same as [`c-pacittiya-atthakatha-verification.md`](c-pacittiya-atthakatha-verification.md).
- **Outputs:** [`c-parivara-atthakatha-detail.md`](c-parivara-atthakatha-detail.md), [`c-parivara-atthakatha-headings.md`](c-parivara-atthakatha-headings.md).

## Result: content ✅, headings ✅ — no structural issues

| Check | XML | Vault | |
|---|---|---|---|
| Lines | 661 | 661 | identical, same order |
| Words added, missing or changed | | | **0** |
| Content block IDs | | `^5-1` … `^5-533` | sequential, no gaps or duplicates |
| Numbered paragraphs | 114 | 114 transclusion groups | every group links exactly the printed number or range |
| Transclusion targets | | 125 → `pi-5.md` | all exist |
| Headings | 87 | 87 | same text, same order, **same parent for every heading** |
| Stray digits after `<pb>` | 0 | | |

The 52 lines that the comparison counts as "identical" differ only by the spacing in finding 1.

The tree matches the XML exactly: the book title at `##`, the 18 chapters at `###`, and 67 sections at `####`.

## Findings

### 1. Spaces the conversion added before punctuation ✅ FIXED 2026-11-17

- **Fixed on the user's approval:** 57 spaces removed on 52 lines, using [`fix_pb_spaces.py`](fix_pb_spaces.py). No other line was touched.
- **After the fix:**
  - Block IDs, transclusion links, the line count and the CRLF line endings are unchanged.
  - The comparison shows 661 / 661 lines identical, with 0 spacing-only differences. A second run of the script finds nothing left.
- A backup of the pre-fix file is in [`backups/`](backups/).
- The uploaded library text still has the old spacing, so it needs a re-upload.
- **No source spaces to keep.**

### 2. Chapter IDs are one apart from `pi-5.md` from the 7th chapter on ℹ️

The aṭṭhakathā follows the XML's **18** chapters. Its `Atthavasapakaraṇāvaṇṇanā` is a section inside `Uposathādipucchāvissajjanā` (`^5-6-1-0`).

`pi-5.md` instead makes `Atthavasapakaraṇaṃ` a chapter of its own (`^5-7-0`; see [`pi-5-verification.md`](pi-5-verification.md) §3). So from Gāthāsaṅgaṇikaṃ on, the same chapter has different heading IDs in the two files:

| Chapter | here | `pi-5.md` |
|---|---|---|
| Paṭhamagāthāsaṅgaṇikaṃ / Gāthāsaṅgaṇikaṃ | `^5-7-0` | `^5-8-0` |
| … | … | … |
| Pañcavaggo | `^5-18-0` | `^5-19-0` |

Heading IDs belong to each file, and the transclusions point at paragraph IDs, so nothing breaks. If the two TOCs are ever aligned, the cleaner fix is on the root side: treat `Atthavasapakaraṇaṃ` as part of chapter 6, as the XML and tipitaka.org's TOC do.

### 3. Faithful to the source ℹ️

- **The 67 "level mismatches" in the content report are false positives.** The XML has no divs; the parent check finds no differences.
