"""Cut one book's part out of a CST XML file that holds several (e.g. vin06t.nrf.xml
holds the Vajirabuddhi on all five Vinaya books), so the comparison scripts can be
run on just that part.

The slice runs from the first block (head / p / trailer) whose text equals FROM
up to, not including, the first later block whose text equals TO (or to the end).
<div> ancestors are rebuilt around the kept blocks, so heading depths survive.

usage: python slice_xml.py <in.xml> <out.xml> --from "text" [--to "text" [--to-nth N]] [--prepend N]
  --to-nth N    stop at the Nth block after FROM whose text equals TO (default 1)
  --prepend-idx I,J   keep these 0-based blocks from the file start instead (e.g. 1 = only the nikaya title)
  --prepend N   also keep the first N blocks of the file (e.g. 2 = the homage line
                and the nikaya title, which the vault repeats at the top of every part)
"""
import re, sys, copy
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding="utf-8")
args, opts, i = [], {}, 1
while i < len(sys.argv):
    if sys.argv[i].startswith("--"):
        opts[sys.argv[i]] = sys.argv[i + 1]; i += 2
    else:
        args.append(sys.argv[i]); i += 1
src, dst = args

def txt(el):
    s = el.text or ""
    for c in el:
        if c.tag not in ("note", "pb"):
            s += txt(c)
        s += c.tail or ""
    return re.sub(r"\s+", " ", s).strip()

root = ET.parse(src).getroot()
body = root.find(".//body")
blocks = []   # (element, [ancestor divs])
def walk(el, chain):
    for ch in el:
        if ch.tag == "div":
            walk(ch, chain + [ch])
        elif ch.tag in ("head", "p", "trailer"):
            blocks.append((ch, chain))
        else:
            walk(ch, chain)
walk(body, [])

start = next(k for k, (b, _) in enumerate(blocks) if txt(b) == opts["--from"])
end = len(blocks)
if "--to" in opts:
    hits = [k for k in range(start + 1, len(blocks)) if txt(blocks[k][0]) == opts["--to"]]
    end = hits[int(opts.get("--to-nth", 1)) - 1]   # --to-nth N: stop at the Nth later match
pre = list(range(int(opts.get("--prepend", 0))))
if "--prepend-idx" in opts:   # comma-separated 0-based block indices, e.g. "1" = only the nikaya title
    pre = [int(v) for v in opts["--prepend-idx"].split(",")]
keep = pre + list(range(start, end))

new_body = ET.Element("body")
stack = []   # [(orig_div, new_div)]
for k in keep:
    el, chain = blocks[k]
    n = 0
    while n < len(stack) and n < len(chain) and stack[n][0] is chain[n]:
        n += 1
    del stack[n:]
    for d in chain[n:]:
        parent = stack[-1][1] if stack else new_body
        nd = ET.SubElement(parent, "div", d.attrib)
        stack.append((d, nd))
    (stack[-1][1] if stack else new_body).append(copy.deepcopy(el))

out = ET.Element(root.tag, root.attrib)
text = ET.SubElement(out, "text")
text.append(new_body)
ET.ElementTree(out).write(dst, encoding="utf-8", xml_declaration=True)
print(f"kept {len(keep)} of {len(blocks)} blocks: '{txt(blocks[start][0])}' … '{txt(blocks[end - 1][0])[:60]}'")
