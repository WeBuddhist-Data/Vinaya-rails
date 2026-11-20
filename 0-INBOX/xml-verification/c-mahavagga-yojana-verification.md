# pi-mahavagga-yojana (Pācityādiyojanā, Mahāvagga) vs tipitaka-xml — verification

- **Date:** 2026-11-17
- **Vault file:** `1-SOURCES/Commentaries/pi-mahavagga-yojana.md`
- **Source:** `tipitaka-xml/romn/vin12t.nrf.xml`. The Mahāvagga part was cut out with [`slice_xml.py`](slice_xml.py):
  - It runs from `Mahāvaggayojanā` up to, not including, the next homage line, which opens the Cūḷavaggayojanā.
  - The part's own homage line and the file's `Vinayapiṭake` title are added in front (`--prepend-idx 1004,1`).
  - That is 846 blocks, ending at `Mahāvaggakhandhakassa, samatto yojanānayoti.`, the vault file's last line. The slice is `tmp/vin12t-mahavagga.xml`.
- **Method:** the same as [`c-parajika-vajirabuddhi-verification.md`](c-parajika-vajirabuddhi-verification.md).
- **Outputs:** [`c-mahavagga-yojana-detail.md`](c-mahavagga-yojana-detail.md), [`c-mahavagga-yojana-headings.md`](c-mahavagga-yojana-headings.md).

## Result: content ✅, headings ✅ (same nesting rule as pi-3)

| Check | XML slice | Vault | |
|---|---|---|---|
| Lines | 846 | 846 | identical, same order |
| Words added, missing or changed | | | **0** |
| Content block IDs | | `^3-1` … `^3-690` | sequential, no gaps or duplicates |
| Numbered paragraphs | 272 | 272 transclusion groups | every group links exactly the printed number or range |
| Transclusion targets | | 286 → `pi-3.md` | all exist |
| Headings | 152 | 152 | same text, same order; 147 have the same parent |
| Stray digits after `<pb>` | 0 | | |

The 76 lines that the comparison counts as "identical" differ only by the spacing in finding 1.

## Findings

### 1. Spaces the conversion added before punctuation ✅ FIXED 2026-11-17

- **Fixed on the user's approval:** 81 spaces removed on 76 lines, using [`fix_pb_spaces.py`](fix_pb_spaces.py). No other line was touched.
- **After the fix:**
  - Block IDs, transclusion links, the line count and the CRLF line endings are unchanged.
  - The comparison shows 846 / 846 lines identical, with 0 spacing-only differences. A second run of the script finds nothing left.
- A backup of the pre-fix file is in [`backups/`](backups/).
- The uploaded library text still has the old spacing, so it needs a re-upload.
- **No source spaces to keep.**

### 2. Five unnumbered kathās nested under the numbered one before them ℹ️ (the vault's rule from pi-3 and pi-4)

In the XML these are flat `subhead`s directly under their khandhaka, like the numbered kathās. The vault puts each one level deeper, under the numbered kathā before it:

| Line | Heading | Nested under |
|---|---|---|
| 348 | `Nasammāvattanādikathā` | `16. Saddhivihārikavattakathā` |
| 358 | `Rādhabrāhmaṇavatthukathā` | `16. Saddhivihārikavattakathā` |
| 396 | `Āṇattivinicchayo` | `22. Nissayapaṭippassaddhikathā` |
| 408 | `Samodhānavinicchayo` | `22. Nissayapaṭippassaddhikathā` |
| 1393 | `Soṇassa pabbajjākathā` | `147. Soṇakoḷivisavatthukathā` |

- **The same rule as the root texts.** `pi-3.md` has the same rule; its `Soṇassa pabbajjā` is nested the same way. `pi-4.md` applies it to 123 headings.
- **✅ Decision (2026-11-17): kept** as this vault's convention, registered in [`vault-annex.md`](../../4-SYSTEM/Guidelines/vault-annex.md) §2 "Registered deviations". Each of the five belongs to the numbered kathā above it, so no change to the file.

### 3. Faithful to the source ℹ️

- **One numbering hint.** The kathā numbers run continuously across the book (`147.` in the 5th khandhaka), as in `pi-3.md`, and this gives the one "numbering restart" hint in the detail report.
- **The 150 "level mismatches" in the content report are false positives.** The XML has no divs.
