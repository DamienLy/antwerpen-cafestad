"""Bouwt de posterweergave na volgens de originele poster (poster_src/poster_original.png, 798 x 501 px):
1. posities: elk café op zijn symbool in het origineel (gevonden met beeldherkenning, zie posterpos.json);
2. knikken: per stuk tussen twee cafés de vorm (recht, recht+45, 45+recht, hoek) die het best op de lijnkleur in het origineel valt;
3. rechttrekken: rechte stukken exact horizontaal, verticaal of 45 graden (kleinste kwadraten);
4. bundels: de volgorde van de lijnen naast elkaar zoals op het origineel;
5. symbolen en namen: grijze pil, gekleurde ring of grote ring, met de naam zoals op de poster.
Schrijft data.json (pp, pd, pl) en poster.json {lijn: [[x, y, slot, station_of_-1], ...]}."""
import json, math
import numpy as np
from PIL import Image, ImageFilter

SC = 1.8                                     # poster px -> poster units used on the site
d = json.load(open('data.json'))
names = [s['n'] for s in d['stations']]; idx = {n: i for i, n in enumerate(names)}
POS = json.load(open('poster_src/posterpos.json'))
P0 = np.array([[POS[n][0] * SC, POS[n][1] * SC] for n in names], float)
IMG0 = Image.open('poster_src/poster_original.png').convert('RGB')
IMG = np.asarray(IMG0.resize((round(IMG0.width * SC), round(IMG0.height * SC)), Image.LANCZOS), float)
hexrgb = lambda h: np.array([int(h[k:k + 2], 16) for k in (1, 3, 5)], float)

def classify(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]; ang = math.degrees(math.atan2(dy, dx)) % 180
    for k, t in ((0, 0), (0, 180), (1, 90), (2, 45), (3, 135)):
        if abs(ang - t) < 12: return k
    return None

SAMPLE = {'geel': (65, 246), 'blauw': (513, 359), 'donkerblauw': (526, 440), 'grijs': (565, 440), 'oranje': (474, 261.5), 'bordeaux': (606.5, 109),
          'magenta': (232, 109), 'groen': (295, 441.5), 'lichtgroen': (595, 199), 'zwart': (530, 207.5), 'roze': (620, 251), 'rood': (341.5, 154)}
def line_colour(l):
    """the line's real colour in the original, sampled on a stretch where only that line runs"""
    x, y = SAMPLE[l['id']]; x, y = x * SC, y * SC
    win = IMG[int(y) - 4:int(y) + 5, int(x) - 4:int(x) + 5].reshape(-1, 3)
    return win[np.argsort(win.sum(1))[:6]].mean(0)
COL = {l['id']: line_colour(l) for l in d['lines']}

def match(x, y, col, r=3):
    win = IMG[max(0, int(y) - r):int(y) + r + 1, max(0, int(x) - r):int(x) + r + 1].reshape(-1, 3)
    if not len(win): return 0.0
    return float(1 - np.linalg.norm(win - col, axis=1).min() / 120)

def cands(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]; sx, sy = (1 if dx >= 0 else -1), (1 if dy >= 0 else -1)
    out = {'straight': []}
    if abs(dx) > abs(dy):
        out['s45'] = [(a[0] + sx * (abs(dx) - abs(dy)), a[1])]; out['45s'] = [(a[0] + sx * abs(dy), b[1])]
    else:
        out['s45'] = [(a[0], a[1] + sy * (abs(dy) - abs(dx)))]; out['45s'] = [(b[0], a[1] + sy * abs(dx))]
    out['hv'] = [(b[0], a[1])]; out['vh'] = [(a[0], b[1])]
    return out

def score(path, col, a, b):
    vals = []; rx = min(14, 0.25 * math.dist(a, b))
    for p, q in zip(path, path[1:]):
        L = math.dist(p, q)
        for t in np.linspace(0, 1, max(2, int(L / 3))):
            x, y = p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t
            if math.dist((x, y), a) > rx and math.dist((x, y), b) > rx: vals.append(match(x, y, col, 7))
    return float(np.mean(vals)) if len(vals) > 2 else 0.0

