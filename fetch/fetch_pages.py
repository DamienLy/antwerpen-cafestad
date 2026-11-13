"""Haalt de URL's uit fetch/urls.txt op en bewaart ze ongewijzigd in fetch/out/ (tekst of beeld)."""
import os, time, json, hashlib, urllib.request
os.makedirs('fetch/out', exist_ok=True)
ok = {}
for line in open('fetch/urls.txt'):
    url = line.strip()
    if not url or url.startswith('#'): continue
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
                                                   "Accept-Language": "nl-BE,nl;q=0.9,en;q=0.8", "Referer": "https://www.openingsuren.vlaanderen/"})
        r = urllib.request.urlopen(req, timeout=25)
        data = r.read(); ct = r.headers.get('Content-Type', '')
        ext = '.png' if 'png' in ct else '.gif' if 'gif' in ct else '.jpg' if 'jpeg' in ct else '.xml' if 'xml' in ct else '.html'
        fn = hashlib.md5(url.encode()).hexdigest()[:12] + ext
        open('fetch/out/' + fn, 'wb').write(data); ok[url] = fn
    except Exception as e:
        print('mislukt', url, e)
    time.sleep(0.3)
json.dump(ok, open('fetch/out/index.json', 'w'), indent=0)
print(len(ok), "opgehaald")
