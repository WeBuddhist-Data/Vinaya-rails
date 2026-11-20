# pi-pacittiya-vimativinodani (Vimativinodanī-ṭīkā, Pācittiya) vs tipitaka-xml — verification

- **Date:** 2026-11-17
- **Vault file:** `1-SOURCES/Commentaries/pi-pacittiya-vimativinodani.md`
- **Source:** `tipitaka-xml/romn/vin07t.nrf.xml`, second volume. It was cut out with [`slice_xml.py`](slice_xml.py):
  - It runs from `Vimativinodanī-ṭīkā (dutiyo bhāgo)` up to, not including, the second homage line after it. The first one opens the Bhikkhunīvibhaṅga and belongs to this part; the second opens the Mahāvaggavaṇṇanā.
  - The volume's own homage and `Vinayapiṭake` lines are added in front (`--prepend-idx 1179,1180`).
  - That is 598 blocks, ending at `Ubhatovibhaṅgaṭṭhakathāvaṇṇanā niṭṭhitā.`, the vault file's last line. The slice is `tmp/vin07t-pacittiya.xml`.
- **Method:** the same as [`c-parajika-vajirabuddhi-verification.md`](c-parajika-vajirabuddhi-verification.md).
- **Outputs:** [`c-pacittiya-vimativinodani-detail.md`](c-pacittiya-vimativinodani-detail.md), [`c-pacittiya-vimativinodani-headings.md`](c-pacittiya-vimativinodani-headings.md), [`c-pacittiya-vimativinodani-spaces-kept.md`](c-pacittiya-vimativinodani-spaces-kept.md).

## Result: content ✅, headings ✅ (one misplaced heading)

| Check | XML slice | Vault | |
|---|---|---|---|
| Lines | 598 | 598 | identical, same order |
| Words added, missing or changed | | | **0** |
| Content block IDs | | `^2-1` … `^2-457` | sequential, no gaps or duplicates |
| Numbered paragraphs | 229 | 229 transclusion groups | every group links exactly the printed number or range |
| Transclusion targets | | 444 → `pi-2.md` | all exist |
| Headings | 135 | 135 | same text, same order; 134 have the same parent |
| Stray digits after `<pb>` | 0 | | |

The 15 lines that the comparison counts as "identical" differ only by the spacing in finding 1.

## Findings

### 1. Spaces the conversion added before punctuation ✅ FIXED 2026-11-17

- **Fixed on the user's approval:** 15 spaces removed on 15 lines, using [`fix_pb_spaces.py`](fix_pb_spaces.py). No other line was touched.
- **After the fix:**
  - Block IDs, transclusion links, the line count and the CRLF line endings are unchanged.
  - The comparison shows 598 / 598 lines identical, with 0 spacing-only differences. A second run of the script finds nothing left.
- A backup of the pre-fix file is in [`backups/`](backups/).
- The uploaded library text still has the old spacing, so it needs a re-upload.

The source itself has **1 space** before punctuation (type A), which stays.

### 2. `Bhikkhunīvibhaṅgavaṇṇanā` is an empty heading inside the Sekhiyakaṇḍa ✅ FIXED 2026-11-17

> **Fixed on the user's approval** with [`fix_pacittiya_vimativinodani.py`](fix_pacittiya_vimativinodani.py). It is now `### Bhikkhunīvibhaṅgavaṇṇanā ^2-4-0`, at the kaṇḍas' rank as in the XML. It holds the five bhikkhunī kaṇḍas, `#### 1. Pārājikakaṇḍaṃ ^2-4-1-0` to `#### 5. Pāṭidesanīyakaṇḍaṃ ^2-4-5-0`, the same shape as pi-2 and the other Pācittiya commentaries.
>
> - **What the text says:** "Bhikkhuvibhaṅgavaṇṇanānayo niṭṭhito." and a new homage line come right before the heading.
> - **What changed:** 29 heading lines.
> - **What didn't:** every non-heading line, all 457 content IDs and all 444 root links are unchanged, as are the line count and the CRLF line endings.
> - **Re-check against the XML:** 598 / 598 lines identical, heading IDs consistent with depth, no hierarchy hints.
> - **Parent check:** the 5 remaining parent differences are the bhikkhunī kaṇḍas now under their vibhaṅga, as intended.
> - **Backup:** [`backups/pi-pacittiya-vimativinodani.pre-toc-fix.md.bak`](backups/).
>
> The description below is of the state before the fix.

```
### 7. Sekhiyakaṇḍaṃ                     ^2-3-0
Namo tassa bhagavato arahato …            ^2-368
#### Bhikkhunīvibhaṅgavaṇṇanā             ^2-3-8-0   ← XML: rend="chapter", same rank as the kaṇḍas; here a child of Sekhiya, with no content
### 1. Pārājikakaṇḍaṃ                    ^2-4-0     ← the bhikkhunī kaṇḍas are siblings of the bhikkhu ones
```

- **To match the XML,** it would be a `###` sibling of the kaṇḍas.
- **To match `pi-2.md` and the Pācittiya aṭṭhakathā,** it would also be the parent of the five bhikkhunī kaṇḍas, as `### Bhikkhunīvibhaṅga… ^2-…`. Their heading IDs `^2-4-0` … `^2-8-0` would then change.

### 3. Faithful to the source ℹ️

- **Numbering restart.** The bhikkhunī kaṇḍa numbers restart at 1, which gives the one "numbering restart" hint in the detail report.
- **The 124 "level mismatches" in the content report are false positives.** The XML has no divs.
