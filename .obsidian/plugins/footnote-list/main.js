// Footnote list: a sidebar with one line of plain text per footnote (label and
// note), in the order the markers appear. A click on the label jumps to the
// marker, a click on the note text to the definition. It stands in for the
// core Footnotes view, which renders every footnote as an embedded note and
// runs out of memory on long commentaries.

const { Plugin, ItemView, MarkdownView, debounce } = require("obsidian");

const DEF_RE = /^\[\^([^\]\s]+)\]:[ \t]?(.*)$/;
const MARK_RE = /\[\^([^\]\s]+)\]/g;
// Some notes have Windows line endings: a "\r" left on a line stops DEF_RE.
const LINE_RE = /\r?\n/;
const VIEW_TYPE = "footnote-list";

// Every footnote of a note: label, note text, the line of its first marker
// (or of its definition when it has no marker) and the line of its definition
// (null when it has none), in marker order, with unreferenced definitions
// last.
function footnoteEntries(source) {
  const lines = source.split(LINE_RE);
  const defs = new Map();
  const first = new Map();
  lines.forEach((line, n) => {
    const d = DEF_RE.exec(line);
    if (d) {
      if (!defs.has(d[1])) defs.set(d[1], { text: d[2].trim(), line: n });
      return;
    }
    for (const m of line.matchAll(MARK_RE)) {
      if (!first.has(m[1])) first.set(m[1], n);
    }
  });
  const entries = [];
  for (const [label, line] of first) {
    const def = defs.get(label);
    // num: Obsidian's running number for this footnote in reading view.
    entries.push({ label, text: def ? def.text : null, line, defLine: def ? def.line : null, num: entries.length + 1 });
  }
  for (const [label, def] of defs) {
    if (!first.has(label)) {
      entries.push({ label, text: def.text, line: def.line, defLine: def.line, orphan: true });
    }
  }
  return entries;
}

// Plain text only: nothing is rendered as markdown, so a note with thousands
// of footnotes costs a few MB.
class FootnoteListView extends ItemView {
  constructor(leaf) {
    super(leaf);
    this.file = null;
    this.entries = [];
    this.filter = "";
  }

  getViewType() {
    return VIEW_TYPE;
  }

  getDisplayText() {
    return "Footnote list";
  }

  getIcon() {
    return "list-ordered";
  }

  async onOpen() {
    const root = this.contentEl;
    root.empty();
    root.addClass("footnote-list-view");
    const input = root.createEl("input", {
      type: "search",
      placeholder: "Filter by label or text",
      cls: "footnote-list-filter",
    });
    input.addEventListener("input", () => {
      this.filter = input.value.trim();
      this.draw();
    });
    this.countEl = root.createDiv({ cls: "footnote-list-count" });
    this.listEl = root.createDiv({ cls: "footnote-list-items" });
    // Each part of a row goes where it lives in the file: the label to the
    // marker in the text, the note text to the definition.
    this.listEl.addEventListener("click", (e) => {
      const part = e.target.closest("[data-line]");
      if (part) this.jump(Number(part.dataset.line), part.dataset.num ? Number(part.dataset.num) : null);
    });

    const refresh = debounce(() => this.load(), 300, true);
    this.registerEvent(this.app.workspace.on("active-leaf-change", refresh));
    this.registerEvent(this.app.workspace.on("file-open", refresh));
    this.registerEvent(this.app.vault.on("modify", (f) => {
      if (this.file && f.path === this.file.path) refresh();
    }));
    await this.load();
  }

  // Follow the note in the most recent markdown tab; clicking into this
  // sidebar does not change it.
  async load() {
    const file = this.app.workspace.getActiveFile();
    if (!file || file.extension !== "md") return;
    this.file = file;
    this.entries = footnoteEntries(await this.app.vault.cachedRead(file));
    this.draw();
  }

  draw() {
    if (!this.listEl) return;
    const q = this.filter.toLowerCase();
    const shown = q
      ? this.entries.filter((e) => e.label.toLowerCase().startsWith(q) || (e.text || "").toLowerCase().includes(q))
      : this.entries;
    this.countEl.setText(
      this.file ? `${this.file.basename}: ${shown.length} of ${this.entries.length} footnotes` : ""
    );
    const frag = document.createDocumentFragment();
    for (const e of shown) {
      const row = frag.createDiv({ cls: "footnote-list-row" + (e.orphan ? " is-orphan" : "") });
      const label = row.createSpan({ cls: "footnote-list-label", text: e.label });
      label.dataset.line = String(e.line);
      label.setAttribute("aria-label", e.orphan ? "Go to definition (no marker)" : "Go to marker");
      const text = row.createSpan({
        cls: "footnote-list-text" + (e.text === null ? " is-missing" : ""),
        text: e.text === null ? "(no definition)" : e.text,
      });
      if (e.defLine !== null) {
        text.dataset.line = String(e.defLine);
        if (e.num) text.dataset.num = String(e.num);
        text.setAttribute("aria-label", "Go to definition");
      }
      if (e.orphan) row.title = "Defined but never marked in the text";
    }
    this.listEl.empty();
    this.listEl.appendChild(frag);
  }

  // Scroll the note to a line, in editing or reading view. num is the
  // footnote's running number when the target is its definition: reading
  // view draws every definition in one list at the bottom, not at its own
  // line, so the line only gets as far as that list and the entry itself is
  // found by number.
  jump(line, num) {
    if (!this.file) return;
    const leaf = this.app.workspace.getLeavesOfType("markdown")
      .find((l) => l.view instanceof MarkdownView && l.view.file && l.view.file.path === this.file.path);
    if (!leaf) return;
    this.app.workspace.setActiveLeaf(leaf, { focus: true });
    leaf.view.setEphemeralState({ line });
    if (leaf.view.getMode() === "source") {
      leaf.view.editor.setCursor({ line, ch: 0 });
    } else if (num) {
      this.revealItem(leaf.view.containerEl, num);
    }
  }

  // The list is drawn only once scrolled near, so wait for the entry briefly.
  revealItem(container, num, tries = 20) {
    const li = container.querySelector(`.markdown-reading-view li[data-footnote-id^="fn-${num}-"]`);
    if (!li) {
      if (tries > 0) window.setTimeout(() => this.revealItem(container, num, tries - 1), 100);
      return;
    }
    li.scrollIntoView({ block: "center" });
    li.removeClass("footnote-list-flash");
    void li.offsetWidth; // restart the animation on a repeat click
    li.addClass("footnote-list-flash");
  }
}

module.exports = class FootnoteList extends Plugin {
  async onload() {
    this.registerView(VIEW_TYPE, (leaf) => new FootnoteListView(leaf));
    this.addCommand({
      id: "open-footnote-list",
      name: "Open footnote list",
      callback: () => this.openList(),
    });
    this.addRibbonIcon("list-ordered", "Open footnote list", () => this.openList());
  }

  async openList() {
    let leaf = this.app.workspace.getLeavesOfType(VIEW_TYPE)[0];
    if (!leaf) {
      leaf = this.app.workspace.getRightLeaf(false);
      await leaf.setViewState({ type: VIEW_TYPE, active: true });
    }
    this.app.workspace.revealLeaf(leaf);
  }
};

module.exports.footnoteEntries = footnoteEntries;
