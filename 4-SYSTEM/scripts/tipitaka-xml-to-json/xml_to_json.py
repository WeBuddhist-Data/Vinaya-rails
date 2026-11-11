#!/usr/bin/env python3
"""Convert a VipassanaTech/tipitaka-xml (CST romn) file into the tipitaka.org
book-export JSON schema consumed by json-to-source-text / json-to-commentary.

Usage: xml_to_json.py <in.xml> <out.json> --title T --breadcrumb B --pitaka P
       --layer {mula,atthakatha,tika,other} --fts N
"""
import argparse, json, re, html, pathlib

HEADER_CLASSES = {"centered", "nikaya", "book"}
REND_MAP = {"centre": "centered"}
P_RE = re.compile(r'<(p|head|trailer)\b([^>]*)>(.*?)</\1>', re.S)

def clean(inner: str) -> str:
    s = re.sub(r'<pb\b[^>]*/>', ' ', inner)
    s = re.sub(r'<note>(.*?)</note>', lambda m: '[' + m.group(1).strip() + ']', s, flags=re.S)
    s = re.sub(r'<[^>]+>', '', s)
    s = html.unescape(s)
    s = s.replace('‘‘', '"').replace('’’', '"')  # match tipitaka.org exports
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r'^(\d+(?:-\d+)?) \.', r'\1.', s)  # "199 ." typo in CST markup
    return s

def convert(xml_path, out_path, title, breadcrumb, pitaka, layer, fts):
    raw = pathlib.Path(xml_path).read_bytes()
    text = raw.decode('utf-16') if raw[:2] in (b'\xff\xfe', b'\xfe\xff') else raw.decode('utf-8')
    stem = pathlib.Path(xml_path).name.split('.')[0]
    ltype = pathlib.Path(xml_path).name.split('.')[1]
    segs, chapter, k, has_body = [], 0, 0, False
    full, pos = [], 0
    pending_num = None  # a <p rend="hangnum">N.</p> waiting for its verse
    for m in P_RE.finditer(text):
        attrs = m.group(2)
        r = re.search(r'rend="([^"]+)"', attrs)
        rend = r.group(1) if r else m.group(1)
        content = clean(m.group(3))
        if not content:
            continue
        if rend == 'hangnum':
            # A hanging paragraph number printed on its own line before a
            # gāthā: carry it onto the next paragraph as its leading "N. ".
            pending_num = content
            continue
        if pending_num:
            content = f"{pending_num} {content}"
            pending_num = None
        css = REND_MAP.get(rend, rend)
        mid_book = False
        if css == 'book' and segs and any(s['css_class'] == 'chapter' for s in segs):
            # A second book title inside the file (e.g. Bhikkhunīvibhaṅgo in
            # vin02m1) opens a new top-level division: keep it as a heading,
            # flagged so vinaya_structure.py can nest what follows it.
            css = 'chapter'
            mid_book = True
        if css == 'nikaya' and any(s['css_class'] == 'chapter' for s in segs):
            # Repeated piṭaka name at the start of a second volume.
            css = 'centered'
        if css == 'chapter' and has_body:
            chapter += 1; k = 0; has_body = False
        if css not in HEADER_CLASSES and css != 'chapter':
            has_body = True
        k += 1
        seg = {
            "id": f"{stem}_ch{chapter}_k{k}", "chapter": chapter, "paragraph": f"k{k}",
            "span_start": pos, "span_end": pos + len(content), "content": content,
            "css_class": css, "original_path": f"{fts}@{stem}.{ltype}{chapter}@k{k}",
        }
        if mid_book:
            seg["mid_book"] = True
        segs.append(seg)
        full.append(content); pos += len(content) + 1
    data = {"id": stem, "title_pali": title, "title_breadcrumb": breadcrumb,
            "collection": pitaka, "pitaka": pitaka, "layer": layer, "layer_type": ltype,
            "fts_prefix": str(fts), "source_filename": f"book/{stem}.{ltype}.html",
            "total_segments": len(segs), "total_characters": len("\n".join(full)),
            "full_text": "\n".join(full), "segments": segs}
    pathlib.Path(out_path).write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')
    return data

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('xml'); ap.add_argument('out')
    ap.add_argument('--title', required=True); ap.add_argument('--breadcrumb', required=True)
    ap.add_argument('--pitaka', required=True); ap.add_argument('--layer', required=True)
    ap.add_argument('--fts', required=True)
    a = ap.parse_args()
    d = convert(a.xml, a.out, a.title, a.breadcrumb, a.pitaka, a.layer, a.fts)
    print(f"{a.out}: {d['total_segments']} segments")
