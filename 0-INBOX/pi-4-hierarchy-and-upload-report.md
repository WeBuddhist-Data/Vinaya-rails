# Cūḷavaggapāḷi (`pi-4`) — root text and commentaries: structure, content, and upload

**Date:** 2026-11-12  
**Texts:**

- Root: `1-SOURCES/Text/pi-4.md` (Cūḷavaggapāḷi, Vinaya book 4)
- `1-SOURCES/Commentaries/pi-culavagga-atthakatha.md` (Cūḷavagga-aṭṭhakathā)
- `1-SOURCES/Commentaries/pi-culavagga-saratthadipani.md` (Sāratthadīpanī-ṭīkā)
- `1-SOURCES/Commentaries/pi-culavagga-vimativinodani.md` (Vimativinodanī-ṭīkā)
- `1-SOURCES/Commentaries/pi-culavagga-vajirabuddhi.md` (Vajirabuddhi-ṭīkā)
- `1-SOURCES/Commentaries/pi-culavagga-yojana.md` (Pācityādiyojanā)

**Checked against three references:**

- **tipitaka.app:** `vp-cv` for the root, and `atta-vp-cv`, `tika-vp-pct`, `tika-vimativinodani-tika`, `tika-vajirabuddhi-tika` and `tika-pacityadiyojanapali` for the commentaries, downloaded 2026-11-12.
- **[VipassanaTech/tipitaka-xml](https://github.com/VipassanaTech/tipitaka-xml):** `romn/` at `c65aa30` (no `romn/` changes on `main` since): `vin02m3.mul`, `vin02a3.att`, `vin02t.tik`, `vin07t.nrf`, `vin06t.nrf`, `vin12t.nrf`.
- **The commentaries' own text:** their printed paragraph numbers, book headings and closing lines.

**How it was built:** the body and structure follow the Vinaya's own sources, in the printed form the repo has and the site shows. From the Abhidhamma vault only the *way of working* is taken (check, build, dry run, upload root then commentaries, read back, report), and its alignment and segment-type rules.

**All six texts are uploaded to prod** (`https://library-prod.webuddhist.com`) and read back.

---

## Built in the source form

All six files were built on 2026-11-12 with the current build, and the source form is its last step (`4-SYSTEM/scripts/tipitaka-xml-to-json/source_form.py`):

- **Printed numbers stay:**
  - on headings: 82 in the root (`1. Kammakkhandhakaṃ`), 12 in each ṭīkā and the aṭṭhakathā, 50 in the Yojanā;
  - at the start of the 455 root paragraphs (`1. Tena samayena…`).

  The block ID still records the number.
- **The piṭaka heading is printed `Vinayapiṭake`.**
- **Variant-reading notes are `{…}`**, as on the site (485 in the root). Brackets inside a note's own text stay. The root has no bracket that is not a note.
- **One heading carries a long note in the source:** `<p rend="subhead">10. Dutiyanavakaṃ <note>idaṃ navakaṃ porāṇapotthakesu…</note>`. The heading is `10. Dutiyanavakaṃ` (`^4-3-10-0`), as the site's contents tree titles it, and the note is its own block right under it (`^4-U1`). On the site both are one line; the heading and the note together are that line word for word. The build step now matches a heading and its note this way; pi-1 to pi-3 come out unchanged with it.
- **Each ṭīkā names the commentary it explains:** `commentary: 1-SOURCES/Commentaries/pi-culavagga-atthakatha.md`.

Every source word is present in order (fidelity check: root 96,649 words; commentaries 24,503 / 15,052 / 8,169 / 5,366 / 21,935). The source form changed only what it is meant to: every block ID and every link stayed the same.

### What was checked and left unchanged

| Item | Why nothing was changed |
|---|---|
| Root paragraphs 77–79 | the XML has none: it prints `76.` then `80.`, and so does the site. The root's numbered IDs run `^4-1` … `^4-458` without them |
| Vajirabuddhi heading *Saṅghabhattādianujānanakathāvaṇṇanā* | it has no text of its own, in the XML and on the site; it is kept as printed |
| Each ṭīkā part's top `# Vinayapiṭake` | the XML prints it once, at the start of each work. Every file needs one top heading as the root of its contents tree. Every other heading is printed in the XML at that point |
| Ranges linked in full | the site links a range by its first number only; ours links every paragraph in it (Sāratthadīpanī 2, Vimativinodanī 13, Vajirabuddhi 16, Yojanā 1 truncated-tail ranges such as `313-4.` = 313–314, recorded in `source_note`) |
| Bold | the site shows bold lemmas; the library stores plain text, so the files carry none |

---

## Root text (`pi-4.md`)

- **207 headings**, levels `#` to `#####` (1 / 1 / 12 / 71 / 122): the twelve khandhakas, from `1. Kammakkhandhakaṃ` to `12. Sattasatikakkhandhakaṃ`, and their sections. No level is skipped, every child ID extends its parent's, siblings run 1…n, and every heading has text under it.
- **457 content IDs:**
  - the homage `^T-1`;
  - 1 unnumbered block `^4-U1` (the Dutiyanavakaṃ note);
  - 455 numbered paragraphs `^4-1` … `^4-458`.
- **2,158 continuation lines.**
- **Against tipitaka-xml (strict):**
  - 2,822 lines, 0 text differences apart from the Dutiyanavakaṃ heading and note above;
  - 207 of 207 headings;
  - every one of the 455 printed numbers starts its own block.
- **Against tipitaka.app:** 2,820 of 2,822 lines exactly equal — the other two are the Dutiyanavakaṃ heading and its note, which make up the site's one line; 205 of 205 headings below the title in the site's tree, with 0 differences in parent, position, children or ID path.

---

## Commentaries

| | Headings | Levels (`#` … ) | Content IDs | Lines = tipitaka.app | Tree vs tipitaka.app | tipitaka-xml (strict) |
|---|---|---|---|---|---|---|
| aṭṭhakathā | 81 | 1 / 1 / 12 / 67 | `^T-1`, `^4-1` … `^4-576` | 669 of 669 | 79 of 79 | 0 differences |
| Sāratthadīpanī | 79 | 1 / 1 / 12 / 65 | `^T-1`, `^4-1` … `^4-312` | 402 of 402 | 77 of 77 | 0 differences |
| Vimativinodanī | 52 | 1 / 1 / 12 / 38 | `^T-1`, `^4-1` … `^4-309` | 362 of 362 | 50 of 50 | 0 differences |
| Vajirabuddhi | 49 | 1 / 1 / 12 / 35 | `^T-1`, `^4-1` … `^4-147` | 212 of 212 | 47 of 47 | 0 differences |
| Yojanā | 82 | 1 / 1 / 1 / 12 / 58 / 9 | `^T-1`, `^4-1` … `^4-489` | 574 of 574 | 80 of 80 | 0 differences |

No duplicate IDs, no skipped levels, every ID is its tree path, every heading has text under it except the one Vajirabuddhi heading above.

---

## Links to the root text (alignment)

| | Linked paragraphs | Link lines | Distinct root targets | Alignment pairs (prod) | Commentary segments aligned |
|---|---|---|---|---|---|
| aṭṭhakathā | 186 | 187 | 186 | 504 | 503 of 577 |
| Sāratthadīpanī | 137 | 164 | 164 | 343 | 303 of 313 |
| Vimativinodanī | 135 | 159 | 159 | 317 | 281 of 310 |
| Vajirabuddhi | 105 | 128 | 128 | 168 | 143 of 148 |
| Yojanā | 180 | 181 | 180 | 416 | 415 of 490 |

The pairs follow the Abhidhamma rule: a group of links aligns every commentary block after it until the next group of links or the next heading.

**Checks:**

- **tipitaka-xml:** every numbered paragraph has exactly the links for its printed number, with ranges expanded, directly before it; every target exists in `pi-4.md` (0 errors).
- **tipitaka.app:** all **186** of the site's aṭṭhakathā → root paragraph links are in our transclusions. For the Cūḷavagga, the site has no paragraph-number links from the aṭṭhakathā to the ṭīkās, so there is nothing further to compare.
- **Sections:** all 819 links land in the khandhaka the commentary paragraph sits in.
- **Layers agree:** every ṭīkā link shares a root paragraph with the aṭṭhakathā or falls in a section the aṭṭhakathā also covers, except 9. Each of those 9 quotes a word that is in the root paragraph it links to:
  - Sāratthadīpanī `182.` *sambahulā saṅghādisesā āpattiyo āpajjati parimāṇampi*, `437.` *pāvāya kusināraṃ*, `445.` *ujjavanikāya*;
  - Vimativinodanī `437.` *apāvuso, amhākaṃ satthāraṃ jānāsī*, `445.` *ujjavanikāya*;
  - Vajirabuddhi `200.` *appaṭiññāya bhikkhūnaṃ kammāni karonti*, `437.` *chinnapātaṃ*, `445.` *tvaṃyeva* (the root: *tvaṃyeva channassa bhikkhuno brahmadaṇḍaṃ…*);
  - Yojanā `200.` *paṭiññā*.
- **Meaning:** at least half the quoted (bold) words of a paragraph occur in the root passage it links to (for the ṭīkās, the aṭṭhakathā on the same root paragraphs counts too) in the share of paragraphs below.

  | aṭṭhakathā | Sāratthadīpanī | Vimativinodanī | Vajirabuddhi | Yojanā |
  |---|---|---|---|---|
  | 175 of 176 | 134 of 135 | 135 of 135 | 88 of 94 | 174 of 175 |

  The rest were read against the whole root paragraph and are linked right. The aṭṭhakathā's `97.` and the Sāratthadīpanī's `294.` open with the root's own words (*chārattaṃ mānattaṃ*, *senāsanaṃ apaññattaṃ hoti*) and go on in their own terms. The others name a khandhaka (*kammakkhandhake*, *cīvarakkhandhake*), give a story's title, or gloss a word in another form than the root's (Vajirabuddhi `303.` *Sudhālepo* for the root's *sudhāmattikālepanaṃ*; `252.` *Anupariyāyī* for *anupariyāyi*). The Yojanā's `82.` explains words of the aṭṭhakathā (*Itaro*, *vattabhede*), which that work has at `81.`; `82.` is the number the source prints.
