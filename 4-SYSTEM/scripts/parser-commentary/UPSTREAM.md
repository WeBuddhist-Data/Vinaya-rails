# Upstream

| | |
|---|---|
| Source repository | https://github.com/WeBuddhist/Nalanda-texts-rails |
| Path | `4-SYSTEM/scripts/parser-commentary/` |
| Pinned commit | `3ec0e1bc` (2026-11-03, "Parsers: note text is a plain string") |
| Copied | 2026-11-03 |
| Origin | https://github.com/WeBuddhist/21-taras-rails, commit `2d14cddf9bdd207e34da4eff58b1d0fa98141a5f` (2026-10-01, "Add support for yigchungs in linter and parser"), vendored into Nalanda-texts-rails on 2026-10-12 |

Copied byte-identical, without the `output/` folder. Every later commit here is a template delta.

**Why vendored:** every vault turns its linted commentaries into the API payloads (text, edition, TOC, durchens, footnotes, alignment to the root text).

Same note as parser-root-text on `output/`.

## Changes made in Nalanda-texts-rails (before the copy)

- 2026-10-12: **durchens** (variant readings written as footnotes). Added `durchen.py`, shared by all four tools. The parser strips markers from `content` and TOC titles and writes `<stem>.durchens.json`. Offer it back to 21-taras-rails.
- 2026-10-26: **footnote types** (shared `durchen.py`): only `[^dN]` (and the old bare `[^N]`) become durchens. Same change as parser-root-text.
- 2026-10-29: **footnotes by position** (shared `durchen.py`): `[^fN]` footnotes (was `[^nN]`) get a position, the gap where the marker stood, written to `<stem>.footnotes.json`. Same change as parser-root-text.
- 2026-10-26: **odd spaces.** Same as parser-root-text: content, TOC titles and durchen texts go through `durchen.normalize_spaces()`.
- 2026-11-03: **note text is a plain string.** Alignment and the root-text heading lookup take the footnote definitions out first, so a transclusion or block ID inside a note is never aligned. Same change as parser-root-text.

## Template changes

None yet.
