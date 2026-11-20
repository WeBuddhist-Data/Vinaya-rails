"""Nest flattened sikkhāpada headings under their vagga.

Under one parent heading (e.g. `### 4. Nissaggiyakaṇḍaṃ ^1-5-0`), the source tags
vaggas and their sikkhāpadas alike, so they come out as siblings:

    #### 1. Cīvaravaggo                    ^1-5-1-0
    #### 1. Paṭhamakathinasikkhāpadaṃ      ^1-5-2-0   <- belongs to the vagga

This script makes every heading that follows a vagga (up to the next vagga or the
end of the parent) a child of that vagga, one '#' deeper, and renumbers the
heading IDs accordingly:

    #### 1. Cīvaravaggo                    ^1-5-1-0
    ##### 1. Paṭhamakathinasikkhāpadaṃ     ^1-5-1-1-0

Only heading lines change. Paragraph lines and their block IDs are untouched,
which the script asserts before writing.

usage: python nest_vaggas.py <file.md> <parent-id e.g. ^1-5-0> [--write]
"""
import re, sys
sys.stdout.reconfigure(encoding="utf-8")
path, parent_id = sys.argv[1], sys.argv[2].lstrip("^")
WRITE = "--write" in sys.argv
VAGGA = re.compile(r"^\d+\.\s+\S*vagg(o|a)\b", re.I)
HEAD = re.compile(r"^(#+)\s+(.*?)\s+\^([\w-]+)\s*$")

raw = open(path, "rb").read().decode("utf-8")
nl = "\r\n" if "\r\n" in raw else "\n"
L = raw.split(nl)

p = next(i for i, l in enumerate(L) if (m := HEAD.match(l)) and m.group(3) == parent_id)
d = len(HEAD.match(L[p]).group(1))
pre = parent_id[:-2]                      # "1-5-0" -> "1-5"

changes, c, vagga_prefix, j = [], 0, None, 0
child_map = None                          # (old_prefix, new_prefix, extra_depth) for descendants
for i in range(p + 1, len(L)):
    m = HEAD.match(L[i])
    if not m:
        continue
    hashes, title, hid = m.groups()
    depth = len(hashes)
    if depth <= d:
        break
    if depth == d + 1:
        old_prefix = hid[:-2]
        if VAGGA.match(title):
            c += 1; j = 0
            vagga_prefix = f"{pre}-{c}"
            new_id, new_depth = f"{vagga_prefix}-0", d + 1
        elif vagga_prefix:
            j += 1
            new_id, new_depth = f"{vagga_prefix}-{j}-0", d + 2
        else:
            c += 1
            new_id, new_depth = f"{pre}-{c}-0", d + 1
        child_map = (old_prefix, new_id[:-2], new_depth - depth)
    else:   # a descendant of the last direct child: carry the prefix and depth change
        op, np_, extra = child_map
        assert hid.startswith(op + "-"), (i + 1, hid, op)
        new_id, new_depth = np_ + hid[len(op):], depth + extra
    new = f"{'#' * new_depth} {title} ^{new_id}"
    if new != L[i]:
        changes.append((i + 1, L[i], new))
        L[i] = new

before = [l for l in raw.split(nl) if not HEAD.match(l)]
after = [l for l in L if not HEAD.match(l)]
assert before == after, "non-heading lines changed"
for ln, a, b in changes:
    print(f"{ln:6}: {a}\n        → {b}")
print(f"\nheadings changed: {len(changes)}; non-heading lines unchanged: True")
if WRITE:
    open(path, "wb").write(nl.join(L).encode("utf-8"))
    print("written:", path)
else:
    print("dry run; pass --write to save")
