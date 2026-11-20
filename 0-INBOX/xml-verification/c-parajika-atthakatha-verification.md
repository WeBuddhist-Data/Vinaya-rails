# pi-parajika-atthakatha (Samantapāsādikā, Pārājikakaṇḍa) vs tipitaka-xml — verification

- **Date:** 2026-11-17
- **Vault file:** `1-SOURCES/Commentaries/pi-parajika-atthakatha.md`
- **Source:** `tipitaka-xml/romn/vin01a.att.xml`. It has no `<div>`s; every heading is a `<p rend="nikaya|book|chapter|title|subhead|subsubhead">`.
- **Method:**
  - Content: the same as for the root texts ([`compare_vin.py`](compare_vin.py)), after removing the 410 root-verse transclusion lines (`![[1-SOURCES/Text/pi-1.md#^1-N]]`), which the vault adds and the XML does not have.
  - Headings: [`compare_headings.py`](compare_headings.py). It checks each heading's **parent** rather than its absolute level, because the XML ranks have gaps.
- **Outputs:** [`c-parajika-atthakatha-detail.md`](c-parajika-atthakatha-detail.md) (content), [`c-parajika-atthakatha-headings.md`](c-parajika-atthakatha-headings.md) (heading tree), [`c-parajika-atthakatha-spaces-kept.md`](c-parajika-atthakatha-spaces-kept.md).

## Result: content ✅

| Check | XML | Vault | |
|---|---|---|---|
| Lines (headings, paragraphs, verse lines) | 2,974 | 2,974 | identical, same order |
| Words added, missing or changed | | | **0** |
| Content block IDs | | `^1-1` … `^1-2538` | sequential, no gaps or duplicates (the commentary convention) |
| Numbered paragraphs (¶1–¶660) | 367 | 367 transclusion groups | every group links exactly the printed number or range, e.g. `482-7.` → `^1-482` … `^1-487` |
| Transclusion targets | | 410 | all exist in `pi-1.md` |
| Headings | 152 | 151 | 151 match by text; the 152nd is finding 3a |
| Stray digits after `<pb>` | 0 | | |

The 273 lines that the comparison counts as "identical" differ only by the spacing in finding 1.

## Findings

### 1. Spaces the conversion added before punctuation ✅ FIXED 2026-11-17

This is the same artifact as in the root texts. For example, the XML has `Visuddhavijjāpaṭisambhidehi<pb ed="P" n="1.0002"/>;` and the vault had `Visuddhavijjāpaṭisambhidehi ;` (line 65).

- **Fixed on the user's approval:** 297 spaces removed on 273 lines, using [`fix_pb_spaces.py`](fix_pb_spaces.py). No other line was touched.
  - The script now skips transclusion lines. Re-running it on pi-1 to pi-5 changes nothing.
- **After the fix:**
  - Block IDs, transclusion links and the line count are unchanged, and the CRLF line endings are kept.
  - The comparison shows 2,974 / 2,974 lines identical, with 0 spacing-only differences. A second run of the script finds nothing left.
- A backup of the pre-fix file is in [`backups/`](backups/).
- The uploaded library text still has the old spacing, so it needs a re-upload.

The source itself has **5 spaces** before punctuation (A 3, B 1, C 1). These stay. The C case is line 2515, `Ādiyeyya <pb/>, hareyya`.

### 2. Block IDs and root links ✅

- **Content IDs:** sequential `^1-1` … `^1-2538`.
- **Root links:** each printed paragraph number is preceded by transclusions of exactly that pi-1 paragraph, or of every paragraph in its range. This includes the 26 truncated ranges the frontmatter mentions (`133-4.`). There are no wrong or dangling links.

### 3. Heading tree ⚠️ (2 nesting errors; deferred with the other TOC fixes)

In 149 of 151 headings, the parent in the vault is the same as in the XML.

a. **The second volume's `Vinayapiṭake` is plain text.** The XML repeats the nikāya title before the second volume. The vault keeps it as a plain block, `Vinayapiṭake ^1-1313` (line 3332), not a heading. The text is kept, so this is harmless.

b. **`Pārājikakaṇḍa-aṭṭhakathā (dutiyo bhāgo)` is nested under the first volume.**

```
## Pārājikakaṇḍa-aṭṭhakathā (paṭhamo bhāgo)     ^1-0
### 1. Pārājikakaṇḍaṃ                         ^1-4-0
### Pārājikakaṇḍa-aṭṭhakathā (dutiyo bhāgo)     ^1-5-0   ← XML: same rank as paṭhamo bhāgo (rend="book")
#### 3. Tatiyapārājikaṃ                       ^1-5-1-0
#### 2. Saṅghādisesakaṇḍaṃ                    ^1-5-3-0
```

To match the XML, it would become a `##` sibling of the first volume, and all `^1-5-…` heading IDs would change.

> **Status 2026-11-17:**
> - **c is FIXED** on the user's approval with [`promote_heading.py`](promote_heading.py). It is now `##### Nigamanavaṇṇanā ^1-5-3-14-0`, a sibling of the 13 rules. One heading line changed; all other lines, IDs and links are unchanged. The section comments on root ¶442, the closing of the whole Saṅghādisesa kaṇḍa.
> - **b is accepted as is.** Every fix would either renumber the sequential content IDs or need a top-level ID like `^2-0`, which means pi-2 in this vault.
> - Backup: [`backups/pi-parajika-atthakatha.pre-toc-fix.md.bak`](backups/).

c. **`Nigamanavaṇṇanā` (line 5317) is one level too deep.** The vault puts it under `13. Kuladūsakasikkhāpadavaṇṇanā` (`^1-5-3-13-1-0`). In the XML it is a `subhead` like the 13 sikkhāpadas, so it is their sibling: the closing section of the Saṅghādisesakaṇḍa, not of the 13th rule.

### 4. Faithful to the source ℹ️

- **The volume break falls inside the Pārājikakaṇḍa.** `3. Tatiyapārājikaṃ` and `4. Catutthapārājikaṃ` come after the `dutiyo bhāgo` heading, so they sit under it and not under `1. Pārājikakaṇḍaṃ`. The XML is laid out the same way. That is why the detail report gives a "numbering restart" hint at `2. Saṅghādisesakaṇḍaṃ`.
- **The 142 "level mismatches" in the content report are false positives.** The XML has no divs, so its tag ranks are not depths. The parent check in finding 3 replaces that test.
