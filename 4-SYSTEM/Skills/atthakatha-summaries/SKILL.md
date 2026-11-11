---
name: atthakatha-summaries
description: Create structured, introductory summaries for each Table of Contents (TOC) level of a root text, based strictly on its Aṭṭhakathā (commentary).
profile: vault-local
---

# Skill: Aṭṭhakathā Summaries

**Purpose:** Create structured, introductory summaries for each Table of Contents (TOC) level of a root text, based strictly on its Aṭṭhakathā (commentary).

## Execution Steps

### 1. Extract TOC and Initialize Rails
- Read the target root text in `1-SOURCES/Texts/`.
- Extract the complete Table of Contents (TOC) tree, including **all levels** regardless of depth.
- Create a new file at `2-RAILS/Sections/<text name>-summaries.md`.
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
Immediately after every Markdown heading (on its own line, before the summary paragraph), insert a link back to the specific line in the TOC using its block ID:

```
[[#^toc-1-1|↑↑]]
```

Full example of a section block:

```markdown
## Section A

[[#^toc-1|↑↑↑]]

Ayaṃ summary paragraph...

[[Source-File#^anchor]]
```

### 2. Match with Aṭṭhakathā
- For each TOC level, search `1-SOURCES/Commentaries/` (or the specific Aṭṭhakathā file) to find the corresponding commentary section.

### 3. Draft Pāli Summaries
- Read the commentary's presentation of the section.
- Write a **single summary paragraph in Pāli** under the corresponding heading in `<text name>-summaries.md`.
- **Constraints:**
  - The summary must act as an effective introduction to the section for someone new to the text.
  - You must use the specific terms and vocabulary found in the commentary.
  - Preserve all Pāli diacritics exactly (e.g., ā, ī, ū, ṭ, ñ).

### 4. Append Citations
- Immediately following the summary paragraph, insert a direct wikilink to the exact commentary section used (e.g., `[[Aṭṭhakathā-File#Section-Name]]`).

### 5. Update Existing Documents
When adding new sections to an already-existing summaries file:
- Add the new entries to the TOC block at the top (maintaining hierarchy for **all levels** and adding unique, hierarchical block IDs to each new line).
- Add backlinks to each new heading pointing to its specific TOC line (e.g., `[[#^toc-1-1|↑]]`).