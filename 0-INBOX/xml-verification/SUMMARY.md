# Vinaya vault vs tipitaka-xml — summary of the verification

- **Date:** 2026-11-13 – 2026-11-17
- **Scope:** the 5 root texts in `1-SOURCES/Text/` and the 24 commentaries in `1-SOURCES/Commentaries/`, each checked one by one against VRI's CST romanised XML (`tipitaka-xml/romn/`).
- **Per-file reports:** `pi-N-verification.md` and `c-<registered-id>-verification.md` in this folder.

## Result in one line

**All 29 files have exactly the same text as the XML.** No word is added, missing or changed. Every block ID is in place, and every root-verse transclusion in the commentaries points at the right paragraph. The only text defect was spacing added by the conversion, now fixed. What remains is the TOC work listed below, deferred by decision.

## 1. Spaces before punctuation ✅ fixed in all 29 files

- **The defect.** The XML→Markdown conversion turned `word<pb/>.` into `word .`. Note that CST always puts a `<pb>` page marker after a word and before its punctuation.
- **The fix.** [`fix_pb_spaces.py`](fix_pb_spaces.py) removed only the spaces the source does not have, after pairing every vault line with its XML line. Each file was fixed on the user's approval.
- **Total: 3,111 spaces removed.**

| Root text | Spaces | Commentaries on it | Spaces |
|---|---|---|---|
| pi-1 Pārājika | 267 | aṭṭhakathā 297 · Sāratthadīpanī 228 · Vajirabuddhi 86 · Vimativinodanī 71 | 682 |
| pi-2 Pācittiya | 257 | aṭṭhakathā 92 · Sāratthadīpanī 37 · Vajirabuddhi 23 · Vimativinodanī 15 · Yojanā 49 | 216 |
| pi-3 Mahāvagga | 446 | aṭṭhakathā 80 · Sāratthadīpanī 51 · Vajirabuddhi 32 · Vimativinodanī 26 · Yojanā 81 | 270 |
| pi-4 Cūḷavagga | 499 | aṭṭhakathā 56 · Sāratthadīpanī 14 · Vajirabuddhi 6 · Vimativinodanī 7 · Yojanā 39 | 122 |
| pi-5 Parivāra | 233 | aṭṭhakathā 57 · Sāratthadīpanī 5 · Vajirabuddhi 10 · Vimativinodanī 9 · Yojanā 38 | 119 |

- **Spaces that are in the source stay**, by the user's decision of 2026-11-13. They are listed per file in `*-spaces-kept.md`, typed A–D.
- **After each fix,** the block IDs, transclusion links, line count and CRLF line endings were checked unchanged, and a second run found nothing left.
- **Backups.** Pre-fix copies are in [`backups/`](backups/), except **pi-1 and pi-2**, whose backups were lost when an old scratchpad folder was cleared.

## 2. Heading tree (TOC) ✅ fixed 2026-11-17 — none of these touched paragraph IDs

| File | Issue | Report |
|---|---|---|
| pi-1 | ✅ **Fixed 2026-11-17:** the Nissaggiya sikkhāpadas are now nested under their 3 vaggas (32 heading lines changed) | [pi-1](pi-1-verification.md) |
| pi-2 | ✅ **Fixed 2026-11-17:** the 12 Bhikkhunī Nissaggiya rules are now nested under `1. Pattavaggo` (12 heading lines changed) | [pi-2](pi-2-verification.md) |
| pi-5 | ✅ **Fixed 2026-11-17:** the Soḷasamahāvāro is rebuilt (93 heading lines). `Bhikkhunīvibhaṅgo` now holds its 16 vāras; the bhikkhunī vāras are de-nested; 56 vaggas sit under their kaṇḍas. **2026-11-20:** `1. Bhikkhuvibhaṅgo` is a heading again (`^5-1-1-0`), holding the 16 bhikkhu vāras as the sibling of `Bhikkhunīvibhaṅgo` (`^5-1-2-0`); the one heading line moved below `Soḷasamahāvāro` is registered in the annex | [pi-5](pi-5-verification.md) §2 |
| parajika-atthakatha | ✅ `Nigamanavaṇṇanā` fixed 2026-11-17. `(dutiyo bhāgo)` under the first volume is **accepted as is**, since a fix would renumber content IDs | [→](c-parajika-atthakatha-verification.md) |
| parajika-saratthadipani | ✅ `Nigamanavaṇṇanā` fixed 2026-11-17. The plain-text `(dutiyo bhāgo)` is **accepted as is**, for the same reason | [→](c-parajika-saratthadipani-verification.md) |
| parajika-vajirabuddhi | ✅ **Fixed 2026-11-17:** each kaṇḍa (and the Verañjakaṇḍa) is now the parent of its own rules and vaggas (102 heading lines) | [→](c-parajika-vajirabuddhi-verification.md) |
| parajika-vimativinodani | ✅ `Nigamanavaṇṇanā` fixed 2026-11-17; the tree now matches the XML exactly | [→](c-parajika-vimativinodani-verification.md) |
| pacittiya-vajirabuddhi | ✅ **Fixed 2026-11-17:** the tree is rebuilt so each kaṇḍa holds its own vaggas and rules, in both the bhikkhu and bhikkhunī parts (193 heading lines) | [→](c-pacittiya-vajirabuddhi-verification.md) |
| pacittiya-vimativinodani | ✅ **Fixed 2026-11-17:** `Bhikkhunīvibhaṅgavaṇṇanā` is now `###` and holds the 5 bhikkhunī kaṇḍas (29 heading lines) | [→](c-pacittiya-vimativinodani-verification.md) |
| pacittiya-yojana | ✅ **Fixed 2026-11-17:** vaggas are now under their Pācittiya kaṇḍas, the bhikkhunī Pāṭidesanīya is its own kaṇḍa, and one mis-tagged rule is restored (192 heading lines) | [→](c-pacittiya-yojana-verification.md) |

