# pi-culavagga-vimativinodani (Vimativinodanī-ṭīkā, Cūḷavagga) vs tipitaka-xml — verification

- **Date:** 2026-11-17
- **Vault file:** `1-SOURCES/Commentaries/pi-culavagga-vimativinodani.md`
- **Source:** `tipitaka-xml/romn/vin07t.nrf.xml`. The Cūḷavagga part was cut out with [`slice_xml.py`](slice_xml.py):
  - It runs from `Cūḷavaggavaṇṇanā` up to, not including, the next homage line, which opens the Parivāravaṇṇanā.
  - The part's own homage line and a `Vinayapiṭake` title are added in front (`--prepend-idx 2429,1180`).
  - That is 362 blocks, ending at `Cūḷavaggavaṇṇanānayo niṭṭhito.`, the vault file's last line. The slice is `tmp/vin07t-culavagga.xml`.
- **Method:** the same as [`c-mahavagga-vimativinodani-verification.md`](c-mahavagga-vimativinodani-verification.md).
- **Outputs:** [`c-culavagga-vimativinodani-detail.md`](c-culavagga-vimativinodani-detail.md), [`c-culavagga-vimativinodani-headings.md`](c-culavagga-vimativinodani-headings.md), [`c-culavagga-vimativinodani-spaces-kept.md`](c-culavagga-vimativinodani-spaces-kept.md).

## Result: content ✅, headings ✅

| Check | XML slice | Vault | |
|---|---|---|---|
| Lines | 362 | 362 | identical, same order |
| Words added, missing or changed | | | **0** |
| Content block IDs | | `^4-1` … `^4-309` | sequential, no gaps or duplicates |
| Numbered paragraphs | 135 | 135 transclusion groups | every group links exactly the printed number or range |
| Transclusion targets | | 159 → `pi-4.md` | all exist |
| Headings | 52 | 52 | same text, same order |
| Stray digits after `<pb>` | 0 | | |

The 7 lines that the comparison counts as "identical" differ only by the spacing in finding 1.

## Findings

### 1. Spaces the conversion added before punctuation ✅ FIXED 2026-11-17

- **Fixed on the user's approval:** 7 spaces removed on 7 lines, using [`fix_pb_spaces.py`](fix_pb_spaces.py). No other line was touched.
- **After the fix:**
  - Block IDs, transclusion links, the line count and the CRLF line endings are unchanged.
  - The comparison shows 362 / 362 lines identical, with 0 spacing-only differences. A second run of the script finds nothing left.
- A backup of the pre-fix file is in [`backups/`](backups/).
- The uploaded library text still has the old spacing, so it needs a re-upload.

The source itself has **1 space** before punctuation (type B), which stays.

### 2. The part title sits above the khandhakas ✅ (deliberate)

- **What the checker reports:** 12 parent differences. They are all of one kind. In the XML, `Cūḷavaggavaṇṇanā` is tagged `chapter`, the same as the 12 khandhakas.
- **What the vault does:** it makes it the `##` title with the khandhakas under it at `###`. This is the same choice as in the other Mahāvagga and Cūḷavagga ṭīkās, and the same shape as `pi-4.md`.
- **No change needed.** The 38 kathā headings under the khandhakas match the XML.

### 3. Faithful to the source ℹ️

- **The 38 "level mismatches" in the content report are false positives.** The XML has no divs.
