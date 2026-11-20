# pi-culavagga-yojana (Pācityādiyojanā, Cūḷavagga) vs tipitaka-xml — verification

- **Date:** 2026-11-17
- **Vault file:** `1-SOURCES/Commentaries/pi-culavagga-yojana.md`
- **Source:** `tipitaka-xml/romn/vin12t.nrf.xml`. The Cūḷavagga part was cut out with [`slice_xml.py`](slice_xml.py):
  - It runs from `Cūḷavaggayojanā` up to, not including, the next homage line, which opens the Parivāra part.
  - Three lines are added in front, in the vault's order (`--prepend-idx 1849,1,1850`): the part's own homage line, the file's `Vinayapiṭake` title, and the part's `Pācityādiyojanā` title.
  - That is 574 blocks, ending at `Cūḷavaggakhandhakassa, samatto yojanānayoti.`, the vault file's last line. The slice is `tmp/vin12t-culavagga.xml`.
- **Method:** the same as [`c-mahavagga-yojana-verification.md`](c-mahavagga-yojana-verification.md).
- **Outputs:** [`c-culavagga-yojana-detail.md`](c-culavagga-yojana-detail.md), [`c-culavagga-yojana-headings.md`](c-culavagga-yojana-headings.md), [`c-culavagga-yojana-spaces-kept.md`](c-culavagga-yojana-spaces-kept.md).

## Result: content ✅, headings ✅ (same nesting rule as pi-4)

| Check | XML slice | Vault | |
|---|---|---|---|
| Lines | 574 | 574 | identical, same order |
| Words added, missing or changed | | | **0** |
| Content block IDs | | `^4-1` … `^4-489` | sequential, no gaps or duplicates |
| Numbered paragraphs | 180 | 180 transclusion groups | every group links exactly the printed number or range |
| Transclusion targets | | 181 → `pi-4.md` | all exist |
| Headings | 82 | 82 | same text, same order; 72 have the same parent |
| Stray digits after `<pb>` | 0 | | |

The 39 lines that the comparison counts as "identical" differ only by the spacing in finding 1.

## Findings

### 1. Spaces the conversion added before punctuation ✅ FIXED 2026-11-17

- **Fixed on the user's approval:** 39 spaces removed on 39 lines, using [`fix_pb_spaces.py`](fix_pb_spaces.py). No other line was touched.
- **After the fix:**
  - Block IDs, transclusion links, the line count and the CRLF line endings are unchanged.
  - The comparison shows 574 / 574 lines identical, with 0 spacing-only differences. A second run of the script finds nothing left.
- A backup of the pre-fix file is in [`backups/`](backups/).
- The uploaded library text still has the old spacing, so it needs a re-upload.

The source itself has **4 spaces** before punctuation (B 3, C 1), which stay. The C case is line 230, `āpattisaññī <pb/> . Pahu cāti`.

### 2. `Cūḷavaggayojanā` sits under `Pācityādiyojanā` ✅ (deliberate)

In the XML the work title `Pācityādiyojanā` is a `title` and the part title `Cūḷavaggayojanā` a `chapter`, so by tag the part outranks the work. The vault reads it the natural way:

```
## Pācityādiyojanā        ^4-0
### Cūḷavaggayojanā       ^4-1-0
#### 1. Kammakkhandhakaṃ  ^4-1-1-0 …
```

This is the same shape as the Pācittiya Yojanā. No change needed.

### 3. Nine unnumbered kathās nested under the numbered one before them ℹ️ (the vault's rule from pi-3 and pi-4)

In the XML these are flat `subhead`s under their khandhaka. The vault puts each one level deeper, under the numbered kathā before it:

| Line | Heading | Nested under |
|---|---|---|
| 50, 64 | `Adhammakammadvādasakakathā`, `Nappaṭippassambhetabbaaṭṭhārasakādikathā` | `1. Tajjanīyakammakathā` |
| 92 | `Adhammakammādidvādasakakathā` | `4. Paṭisāraṇīyakammakathā` |
| 312–338 | `Paṭicchanna-`, `Samodhāna-`, `Agghasamodhāna-`, `Suddhantaparivāsādikathā` | `2. Parivāsakathā` |
| 491, 499 | `Tividhasalākaggāhakathā`, `Tassapāpiyasikāvinayakathā` | `9. Adhikaraṇavūpasamanasamathakathā` |

- **The same rule as the root text.** `pi-4.md` nests its `Adhammakammadvādasakaṃ` under `1. Tajjanīyakammaṃ` the same way.
- **✅ Decision (2026-11-17): kept** as this vault's convention, registered in [`vault-annex.md`](../../4-SYSTEM/Guidelines/vault-annex.md) §2 "Registered deviations". Each of the nine belongs to the numbered kathā above it, so no change to the file.

### 4. Faithful to the source ℹ️

- **The 79 "level mismatches" in the content report are false positives.** The XML has no divs.
