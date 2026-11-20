"""List XML headings that tipitaka.app shows as headings in its content view
but leaves out of its contents tree, and say how the vault holds each one.

usage: python titles_not_in_site_toc.py
"""
import re, sys, json, difflib
import xml.etree.ElementTree as ET
sys.stdout.reconfigure(encoding="utf-8")
XML = r"D:\Work\OpenPecha\tipitaka-xml\romn"
FILES = [("pi-1", "vin01m.mul.xml", "vp-prj"), ("pi-2", "vin02m1.mul.xml", "vp-pct"),
         ("pi-3", "vin02m2.mul.xml", "vp-mv"), ("pi-4", "vin02m3.mul.xml", "vp-cv"),
         ("pi-5", "vin02m4.mul.xml", "vp-pv")]
HEAD_RENDS = {"title", "chapter", "subhead", "subsubhead"}

def inner(el):
    s = el.text or ""
    for ch in el:
        if ch.tag == "note":
            s += "{" + inner(ch) + "}"
        elif ch.tag != "pb":
            s += inner(ch)
        s += ch.tail or ""
    return re.sub(r"\s+", " ", s).strip()

def norm(t):
    return re.sub(r"\s+", " ", t.replace("‘‘", '"').replace("’’", '"')).strip()

for vid, xf, site in FILES:
    root = ET.parse(f"{XML}\\{xf}").getroot()
    heads = []
    def walk(el, ctx):
        for ch in el:
            if ch.tag == "div":
                walk(ch, ctx + [ch.get("id")])
            elif ch.tag == "head" and ch.get("rend") != "book" or (ch.tag == "p" and ch.get("rend") in HEAD_RENDS):
                heads.append((inner(ch), ch.tag, ch.get("rend"), "/".join(ctx)))
            else:
                walk(ch, ctx)
    walk(root.find(".//body"), [])
    tree = json.load(open(f"0-INBOX/tipitaka-app/{site}.json", encoding="utf-8"))
    st = [norm(n["title"]) for n in tree]
    xt = [norm(h[0]) for h in heads]
    md = open(f"1-SOURCES/Text/{vid}.md", encoding="utf-8").read()
    sm = difflib.SequenceMatcher(None, xt, st, autojunk=False)
    missing = [i for t, i1, i2, j1, j2 in sm.get_opcodes() if t in ("delete", "replace") for i in range(i1, i2)]
    extra = [j for t, i1, i2, j1, j2 in sm.get_opcodes() if t in ("insert", "replace") for j in range(j1, j2)]
    print(f"== {vid} ({xf} vs {site}): XML headings {len(xt)}, site tree {len(st)}, XML-only {len(missing)}, site-only {len(extra)}")
    for i in missing:
        text, tag, rend, ctx = heads[i]
        m = re.search(r"^(#*)\s*(\*\*)?" + re.escape(text) + r"(\*\*)?\s*(\^[\w-]+)?\s*$", md, flags=re.M)
        if m:
            ln = md[:m.start()].count("\n") + 1
            how = f"vault line {ln}: " + ("heading " + m.group(1) if m.group(1) else "text line") + f" {m.group(4) or ''}"
        else:
            how = "not found as a whole line in the vault"
        prev = xt[i - 1] if i else ""
        print(f"  - <{tag} rend={rend}> `{text}` in div {ctx or '(book)'}; after `{prev[:40]}` → {how}")
    for j in extra:
        print(f"  + site-only node `{st[j]}` ({tree[j]['key']})")
