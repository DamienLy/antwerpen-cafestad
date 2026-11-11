#!/usr/bin/env bash
# Bouwt de kaart opnieuw: van ruwe gegevens naar docs/index.html
set -e
cd "$(dirname "$0")"
python3 geo.py        # cafés + coördinaten -> data.json
python3 blurbs.py     # buurt per café
python3 texts.py      # beschrijving + filterlabels per café
python3 poster.py     # posterposities voor het tabblad Poster <-> kaart
python3 osm.py        # OpenStreetMap-ondergrond -> osm.json
PYTHONHASHSEED=0 python3 route.py      # lijnen langs de straten -> routes.json (nodig: pip install networkx scipy numpy)
python3 build.py      # alles in de sjabloonpagina -> site.html
cp site.html ../docs/index.html
cp data.json ../data/cafes.json
cp osm.json ../data/basemap.json
rm -f data.json osm.json routes.json site.html antwerpen-cafestad.html
echo "Klaar: docs/index.html is bijgewerkt"
