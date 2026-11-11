#!/bin/bash
# Rebuild every Vinaya draft (roots, aṭṭhakathā, ṭīkā) into 0-INBOX/temp/vinaya.
set -e
cd "$(dirname "$0")/../.."
./0-INBOX/raw-data/build_roots.sh >/dev/null
for i in 1 2 3 4 5; do
  j=$(sed -n "${i}p" <<< $'vin01m\nvin02m1\nvin02m2\nvin02m3\nvin02m4')
  python3 -B 4-SYSTEM/scripts/tipitaka-xml-to-json/fidelity_check.py 0-INBOX/raw-data/$j.json 0-INBOX/temp/vinaya/pi-$i.md
done
python3 -B 0-INBOX/raw-data/build_tika_json.py >/dev/null
P=0-INBOX/raw-data/build_commentary.py
while read b src name; do
  python3 -B $P $src $b $name 2>&1 | grep -v '^Wrote' | grep -v 'headings, deepest'
done <<'LIST'
1 vin01a pi-parajika-atthakatha
2 vin02a1 pi-pacittiya-atthakatha
3 vin02a2 pi-mahavagga-atthakatha
4 vin02a3 pi-culavagga-atthakatha
5 vin02a4 pi-parivara-atthakatha
1 parts/pi-parajika-saratthadipani pi-parajika-saratthadipani
2 parts/pi-pacittiya-saratthadipani pi-pacittiya-saratthadipani
3 parts/pi-mahavagga-saratthadipani pi-mahavagga-saratthadipani
4 parts/pi-culavagga-saratthadipani pi-culavagga-saratthadipani
5 parts/pi-parivara-saratthadipani pi-parivara-saratthadipani
1 parts/pi-parajika-vimativinodani pi-parajika-vimativinodani
2 parts/pi-pacittiya-vimativinodani pi-pacittiya-vimativinodani
3 parts/pi-mahavagga-vimativinodani pi-mahavagga-vimativinodani
4 parts/pi-culavagga-vimativinodani pi-culavagga-vimativinodani
5 parts/pi-parivara-vimativinodani pi-parivara-vimativinodani
1 parts/pi-parajika-vajirabuddhi pi-parajika-vajirabuddhi
2 parts/pi-pacittiya-vajirabuddhi pi-pacittiya-vajirabuddhi
3 parts/pi-mahavagga-vajirabuddhi pi-mahavagga-vajirabuddhi
4 parts/pi-culavagga-vajirabuddhi pi-culavagga-vajirabuddhi
5 parts/pi-parivara-vajirabuddhi pi-parivara-vajirabuddhi
2 parts/pi-pacittiya-yojana pi-pacittiya-yojana
3 parts/pi-mahavagga-yojana pi-mahavagga-yojana
4 parts/pi-culavagga-yojana pi-culavagga-yojana
5 parts/pi-parivara-yojana pi-parivara-yojana
LIST
