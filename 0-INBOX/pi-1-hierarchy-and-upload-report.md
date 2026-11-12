# Pārājikapāḷi (`pi-1`) — root text and commentaries: structure, content, and upload

**Date:** 2026-11-11  
**Texts:**

- Root: `1-SOURCES/Text/pi-1.md` (Pārājikapāḷi, Vinaya book 1)
- `1-SOURCES/Commentaries/pi-parajika-atthakatha.md` (Pārājikakaṇḍa-aṭṭhakathā)
- `1-SOURCES/Commentaries/pi-parajika-saratthadipani.md` (Sāratthadīpanī-ṭīkā)
- `1-SOURCES/Commentaries/pi-parajika-vimativinodani.md` (Vimativinodanī-ṭīkā)
- `1-SOURCES/Commentaries/pi-parajika-vajirabuddhi.md` (Vajirabuddhi-ṭīkā)

**Checked against three references:**

- **tipitaka.app:** `vp-prj` for the root, and `atta-vp-prj`, `tika-vp-prj`, `tika-vimativinodani-tika` and `tika-vajirabuddhi-tika` for the commentaries. The data was read through the `/api/children`, `/api/text` and `/api/links` endpoints and re-fetched today; it is identical to the saved copies in `0-INBOX/tipitaka-app/`.
- **[VipassanaTech/tipitaka-xml](https://github.com/VipassanaTech/tipitaka-xml):** `romn/` at commit `22c6232`: `vin01m.mul`, `vin01a.att`, `vin01t1/2.tik`, `vin07t.nrf`, `vin06t.nrf`.
- **The commentaries' own text:** their printed paragraph numbers, book headings and colophons.

The live WeBuddhist **prod** library (`https://library-prod.webuddhist.com`) was then read back and compared with the files.

This note is for someone opening the project cold. It records what was checked, what was fixed, what differs from the website on purpose, and what is in the library. **All five texts are uploaded to prod and committed** (`f85fb47`, on `main`, not pushed).

---

## Summary of changes

### What was fixed

| Issue | What was wrong | Fix | Example | Applied to |
|---|---|---|---|---|
| Shortened range citations not linked | CST prints some ranges with a shortened tail. The converter read `133-4.` as "133 down to 4" and silently made no link | kept as printed, linked to the full range, and recorded in each file's `source_note` | `133-4.` → `^1-133`, `^1-134`; `148-9.` → `^1-148`, `^1-149` | aṭṭhakathā 26, Sāratthadīpanī 4, Vimativinodanī 18, Vajirabuddhi 32 |
| Sāratthadīpanī volume break as a heading | the second volume's title was a `###` heading, which shifted the sibling positions of the four kaṇḍas after it. tipitaka.app joins the volumes with no heading | kept as a line of text | `Sāratthadīpanī-ṭīkā (dutiyo bhāgo) ^1-1365` | Sāratthadīpanī |
| Ṭīkā part boundary | when the whole-Vinaya Vimativinodanī (`vin07t`) was split per root book, the next volume's header (`Namo tassa…`, `Vinayapiṭake`) was left as the last lines of the Pārājika part | each part now ends where the site's next volume begins; no text was lost, and no other block ID changed | the file no longer ends `Namo tassa… / Vinayapiṭake` | Vimativinodanī |
| Aṭṭhakathā title | the title was `Samantapāsādikā (Pārājika)`, the name of the whole Vinaya commentary and not the title of this book | set to the book's own title, as tipitaka.app, tipitaka-xml and the colophon (`Pārājikakaṇḍa-aṭṭhakathā niṭṭhitā.`) give it. `finalize.py` now takes the aṭṭhakathā title from the source file | `Samantapāsādikā (Pārājika)` → `Pārājikakaṇḍa-aṭṭhakathā` | file frontmatter and prod text `lfmZoqj9eYuJrsOUTSM4Z` |
| Upload to the wrong host | the upload script's default host is `library.webuddhist.com`, not prod, and the first pi-1 upload went there | deleted there; uploaded again to prod | receipt in `upload_ledger.library.webuddhist.com.json` | pi-1 |
| Library category and tag missing | not set | `category_id: 4wuvGxIgXNZ5mb0bDWvkC` (Monastic Rules, འདུལ་བ།) and `tag_ids: [296WZOr8MXWteSqBBI7pl]` (Theravāda), as on the Abhidhamma texts | — | all five files |

The fixes are in `4-SYSTEM/Skills/json-to-commentary/scripts/converters/tipitaka_org_atthakatha.py`, `0-INBOX/raw-data/build_tika_json.py` and `0-INBOX/raw-data/finalize.py`. Every file was rebuilt with `build_all.sh` and then `finalize.py`.

### What was checked and left unchanged

| Item | Why nothing was changed |
|---|---|
| 27 spacing differences (`Athakho` on the site, `Atha kho` ours) | the XML has a real space between two bold runs (`<hi>Atha</hi> <hi>kho…`), which the site's display drops. Ours follows the source: root 1, aṭṭhakathā 23, Sāratthadīpanī 1, Vimativinodanī 1, Vajirabuddhi 0 |
| Bold | the site shows bold lemmas as `**…**`; the library stores plain text, so the files carry none |
| Ranges linked in full | the site links a range only by its first number; ours links every paragraph in it, as in the Abhidhamma vault |
| 25 Sāratthadīpanī paragraphs whose root links differ from the aṭṭhakathā paragraph the site joins them to | the two texts print different ranges for the same passage (e.g. aṭṭhakathā `43-44.`, ṭīkā `43.`). Each is linked as its own text prints it, and the ranges always overlap |
| The sixteen dreams in the Sāratthadīpanī (32 links to root 1–16) | linked as printed, as tipitaka.app also does. Recorded in `source_note` and left **for a reviewer** (below) |
| Three ṭīkā titles carry `(Pārājika)` | the Vimativinodanī and Vajirabuddhi are single works on all five books, and the library needs a unique title for each part. tipitaka.app titles the Sāratthadīpanī the same way, `Sāratthadīpanī-ṭīkā (Pārājika)` |

---

## What these files are

`pi-1.md` is the **root mūla** of the Pārājikapāḷi, the first book of the Vinayapiṭaka (CST `vin01m`). The four commentaries on it are:

- the **aṭṭhakathā**, the Pārājika part of the Samantapāsādikā (`vin01a`)
- three **ṭīkās**:
  - the Sāratthadīpanī (`vin01t1` + `vin01t2`, its two volumes)
  - the Pārājika part of the Vimativinodanī (`vin07t`)
  - the Pārājika part of the Vajirabuddhi (`vin06t`)

The Vinaya has no anuṭīkā. Each numbered commentary paragraph links to the root paragraphs it explains, and those links become the alignment in the library.

---

## How IDs work

| Track | Shape | Example | Meaning |
|---|---|---|---|
| Heading | ends in `-0` | `^1-2-1-0` | TOC node only; the ID is its path in the tree |
| Root content | book + printed paragraph number | `^1-133` | root paragraph 133 |
| Root content without a number | `U` | `^1-U3` | unnumbered root block (12) |
| Homage | `T-1` | `^T-1` | `Namo tassa bhagavato…` at the top of each file |
| Commentary content | running counter | `^1-1` … `^1-2538` | the Nth paragraph of that commentary file |
| Link to root | transclusion | `![[1-SOURCES/Text/pi-1.md#^1-133]]` | the root paragraph a commentary paragraph explains |

Unlike the Paṭṭhāna, the Pārājika root has one numbering run: paragraphs 1–662 run straight through the book, and the commentaries cite exactly these numbers.

---

## Root text (`pi-1.md`)

### Outline

```
# Vinayapiṭake                      ^0
## Pārājikapāḷi                     ^1-0
### Verañjakaṇḍaṃ                   ^1-1-0
### Pārājikakaṇḍaṃ                  ^1-2-0
#### Paṭhamapārājikaṃ … Catutthapārājikaṃ
##### Sudinnabhāṇavāro …
### Saṅghādisesakaṇḍaṃ              ^1-3-0
### Aniyatakaṇḍaṃ                   ^1-4-0
### Nissaggiyakaṇḍaṃ                ^1-5-0
```

- **80 headings** at levels `#` to `#####` (1 / 1 / 5 / 52 / 21), each with a `-0` anchor.
  - Every child ID extends its parent's, siblings run 1…n with no gaps, and no level is skipped.

### Body

- **675 content IDs:**
  - the homage `^T-1`
  - 12 unnumbered blocks, `^1-U1` … `^1-U12`
  - 662 numbered paragraphs, `^1-1` … `^1-662`, with no gaps or duplicates
- **1,722 continuation lines**: they have no ID of their own and belong to the block whose ID follows.

### Compared with tipitaka.app (`vp-prj`) and tipitaka-xml (`vin01m`)

- **Lines:** the site has **2,477 paragraphs**, and the file has the same total: 80 headings + 675 ID lines + 1,722 continuation lines. The XML matches it 1:1 as well.
- **Text:** every line is identical to the site and the XML, apart from the conventions above.
- **Paragraph numbers:** all **662 printed numbers** start their own `^1-N` block.
- **Tree:** the site's contents tree matches **78 of 78** headings below the title. Each has the same parent, position and number of children, and every heading ID is its tree path.

---

## Commentaries

### Outline

```
# Vinayapiṭake (aṭṭhakathā | ṭīkā)               ^0
## <work title>                                  ^1-0
### Ganthārambhakathā(vaṇṇanā), Bāhiranidānakathā(vaṇṇanā)
### Verañjakaṇḍavaṇṇanā
### Pārājikakaṇḍa(ṃ|o) · Saṅghādisesakaṇḍa · Aniyatakaṇḍa · Nissaggiyakaṇḍa
#### the sikkhāpadas …
##### / ###### their parts (vaṇṇanā, vinicchayakathā …)
```

| | Headings | Levels used (`#` … ) | Content IDs |
|---|---|---|---|
| aṭṭhakathā | 151 | 1 / 1 / 5 / 25 / 88 / 31 | `^T-1`, `^1-1` … `^1-2538` |
| Sāratthadīpanī | 153 | 1 / 1 / 8 / 44 / 99 | `^T-1`, `^1-1` … `^1-2784` |
| Vimativinodanī | 138 | 1 / 1 / 8 / 35 / 93 | `^T-1`, `^1-1` … `^1-1025` |
| Vajirabuddhi | 112 | 1 / 1 / 7 / 14 / 82 / 7 | `^T-1`, `^1-1` … `^1-724` |

- Each tree follows tipitaka.app's contents tree for that work, and differs between works where the works differ.
  - The aṭṭhakathā has `### Pārājikakaṇḍa-aṭṭhakathā (dutiyo bhāgo)` as a division, as the site does.
  - The Vajirabuddhi puts the saṅgīti chapters at `###`.
- No level is skipped. Every heading ID ends in `-0` and extends its parent's, and siblings run 1…n with no gaps.

### Compared with tipitaka.app and tipitaka-xml

| Layer | Site paragraphs | Lines identical to the site | Headings (parent, position, children) | XML |
|---|---|---|---|---|
| aṭṭhakathā | 2,974 | 2,974 of 2,974 | 149 of 149 | 1:1, no errors |
| Sāratthadīpanī | 3,319 | 3,319 of 3,319 | 151 of 151 | 1:1, no errors |
| Vimativinodanī | 1,179 (of the work's 3,136) | 1,179 of 1,179 | 136 of 136 | 1:1, no errors |
| Vajirabuddhi | 991 (of the work's 2,673) | 991 of 991 | 110 of 110 | 1:1, no errors |

"Identical" means after the conventions above. The only line that differs is the piṭaka label. The Vimativinodanī and Vajirabuddhi parts end exactly where the site's next book (Pācittiya) begins.

---

## Links to the root text (alignment)

Each numbered commentary paragraph has one `![[1-SOURCES/Text/pi-1.md#^1-N]]` line per root paragraph directly above it. A printed range becomes consecutive lines.

| | Linked paragraphs | Link lines | Distinct root targets | Alignment pairs (prod) | Commentary segments aligned |
|---|---|---|---|---|---|
| aṭṭhakathā | 367 | 410 | 410 | 2,305 | 2,040 of 2,539 |
| Sāratthadīpanī | 337 | 408 | 376 | 2,145 | 1,905 of 2,785 |
| Vimativinodanī | 279 | 330 | 329 | 888 | 778 of 1,026 |
| Vajirabuddhi | 206 | 248 | 247 | 697 | 561 of 725 |

The pairs follow the Abhidhamma vault's rule, used for its pi-1 … pi-7 uploads: a group of links aligns every commentary block after it **until the next group of links or the next heading**. Commentary under a heading that has no link of its own stays unaligned. (Changed 2026-11-12; see "Brought in line with the Abhidhamma uploads" below.)

**Checks:**

- **Against tipitaka-xml:** every numbered paragraph has exactly the links for its printed number, with ranges expanded, directly before it. Every target exists in `pi-1.md`, and there is no stray or misplaced link (0 errors).
- **Against tipitaka.app:**
  - **Aṭṭhakathā → root:** all **367** of the site's links are in our transclusions; 367 is also our number of linked aṭṭhakathā paragraphs.
  - **Ṭīkā → aṭṭhakathā:** for **303** of the site's 328 Sāratthadīpanī links, the ṭīkā and aṭṭhakathā paragraphs it joins link to the same root paragraphs. The other 25 are the printed-range differences above.
  - The site has no links for the Vimativinodanī or Vajirabuddhi.
- **Unresolved citations:** 0.
- **No backward jumps** apart from the two in the Sāratthadīpanī where the sixteen-dreams list restarts at 1.
- **No links between commentary layers.** As in the Abhidhamma vault, every commentary aligns only to the root.

---

## Titles

| Text | Ours (file = prod) | tipitaka.app | tipitaka-xml book heading | Colophon |
|---|---|---|---|---|
| Root | Pārājikapāḷi | Pārājikapāḷi | Pārājikapāḷi | Pārājikapāḷi niṭṭhitā. |
| aṭṭhakathā | Pārājikakaṇḍa-aṭṭhakathā | Pārājikakaṇḍa-aṭṭhakathā | Pārājikakaṇḍa-aṭṭhakathā (paṭhamo / dutiyo bhāgo) | Pārājikakaṇḍa-aṭṭhakathā niṭṭhitā. |
| Sāratthadīpanī | Sāratthadīpanī-ṭīkā (Pārājika) | Sāratthadīpanī-ṭīkā (Pārājika) | Sāratthadīpanī-ṭīkā (paṭhamo / dutiyo bhāgo) | … nāma vinayaṭīkā |
| Vimativinodanī | Vimativinodanī-ṭīkā (Pārājika) | Vimativinodanī-ṭīkā | Vimativinodanī-ṭīkā (paṭhamo bhāgo) | Vimativinodanīṭīkā niṭṭhitā. |
| Vajirabuddhi | Vajirabuddhi-ṭīkā (Pārājika) | Vajirabuddhi-ṭīkā | Vajirabuddhi-ṭīkā | Vajirabuddhiṭīkā niṭṭhitā. |

The volume label `(paṭhamo bhāgo)` is dropped because each file holds the whole Pārājika part. All five carry `category_id: 4wuvGxIgXNZ5mb0bDWvkC` and `tag_ids: [296WZOr8MXWteSqBBI7pl]`, with `license: cc0`.

---

## Library upload (prod)

Uploaded on 2026-11-11 to `https://library-prod.webuddhist.com`, with `root-text-upload` for the root and `commentary-upload` for the commentaries. Each commentary is a `commentary_of` the Pārājikapāḷi and aligned to its edition. The IDs are saved in each file's frontmatter and in the upload ledgers.

| | text_id | edition_id | toc_id | Characters | Segments | TOC nodes | Alignment pairs |
|---|---|---|---|---|---|---|---|
| Pārājikapāḷi | `NeySMirSFLEgeMNztyy7J` | `LOajhD42NZB0aoZx6eb3h` | `6c1NiwTHbBorpKNNNrODG` | 644,430 | 675 | 80 | — |
| aṭṭhakathā | `lfmZoqj9eYuJrsOUTSM4Z` | `G5Xf8XNTGD4j85Tm6OIIx` | `m6ykvvoTF1Yg8E0LYTPtd` | 1,175,920 | 2,539 | 151 | 2,305 |
| Sāratthadīpanī | `PcV57z4T2gqDv1ILRtdlE` | `Sn25vAbquEf1le6nDc5xk` | `MTj4DjWPJeozNS67yvive` | 1,655,243 | 2,785 | 153 | 2,145 |
| Vimativinodanī | `p2lM0D26XkcAZZB1PkeCP` | `9lWiR3WIQyOUIKw74nBhX` | `5qLTOIwtRTajzFH1UYw8n` | 656,711 | 1,026 | 138 | 888 |
| Vajirabuddhi | `URgLMpwpciSEK0p2jJwXF` | `FDVzp6dZeXBwYcEhN51bA` | `Q2SZgsWAnBdP8lX7Xk59y` | 523,159 | 725 | 112 | 697 |

**Read back from prod (2026-11-12, after the change below), all five texts:**

- **Root record:** the root text lists all four commentaries.
- **Segments:** the same references in the same order as the file's blocks, and each segment's text is identical to its block. The root's segments are `verse` and every commentary segment after the homage (`T-1`, `top_segment`) is `paragraph`, as in the Abhidhamma uploads.
- **Table of contents:** one node per heading, with the same title and depth in the same order. Every span starts at the heading's first block and ends at the last block before the next heading of the same or a higher level.
- **Alignments:** the live pairs are identical to the parser output. Their root targets are exactly the file's transclusion targets, and every target exists in the root.
- **Titles:** identical to the files' `title:` lines.

### Source form (2026-11-12)

The Vinaya files keep the body and structure of their own sources; only the Abhidhamma vault's *way of working* is followed, not its format. So, as tipitaka-xml prints them and tipitaka.app shows them:

- **printed numbers stay** on headings (`1. Pārājikakaṇḍaṃ`) and at the start of root paragraphs (`1. Tena samayena…`); the block ID still records the number;
- **the piṭaka heading is `Vinayapiṭake`**, as printed (it was `Vinayapiṭake (aṭṭhakathā)` / `(ṭīkā)`);
- **variant-reading notes are `{…}`**, as on the site (a `<note>` in the XML); brackets inside a note's own text stay;
- **no homage is added** where the source prints none.

The step is `4-SYSTEM/scripts/tipitaka-xml-to-json/source_form.py`, run last in `build_roots.sh` and `build_commentary.py`. Checked with `verify.py --strict` (nothing normalised: 0 text differences) and line by line against tipitaka.app (every line exactly equal, the site's own bold and page markers aside). Bold stays plain: the library stores plain text. No block ID, heading ID, link or alignment pair changed.

On prod (same day): the root editions' text, segmentation and contents tree were replaced and every commentary's alignment put back; the commentaries got new contents trees (titles with their printed numbers, `Vinayapiṭake`). Text and edition IDs are unchanged; the new contents-tree IDs are in the files, the ledgers and the table above. Read back: text, segments, contents trees and pairs equal the files.

### Brought in line with the Abhidhamma uploads (2026-11-12)

The Abhidhamma vault's pi-1 … pi-7 uploads are the reference. Compared with them, two things in the first pi-1 upload differed: the commentary parser in this vault let a group of links run on across headings, and it typed every block of several lines (a gāthā) as `verse`. Both rules now follow the Abhidhamma parser (`4-SYSTEM/Skills/commentary-upload/scripts/parser-commentary/`). On all nine Vinaya commentaries (pi-1 and pi-2), the three Dhammasaṅgaṇī commentaries and the Paṭṭhāna aṭṭhakathā, the parser's output is now identical to the Abhidhamma parser's. On the Dhammasaṅgaṇī it reproduces the live Abhidhamma pairs exactly (1,980 / 853 / 956). The Vinaya text, block IDs and contents trees did not change.

On prod, for each of the four commentaries:

1. the live segments, alignments and contents tree were backed up;
2. the segmentation was replaced (`DELETE` + `POST /v2/editions/{id}/segmentation`): same references and spans, 608 segments `verse` → `paragraph` (214 / 278 / 13 / 103);
3. the alignment was replaced (`PUT /v2/editions/{id}/alignments/{root edition}`): 2,468 / 2,388 / 954 / 748 → 2,305 / 2,145 / 888 / 697 pairs. Only the pairs that ran on across a heading were removed; none was added;
4. everything was read back: segments, types, content, contents tree and pairs equal the parser output.

The text, edition and contents IDs are unchanged. Each step is logged in `upload_ledger.json`.

The three ṭīkā files also gained `commentary: 1-SOURCES/Commentaries/pi-parajika-atthakatha.md`, as the Abhidhamma ṭīkā files name the commentary they explain. It is a vault note only; nothing sent to the library changes.

---

## Things to know

- **The upload script's default host is not prod.** Set `WEBUDDHIST_API_BASE=https://library-prod.webuddhist.com` before uploading. Prod needs the API key even for reads.
- **The API key** is in `4-SYSTEM/scripts/.env` (`WEBUDDHIST_API_KEY`). It is git-ignored; never commit it.
- **The linter rewrites a tracked file.** Running the commentary linter rewrites `4-SYSTEM/Skills/commentary-upload/scripts/linter-commentary/languages.py`; restore it with `git checkout`. As in the Abhidhamma vault, the linter and parser output that was uploaded is committed (see Files).
- **Changing a title on prod** only needs a PATCH to `/v2/texts/{text_id}` (`{"title": {"pi": "…"}}`). It does not touch the edition, TOC or alignment.
- **Not looked at:** the WeBuddhist reader. Open the texts there to see the TOC and the commentary panel.

## For a reviewer to decide

**The sixteen dreams in the Sāratthadīpanī.** After the citation `236-237.` in the Saṅghādisesakaṇḍa, the ṭīkā retells King Kosala's sixteen dreams, numbering the dreams 1–16 and then their meanings 1–16.

- CST marks these as paragraph numbers, so they are linked to root paragraphs 1–16 of the Verañjakaṇḍa: 32 links that are list numbers, not citations.
- tipitaka.app links them the same way.
- They are linked as printed, following the Abhidhamma practice, and recorded in `source_note`.

Should they be dropped? Dropping them would mean re-uploading the Sāratthadīpanī alignment.

## Files

Committed in `f85fb47` (first upload) and `be85fd7` (this report):

- `pi-1.md` and the four commentary files
- the two upload ledgers and the wrong-host receipt
- `0-INBOX/raw-data/finalize.py`

Committed with the 2026-11-12 change, as Abhidhamma pi-3 was:

- the three ṭīkā files (`commentary:` line)
- linter output: `4-SYSTEM/scripts/linter-root-text/output/pi-1.lint.json` and `4-SYSTEM/Skills/commentary-upload/scripts/linter-commentary/output/pi-parajika-*.lint.json`
- parser output: `4-SYSTEM/scripts/parser-root-text/output/pi-1/` (edition, text, toc) and `4-SYSTEM/Skills/commentary-upload/scripts/parser-commentary/output/pi-parajika-*/` (alignment, edition, text, toc) — exactly what is live
- the parser rule change (`parser.py`, its `README.md`, the skill's `SKILL.md`), `finalize.py`, the upload ledger and this report

Not committed:

- books 2–5 (`pi-2` … `pi-5` and their commentaries)
- the tipitaka-xml checker and its audit
- `compare_md_site.py` and `.gitignore`

Never commit `.env`.

## Related

- Earlier pi-1 audit: `0-INBOX/pi-1-commentary-audit.md`
- tipitaka-xml check of all 29 Vinaya files: `0-INBOX/vinaya-tipitaka-xml-audit.md` and `0-INBOX/tipitaka-xml-check/verify.py`
- Site comparisons: `0-INBOX/tipitaka-app/compare_tree.py`, `compare_md_site.py`
- Model for this report: the Abhidhamma vault's `0-INBOX/pi-7-hierarchy-and-upload-report.md`
