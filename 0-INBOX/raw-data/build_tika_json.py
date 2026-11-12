"""Split / merge the Vinaya ṭīkā JSONs into one JSON per (work, root book).

A part starts at a boundary segment (matched by its exact content); that
segment becomes the part's 'book' title. The first part keeps the file's own
homage / nikaya / book header. Output: 0-INBOX/raw-data/parts/<name>.json
"""
import json
from pathlib import Path

R = Path("0-INBOX/raw-data")
OUT = R / "parts"
OUT.mkdir(exist_ok=True)

# (sources, [(book, out_name, boundary content or None for "from start")])
PLAN = [
    (["vin01t1", "vin01t2"], [(1, "pi-parajika-saratthadipani", None)]),
    (["vin02t"], [
        (2, "pi-pacittiya-saratthadipani", None),
        (3, "pi-mahavagga-saratthadipani", "Mahāvagga-ṭīkā"),
        (4, "pi-culavagga-saratthadipani", "Cūḷavagga-ṭīkā"),
        (5, "pi-parivara-saratthadipani", "Parivāra-ṭīkā"),
    ]),
    (["vin07t"], [
        (1, "pi-parajika-vimativinodani", None),
        (2, "pi-pacittiya-vimativinodani", "Vimativinodanī-ṭīkā (dutiyo bhāgo)"),
        (3, "pi-mahavagga-vimativinodani", "Mahāvaggavaṇṇanā"),
        (4, "pi-culavagga-vimativinodani", "Cūḷavaggavaṇṇanā"),
        (5, "pi-parivara-vimativinodani", "Parivāravaṇṇanā"),
    ]),
    (["vin06t"], [
        (1, "pi-parajika-vajirabuddhi", None),
        (2, "pi-pacittiya-vajirabuddhi", "Pācittiyavaṇṇanā"),
        (3, "pi-mahavagga-vajirabuddhi", "Mahāvaggavaṇṇanā"),
        (4, "pi-culavagga-vajirabuddhi", "Cūḷavaggavaṇṇanā"),
        (5, "pi-parivara-vajirabuddhi", "Parivāravaṇṇanā"),
    ]),
    (["vin12t"], [
        (2, "pi-pacittiya-yojana", None),
        (3, "pi-mahavagga-yojana", "Mahāvaggayojanā"),
        (4, "pi-culavagga-yojana", "Cūḷavaggayojanā"),
        (5, "pi-parivara-yojana", "Parivāravaggayojanā"),
    ]),
]


def is_volume_header(seg, file_head):
    """Homage line, repeated piṭaka name, or repeated work title."""
    c = seg["content"]
    if c.startswith("Namo tassa bhagavato"):
        return True
    if c == "Vinayapiṭake":
        return True
    work_titles = {s["content"] for s in file_head if s["css_class"] == "book"}
    return seg["css_class"] == "title" and c in work_titles


def load(stem):
    return json.loads((R / f"{stem}.json").read_text(encoding="utf-8"))


def main():
    manifest = []
    for sources, parts in PLAN:
        datas = [load(s) for s in sources]
        base = dict(datas[0])
        segs, offset = [], 0
        for n, d in enumerate(datas):
            for s in d["segments"]:
                s = dict(s)
                s["chapter"] += offset
                if n > 0 and s["css_class"] == "nikaya":
                    s["css_class"] = "centered"   # volume 2+: repeated piṭaka name
                elif n > 0 and s["css_class"] == "book":
                    # volume 2+: the volume title is a line of text, not a
                    # division (tipitaka.app joins the volumes with no heading)
                    s["css_class"] = "centered"
                segs.append(s)
            offset = segs[-1]["chapter"] + 1
        # find boundaries
        idx = []
        for book, name, boundary in parts:
            if boundary is None:
                idx.append(0)
            else:
                hits = [i for i, s in enumerate(segs)
                        if s["content"] == boundary and s["css_class"] in ("chapter", "book")]
                assert len(hits) == 1, (name, boundary, hits)
                i = hits[0]
                # The next volume's header (homage, repeated piṭaka name,
                # repeated work title) is printed just before the boundary
                # heading: it opens the next part, not closes this one.
                while i > 0 and is_volume_header(segs[i - 1], segs[0:3]):
                    i -= 1
                idx.append(i)
        idx.append(len(segs))
        for k, (book, name, boundary) in enumerate(parts):
            part = segs[idx[k]:idx[k + 1]]
            if boundary is not None:
                j = next(n for n, s in enumerate(part) if s["content"] == boundary
                         and s["css_class"] in ("chapter", "book"))
                head = part[:j]              # homage [+ piṭaka name] [+ work title]
                # Every part opens with the homage (^T-1), as every Abhidhamma
                # commentary part does (abhidhamma-rails pi-4 … pi-7 reports:
                # "homage line ^T-1 at the top of the ṭīkās"). A single-volume
                # work (vin06t Vajirabuddhi) prints it only once, at the start:
                # the later parts get it here, as they get the piṭaka line.
                homage = [s for s in head if s["content"].startswith("Namo tassa")] or [
                    {"id": "synthetic_homage", "chapter": part[j]["chapter"],
                     "paragraph": "k0", "content": "Namo tassa bhagavato arahato sammāsambuddhassa",
                     "css_class": "centered", "synthetic": True}]
                pitaka = [dict(s, css_class="nikaya") for s in head
                          if s["content"] == "Vinayapiṭake"][:1] or [
                    {"id": "synthetic_nikaya", "chapter": part[j]["chapter"],
                     "paragraph": "k0", "content": "Vinayapiṭake",
                     "css_class": "nikaya", "synthetic": True}]
                work = [s for s in head if s["css_class"] == "title"]
                if work:
                    # repeated work title (vin12t 'Pācityādiyojanā'): it heads
                    # the part, with the boundary as its first division -- the
                    # same shape as the work's first part
                    part = (homage + pitaka + [dict(work[0], css_class="book")]
                            + [dict(part[j], css_class="chapter")] + part[j + 1:])
                else:
                    part = homage + pitaka + [dict(part[j], css_class="book")] + part[j + 1:]
            title = next(s["content"] for s in part if s["css_class"] == "book")
            ids = "+".join(sources)
            d = dict(base, segments=part, total_segments=len(part),
                     title_pali=title,
                     title_breadcrumb=f"Tīkā > Vinayapiṭaka (ṭīkā) > {title}",
                     id=ids, source_parts=sources,
                     source_filename="+".join(f"book/{s}.{d0['layer_type']}.html" for s, d0 in zip(sources, datas)))
            d.pop("full_text", None)
            (OUT / f"{name}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
            manifest.append((name, book, len(part)))
    for m in manifest:
        print(*m)


if __name__ == "__main__":
    main()
