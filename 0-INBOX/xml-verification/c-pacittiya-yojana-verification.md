# pi-pacittiya-yojana (Pācityādiyojanā, Pācittiya) vs tipitaka-xml — verification

- **Date:** 2026-11-17
- **Vault file:** `1-SOURCES/Commentaries/pi-pacittiya-yojana.md`
- **Source:** `tipitaka-xml/romn/vin12t.nrf.xml`, which holds the Pācityādiyojanā on the four later books. The Pācittiya part was cut out with [`slice_xml.py`](slice_xml.py), from the first homage line up to, not including, the second one, which opens `Mahāvaggayojanā`. That is 1,004 of 2,992 blocks, ending at `Bhikkhunīnaṃ vibhaṅgassa, samatto yojanānayoti.`, the vault file's last line. The slice is `tmp/vin12t-pacittiya.xml`.
- **Method:** the same as [`c-parajika-vajirabuddhi-verification.md`](c-parajika-vajirabuddhi-verification.md).
- **Outputs:** [`c-pacittiya-yojana-detail.md`](c-pacittiya-yojana-detail.md), [`c-pacittiya-yojana-headings.md`](c-pacittiya-yojana-headings.md), [`c-pacittiya-yojana-spaces-kept.md`](c-pacittiya-yojana-spaces-kept.md).

## Result: content ✅, heading tree ⚠️ (flat, as in the XML)

| Check | XML slice | Vault | |
|---|---|---|---|
| Lines | 1,004 | 1,004 | identical, same order |
| Words added, missing or changed | | | **0** |
| Content block IDs | | `^2-1` … `^2-760` | sequential, no gaps or duplicates |
| Numbered paragraphs | 417 | 417 transclusion groups | every group links exactly the printed number or range |
| Transclusion targets | | 419 → `pi-2.md` | all exist |
| Headings | 237 | 237 | same text, same order; 236 have the same parent |
| Stray digits after `<pb>` | 0 | | |

The 49 lines that the comparison counts as "identical" differ only by the spacing in finding 1.

## Findings

### 1. Spaces the conversion added before punctuation ✅ FIXED 2026-11-17

- **Fixed on the user's approval:** 49 spaces removed on 49 lines, using [`fix_pb_spaces.py`](fix_pb_spaces.py). No other line was touched.
- **After the fix:**
  - Block IDs, transclusion links, the line count and the CRLF line endings are unchanged.
  - The comparison shows 1,004 / 1,004 lines identical, with 0 spacing-only differences. A second run of the script finds nothing left.
- A backup of the pre-fix file is in [`backups/`](backups/).
- The uploaded library text still has the old spacing, so it needs a re-upload.

The source itself has **2 spaces** before punctuation (B 1, C 1), which stay. The C case is line 875, `āmisagatikāni <pb/> . Etthāti`.

### 2. Heading tree: kaṇḍas and vaggas are siblings ✅ FIXED 2026-11-17

> **Fixed on the user's approval** with [`fix_pacittiya_yojana.py`](fix_pacittiya_yojana.py) (built on [`heading_tree.py`](heading_tree.py)):
> - **Bhikkhu Pācittiya kaṇḍa.** Vaggas 2–9 now sit under `#### 5. Pācittiyakaṇḍaṃ ^2-1-1-0`, after the 1st vagga's rules. The yojanā has no `1. Musāvādavaggo` heading, so those 10 rules stay directly under the kaṇḍa. This leaves the one expected "numbering restart" hint, at `2. Bhūtagāmavaggo`.
> - **Bhikkhunī Pācittiya kaṇḍa.** Vaggas 1–9 now sit under `#### 4. Pācittiyakaṇḍaṃ ^2-2-4-0`.
> - **Bhikkhunī Pāṭidesanīya.** `#### 5. Pāṭidesanīyasikkhāpada-atthayojanā ^2-2-5-0` is now its own kaṇḍa. The text closes the khuddaka part ("Bhikkhunivibhaṅge khuddakavaṇṇanāya / Yojanā samattā.") right before it.
> - **A rule the XML mis-tagged.** Bhikkhunī Andhakāravagga `5. Pañcamasikkhāpadaṃ` is tagged `subsubhead` in the XML, unlike its nine siblings, and had landed under rule 4. It is rule 5 again.
> - **One seven-level heading.** `Pakiṇṇakakathā` (line 590) is now seven levels deep and carries its title in **bold** (CLAUDE.md §5a).
>
> **Checks:**
> - **What changed:** 192 heading lines.
> - **What didn't:** every non-heading line, all 760 content IDs and all 419 root links are unchanged, as are the line count and the CRLF line endings.
> - **Re-check against the XML:** 1,004 / 1,004 lines identical, heading IDs consistent with depth.
> - **Backup:** [`backups/pi-pacittiya-yojana.pre-toc-fix.md.bak`](backups/).
>
> The description below is of the state before the fix.

The XML tags kaṇḍas **and** vaggas as `title`, so the vault puts them side by side at `####`. This is the pattern already seen in pi-1, pi-2 and pi-5.

```
### Pācittiyayojanā                          ^2-1-0
#### 5. Pācittiyakaṇḍaṃ                       ^2-1-1-0
##### 1. Musāvādasikkhāpada-atthayojanā       ^2-1-1-1-0   ← the yojanā has no "1. Musāvādavaggo" heading,
#### 2. Bhūtagāmavaggo                        ^2-1-2-0        so the 1st vagga's rules sit directly under the kaṇḍa
…
#### 9. Ratanavaggo                           ^2-1-9-0
#### 6. Pāṭidesanīyakaṇḍaṃ                    ^2-1-10-0
### Bhikkhunīvibhaṅgo                        ^2-2-0
#### 4. Pācittiyakaṇḍaṃ                       ^2-2-4-0     ← empty; its 9 vaggas are its siblings
#### 1. Lasuṇavaggo                           ^2-2-5-0
#### 9. Chattupāhanavaggo                     ^2-2-13-0
##### 5. Pāṭidesanīyasikkhāpada-atthayojanā   ^2-2-13-12-0 ← tagged subhead, so it lands inside the 9th vagga
```

- **The fix** would nest the vaggas 2–9 under `5. Pācittiyakaṇḍaṃ` and the 9 bhikkhunī vaggas under `4. Pācittiyakaṇḍaṃ`. It would also raise the bhikkhunī Pāṭidesanīya to a kaṇḍa of its own. Heading IDs `^2-1-2-0` … and `^2-2-5-0` … would change. The paragraph IDs `^2-N` would not.
- **`Pakiṇṇakakathā`** (line 590) is the one parent difference the checker reports. The vault nests it under `3. Bhikkhunupassayasikkhāpadaṃ`, where the XML has it as a sibling. That reads correctly, so no change is needed.

### 3. Faithful to the source ℹ️

- **`Bhikkhunīvibhaṅgo`** is a `###` sibling of `Pācittiyayojanā`, as in the XML (both `chapter`).
- **The 232 "level mismatches" in the content report are false positives.** The XML has no divs.
