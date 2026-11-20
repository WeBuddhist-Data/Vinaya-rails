# pi-1 (Pārājikapāḷi) vs tipitaka-xml — verification

- **Date:** 2026-11-13
- **Vault file:** `1-SOURCES/Text/pi-1.md`
- **Source:** `tipitaka-xml/romn/vin01m.mul.xml` (CST, romanised). TOC reference: `tipitaka-xml/tipitaka.org/romn/cscd/vin01m.mul.toc.xml`.
- **Script:** [`compare_vin.py`](compare_vin.py), run as `python -I compare_vin.py <vault.md> <report.md> <xml...>`
- **Full output:** [`pi-1-detail.md`](pi-1-detail.md)

## Method

- Each XML `<p>`, `<head>` and `<trailer>` counts as one line, and each vault line counts as one line. The two streams are diffed in order.
- XML markup is mapped to the vault's conventions before diffing:
  - `<note>` becomes `{…}`
  - `<pb>` is removed
  - `‘‘` and `’’` become `"`
- Heading levels are compared using:
  - XML `div` nesting (book = 1, kaṇḍa = 2), with `title` = kaṇḍa + 1 and `subhead` = kaṇḍa + 2
  - the vault's `#` count

## Result: content ✅

| Check | XML | Vault | |
|---|---|---|---|
| Lines (headings + paragraphs + trailers) | 2,477 | 2,477 | identical, same order |
| Numbered paragraphs | ¶1–¶662 | `^1-1` … `^1-662` | every ID equals its printed number; no gaps or duplicates |
| Text differences | | | **0** |
| Headings | 80 | 80 | same text, same order, same level |
| Heading IDs vs `#` depth | | | all consistent |

The vault content is a faithful copy of the XML. No words are missing, added or changed, and the variant-reading notes `{…}` are all kept.

## Findings

### 1. Hierarchy: the Nissaggiya vaggas are flattened ✅ FIXED 2026-11-17

> **Fixed on the user's approval** with [`nest_vaggas.py`](nest_vaggas.py) (`pi-1.md ^1-5-0`). The 30 sikkhāpadas now sit one level under their vagga, and their IDs are renumbered to match the printed numbers, e.g. `##### 1. Paṭhamakathinasikkhāpadaṃ ^1-5-1-1-0` and `#### 2. Kosiyavaggo ^1-5-2-0`.
>
> - **What changed:** 32 heading lines. `1. Cīvaravaggo` kept `^1-5-1-0`.
> - **What didn't:** every non-heading line and all 675 paragraph IDs are unchanged, as are the line count and the CRLF line endings.
> - **Re-check against the XML:**
>   - all 2,477 lines identical;
>   - heading IDs consistent with depth;
>   - no "numbering restart" hints left;
>   - the 30 "level mismatches" are the intended extra depth.
> - **Reused IDs:** `^1-5-2-0` and `^1-5-3-0` now mean the Kosiya and Patta vaggas. Nothing in the vault linked to the old meaning.
> - **Backup:** [`backups/pi-1.pre-toc-fix.md.bak`](backups/).
> - **Library:** the uploaded TOC still has the old heading IDs and needs a re-upload.
>
> The description below is of the state before the fix.

The three vaggas are tagged `<p rend="title">` in the XML, just like the sikkhāpadas. The vault copied this, so each vagga is a **sibling** of its own sikkhāpadas rather than their parent:

```
### 4. Nissaggiyakaṇḍaṃ            ^1-5-0
#### 1. Cīvaravaggo                ^1-5-1-0
#### 1. Paṭhamakathinasikkhāpadaṃ  ^1-5-2-0    ← numbering restarts at the same level
…
#### 10. Rājasikkhāpadaṃ           ^1-5-11-0
#### 2. Kosiyavaggo                ^1-5-12-0
#### 1. Kosiyasikkhāpadaṃ          ^1-5-13-0
…
#### 3. Pattavaggo                 ^1-5-23-0
#### 1. Pattasikkhāpadaṃ           ^1-5-24-0 … ^1-5-33-0
```

