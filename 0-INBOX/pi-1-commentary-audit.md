# Pārājikapāḷi (`pi-1`) — root text and commentaries: structure, content, links

**Date:** 2026-11-11
**Texts:**

- Root: `1-SOURCES/Text/pi-1.md` (Pārājikapāḷi, Vinaya book 1)
- `1-SOURCES/Commentaries/pi-parajika-atthakatha.md` (Samantapāsādikā)
- `1-SOURCES/Commentaries/pi-parajika-saratthadipani.md` (Sāratthadīpanī-ṭīkā)
- `1-SOURCES/Commentaries/pi-parajika-vimativinodani.md` (Vimativinodanī-ṭīkā)
- `1-SOURCES/Commentaries/pi-parajika-vajirabuddhi.md` (Vajirabuddhi-ṭīkā)

**Checked against:** tipitaka.app (`vp-prj` for the root; `atta-vp-prj`, `tika-vp-prj`, `tika-vimativinodani-tika`, `tika-vajirabuddhi-tika` for the commentaries), through its `/api/children`, `/api/text` and `/api/links` endpoints. The site data is saved in `0-INBOX/tipitaka-app/` (`*.json` contents trees, `text/`, `links/`); the checks are `compare_toc.py`, `compare_tree.py`, `compare_text.py` and `compare_links.py` in the same folder.

Same checks as the Abhidhamma audits (e.g. the Kathāvatthu report). Nothing in the source text was altered.

---

## Summary

| Check | Result |
|---|---|
| Paragraph count, ours vs site | identical in all five files (2,477 / 2,974 / 3,319 / 3,136 / 2,673) |
| Text, word for word | identical apart from 27 spacing differences, all where the site drops the space between two bold runs (see below) |
| Headings | follow the site's contents tree exactly: root 78/78, aṭṭhakathā 149/149, Sāratthadīpanī 151/151, Vimativinodanī 136/136, Vajirabuddhi 110/110 |
| Hierarchy | every heading has the same parent, the same position among its siblings and the same number of children as on the site, and every heading ID is its path in the tree (`compare_tree.py`) |
| Links to the root (aṭṭhakathā) | all 367 of the site's paranum links are present; ours has 410 (ranges linked in full) |
| Links (ṭīkā) | the site's 328 Sāratthadīpanī paranum links all join paragraphs with the same printed number, which is what our ṭīkā → root links use |
| Unresolved citations | 0 |
| Linter | passes, all five files |
| Library category and tag | `category_id: 4wuvGxIgXNZ5mb0bDWvkC` (Monastic Rules, འདུལ་བ།), `tag_ids: [296WZOr8MXWteSqBBI7pl]` (Theravāda); no Chants tag |

## What was fixed

| Issue | What was wrong | Fix | Files |
|---|---|---|---|
| Abbreviated range citations | CST prints some ranges with a truncated tail (`133-4.` = 133–134, `146-9.` = 146–149); the converter read them as "133 down to 4" and made no link, silently | kept as printed; linked to the full range; recorded in each file's `source_note` | aṭṭhakathā 26, Sāratthadīpanī 4, Vimativinodanī 18, Vajirabuddhi 32 (241 across all five books) |

| Sāratthadīpanī volume break | the second volume's title `Sāratthadīpanī-ṭīkā (dutiyo bhāgo)` was a `###` heading, shifting the sibling positions of the four kaṇḍas after it; tipitaka.app joins the volumes with no heading | kept as a line of text, not a heading | Sāratthadīpanī |

The fixes are in `4-SYSTEM/Skills/json-to-commentary/scripts/converters/tipitaka_org_atthakatha.py` and `0-INBOX/raw-data/build_tika_json.py`; every file was rebuilt with `0-INBOX/raw-data/build_all.sh`.

## What was checked and left unchanged

| Item | Why nothing was changed |
|---|---|
| 27 spacing differences (`Athakho` on the site, `Atha kho` ours) | the XML has a real space between two `<hi rend="bold">` runs (`<hi>Atha</hi> <hi>kho …`); the site's display drops it. Ours follows the source. Root 1, aṭṭhakathā 23, Sāratthadīpanī 1, Vimativinodanī 1, Vajirabuddhi 0 |
| Bold and note markup | the site shows bold lemmas as `**…**` and notes as `{…}`; our files have plain text and `[…]`, as the Abhidhamma files do |
| Range citations linked in full | the site links a range only by its first number; ours links every paragraph in the range, as the Abhidhamma files do |

## Known source irregularity

**Sāratthadīpanī, Saṅghādisesakaṇḍa.** After the citation `236-237.`, the ṭīkā retells King Kosala's sixteen dreams (from the Mahāsupina-jātaka), numbering the dreams 1–16 and then their meanings 1–16. CST marks these as paragraph numbers (`<p rend="bodytext" n="1"><hi rend="paranum">1</hi>`), so they are linked to root paragraphs 1–16 of the Verañjakaṇḍa — 32 links that are list numbers, not citations. tipitaka.app links them the same way (32 paranum links). Following the Abhidhamma practice, they are linked exactly as printed and recorded in the file's `source_note`. **A reviewer should decide whether to drop these 32 links.**

No other citation in the four commentaries runs backwards or jumps outside its section.

## Still to do before upload

- linter + parser outputs (text, edition, TOC, alignment JSON) — the "structural audit" commit
- library upload: root text first, then the four commentaries
