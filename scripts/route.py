"""Route every line along real streets and work out which lines share a street, so they can be drawn side by side
like tram lines. Writes routes.json: {line_id: [chunk, ...]}, chunk = [[x, y, slot, fixed], ...]
- slot  : side-by-side position for the segment that starts at this point (0 = centre), in a fixed order per street
- fixed : 1 for the café itself (the drawing must pass exactly through it)
Each street segment is drawn once per line, so a line that goes to a café and comes back does not show double."""
import json, math
import numpy as np
import networkx as nx
from scipy.spatial import cKDTree

C = math.cos(math.radians(51.214))
P = lambda la, lo: ((lo - 4.41) * C * 1e5, (51.214 - la) * 1e5)
FACTOR = {'M': .7, 'T': .8, 'R': 1.0, 'P': 1.0}   # lean towards bigger streets, like a tram would
SNAP = 3.0

feats = json.load(open('basemap_raw.json'))
ways = [(k, [P(a, b) for a, b in ll]) for k, n, ll in feats if k in FACTOR and len(ll) < 900]

key = lambda p: (round(p[0] / SNAP), round(p[1] / SNAP))
coord = {}
segs = []
for k, pts in ways:
    ks = [key(p) for p in pts]
    for p, kk in zip(pts, ks): coord.setdefault(kk, p)
    for a, b in zip(ks, ks[1:]):
        if a != b: segs.append((a, b, FACTOR[k]))

# way ends that land in the middle of another street (junction simplified away): split that segment
deg = {}
for a, b, _ in segs:
    deg[a] = deg.get(a, 0) + 1; deg[b] = deg.get(b, 0) + 1
ends = [kk for kk, d in deg.items() if d == 1]
tree = cKDTree([((coord[a][0] + coord[b][0]) / 2, (coord[a][1] + coord[b][1]) / 2) for a, b, _ in segs])
split = {}
for e in ends:
    px, py = coord[e]
    for i in tree.query_ball_point((px, py), 120):
        a, b, f = segs[i]
        if e in (a, b): continue
        (ax, ay), (bx, by) = coord[a], coord[b]
        dx, dy = bx - ax, by - ay; L2 = dx * dx + dy * dy
        if L2 == 0: continue
        t = ((px - ax) * dx + (py - ay) * dy) / L2
        if 0.02 < t < 0.98 and math.hypot(ax + t * dx - px, ay + t * dy - py) < 12:
            split.setdefault(i, []).append((t, e))
G = nx.Graph()
def add(a, b, f):
    w = math.dist(coord[a], coord[b]) * f
    if not G.has_edge(a, b) or G[a][b]['w'] > w: G.add_edge(a, b, w=w, f=f)
for i, (a, b, f) in enumerate(segs):
    chain = [a] + [e for t, e in sorted(split.get(i, []))] + [b]
    for u, v in zip(chain, chain[1:]): add(u, v, f)
# bridge small gaps between dead ends and nearby nodes
kk = list(G.nodes); kt = cKDTree([coord[n] for n in kk])
for e in [n for n in G.nodes if G.degree(n) == 1]:
    for j in kt.query_ball_point(coord[e], 18):
        o = kk[j]
        if o != e and not G.has_edge(e, o): G.add_edge(e, o, w=math.dist(coord[e], coord[o]) * 1.2, f=1.2)
G = G.subgraph(max(nx.connected_components(G), key=len)).copy()

# attach every café to the nearest point ON a street (not the nearest crossing) -> no spikes past the café
d = json.load(open('data.json'))
st = {s['n']: s for s in d['stations']}
for s in d['stations']:
    sp = P(s['lat'], s['lon'])
    E = list(G.edges)
    A = np.array([coord[u] for u, v in E]); Bv = np.array([coord[v] for u, v in E])
    D = Bv - A; L2 = (D ** 2).sum(1); L2[L2 == 0] = 1e-9
    t = np.clip(((np.array(sp) - A) * D).sum(1) / L2, 0, 1)
    proj = A + D * t[:, None]; dist = np.hypot(*(proj - np.array(sp)).T)
    i = int(dist.argmin()); u, v = E[i]; ti = float(t[i])
    if ti < 0.08: att = u
    elif ti > 0.92: att = v
    else:
        att = ('A', s['n']); coord[att] = tuple(proj[i]); f = G[u][v]['f']
        G.remove_edge(u, v); add(u, att, f); add(att, v, f)
    sn = ('S', s['n']); coord[sn] = sp
    G.add_edge(sn, att, w=math.dist(sp, coord[att]) * 3 + 1, f=3)   # costly, so no other line cuts through a café

