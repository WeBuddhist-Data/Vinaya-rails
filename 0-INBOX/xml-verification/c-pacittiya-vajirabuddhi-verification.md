# pi-pacittiya-vajirabuddhi (Vajirabuddhi-ṭīkā, Pācittiya) vs tipitaka-xml — verification

- **Date:** 2026-11-17
- **Vault file:** `1-SOURCES/Commentaries/pi-pacittiya-vajirabuddhi.md`
- **Source:** `tipitaka-xml/romn/vin06t.nrf.xml`. The Pācittiya part was cut out with [`slice_xml.py`](slice_xml.py):
  - It runs from the `Pācittiyavaṇṇanā` chapter heading up to, not including, the second homage line after it. The first one opens the Bhikkhunīvibhaṅgavaṇṇanā and belongs to this part; the second opens the Mahāvaggavaṇṇanā.
  - The file's `Vinayapiṭake` title is added in front (`--prepend-idx 1`), because the vault repeats it at the top of every part.
  - That is 716 blocks, ending at `Ubhatovibhaṅgaṭṭhakathāvaṇṇanā niṭṭhitā.`, the vault file's last line. The slice is `tmp/vin06t-pacittiya.xml`.
- **Method:** the same as [`c-parajika-vajirabuddhi-verification.md`](c-parajika-vajirabuddhi-verification.md).
- **Outputs:** [`c-pacittiya-vajirabuddhi-detail.md`](c-pacittiya-vajirabuddhi-detail.md), [`c-pacittiya-vajirabuddhi-headings.md`](c-pacittiya-vajirabuddhi-headings.md), [`c-pacittiya-vajirabuddhi-spaces-kept.md`](c-pacittiya-vajirabuddhi-spaces-kept.md).

## Result: content ✅, heading tree ⚠️ (inherited from the XML)

| Check | XML slice | Vault | |
|---|---|---|---|
| Lines | 716 | 716 | identical, same order |
| Words added, missing or changed | | | **0** |
| Content block IDs | | `^2-1` … `^2-499` | sequential, no gaps or duplicates |
| Numbered paragraphs | 251 | 251 transclusion groups | every group links exactly the printed number or range |
| Transclusion targets | | 351 → `pi-2.md` | all exist |
| Headings | 196 | 196 | same text, same order |
| Stray digits after `<pb>` | 0 | | |

The 21 lines that the comparison counts as "identical" differ only by the spacing in finding 1.

## Findings

### 1. Spaces the conversion added before punctuation ✅ FIXED 2026-11-17

- **Fixed on the user's approval:** 23 spaces removed on 21 lines, using [`fix_pb_spaces.py`](fix_pb_spaces.py). No other line was touched.
- **After the fix:**
  - Block IDs, transclusion links, the line count and the CRLF line endings are unchanged.
  - The comparison shows 716 / 716 lines identical, with 0 spacing-only differences. A second run of the script finds nothing left.
- A backup of the pre-fix file is in [`backups/`](backups/).
- The uploaded library text still has the old spacing, so it needs a re-upload.

The source itself has **1 space** before punctuation (C), which stays: line 472, `gaṇhanti <pb/>, gaṇabhoja…`.

### 2. Heading tree: the XML's ranks are upside down ✅ FIXED 2026-11-17

