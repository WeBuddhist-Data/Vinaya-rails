# pi-pacittiya-saratthadipani (Sāratthadīpanī-ṭīkā, Pācittiya) vs tipitaka-xml — verification

- **Date:** 2026-11-17
- **Vault file:** `1-SOURCES/Commentaries/pi-pacittiya-saratthadipani.md`
- **Source:** `tipitaka-xml/romn/vin02t.tik.xml` (Sāratthadīpanī volume 3, on the four later books). The Pācittiya part was cut out with [`slice_xml.py`](slice_xml.py), from the first homage line up to, not including, the **third** one, which opens `Mahāvagga-ṭīkā` (`--to-nth 2`). The second homage line opens the Bhikkhunīvibhaṅga and belongs to this part. That is 715 of 2,401 blocks, ending at `Pācittiyavaṇṇanā niṭṭhitā.`, the vault file's last line. The slice is `tmp/vin02t-pacittiya.xml`.
- **Method:** the same as [`c-parajika-vajirabuddhi-verification.md`](c-parajika-vajirabuddhi-verification.md).
- **Outputs:** [`c-pacittiya-saratthadipani-detail.md`](c-pacittiya-saratthadipani-detail.md), [`c-pacittiya-saratthadipani-headings.md`](c-pacittiya-saratthadipani-headings.md).

## Result: content ✅, headings ✅

| Check | XML slice | Vault | |
|---|---|---|---|
| Lines | 715 | 715 | identical, same order |
| Words added, missing or changed | | | **0** |
| Content block IDs | | `^2-1` … `^2-566` | sequential, no gaps or duplicates |
| Numbered paragraphs | 233 | 233 transclusion groups | every group links exactly the printed number or range |
| Transclusion targets | | 325 → `pi-2.md` | all exist |
| Headings | 130 | 130 | same text, same order, **same parent for every heading** |
| Stray digits after `<pb>` | 0 | | |

The 35 lines that the comparison counts as "identical" differ only by the spacing in finding 1.

## Findings

### 1. Spaces the conversion added before punctuation ✅ FIXED 2026-11-17

- **Fixed on the user's approval:** 37 spaces removed on 35 lines, using [`fix_pb_spaces.py`](fix_pb_spaces.py). No other line was touched.
- **After the fix:**
  - Block IDs, transclusion links, the line count and the CRLF line endings are unchanged.
  - The comparison shows 715 / 715 lines identical, with 0 spacing-only differences. A second run of the script finds nothing left.
- A backup of the pre-fix file is in [`backups/`](backups/).
- The uploaded library text still has the old spacing, so it needs a re-upload.
- **No source spaces to keep.**

### 2. Faithful to the source ℹ️

- **No Bhikkhunīvibhaṅga heading.** The XML marks the start of the Bhikkhunīvibhaṅga only with a second homage line, which the vault keeps as text (`^2-454`, line 1574). The five bhikkhunī kaṇḍas follow as `###` siblings of the bhikkhu kaṇḍas, each labelled `(bhikkhunīvibhaṅgavaṇṇanā)`.
  - That is why the kaṇḍa numbers restart at 1, and why the detail report gives one "numbering restart" hint.
  - So the heading IDs differ from the root and the aṭṭhakathā: here `^2-5-0` is the bhikkhunī Saṅghādisesakaṇḍa, while in `pi-2.md` and the aṭṭhakathā it is the Bhikkhunīvibhaṅga itself. Heading IDs are per file, so nothing breaks. Keep this in mind if the commentaries' TOCs are ever aligned with the root's.
- **No `8. Sattādhikaraṇasamathā`.** The ṭīkā has no section on it, as in the source.
- **The 120 "level mismatches" in the content report are false positives.** The parent check finds no differences.
