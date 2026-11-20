# pi-pacittiya-atthakatha (Samantapāsādikā, Pācittiya) vs tipitaka-xml — verification

- **Date:** 2026-11-17
- **Vault file:** `1-SOURCES/Commentaries/pi-pacittiya-atthakatha.md`
- **Source:** `tipitaka-xml/romn/vin02a1.att.xml` (the whole file). Root text: `pi-2.md`.
- **Method:** the same as [`c-parajika-atthakatha-verification.md`](c-parajika-atthakatha-verification.md), using [`check_links.py`](check_links.py) and [`compare_headings.py`](compare_headings.py).
- **Outputs:** [`c-pacittiya-atthakatha-detail.md`](c-pacittiya-atthakatha-detail.md), [`c-pacittiya-atthakatha-headings.md`](c-pacittiya-atthakatha-headings.md).

## Result: content ✅, headings ✅

| Check | XML | Vault | |
|---|---|---|---|
| Lines | 1,466 | 1,466 | identical, same order |
| Words added, missing or changed | | | **0** |
| Content block IDs | | `^2-1` … `^2-1185` | sequential, no gaps or duplicates |
| Numbered paragraphs | 463 | 463 transclusion groups | every group links exactly the printed number or range |
| Transclusion targets | | 524 → `pi-2.md` | all exist |
| Headings | 246 | 246 | same text, same order; 245 have the same parent (the other is finding 2) |
| Stray digits after `<pb>` | 1 | 1 | finding 3 |

The 89 lines that the comparison counts as "identical" differ only by the spacing in finding 1.

## Findings

### 1. Spaces the conversion added before punctuation ✅ FIXED 2026-11-17

- **Fixed on the user's approval:** 92 spaces removed on 89 lines, using [`fix_pb_spaces.py`](fix_pb_spaces.py). No other line was touched.
- **After the fix:**
  - Block IDs, transclusion links, the line count and the CRLF line endings are unchanged.
  - The comparison shows 1,466 / 1,466 lines identical, with 0 spacing-only differences. A second run of the script finds nothing left.
- A backup of the pre-fix file is in [`backups/`](backups/).
- The uploaded library text still has the old spacing, so it needs a re-upload.
- **No source spaces to keep.** This file has none of types A–D.

### 2. `Bhikkhunīvibhaṅgavaṇṇanā` sits under the book title ✅ (deliberate, matches the root text)

- In the XML this heading is `rend="book"`, the same rank as `Pācittiya-aṭṭhakathā`.
- The vault puts it one level lower, `### Bhikkhunīvibhaṅgavaṇṇanā ^2-5-0`, beside the kaṇḍas 5–8. This is the same place and the same ID as `### Bhikkhunīvibhaṅgo ^2-5-0` in `pi-2.md`, where the XML's `subbook` div sits inside the book.
- So the commentary's tree lines up with its root. **No change needed.**

### 3. Stray digit in the source ℹ️

- Line 1318 reads `Acelakavaggassa 9 paṭhamasikkhāpada…`. The XML has `Acelakavaggassa <pb ed="M" n="0.0121"/><pb ed="V" n="0.0109"/>9 paṭhamasikkhāp…`.
- This is the vin02a1 case noted earlier, and the `deva master` file has the same digit. It is VRI's typo, faithfully copied. Leave it, or mark it with `[Ed: …]`.
