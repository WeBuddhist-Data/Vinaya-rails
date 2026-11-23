"""Rename the Vinaya root files pi-N to pi-<book>pali and repoint everything that names them.

  pi-1 -> pi-parajikapali   pi-2 -> pi-pacittiyapali   pi-3 -> pi-mahavaggapali
  pi-4 -> pi-culavaggapali  pi-5 -> pi-parivarapali     (CLAUDE.md §4: no diacritics)

- git mv the five files in 1-SOURCES/Text/, and the parser/linter output named after them;
- commentaries: `1-SOURCES/Text/pi-N.md` (transclusions and root_text) -> new path;
- vault-annex.md: every `pi-N` / `pi-N.md`;
- add-block-id-commentary/apply.py: the new stems added to its root-stem -> book map;
- interlinear-gloss generate_ai_gloss.py: its hard-coded source path;
- tipitaka-xml-to-json comments that cite pi-N.
Bytes other than the replaced names are untouched (line endings kept).

usage: python rename_roots.py [--write]      (from the vault root)
"""
import re, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
GIT = r"C:\Users\Uzumaki Sither\AppData\Local\GitHubDesktop\app-3.6.11\resources\app\git\cmd\git.exe"
NEW = {"1": "pi-parajikapali", "2": "pi-pacittiyapali", "3": "pi-mahavaggapali", "4": "pi-culavaggapali", "5": "pi-parivarapali"}
W = "--write" in sys.argv
git = lambda *a: subprocess.run([GIT, *a], capture_output=True, text=True, check=True).stdout

edits = {}
def sub(path, pattern, repl):
    p = Path(path)
    s = edits.get(path, p.read_bytes().decode("utf-8"))
    s2, n = re.subn(pattern, repl, s)
    edits[path] = s2
    return n

counts = {}
for f in sorted(Path("1-SOURCES/Commentaries").glob("*.md")):
    n = sub(str(f), r"1-SOURCES/Text/pi-([1-5])\.md", lambda m: f"1-SOURCES/Text/{NEW[m.group(1)]}.md")
    if n: counts[str(f)] = n
tok = r"(?<![\w-])pi-([1-5])(?![\w])"
for f in ["4-SYSTEM/Guidelines/vault-annex.md", "4-SYSTEM/scripts/tipitaka-xml-to-json/source_form.py",
          "4-SYSTEM/scripts/tipitaka-xml-to-json/apply_site_toc.py",
          "4-SYSTEM/Skills/interlinear-gloss/scripts/generate_ai_gloss.py"]:
    counts[f] = sub(f, tok, lambda m: NEW[m.group(1)])
ap = "4-SYSTEM/Skills/add-block-id-commentary/apply.py"
s = Path(ap).read_bytes().decode("utf-8")
if "pi-parajikapali" not in s:
    anchor = '"pi-kathavatthu": 5, "pi-5": 5,'
    assert s.count(anchor) == 1, "apply.py map not found"
    nl = "\r\n" if "\r\n" in s else "\n"
    indent = re.search(r"\n([ \t]*)" + re.escape(anchor), s).group(1)
    add = nl.join(f'{indent}"{NEW[k]}": {k},' for k in "12345")
    edits[ap] = s.replace(anchor, anchor + nl + indent + "# Vinaya roots, renamed 2026-11-23 from pi-1 … pi-5" + nl + add)
    counts[ap] = 5

moves = [(f"1-SOURCES/Text/pi-{k}.md", f"1-SOURCES/Text/{v}.md") for k, v in NEW.items()]
for f in git("ls-files", "4-SYSTEM/scripts").splitlines():
    m = re.match(r"^(4-SYSTEM/scripts/[^/]+/output/)(?:pi-([1-5])/)?pi-([1-5])(\.[\w.]+)$", f)
    if m and (m.group(2) is None or m.group(2) == m.group(3)):
        k = m.group(3)
        new = f"{m.group(1)}{NEW[k] + '/' if m.group(2) else ''}{NEW[k]}{m.group(4)}"
        moves.append((f, new))

for f, n in counts.items():
    print(f"{n:5}  {f}")
print(f"files to move: {len(moves)}")
for a, b in moves[:8]:
    print(f"   {a}  ->  {b}")
if W:
    for f, s in edits.items():
        Path(f).write_bytes(s.encode("utf-8"))
    for a, b in moves:
        Path(b).parent.mkdir(parents=True, exist_ok=True)
        git("mv", a, b)
    print("written")
else:
    print("dry run; pass --write to apply")
