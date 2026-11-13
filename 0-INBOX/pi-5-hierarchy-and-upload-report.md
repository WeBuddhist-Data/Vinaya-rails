# Parivārapāḷi (`pi-5`) — root text and commentaries: structure, content, and upload

**Date:** 2026-11-13  
**Texts:**

- Root: `1-SOURCES/Text/pi-5.md` (Parivārapāḷi, Vinaya book 5)
- `1-SOURCES/Commentaries/pi-parivara-atthakatha.md` (Parivāra-aṭṭhakathā)
- `1-SOURCES/Commentaries/pi-parivara-saratthadipani.md` (Sāratthadīpanī-ṭīkā)
- `1-SOURCES/Commentaries/pi-parivara-vimativinodani.md` (Vimativinodanī-ṭīkā)
- `1-SOURCES/Commentaries/pi-parivara-vajirabuddhi.md` (Vajirabuddhi-ṭīkā)
- `1-SOURCES/Commentaries/pi-parivara-yojana.md` (Pācityādiyojanā)

**Checked against three references:**

- **tipitaka.app:** `vp-pv` for the root, and `atta-vp-pv`, `tika-vp-pct`, `tika-vimativinodani-tika`, `tika-vajirabuddhi-tika` and `tika-pacityadiyojanapali` for the commentaries, downloaded 2026-11-12. Their contents trees are identical to the ones the build used.
- **[VipassanaTech/tipitaka-xml](https://github.com/VipassanaTech/tipitaka-xml):** `romn/` at `c65aa30` (no `romn/` changes on `main` since): `vin02m4.mul`, `vin02a4.att`, `vin02t.tik`, `vin07t.nrf`, `vin06t.nrf`, `vin12t.nrf`.
- **The commentaries' own text:** their printed paragraph numbers, book headings and closing lines.

**How it was built:** the body and structure follow the Vinaya's own sources, in the printed form the repo has and the site shows. From the Abhidhamma vault only the *way of working* is taken (check, build, dry run, upload root then commentaries, read back, report), and its alignment and segment-type rules.

**All six texts are uploaded to prod** (`https://library-prod.webuddhist.com`) and read back.

---

## Built in the source form

All six files were rebuilt on 2026-11-12 with the current build (they had been drafted on 2026-11-11 in the older form), and the source form is its last step (`4-SYSTEM/scripts/tipitaka-xml-to-json/source_form.py`):

- **Printed numbers stay:**
  - on headings: 227 in the root (`1. Katthapaññattivāro`); the commentaries print none on their Parivāra headings;
  - at the start of the 501 root paragraphs (`1. Yaṃ tena bhagavatā…`).

  The block ID still records the number.
- **The piṭaka heading is printed `Vinayapiṭake`.**
- **Variant-reading notes are `{…}`**, as on the site (207 in the root). The root has no bracket that is not a note, and no heading carries a note.
- **Each ṭīkā names the commentary it explains:** `commentary: 1-SOURCES/Commentaries/pi-parivara-atthakatha.md`.

Every source word is present in order (fidelity check: root 63,281 words; commentaries 22,132 / 6,265 / 6,765 / 6,155 / 16,990). Against the drafts, every paragraph ID and every link is unchanged.

### The book's opening line `1. Bhikkhuvibhaṅgo`

The XML prints `<head rend="title">1. Bhikkhuvibhaṅgo</head>` right after the book title, before the first chapter. The site shows it as a title-style line in the book's own opening text (paragraph role `title`, in the `vp-pv` book node), **not** as a node of its contents tree: the tree, and all five commentaries, begin the Parivāra at `Soḷasamahāvāro`. As a heading it moved every top-level division one place down against the site (19 differences).

It is therefore kept, word for word, as a text line under `## Parivārapāḷi` (`^5-U1`), the same treatment as pi-4's Dutiyanavakaṃ note. The two unnumbered verse blocks after it became `^5-U2` and `^5-U3`; nothing links to them or to any heading ID. The rule is in `apply_site_toc.py` (a title printed before the site tree's first node, and not in the tree, is part of the book's opening); pi-1 to pi-4 rebuilt with it are identical to their committed files.

### What was checked and left unchanged

| Item | Why nothing was changed |
|---|---|
| 11 root headings with no text of their own (`4. Nissaggiyakaṇḍaṃ` followed by `1. Kathinavaggo`, …), Vimativinodanī 3, Yojanā 1 | the site's tree has them empty at the same places, with their vaggas as siblings |
| Each ṭīkā part's top `# Vinayapiṭake` | the XML prints it once, at the start of each work. Every file needs one top heading as the root of its contents tree |
| Ranges linked in full | the site links a range by its first number only; ours links every paragraph in it (aṭṭhakathā 1, Sāratthadīpanī 1, Vimativinodanī 2, Vajirabuddhi 10, Yojanā 6 truncated-tail ranges such as `406-7.` = 406–407, recorded in `source_note`) |
| The aṭṭhakathā's last line `Vinaya-aṭṭhakathā niṭṭhitā.` | the Parivāra-aṭṭhakathā closes the whole Vinaya aṭṭhakathā; the source and the site print it so |
| Bold | the site shows bold lemmas; the library stores plain text, so the files carry none |

---

## Root text (`pi-5.md`)

- **255 headings**, levels `#` to `#####` (1 / 1 / 19 / 116 / 118): the nineteen divisions, from `Soḷasamahāvāro` to `Pañcavaggo`, and their sections. No level is skipped, every child ID extends its parent's, siblings run 1…n.
- **505 content IDs:**
  - the homage `^T-1`;
  - 3 unnumbered blocks `^5-U1` (the opening line) and `^5-U2`, `^5-U3` (verses);
  - 501 numbered paragraphs `^5-1` … `^5-501`, none missing.
- **2,851 continuation lines.**
- **Against tipitaka-xml (strict):**
  - 3,611 lines, 0 text differences;
  - 255 of 256 headings, the 256th being the opening line above;
  - every one of the 501 printed numbers starts its own block.
- **Against tipitaka.app:** all 3,611 lines exactly equal; 253 of 253 headings below the title in the site's tree, with 0 differences in parent, position, children or ID path.

---

## Commentaries

| | Headings | Levels (`#` … ) | Content IDs | Lines = tipitaka.app | Tree vs tipitaka.app | tipitaka-xml (strict) |
|---|---|---|---|---|---|---|
| aṭṭhakathā | 87 | 1 / 1 / 18 / 67 | `^T-1`, `^5-1` … `^5-533` | 661 of 661 | 85 of 85 | 0 differences |
| Sāratthadīpanī | 64 | 1 / 1 / 15 / 36 / 11 | `^T-1`, `^5-1` … `^5-173` | 250 of 250 | 62 of 62 | 0 differences |
| Vimativinodanī | 66 | 1 / 1 / 18 / 45 / 1 | `^T-1`, `^5-1` … `^5-273` | 348 of 348 | 64 of 64 | 0 differences |
| Vajirabuddhi | 78 | 1 / 1 / 17 / 59 | `^T-1`, `^5-1` … `^5-144` | 248 of 248 | 76 of 76 | 0 differences |
| Yojanā | 88 | 1 / 1 / 1 / 18 / 67 | `^T-1`, `^5-1` … `^5-474` | 571 of 571 | 86 of 86 | 0 differences |

No duplicate IDs, no skipped levels, every ID is its tree path.

---

## Links to the root text (alignment)

| | Linked paragraphs | Link lines | Distinct root targets | Alignment pairs (prod) | Commentary segments aligned |
|---|---|---|---|---|---|
| aṭṭhakathā | 114 | 125 | 125 | 560 | 503 of 534 |
| Sāratthadīpanī | 74 | 80 | 80 | 163 | 153 of 174 |
| Vimativinodanī | 97 | 113 | 113 | 281 | 258 of 274 |
| Vajirabuddhi | 94 | 106 | 105 | 150 | 133 of 145 |
| Yojanā | 109 | 120 | 120 | 487 | 437 of 475 |

The pairs follow the Abhidhamma rule: a group of links aligns every commentary block after it until the next group of links or the next heading.

**Checks:**

- **tipitaka-xml:** every numbered paragraph has exactly the links for its printed number, with ranges expanded, directly before it; every target exists in `pi-5.md` (0 errors).
- **tipitaka.app:** all **114** of the site's aṭṭhakathā → root paragraph links are in our transclusions. The site has no paragraph-number links from the aṭṭhakathā to the ṭīkās for the Parivāra.
- **Order and sections:** in all five, the 544 links run in root order. Each commentary division's links fall in the matching root division. The names differ (`Samuṭṭhānasīsavaṇṇanā` for `Samuṭṭhānasīsasaṅkhepo`; the aṭṭhakathā's `Dutiyagāthāsaṅgaṇikaṃ` and `Aparadutiyagāthāsaṅgaṇikaṃ` for the root's `Aparagāthāsaṅgaṇikaṃ` and `Dutiyagāthāsaṅgaṇikaṃ`), one heading can cover two root divisions (`Saṅgāmadvayavaṇṇanā` for `Cūḷasaṅgāmo` and `Mahāsaṅgāmo`), and a ṭīkā without a heading of its own for a root division carries on under the one before; the ṭīkās have `Samathabhedaṃ` at the top level where the root has it inside `Antarapeyyālaṃ`. Each follows its own site tree.
- **Layers:** 65 ṭīkā links share no root paragraph or section with the aṭṭhakathā (Sāratthadīpanī 16, Vimativinodanī 24, Vajirabuddhi 25, Yojanā 0) — mostly the Samathabheda paragraphs 293–319 and the Samuṭṭhāna and paccaya chapters, which the aṭṭhakathā does not take paragraph by paragraph. Their quoted words are in the root paragraphs they link to (counted in the meaning check below).
- **Meaning:** at least half the quoted (bold) words of a paragraph occur in the root passage it links to (for the ṭīkās, the aṭṭhakathā on the same root paragraphs counts too) in the share of paragraphs below.

  | aṭṭhakathā | Sāratthadīpanī | Vimativinodanī | Vajirabuddhi | Yojanā |
  |---|---|---|---|---|
  | 107 of 110 | 72 of 73 | 92 of 94 | 80 of 82 | 104 of 106 |

  The rest were read against the whole root paragraph and are linked right. They give the root's word in another form (aṭṭhakathā `379.` *bahujanaahitāya* for *bahujanāhitāya*, `454.` *na sākacchātabbo* for *na sākacchitabbo*; Vajirabuddhi `419.` *kāyikaupaghātikā* for *kāyikena upaghātikena*; Yojanā `481.` *hotichejja* for *hoti chejjaṃ*), point to the verse itself (aṭṭhakathā `367.` *paṭhamagāthā*, for *anuyogavattaṃ nisāmaya*), or name another work (`332.` *gaṇṭhipadesu*, *pavāraṇagāthā*, *pavāraṇakathā* on the root's *pavāraṇākammassa*).
