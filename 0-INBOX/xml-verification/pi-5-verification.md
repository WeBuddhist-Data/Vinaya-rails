# pi-5 (Parivārapāḷi) vs tipitaka-xml — verification

- **Date:** 2026-11-17
- **Vault file:** `1-SOURCES/Text/pi-5.md`
- **Source:** `tipitaka-xml/romn/vin02m4.mul.xml` (1 book div, 18 chapter divs). TOC reference: `tipitaka.org/romn/cscd/vin02m4.mul.toc.xml`.
- **Method:** the same as pi-1 ([`pi-1-verification.md`](pi-1-verification.md)).
- **Full output:** [`pi-5-detail.md`](pi-5-detail.md)

## Result: content ✅, hierarchy ✅ (fixed 2026-11-17 and 2026-11-20, see finding 2)

| Check | XML | Vault | |
|---|---|---|---|
| Lines | 3,645 | 3,611 | 3,577 identical, 34 hangnum merges (below) |
| Numbered paragraphs | ¶1–¶501 | `^5-1` … `^5-501` | every ID equals its printed number |
| Words added, missing or changed | | | **0** |
| Headings | 256 | 256 | `1. Bhikkhuvibhaṅgo` was a paragraph; a heading again since 2026-11-20 (finding 2a) |
| Heading IDs vs `#` depth | | | all consistent, no skipped levels |
| Stray digits after `<pb>` | 0 | | |

The only content-level differences are layout: in **34 places** the XML puts a gāthā's paragraph number on its own line (`<p rend="hangnum">3.</p>`), and the vault joins it to the first verse line (`3. Upāli dāsako ceva, …`) so it can start the `^5-3` block. That is why the vault has 34 fewer lines. Besides the homage `^T-1`, there are 2 unnumbered blocks: `^5-U1` and `^5-U2`, gāthā blocks right after a heading. Until 2026-11-20 these were `^5-U2` and `^5-U3`, and `^5-U1` was the line `1. Bhikkhuvibhaṅgo` (finding 2a).

## Findings

### 1. Spaces the conversion added before punctuation ✅ FIXED 2026-11-17

This is the same artifact as in pi-1 to pi-4: `word<pb/>.` became `word .`.

- **Fixed on the user's approval:** 233 spaces removed on 208 lines, using [`fix_pb_spaces.py`](fix_pb_spaces.py). No other line was touched.
- **After the fix:**
  - Block IDs and the line count (4,395) are unchanged, and a second run of the script finds nothing left.
  - The comparison shows 0 spacing-only differences; the 34 remaining hunks are the hangnum merges above.
- A backup of the pre-fix file is in [`backups/`](backups/).
- The uploaded library text still has the old spacing, so it needs a re-upload.

The source itself has **22 spaces** before punctuation (A 1, B 7, D 14). These stay, and are listed in [`pi-5-spaces-kept.md`](pi-5-spaces-kept.md). Most D cases are a source space after a paragraph number before `…` (`176. …Anādariyaṃ`) or before `…pe…`.

### 2. Hierarchy of the Soḷasamahāvāro ✅ FIXED 2026-11-17 (b, c, d) and 2026-11-20 (a)

