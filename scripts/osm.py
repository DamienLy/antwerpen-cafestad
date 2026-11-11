"""Turn the decoded OSM basemap (basemap_raw.json) into compact SVG path strings, pre-projected."""
import json, math
C = math.cos(math.radians(51.214))
P = lambda la, lo: ((lo - 4.41) * C * 1e5, (51.214 - la) * 1e5)
X0, X1, Y0, Y1 = -3400, 4000, -3200, 3600   # clip box (svg units, ~1 unit = 0.7-1.1 m)

def rdp(pts, eps):
    if len(pts) < 3: return pts
    a, b = pts[0], pts[-1]
    dx, dy = b[0]-a[0], b[1]-a[1]; L = math.hypot(dx, dy)
    best, idx = -1, 0
    for i in range(1, len(pts)-1):
        p = pts[i]
        d = math.hypot(p[0]-a[0], p[1]-a[1]) if L == 0 else abs(dy*p[0]-dx*p[1]+b[0]*a[1]-b[1]*a[0])/L
        if d > best: best, idx = d, i
    if best <= eps: return [a, b]
    return rdp(pts[:idx+1], eps)[:-1] + rdp(pts[idx:], eps)

def d_of(pts, close=False):
    q = [(round(x), round(y)) for x, y in pts]
    out = [q[0]]
    for p in q[1:]:
        if p != out[-1]: out.append(p)
    if len(out) < 2: return ''
    s = f"M{out[0][0]} {out[0][1]}l" + " ".join(f"{b[0]-a[0]} {b[1]-a[1]}" for a, b in zip(out, out[1:]))
    return s + ("z" if close else "")

EPS = {'R': 2.5, 'T': 2, 'M': 2, 'P': 1.5, 'Z': 3, 'W': 3, 'G': 3}
feats = json.load(open('basemap_raw.json'))
paths = {k: [] for k in EPS}
named = {}
for k, n, ll in feats:
    if len(ll) > 900: continue
    pts = [P(a, b) for a, b in ll]
    if not any(X0 < x < X1 and Y0 < y < Y1 for x, y in pts): continue
    closed = k in 'WG'
    pts = rdp(pts, EPS[k])
    if closed and len(pts) < 3: continue
    d = d_of(pts, closed)
    if not d: continue
    paths[k].append(d)
    if n and k in 'MTP':
        L = sum(math.hypot(b[0]-a[0], b[1]-a[1]) for a, b in zip(pts, pts[1:]))
        if L > named.get(n, (0,))[0]:
            # orient left-to-right so labels read the right way
            if pts[0][0] > pts[-1][0]: pts = pts[::-1]
            xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
            named[n] = (L, d_of(pts), [round(min(xs)), round(min(ys)), round(max(xs)), round(max(ys))], k)
out = {k: "".join(v) for k, v in paths.items()}
out['N'] = [[n, round(v[0]), v[1], v[2], v[3]] for n, v in sorted(named.items(), key=lambda t: -t[1][0]) if v[0] > 60]
json.dump(out, open('osm.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print({k: len(v) for k, v in out.items() if k != 'N'}, 'names', len(out['N']), 'bytes', len(json.dumps(out, ensure_ascii=False)))
