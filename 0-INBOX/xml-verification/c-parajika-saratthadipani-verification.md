# pi-parajika-saratthadipani (Sāratthadīpanī-ṭīkā, Pārājika) vs tipitaka-xml — verification

- **Date:** 2026-11-17
- **Vault file:** `1-SOURCES/Commentaries/pi-parajika-saratthadipani.md`
- **Source:** `tipitaka-xml/romn/vin01t1.tik.xml` + `vin01t2.tik.xml` (the two volumes, read in order). There are no `<div>`s; every heading is a `<p rend="…">`.
- **Method:** the same as [`c-parajika-atthakatha-verification.md`](c-parajika-atthakatha-verification.md): content compared with the 408 transclusion lines removed, and heading parents checked with [`compare_headings.py`](compare_headings.py).
- **Outputs:** [`c-parajika-saratthadipani-detail.md`](c-parajika-saratthadipani-detail.md) (content), [`c-parajika-saratthadipani-headings.md`](c-parajika-saratthadipani-headings.md), [`c-parajika-saratthadipani-spaces-kept.md`](c-parajika-saratthadipani-spaces-kept.md).

## Result: content ✅

| Check | XML | Vault | |
|---|---|---|---|
| Lines | 3,319 | 3,319 | identical, same order |
| Words added, missing or changed | | | **0** |
| Content block IDs | | `^1-1` … `^1-2784` | sequential, no gaps or duplicates |
| Numbered paragraphs | 337 | 337 transclusion groups | every group links exactly the printed number or range |
| Transclusion targets | | 408 → `pi-1.md` | all exist |
| Headings | 155 | 153 | 153 match by text; the other 2 are finding 3a |
| Stray digits after `<pb>` | 1 | 1 | finding 4 |

The 220 lines that the comparison counts as "identical" differ only by the spacing in finding 1.

## Findings

### 1. Spaces the conversion added before punctuation ✅ FIXED 2026-11-17

- **Fixed on the user's approval:** 228 spaces removed on 220 lines, using [`fix_pb_spaces.py`](fix_pb_spaces.py). No other line was touched.
- **After the fix:**
  - Block IDs, transclusion links, the line count and the CRLF line endings are unchanged.
  - The comparison shows 3,319 / 3,319 lines identical, with 0 spacing-only differences. A second run of the script finds nothing left.
- A backup of the pre-fix file is in [`backups/`](backups/).
- The uploaded library text still has the old spacing, so it needs a re-upload.

The source itself has **3 spaces** before punctuation (B 2, D 1). These stay.

### 2. Block IDs and root links ✅

- **Root links:** every numbered paragraph is preceded by transclusions of exactly its pi-1 paragraph or range, including the 4 truncated ranges (`61-2.`).
- **The 16 dreams.** The frontmatter's `source_note` explains that the 16 dreams of King Kosala are numbered as CST paragraphs, so they link to root `^1-1` … `^1-16`. That matches the printed numbers, so the check passes, but those 32 links point at unrelated root paragraphs, as the note says.

### 3. Heading tree ⚠️ (the second volume; deferred with the other TOC fixes)

a. **The second volume's headings are plain text.**

```
Paṭhamo bhāgo niṭṭhito.                         ^1-1362
Namo tassa bhagavato arahato sammāsambuddhassa  ^1-1363
Vinayapiṭake                                    ^1-1364
Sāratthadīpanī-ṭīkā (dutiyo bhāgo)              ^1-1365   ← XML: rend="book", like the first volume's title
### 1. Pārājikakaṇḍaṃ                           ^1-5-0
```

b. **As a result, the kaṇḍas of the second volume sit under the first volume.** `1. Pārājikakaṇḍaṃ` … `4. Nissaggiyakaṇḍaṃ` (`^1-5-0` … `^1-8-0`) are siblings of `Verañjakaṇḍavaṇṇanā` under `## Sāratthadīpanī-ṭīkā (paṭhamo bhāgo)`. In the XML they belong to the second volume.

- Here the volume break falls cleanly between the Verañjakaṇḍa and the Pārājikakaṇḍa. So there are two ways to fix it:
  - make `(dutiyo bhāgo)` a `##` heading over the four kaṇḍas, which would change their heading IDs;
  - or record that the vault ignores the volume division.
- The Pārājika aṭṭhakathā handled its second volume differently: it kept the volume title as a heading, but one level too deep. The two files should follow the same rule.

> **Status 2026-11-17:**
> - **c is FIXED** on the user's approval with [`promote_heading.py`](promote_heading.py). It is now `#### Nigamanavaṇṇanā ^1-6-14-0`, a sibling of the 13 rules. One heading line changed; all other lines, IDs and links are unchanged.
> - **a/b are accepted as is.** Turning the plain-text `(dutiyo bhāgo)` line into a heading would remove its content ID `^1-1365` and leave a gap in the sequence.
> - Backup: [`backups/pi-parajika-saratthadipani.pre-toc-fix.md.bak`](backups/).

c. **`Nigamanavaṇṇanā` (line 6257) is one level too deep.** This is the same as in the aṭṭhakathā. The vault puts it under `13. Kuladūsakasikkhāpadavaṇṇanā`, but in the XML it is a sibling of the 13 rules, under `2. Saṅghādisesakaṇḍaṃ`.

### 4. Stray digit in the source ℹ️

- Line 621 reads `Sabbameva 2 hidanti …`. The XML has `Sabbameva <pb ed="V" n="1.0082"/>2 <hi rend="bold">…`.
- This is the vin01t1 case noted earlier, also present in the `deva master` file. It is VRI's typo, faithfully copied. Leave it, or mark it with `[Ed: …]`.