> **2026-11-20, finding a fixed on the user's approval** with [`fix_pi5_bhikkhuvibhanga.py`](fix_pi5_bhikkhuvibhanga.py) (built on [`heading_tree.py`](heading_tree.py)):
>
> ```
> ### Soḷasamahāvāro                ^5-1-0
> #### 1. Bhikkhuvibhaṅgo           ^5-1-1-0     ← was the text line ^5-U1
> ##### 1.–8. vāras ×2 (bhikkhu)    ^5-1-1-1-0 … ^5-1-1-16-0
> #### Bhikkhunīvibhaṅgo            ^5-1-2-0     (was ^5-1-17-0)
> ##### 1.–8. vāras ×2 (bhikkhunī)  ^5-1-2-1-0 … ^5-1-2-16-0
> ### Samuṭṭhānasīsasaṅkhepo        ^5-2-0       (unchanged, as are all later chapters)
> ```
>
> - **Why.** Soḷasamahāvāro is one unit made of the two vibhaṅgas:
>   - the Vajirabuddhi closes it with `Mahāvibhaṅge ca bhikkhunivibhaṅge soḷasamahāvāravaṇṇanā niṭṭhitā.` ([pi-parivara-vajirabuddhi.md:66](../../1-SOURCES/Commentaries/pi-parivara-vajirabuddhi.md));
>   - the XML's chapter `div vin5_1` holds both halves.
>
>   Each vibhaṅga closes its own 16 vāras (lines 1122–1123 and 1732), so the two vibhaṅgas are siblings.
> - **The one change of printed order.** In the XML, `<head rend="title">1. Bhikkhuvibhaṅgo</head>` stands *before* `Soḷasamahāvāro`, outside the chapter div. That is why tipitaka.app shows it as a title in its reading view but not in its contents tree. The vault moves this one heading line below `### Soḷasamahāvāro`, because a tree cannot put a child before its parent. No other line moves. This is registered in `vault-annex.md` §2 as a vault-only deviation.
> - **Checks:**
>   - **What changed:** 121 heading lines, plus the converted line. The bhikkhu vāras move one level deeper, and all 56 vaggas are now seven levels deep in **bold**.
>   - **What didn't:** every other non-heading line, the line count and the CRLF line endings. The 501 numbered paragraph IDs `^5-1` … `^5-501` run in sequence, and `^T-1` is unchanged.
>   - **Unnumbered IDs renumbered.** The old `^5-U1` is gone, so the two gāthā blocks `^5-U2` and `^5-U3` became `^5-U1` (line 1764) and `^5-U2` (line 3214), and the `U` series runs without a gap. Nothing in 1-SOURCES, 2-RAILS or 3-TRANSFORMATIONS linked to any of them, or to any pi-5 heading ID. The `U` series in pi-1 to pi-4 was checked too and has no gaps.
>   - **Transclusions:** all 5 Parivāra commentaries pass [`check_links.py`](check_links.py): 544 links in 488 groups, 0 mismatches, 0 missing targets.
>   - **Re-check against the XML:** 3,576 identical lines plus the 34 hangnum merges. The only new difference is the moved heading line. The old block-ID warning `^5-U1 but paragraph number 1` is gone.
>   - **Backup:** [`backups/pi-5.pre-bhikkhuvibhanga-fix.md.bak`](backups/).
>   - **Library:** the prod edition still has the old segments `5-U1`, `5-U2` and `5-U3` and the old TOC. Both need updating there.

> **Fixed on the user's approval** with [`restructure_pi5_solasa.py`](restructure_pi5_solasa.py). The chapter's 120 headings were re-parented by type, and their IDs renumbered from the new tree:
>
> - **b.** `#### Bhikkhunīvibhaṅgo ^5-1-17-0` is now the parent of all 16 bhikkhunī vāras.
> - **c.** Bhikkhunī vāras 3–8 and the 8 paccayavāras are siblings of `2. Katāpattivāro` (`^5-1-17-3-0` … `^5-1-17-16-0`).
> - **d.** All 56 vaggas sit under their kaṇḍa. The 18 bhikkhunī vaggas are seven levels deep and carry their title in **bold** (CLAUDE.md §5a). These are the first `#######` headings in the vault.
> - **a.** `1. Bhikkhuvibhaṅgo` stayed plain text (`^5-U1`) on 2026-11-17, because it precedes the `Soḷasamahāvāro` heading. *Superseded 2026-11-20, see above.*
>
> **Checks:**
> - **What changed:** 93 heading lines.
> - **What didn't:** every non-heading line and all 505 paragraph IDs are unchanged, as are the line count and the CRLF line endings.
> - **Re-check against the XML:**
>   - content as before: 3,577 identical lines plus the 34 hangnum merges;
>   - heading IDs consistent with depth;
>   - the only hierarchy hints left are the two expected restarts at the paccayavāras.
> - **Script updates:** [`compare_vin.py`](compare_vin.py) and [`fix_pb_spaces.py`](fix_pb_spaces.py) now read bold `#######` headings.
> - **Backup:** [`backups/pi-5.pre-toc-fix.md.bak`](backups/).
> - **Library:** the uploaded TOC needs a re-upload.
>
> The description below is of the state before the fix.

The first chapter covers the 16 mahāvāras of the **Bhikkhuvibhaṅga**, then the 16 of the **Bhikkhunīvibhaṅga**. The vault's TOC gets this wrong in four ways. All other chapters (`^5-2` … `^5-19`) are fine.