The text is correct as transmitted. Structurally, though, the sikkhāpadas belong under their vagga: each vagga's sikkhāpadas are numbered 1–10, and the IDs run 2…33 without matching those printed numbers. The corrected tree would be:

```
#### 1. Cīvaravaggo                ^1-5-1-0
##### 1. Paṭhamakathinasikkhāpadaṃ ^1-5-1-1-0  … ##### 10. Rājasikkhāpadaṃ ^1-5-1-10-0
#### 2. Kosiyavaggo                ^1-5-2-0
##### 1. Kosiyasikkhāpadaṃ         ^1-5-2-1-0  … ^1-5-2-10-0
#### 3. Pattavaggo                 ^1-5-3-0
##### 1. Pattasikkhāpadaṃ          ^1-5-3-1-0  … ^1-5-3-10-0
```

The fix would change 33 heading IDs and nothing else:
- No file in the vault links to any `pi-1#^1-5-*-0` heading.
- The paragraph IDs `^1-N`, which the commentaries transclude, stay the same.

However, pi-1 is already uploaded (see `0-INBOX/pi-1-hierarchy-and-upload-report.md`), so the TOC would need to be **re-uploaded**.

The other levels are correct:
- Pārājika: pārājika → bhāṇavāra / vinītavatthu
- Saṅghādisesa and Aniyata: sikkhāpada → vinītavatthu

### 2. Spurious space before punctuation — ✅ FIXED 2026-11-13

**Fixed** with [`fix_pb_spaces.py`](fix_pb_spaces.py), on the user's instruction ("if the case is what I have given you, then remove the space").

- The script pairs each vault line with its XML line. It drops a space only where the XML, with `<pb>` deleted, has no space before that punctuation mark.
- **Result:** 267 spaces removed on 240 lines.
  - Block IDs, line count and headings are unchanged.
  - Re-running `compare_vin.py` now gives 2,477 / 2,477 lines identical, with 0 spacing-only differences.
- **Two spaces were kept** because the source has them, with a space before the marker:
  - line 2210, `paggaṇheyya <pb/>, so`
  - line 2696, `upasaṅkamitvā <pb/>.`
- A backup of the pre-fix file was kept outside the vault.
- **55 spaces before punctuation stay, by decision (2026-11-13).** All of them are in the source XML, and tipitaka.app shows them too. The user checked each type on the web and kept all four. The full list is in [`pi-1-spaces-kept.md`](pi-1-spaces-kept.md).

  | Type | Count | Example on the web |
  |---|---|---|
  | A: `word <pb/>…` | 22 | `yāmā devā …` |
  | B: `word <pb/> …pe…` | 30 | ¶42 `no sarāgāya …pe…` (¶41 has no marker and no space) |
  | C: `word <pb/>,` | 2 | `paggaṇheyya , so` |
  | D: plain source space | 1 | `{…} … saṅghassa` |
- The uploaded library text still has the old spacing. It needs a text re-upload; the segment IDs are unchanged.

Original finding:

**242 vault lines** have a space before `.` `,` `;` `!` `?` that the XML does not have. Examples:
- `nisīdi .`
- `gotamo’ti .`
- `paṭisaṃvedesiṃ ,`

These spaces sit where a `<pb>` page-break tag stood next to the punctuation in the XML (e.g. `nisīdi<pb ed="P" n="3.0002" />.`). The conversion turned the tag into a space. The XML itself has only 2 such cases.

Confirmed on 2026-11-13 that the space is **not in any source**:

| Source | Example | Space before punctuation? |
|---|---|---|
| git `romn/vin01m.mul.xml` | `nisīdi<pb …/>.` | no (2 in the whole file) |
| git `deva master/vin01m.mul.xml` | `निसीदि<pb …/>।` | no |
| tipitaka.org `romn/cscd/vin01m.mul0.xml` (live) | `nisīdi<pb …/>.` | no |
| tipitaka.app `vp-prj` (rendered) | `निसीदि. एकमन्तं` | no (0 on the page) |

Replacing every `<pb>` in the romn XML with a space gives exactly **269** space-before-punctuation cases, the same count as `pi-1.md`. That pins the cause on the conversion step.

