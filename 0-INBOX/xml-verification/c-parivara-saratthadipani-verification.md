# pi-parivara-saratthadipani (Sāratthadīpanī-ṭīkā, Parivāra) vs tipitaka-xml — verification

- **Date:** 2026-11-17
- **Vault file:** `1-SOURCES/Commentaries/pi-parivara-saratthadipani.md`
- **Source:** `tipitaka-xml/romn/vin02t.tik.xml`. The Parivāra part was cut out with [`slice_xml.py`](slice_xml.py):
  - It runs from `Parivāra-ṭīkā` to the end of the file.
  - The part's own homage line and the file's `Vinayapiṭake` title are added in front (`--prepend-idx 2152,1`).
  - That is 250 blocks, ending at `Sāratthadīpanī nāma vinayaṭīkā niṭṭhitā.`, the vault file's last line. The slice is `tmp/vin02t-parivara.xml`.
- **Method:** the same as [`c-mahavagga-saratthadipani-verification.md`](c-mahavagga-saratthadipani-verification.md).
- **Outputs:** [`c-parivara-saratthadipani-detail.md`](c-parivara-saratthadipani-detail.md), [`c-parivara-saratthadipani-headings.md`](c-parivara-saratthadipani-headings.md), [`c-parivara-saratthadipani-spaces-kept.md`](c-parivara-saratthadipani-spaces-kept.md).

## Result: content ✅, headings ✅

| Check | XML slice | Vault | |
|---|---|---|---|
| Lines | 250 | 250 | identical, same order |
| Words added, missing or changed | | | **0** |
| Content block IDs | | `^5-1` … `^5-173` | sequential, no gaps or duplicates |
| Numbered paragraphs | 74 | 74 transclusion groups | every group links exactly the printed number or range |
| Transclusion targets | | 80 → `pi-5.md` | all exist |
| Headings | 64 | 64 | same text, same order |
| Stray digits after `<pb>` | 0 | | |

The 5 lines that the comparison counts as "identical" differ only by the spacing in finding 1.

## Findings

### 1. Spaces the conversion added before punctuation ✅ FIXED 2026-11-17

- **Fixed on the user's approval:** 5 spaces removed on 5 lines, using [`fix_pb_spaces.py`](fix_pb_spaces.py). No other line was touched.
- **After the fix:**
  - Block IDs, transclusion links, the line count and the CRLF line endings are unchanged.
  - The comparison shows 250 / 250 lines identical, with 0 spacing-only differences. A second run of the script finds nothing left.
- A backup of the pre-fix file is in [`backups/`](backups/).
- The uploaded library text still has the old spacing, so it needs a re-upload.

The source itself has **1 space** before punctuation (type B), which stays.

### 2. The part title sits above its chapters ✅ (deliberate)

- **What the checker reports:** 15 parent differences. They are all of one kind. In the XML, `Parivāra-ṭīkā` is tagged `chapter`, the same as its 15 chapters.
- **What the vault does:** it makes it the `##` title with the chapters under it at `###`, the same choice as in the other Sāratthadīpanī parts.
- **No change needed.** The 47 section headings below the chapters match the XML.

### 3. Faithful to the source ℹ️

- **Only 15 chapters.** The ṭīkā comments on fewer chapters than the Parivāra has. For example, `Saṅgāmadvayavaṇṇanā` covers Cūḷasaṅgāma and Mahāsaṅgāma together, and there is no Khandhakapucchāvāra or Codanākaṇḍa. So its chapter IDs do not line up with `pi-5.md`'s. Heading IDs belong to each file, so nothing breaks.
- **The 47 "level mismatches" in the content report are false positives.** The XML has no divs.