- **No links between commentary layers.**

---

## Titles

| Text | Ours (file = prod) | tipitaka.app | `##` book heading | Last line |
|---|---|---|---|---|
| Root | Cūḷavaggapāḷi | Cūḷavaggapāḷi | Cūḷavaggapāḷi | Cūḷavaggapāḷi niṭṭhitā. |
| aṭṭhakathā | Cūḷavagga-aṭṭhakathā | Cūḷavagga-aṭṭhakathā | Cūḷavagga-aṭṭhakathā | Cūḷavagga-aṭṭhakathā niṭṭhitā. |
| Sāratthadīpanī | Sāratthadīpanī-ṭīkā (Cūḷavagga) | Sāratthadīpanī-ṭīkā (Pācittiyādi) | Cūḷavagga-ṭīkā | Cūḷavaggavaṇṇanā niṭṭhitā. |
| Vimativinodanī | Vimativinodanī-ṭīkā (Cūḷavagga) | Vimativinodanī-ṭīkā | Cūḷavaggavaṇṇanā | Cūḷavaggavaṇṇanānayo niṭṭhito. |
| Vajirabuddhi | Vajirabuddhi-ṭīkā (Cūḷavagga) | Vajirabuddhi-ṭīkā | Cūḷavaggavaṇṇanā | Cūḷavaggavaṇṇanā niṭṭhitā. |
| Yojanā | Pācityādiyojanā (Cūḷavagga) | Pācityādiyojanāpāḷi | Pācityādiyojanā | Cūḷavaggakhandhakassa, samatto yojanānayoti. |