**Does `<pb>` ever split a word?** On 2026-11-13 I scanned all 23 Vinaya `romn` XML files (5 root books and 18 commentary files): every `<pb>` was classified by the characters on each side.

- **`letter<pb>letter` (a page break inside a word): 0 cases anywhere.** So the converter's space never split a word.
- `space<pb>space`: about 25,000 cases. Dropping the tag leaves the normal single space.
- `glued<pb>punctuation`: 4,114 cases. The next character is `,` 2,060 times, `.` 1,837, `?` 97, `;` 96, `!` 23 and `…` once. These are the only cases where the converter adds a wrong space.

So the right fix for every case is the same: remove `<pb>` without adding a space, then collapse doubled spaces.

**Why `<pb>` comes before the punctuation.** CST does not mark a page break as a point between characters. It **tags the first word of the new page**: the marker goes straight after that word, before any punctuation attached to it. The evidence from all 23 Vinaya romn files:

- Every volume's first-page marker (`n="….0001"`) sits after the **first word** of the text, never before it:
  - `Tena [T 1.0001][P 3.0001][M 0.0001][V 0.0001] samayena` (vin01m)
  - `Yo [P 1.0001] kappakoṭīhi` (vin01a)
  - `Karuṇāpuṇṇahadayaṃ[M 1.0001], sugataṃ` (vin07t)
  - There's no earlier page, so the marker must belong to the word in front of it.
- Positions of the 26,239 marker runs:

  | Where the marker is | Count |
  |---|---|
  | between two spaces (after a word, no punctuation) | 22,007 |
  | glued to a word, before its punctuation | 4,027 |
  | after a space, before `…` / punctuation | 68 |
  | after a closing tag, before punctuation | 66 |
  | **after punctuation, before a space (`word.<pb/> Next`)** | **0** |

- VRI's plain-text export (`root text files/vin01m.mul.txt`) uses the same layout: `निसीदि @३.०००२।` (word, marker, then danda).

So `nisīdi<pb ed="P" n="3.0002"/>.` means "PTS Vin III page 2 begins with the word *nisīdi*". It's an intentional word anchor, not misplaced markup. Removing the tag with no space reproduces the source text exactly. If page references are ever wanted in the vault, they belong next to the word, not after the punctuation.

**Stray digits after `<pb>` (a source error, not a vault one).** There are 5 cases of `<pb …/>N`, where a digit follows the page break:

| File | Context | In vault |
|---|---|---|
| `vin01m` (pi-1 ¶?) | `sāketā sāvatthiṃ <pb/>2 addhānamaggappaṭipannā` | `pi-1.md` line 2637, kept as `2` |
| `vin02m1` (pi-2) | `Tena <pb/>0 kho pana samayena` | not yet checked |
| `vin01t1`, `vin02a1`, `vin09t` | commentary files | not yet checked |

`deva master` has the same digit (`<pb/>२`, `<pb/>०`), so this is a typo in VRI's master text. The vault reproduces the source faithfully, so these should be left as they are, or at most marked `[Ed: …]`. They should not be silently deleted.

### 3. Formatting dropped on conversion (by design?) ℹ️

The vault does not keep these:
- `<hi rend="bold">`: 751 spans, mostly the rule formulas and the word-analysis lemmas
- the gāthā / centre paragraph types

The text inside them is fully present, and each one is still on its own line.

### 4. Unregistered block-ID convention ℹ️

12 unnumbered blocks (uddāna verses, and the "Ime kho panāyasmanto … uddesaṃ āgacchanti" lines) carry `^1-U1` … `^1-U12`.

- This is the convention in `0-INBOX/pi-1-hierarchy-and-upload-report.md`.
- It is **not** registered in `4-SYSTEM/Guidelines/vault-annex.md`.
- `vault-variants.md` §2 says unlabelled sections get no verse-level ID.

This is only a documentation gap, because the IDs are already uploaded.

## Not checked

- `romn` against `deva master`: the Devanagari master is the canonical source, and `romn` is generated from it.
- The commentaries: those come later, one book at a time.
