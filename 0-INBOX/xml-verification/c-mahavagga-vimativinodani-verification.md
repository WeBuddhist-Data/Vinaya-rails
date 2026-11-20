# pi-mahavagga-vimativinodani (Vimativinodanī-ṭīkā, Mahāvagga) vs tipitaka-xml — verification

- **Date:** 2026-11-17
- **Vault file:** `1-SOURCES/Commentaries/pi-mahavagga-vimativinodani.md`
- **Source:** `tipitaka-xml/romn/vin07t.nrf.xml`. The Mahāvagga part was cut out with [`slice_xml.py`](slice_xml.py):
  - It runs from `Mahāvaggavaṇṇanā` up to, not including, the next homage line, which opens the Cūḷavaggavaṇṇanā.
  - The part's own homage line and a `Vinayapiṭake` title are added in front (`--prepend-idx 1777,1180`).
  - That is 653 blocks, ending at `Mahāvaggavaṇṇanānayo niṭṭhito.`, the vault file's last line. The slice is `tmp/vin07t-mahavagga.xml`.
- **Method:** the same as [`c-parajika-vajirabuddhi-verification.md`](c-parajika-vajirabuddhi-verification.md).
- **Outputs:** [`c-mahavagga-vimativinodani-detail.md`](c-mahavagga-vimativinodani-detail.md), [`c-mahavagga-vimativinodani-headings.md`](c-mahavagga-vimativinodani-headings.md), [`c-mahavagga-vimativinodani-spaces-kept.md`](c-mahavagga-vimativinodani-spaces-kept.md).

## Result: content ✅, headings ✅

| Check | XML slice | Vault | |
|---|---|---|---|
| Lines | 653 | 652 | 652 identical; the XML's extra line is an empty paragraph (below) |
| Words added, missing or changed | | | **0** |
| Content block IDs | | `^3-1` … `^3-544` | sequential, no gaps or duplicates |
| Numbered paragraphs | 212 | 212 transclusion groups | every group links exactly the printed number or range |
| Transclusion targets | | 252 → `pi-3.md` | all exist |
| Headings | 105 | 105 | same text, same order |
| Stray digits after `<pb>` | 0 | | |

**The empty paragraph.** Before `Adhammikakatikādikathāvaṇṇanā niṭṭhitā.` (vault line 1048), the XML has an empty `<p rend="centre"> </p>`. The vault rightly has no line for it. [`fix_pb_spaces.py`](fix_pb_spaces.py) and [`kept_spaces.py`](kept_spaces.py) now skip empty paragraphs too. Re-running them on pi-1, pi-3, pi-5, the Pārājika aṭṭhakathā and the Pācittiya Yojanā changes nothing.

The 25 lines that the comparison counts as "identical" differ only by the spacing in finding 1.

## Findings

### 1. Spaces the conversion added before punctuation ✅ FIXED 2026-11-17

- **Fixed on the user's approval:** 26 spaces removed on 25 lines, using [`fix_pb_spaces.py`](fix_pb_spaces.py). No other line was touched.
- **After the fix:**
  - Block IDs, transclusion links, the line count and the CRLF line endings are unchanged.
  - The comparison shows 652 identical lines and 0 spacing-only differences. The only remaining hunk is the XML's empty paragraph. A second run of the script finds nothing left.
- A backup of the pre-fix file is in [`backups/`](backups/).
- The uploaded library text still has the old spacing, so it needs a re-upload.

The source itself has **1 space** before punctuation (type B), which stays.

### 2. The part title sits above the khandhakas ✅ (deliberate)

- **What the checker reports:** 10 parent differences. In the XML, `Mahāvaggavaṇṇanā` is tagged `chapter`, the same as the 10 khandhakas.
- **What the vault does:** it makes it the `##` title with the khandhakas under it at `###`. That is the same choice as in the Mahāvagga Sāratthadīpanī, and the same shape as `pi-3.md`.
- **No change needed.** All 93 kathā headings under the khandhakas match the XML.

### 3. Faithful to the source ℹ️

- **The 93 "level mismatches" in the content report are false positives.** The XML has no divs.