- **No links between commentary layers.**

---

## Titles

| Text | Ours (file = prod) | tipitaka.app | `##` book heading | Last line |
|---|---|---|---|---|
| Root | Parivārapāḷi | Parivārapāḷi | Parivārapāḷi | Parivārapāḷi niṭṭhitā. |
| aṭṭhakathā | Parivāra-aṭṭhakathā | Parivāra-aṭṭhakathā | Parivāra-aṭṭhakathā | Vinaya-aṭṭhakathā niṭṭhitā. |
| Sāratthadīpanī | Sāratthadīpanī-ṭīkā (Parivāra) | Sāratthadīpanī-ṭīkā (Pācittiyādi) | Parivāra-ṭīkā | Sāratthadīpanī nāma vinayaṭīkā niṭṭhitā. |
| Vimativinodanī | Vimativinodanī-ṭīkā (Parivāra) | Vimativinodanī-ṭīkā | Parivāravaṇṇanā | Vimativinodanīṭīkā niṭṭhitā. |
| Vajirabuddhi | Vajirabuddhi-ṭīkā (Parivāra) | Vajirabuddhi-ṭīkā | Parivāravaṇṇanā | Vajirabuddhiṭīkā niṭṭhitā. |
| Yojanā | Pācityādiyojanā (Parivāra) | Pācityādiyojanāpāḷi | Pācityādiyojanā | Pācityādivaṇṇanāya yojanā samattā. |