The ṭīkā and Yojanā titles add the part, "(Cūḷavagga)", by the same rule as pi-1 to pi-3: each is one part of a work that spans several books, and the library needs a unique title for it. All six carry `category_id: 4wuvGxIgXNZ5mb0bDWvkC`, `tag_ids: [296WZOr8MXWteSqBBI7pl]` and `license: cc0`, as pi-1 to pi-3 do.

---

## Library upload (prod)

Uploaded on 2026-11-12 to `https://library-prod.webuddhist.com`: `root-text-upload` for the root, then `commentary-upload` once per commentary. Each commentary followed a dry run whose characters, segment, contents-tree and pair counts matched the ones checked beforehand. Each commentary is a `commentary_of` the Cūḷavaggapāḷi and aligned to its edition.

| | text_id | edition_id | toc_id | Characters | Segments | TOC nodes | Alignment pairs |
|---|---|---|---|---|---|---|---|
| Cūḷavaggapāḷi | `f3Ai1VjpwISPoauHYGms3` | `5H1pn627NnQSdaoR8tm41` | `WebqDfM9Wtm4ggHqYb2E6` | 894,318 | 457 | 207 | — |
| aṭṭhakathā | `KZOMp52ShwAAWSPsv3Df8` | `k6fcIWWa2vO1lUbEqsypj` | `j2ZT9vGLttMEFGC3yp46c` | 227,199 | 577 | 81 | 504 |
| Sāratthadīpanī | `S0VZUoy0iHwRShwIL6pGP` | `SrVOfbmgdZqqnyywCZJET` | `bWQLxTGlQbYD6wZuUziaB` | 143,129 | 313 | 79 | 343 |
| Vimativinodanī | `qbE0l0yeCg4y4ObTAChS6` | `lQkt254Ez1GuPbc91ZN3l` | `pN1HOdHKXzR4zPuXmCBuj` | 83,131 | 310 | 52 | 317 |
| Vajirabuddhi | `VyiiYnrggyU0AeTyrvxxH` | `oUrhQKqYRWMJFLmlEo8F2` | `fVKwzMXy5YVMKpewBoqCE` | 50,470 | 148 | 49 | 168 |
| Yojanā | `yzydhNpQTaVXL6COSI7NW` | `jJCCXyPh4kPfsc5VHiyGb` | `dOQYCUuq5jX0WeV1X3LUI` | 210,911 | 490 | 82 | 416 |

