// Deep headings: Obsidian only knows headings # to ######, so a deeper node
// written '####### title ^1-2-3-1-1-4-0' is plain text to it: no heading
// style, no fold arrow. This makes 7+ '#' lines behave like headings, in the
// editor and in reading view: styled, with an arrow that folds everything
// down to the next heading of the same or a higher level.

const { Plugin, MarkdownView } = require("obsidian");
const { foldService, foldEffect, unfoldEffect, foldedRanges } = require("@codemirror/language");
const { Prec } = require("@codemirror/state");
const { ViewPlugin, Decoration, WidgetType } = require("@codemirror/view");

const HEAD_RE = /^(#+)\s/;
const DEEP_RE = /^#{7,}\s/;
const DEEP_TEXT_RE = /^(#{7,})\s+/;

// Number of '#' of a heading line, 0 when the line is not a heading.
function headingLevel(text) {
  const m = HEAD_RE.exec(text);
  return m ? m[1].length : 0;
}

// ---------------------------------------------------------------------------
// Editor (Live Preview and Source mode)
// ---------------------------------------------------------------------------

// What a deep heading folds: the rest of its line down to the last non-blank
// line before the next heading of the same or a higher level.
function deepRange(doc, head) {
  const level = headingLevel(head.text);
  let last = head;
  for (let n = head.number + 1; n <= doc.lines; n++) {
    const line = doc.line(n);
    const lv = headingLevel(line.text);
    if (lv && lv <= level) break;
    last = line;
  }
  while (last.number > head.number && !last.text.trim()) last = doc.line(last.number - 1);
  return last.number === head.number ? null : { from: head.to, to: last.to };
}

// The existing fold that starts where this heading's range starts, if any.
function foldAt(state, from) {
  let found = null;
  foldedRanges(state).between(from, from, (a, b) => {
    if (a === from) found = { from: a, to: b };
  });
  return found;
}

// Lets Obsidian's own fold commands (Toggle fold, Fold all) fold deep headings.
const deepFold = Prec.highest(
  foldService.of((state, lineStart) => {
    const head = state.doc.lineAt(lineStart);
    return DEEP_RE.test(head.text) ? deepRange(state.doc, head) : null;
  })
);

class FoldArrow extends WidgetType {
  constructor(folded) {
    super();
    this.folded = folded;
  }

  eq(other) {
    return other.folded === this.folded;
  }

  toDOM(view) {
    const el = document.createElement("span");
    el.className = "deep-heading-fold" + (this.folded ? " is-collapsed" : "");
    el.setAttribute("aria-label", this.folded ? "Expand" : "Collapse");
    el.addEventListener("mousedown", (e) => {
      e.preventDefault();
      e.stopPropagation();
      const head = view.state.doc.lineAt(view.posAtDOM(el));
      const range = deepRange(view.state.doc, head);
      if (!range) return;
      const open = foldAt(view.state, range.from);
      view.dispatch({ effects: open ? unfoldEffect.of(open) : foldEffect.of(range) });
    });
    return el;
  }

  ignoreEvent() {
    return true;
  }
}

const deepLines = ViewPlugin.fromClass(
  class {
    constructor(view) {
      this.decorations = this.build(view);
    }

    update(u) {
      if (u.docChanged || u.viewportChanged || u.transactions.some((t) => t.effects.length)) {
        this.decorations = this.build(u.view);
      }
    }

    build(view) {
      const doc = view.state.doc;
      const decos = [];
      for (const { from, to } of view.visibleRanges) {
        for (let pos = from; pos <= to; ) {
          const line = doc.lineAt(pos);
          if (DEEP_RE.test(line.text)) {
            const level = headingLevel(line.text);
            decos.push(Decoration.line({
              attributes: { class: "deep-heading-line", "data-level": String(level) },
            }).range(line.from));
            const range = deepRange(doc, line);
            if (range) {
              decos.push(Decoration.widget({
                widget: new FoldArrow(!!foldAt(view.state, range.from)),
                side: -1,
              }).range(line.from));
            }
          }
          pos = line.to + 1;
        }
      }
      return Decoration.set(decos, true);
    }
  },
  { decorations: (v) => v.decorations }
);

// ---------------------------------------------------------------------------
// Reading view
// ---------------------------------------------------------------------------

module.exports = class DeepHeadings extends Plugin {
  onload() {
    this.registerEditorExtension([deepFold, deepLines]);

    this.collapsed = new Map(); // file path -> Set of collapsed heading keys
    this.pending = null;
    this.registerMarkdownPostProcessor((el, ctx) => {
      this.renderHeadings(el, ctx.sourcePath);
      this.schedule();
    });
    this.registerEvent(this.app.workspace.on("layout-change", () => this.schedule()));
    this.register(() => window.clearTimeout(this.pending));
  }

  // Turn each '####### title' paragraph into a heading with a collapse arrow.
  renderHeadings(el, path) {
    for (const p of Array.from(el.querySelectorAll("p"))) {
      const first = p.firstChild;
      if (!first || first.nodeType !== Node.TEXT_NODE) continue;
      const m = DEEP_TEXT_RE.exec(first.textContent);
      if (!m) continue;
      const level = m[1].length;
      first.textContent = first.textContent.slice(m[0].length);

      const head = document.createElement("div");
      head.className = "deep-heading";
      head.dataset.level = String(level);
      const arrow = head.appendChild(document.createElement("span"));
      arrow.className = "deep-heading-toggle";
      const title = head.appendChild(document.createElement("span"));
      title.className = "deep-heading-title";
      // A heading is one line; lines after it with no blank line between
      // stay a paragraph.
      while (p.firstChild && p.firstChild.nodeName !== "BR") title.appendChild(p.firstChild);
      if (p.firstChild) p.removeChild(p.firstChild);
      p.before(head);
      if (!p.textContent.trim()) p.remove();

      const key = `${level}\u0000${title.textContent.trim()}`;
      head.dataset.key = key;
      arrow.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        const set = this.collapsedFor(path);
        if (set.has(key)) set.delete(key);
        else set.add(key);
        this.applyCollapse(head.closest(".markdown-preview-sizer"), path);
      });
    }
  }

  collapsedFor(path) {
    if (!this.collapsed.has(path)) this.collapsed.set(path, new Set());
    return this.collapsed.get(path);
  }

  // Hide every rendered section under a collapsed deep heading, down to the
  // next heading (deep or h1-h6) of the same or a higher level.
  applyCollapse(sizer, path) {
    if (!sizer) return;
    const set = this.collapsed.get(path);
    const stack = [];
    for (const child of Array.from(sizer.children)) {
      if (/\bmod-(header|footer)\b/.test(child.className)) continue;
      const deep = child.querySelector(".deep-heading");
      let level = 0;
      if (deep) level = Number(deep.dataset.level);
      else {
        const h = child.querySelector(":scope > h1, :scope > h2, :scope > h3, :scope > h4, :scope > h5, :scope > h6");
        if (h) level = Number(h.tagName[1]);
      }
      if (level) while (stack.length && stack[stack.length - 1] >= level) stack.pop();
      child.classList.toggle("deep-heading-hidden", stack.length > 0);
      if (deep) {
        const isCollapsed = !!(set && set.has(deep.dataset.key));
        deep.classList.toggle("is-collapsed", isCollapsed);
        if (isCollapsed) stack.push(level);
      }
    }
  }

  // Reading view renders sections lazily while scrolling: re-apply after.
  schedule() {
    if (this.pending) return;
    this.pending = window.setTimeout(() => {
      this.pending = null;
      for (const leaf of this.app.workspace.getLeavesOfType("markdown")) {
        const view = leaf.view;
        if (!(view instanceof MarkdownView) || !view.file) continue;
        const sizer = view.previewMode.containerEl.querySelector(".markdown-preview-sizer");
        this.applyCollapse(sizer, view.file.path);
      }
    }, 50);
  }
};
