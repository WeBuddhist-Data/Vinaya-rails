// Footnote labels: Obsidian renumbers footnotes 1, 2, 3 in reading view, in
// order of first reference, and drops the label written in the file. This
// puts the label back on each entry of the footnote list at the bottom
// (li[data-footnote-id="fn-<N>-<hash>"]) as data-footlabel, which styles.css
// draws. It never moves an entry: the order is Obsidian's own. The in-text
// markers keep data-footref themselves and are styled by
// snippets/footnote-kinds.css. The sidebar list is a separate plugin,
// footnote-list.

const { Plugin, TFile } = require("obsidian");

const DEF_RE = /^\[\^([^\]\s]+)\]:/;
const MARK_RE = /\[\^([^\]\s]+)\]/g;
const LINE_RE = /\r?\n/;
const ITEM_SEL = "li[data-footnote-id]";

// Labels in the order Obsidian numbers them: first reference in the body,
// definition lines skipped. refs[N - 1] is the label of footnote N.
function footnoteOrder(source) {
  const refs = [];
  const seen = new Set();
  for (const line of source.split(LINE_RE)) {
    if (DEF_RE.test(line)) continue;
    for (const m of line.matchAll(MARK_RE)) {
      if (!seen.has(m[1])) {
        seen.add(m[1]);
        refs.push(m[1]);
      }
    }
  }
  return refs;
}

function labelItem(li, refs) {
  const m = /^fn-(\d+)-/.exec(li.getAttribute("data-footnote-id") || "");
  const label = m && refs[Number(m[1]) - 1];
  if (!label) return;
  li.setAttribute("data-footlabel", label);
  // CSS attr() reads the element's own attribute, and the label is drawn
  // before the entry's first paragraph, so it needs the label too.
  const p = li.querySelector(":scope > p");
  if (p) p.setAttribute("data-footlabel", label);
}

function itemsIn(node) {
  if (!(node instanceof HTMLElement)) return [];
  if (node.matches(ITEM_SEL)) return [node];
  return Array.from(node.querySelectorAll(ITEM_SEL));
}

module.exports = class FootnoteLabels extends Plugin {
  async onload() {
    this.cache = new Map(); // path -> { mtime, order }

    this.registerMarkdownPostProcessor(async (el, ctx) => {
      const items = itemsIn(el);
      if (!items.length || !ctx.sourcePath) return;
      const order = await this.orderFor(ctx.sourcePath);
      if (order) items.forEach((li) => labelItem(li, order));
    });

    // The footnote list is not always handed to post-processors, so also
    // catch it when it is added to a markdown view.
    const observer = new MutationObserver((mutations) => {
      for (const mu of mutations) {
        for (const node of mu.addedNodes) {
          const items = itemsIn(node);
          if (items.length) this.labelInView(items);
        }
      }
    });
    observer.observe(document.body, { childList: true, subtree: true });
    this.register(() => observer.disconnect());

    this.app.workspace.onLayoutReady(() => {
      this.labelInView(Array.from(document.querySelectorAll(ITEM_SEL)));
    });
  }

  async labelInView(items) {
    const leaves = this.app.workspace.getLeavesOfType("markdown");
    for (const leaf of leaves) {
      const file = leaf.view && leaf.view.file;
      if (!file) continue;
      const mine = items.filter((li) => leaf.view.containerEl.contains(li));
      if (!mine.length) continue;
      const order = await this.orderFor(file.path);
      if (order) mine.forEach((li) => labelItem(li, order));
    }
  }

  async orderFor(path) {
    const file = this.app.vault.getAbstractFileByPath(path);
    if (!(file instanceof TFile)) return null;
    const hit = this.cache.get(path);
    if (hit && hit.mtime === file.stat.mtime) return hit.order;
    const order = footnoteOrder(await this.app.vault.cachedRead(file));
    this.cache.set(path, { mtime: file.stat.mtime, order });
    return order;
  }
};

module.exports.footnoteOrder = footnoteOrder;
