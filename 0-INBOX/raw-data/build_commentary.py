"""Build one Vinaya commentary draft: converter -> structure pass -> block IDs -> fidelity check.
Usage: build_commentary.py <json-stem> <book> <out-name> [title]"""
import sys, re, json, types, pathlib, subprocess
stem, book, outname = sys.argv[1], int(sys.argv[2]), sys.argv[3]
root = f"1-SOURCES/Text/pi-{book}.md"
draft_root = pathlib.Path(f"0-INBOX/temp/vinaya/pi-{book}.md")
ids = set(re.findall(r"\^(\S+)\s*$", draft_root.read_text(encoding="utf-8"), re.M))
src = pathlib.Path("4-SYSTEM/Skills/json-to-commentary/scripts/converters/tipitaka_org_atthakatha.py").read_bytes().rstrip(b"\x00").decode()
mod = types.ModuleType("conv"); exec(compile(src, "conv", "exec"), mod.__dict__)
mod.ROOT_TEXT_PATH, mod.BOOK_ID, mod.KEEP_REF_NUMBER, mod.ROOT_IDS, mod.H3_FIRST_HEADING = root, book, True, ids, True
jpath = f"0-INBOX/raw-data/{stem}.json"
chs = {s["chapter"] for s in json.load(open(jpath))["segments"]}
out = f"0-INBOX/temp/vinaya/{outname}.md"
mod.convert_json_to_commentary(jpath, out, chapter_context={c: "main" for c in chs})
S = "4-SYSTEM/scripts/tipitaka-xml-to-json"
subprocess.run(["python3", "-B", f"{S}/vinaya_structure.py", out, jpath], check=True)
SITE = {"atthakatha": "atta-vp-{b}", "saratthadipani": "tika-vp-{b2}", "vajirabuddhi": "tika-vajirabuddhi-tika",
        "vimativinodani": "tika-vimativinodani-tika", "yojana": "tika-pacityadiyojanapali"}
slug, work = re.match(r"pi-([a-z]+)-([a-z]+)$", outname).groups()
bk = {"parajika": "prj", "pacittiya": "pct", "mahavagga": "mv", "culavagga": "cv", "parivara": "pv"}[slug]
site = SITE[work].format(b=bk, b2="prj" if bk == "prj" else "pct")
subprocess.run(["python3", "-B", f"{S}/apply_site_toc.py", out, f"0-INBOX/tipitaka-app/{site}.json"], check=True)
subprocess.run(["python3", "-B", "4-SYSTEM/Skills/add-block-id-commentary/apply.py", "apply", out], check=True, stdout=subprocess.DEVNULL)
subprocess.run(["python3", "-B", f"{S}/fidelity_check.py", jpath, out])
txt = pathlib.Path(out).read_text(encoding="utf-8")
print(f"  transclusions={txt.count('![[')} unresolved={len(mod.UNRESOLVED)}")
pathlib.Path(out.replace(".md", ".unresolved.json")).write_text(json.dumps(mod.UNRESOLVED, ensure_ascii=False, indent=1), encoding="utf-8")
