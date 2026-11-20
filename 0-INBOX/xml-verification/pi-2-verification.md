# pi-2 (Pācittiyapāḷi) vs tipitaka-xml — verification

- **Date:** 2026-11-13
- **Vault file:** `1-SOURCES/Text/pi-2.md`
- **Source:** `tipitaka-xml/romn/vin02m1.mul.xml`. TOC reference: `tipitaka.org/romn/cscd/vin02m1.mul.toc.xml`.
- **Method:** the same as pi-1 ([`pi-1-verification.md`](pi-1-verification.md)), using [`compare_vin.py`](compare_vin.py).
- **Full output:** [`pi-2-detail.md`](pi-2-detail.md)

## Result: content ✅

| Check | XML | Vault | |
|---|---|---|---|
| Lines (headings + paragraphs + trailers) | 3,690 | 3,690 | identical, same order |
| Numbered paragraphs | ¶1–¶1242 | `^2-1` … `^2-1242` | every ID equals its printed number |
| Text differences | | | **0** |
| Headings | 260 | 260 | same text, same order |
| Heading IDs vs `#` depth | | | all consistent, no skipped levels |
| Unnumbered blocks | | 11 | `^2-U*`, as in pi-1 |

## Findings

### 1. Spaces the conversion added before punctuation ✅ FIXED 2026-11-13

This is the same artifact as in pi-1: `word<pb/>.` became `word .`.

- **Fixed on the user's approval:** 257 spaces removed on 233 lines, using [`fix_pb_spaces.py`](fix_pb_spaces.py).
- Re-running the comparison gives 3,690 / 3,690 lines identical, with 0 spacing-only differences.
- Block IDs and the line count (5,226) are unchanged.
- A backup of the pre-fix file was kept outside the vault.
- The uploaded library text still has the old spacing, so it needs a re-upload.

The source itself has **24 spaces** before punctuation. These stay, by the same decision as for pi-1, and are listed in [`pi-2-spaces-kept.md`](pi-2-spaces-kept.md).

| Type | Count | Example |
|---|---|---|
| A: `word <pb/>…` | 8 | |
| B: `word <pb/> …pe…` | 12 | |
| C: `word <pb/>,` / `.` | 3 | ¶ line 846 `samayo <pb/>. Satthagam…` · line 994 `Gaṇabhojane <pb/>, aññatra` · line 5172 `bhuñjeyya <pb/>, paṭidesetabbaṃ` |
| D: plain source space | 1 | line 2347 `bhagavā …pe… kathañhi` |

### 2. Hierarchy: Bhikkhunī Nissaggiya `Pattavaggo` is flattened ✅ FIXED 2026-11-17

> **Fixed on the user's approval** with [`nest_vaggas.py`](nest_vaggas.py) (`pi-2.md ^2-5-3-0`). The 12 sikkhāpadas now sit one level under `##### 1. Pattavaggo ^2-5-3-1-0`, from `###### 1. Paṭhamasikkhāpadaṃ ^2-5-3-1-1-0` to `###### 12. Dvādasamasikkhāpadaṃ ^2-5-3-1-12-0`. That is the same shape as the Bhikkhunī Pācittiya vaggas.
>
> - **What changed:** 12 heading lines.
> - **What didn't:** every non-heading line and all 1,253 paragraph IDs are unchanged, as are the line count and the CRLF line endings.
> - **Re-check against the XML:** 3,690 / 3,690 lines identical, heading IDs consistent with depth, no hierarchy hints.
> - **Links:** nothing in the vault linked to the old heading IDs.
> - **Backup:** [`backups/pi-2.pre-toc-fix.md.bak`](backups/).
> - **Library:** the uploaded TOC needs a re-upload.
>
> The description below is of the state before the fix.

This is the same problem as the pi-1 Nissaggiya: the source tags the vagga and its sikkhāpadas alike (`subhead`).

```
#### 3. Nissaggiyakaṇḍaṃ (bhikkhunīvibhaṅgo)  ^2-5-3-0
##### 1. Pattavaggo                        ^2-5-3-1-0
##### 1. Paṭhamasikkhāpadaṃ                ^2-5-3-2-0   ← should be ###### ^2-5-3-1-1-0
…
##### 12. Dvādasamasikkhāpadaṃ             ^2-5-3-13-0  ← ^2-5-3-1-12-0
```

- 13 heading IDs would change. The paragraph IDs `^2-N` would not.
- The Bhikkhunī Pācittiyakaṇḍa (Lasuṇavaggo …) **is** nested correctly: vagga, then sikkhāpada.

### 3. Faithful to the source, but worth knowing ℹ️

- **Abbreviated source.** In the Bhikkhunī Sekhiya, the source gives only `1. Parimaṇḍalavaggo` and `7. Pādukavaggo`, so they get the IDs `^2-5-6-1-0` and `^2-5-6-2-0`.
- **Merged rules.** In the Chattupāhanavaggo, the source merges three rules into `8-9-10. Aṭṭhama-navama-dasamasikkhāpadaṃ` (`^2-5-4-9-8-0`). From there the IDs no longer match the printed numbers: rule 11 is `^2-5-4-9-9-0`.
- **No Mahāvibhaṅga heading.** The book starts at `5. Pācittiyakaṇḍaṃ`, continuing the kaṇḍa numbering from pi-1. Kaṇḍas 5–8 sit directly under the book, while the Bhikkhunī kaṇḍas sit under `Bhikkhunīvibhaṅgo` (the XML `subbook` div). There is no "Mahāvibhaṅgo" heading because the XML has none. tipitaka.org's TOC lists the same 11 kaṇḍas.
- **29 "level mismatches" in the detail report are false positives.** In the Bhikkhunī kaṇḍas the XML goes straight from kaṇḍa to `subhead`, with no `title` level. The vault puts these one level below the kaṇḍa, without skipping a level, which is correct.

### 4. Stray digit in the source ℹ️

- [pi-2.md:988](../../1-SOURCES/Text/pi-2.md:988) reads `215. Tena 0 kho pana samayena…`.
- The source has `Tena <pb ed="M" n="0.0100"/>0 kho`, and `deva master` has the same `०`. So this is VRI's typo, faithfully copied. Leave it, or mark it with `[Ed: …]`.
