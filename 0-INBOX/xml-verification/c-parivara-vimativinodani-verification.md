# pi-parivara-vimativinodani (Vimativinodanī-ṭīkā, Parivāra) vs tipitaka-xml — verification

- **Date:** 2026-11-17
- **Vault file:** `1-SOURCES/Commentaries/pi-parivara-vimativinodani.md`
- **Source:** `tipitaka-xml/romn/vin07t.nrf.xml`. The Parivāra part was cut out with [`slice_xml.py`](slice_xml.py):
  - It runs from `Parivāravaṇṇanā` to the end of the file.
  - The part's own homage line and a `Vinayapiṭake` title are added in front (`--prepend-idx 2790,1180`).
  - That is 348 blocks, ending at `Vimativinodanīṭīkā niṭṭhitā.`, the vault file's last line. The slice is `tmp/vin07t-parivara.xml`.
- **Method:** the same as [`c-mahavagga-vimativinodani-verification.md`](c-mahavagga-vimativinodani-verification.md).
- **Outputs:** [`c-parivara-vimativinodani-detail.md`](c-parivara-vimativinodani-detail.md), [`c-parivara-vimativinodani-headings.md`](c-parivara-vimativinodani-headings.md).

## Result: content ✅, headings ✅

| Check | XML slice | Vault | |
|---|---|---|---|
| Lines | 348 | 348 | identical, same order |
| Words added, missing or changed | | | **0** |
| Content block IDs | | `^5-1` … `^5-273` | sequential, no gaps or duplicates |
| Numbered paragraphs | 97 | 97 transclusion groups | every group links exactly the printed number or range |
| Transclusion targets | | 113 → `pi-5.md` | all exist |
| Headings | 66 | 66 | same text, same order |
| Stray digits after `<pb>` | 0 | | |

The 8 lines that the comparison counts as "identical" differ only by the spacing in finding 1.

## Findings

### 1. Spaces the conversion added before punctuation ✅ FIXED 2026-11-17

- **Fixed on the user's approval:** 9 spaces removed on 8 lines, using [`fix_pb_spaces.py`](fix_pb_spaces.py). No other line was touched.
- **After the fix:**
  - Block IDs, transclusion links, the line count and the CRLF line endings are unchanged.
  - The comparison shows 348 / 348 lines identical, with 0 spacing-only differences. A second run of the script finds nothing left.
- A backup of the pre-fix file is in [`backups/`](backups/).
- The uploaded library text still has the old spacing, so it needs a re-upload.
- **No source spaces to keep.**

### 2. The part title sits above its chapters ✅ (deliberate)

- **What the checker reports:** 17 parent differences. They are all of one kind. In the XML, `Parivāravaṇṇanā` is tagged `chapter`, the same as its 17 chapters.
- **What the vault does:** it makes it the `##` title with the chapters under it at `###`. This is the same choice as in the other Vimativinodanī and Sāratthadīpanī parts.
- **No change needed.** The section headings below the chapters match the XML.

### 3. Faithful to the source ℹ️

- **Chapter IDs differ from `pi-5.md`.** The ṭīkā has its own chapter list; for example, it has `Paññattivāravaṇṇanā` and `Samathabhedaṃ` as chapters of their own. So its heading IDs do not line up with the root's. Heading IDs belong to each file, so nothing breaks.
- **The 47 "level mismatches" in the content report are false positives.** The XML has no divs.
