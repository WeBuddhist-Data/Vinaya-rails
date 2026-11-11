"""Compare a source JSON (built from tipitaka-xml) with tipitaka.app's text,
paragraph by paragraph (both use the same CST paragraph order).

Normalisation on both sides: page markers |T1.0001| removed, ‘‘ ’’ -> ",
bold ** and note braces {} normalised, whitespace collapsed, a leading printed number "N." / "N-M." removed.
Differences are classed as:
  glued  - one of our words is two site words run together (or the reverse)
  other  - anything else
Usage: compare_text.py <site-text.json> <source.json> [label]
"""
import difflib, json, re, sys
from pathlib import Path

LEAD = re.compile(r"^\s*\d+(?:-\d+)*\s*\.\s*")


def norm(s):
    s = re.sub(r"\|[A-Z]\d+\.\d+\|", " ", s)
    s = s.replace("‘‘", '"').replace("’’", '"')
    # display markup only: the site shows bold lemmas as **…** and CST notes
    # as {…}; the source JSON has plain text and […] (as the Abhidhamma JSON)
    s = s.replace("**", "").replace("{", "[").replace("}", "]")
    s = re.sub(r"\s+", " ", s).strip()
    return LEAD.sub("", s)


def main(site_path, src_path, label=None):
    site = json.loads(Path(site_path).read_text(encoding="utf-8"))["paras"]
    src = json.loads(Path(src_path).read_text(encoding="utf-8"))["segments"]
    label = label or Path(src_path).stem
    if len(site) != len(src):
        print(f"{label}: paragraph count differs (site {len(site)}, ours {len(src)})")
    glued, other, same = [], [], 0
    for k, (a, b) in enumerate(zip(site, src)):
        sa, sb = norm(a["t"]), norm(b["content"])
        if sa == sb:
            same += 1
            continue
        wa, wb = sa.split(" "), sb.split(" ")
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, wa, wb, autojunk=False).get_opcodes():
            if op == "equal":
                continue
            x, y = " ".join(wa[i1:i2]), " ".join(wb[j1:j2])
            if x.replace(" ", "") == y.replace(" ", ""):
                glued.append((k, x, y))
            else:
                other.append((k, x, y))
    print(f"{label}: {len(src)} paragraphs, {same} identical, "
          f"{len(glued)} spacing differences, {len(other)} other differences")
    for k, x, y in glued[:15]:
        print(f"  spacing  #{k}: site '{x}'  ours '{y}'")
    for k, x, y in other[:15]:
        print(f"  other    #{k}: site '{x[:80]}'  ours '{y[:80]}'")
    return glued, other


if __name__ == "__main__":
    main(*sys.argv[1:])
