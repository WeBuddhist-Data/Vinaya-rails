# pi-mahavagga-saratthadipani (Sāratthadīpanī-ṭīkā, Mahāvagga) vs tipitaka-xml — verification

- **Date:** 2026-11-17
- **Vault file:** `1-SOURCES/Commentaries/pi-mahavagga-saratthadipani.md`
- **Source:** `tipitaka-xml/romn/vin02t.tik.xml`. The Mahāvagga part was cut out with [`slice_xml.py`](slice_xml.py):
  - It runs from `Mahāvagga-ṭīkā` up to, not including, the next homage line, which opens the Cūḷavagga-ṭīkā.
  - The part's own homage line and the file's `Vinayapiṭake` title are added in front, in the vault's order (`--prepend-idx 715,1`). The XML gives `Vinayapiṭake` only once, at the top of the file, and the vault repeats it at the top of every part.
  - That is 1,037 blocks, ending at `Mahāvaggavaṇṇanā niṭṭhitā.`, the vault file's last line. The slice is `tmp/vin02t-mahavagga.xml`.
- **Method:** the same as [`c-parajika-vajirabuddhi-verification.md`](c-parajika-vajirabuddhi-verification.md).
- **Outputs:** [`c-mahavagga-saratthadipani-detail.md`](c-mahavagga-saratthadipani-detail.md), [`c-mahavagga-saratthadipani-headings.md`](c-mahavagga-saratthadipani-headings.md).

## Result: content ✅, headings ✅

| Check | XML slice | Vault | |
|---|---|---|---|
| Lines | 1,037 | 1,037 | identical, same order |
| Words added, missing or changed | | | **0** |
| Content block IDs | | `^3-1` … `^3-766` | sequential, no gaps or duplicates |
| Numbered paragraphs | 210 | 210 transclusion groups | every group links exactly the printed number or range |
| Transclusion targets | | 251 → `pi-3.md` | all exist |
| Headings | 145 | 145 | same text, same order |
| Stray digits after `<pb>` | 0 | | |

The 49 lines that the comparison counts as "identical" differ only by the spacing in finding 1.

## Findings

### 1. Spaces the conversion added before punctuation ✅ FIXED 2026-11-17

- **Fixed on the user's approval:** 51 spaces removed on 49 lines, using [`fix_pb_spaces.py`](fix_pb_spaces.py). No other line was touched.
- **After the fix:**
  - Block IDs, transclusion links, the line count and the CRLF line endings are unchanged.
  - The comparison shows 1,037 / 1,037 lines identical, with 0 spacing-only differences. A second run of the script finds nothing left.
- A backup of the pre-fix file is in [`backups/`](backups/).
- The uploaded library text still has the old spacing, so it needs a re-upload.
- **No source spaces to keep.**

### 2. The part title sits above the khandhakas ✅ (deliberate)

- **What the checker reports:** 10 parent differences. In the XML, `Mahāvagga-ṭīkā` is tagged `chapter`, the same as the 10 khandhakas, so by tag they are siblings.
- **What the vault does:** it makes `Mahāvagga-ṭīkā` the `##` title with the khandhakas under it at `###`. That is the book's own title over its chapters, the same shape as the Pācittiya part (`## Sāratthadīpanī-ṭīkā (tatiyo bhāgo)`) and as `pi-3.md`.
- **No change needed.** Under the khandhakas, all 133 kathā headings match the XML.

### 3. Faithful to the source ℹ️

- **The 133 "level mismatches" in the content report are false positives.** The XML has no divs.