> **Fixed on the user's approval** with [`fix_pacittiya_vajirabuddhi.py`](fix_pacittiya_vajirabuddhi.py) (built on [`heading_tree.py`](heading_tree.py)). Each kaṇḍa now holds its own vaggas and rules, the same shape as `pi-2.md` and the Pācittiya aṭṭhakathā:
>
> ```
> ## Pācittiyavaṇṇanā                   ^2-0
> ### 5. Pācittiyakaṇḍo                 ^2-1-0    + 9 vaggas → rules
> ### 6. Pāṭidesanīyakaṇḍo              ^2-2-0    + 2 rules
> ### 7. Sekhiyakaṇḍo                   ^2-3-0    + 7 vaggas + Pakiṇṇakavaṇṇanā
> ### 8. Sattādhikaraṇasamathavaṇṇanā   ^2-4-0
> ### Bhikkhunīvibhaṅgavaṇṇanā          ^2-5-0    (same ID as pi-2's Bhikkhunīvibhaṅgo)
> #### 1. Pārājikakaṇḍavaṇṇanā          ^2-5-1-0  + Ganthārambhavaṇṇanā + 4 pārājikas
> #### 2.–3. Saṅghādisesa-, Nissaggiya…  ^2-5-2-0, ^2-5-3-0 + their rules
> #### 4. Pācittiyakaṇḍavaṇṇanā         ^2-5-4-0  + 9 vaggas → rules, + Nigamanavaṇṇanā
> ```
>
> **Placement follows the text's own closing lines:**
> - **`Pakiṇṇakavaṇṇanā`** closes between "Pādukavaggavaṇṇanā niṭṭhitā." and "Sekhiyakaṇḍavaṇṇanā niṭṭhitā.".
> - **`Nigamanavaṇṇanā`** closes between "Chattupāhanavaggavaṇṇanā niṭṭhitā." and "Pācittiyakaṇḍavaṇṇanā niṭṭhitā.".
> - **`Ganthārambhavaṇṇanā`** follows the `1. Pārājikakaṇḍavaṇṇanā` title in the text, so it is that kaṇḍa's first section.
>
> **Checks:**
> - **What changed:** 193 heading lines; nothing is deeper than `######`.
> - **What didn't:** every non-heading line, all 499 content IDs and all 351 root links are unchanged, as are the line count and the CRLF line endings.
> - **Re-check against the XML:** 716 / 716 lines identical, heading IDs consistent with depth, no hierarchy hints left (9 before).
> - **Backup:** [`backups/pi-pacittiya-vajirabuddhi.pre-toc-fix.md.bak`](backups/).
>
> The description below is of the state before the fix.

As in the Pārājika Vajirabuddhi, this XML tags the **vaggas as `title`** and the **kaṇḍas as `subhead`**, so a kaṇḍa ranks *below* the vaggas it contains. The vault follows the tags, which gives:

**Bhikkhuvibhaṅga**

```
### 5. Pācittiyakaṇḍo                  ^2-1-0     ← empty; its 9 vaggas are its siblings
### 1. Musāvādavaggo                    ^2-2-0
…
### 9. Ratanavaggo                      ^2-10-0
#### 10. Nandattherasikkhāpadavaṇṇanā   ^2-10-10-0
#### 6. Pāṭidesanīyakaṇḍo               ^2-10-11-0  ← kaṇḍas 6–8 and the 7 sekhiya vaggas sit inside the Ratanavagga,
#### 1. Paṭhamapāṭidesanīya…            ^2-10-12-0     flat beside its rules
#### 7. Sekhiyakaṇḍo                    ^2-10-14-0
#### 1. Parimaṇḍalavaggavaṇṇanā         ^2-10-15-0
#### 8. Sattādhikaraṇasamathavaṇṇanā    ^2-10-22-0
```

**Bhikkhunīvibhaṅga**

```
### Bhikkhunīvibhaṅgavaṇṇanā            ^2-11-0
#### 1. Pārājikakaṇḍavaṇṇanā            ^2-11-1-0  ← empty
#### Ganthārambhavaṇṇanā                ^2-11-2-0  ← holds the 4 pārājika, the 2nd and 3rd kaṇḍas with all their rules,
##### 1. Paṭhamapārājikasikkhāpada…     ^2-11-2-1-0   and the "4. Pācittiyakaṇḍavaṇṇanā" title (26 headings)
##### 2. Saṅghādisesakaṇḍavaṇṇanā       ^2-11-2-5-0
#### 1. Lasuṇavaggo                     ^2-11-3-0  ← the 9 pācittiya vaggas are siblings of the Ganthārambha
```

The checker also flags 3 smaller parent differences:
- **`Pakiṇṇakavaṇṇanā`** (line 1250) sits under `7. Pādukavaggavaṇṇanā`. In the XML it is a sibling.
- **`Nigamanavaṇṇanā`** (line 2034) sits under the 11th rule of the Chattupāhanavagga, the same slip as in the other files.
- **`Bhikkhunīvibhaṅgavaṇṇanā`** sits under `Pācittiyavaṇṇanā`, though the XML ranks it `book`. This one is deliberate, and matches `pi-2.md` and the aṭṭhakathā.

**The fix:** make each kaṇḍa the parent of its vaggas and rules, and move `Ganthārambhavaṇṇanā` before or above `1. Pārājikakaṇḍavaṇṇanā`. Most heading IDs from `^2-1-0` on would change. The paragraph IDs `^2-N` would not.

### 3. Faithful to the source ℹ️

- **The 192 "level mismatches" in the content report are false positives.** The XML has no divs.
