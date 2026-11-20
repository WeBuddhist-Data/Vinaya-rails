# pi-parivara-vajirabuddhi (Vajirabuddhi-ṭīkā, Parivāra) vs tipitaka-xml — verification

- **Date:** 2026-11-17
- **Vault file:** `1-SOURCES/Commentaries/pi-parivara-vajirabuddhi.md`
- **Source:** `tipitaka-xml/romn/vin06t.nrf.xml`. The Parivāra part was cut out with [`slice_xml.py`](slice_xml.py):
  - It runs from `Parivāravaṇṇanā` to the end of the file.
  - The part's own homage line and the file's `Vinayapiṭake` title are added in front (`--prepend-idx 2426,1`).
  - That is 248 blocks, ending at `Vajirabuddhiṭīkā niṭṭhitā.`, the vault file's last line. The slice is `tmp/vin06t-parivara.xml`.
- **Method:** the same as [`c-parajika-vajirabuddhi-verification.md`](c-parajika-vajirabuddhi-verification.md).
- **Outputs:** [`c-parivara-vajirabuddhi-detail.md`](c-parivara-vajirabuddhi-detail.md), [`c-parivara-vajirabuddhi-headings.md`](c-parivara-vajirabuddhi-headings.md).

## Result: content ✅, headings ✅ — no structural issues

| Check | XML slice | Vault | |
|---|---|---|---|
| Lines | 248 | 248 | identical, same order |
| Words added, missing or changed | | | **0** |
| Content block IDs | | `^5-1` … `^5-144` | sequential, no gaps or duplicates |
| Numbered paragraphs | 94 | 94 transclusion groups | every group links exactly the printed number or range |
| Transclusion targets | | 106 → `pi-5.md` | all exist |
| Headings | 78 | 78 | same text, same order, **same parent for every heading** |
| Stray digits after `<pb>` | 0 | | |

The 9 lines that the comparison counts as "identical" differ only by the spacing in finding 1.

The tree matches the XML exactly: `Parivāravaṇṇanā` at `##`, 17 sections (`title`) at `###`, and 59 subsections (`subhead`) at `####`.

## Findings

### 1. Spaces the conversion added before punctuation ✅ FIXED 2026-11-17

- **Fixed on the user's approval:** 10 spaces removed on 9 lines, using [`fix_pb_spaces.py`](fix_pb_spaces.py). No other line was touched.
- **After the fix:**
  - Block IDs, transclusion links, the line count and the CRLF line endings are unchanged.
  - The comparison shows 248 / 248 lines identical, with 0 spacing-only differences. A second run of the script finds nothing left.
- A backup of the pre-fix file is in [`backups/`](backups/).
- The uploaded library text still has the old spacing, so it needs a re-upload.
- **No source spaces to keep.**

### 2. Faithful to the source ℹ️

- **Chapter IDs differ from `pi-5.md`.** The ṭīkā has its own set of 17 chapters, so its heading IDs do not line up with the root's. Heading IDs belong to each file, so nothing breaks.
- **The 76 "level mismatches" in the content report are false positives.** The XML has no divs; the parent check finds no differences.