The ṭīkā and Yojanā titles add the part, "(Parivāra)", by the same rule as pi-1 to pi-4: each is one part of a work that spans several books, and the library needs a unique title for it. All six carry `category_id: 4wuvGxIgXNZ5mb0bDWvkC`, `tag_ids: [296WZOr8MXWteSqBBI7pl]` and `license: cc0`, as pi-1 to pi-4 do.

---

## Library upload (prod)

Uploaded on 2026-11-13 to `https://library-prod.webuddhist.com`: `root-text-upload` for the root, then `commentary-upload` once per commentary. Each commentary followed a dry run whose characters, segment, contents-tree and pair counts matched the ones checked beforehand. Each commentary is a `commentary_of` the Parivārapāḷi and aligned to its edition.

| | text_id | edition_id | toc_id | Characters | Segments | TOC nodes | Alignment pairs |
|---|---|---|---|---|---|---|---|
| Parivārapāḷi | `FO8DQdu0kqajKngcQD10L` | `6za9aG69dlALeYGkIXKGH` | `eZW3SqS77wrhUj4EbXydd` | 604,403 | 505 | 255 | — |
| aṭṭhakathā | `pdNw4d78h6Br8H6HcigBr` | `c9SFEhNIF5nZeeJwWRYRj` | `zFniku2ihFap2KOrUdum8` | 210,992 | 534 | 87 | 560 |
| Sāratthadīpanī | `12dSaFsfBvzJNcXmqsixl` | `9C75QQABofkXHPTbORiy7` | `prsQSUT3k0QSpf9nD1Y4p` | 60,735 | 174 | 64 | 163 |
| Vimativinodanī | `VARkwbEaVaVbli3MCjXLu` | `33oZI6xY75ws4ufJEERsp` | `C4zRSnmK0kTTSYIHvnkSU` | 69,874 | 274 | 66 | 281 |
| Vajirabuddhi | `xc7s4FU2jIMKe6Ev9ZNoF` | `2hcjun3jxrlj54y7ZQ6Vi` | `xnHLKIE1nbVvmfI3w4kpz` | 59,893 | 145 | 78 | 150 |
| Yojanā | `DOGpiAHLksHx5mEG1t9Fs` | `WX987dZ07SNUEOAyg6Bgo` | `z680B7mLle2d9PGltHYEV` | 162,471 | 475 | 88 | 487 |

