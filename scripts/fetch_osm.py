"""Haalt alle cafés/bars in Antwerpen uit OpenStreetMap, met openingsuren (draait in GitHub Actions, die wel internet hebben).
Schrijft data/osm_pois.json. Daarna koppelt scripts/hours.py die aan onze cafés."""
import json, time, urllib.request, urllib.parse
URLS = ["https://overpass-api.de/api/interpreter", "https://overpass.kumi.systems/api/interpreter", "https://maps.mail.ru/osm/tools/overpass/api/interpreter"]
BBOX = "51.180,4.360,51.250,4.470"
QUERY = f'[out:json][timeout:120];nwr["amenity"~"^(bar|pub|cafe|restaurant|biergarten|nightclub)$"]["name"]({BBOX});out center tags;'

def q(query):
    last = None
    for url in URLS:
        for attempt in range(2):
            try:
                data = urllib.parse.urlencode({"data": query}).encode()
                req = urllib.request.Request(url, data=data, headers={"User-Agent": "cafekaart-antwerpen/1.0 (github.com)"})
                return json.load(urllib.request.urlopen(req, timeout=180))
            except Exception as e:
                last = e; print("mislukt:", url, e); time.sleep(10)
    raise last

pois = q(QUERY)
out = []
for e in pois["elements"]:
    t = e["tags"]
    out.append({"name": t["name"], "amenity": t.get("amenity", ""),
                "lat": e.get("lat", e.get("center", {}).get("lat")), "lon": e.get("lon", e.get("center", {}).get("lon")),
                "street": t.get("addr:street", ""), "nr": t.get("addr:housenumber", ""),
                "hours": t.get("opening_hours", ""), "website": t.get("website", t.get("contact:website", ""))})
json.dump(out, open("data/osm_pois.json", "w"), ensure_ascii=False, indent=0)
print(len(out), "zaken,", sum(1 for o in out if o["hours"]), "met openingsuren")