# 1. bends from the original
# the rectangle around Dam 12 / Zorro has right-angled corners on the poster; the colour test reads them as chamfers
OVERRIDE = {('Quinten Matsijs', 'Zorro'): 'hv', ('De Zwaan', 'Café de Zwoele Zwaluw'): 'vh', ('Café de Zwoele Zwaluw', 'Dam 12'): 'hv',
            ('Café Ernst', 'Bar Lucy'): 'vh', ('Dam 12', 'Café Ernst'): 'straight', ('Zorro', 'De Zwaan'): 'straight', ('Bar Lucy', 'Quinten Matsijs'): 'straight'}
choice = {}
for l in d['lines']:
    for a, b in zip(l['s'], l['s'][1:]):
        i, j = idx[a], idx[b]
        if (i, j) in choice or (j, i) in choice: continue
        A, B = tuple(P0[i]), tuple(P0[j]); cs = cands(A, B)
        cs = {k: v for k, v in cs.items() if not v or min(math.dist(v[0], A), math.dist(v[0], B)) > 8}
        share = len(set(d['stations'][i]['l']) & set(d['stations'][j]['l']))
        span = (share - 1) / 2 * 13.9 + 3
        def best(path):
            out = -9
            for o in np.arange(-span, span + .1, 3):
                for ox, oy in ((o, 0), (0, o), (o * .707, o * .707), (o * .707, -o * .707)):
                    out = max(out, score([(x + ox, y + oy) for x, y in path], COL[l['id']], (A[0] + ox, A[1] + oy), (B[0] + ox, B[1] + oy)))
            return out
        sc = {k: best([A, *v, B]) for k, v in cs.items()}
        if classify(A, B) is not None: sc['straight'] += .12
        c = max(sc, key=sc.get)
        ov = OVERRIDE.get((a, b)); ovr = OVERRIDE.get((b, a))
        if ov: c = ov
        elif ovr: c = {'hv': 'vh', 'vh': 'hv', 's45': '45s', '45s': 's45'}.get(ovr, ovr)
        choice[(i, j)] = c
print('knikken:', {k: list(choice.values()).count(k) for k in sorted(set(choice.values()))})

# 2. straighten: octilinear straight pieces become exact
n = len(names); rows = []; rhs = []
def row(coefs, v, w):
    r = np.zeros(2 * n)
    for k, c in coefs: r[k] = c * w
    rows.append(r); rhs.append(v * w)
for i in range(n):
    row([(2 * i, 1)], P0[i, 0], 1); row([(2 * i + 1, 1)], P0[i, 1], 1)
for (i, j), c in choice.items():
    k = classify(P0[i], P0[j]) if c == 'straight' else None
    if k == 0: row([(2 * i + 1, 1), (2 * j + 1, -1)], 0, 15)
    elif k == 1: row([(2 * i, 1), (2 * j, -1)], 0, 15)
    elif k == 2: row([(2 * i, 1), (2 * j, -1), (2 * i + 1, -1), (2 * j + 1, 1)], 0, 15)
    elif k == 3: row([(2 * i, 1), (2 * j, -1), (2 * i + 1, 1), (2 * j + 1, -1)], 0, 15)
P = np.linalg.lstsq(np.array(rows), np.array(rhs), rcond=None)[0].reshape(n, 2)
print('gemiddelde verschuiving door rechttrekken', round(float(np.hypot(*(P - P0).T).mean()), 2), 'eenheden')

# 3. polylines
bends = {k: cands(tuple(P[k[0]]), tuple(P[k[1]]))[c] for k, c in choice.items()}
lines = {}
for l in d['lines']:
    pts = [[*P[idx[l['s'][0]]], idx[l['s'][0]]]]
    for a, b in zip(l['s'], l['s'][1:]):
        i, j = idx[a], idx[b]
        mid = bends[(i, j)] if (i, j) in bends else bends[(j, i)][::-1]
        for m in mid: pts.append([m[0], m[1], -1])
        pts.append([*P[j], j])
    lines[l['id']] = pts

# 4. bundle order from the original: where does each colour sit across the shared piece?
GAP = 13.9   # distance between parallel lines on the poster, in poster units
key = lambda p: (round(p[0]), round(p[1]))
canon = lambda u, v: (u, v) if u < v else (v, u)
users = {}
for lid, pts in lines.items():
    for p, q in zip(pts, pts[1:]): users.setdefault(canon(key(p), key(q)), set()).add(lid)
