"""Small helper for re-parenting headings in a vault file without moving any text.

Build the heading tree from a file, move nodes (with their subtrees) to a new
parent, then write it back: depths come from the tree, heading IDs are renumbered
from the tree under a fixed root, and headings deeper than ###### get their title
in **bold** (CLAUDE.md §5a). The tree's pre-order must equal document order, so
no text can move; non-heading lines are asserted unchanged.
"""
import re

HEAD = re.compile(r"^(#+)\s+(.*?)\s+\^([\w-]+)\s*$")
unbold = lambda t: re.sub(r"^\*\*(.*)\*\*$", r"\1", t)


class Node:
    def __init__(self, line, depth, title, hid):
        self.line, self.depth, self.title, self.id = line, depth, title, hid
        self.parent, self.kids = None, []

    def move_to(self, parent):
        if self.parent:
            self.parent.kids.remove(self)
        self.parent = parent
        parent.kids.append(self)
        parent.kids.sort(key=lambda n: n.line)

    def __repr__(self):
        return f"{self.title} ^{self.id}"


class Tree:
    def __init__(self, path):
        self.path = path
        raw = open(path, "rb").read().decode("utf-8")
        self.nl = "\r\n" if "\r\n" in raw else "\n"
        self.raw, self.L = raw, raw.split(self.nl)
        self.nodes, stack = [], []
        for i, l in enumerate(self.L):
            m = HEAD.match(l)
            if not m:
                continue
            n = Node(i, len(m.group(1)), unbold(m.group(2)), m.group(3))
            while stack and stack[-1].depth >= n.depth:
                stack.pop()
            if stack:
                n.parent = stack[-1]; stack[-1].kids.append(n)
            stack.append(n); self.nodes.append(n)

    def by_id(self, hid):
        return next(n for n in self.nodes if n.id == hid.lstrip("^"))

    def renumber(self, root):
        def go(n, prefix, depth):
            n.new_id, n.new_depth = prefix + "-0", depth
            for k, c in enumerate(n.kids, 1):
                go(c, f"{prefix}-{k}", depth + 1)
        go(root, root.id[:-2], root.depth)
        sub = []
        def pre(n):
            sub.append(n); [pre(c) for c in n.kids]
        pre(root)
        assert [n.line for n in sub] == sorted(n.line for n in sub), "tree order differs from document order"
        return sub

    def apply(self, root, write=False):
        sub = self.renumber(root)
        changes = []
        for n in sub:
            title = f"**{n.title}**" if n.new_depth > 6 else n.title
            new = f"{'#' * n.new_depth} {title} ^{n.new_id}"
            if new != self.L[n.line]:
                changes.append((n.line + 1, self.L[n.line], new))
                self.L[n.line] = new
        before = [l for l in self.raw.split(self.nl) if not HEAD.match(l)]
        assert before == [l for l in self.L if not HEAD.match(l)], "non-heading lines changed"
        if write:
            open(self.path, "wb").write(self.nl.join(self.L).encode("utf-8"))
        return changes

    def outline(self, root, collapse=lambda n: False, ind=0, out=None):
        out = [] if out is None else out
        out.append("  " * ind + f"{'#' * n.new_depth if (n := root) else ''} {root.title}  ^{root.new_id}")
        if collapse(root) and root.kids:
            out[-1] += f"   [+ {len(root.kids)} children ^{root.kids[0].new_id} … ^{root.kids[-1].new_id}]"
        else:
            for c in root.kids:
                self.outline(c, collapse, ind + 1, out)
        return out
