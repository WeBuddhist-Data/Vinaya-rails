# Vinaya — completeness re-check and file rename (2026-11-23)

The user's plan:
1. Check each book against tipitaka-xml for complete content.
2. If complete, it is fine; if not, ingest it and redo the content, TOC and block-ID checks.
3. Do the same for the commentaries.
4. Rename `pi-N` to `pi-<book name>`.

## 1. Root texts: complete ✅

tipitaka.app lists 5 Vinaya books: Pārājika, Pācittiya, Mahāvagga, Cūḷavagga and Parivāra. All 5 are in the vault.

[`compare_vin.py`](compare_vin.py) compares each with its XML line by line:

| Book | XML lines | In the vault | Differences (all known and documented 2026-11-17/20) |
|---|---|---|---|
| Pārājikapāḷi (`vin01m`) | 2,477 | 2,477 | none |
| Pācittiyapāḷi (`vin02m1`) | 3,690 | 3,690 | none |
| Mahāvaggapāḷi (`vin02m2`) | 2,759 | all | 2 verse numbers joined to their verse; 1 space inside `{ }` |
| Cūḷavaggapāḷi (`vin02m3`) | 2,821 | all | the `Dutiyanavakaṃ` note kept as text; 1 space inside `{ }` |
| Parivārapāḷi (`vin02m4`) | 3,645 | all | 34 verse numbers joined to their verse; `1. Bhikkhuvibhaṅgo` moved below `Soḷasamahāvāro` |

Since every book is complete, step 2 is not needed. The TOC and block IDs were fixed and checked on 2026-11-17/20.

## 3. Commentaries: complete ✅

[`comm_coverage.py`](comm_coverage.py) lines up each CSCD commentary XML with all the vault files cut from it, in book order. A ṭīkā file is cut into up to 5 vault files, so this also checks the joins between books.

| Layer | XML | Vault files | XML lines missing | Vault lines not in the XML |
|---|---|---|---|---|
| aṭṭhakathā | `vin01a`, `vin02a1`–`a4` | 5 | 0 | 0 |
| Sāratthadīpanī | `vin01t1`+`t2`, `vin02t` | 5 | 0 | 3 |
| Vajirabuddhi | `vin06t` | 5 | 0 | 4 |
| Vimativinodanī | `vin07t` | 5 | 0 | 3 |
| Yojanā | `vin12t` | 4 | 0 | 3 |

The 13 "extra" lines are the `# Vinayapiṭake` title that opens every vault file, where the XML prints it once per file.

**Not ingested, by decision:** seven post-canonical works from the same CSCD shelf (Dvemātikā–Kaṅkhāvitaraṇī, Vinayasaṅgaha, Vinayālaṅkāra, the Kaṅkhāvitaraṇī ṭīkās, Vinayavinicchaya and its ṭīkā, Khuddasikkhā–Mūlasikkhā). They are documented in `4-SYSTEM/Guidelines/vault-annex.md` §1.

## 4. Rename ✅ ([`rename_roots.py`](rename_roots.py))

| Before | After |
|---|---|
| `pi-1.md` | `pi-parajikapali.md` |
| `pi-2.md` | `pi-pacittiyapali.md` |
| `pi-3.md` | `pi-mahavaggapali.md` |
| `pi-4.md` | `pi-culavaggapali.md` |
| `pi-5.md` | `pi-parivarapali.md` |

The new names follow CLAUDE.md §4: lowercase, hyphenated, no diacritics.

**What else was updated:**
- **Commentaries:** in all 24, 6,105 transclusions and the `root_text:` lines now point at the new names. `check_links.py` finds 0 problems.
- **`vault-annex.md`:** its 17 mentions.
- **`add-block-id-commentary/apply.py`:** the new stems added to its root-to-book map. The `pi-1` … `pi-5` entries stay, because they are the Abhidhamma vault's roots.
- **`interlinear-gloss`:** its hard-coded source path.
- **`tipitaka-xml-to-json`:** comments that cite the old names.
- **Generated linter and parser output:** 30 files moved to the new names.

**Not changed:**
- **The library:** titles and ids live in the frontmatter, which is unchanged.
- **The git-ignored prod ledger** (`4-SYSTEM/ledgers/prod/texts.json`): it is still keyed by the old paths. `library-upload` falls back to the frontmatter ids, and the skill forbids editing ledgers by hand.
