# pi-3 (Mahāvaggapāḷi) vs tipitaka-xml — verification

- **Date:** 2026-11-17
- **Vault file:** `1-SOURCES/Text/pi-3.md`
- **Source:** `tipitaka-xml/romn/vin02m2.mul.xml` (1 book div, 10 khandhaka divs)
- **Method:** the same as pi-1 ([`pi-1-verification.md`](pi-1-verification.md)).
- **Full output:** [`pi-3-detail.md`](pi-3-detail.md)

## Result: content ✅ (3 layout-only differences)

| Check | XML | Vault | |
|---|---|---|---|
| Lines | 2,759 | 2,757 | 2,754 identical; the 3 others are below |
| Numbered paragraphs | ¶1–¶477 | `^3-1` … `^3-477` | every ID equals its printed number |
| Words added, missing or changed | | | **0** |
| Headings | 294 | 294 | same text, same order |
| Heading IDs vs `#` depth | | | all consistent, no skipped levels |
| Stray digits after `<pb>` | 0 | | |

The three differences change layout only, not text:

1. **Line 281 (¶39) and line 934 (¶131).** The XML puts the paragraph number on a line of its own (`<p rend="hangnum">39.</p>`), before the first gāthā line. The vault joins it to that line: `39. Nerañjarāyaṃ bhagavā, …`. This is needed so the line can start the `^3-39` block. That's why the vault has 2 fewer lines.
2. **Line 2604.** The XML note has a leading space, `<note> parihāyissati (sī. syā.)</note>`. The vault writes `{parihāyissati (sī. syā.)}`, as every other note is written. This is harmless.

There is also a markup quirk in ¶199: the XML has `199 .` (a space between the number and its dot). The vault normalises it to `199.`.

## Findings

### 1. Spaces the conversion added before punctuation ✅ FIXED 2026-11-17

This is the same artifact as in pi-1 and pi-2: `word<pb/>.` became `word .`.

- **Fixed on the user's approval:** 446 spaces removed on 376 lines, using [`fix_pb_spaces.py`](fix_pb_spaces.py).
  - The script now merges `hangnum` lines and normalises note spacing and `N .`. Re-running it on pi-1 and pi-2 changes nothing.
- **After the fix:**
  - Block IDs and the line count (3,565) are unchanged, and a second run of the script finds nothing left.
  - The comparison shows only the 3 layout differences above, plus the intended `199.` normalisation.
- A backup of the pre-fix file is in [`backups/`](backups/).
- The uploaded library text still has the old spacing, so it needs a re-upload.

The source itself has **36 spaces** before punctuation (A 19, B 15, D 2). These stay, and are listed in [`pi-3-spaces-kept.md`](pi-3-spaces-kept.md). Both D cases are on line 839: `upasampādenti …pe…` and `upasampādetabbo …pe…`.

### 2. Hierarchy: two unnumbered sub-headings nested by the vault ✅ KEPT as a vault convention (2026-11-17)

> **Decision:** keep the nesting where the unnumbered heading belongs to the numbered section above it. This is this vault's convention only, registered in [`vault-annex.md`](../../4-SYSTEM/Guidelines/vault-annex.md) §2 "Registered deviations". No change to the file.

In the XML, every section heading is a `<p rend="subhead">` directly under its khandhaka, including two unnumbered ones. The vault puts these two **one level deeper**, under the kathā before them:

```
### 1. Mahākhandhako                              ^3-1-0
#### 14. Sāriputtamoggallānapabbajjākathā          ^3-1-14-0
##### Abhiññātānaṃ pabbajjā                        ^3-1-14-1-0   ← XML: same rank as "14."
#### 15. Upajjhāyavattakathā                       ^3-1-15-0
…
### 5. Cammakkhandhako                             ^3-5-0
#### 147. Soṇakoḷivisavatthu                       ^3-5-1-0
##### Soṇassa pabbajjā                             ^3-5-1-1-0    ← XML: same rank as "147."
```

This makes sense: an unnumbered heading inside a numbered series reads as a sub-section. But it is the vault's own interpretation, not the source's.
- **To match the XML:** move each to `####` with its own sibling ID. That would renumber the IDs of every later kathā in those two khandhakas.
- **To keep it:** record it as a deliberate choice.

### 3. Faithful to the source ℹ️

- **Continuous section numbers.** The section headings run 1–280 across the whole book, as printed. The ID ordinals restart in each khandhaka: `68. Sannipātānujānanā` is `^3-2-1-0`.
- **Uddāna headings.** Each khandhaka ends with a `Tassuddānaṃ` heading, as in the source.
- **The 280 "level mismatches" in the detail report are false positives.** The XML has no `title` level, so its `subhead` sits directly under the khandhaka. The vault correctly puts it one level below the khandhaka.
- **TOC reference.** tipitaka.org's TOC (`vin02m2.mul.toc.xml`) lists the 10 khandhakas, which matches.
