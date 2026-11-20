# pi-4 (Cūḷavaggapāḷi) vs tipitaka-xml — verification

- **Date:** 2026-11-17
- **Vault file:** `1-SOURCES/Text/pi-4.md`
- **Source:** `tipitaka-xml/romn/vin02m3.mul.xml` (1 book div, 12 khandhaka divs)
- **Method:** the same as pi-1 ([`pi-1-verification.md`](pi-1-verification.md)).
- **Full output:** [`pi-4-detail.md`](pi-4-detail.md)

## Result: content ✅ (2 layout-only differences)

| Check | XML | Vault | |
|---|---|---|---|
| Lines | 2,821 | 2,822 | 2,819 identical; the 2 others are below |
| Numbered paragraphs | 455 (¶1–¶458; some numbers are ranges) | 455 blocks `^4-N` | every ID equals its printed number |
| Words added, missing or changed | | | **0** |
| Headings | 207 | 207 | same text and order (one heading's note was moved out, see below) |
| Heading IDs vs `#` depth | | | all consistent, no skipped levels |
| Stray digits after `<pb>` | 0 | | |

The two differences change layout only, not text:

1. **A heading's note became its own block (line 1218 → 1220).**
   - In the XML, the heading `10. Dutiyanavakaṃ` carries a long editorial `<note>`. The note explains that old manuscripts mixed this navaka up, and it quotes the clean Sinhalese/Siamese reading, ¶183 (1-9).
   - The vault keeps the heading as `#### 10. Dutiyanavakaṃ ^4-3-10-0` and puts the note on its own line right after it: `{idaṃ navakaṃ …} ^4-U1`.
   - The note text matches the XML **exactly**, including the source's `§` separators. This is why the vault has one more line.
2. **Line 2494.** The XML note has a leading space, `353. { a. ni. 10.37}`. The vault writes `{a. ni. 10.37}`, as for all other notes.

## Findings

### 1. Spaces the conversion added before punctuation ✅ FIXED 2026-11-17

This is the same artifact as in pi-1 to pi-3: `word<pb/>.` became `word .`.

- **Fixed on the user's approval:** 499 spaces removed on 441 lines, using [`fix_pb_spaces.py`](fix_pb_spaces.py). No other line was touched.
  - The script now also handles a note split out of a heading. Re-running it on pi-1, pi-2 and pi-3 changes nothing.
- **After the fix:**
  - Block IDs and the line count (3,510) are unchanged, and a second run of the script finds nothing left.
  - The comparison shows 2,819 / 2,821 lines identical with 0 spacing-only differences; the 2 remaining are the layout differences above.
- A backup of the pre-fix file is in [`backups/`](backups/).
- The uploaded library text still has the old spacing, so it needs a re-upload.

The source itself has **20 spaces** before punctuation (A 5, B 9, D 6). These stay, and are listed in [`pi-4-spaces-kept.md`](pi-4-spaces-kept.md). All 6 D cases are a space after a variant note, e.g. `{osaṇhenti (sī. syā.)} …pe…`.

### 2. Hierarchy: unnumbered sections nested under the numbered ones ✅ KEPT as a vault convention (2026-11-17)

> **Decision:** keep the nesting where the unnumbered heading belongs to the numbered section above it. This is this vault's convention only, registered in [`vault-annex.md`](../../4-SYSTEM/Guidelines/vault-annex.md) §2 "Registered deviations". No change to the file.

In the XML every section heading is a flat `<p rend="subhead">` under its khandhaka. The vault nests each **unnumbered** subhead under the **numbered** subhead before it:

```
### 1. Kammakkhandhakaṃ                ^4-1-0
#### 1. Tajjanīyakammaṃ                ^4-1-1-0
##### Adhammakammadvādasakaṃ           ^4-1-1-1-0
##### Dhammakammadvādasakaṃ            ^4-1-1-2-0   …
### 6. Senāsanakkhandhakaṃ             ^4-6-0
#### 1. Paṭhamabhāṇavāro                ^4-6-1-0
##### Vihārānujānanaṃ                  ^4-6-1-1-0   …
```

- This applies to **123 headings**.
- pi-3 used the same rule for its two unnumbered subheads.
- In pi-4 the nesting reads correctly throughout: sections sit under their kamma, bhāṇavāra or samatha.
- `Khuddakavatthūni` (5th khandhaka) has no numbered heading before it, so it stays directly under the khandhaka.

The text is the same either way. Only the TOC depth differs from the source. Record it as a deliberate convention, or flatten it later if the TOC must mirror the XML exactly.

### 3. Faithful to the source ℹ️

- **The 70 "level mismatches" in the detail report are false positives.** The XML has no `title` level, so its `subhead` sits directly under the khandhaka.
- **TOC reference.** tipitaka.org's TOC (`vin02m3.mul.toc.xml`) lists the 12 khandhakas, which matches.
