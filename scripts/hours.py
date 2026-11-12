"""Openingsuren per café in data.json (s['o'], OpenStreetMap-notatie).
Bronnen, beste eerst:
1. hours_src/schlouk.json  - Schlouk Map, per café nagekeken op naam én adres (opgehaald via de GitHub-workflow 'Pagina's ophalen')
2. data/osm_pois.json      - OpenStreetMap, dichtstbijzijnde zaak met dezelfde naam binnen 150 m (workflow 'Openingsuren verversen')"""
import json, math, re, unicodedata, sys, os
osm_src = sys.argv[1] if len(sys.argv) > 1 else '../data/osm_pois.json'
d = json.load(open('data.json'))
def core(s):
    w = [x for x in re.split(r"[^a-z0-9]+", unicodedata.normalize('NFKD', s.lower()).encode('ascii', 'ignore').decode())
         if x and x not in ['cafe', 'bar', 'taproom', 'pub', 'de', 'het', 't', 'in', 'irish']]
    return ''.join(w)
def dist(a, b, c, e): return math.hypot((b - e) * 111320 * math.cos(math.radians(a)), (a - c) * 110540)
sch = {}
if os.path.exists('hours_src/schlouk.json'):
    for r in json.load(open('hours_src/schlouk.json')).values():
        if r.get('cafe') and re.search(r'\d\d:\d\d', r['hours']) and not re.search(r'[ap]m', r['hours']): sch[r['cafe']] = r['hours']
pois = json.load(open(osm_src)) if os.path.exists(osm_src) else []
src = {'schlouk': 0, 'osm': 0}
for s in d['stations']:
    s.pop('o', None); s.pop('os', None)
    if s['n'] in sch:
        s['o'] = sch[s['n']]; s['os'] = 'Schlouk Map'; src['schlouk'] += 1; continue
    best = None
    for p in pois:
        if p.get('lat') is None or not p.get('hours'): continue
        m = dist(s['lat'], s['lon'], p['lat'], p['lon'])
        if m > 150: continue
        a, b = core(s['n']), core(p['name'])
        if (a == b or (len(a) >= 4 and (a in b or b in a))) and (best is None or m < best[0]): best = (m, p)
    if best:
        s['o'] = best[1]['hours']; s['os'] = 'OpenStreetMap'; src['osm'] += 1
json.dump(d, open('data.json', 'w'), ensure_ascii=False)
print(sum(src.values()), 'van', len(d['stations']), 'cafés met openingsuren', src)
