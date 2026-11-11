"""Fetch a book's full text and its cross-layer links from tipitaka.app.
Usage: fetch_text.py <key> [<key> ...]   e.g. vp-prj atta-vp-prj
Writes 0-INBOX/tipitaka-app/text/<key>.json and links/<key>.json."""
import json, sys, time, urllib.request
from pathlib import Path
V = "7d17987e5be3e268"
OUT = Path("0-INBOX/tipitaka-app")
def get(path):
    req = urllib.request.Request(f"https://tipitaka.app/api/{path}&v={V}", headers={"User-Agent": "rails-toc-check"})
    return json.load(urllib.request.urlopen(req, timeout=60))
for key in sys.argv[1:]:
    first = get(f"text?key={key}&from=0&to=150")
    n = first["book"]["paraCount"]
    paras, links = list(first["paras"]), []
    for start in range(150, n, 150):
        paras += get(f"text?key={key}&from={start}&to={start+150}")["paras"]; time.sleep(0.2)
    for start in range(0, n, 150):
        links += get(f"links?key={key}&from={start}&to={start+150}"); time.sleep(0.2)
    for sub in ("text", "links"):
        (OUT / sub).mkdir(exist_ok=True)
    (OUT / "text" / f"{key}.json").write_text(json.dumps({"book": first["book"], "paras": paras}, ensure_ascii=False, indent=0), encoding="utf-8")
    (OUT / "links" / f"{key}.json").write_text(json.dumps(links, ensure_ascii=False, indent=0), encoding="utf-8")
    print(key, "paras", len(paras), "of", n, "links", len(links))
