"""Compare the heading tree of a vault file with tipitaka.app's contents tree:
for every heading, its parent, its position among its siblings, and its
number of children; and check that each heading's block ID is its path
in the tree (e.g. ^1-2-3-0 = 3rd child of the 2nd ### under book 1).

Headings are matched in order by title (leading numbers ignored). For a file
that is one part of a larger work, the site tree is cut to the matched span.
Usage: compare_tree.py <file.md> <site-toc.json>
"""
import difflib, json, re, sys
from pathlib import Path

NUM = re.compile(r"^\s*\d+(?:-\d+)*\.\s*")
NOTE = re.compile(r"\s*\[.*\]\s*$")


def key(t):
    return NOTE.sub("", NUM.sub("", t.replace("**", ""))).strip()


def tree(nodes):
    """nodes: list of (depth, title) in document order -> list of
    (title, parent_index or None, sibling_position, n_children, path)."""
    out, stack = [], []  # stack of indices
    counters = {}
    for i, (d, t) in enumerate(nodes):
        while stack and nodes[stack[-1]][0] >= d:
            stack.pop()
        parent = stack[-1] if stack else None
        counters[parent] = counters.get(parent, 0) + 1
        path = (out[parent][4] if parent is not None else ()) + (counters[parent],)
        out.append([t, parent, counters[parent], 0, path])
        if parent is not None:
            out[parent][3] += 1
        stack.append(i)
    return out


def main(md, toc):
    lines = Path(md).read_text(encoding="utf-8").split("\n")
    mine, ids = [], []
    book = None
    for l in lines:
        m = re.match(r"^(#+)\s+(.*?)\s+\^(\S+)\s*$", l)
        if not m:
            continue
        if len(m.group(1)) == 2:
            book = m.group(3).split("-")[0]
        if len(m.group(1)) >= 3:
            mine.append((len(m.group(1)), key(m.group(2))))
            ids.append(m.group(3))
    site_all = json.loads(Path(toc).read_text(encoding="utf-8"))
    theirs_all = [(n["depth"], key(n["title"])) for n in site_all]
    sm = difflib.SequenceMatcher(None, [t for _, t in mine], [t for _, t in theirs_all], autojunk=False)
    blocks = [b for b in sm.get_matching_blocks() if b.size]
    lo, hi = blocks[0].b, blocks[-1].b + blocks[-1].size
    theirs = theirs_all[lo:hi]
    # normalise depths so both trees start at the same top level
    off = min(d for d, _ in theirs) - 3
    theirs = [(d - off, t) for d, t in theirs]
    A, B = tree(mine), tree(theirs)
    sm = difflib.SequenceMatcher(None, [t for _, t in mine], [t for _, t in theirs], autojunk=False)
    amap = {}
    for op, a1, a2, b1, b2 in sm.get_opcodes():
        if op == "equal":
            for a, b in zip(range(a1, a2), range(b1, b2)):
                amap[a] = b
    diffs = []
    for a, b in amap.items():
        pa, pb = A[a][1], B[b][1]
        same_parent = (pa is None and pb is None) or (pa is not None and pb is not None and amap.get(pa) == pb)
        if not same_parent:
            diffs.append(f"parent differs: '{A[a][0]}' — vault parent '{A[pa][0] if pa is not None else '(book)'}', "
                         f"site parent '{B[pb][0] if pb is not None else '(book)'}'")
        elif A[a][2] != B[b][2] or A[a][3] != B[b][3]:
            diffs.append(f"siblings/children differ: '{A[a][0]}' — vault position {A[a][2]}, {A[a][3]} children; "
                         f"site position {B[b][2]}, {B[b][3]} children")
    unmatched_vault = [A[a][0] for a in range(len(A)) if a not in amap]
    unmatched_site = [B[b][0] for b in range(len(B)) if b not in amap.values()]
    bad_ids = [(i, "-".join([book] + [str(x) for x in A[k][4]]) + "-0")
               for k, i in enumerate(ids) if i != "-".join([book] + [str(x) for x in A[k][4]]) + "-0"]
    print(f"{Path(md).name}: {len(A)} headings, {len(amap)} matched; "
          f"{len(diffs)} parent/sibling/child differences; {len(bad_ids)} IDs not matching their tree path; "
          f"vault-only {len(unmatched_vault)}, site-only {len(unmatched_site)}")
    for d in diffs[:10]:
        print("  ", d)
    for t in unmatched_vault[:5]:
        print("   vault only:", t)
    for t in unmatched_site[:5]:
        print("   site only:", t)
    for i, want in bad_ids[:5]:
        print(f"   id ^{i} but tree path ^{want}")


if __name__ == "__main__":
    main(*sys.argv[1:])
