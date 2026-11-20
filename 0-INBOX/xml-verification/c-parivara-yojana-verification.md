# pi-parivara-yojana (Pācityādiyojanā, Parivāra) vs tipitaka-xml — verification

- **Date:** 2026-11-17
- **Vault file:** `1-SOURCES/Commentaries/pi-parivara-yojana.md`
- **Source:** `tipitaka-xml/romn/vin12t.nrf.xml`. The Parivāra part was cut out with [`slice_xml.py`](slice_xml.py):
  - It runs from `Parivāravaggayojanā` to the end of the file.
  - Three lines are added in front, in the vault's order (`--prepend-idx 2422,1,2423`): the part's own homage line, the file's `Vinayapiṭake` title, and the part's `Pācityādiyojanā` title.
  - That is 571 blocks, ending at `Pācityādivaṇṇanāya yojanā samattā.`, the vault file's last line. The slice is `tmp/vin12t-parivara.xml`.
- **Method:** the same as [`c-culavagga-yojana-verification.md`](c-culavagga-yojana-verification.md).
- **Outputs:** [`c-parivara-yojana-detail.md`](c-parivara-yojana-detail.md), [`c-parivara-yojana-headings.md`](c-parivara-yojana-headings.md), [`c-parivara-yojana-spaces-kept.md`](c-parivara-yojana-spaces-kept.md).

## Result: content ✅, headings ✅

| Check | XML slice | Vault | |
|---|---|---|---|
| Lines | 571 | 571 | identical, same order |
| Words added, missing or changed | | | **0** |
| Content block IDs | | `^5-1` … `^5-474` | sequential, no gaps or duplicates |
| Numbered paragraphs | 109 | 109 transclusion groups | every group links exactly the printed number or range |
| Transclusion targets | | 120 → `pi-5.md` | all exist |
| Headings | 88 | 88 | same text, same order; 87 have the same parent |
| Stray digits after `<pb>` | 0 | | |

The 37 lines that the comparison counts as "identical" differ only by the spacing in finding 1.

## Findings

### 1. Spaces the conversion added before punctuation ✅ FIXED 2026-11-17

- **Fixed on the user's approval:** 38 spaces removed on 37 lines, using [`fix_pb_spaces.py`](fix_pb_spaces.py). No other line was touched.
- **After the fix:**
  - Block IDs, transclusion links, the line count and the CRLF line endings are unchanged.
  - The comparison shows 571 / 571 lines identical, with 0 spacing-only differences. A second run of the script finds nothing left.
- A backup of the pre-fix file is in [`backups/`](backups/).
- The uploaded library text still has the old spacing, so it needs a re-upload.

The source itself has **1 space** before punctuation (type B), which stays.

### 2. `Parivāravaggayojanā` sits under `Pācityādiyojanā` ✅ (deliberate)

This is the same choice as in the Pācittiya and Cūḷavagga Yojanā. The XML tags the work title as `title` and the part title as `chapter`. The vault puts the work title on top:

```
## Pācityādiyojanā        ^5-0
### Parivāravaggayojanā   ^5-1-0
#### …                    (18 chapters)
##### …                   (67 sections)
```

Everything below matches the XML. No change needed.

### 3. Faithful to the source ℹ️

- **The 85 "level mismatches" in the content report are false positives.** The XML has no divs.