order_default = {l['id']: k for k, l in enumerate(d['lines'])}
seg_order = {}; seg_raw = {}
for (u, v), us in users.items():
    if len(us) < 2: continue
    (ax, ay), (bx, by) = u, v; L = math.hypot(bx - ax, by - ay)
    if L < 1: continue
    tx, ty = (bx - ax) / L, (by - ay) / L; nx, ny = -ty, tx
    span = (len(us) - 1) / 2 * GAP + 6
    pos = {lid: [] for lid in us}
    for t in np.linspace(0.15, 0.85, 7):
        cx, cy = ax + (bx - ax) * t, ay + (by - ay) * t
        if min(math.dist((cx, cy), tuple(P[k])) for k in range(n)) < 20: continue
        offs = np.linspace(-span, span, int(span * 2) + 1)
        for lid in us:
            sc = [match(cx + nx * o, cy + ny * o, COL[lid], 1) for o in offs]
            pos[lid].append(offs[int(np.argmax(sc))])
    ori = (tx, ty) if (tx > 1e-6 or (abs(tx) <= 1e-6 and ty > 0)) else (-tx, -ty)
    flip = ori != (tx, ty)
    est = {l: (np.median(pos[l]) * (-1 if flip else 1)) for l in us if pos[l]}
    seg_raw[(u, v)] = (frozenset(us), (round(ori[0], 1), round(ori[1], 1)), est, flip)
# one order per connected run of pieces with the same lines and orientation: vote, so a bundle never swaps places
par = {c: c for c in seg_raw}
def find(c):
    while par[c] != c: par[c] = par[par[c]]; c = par[c]
    return c
by_node = {}
for c, (grp, ori, est, flip) in seg_raw.items():
    for nd in c: by_node.setdefault(nd, []).append(c)
for nd, cs in by_node.items():
    for c1 in cs:
        for c2 in cs:
            if c1 < c2 and seg_raw[c1][0] == seg_raw[c2][0] and seg_raw[c1][1] == seg_raw[c2][1]: par[find(c1)] = find(c2)
runs = {}
for c in seg_raw: runs.setdefault(find(c), []).append(c)
for r, cs in runs.items():
    grp = sorted(seg_raw[cs[0]][0], key=order_default.get)
    ests = [seg_raw[c][2] for c in cs if len(seg_raw[c][2]) == len(grp)]
    if ests:
        mean = {l: np.mean([e[l] for e in ests]) for l in grp}; o = sorted(grp, key=lambda l: (mean[l], order_default[l]))
    else: o = grp
    for c in cs: seg_order[c] = o[::-1] if seg_raw[c][3] else o
# the rectangle around Dam 12 / Zorro: black runs on the outside all the way round, as on the poster
BOX = np.mean([P[idx[n_]] for n_ in ['Dam 12', 'Café Ernst', 'De Zwaan', 'Zorro', 'Café de Zwoele Zwaluw', 'Bar Lucy']], 0)
for c, (grp, ori, est, flip) in seg_raw.items():
    if grp != frozenset({'zwart', 'lichtgroen'}): continue
    (ax, ay), (bx, by) = c; L = math.hypot(bx - ax, by - ay) or 1
    tx, ty = (bx - ax) / L, (by - ay) / L; nx, ny = -ty, tx           # normal of the canonical direction
    outward = ((ax + bx) / 2 - BOX[0]) * nx + ((ay + by) / 2 - BOX[1]) * ny > 0
    seg_order[c] = ['lichtgroen', 'zwart'] if outward else ['zwart', 'lichtgroen']
out = {}
for lid, pts in lines.items():
    res = []
    for k, p in enumerate(pts):
        if k < len(pts) - 1:
            u, v = key(p), key(pts[k + 1]); c = canon(u, v)
            us = seg_order.get(c) or [lid]
            sl = us.index(lid) - (len(us) - 1) / 2
            if (u, v) != c: sl = -sl
        else: sl = res[-1][2]
        res.append([round(p[0], 1), round(p[1], 1), sl, p[3] if len(p) > 3 else p[2]])
    out[lid] = res
