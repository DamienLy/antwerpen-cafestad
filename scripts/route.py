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
    E = [e for e in G.edges if e[0][0] != 'S' and e[1][0] != 'S']
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

# attach points; cafés far from any street keep their own node in the line
attach = {n: next(iter(G[('S', n)])) for n in st}
far = {n for n, a in attach.items() if math.dist(coord[('S', n)], coord[a]) > 25}
links = {n: [round(coord[a][0], 1), round(coord[a][1], 1)] for n, a in attach.items() if 4 < math.dist(coord[('S', n)], coord[a]) and n not in far}
end = lambda n: ('S', n) if n in far else attach[n]
for n in st:   # cafés are not through-roads
    if n not in far: G.remove_node(('S', n))

order = {l['id']: i for i, l in enumerate(d['lines'])}
canon = lambda u, v: (u, v) if str(u) < str(v) else (v, u)

def route_all(bonus):
    """route every line; edges already used by other lines are cheaper (bundling)"""
    edges, detours = {}, []
    for l in d['lines']:
        lid = l['id']; E = set()
        def w(u, v, a):
            k = canon(u, v); others = len(bonus.get(k, set()) - {lid})
            return a['w'] * (0.55 if others else 1.0)
        for a, b in zip(l['s'], l['s'][1:]):
            na, nb = end(a), end(b)
            if na == nb: continue
            p = nx.shortest_path(G, na, nb, weight=w)
            straight = math.dist(coord[na], coord[nb])
            routed = sum(math.dist(coord[x], coord[y]) for x, y in zip(p, p[1:]))
            if routed > 1.5 * straight + 100: p = [na, nb]; detours.append((lid, a, b))
            for u, v in zip(p, p[1:]): E.add(canon(u, v))
        edges[lid] = E
    return edges, detours

edges, _ = route_all({})
for it in range(3):
    use = {}
    for lid, E in edges.items():
        for e in E: use.setdefault(e, set()).add(lid)
    edges, detours = route_all(use)
print('omwegen vervangen door rechte lijn:', len(detours))

users = {}
for lid, E in edges.items():
    for e in E: users.setdefault(e, set()).add(lid)

def chains(E):
    """split a line's edge set into polylines that run from junction/end to junction/end"""
    adj = {}
    for u, v in E: adj.setdefault(u, []).append(v); adj.setdefault(v, []).append(u)
    used = set(); out = []
    stops = [n for n, nb in adj.items() if len(nb) != 2]
    def walk(a, b):
        ch = [a, b]; used.add(canon(a, b))
        while len(adj[ch[-1]]) == 2:
            nxt = [x for x in adj[ch[-1]] if canon(ch[-1], x) not in used]
            if not nxt: break
            used.add(canon(ch[-1], nxt[0])); ch.append(nxt[0])
        return ch
    for a in stops:
        for b in adj[a]:
            if canon(a, b) not in used: out.append(walk(a, b))
    for u, v in E:   # pure loops
        if canon(u, v) not in used: out.append(walk(u, v))
    return out, {n for n, nb in adj.items() if len(nb) > 2}

def slot_of(lid, u, v):
    us = sorted(users[canon(u, v)], key=order.get); sl = us.index(lid) - (len(us) - 1) / 2
    return sl if (u, v) == canon(u, v) else -sl

def steady(ch, min_len=90):
    for _ in range(4):
        runs = []
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
for l in d['lines']:
    lid = l['id']; chs, junc = chains(edges[lid])
    # one shared slot per junction of this line, so every chain ending there meets at the same point
    jslot = {}
    for ch in sorted(chs, key=lambda c: -sum(math.dist(coord[a], coord[b]) for a, b in zip(c, c[1:]))):
        for end_i, nb_i in ((0, 1), (-1, -2)):
            n = ch[end_i]
            if n in junc and n not in jslot: jslot[n] = (ch[end_i], ch[nb_i])
    res = []
    for ch in chs:
        pts = []
        for j, u in enumerate(ch):
            sl = slot_of(lid, u, ch[j + 1]) if j < len(ch) - 1 else 0
            pts.append([*coord[u], sl, 0])
        if len(pts) > 2: pts = steady(pts)
        pts[-1][2] = pts[-2][2]
        # junction anchors: [x, y, slot, 0] of the reference edge at that node, as extra end info
        anchors = []
        for end_i in (0, -1):
            n = ch[end_i]
            if n in jslot:
                a, b = jslot[n]; anchors.append([round(coord[b][0] - coord[a][0], 2), round(coord[b][1] - coord[a][1], 2), slot_of(lid, a, b)])
            else: anchors.append(None)
        keep = [pts[0]]
        for j in range(1, len(pts) - 1):
            a, b, c2 = keep[-1], pts[j], pts[j + 1]
            if b[2] != a[2]: keep.append(b); continue
            dx, dy = c2[0] - a[0], c2[1] - a[1]; L = math.hypot(dx, dy) or 1
            if abs(dy * b[0] - dx * b[1] + c2[0] * a[1] - c2[1] * a[0]) / L > 1.5: keep.append(b)
        keep.append(pts[-1])
        res.append({'p': [[round(p[0], 1), round(p[1], 1), p[2]] for p in keep], 'a': anchors})
    out[lid] = res
json.dump({'lines': out, 'links': links}, open('routes.json', 'w'), separators=(',', ':'))
print('ketens per lijn', {k: len(v) for k, v in out.items()}, 'links', len(links), 'ver:', sorted(far))
print('gedeelde straatstukken', sum(1 for v in users.values() if len(v) > 1), 'van', len(users))