# route each line, café to café
order = {l['id']: i for i, l in enumerate(d['lines'])}
seqs, detours = {}, []
for l in d['lines']:
    path = [('S', l['s'][0])]
    for a, b in zip(l['s'], l['s'][1:]):
        sa, sb = ('S', a), ('S', b)
        p = nx.shortest_path(G, sa, sb, weight='w')
        straight = math.dist(coord[sa], coord[sb])
        routed = sum(math.dist(coord[x], coord[y]) for x, y in zip(p, p[1:]))
        if routed > 1.5 * straight + 100:
            p = [sa, sb]; detours.append((l['id'], a, b))
        path += p[1:]
    seqs[l['id']] = path
print('omwegen vervangen door rechte lijn:', len(detours))

# street-only paths: the café itself is left out, so lines never pinch towards a café; a thin link is drawn instead
attach = {}
for n in st:
    sn = ('S', n); att = next(iter(G[sn]))
    attach[n] = att
far = {n for n, a in attach.items() if math.dist(coord[('S', n)], coord[a]) > 25}   # no street close by: the line itself goes to the café
links = {n: [round(coord[a][0], 1), round(coord[a][1], 1)] for n, a in attach.items() if 4 < math.dist(coord[('S', n)], coord[a]) and n not in far}
for l in d['lines']:
    path = [x for x in seqs[l['id']] if x[0] != 'S' or x[1] in far]
    path = [x for j, x in enumerate(path) if j == 0 or x != path[j - 1]]
    mine = {attach[n] for n in l['s']}
    changed = True
    while changed:
        changed = False
        for j in range(1, len(path) - 1):
            if path[j - 1] == path[j + 1] and path[j] not in mine:
                del path[j:j + 2]; changed = True; break
    seqs[l['id']] = path

canon = lambda u, v: (u, v) if str(u) < str(v) else (v, u)
users = {}
for lid, path in seqs.items():
    for u, v in zip(path, path[1:]):
        users.setdefault(canon(u, v), set()).add(lid)

def steady(ch, min_len=90):
    """remove short slot excursions so bundles do not wobble"""
    for _ in range(4):
        runs = []  # [start_idx, end_idx(exclusive segments), slot, length]
        for j in range(len(ch) - 1):
            L = math.dist(ch[j][:2], ch[j + 1][:2])
            if runs and runs[-1][2] == ch[j][2]: runs[-1][1] = j + 1; runs[-1][3] += L
            else: runs.append([j, j + 1, ch[j][2], L])
        done = True
        for k, r in enumerate(runs):
            if r[3] >= min_len or len(runs) == 1: continue
            prev = runs[k - 1][2] if k > 0 else None; nxt = runs[k + 1][2] if k + 1 < len(runs) else None
            new = prev if prev is not None and (prev == nxt or nxt is None) else nxt if prev is None else None
            if new is None: continue
            for j in range(r[0], r[1]): ch[j][2] = new
            done = False
        if done: break
    return ch

out = {}
for lid, path in seqs.items():
    seen = set(); chunks = []; cur = []
    for u, v in zip(path, path[1:]):
        c = canon(u, v)
        if c in seen:
            if cur: chunks.append(cur); cur = []
            continue
        seen.add(c)
        us = sorted(users[c], key=order.get); slot = us.index(lid) - (len(us) - 1) / 2
        if (u, v) != c: slot = -slot
        if not cur: cur.append([*coord[u], slot, 0])
        else: cur[-1][2] = slot
        cur.append([*coord[v], 0, 0])
    if cur: chunks.append(cur)
    clean = []
    for ch in chunks:
        if len(ch) > 2: ch = steady(ch)
        if len(ch) > 1: ch[-1][2] = ch[-2][2]
        keep = [ch[0]]
        for j in range(1, len(ch) - 1):
            a, b, c2 = keep[-1], ch[j], ch[j + 1]
            if b[2] != a[2]: keep.append(b); continue
            dx, dy = c2[0] - a[0], c2[1] - a[1]; L = math.hypot(dx, dy) or 1
            if abs(dy * b[0] - dx * b[1] + c2[0] * a[1] - c2[1] * a[0]) / L > 1.5: keep.append(b)
        keep.append(ch[-1])
        clean.append([[round(p[0], 1), round(p[1], 1), p[2], 0] for p in keep])
    out[lid] = clean
json.dump({'lines': out, 'links': links}, open('routes.json', 'w'), separators=(',', ':'))
print('links', len(links), 'ver van een straat:', sorted(far))
print('gedeelde straatstukken', sum(1 for v in users.values() if len(v) > 1), 'van', len(users))
