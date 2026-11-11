# 4-SYSTEM/scripts

Standalone scripts that are not bundled inside a single skill — either because several skills use them, or because they are vault-maintenance tools rather than steps in a workflow.

A script that belongs to exactly one skill lives in that skill's own `scripts/` folder instead, so the skill stays self-contained and can be installed anywhere.

| Script | What it does |
| ------ | ------------ |
| `install-skills.py` | Installs skills from the shared skill library into `4-SYSTEM/Skills/`, resolving the library's logical location names to this vault's paths and writing the `.claude/commands/` stubs. See [`../How-to guides/Sync with rails-template.md`](../How-to%20guides/Sync%20with%20rails-template.md). |
| `tipitaka-xml-to-json/` | Pāli Tipiṭaka intake from the VipassanaTech/tipitaka-xml (CST) repo: `xml_to_json.py` turns a romn XML file into the tipitaka.org JSON schema the `json-to-source-text` / `json-to-commentary` converters read; `vinaya_structure.py` nests vagga and mid-file book headings; `apply_site_toc.py` sets heading levels from the tipitaka.app contents tree (the reference the Abhidhamma vault checked its TOCs against; trees saved in `0-INBOX/tipitaka-app/`); `heading_ids.py` assigns `^T-N`, heading and `U` IDs (step 4 of `add-block-id-root-text`); `fidelity_check.py` checks every source word is in the markdown, in order. Driven by `0-INBOX/raw-data/build_all.sh`. |
| `linter-root-text/` · `linter-commentary/` | Lint a root text or a commentary in `1-SOURCES/` against the API rules (frontmatter, block IDs, TOC headings, yigchungs, durchens `[^dN]`, footnotes `[^fN]`, `tag_ids`) and write `output/<stem>.lint.json`. Run before the parser. See each folder's `README.md`. |
| `parser-root-text/` · `parser-commentary/` | Turn a linted source into the API payloads in `output/<stem>/`: text, edition, TOC, yigchungs, durchens, footnotes (by position) and, for a commentary, its alignment to the root text. The four tools share `durchen.py`, kept byte-identical. Vendored: see each folder's `UPSTREAM.md`. |

## Conventions

**Vendored code records its upstream.** If you copy a tool in from another repository rather than writing it here, put an `UPSTREAM.md` beside it recording the source repository, the path, the commit it was pinned at, and the date. Make the first commit byte-identical to upstream so that every later commit reads as your delta — then a re-sync is a diff rather than an archaeology exercise. Say in the same file *why* it was forked, and whether the changes should be offered back upstream.

**Nothing here writes to `1-SOURCES/` in place.** Scripts may create whole files from reviewed inbox material; they may not rewrite a source file's content.

**Credentials never live in the repository.** A script that needs one reads it from the environment or from a `.env` file that is git-ignored, and ships a `.env.example` containing **placeholders only** — never a real address, password or token, even an expired one.

**Generated output goes to `0-INBOX/`**, not into this folder.
