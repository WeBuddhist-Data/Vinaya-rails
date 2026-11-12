#!/bin/bash
# Rebuild the five Vinaya root-text drafts from tipitaka-xml.
set -e
cd "$(dirname "$0")/../.."
T=0-INBOX/temp/vinaya; mkdir -p $T
python3 -B 0-INBOX/raw-data/build_json.py
KEYS=(x vp-prj vp-pct vp-mv vp-cv vp-pv)
i=1
for n in vin01m vin02m1 vin02m2 vin02m3 vin02m4; do
  python3 -B 4-SYSTEM/Skills/json-to-source-text/converters/tipitaka_org_book.py 0-INBOX/raw-data/$n.json $T/pi-$i.md 2>/dev/null
  python3 -B 4-SYSTEM/scripts/tipitaka-xml-to-json/vinaya_structure.py $T/pi-$i.md 0-INBOX/raw-data/$n.json
  python3 -B 4-SYSTEM/scripts/tipitaka-xml-to-json/apply_site_toc.py $T/pi-$i.md 0-INBOX/tipitaka-app/${KEYS[$i]}.json
  L=$(grep -n '^## ' $T/pi-$i.md | head -1 | cut -d: -f1)
  python3 -B 4-SYSTEM/Skills/add-block-id-root-text/apply.py apply $T/pi-$i.md --zones "1=@$L" >/dev/null
  python3 -B 4-SYSTEM/scripts/tipitaka-xml-to-json/heading_ids.py $T/pi-$i.md $i
  # last: the source's printed form (numbers, piṭaka heading, {notes})
  python3 -B 4-SYSTEM/scripts/tipitaka-xml-to-json/source_form.py $T/pi-$i.md 0-INBOX/raw-data/$n.json
  i=$((i+1))
done
