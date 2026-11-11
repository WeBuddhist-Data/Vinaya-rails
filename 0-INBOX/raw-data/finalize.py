"""Write final frontmatter on the Vinaya drafts and copy them into 1-SOURCES.

Frontmatter mirrors the Abhidhamma vault's 1-SOURCES files. Library IDs
(category_id, tag_ids, text_id, edition_id, toc_id, commentary_of) are left
out: they are assigned by the library upload, which has not happened.
"""
import json
import re
import shutil
from pathlib import Path

T = Path("0-INBOX/temp/vinaya")
R = Path("0-INBOX/raw-data")
XML = "https://github.com/VipassanaTech/tipitaka-xml/blob/main/romn"

ROOTS = {1: "vin01m", 2: "vin02m1", 3: "vin02m2", 4: "vin02m3", 5: "vin02m4"}
BOOK = {1: ("parajika", "Pārājika"), 2: ("pacittiya", "Pācittiya"),
        3: ("mahavagga", "Mahāvagga"), 4: ("culavagga", "Cūḷavagga"),
        5: ("parivara", "Parivāra")}
WORK = {
    "atthakatha": ("Samantapāsādikā", "atthakatha"),
    "saratthadipani": ("Sāratthadīpanī-ṭīkā", "tika"),
    "vimativinodani": ("Vimativinodanī-ṭīkā", "tika"),
    "vajirabuddhi": ("Vajirabuddhi-ṭīkā", "tika"),
    "yojana": ("Pācityādiyojanā", "other"),
}
ATT = {1: "vin01a", 2: "vin02a1", 3: "vin02a2", 4: "vin02a3", 5: "vin02a4"}


def q(v):
    v = str(v)
    return f'"{v}"' if any(c in v for c in ':#[]\'"') else v


def fm(d):
    out = ["---"]
    for k, v in d.items():
        if isinstance(v, list):
            out.append(f"{k}:")
            out += [f"  - {x}" for x in v]
        else:
            out.append(f"{k}: {q(v)}")
    out.append("---")
    return "\n".join(out) + "\n"


def set_frontmatter(path, meta):
    text = path.read_text(encoding="utf-8")
    body = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S)
    path.write_text(fm(meta) + body, encoding="utf-8")


def content_ids(path, book):
    return [int(m) for m in re.findall(rf"\^{book}-(\d+)\s*$", path.read_text(encoding="utf-8"), re.M) if m != "0"]


def segs_count(stem):
    return json.loads((R / f"{stem}.json").read_text(encoding="utf-8"))["total_segments"]


def main():
    Path("1-SOURCES/Text").mkdir(parents=True, exist_ok=True)
    Path("1-SOURCES/Commentaries").mkdir(parents=True, exist_ok=True)
    for b, stem in ROOTS.items():
        p = T / f"pi-{b}.md"
        title = json.loads((R / f"{stem}.json").read_text(encoding="utf-8"))["title_pali"]
        ids = content_ids(p, b)
        set_frontmatter(p, {
            "title": title, "language": "Pali", "script": "Roman (PTS diacritics)",
            "file_type": "root-text", "lang_tag": "pi", "verse_id_format": "book-verse",
            "pitaka": "vinaya", "layer": "mula", "copyright": "Public domain", "license": "cc0",
            "source_description": f"Chaṭṭha Saṅgāyana Tipiṭaka (CST) romanised XML, VipassanaTech/tipitaka-xml romn/{stem}.mul.xml. Mūla > Vinayapiṭaka > {title}; {segs_count(stem)} segments in source; paragraphs {min(ids)}–{max(ids)}.",
            "source_filename": f"romn/{stem}.mul.xml",
            "source": f"{XML}/{stem}.mul.xml",
            "other_ids": [f"tipitaka.org: {stem}"],
        })
        shutil.copy(p, f"1-SOURCES/Text/pi-{b}.md")
        print("root", p.name, title, len(ids))
    for p in sorted(T.glob("pi-*-*.md")):
        slug, work = re.match(r"pi-([a-z]+)-([a-z]+)\.md", p.name).groups()
        b = next(k for k, v in BOOK.items() if v[0] == slug)
        wname, layer = WORK[work]
        if work == "atthakatha":
            stem = ATT[b]
            srcs = [stem]
            data = json.loads((R / f"{stem}.json").read_text(encoding="utf-8"))
        else:
            data = json.loads((R / "parts" / f"{p.stem}.json").read_text(encoding="utf-8"))
            srcs = data["source_parts"]
        ext = data["layer_type"]
        text = p.read_text(encoding="utf-8")
        cited = sorted({int(m) for m in re.findall(rf"!\[\[1-SOURCES/Text/pi-{b}\.md#\^{b}-(\d+)\]\]", text)})
        title = f"{wname} ({BOOK[b][1]})"
        meta = {
            "title": title, "language": "Pali", "script": "Roman (PTS diacritics)",
            "file_type": "commentary", "registered_id": f"{slug}-{work}", "lang_tag": "pi",
            "verse_id_format": "book-verse", "pitaka": "vinaya", "layer": layer,
            "root_text": f"1-SOURCES/Text/pi-{b}.md",
            "covers_verses": f"{b}-{cited[0]}–{b}-{cited[-1]}" if cited else "",
            "copyright": "Public domain", "license": "cc0",
            "source_description": f"Chaṭṭha Saṅgāyana Tipiṭaka (CST) romanised XML, VipassanaTech/tipitaka-xml {', '.join(f'romn/{s}.{ext}.xml' for s in srcs)}"
                                  + ("" if work == "atthakatha" and b == 1 or len(srcs) > 1 or work == "atthakatha" else f" — the part commenting on {BOOK[b][1]}")
                                  + f"; {data['total_segments']} segments; root citations linked by printed paragraph number.",
            "source_filename": ", ".join(f"romn/{s}.{ext}.xml" for s in srcs),
            "source": f"{XML}/{srcs[0]}.{ext}.xml",
            "other_ids": [f"tipitaka.org: {s}" for s in srcs],
        }
        if not cited:
            meta.pop("covers_verses")
        set_frontmatter(p, meta)
        shutil.copy(p, f"1-SOURCES/Commentaries/{p.name}")
        print("comm", p.name, title, len(cited))


if __name__ == "__main__":
    main()
