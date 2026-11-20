# pi-mahavagga-vajirabuddhi (Vajirabuddhi-ṭīkā, Mahāvagga) vs tipitaka-xml — verification

- **Date:** 2026-11-17
- **Vault file:** `1-SOURCES/Commentaries/pi-mahavagga-vajirabuddhi.md`
- **Source:** `tipitaka-xml/romn/vin06t.nrf.xml`. The Mahāvagga part was cut out with [`slice_xml.py`](slice_xml.py):
  - It runs from `Mahāvaggavaṇṇanā` up to, not including, the next homage line, which opens the Cūḷavaggavaṇṇanā.
  - The part's own homage line and the file's `Vinayapiṭake` title are added in front (`--prepend-idx 1706,1`).
  - That is 510 blocks, ending at `Mahāvaggassa līnatthapakāsanā niṭṭhitā.`, the vault file's last line. The slice is `tmp/vin06t-mahavagga.xml`.
- **Method:** the same as [`c-parajika-vajirabuddhi-verification.md`](c-parajika-vajirabuddhi-verification.md).
- **Outputs:** [`c-mahavagga-vajirabuddhi-detail.md`](c-mahavagga-vajirabuddhi-detail.md), [`c-mahavagga-vajirabuddhi-headings.md`](c-mahavagga-vajirabuddhi-headings.md), [`c-mahavagga-vajirabuddhi-spaces-kept.md`](c-mahavagga-vajirabuddhi-spaces-kept.md).

## Result: content ✅, headings ✅ (the vault's tree is better than the XML's)

| Check | XML slice | Vault | |
|---|---|---|---|
| Lines | 510 | 510 | identical, same order |
| Words added, missing or changed | | | **0** |
| Content block IDs | | `^3-1` … `^3-325` | sequential, no gaps or duplicates |
| Numbered paragraphs | 170 | 170 transclusion groups | every group links exactly the printed number or range |
| Transclusion targets | | 191 → `pi-3.md` | all exist |
| Headings | 114 | 114 | same text, same order |
| Stray digits after `<pb>` | 0 | | |

The 31 lines that the comparison counts as "identical" differ only by the spacing in finding 1.

## Findings

### 1. Spaces the conversion added before punctuation ✅ FIXED 2026-11-17

- **Fixed on the user's approval:** 32 spaces removed on 31 lines, using [`fix_pb_spaces.py`](fix_pb_spaces.py). No other line was touched.
- **After the fix:**
  - Block IDs, transclusion links, the line count and the CRLF line endings are unchanged.
  - The comparison shows 510 / 510 lines identical, with 0 spacing-only differences. A second run of the script finds nothing left.
- A backup of the pre-fix file is in [`backups/`](backups/).
- The uploaded library text still has the old spacing, so it needs a re-upload.

The source itself has **3 spaces** before punctuation (all type B, `word <pb/> …pe…`). These stay.

### 2. Kathās nested under their khandhaka ✅ (the vault improves on the XML)

- **In the XML,** the 10 khandhaka titles and their 102 kathā headings are all flat `subhead`s directly under `Mahāvaggavaṇṇanā`.
- **The vault** nests each kathā under its khandhaka:

  ```
  ## Mahāvaggavaṇṇanā                  ^3-0
  ### 1. Mahākhandhakavaṇṇanā           ^3-1-0
  #### Bodhikathāvaṇṇanā                ^3-1-1-0
  …
  ### 10. Kosambakakkhandhakavaṇṇanā    ^3-10-0
  #### Saṅghasāmaggīkathāvaṇṇanā        ^3-10-5-0
  ```

- **Why the checker flags 102 headings:** they are the kathās, so these are not errors.
- **No change needed.** This is the correct reading, and it gives the same shape as `pi-3.md`, the Mahāvagga aṭṭhakathā and the Sāratthadīpanī.

### 3. Faithful to the source ℹ️

- **The 102 "level mismatches" in the content report are the same headings.** They are not errors.
