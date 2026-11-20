# pi-culavagga-saratthadipani (Sāratthadīpanī-ṭīkā, Cūḷavagga) vs tipitaka-xml — verification

- **Date:** 2026-11-17
- **Vault file:** `1-SOURCES/Commentaries/pi-culavagga-saratthadipani.md`
- **Source:** `tipitaka-xml/romn/vin02t.tik.xml`. The Cūḷavagga part was cut out with [`slice_xml.py`](slice_xml.py):
  - It runs from `Cūḷavagga-ṭīkā` up to, not including, the next homage line, which opens the Parivāra-ṭīkā.
  - The part's own homage line and the file's `Vinayapiṭake` title are added in front (`--prepend-idx 1751,1`).
  - That is 402 blocks, ending at `Cūḷavaggavaṇṇanā niṭṭhitā.`, the vault file's last line. The slice is `tmp/vin02t-culavagga.xml`.
- **Method:** the same as [`c-mahavagga-saratthadipani-verification.md`](c-mahavagga-saratthadipani-verification.md).
- **Outputs:** [`c-culavagga-saratthadipani-detail.md`](c-culavagga-saratthadipani-detail.md), [`c-culavagga-saratthadipani-headings.md`](c-culavagga-saratthadipani-headings.md), [`c-culavagga-saratthadipani-spaces-kept.md`](c-culavagga-saratthadipani-spaces-kept.md).

## Result: content ✅, headings ✅

| Check | XML slice | Vault | |
|---|---|---|---|
| Lines | 402 | 402 | identical, same order |
| Words added, missing or changed | | | **0** |
| Content block IDs | | `^4-1` … `^4-312` | sequential, no gaps or duplicates |
| Numbered paragraphs | 137 | 137 transclusion groups | every group links exactly the printed number or range |
| Transclusion targets | | 164 → `pi-4.md` | all exist |
| Headings | 79 | 79 | same text, same order |
| Stray digits after `<pb>` | 0 | | |

The 14 lines that the comparison counts as "identical" differ only by the spacing in finding 1.

## Findings

### 1. Spaces the conversion added before punctuation ✅ FIXED 2026-11-17

- **Fixed on the user's approval:** 14 spaces removed on 14 lines, using [`fix_pb_spaces.py`](fix_pb_spaces.py). No other line was touched.
- **After the fix:**
  - Block IDs, transclusion links, the line count and the CRLF line endings are unchanged.
  - The comparison shows 402 / 402 lines identical, with 0 spacing-only differences. A second run of the script finds nothing left.
- A backup of the pre-fix file is in [`backups/`](backups/).
- The uploaded library text still has the old spacing, so it needs a re-upload.

The source itself has **1 space** before punctuation (type B), which stays.

### 2. The part title sits above the khandhakas ✅ (deliberate)

- **What the checker reports:** 12 parent differences. They are all of one kind. In the XML, `Cūḷavagga-ṭīkā` is tagged `chapter`, the same as the 12 khandhakas.
- **What the vault does:** it makes it the `##` title with the khandhakas under it at `###`. This is the same choice as in the Mahāvagga Sāratthadīpanī, and the same shape as `pi-4.md`.
- **No change needed.** All kathā headings under the khandhakas match the XML.

### 3. Faithful to the source ℹ️

- **The 65 "level mismatches" in the content report are false positives.** The XML has no divs.