# fix: station index lives in position 3 of the input points
for lid, pts in lines.items():
    for r, p in zip(out[lid], pts): r[3] = p[2]

# 5. symbol direction/extent and label style per station (as on the poster)
LABEL = {}
for n_ in ['The Joker', 'Kulminator', 'K. Zeppos', 'Café Tati', 'Cabagine', "'t Werkhuys", 'Bar Bakeliet', 'Bar Leon', 'Corso', 'Café de Zwoele Zwaluw']: LABEL[n_] = 'B'
for n_ in ['Baron', 'Vitrin', 'Hopper', 'Chatleroi']: LABEL[n_] = 'LR'
for n_ in ['BarBob', 'Café Mombasa', 'In de stad Aalst']: LABEL[n_] = 'RR'
for n_ in ['Fetish Café', 'De Vuile Was']: LABEL[n_] = 'R60'
for n_ in ['CUT', 'Café Kamiel', 'Den Tweede zit', 'De Kat', 'Plaza Real', 'Café Pelikaan', 'Apropos', 'Barbossa', 'Korsakov', 'Hypothalamus',
           'De Pallieter', 'De Varkenspoot', 'De Arme Duivel', 'De Rui', 'De Nieuwe Linde', 'Boekowski', 'Bier Central', "Kelly's Irish Pub", 'Heilig Huisken']: LABEL[n_] = 'R'
for n_ in ['Jones&Co', 'Café Ernst', 'Dam 12', 'Zorro', 'De Zwaan']: LABEL[n_] = 'L'
for n_ in ["Philly's", 'De Vagant']: LABEL[n_] = 'R'
HUB = {"Kid's": 'HA', 'Cabron': 'HA', 'Tram 3': 'HAL', 'De Duifkens': 'HA', 'Café Des Arts': 'HB', 'Quinten Matsijs': 'HL', 'De Muze': 'HL',
       'Boer van Tienen': 'HR', 'Bar Brul': 'HR', 'Izzy Maze': 'HR', 'Café Jozef': 'HR', 'ABC': 'HBR'}
def unit(v):
    m = math.hypot(*v); return (v[0] / m, v[1] / m) if m else (1, 0)
def octi(v):
    a = round(math.degrees(math.atan2(v[1], v[0])) / 45) % 4   # 0 horizontal, 1 diag down-right, 2 vertical, 3 diag up-right
    return a
for s in d['stations']:
    i = idx[s['n']]; vecs = []; info = []
    for lid, pts in out.items():
        for k, p in enumerate(pts):
            if p[3] != i: continue
            if k + 1 < len(pts): q = pts[k + 1]; v = unit((q[0] - p[0], q[1] - p[1])); vecs.append(v); info.append((v, p[2]))
            if k > 0: q = pts[k - 1]; v = unit((p[0] - q[0], p[1] - q[1])); vecs.append(v); info.append((v, q[2]))
    from collections import Counter
    main = Counter(octi(v) for v in vecs).most_common(1)[0][0]
    ux, uy = [(1, 0), (.7071, .7071), (0, 1), (.7071, -.7071)][main]
    sls = [sl if v[0] * ux + v[1] * uy > 0 else -sl for v, sl in info if octi(v) == main]
    lo, hi = (min(sls), max(sls)) if sls else (0, 0)
    if s['h']: lab = HUB[s['n']]
    elif s['n'] in LABEL: lab = LABEL[s['n']]
    elif abs(uy) < .2: lab = 'A'
    elif abs(ux) < .2: lab = 'L'
    elif uy > 0: lab = 'R'          # going down-right
    else: lab = 'L'                 # going up-right
    s['pp'] = [round(float(P[i][0]), 1), round(float(P[i][1]), 1)]
    s['pd'] = [round(ux, 3), round(uy, 3), lo, hi]
    s['pl'] = lab
json.dump(d, open('data.json', 'w'), ensure_ascii=False)
json.dump({'gap': GAP, 'lines': out, 'w': round(IMG0.width * SC), 'h': round(IMG0.height * SC)}, open('poster.json', 'w'), separators=(',', ':'))
print('posterlijnen klaar; bundels met eigen volgorde:', sum(1 for k, v in seg_order.items() if v != sorted(v, key=order_default.get)))
