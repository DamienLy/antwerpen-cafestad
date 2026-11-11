"""Haalt echte OpenStreetMap-data op (draait in GitHub Actions, die wel internet hebben).
- data/osm_pois.json: alle cafés/bars in Antwerpen met coördinaten -> om onze cafés exact te plaatsen
- data/basemap.json: straten, water en parken voor de achtergrondkaart"""
import json, urllib.request, urllib.parse
URL = "https://overpass-api.de/api/interpreter"
BBOX = "51.180,4.360,51.250,4.470"
def q(query):
    data = urllib.parse.urlencode({"data": query}).encode()
    req = urllib.request.Request(URL, data=data, headers={"User-Agent": "antwerpen-cafestad/1.0"})
    return json.load(urllib.request.urlopen(req, timeout=180))
pois = q(f'[out:json][timeout:120];nwr["amenity"~"^(bar|pub|cafe|restaurant|biergarten|nightclub)$"]["name"]({BBOX});out center tags;')
json.dump([{"name": e["tags"]["name"], "lat": e.get("lat", e.get("center", {}).get("lat")), "lon": e.get("lon", e.get("center", {}).get("lon")),
            "street": e["tags"].get("addr:street", ""), "nr": e["tags"].get("addr:housenumber", "")} for e in pois["elements"]],
          open("data/osm_pois.json", "w"), ensure_ascii=False)
base = q(f'[out:json][timeout:180];(way["highway"~"^(primary|secondary|tertiary|pedestrian|residential)$"]({BBOX});'
         f'way["natural"="water"]({BBOX});way["waterway"="riverbank"]({BBOX});way["leisure"="park"]({BBOX}););out geom;')
json.dump([{"t": ("water" if e["tags"].get("natural") == "water" or "waterway" in e["tags"] else "park" if e["tags"].get("leisure") else e["tags"].get("highway")),
            "n": e["tags"].get("name", ""), "g": [[round(p["lat"], 5), round(p["lon"], 5)] for p in e.get("geometry", [])]} for e in base["elements"]],
          open("data/basemap.json", "w"), ensure_ascii=False)
print(len(pois["elements"]), "pois,", len(base["elements"]), "basemap ways")
