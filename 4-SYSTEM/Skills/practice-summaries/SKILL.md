---
name: practice-summaries
description: Extract practical information from commentaries to provide guidance on sabbapāpassa akaraṇa, kusalassa upasampadā, and sacittapariyodapana based on the root text.
profile: vault-local
---

# Skill: Practice Summaries

**Purpose:** Create structured practice-oriented summaries for each Table of Contents (TOC) level of a root text, based on its commentaries (Aṭṭhakathā, Mūlaṭīkā, or Anuṭīkā), focusing on ethical conduct and mental development.

## Execution Steps

### 1. Extract TOC and Initialize Rails
- Read the target root text in `1-SOURCES/`.
- Extract the complete Table of Contents (TOC) tree, including **all levels** regardless of depth.
- Create a new file at `2-RAILS/Sections/<text name>-practice.md`.
- At the very top of the file, before any section headings, insert a **TOC block** (see format below).
- Then outline the rest of the file using Markdown headings that match the extracted TOC tree for **all levels**.

#### TOC Block Format
The TOC block is a nested bullet list using Obsidian within-file heading links (`[[#Heading Name]]`). It must reflect the **full heading hierarchy** of the document, capturing every level present in the source text. **Each line in the TOC must end with a unique, hierarchical Obsidian block ID** (e.g., `^toc-1-1`) for granular referencing. Example:

```markdown
## Contents

- [[#Level 1 Section]] ^toc-1
  - [[#Level 2 Subsection]] ^toc-1-1
    - [[#Level 3 Sub-subsection]] ^toc-1-1-1
      - [[#Level 4 Sub-sub-subsection]] ^toc-1-1-1-1
        - [[#Level 5 Sub-sub-sub-subsection]] ^toc-1-1-1-1-1
```

#### Heading Backlink Format
Immediately after every Markdown heading (on its own line, before the summary content), insert a link back to the specific line in the TOC using its block ID:

```
[[#^toc-1-1|↑↑↑]]
```

Full example of a section block:

```markdown
## Section A

[[#^toc-1|↑↑↑]]

Summary content...

[[Source-File#^anchor]]
```

### 2. Match with Commentaries
- For each TOC level, search `1-SOURCES/` for the corresponding commentary sections. Look specifically for:
    - Definitions of wholesome (*kusala*) and unwholesome (*akusala*) behaviors.
    - Instructions on abandonment of faults.
    - Methods for developing specific mental qualities or meditation subjects.

### 3. Draft Practice Summaries
- Under the corresponding heading in `<text name>-practice.md`, write a **single paragraph** in **Pāli** containing the practice summary. The paragraph weaves together whichever of the three pillars are supported by the commentary material found:
    - **sabbapāpassa akaraṇavidhi** — the method of not doing any evil: practical guidance on avoiding the akusala states described in the section.
    - **kusalassa upasampadāvidhi** — the method of achieving the good: practical guidance on cultivating the kusala states described in the section.
    - **sacittapariyodapanavidhi** — the method of purifying one's own mind: meditative or mindfulness-based applications derived from the commentary's analysis.
- **Constraints:**
    - The summary **must be written entirely in Pāli** with correct diacritics (e.g., ā, ī, ū, ṭ, ñ).
    - Include only the pillars for which the commentary provides concrete material — a section may yield one, two, or all three pillars depending on what is found.
    - The three pillars are **not written as separate labelled sub-sections or bullet points** — they are woven into a single flowing paragraph of Pāli prose.
    - The summary must be grounded in the traditional commentary's interpretation and may quote or closely paraphrase the commentary's own Pāli wording.
    - Maintain a clear, instructional tone in the Pāli prose.

### 4. Append Citations
- Immediately following the summary paragraph, insert a direct wikilink to the exact source section used (e.g., `[[pi-1-at#Section-Name]]`).

### 5. Update Existing Documents
When adding new sections to an already-existing practice file:
- Add the new entries to the TOC block at the top (maintaining hierarchy for **all levels** and adding unique, hierarchical block IDs to each new line).
- Add backlinks to each new heading pointing to its specific TOC line (e.g., `[[#^toc-1-1|↑↑↑]]`).
