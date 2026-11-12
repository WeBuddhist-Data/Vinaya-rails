# Mahāvaggapāḷi (`pi-3`) — root text and commentaries: structure, content, and upload

**Date:** 2026-11-12  
**Texts:**

- Root: `1-SOURCES/Text/pi-3.md` (Mahāvaggapāḷi, Vinaya book 3)
- `1-SOURCES/Commentaries/pi-mahavagga-atthakatha.md` (Mahāvagga-aṭṭhakathā)
- `1-SOURCES/Commentaries/pi-mahavagga-saratthadipani.md` (Sāratthadīpanī-ṭīkā)
- `1-SOURCES/Commentaries/pi-mahavagga-vimativinodani.md` (Vimativinodanī-ṭīkā)
- `1-SOURCES/Commentaries/pi-mahavagga-vajirabuddhi.md` (Vajirabuddhi-ṭīkā)
- `1-SOURCES/Commentaries/pi-mahavagga-yojana.md` (Pācityādiyojanā)

**Checked against three references:**

- **tipitaka.app:** `vp-mv` for the root, and `atta-vp-mv`, `tika-vp-pct`, `tika-vimativinodani-tika`, `tika-vajirabuddhi-tika` and `tika-pacityadiyojanapali` for the commentaries, downloaded 2026-11-12.
- **[VipassanaTech/tipitaka-xml](https://github.com/VipassanaTech/tipitaka-xml):** `romn/` at `c65aa30`: `vin02m2.mul`, `vin02a2.att`, `vin02t.tik`, `vin07t.nrf`, `vin06t.nrf`, `vin12t.nrf`.
- **The commentaries' own text:** their printed paragraph numbers, book headings and closing lines.

**How it was built:** the body and structure follow the Vinaya's own sources, in the printed form the repo has and the site shows. From the Abhidhamma vault only the *way of working* is taken (check, build, dry run, upload root then commentaries, read back, report), and its alignment and segment-type rules.

**All six texts are uploaded to prod** (`https://library-prod.webuddhist.com`) and read back.

---

## Built in the source form

All six files were rebuilt on 2026-11-12 with the current build, and the source form is its last step (`4-SYSTEM/scripts/tipitaka-xml-to-json/source_form.py`):

- **Printed numbers stay:**
  - on headings: 290 in the root (`1. Mahākhandhako`), 10 in each ṭīkā, 145 in the Yojanā;
  - at the start of the 477 root paragraphs (`1. Tena samayena…`).
  
  The block ID still records the number.
- **The piṭaka heading is printed `Vinayapiṭake`.**
- **Variant-reading notes are `{…}`**, as on the site (424 in the root). Brackets inside a note's own text stay.
- **One bracket in the source is not a note:** a lone `[` that the XML never closes ("…āgatā} [ Evaṃ vutte bhagavā…"). It stays as printed. The build step now leaves a bracket that is not closed on its line as printed; pi-1 and pi-2 come out unchanged with it.
- **Each ṭīkā names the commentary it explains:** `commentary: 1-SOURCES/Commentaries/pi-mahavagga-atthakatha.md`.

Against the files before the rebuild: every block ID and all 1,283 links are unchanged. Every source word is present in order (fidelity check: root 102,214 words; commentaries 38,544 / 41,356 / 21,183 / 20,587 / 37,118).

### What was checked and left unchanged

| Item | Why nothing was changed |
|---|---|
| Vimativinodanī `15.` | CST misprint for 25 (the lemmas *āḷambara*, *vikesika* are in root `3-25`, Yasa's story). Linked as printed, to `3-15`, and recorded in `source_note` |
| Each ṭīkā part's top `# Vinayapiṭake` | the XML prints it once, at the start of each work. Every file needs one top heading as the root of its contents tree. Every other heading, and each part's homage, is printed in the XML at that point |
| Ranges linked in full | the site links a range by its first number only; ours links every paragraph in it (aṭṭhakathā 9, Vimativinodanī 14, Vajirabuddhi 13, Yojanā 1 truncated-tail ranges such as `44-9.` = 44–49, recorded in `source_note`) |
| Bold | the site shows bold lemmas; the library stores plain text, so the files carry none |

---

## Root text (`pi-3.md`)

- **294 headings**, levels `#` to `#####` (1 / 1 / 10 / 280 / 2): the ten khandhakas, from `1. Mahākhandhako` to `10. Kosambakakkhandhako`, and their sections. No level is skipped, every child ID extends its parent's, siblings run 1…n, and every heading has text under it.
- **491 content IDs:**
  - the homage `^T-1`;
  - 13 unnumbered blocks `^3-U…`;
  - 477 numbered paragraphs `^3-1` … `^3-477`.
- **1,972 continuation lines.**
- **Against tipitaka-xml (strict):**
  - 2,757 lines, 0 text differences;
  - 294 of 294 headings;
  - every one of the 477 printed numbers starts its own block.
- **Against tipitaka.app:** all 2,757 lines exactly equal; 292 of 292 headings below the title in the site's tree, with 0 differences in parent, position, children or ID path.

---

## Commentaries

| | Headings | Levels (`#` … ) | Content IDs | Lines = tipitaka.app | Tree vs tipitaka.app | tipitaka-xml (strict) |
|---|---|---|---|---|---|---|
| aṭṭhakathā | 141 | 1 / 1 / 10 / 129 | `^T-1`, `^3-1` … `^3-757` | 922 of 922 | 139 of 139 | 0 differences |
| Sāratthadīpanī | 145 | 1 / 1 / 10 / 133 | `^T-1`, `^3-1` … `^3-766` | 1,037 of 1,037 | 143 of 143 | 0 differences |
| Vimativinodanī | 105 | 1 / 1 / 10 / 93 | `^T-1`, `^3-1` … `^3-544` | 652 of 652 | 103 of 103 | 0 differences |
| Vajirabuddhi | 114 | 1 / 1 / 10 / 102 | `^T-1`, `^3-1` … `^3-325` | 510 of 510 | 112 of 112 | 0 differences |
| Yojanā | 152 | 1 / 1 / 10 / 135 / 5 | `^T-1`, `^3-1` … `^3-690` | 846 of 846 | 150 of 150 | 0 differences |

No duplicate IDs, no skipped levels, every ID is its tree path, every heading has text under it.

---

## Links to the root text (alignment)

| | Linked paragraphs | Link lines | Distinct root targets | Alignment pairs (prod) | Commentary segments aligned |
|---|---|---|---|---|---|
| aṭṭhakathā | 275 | 303 | 303 | 799 | 748 of 758 |
| Sāratthadīpanī | 210 | 251 | 251 | 852 | 762 of 767 |
| Vimativinodanī | 212 | 252 | 251 | 667 | 539 of 545 |
| Vajirabuddhi | 170 | 191 | 191 | 347 | 319 of 326 |
| Yojanā | 272 | 286 | 285 | 707 | 680 of 691 |

The pairs follow the Abhidhamma rule: a group of links aligns every commentary block after it until the next group of links or the next heading.

**Checks:**

- **tipitaka-xml:** every numbered paragraph has exactly the links for its printed number, with ranges expanded, directly before it; every target exists in `pi-3.md` (0 errors).
- **tipitaka.app:** all **275** of the site's aṭṭhakathā → root paragraph links are in our transclusions. For the Mahāvagga, the site has no paragraph-number links from the aṭṭhakathā to the ṭīkās (only word-level gloss links), so there is nothing further to compare.
- **Sections:** all 1,283 links land in the khandhaka the commentary paragraph sits in. The Sāratthadīpanī spells the fourth `Pavāraṇakkhandhaka`, the root `Pavāraṇākkhandhako`; it is the same khandhaka.
- **Layers agree:** every ṭīkā link shares a root paragraph with the aṭṭhakathā or falls in a section the aṭṭhakathā also covers, except 8. Each of those 8 quotes a word that is in the root paragraph it links to:
  - Sāratthadīpanī `288.` *yānassa bhūmi*, `312.` *samādāya*, `378.` *matakacīvara*, `465.` *bālakaloṇakāragāma*, `466.` *pācīnavaṃsadāya*;
  - Vimativinodanī `131.` *vinayamhi*, `466.` *attakāmarūpā*;
  - Vajirabuddhi `146.` *samugghāta*.
- **Meaning:** at least half the quoted (bold) words of a paragraph occur in the root passage it links to (for the ṭīkās, the aṭṭhakathā on the same root paragraphs counts too) in the share of paragraphs below. The rest name other works or teachers (*Visuddhimagga*, *mātikāṭṭhakathā*, *gaṇṭhipada*), give a story's title ("Rādhabrāhmaṇavatthu"), or quote a stock formula from the suttas.

  | aṭṭhakathā | Sāratthadīpanī | Vimativinodanī | Vajirabuddhi | Yojanā |
  |---|---|---|---|---|
  | 266 of 268 | 200 of 205 | 209 of 210 | 143 of 154 | 262 of 264 |
- **No links between commentary layers.**

---

## Titles

| Text | Ours (file = prod) | tipitaka.app | `##` book heading | Last line |
|---|---|---|---|---|
| Root | Mahāvaggapāḷi | Mahāvaggapāḷi | Mahāvaggapāḷi | Mahāvaggapāḷi niṭṭhitā. |
| aṭṭhakathā | Mahāvagga-aṭṭhakathā | Mahāvagga-aṭṭhakathā | Mahāvagga-aṭṭhakathā | Mahāvagga-aṭṭhakathā niṭṭhitā. |
| Sāratthadīpanī | Sāratthadīpanī-ṭīkā (Mahāvagga) | Sāratthadīpanī-ṭīkā (Pācittiyādi) | Mahāvagga-ṭīkā | Mahāvaggavaṇṇanā niṭṭhitā. |
| Vimativinodanī | Vimativinodanī-ṭīkā (Mahāvagga) | Vimativinodanī-ṭīkā | Mahāvaggavaṇṇanā | Mahāvaggavaṇṇanānayo niṭṭhito. |
| Vajirabuddhi | Vajirabuddhi-ṭīkā (Mahāvagga) | Vajirabuddhi-ṭīkā | Mahāvaggavaṇṇanā | Mahāvaggassa līnatthapakāsanā niṭṭhitā. |
| Yojanā | Pācityādiyojanā (Mahāvagga) | Pācityādiyojanāpāḷi | Mahāvaggayojanā | Mahāvaggakhandhakassa, samatto yojanānayoti. |

The ṭīkā and Yojanā titles add the part, "(Mahāvagga)", by the same rule as pi-1 and pi-2: each is one part of a work that spans several books, and the library needs a unique title for it. All six carry `category_id: 4wuvGxIgXNZ5mb0bDWvkC`, `tag_ids: [296WZOr8MXWteSqBBI7pl]` and `license: cc0`.

---

## Library upload (prod)

Uploaded on 2026-11-12 to `https://library-prod.webuddhist.com`: `root-text-upload` for the root, then `commentary-upload` once per commentary. Each commentary followed a dry run whose segment, contents-tree and pair counts matched the ones agreed beforehand. Each commentary is a `commentary_of` the Mahāvaggapāḷi and aligned to its edition.

| | text_id | edition_id | toc_id | Characters | Segments | TOC nodes | Alignment pairs |
|---|---|---|---|---|---|---|---|
| Mahāvaggapāḷi | `UuDkWSmWOL5PESPmgILv6` | `VVPfVPNWsbjPzk3bMocKP` | `3xPDH8mIs5yt969isbaNB` | 905,627 | 491 | 294 | — |
| aṭṭhakathā | `sB4W6zmMtsYGeWdX0fYgj` | `Xq9kTf5x3VksG44HNonAP` | `EOBIi8UcS1FAAF3nwqfE9` | 346,395 | 758 | 141 | 799 |
| Sāratthadīpanī | `r044xwsKCdvWjgbJyJb0h` | `MTQ3EE81YEH9aEcDYNS1N` | `JevcqrL6V236B0siaPqO9` | 396,727 | 767 | 145 | 852 |
| Vimativinodanī | `BlavXdDozOQTQtORNfZKu` | `k1D5JciSEUihRFJHk74dI` | `Jzw90MuM0lmzOGfk9SAcd` | 207,874 | 545 | 105 | 667 |
| Vajirabuddhi | `Pyri5OTh9Q241BlCKUCMq` | `N4uslAtsG71RM8zF9eOxG` | `gVBvwWbNRiDmPyYa0FHpH` | 193,666 | 326 | 114 | 347 |
| Yojanā | `wZROjY39redLF5pkCRgy5` | `Lfb6tMuOj5AJnYbMptDBv` | `9KC7V3xz6Qi8cHVmJIBVV` | 348,378 | 691 | 152 | 707 |

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
- **The commentary linter rewrites `languages.py`.** It was restored to the vault's version after the dry runs.
- **Not looked at:** the WeBuddhist reader.

## Files

Committed together, after the upload:

- `pi-3.md` and the five commentary files, with their library IDs
- linter output: `4-SYSTEM/scripts/linter-root-text/output/pi-3.lint.json` and `4-SYSTEM/Skills/commentary-upload/scripts/linter-commentary/output/pi-mahavagga-*.lint.json`
- parser output: `4-SYSTEM/scripts/parser-root-text/output/pi-3/` (edition, text, toc) and `4-SYSTEM/Skills/commentary-upload/scripts/parser-commentary/output/pi-mahavagga-*/` (alignment, edition, text, toc)
- the source data `0-INBOX/raw-data/vin02m2.json` and `vin02a2.json`
- the build fixes `source_form.py` (a bracket not closed on its line stays as printed) and `fidelity_check.py` (braces count as punctuation)
- the two upload ledgers and this report

## Related

- pi-1 and pi-2 reports: `0-INBOX/pi-1-hierarchy-and-upload-report.md`, `0-INBOX/pi-2-hierarchy-and-upload-report.md`
- tipitaka-xml check of all Vinaya files: `0-INBOX/vinaya-tipitaka-xml-audit.md`