**Read back from prod (2026-11-12), all six texts:**

- **Root record:** the root lists all five commentaries, with the category, tag and licence above.
- **Segments:** the same references in the same order as the file's blocks, and each segment's text is identical to its block. The root's are `verse`; every commentary segment is `paragraph`, the homage `T-1` `top_segment`.
- **Table of contents:** one node per heading, with the same title and depth in the same order, and every span right.
- **Alignments:** the live pairs equal the parser output, and their root targets are exactly the file's transclusion targets. They run commentary → root only.
- **Frontmatter:** the upload added only the IDs (`commentary_of`, `text_id`, `edition_id`, `toc_id`, `aligned_to_edition_id`).

The committed linter and parser output was regenerated from the final files and equals what was uploaded.

---

## Things to know

- **The upload scripts' default host is not prod.** Set `WEBUDDHIST_API_BASE=https://library-prod.webuddhist.com`. Prod needs the API key even for reads; it is in the git-ignored `4-SYSTEM/scripts/.env`.
- **Use `/opt/homebrew/bin/python3.11`.** It has both PyYAML and root certificates; `/usr/local/bin/python3.13` fails the HTTPS calls.
- **The linters rewrite `languages.py`.** Both were restored to the vault's version after the runs.
- **Not looked at:** the WeBuddhist reader.

## Files

Committed in three batches, after the upload:

1. the root: `pi-4.md` with its library IDs, `0-INBOX/raw-data/vin02m3.json`, `4-SYSTEM/scripts/linter-root-text/output/pi-4.lint.json`, `4-SYSTEM/scripts/parser-root-text/output/pi-4/` (edition, text, toc), the root upload ledger, and the build fix in `source_form.py` (a heading's note matched as heading, then note);
2. the aṭṭhakathā, Sāratthadīpanī and Vimativinodanī with their IDs, their linter output (`4-SYSTEM/Skills/commentary-upload/scripts/linter-commentary/output/`) and parser output (`…/parser-commentary/output/pi-culavagga-*/`: alignment, edition, text, toc), `0-INBOX/raw-data/vin02a3.json`, and the commentary ledger with their entries;
3. the Vajirabuddhi and Yojanā the same way, the full commentary ledger, and this report.

## Related

- pi-1 to pi-3 reports: `0-INBOX/pi-1-hierarchy-and-upload-report.md`, `0-INBOX/pi-2-hierarchy-and-upload-report.md`, `0-INBOX/pi-3-hierarchy-and-upload-report.md`
- tipitaka-xml check of all Vinaya files: `0-INBOX/vinaya-tipitaka-xml-audit.md`
