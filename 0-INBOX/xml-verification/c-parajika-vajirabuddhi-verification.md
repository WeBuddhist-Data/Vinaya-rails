# pi-parajika-vajirabuddhi (Vajirabuddhi-ṭīkā, Pārājika) vs tipitaka-xml — verification

- **Date:** 2026-11-17
- **Vault file:** `1-SOURCES/Commentaries/pi-parajika-vajirabuddhi.md`
- **Source:** `tipitaka-xml/romn/vin06t.nrf.xml`, which holds the Vajirabuddhi on all five books. The Pārājika part was cut out with [`slice_xml.py`](slice_xml.py): from the start of the file up to, not including, the `Pācittiyavaṇṇanā` chapter heading. That is 991 of 2,673 blocks, ending at `Nissaggiyavaṇṇanā niṭṭhitā.`, the vault file's last line. The slice is `tmp/vin06t-parajika.xml`.
- **Method:** the same as [`c-parajika-atthakatha-verification.md`](c-parajika-atthakatha-verification.md). The ID and link checks are now in [`check_links.py`](check_links.py).
- **Outputs:** [`c-parajika-vajirabuddhi-detail.md`](c-parajika-vajirabuddhi-detail.md), [`c-parajika-vajirabuddhi-headings.md`](c-parajika-vajirabuddhi-headings.md), [`c-parajika-vajirabuddhi-spaces-kept.md`](c-parajika-vajirabuddhi-spaces-kept.md).

## Result: content ✅

| Check | XML slice | Vault | |
|---|---|---|---|
| Lines | 991 | 991 | identical, same order |
| Words added, missing or changed | | | **0** |
| Content block IDs | | `^1-1` … `^1-724` | sequential, no gaps or duplicates |
| Numbered paragraphs | 206 | 206 transclusion groups | every group links exactly the printed number or range (incl. 32 truncated ranges) |
| Transclusion targets | | 248 → `pi-1.md` | all exist |
| Headings | 112 | 112 | same text, same order |
| Stray digits after `<pb>` | 0 | | |

The 78 lines that the comparison counts as "identical" differ only by the spacing in finding 1.

## Findings

### 1. Spaces the conversion added before punctuation ✅ FIXED 2026-11-17

- **Fixed on the user's approval:** 86 spaces removed on 78 lines, using [`fix_pb_spaces.py`](fix_pb_spaces.py). No other line was touched.
- **After the fix:**
  - Block IDs, transclusion links, the line count and the CRLF line endings are unchanged.
  - The comparison shows 991 / 991 lines identical, with 0 spacing-only differences. A second run of the script finds nothing left.
- A backup of the pre-fix file is in [`backups/`](backups/).
- The uploaded library text still has the old spacing, so it needs a re-upload.

The source itself has **4 spaces** before punctuation (B 3, C 1). These stay. The C case is line 333, `rūpupādānakkhandho <pb/>..pe…`.

### 2. Heading tree: kaṇḍas 2–4 sit inside the 4th pārājika ✅ FIXED 2026-11-17

> **Fixed on the user's approval** with [`fix_parajika_vajirabuddhi.py`](fix_parajika_vajirabuddhi.py) (built on [`heading_tree.py`](heading_tree.py)). Under `### Pārājikavaṇṇanā ^1-7-0`, each kaṇḍa is now the parent of its own material:
>
> ```
> #### Verañjakaṇḍo          ^1-7-1-0    + its 5 sections
> #### 1. Pārājikakaṇḍo      ^1-7-2-0    + the 4 pārājikas, each with its sections
> #### 2. Saṅghādisesakaṇḍo  ^1-7-3-0    + 13 rules
> #### 3. Aniyatakaṇḍo       ^1-7-4-0    + 2 rules
> #### 4. Nissaggiyakaṇḍo    ^1-7-5-0    + 3 vaggas → 10 rules each
> ```
>
> **`Nigamanavaṇṇanā` stays under the 4th pārājika.** The text closes it with "Catutthapārājikavaṇṇanā niṭṭhitā." before "Pārājikakaṇḍavaṇṇanā niṭṭhitā.".
>
> **Checks:**
> - **What changed:** 102 heading lines; nothing is deeper than `######`.
> - **What didn't:** every non-heading line, all 724 content IDs and all 248 root links are unchanged, as are the line count and the CRLF line endings.
> - **Re-check against the XML:** 991 / 991 lines identical, heading IDs consistent with depth, no hierarchy hints left (5 before).
> - **Backup:** [`backups/pi-parajika-vajirabuddhi.pre-toc-fix.md.bak`](backups/).
>
> The description below is of the state before the fix.

In the XML, after `4. Catutthapārājikaṃ` (`title`) **every** heading is a flat `subhead`: the closing sections of the 4th pārājika, the kaṇḍa titles `2. Saṅghādisesakaṇḍo`, `3. Aniyatakaṇḍo` and `4. Nissaggiyakaṇḍo`, every sikkhāpada, and its `Padabhājanīya-`/`Vinītavatthuvaṇṇanā`. The vault follows the XML for the kaṇḍas:

```
#### 4. Catutthapārājikaṃ                       ^1-7-11-0
##### Nigamanavaṇṇanā                           ^1-7-11-7-0
##### 2. Saṅghādisesakaṇḍo                       ^1-7-11-8-0    ← a kaṇḍa, inside the 4th pārājika
##### 1. Sukkavissaṭṭhisikkhāpadavaṇṇanā         ^1-7-11-9-0    ← sibling of its own kaṇḍa
…
##### 3. Aniyatakaṇḍo                           ^1-7-11-22-0
##### 4. Nissaggiyakaṇḍo                         ^1-7-11-25-0   ← empty
#### 1. Cīvaravaggo                              ^1-7-12-0      ← the Nissaggiya vaggas are `title`s in the XML,
                                                                  so they are siblings of the 4th pārājika
```

- So the 13 saṅghādisesa and 2 aniyata rules sit under the 4th pārājika. The Nissaggiya vaggas sit outside their kaṇḍa.
- The vault goes **beyond** the XML in one place, and sensibly: it nests each `Padabhājanīyavaṇṇanā` / `Vinītavatthuvaṇṇanā` / `Pakiṇṇakavaṇṇanā` under its sikkhāpada. These are the 7 "parent mismatches" in the headings report, and they are improvements, not errors.
- **The fix** would be to make each kaṇḍa the parent of its rules or vaggas, at the level of the 4 pārājikas or above them. About 60 heading IDs from `^1-7-11-8-0` on would change. The paragraph IDs `^1-N` would not.

### 3. Faithful to the source ℹ️

- **The 103 "level mismatches" in the content report are false positives.** The XML has no divs, and the parent check above replaces that test.
