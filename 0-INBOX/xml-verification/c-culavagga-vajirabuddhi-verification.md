# pi-culavagga-vajirabuddhi (Vajirabuddhi-ṭīkā, Cūḷavagga) vs tipitaka-xml — verification

- **Date:** 2026-11-17
- **Vault file:** `1-SOURCES/Commentaries/pi-culavagga-vajirabuddhi.md`
- **Source:** `tipitaka-xml/romn/vin06t.nrf.xml`. The Cūḷavagga part was cut out with [`slice_xml.py`](slice_xml.py):
  - It runs from `Cūḷavaggavaṇṇanā` up to, not including, the next homage line, which opens the Parivāravaṇṇanā.
  - The part's own homage line and the file's `Vinayapiṭake` title are added in front (`--prepend-idx 2215,1`).
  - That is 212 blocks, ending at `Cūḷavaggavaṇṇanā niṭṭhitā.`, the vault file's last line. The slice is `tmp/vin06t-culavagga.xml`.
- **Method:** the same as [`c-parajika-vajirabuddhi-verification.md`](c-parajika-vajirabuddhi-verification.md).
- **Outputs:** [`c-culavagga-vajirabuddhi-detail.md`](c-culavagga-vajirabuddhi-detail.md), [`c-culavagga-vajirabuddhi-headings.md`](c-culavagga-vajirabuddhi-headings.md).

## Result: content ✅, headings ✅ — no structural issues

| Check | XML slice | Vault | |
|---|---|---|---|
| Lines | 212 | 212 | identical, same order |
| Words added, missing or changed | | | **0** |
| Content block IDs | | `^4-1` … `^4-147` | sequential, no gaps or duplicates |
| Numbered paragraphs | 105 | 105 transclusion groups | every group links exactly the printed number or range |
| Transclusion targets | | 128 → `pi-4.md` | all exist |
| Headings | 49 | 49 | same text, same order, **same parent for every heading** |
| Stray digits after `<pb>` | 0 | | |

The 6 lines that the comparison counts as "identical" differ only by the spacing in finding 1.

The tree matches the XML exactly: `Cūḷavaggavaṇṇanā` at `##`, the 12 khandhakas (`title`) at `###`, and 35 kathās (`subhead`) at `####`.

## Findings

### 1. Spaces the conversion added before punctuation ✅ FIXED 2026-11-17

- **Fixed on the user's approval:** 6 spaces removed on 6 lines, using [`fix_pb_spaces.py`](fix_pb_spaces.py). No other line was touched.
- **After the fix:**
  - Block IDs, transclusion links, the line count and the CRLF line endings are unchanged.
  - The comparison shows 212 / 212 lines identical, with 0 spacing-only differences. A second run of the script finds nothing left.
- A backup of the pre-fix file is in [`backups/`](backups/).
- The uploaded library text still has the old spacing, so it needs a re-upload.
- **No source spaces to keep.**

### 2. Faithful to the source ℹ️

- **The 47 "level mismatches" in the content report are false positives.** The XML has no divs; the parent check finds no differences.