**✅ Decided 2026-11-17: unnumbered headings stay nested.** Where an unnumbered heading belongs to the numbered heading before it, the vault nests it one level deeper, unlike the XML's flat level. This applies in pi-3 (2), pi-4 (123), the Mahāvagga Yojanā (5) and the Cūḷavagga Yojanā (9). It is registered as **this vault's convention only, not a general rule**, in [`vault-annex.md`](../../4-SYSTEM/Guidelines/vault-annex.md) §2 "Registered deviations". No file changes were needed.

**Cross-file ID differences.** These break nothing, but matter if TOCs are ever aligned:
- pi-5 makes `Atthavasapakaraṇaṃ` a chapter, which the XML and tipitaka.org do not.
- Some commentaries have no Bhikkhunīvibhaṅga heading, so their `^2-5-0` means something different.

## 3. Faithful to the source — leave, or mark with `[Ed: …]` ℹ️

Stray digits after a `<pb>` in VRI's own text, also in the `deva master` files:

| File | Line | Text |
|---|---|---|
| pi-1 | 2637 | `sāvatthiṃ 2` |
| pi-2 | 988 | `Tena 0 kho` |
| pi-parajika-saratthadipani | 621 | `Sabbameva 2 hidanti` |
| pi-pacittiya-atthakatha | 1318 | `Acelakavaggassa 9 paṭhamasikkhāpada…` |

## 4. Still to do

- **Library:** ✅ **done on prod 2026-11-20** with `library-upload` (installed from rails-template the same day), by a developer's decision:
  - All 29 editions were fully replaced: segmentation deleted → whole content replaced → segmentation posted → TOC rebuilt. pi-5 needed this anyway (504 segments, the old `^5-U1` is gone). The other 28 used the vault-local `--full-replace` flag.
  - The alignments of all 24 commentaries were pushed again from their transclusions.
  - `status` and `verify` report all 29 `ok`, including the segment types (paragraph → verse) that had differed in 23 commentaries.
  - The new `toc_id`s are in the frontmatter of all 29 notes (written with `update --only ids`, added to the skill the same day) and in the git-ignored ledger `4-SYSTEM/ledgers/prod/texts.json`. `status` and `verify` confirm frontmatter, ledger and prod agree.
- **TOC fixes:** ✅ all done 2026-11-17. Every row in section 2 is fixed or accepted, and each fix has a `*.pre-toc-fix.md.bak` backup in [`backups/`](backups/).
- **Commit:** nothing has been committed.

## Tools (this folder)

- **[`compare_vin.py`](compare_vin.py)** compares content line by line.
- **[`compare_headings.py`](compare_headings.py)** checks each heading's parent.
- **[`check_links.py`](check_links.py)** checks block IDs and transclusions.
- **[`fix_pb_spaces.py`](fix_pb_spaces.py)** removes the conversion spaces.
- **[`kept_spaces.py`](kept_spaces.py)** lists the source spaces that stay.
- **[`slice_xml.py`](slice_xml.py)** cuts one book's part out of a multi-book ṭīkā XML.

Intermediate files are in `tmp/`.
