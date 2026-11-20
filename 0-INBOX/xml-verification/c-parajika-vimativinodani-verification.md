# pi-parajika-vimativinodani (Vimativinodanī-ṭīkā, Pārājika) vs tipitaka-xml — verification

- **Date:** 2026-11-17
- **Vault file:** `1-SOURCES/Commentaries/pi-parajika-vimativinodani.md`
- **Source:** `tipitaka-xml/romn/vin07t.nrf.xml`, which holds the Vimativinodanī on all five books. The Pārājika part is the first volume (`paṭhamo bhāgo`). It was cut out with [`slice_xml.py`](slice_xml.py), from the first homage line up to, not including, the second one that opens the `dutiyo bhāgo`. That is 1,179 of 3,137 blocks, ending at `Paṭhamo bhāgo niṭṭhito.`, the vault file's last line. The slice is `tmp/vin07t-parajika.xml`.
- **Method:** the same as [`c-parajika-vajirabuddhi-verification.md`](c-parajika-vajirabuddhi-verification.md).
- **Outputs:** [`c-parajika-vimativinodani-detail.md`](c-parajika-vimativinodani-detail.md), [`c-parajika-vimativinodani-headings.md`](c-parajika-vimativinodani-headings.md), [`c-parajika-vimativinodani-spaces-kept.md`](c-parajika-vimativinodani-spaces-kept.md).

## Result: content ✅, headings ✅ (one small nesting slip)

| Check | XML slice | Vault | |
|---|---|---|---|
| Lines | 1,179 | 1,179 | identical, same order |
| Words added, missing or changed | | | **0** |
| Content block IDs | | `^1-1` … `^1-1025` | sequential, no gaps or duplicates |
| Numbered paragraphs | 279 | 279 transclusion groups | every group links exactly the printed number or range |
| Transclusion targets | | 330 → `pi-1.md` | all exist |
| Headings | 138 | 138 | same text, same order; 137 have the same parent |
| Stray digits after `<pb>` | 0 | | |

The 71 lines that the comparison counts as "identical" differ only by the spacing in finding 1.

## Findings

### 1. Spaces the conversion added before punctuation ✅ FIXED 2026-11-17

- **Fixed on the user's approval:** 71 spaces removed on 71 lines, using [`fix_pb_spaces.py`](fix_pb_spaces.py). No other line was touched.
- **After the fix:**
  - Block IDs, transclusion links, the line count and the CRLF line endings are unchanged.
  - The comparison shows 1,179 / 1,179 lines identical, with 0 spacing-only differences. A second run of the script finds nothing left.
- A backup of the pre-fix file is in [`backups/`](backups/).
- The uploaded library text still has the old spacing, so it needs a re-upload.

The source itself has **4 spaces** before punctuation (B 2, C 1, D 1). These stay. The C case is line 265, `voharati <pb/>. Paccatthi…`.

### 2. `Nigamanavaṇṇanā` one level too deep ✅ FIXED 2026-11-17

> **Fixed on the user's approval** with [`promote_heading.py`](promote_heading.py). It is now `#### Nigamanavaṇṇanā ^1-6-14-0`, a sibling of the 13 rules.
> - One heading line changed; all other lines, IDs and links are unchanged.
> - The heading parent check now finds **0** differences from the XML.
> - Backup: [`backups/pi-parajika-vimativinodani.pre-toc-fix.md.bak`](backups/).

This is the same slip as in the aṭṭhakathā and the Sāratthadīpanī. `##### Nigamanavaṇṇanā ^1-6-13-1-0` (line 2314) sits under `13. Kuladūsakasikkhāpadavaṇṇanā`. In the XML it is a sibling of the 13 rules, under `2. Saṅghādisesakaṇḍo`.

Apart from this, the heading tree matches the XML: one `##` volume heading, the five kaṇḍa `chapter`s at `###`, and their sections below.

### 3. Faithful to the source ℹ️

- **The 129 "level mismatches" in the content report are false positives.** The XML has no divs, and the parent check replaces that test.