**a. `1. Bhikkhuvibhaṅgo` is not a heading.** In the XML it is `<head rend="title">`, just before the chapter head `Soḷasamahāvāro`. The vault turned it into a plain block, `1. Bhikkhuvibhaṅgo ^5-U1` (line 30). The text is kept, but it is missing from the TOC, and its counterpart `Bhikkhunīvibhaṅgo` *is* a heading.

**b. `Bhikkhunīvibhaṅgo` is nested under the last vāra of the bhikkhu part.**

```
#### 8. Samuccayavāro          ^5-1-16-0
##### Bhikkhunīvibhaṅgo        ^5-1-16-1-0   ← child of Samuccayavāro, with no content
#### 1. Katthapaññattivāro     ^5-1-17-0     ← the bhikkhunī vāras are siblings of the bhikkhu ones
#### 2. Katāpattivāro          ^5-1-18-0
```

It should be the parent of the bhikkhunī vāras, at the same rank as `1. Bhikkhuvibhaṅgo`.

**c. Bhikkhunī vāras 3–8 and the 8 paccayavāras are nested under `2. Katāpattivāro`** (`^5-1-18-15-0` … `^5-1-18-32-0`, 18 headings, lines 1595–1724). In the XML these are tagged `subhead` instead of `title` (a source inconsistency: the bhikkhu part tags the same vāras `title`), and the vault followed the tag. So `3. Vipattivāro`, `1. Katthapaññattivāro`, its `1. Pārājikakaṇḍaṃ` and so on all appear as siblings of the Katāpattivāro's own kaṇḍas.

**d. Vaggas flattened beside their kaṇḍa**, as in pi-1 and pi-2. For example:

```
##### 4. Nissaggiyakaṇḍaṃ       ^5-1-1-4-0
##### 1. Kathinavaggo           ^5-1-1-5-0    ← should be one level deeper
##### 2. Kosiyavaggo            ^5-1-1-6-0
##### 5. Pācittiyakaṇḍaṃ        ^5-1-1-8-0
```

This affects the Nissaggiya, Pācittiya and Sekhiya vaggas in the bhikkhu Katthapaññatti- and Katāpattivāra (19 each), and the Pācittiya vaggas in the bhikkhunī ones (9 each): **56 vagga headings**. The source tags kaṇḍa and vagga alike (`subhead`).

A corrected outline would look like this:

```
### Soḷasamahāvāro
#### 1. Bhikkhuvibhaṅgo
##### 1. Katthapaññattivāro … 8. Samuccayavāro, 1. Katthapaññattivāro … 8. Samuccayavāro
###### 4. Nissaggiyakaṇḍaṃ
####### 1. Kathinavaggo …
#### Bhikkhunīvibhaṅgo
##### 1. Katthapaññattivāro … (same shape)
```

- Almost every heading ID in `^5-1-…` would change. The paragraph IDs `^5-N` would not.
- The library TOC would need re-uploading.

### 3. Faithful to the source ℹ️

- **Restarting vāra numbers.** In each vibhaṅga the 8 vāras run 1–8 twice (the second time as the *paccayavāras*: "Aṭṭhapaccayavārā niṭṭhitā"). The vault numbers them `^5-1-1` … `^5-1-16`, which is fine. So the hierarchy hints for lines 1017 and 1127 in the detail report are expected; the other 17 hints are findings 2c and 2d.
- **`Atthavasapakaraṇaṃ`.** In the XML this is a `subhead` outside any chapter div, between Uposathādipucchāvissajjanā and Gāthāsaṅgaṇikaṃ. The vault makes it its own chapter `^5-7-0`. That is reasonable (it has its own "niṭṭhitaṃ"), but tipitaka.org's TOC lists only the **18** chapter divs, so from Gāthāsaṅgaṇikaṃ on the vault chapter number is one higher than the XML div number (`^5-8` = `vin5_7`).
- **`Samathabhedo`** is a `title` inside Antarapeyyālaṃ, and the vault correctly nests vāras 6–21 under it.
- **The 99 "level mismatches" in the detail report are false positives**, apart from the ones covered in finding 2. The XML has no `title` level in chapters 2–18, so its `subhead` sits directly under the chapter.
