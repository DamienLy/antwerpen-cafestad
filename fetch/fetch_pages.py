"""Haalt de URL's uit fetch/urls.txt op en bewaart wat lukt in fetch/out/ (alleen de nuttige tekst)."""
import os, re, time, json, hashlib, urllib.request
os.makedirs('fetch/out', exist_ok=True)
ok = {}
for line in open('fetch/urls.txt'):
    url = line.strip()
    if not url or url.startswith('#'): continue
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15", "Accept-Language": "nl-BE,nl;q=0.9,en;q=0.8"})
        r = urllib.request.urlopen(req, timeout=30)
        if r.status == 200 and r.geturl().rstrip('/') == url.rstrip('/'):
            html = r.read().decode('utf-8', 'ignore')
            fn = hashlib.md5(url.encode()).hexdigest()[:12] + '.html'
            open('fetch/out/' + fn, 'w').write(html); ok[url] = fn
    except Exception as e:
        pass
    time.sleep(0.4)
json.dump(ok, open('fetch/out/index.json', 'w'), indent=0)
print(len(ok), 'pagina\'s opgehaald')
