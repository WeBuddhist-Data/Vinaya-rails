# pi-mahavagga-atthakatha (Samantapāsādikā, Mahāvagga) vs tipitaka-xml — verification

- **Date:** 2026-11-17
- **Vault file:** `1-SOURCES/Commentaries/pi-mahavagga-atthakatha.md`
- **Source:** `tipitaka-xml/romn/vin02a2.att.xml` (the whole file). Root text: `pi-3.md`.
- **Method:** the same as [`c-pacittiya-atthakatha-verification.md`](c-pacittiya-atthakatha-verification.md).
- **Outputs:** [`c-mahavagga-atthakatha-detail.md`](c-mahavagga-atthakatha-detail.md), [`c-mahavagga-atthakatha-headings.md`](c-mahavagga-atthakatha-headings.md), [`c-mahavagga-atthakatha-spaces-kept.md`](c-mahavagga-atthakatha-spaces-kept.md).

## Result: content ✅, headings ✅ — no structural issues

| Check | XML | Vault | |
|---|---|---|---|
| Lines | 922 | 922 | identical, same order |
| Words added, missing or changed | | | **0** |
| Content block IDs | | `^3-1` … `^3-757` | sequential, no gaps or duplicates |
| Numbered paragraphs | 275 | 275 transclusion groups | every group links exactly the printed number or range |
| Transclusion targets | | 303 → `pi-3.md` | all exist |
| Headings | 141 | 141 | same text, same order, **same parent for every heading** |
| Stray digits after `<pb>` | 0 | | |

The 77 lines that the comparison counts as "identical" differ only by the spacing in finding 1.

The tree is simple and matches the XML exactly: the book title at `##`, 10 khandhaka `chapter`s at `###`, and 129 kathā `subhead`s at `####`.

## Findings

### 1. Spaces the conversion added before punctuation ✅ FIXED 2026-11-17

- **Fixed on the user's approval:** 80 spaces removed on 77 lines, using [`fix_pb_spaces.py`](fix_pb_spaces.py). No other line was touched.
- **After the fix:**
  - Block IDs, transclusion links, the line count and the CRLF line endings are unchanged.
  - The comparison shows 922 / 922 lines identical, with 0 spacing-only differences. A second run of the script finds nothing left.
- A backup of the pre-fix file is in [`backups/`](backups/).
- The uploaded library text still has the old spacing, so it needs a re-upload.

The source itself has **1 space** before punctuation (C), which stays: line 2076, `ovaṭṭikaṃ <pb/> . Kaṇḍusaka…`.

### 2. Faithful to the source ℹ️

- **The 129 "level mismatches" in the content report are false positives.** The XML has no divs; the parent check finds no differences.
