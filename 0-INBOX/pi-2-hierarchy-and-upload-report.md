# Pācittiyapāḷi (`pi-2`) — root text and commentaries: structure, content, and upload

**Date:** 2026-11-12  
**Texts:**

- Root: `1-SOURCES/Text/pi-2.md` (Pācittiyapāḷi, Vinaya book 2)
- `1-SOURCES/Commentaries/pi-pacittiya-atthakatha.md` (Pācittiya-aṭṭhakathā)
- `1-SOURCES/Commentaries/pi-pacittiya-saratthadipani.md` (Sāratthadīpanī-ṭīkā)
- `1-SOURCES/Commentaries/pi-pacittiya-vimativinodani.md` (Vimativinodanī-ṭīkā)
- `1-SOURCES/Commentaries/pi-pacittiya-vajirabuddhi.md` (Vajirabuddhi-ṭīkā)
- `1-SOURCES/Commentaries/pi-pacittiya-yojana.md` (Pācityādiyojanā)

**Checked against three references:**

- **tipitaka.app:** `vp-pct` for the root, and `atta-vp-pct`, `tika-vp-pct`, `tika-vimativinodani-tika`, `tika-vajirabuddhi-tika` and `tika-pacityadiyojanapali` for the commentaries (`/api/children`, `/api/text`, `/api/links`). Downloaded three times, the last on 2026-11-12; the data was identical each time.
- **[VipassanaTech/tipitaka-xml](https://github.com/VipassanaTech/tipitaka-xml):** `romn/` at `c65aa30` (current `main`): `vin02m1.mul`, `vin02a1.att`, `vin02t.tik`, `vin07t.nrf`, `vin06t.nrf`, `vin12t.nrf`. The upstream commits since the pi-1 check (`22c6232`) change only the Devanagari master, not `romn/`.
- **The commentaries' own text:** their printed paragraph numbers, book headings and colophons.

**How it was built and uploaded:** as for pi-1, and following the Abhidhamma vault's pi-1 … pi-7 uploads, which are the reference.

The live WeBuddhist **prod** library (`https://library-prod.webuddhist.com`) was read back after the upload and compared with the files. **All six texts are uploaded to prod.**

---

## Summary of changes

### What was fixed

| Issue | What was wrong | Fix | Applied to |
|---|---|---|---|
| Vajirabuddhi heading levels | the part's `##` title (`Pācittiyavaṇṇanā`) is itself a site node, so the site-tree pass levelled its children one too deep. A no-skip clamp then nested the nine bhikkhu vaggas under `Pācittiyakaṇḍo` | `apply_site_toc.py` levels that title's subtree from the title. The tree now matches tipitaka.app (194/194), with `### Pācittiyakaṇḍo` an empty label and the vaggas beside it, as in the pi-1 Vajirabuddhi. Old and new script run on all 24 Vinaya commentaries: only this file changes | Vajirabuddhi |
| No link from the ṭīkās to the aṭṭhakathā | the Abhidhamma ṭīkā files name the commentary they explain (`commentary: …-atthakatha.md`); ours did not | `commentary: 1-SOURCES/Commentaries/pi-pacittiya-atthakatha.md` added; also written by `finalize.py`. The sources say so: the Vimativinodanī closes "Iti samantapāsādikāya vinayaṭṭhakathāya vimativinodaniyaṃ", the Yojanā "Iti samantapāsādikāya vinayasaṃvaṇṇanāya". It is a vault note only and changes nothing sent to the library | the four ṭīkās |
| Commentary parser rules | the parser let a group of links run on across headings and typed every block of several lines as `verse` | it now follows the Abhidhamma parser: a heading ends the scope, and every commentary block is a `paragraph`. On the nine Vinaya commentaries, the three Dhammasaṅgaṇī commentaries and the Paṭṭhāna aṭṭhakathā, the output is identical to the Abhidhamma parser's. The Vinaya text, IDs and contents trees did not change | all five commentaries (and pi-1, re-aligned on prod the same day) |
| Ṭīkā part boundaries | the next volume's header (homage, piṭaka line, work title) was left at the end of the previous part | each part starts at its own header (fixed for pi-1, applies here too) | all four ṭīkā parts |

### What was checked and left unchanged

| Item | Why nothing was changed |
|---|---|
| Aṭṭhakathā `141-144.` | CST prints this range before the comment on the Ovāda rule, though only root `^2-144` is that rule (141–143 end the Sappāṇaka rule; the quoted *lābhino honti* is in 144). The repo marks the paragraph `n="141-144"`, so it is linked exactly as printed, which includes 144. tipitaka.app links only 141 |
| Vajirabuddhi `31-3.` | CST misprint for 231–233 (the lemmas *paṭiyāloka*, *pūvagaṇanā* are in `2-231`, `2-233`). Linked as printed, to `2-31` … `2-33`, and recorded in `source_note` |
| 37 Sāratthadīpanī paragraphs whose root links differ from the aṭṭhakathā paragraph the site joins them to | the two texts print different ranges for the same passage (e.g. aṭṭhakathā `16.`, ṭīkā `16-26.`). Each is linked as its own text prints it, and every pair overlaps |
| Seven empty kaṇḍa labels in the Vajirabuddhi (e.g. `Sekhiyakaṇḍo` under `Ratanavaggo`) | they follow the site's tree, the same pattern as the pi-1 Vajirabuddhi. The links are not affected |
| Ranges linked in full | the site links a range by its first number only; ours links every paragraph in it, as in the Abhidhamma vault |
| Upstream typo fixes | five root typos (e.g. `ukaṭṭhaṃ` → `ukkaṭṭhaṃ`, `ārācesuṃ` → `ārocesuṃ`) are fixed in tipitaka-xml's Devanagari master but not yet in `romn/`. Our file follows `romn/`; pick them up once upstream regenerates it |

### Source form (2026-11-12)

The Vinaya files keep the body and structure of their own sources; only the Abhidhamma vault's *way of working* is followed, not its format. So, as tipitaka-xml prints them and tipitaka.app shows them:

- **printed numbers stay** on headings (`1. Pārājikakaṇḍaṃ`) and at the start of root paragraphs (`1. Tena samayena…`); the block ID still records the number;
- **the piṭaka heading is `Vinayapiṭake`**, as printed (it was `Vinayapiṭake (aṭṭhakathā)` / `(ṭīkā)`);
- **variant-reading notes are `{…}`**, as on the site (a `<note>` in the XML); brackets inside a note's own text stay;
- **no homage is added** where the source prints none.

The step is `4-SYSTEM/scripts/tipitaka-xml-to-json/source_form.py`, run last in `build_roots.sh` and `build_commentary.py`. Checked with `verify.py --strict` (nothing normalised: 0 text differences) and line by line against tipitaka.app (every line exactly equal, the site's own bold and page markers aside). Bold stays plain: the library stores plain text. No block ID, heading ID, link or alignment pair changed.

On prod (same day): the root editions' text, segmentation and contents tree were replaced and every commentary's alignment put back; the commentaries got new contents trees (titles with their printed numbers, `Vinayapiṭake`). Text and edition IDs are unchanged; the new contents-tree IDs are in the files, the ledgers and the table above. Read back: text, segments, contents trees and pairs equal the files.

---

## What these files are

`pi-2.md` is the **root mūla** of the Pācittiyapāḷi (CST `vin02m1`). It has two divisions: the bhikkhu Pācittiya, Pāṭidesanīya, Sekhiya and Adhikaraṇasamatha kaṇḍas, and the Bhikkhunīvibhaṅga.

There are five commentaries:

- the **aṭṭhakathā** (`vin02a1`), the Pācittiya part of the Samantapāsādikā
- three **ṭīkās**, each the Pācittiya part of its work:
  - the Sāratthadīpanī (`vin02t`)
  - the Vimativinodanī (`vin07t`)
  - the Vajirabuddhi (`vin06t`)
- the **Pācityādiyojanā** (`vin12t`), a construing guide to the Samantapāsādikā

Each numbered commentary paragraph links to the root paragraphs it explains, and those links become the alignment in the library.

---

## How IDs work

| Track | Shape | Example | Meaning |
|---|---|---|---|
| Heading | ends in `-0` | `^2-1-1-0` | TOC node only; the ID is its path in the tree |
| Root content | book + printed paragraph number | `^2-133` | root paragraph 133 |
| Root content without a number | `U` | `^2-U3` | unnumbered root block (10) |
| Homage | `T-1` | `^T-1` | `Namo tassa bhagavato…` at the top of each file |
| Commentary content | running counter | `^2-1` … `^2-1185` | the Nth paragraph of that commentary file |
| Link to root | transclusion | `![[1-SOURCES/Text/pi-2.md#^2-133]]` | the root paragraph a commentary paragraph explains |

---

## Root text (`pi-2.md`)

- **260 headings**, levels `#` to `######` (1 / 1 / 5 / 27 / 132 / 94). No level is skipped, every child ID extends its parent's, and siblings run 1…n.
- **1,253 content IDs:** the homage `^T-1`, 10 unnumbered `^2-U…`, and 1,242 numbered paragraphs `^2-1` … `^2-1242`. **2,177 continuation lines.**
- **Against tipitaka-xml:** 3,690 lines, 1:1; 260 of 260 headings; every one of the 1,242 printed numbers starts its own block.
- **Against tipitaka.app:** 3,690 of 3,690 lines identical; 258 of 258 headings below the title match the site's tree (parent, position, children, ID path).

---

## Commentaries

| | Headings | Levels (`#` … ) | Content IDs | Opens with |
|---|---|---|---|---|
| aṭṭhakathā | 246 | 1 / 1 / 5 / 25 / 126 / 88 | `^T-1`, `^2-1` … `^2-1185` | homage |
| Sāratthadīpanī | 130 | 1 / 1 / 8 / 36 / 84 | `^T-1`, `^2-1` … `^2-566` | homage |
| Vimativinodanī | 135 | 1 / 1 / 8 / 35 / 90 | `^T-1`, `^2-1` … `^2-457` | homage |
| Vajirabuddhi | 196 | 1 / 1 / 11 / 115 / 67 / 1 | `^2-1` … `^2-499` | no homage: the one-volume Vajirabuddhi prints it once, before its Pārājika part |
| Yojanā | 237 | 1 / 1 / 2 / 24 / 207 / 2 | `^T-1`, `^2-1` … `^2-760` | homage |

| Layer | Lines identical to tipitaka.app | Headings in the site's tree | tipitaka-xml |
|---|---|---|---|
| aṭṭhakathā | 1,465 of 1,466 | 244 of 244 | 1:1, no errors |
| Sāratthadīpanī | 714 of 715 | 128 of 128 | 1:1, no errors |
| Vimativinodanī | 597 of 598 | 133 of 133 | 1:1, no errors |
| Vajirabuddhi | 716 of 717 | 194 of 194 | 1:1, no errors |
| Yojanā | 1,003 of 1,004 | 235 of 235 | 1:1, no errors |

The one line in each file not on the site is the piṭaka label. Each ṭīkā part starts and ends exactly where the site's Pācittiya part does.

---

## Links to the root text (alignment)

| | Linked paragraphs | Link lines | Distinct root targets | Alignment pairs (prod) | Commentary segments aligned |
|---|---|---|---|---|---|
| aṭṭhakathā | 463 | 524 | 524 | 1,389 | 1,176 of 1,186 |
| Sāratthadīpanī | 233 | 325 | 325 | 820 | 565 of 567 |
| Vimativinodanī | 229 | 444 | 444 | 793 | 457 of 458 |
| Vajirabuddhi | 251 | 351 | 351 | 670 | 482 of 499 |
| Yojanā | 417 | 419 | 419 | 751 | 747 of 761 |

The pairs follow the Abhidhamma rule: a group of links aligns every commentary block after it until the next group of links or the next heading.

**Checks:**

- **tipitaka-xml:** every numbered paragraph has exactly the links for its printed number, with ranges expanded, directly before it. Every target exists in `pi-2.md` (0 errors).
- **tipitaka.app:**
  - **Aṭṭhakathā → root:** all **463** of the site's links are in our transclusions.
  - **Sāratthadīpanī:** 209 of the site's 397 links fall in our Pācittiya part. For 172 of them, the ṭīkā and aṭṭhakathā paragraphs link to the same root paragraphs; the other 37 are the overlapping printed-range differences.
  - The site has no links for the Vimativinodanī, Vajirabuddhi or Yojanā.
- **Sections:** all 2,063 links land in the commentary paragraph's own division (bhikkhu or bhikkhunī). At the level of the individual rule, the few name mismatches are the commentary's own "the fifth [rule] is plain" paragraphs (`169. Pañcamaṃ uttānatthameva`), or headings that cover a vagga or a run of rules (`Paṭhamādisikkhāpadavaṇṇanā`). Each was read.
- **Meaning:** the share of paragraphs where at least half the quoted (bold) words occur in the root passage they link to. For the ṭīkās, the aṭṭhakathā on the same root paragraphs counts too. The rest quote other works or teachers (*Mahāaṭṭhakathā*, *gaṇṭhipada*, *dhammasiritthero*).

  | aṭṭhakathā | Sāratthadīpanī | Vimativinodanī | Vajirabuddhi | Yojanā |
  |---|---|---|---|---|
  | 432 of 437 | 184 of 190 | 176 of 182 | 164 of 194 | 363 of 371 |
- **Layers agree:** every ṭīkā link shares a root paragraph with the aṭṭhakathā or falls in a rule the aṭṭhakathā covers. The one exception, Vajirabuddhi `289. Rahonisajjasikkhāpadaṃ uttānatthameva`, is covered by the aṭṭhakathā's `284.`.
- **No links between commentary layers.** Every commentary aligns only to the root, as in the Abhidhamma vault.

---

## Titles

| Text | Ours (file = prod) | tipitaka.app | tipitaka-xml book heading | Last line |
|---|---|---|---|---|
| Root | Pācittiyapāḷi | Pācittiyapāḷi | Pācittiyapāḷi | Pācittiyapāḷi niṭṭhitā. |
| aṭṭhakathā | Pācittiya-aṭṭhakathā | Pācittiya-aṭṭhakathā | Pācittiya-aṭṭhakathā | Ubhatovibhaṅgaṭṭhakathā niṭṭhitā. |
| Sāratthadīpanī | Sāratthadīpanī-ṭīkā (Pācittiya) | Sāratthadīpanī-ṭīkā (Pācittiyādi) | Sāratthadīpanī-ṭīkā (tatiyo bhāgo) | Pācittiyavaṇṇanā niṭṭhitā. |
| Vimativinodanī | Vimativinodanī-ṭīkā (Pācittiya) | Vimativinodanī-ṭīkā | Vimativinodanī-ṭīkā (dutiyo bhāgo) | Ubhatovibhaṅgaṭṭhakathāvaṇṇanā niṭṭhitā. |
| Vajirabuddhi | Vajirabuddhi-ṭīkā (Pācittiya) | Vajirabuddhi-ṭīkā | — (part heading `Pācittiyavaṇṇanā`) | Ubhatovibhaṅgaṭṭhakathāvaṇṇanā niṭṭhitā. |
| Yojanā | Pācityādiyojanā (Pācittiya) | Pācityādiyojanāpāḷi | Pācityādiyojanā | … samatto yojanānayoti. |

The ṭīkā and Yojanā titles add the part, "(Pācittiya)", by the same rule as pi-1. The library needs a unique title for each part of a work that spans several books. All six carry `category_id: 4wuvGxIgXNZ5mb0bDWvkC`, `tag_ids: [296WZOr8MXWteSqBBI7pl]` and `license: cc0`.

---

## Library upload (prod)

Uploaded on 2026-11-12 to `https://library-prod.webuddhist.com`: `root-text-upload` for the root, then `commentary-upload` once per commentary, each after a dry run whose counts matched the ones agreed beforehand. Each commentary is a `commentary_of` the Pācittiyapāḷi and aligned to its edition. The IDs are in each file's frontmatter and in the upload ledgers.

| | text_id | edition_id | toc_id | Characters | Segments | TOC nodes | Alignment pairs |
|---|---|---|---|---|---|---|---|
| Pācittiyapāḷi | `QUJx63k0I45O2i7ypmZRP` | `MAjWAYsgc2Iyv5wtXcOcc` | `MFluV3CnTeHPDg8jVtwjx` | 738,928 | 1,253 | 260 | — |
| aṭṭhakathā | `zyKRXBrnCwF2C09KgyDtp` | `lWE26PLVKL3OZJC1rvSVM` | `qcCFqKJLR7lYSoRkRv3PB` | 359,193 | 1,186 | 246 | 1,389 |
| Sāratthadīpanī | `tqqaZvFMtg2ZyqqO8YD1v` | `BoRg7jYapQfMppmuVrAD7` | `k5traw26hraiDBSUVDknB` | 203,214 | 567 | 130 | 820 |
| Vimativinodanī | `wKH7J4lNoLp5ZzfRuv4Uk` | `zaq0MP3eFmmIhkB9zRKyi` | `yj0LnzE4h98ciF52dkXHL` | 108,397 | 458 | 135 | 793 |
| Vajirabuddhi | `NhOl0hggpKU6eN4IHBTrv` | `rcGLzvX5UV75h8pEd42oR` | `moiBkUuN4r5uWuTZMwGVi` | 147,349 | 499 | 196 | 670 |
| Yojanā | `vsbm8MUFloI3jclNqO5r4` | `jUhyZBdaHqgtA49chJr7m` | `cFJ1PLAa9CtivQ3LI075l` | 262,065 | 761 | 237 | 751 |

**Read back from prod (2026-11-12), all six texts:**

- **Root record:** the root lists all five commentaries, with the category, tag and licence above.
- **Segments:** the same references in the same order as the file's blocks, and each segment's text is identical to its block. The root's segments are `verse`; every commentary segment is `paragraph` (the homage `T-1`, where the source prints one, is `top_segment`), as in the Abhidhamma uploads.
- **Table of contents:** one node per heading, with the same title and depth in the same order. Every span starts at the heading's first block and ends at the last block before the next heading of the same or a higher level.
- **Alignments:** the live pairs equal the parser output, and their root targets are exactly the file's transclusion targets. They run commentary → root only.
- **Titles:** identical to the files' `title:` lines.
- **Frontmatter:** the upload added only the IDs (`commentary_of`, `text_id`, `edition_id`, `toc_id`, `aligned_to_edition_id`).

---

## Things to know

- **The upload scripts' default host is not prod.** Set `WEBUDDHIST_API_BASE=https://library-prod.webuddhist.com`. Prod needs the API key even for reads; it is in the git-ignored `4-SYSTEM/scripts/.env`.
- **Use a Python with both PyYAML and root certificates.** `/usr/local/bin/python3.13` fails the HTTPS calls (`CERTIFICATE_VERIFY_FAILED`); the first root attempt stopped there before anything was created (recorded in the ledger). `/opt/homebrew/bin/python3.11` works.
- **The commentary linter rewrites `languages.py`.** It was restored to the vault's version after the dry runs.
- **Not looked at:** the WeBuddhist reader.

## Files

Committed together, as Abhidhamma pi-3 was:

- `pi-2.md` and the five commentary files, with their library IDs
- linter output: `4-SYSTEM/scripts/linter-root-text/output/pi-2.lint.json` and `4-SYSTEM/Skills/commentary-upload/scripts/linter-commentary/output/pi-pacittiya-*.lint.json`
- parser output: `4-SYSTEM/scripts/parser-root-text/output/pi-2/` (edition, text, toc) and `4-SYSTEM/Skills/commentary-upload/scripts/parser-commentary/output/pi-pacittiya-*/` (alignment, edition, text, toc) — exactly what is live
- the source data `0-INBOX/raw-data/vin02m1`, `vin02a1`, `vin02t`, `vin12t` `.json`
- the build fixes `build_tika_json.py` and `apply_site_toc.py`, the two upload ledgers, and this report

Not committed: books 3–5, the scratch folders `0-INBOX/raw-data/parts/` and `0-INBOX/temp/vinaya/`, the root upload's own output folders under `4-SYSTEM/Skills/translation-upload/scripts/`, the verification tools, and `.gitignore`. Never commit `.env`.

## Related

- pi-1 report: `0-INBOX/pi-1-hierarchy-and-upload-report.md`
- tipitaka-xml check of all 29 Vinaya files: `0-INBOX/vinaya-tipitaka-xml-audit.md`
- Model: the Abhidhamma vault's `0-INBOX/pi-3-hierarchy-and-upload-report.md` … `pi-7-hierarchy-and-upload-report.md`