**Read back from prod (2026-11-13), all six texts:**

- **Root record:** the root lists all five commentaries, with the category, tag and licence above.
- **Segments:** the same references in the same order as the file's blocks, and each segment's text is identical to its block. The root's are `verse`; every commentary segment is `paragraph`, the homage `T-1` `top_segment`.
- **Table of contents:** one node per heading, with the same title and depth in the same order, and every span right.
- **Alignments:** the live pairs equal the parser output, and their root targets are exactly the file's transclusion targets. They run commentary → root only.
- **Frontmatter:** the upload added only the IDs (`commentary_of`, `text_id`, `edition_id`, `toc_id`, `aligned_to_edition_id`).

The committed linter and parser output was regenerated from the final files and equals what was uploaded. The commentary linter and parser output is identical to the Abhidhamma parser's.

---

## Things to know

- **The upload scripts' default host is not prod.** Set `WEBUDDHIST_API_BASE=https://library-prod.webuddhist.com`. Prod needs the API key even for reads; it is in the git-ignored `4-SYSTEM/scripts/.env`.
- **Use `/opt/homebrew/bin/python3.11`.** It has both PyYAML and root certificates; `/usr/local/bin/python3.13` fails the HTTPS calls.
- **The linters rewrite `languages.py`.** Both were restored to the vault's version after the runs.
- **Not looked at:** the WeBuddhist reader.

## Files

Committed in three batches, after the upload:

1. the root: `pi-5.md` with its library IDs, `0-INBOX/raw-data/vin02m4.json`, `4-SYSTEM/scripts/linter-root-text/output/pi-5.lint.json`, `4-SYSTEM/scripts/parser-root-text/output/pi-5/` (edition, text, toc), the root upload ledger, and the build step `apply_site_toc.py` (the book's opening line);
2. the aṭṭhakathā, Sāratthadīpanī and Vimativinodanī with their IDs, their linter output (`4-SYSTEM/Skills/commentary-upload/scripts/linter-commentary/output/`) and parser output (`…/parser-commentary/output/pi-parivara-*/`: alignment, edition, text, toc), `0-INBOX/raw-data/vin02a4.json`, and the commentary ledger with their entries;
3. the Vajirabuddhi and Yojanā the same way, the full commentary ledger, and this report.

## Related

- pi-1 to pi-4 reports: `0-INBOX/pi-1-hierarchy-and-upload-report.md` … `0-INBOX/pi-4-hierarchy-and-upload-report.md`
- tipitaka-xml check of all Vinaya files: `0-INBOX/vinaya-tipitaka-xml-audit.md`
