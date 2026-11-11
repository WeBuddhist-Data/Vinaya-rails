Read `4-SYSTEM/Skills/edition-spacing-fix/SKILL.md` in full, then execute it on the file(s) or input the user specifies.

Skill purpose: Scan a published edition on the library backend for spacing errors — words run together ("whomI", "forthlike", "ofthe"), no space after punctuation ("wheels,fire"), doubled or stray spaces, odd whitespace — record every hit in a mapping file, and after human review fix the approved ones in place, bottom-up, through PATCH /v2/editions/{id}/content without moving a single segment boundary.
