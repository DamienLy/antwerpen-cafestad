import json

# name: (address, lat, lon, quality)  quality: gps = coords from source page, adres = address found, position placed by street
A = {
 "Café Jozef": ("Koningin Astridplein 43", 51.21881, 4.42044, "gps"),
 "Bier Central": ("De Keyserlei 25", 51.21815, 4.41770, "adres"),
 "Kelly's Irish Pub": ("De Keyserlei 27", 51.21820, 4.41790, "adres"),
 "Jones&Co": ("Pelgrimstraat 7", 51.21970, 4.40030, "adres"),
 "De Vagant": ("Reyndersstraat 25", 51.21900, 4.39900, "adres"),
 "Philly's": ("Grote Pieter Potstraat 7", 51.22050, 4.39800, "adres"),
 "Cantaloop": ("Onze-Lieve-Vrouwstraat 1, Berchem", 51.19750, 4.42350, "adres"),
 "Rood-Wit": ("Generaal Drubbelstraat 42, Berchem", 51.19950, 4.42000, "adres"),
 "Café Des Arts": ("Boomgaardstraat 350, Berchem", 51.20050, 4.42450, "adres"),
 "Cabagine": ("Victor Jacobslei 68, Berchem", 51.19850, 4.42700, "adres"),
 "Café Tati": ("Victor Jacobslei 69, Berchem", 51.19860, 4.42720, "adres"),
 "De Duifkens": ("Graanmarkt 5", 51.21625, 4.41170, "adres"),
 "Oud Arsenaal": ("Maria Pijpelincxstraat 4", 51.21650, 4.41000, "adres"),
 "Boer van Tienen": ("Mechelseplein 6", 51.21420, 4.40500, "adres"),
 "K. Zeppos": ("Vleminckveld 78", 51.21400, 4.40250, "adres"),
 "Kulminator": ("Vleminckveld 32", 51.21450, 4.40350, "adres"),
 "The Joker": ("Kleine Markt 16", 51.21531, 4.40208, "gps"),
 "Baron": ("Marnixplaats 5", 51.20820, 4.39480, "adres"),
 "Vitrin": ("Marnixplaats 14", 51.20780, 4.39550, "adres"),
 "Hopper": ("Leopold De Waelstraat 2", 51.20880, 4.39580, "adres"),
 "Chatleroi": ("Graaf van Hoornestraat 2", 51.20980, 4.39700, "adres"),
 "Izzy Maze": ("Leopoldplaats 2", 51.21330, 4.40900, "adres"),
 "Café Plastron": ("Troonplaats 5", 51.20580, 4.40780, "adres"),
 "Bar d'Henri": ("Montignystraat 21", 51.20400, 4.39850, "adres"),
 "Pamela": ("Marnixplaats 21", 51.20760, 4.39450, "adres"),
 "Ons Huis": ("Geluwestraat 1, Berchem", 51.19350, 4.42250, "adres"),
 "Repos": ("Lodewijk De Koninckstraat 39, Berchem", 51.19750, 4.41650, "adres"),
 "De Buis": ("Marie-Josélaan 29, Berchem", 51.19400, 4.41950, "adres"),
 "Den Draak": ("Draakplaats 1", 51.20620, 4.42900, "adres"),
 "Gitanes": ("Tramplein 3, Berchem", 51.20500, 4.43180, "adres"),
 "Kid's": ("Grote Markt 50", 51.22080, 4.39980, "adres"),
 "Cousteau": ("Paardenmarkt 42", 51.22400, 4.40850, "adres"),
 "Hessenhuis": ("Falconrui 79", 51.22620, 4.40350, "adres"),
 "Bosbar": ("Ankerrui 5-7 (Het Bos)", 51.22620, 4.40750, "adres"),
 "Café Moeskop": ("Dageraadplaats 17", 51.20790, 4.43100, "adres"),
 "ZeeZicht": ("Dageraadplaats 7-8", 51.20730, 4.43020, "adres"),
 "Gorillaz": ("Dageraadplaats 14", 51.20769, 4.43044, "gps"),
 "De Zure": ("Dageraadplaats 4", 51.20681, 4.43056, "gps"),
 "Bobby": ("Isabellalei 161", 51.20550, 4.41950, "adres"),
 "Foxy": ("Vosstraat 23, Borgerhout", 51.21280, 4.43450, "adres"),
 "Bar Brul": ("Karel de Preterlei 222, Borgerhout", 51.20750, 4.43900, "adres"),
 "Tram 3": ("Oude Koornmarkt 38", 51.22000, 4.39880, "adres"),
 "'t Vervolg": ("Melkmarkt 9", 51.22070, 4.40190, "adres"),
 "Cabron": ("Kaasrui 1", 51.22180, 4.39980, "adres"),
 "11e Gebod": ("Torfbrug 10", 51.22100, 4.40130, "adres"),
 "Cinq": ("Torfbrug 5", 51.22090, 4.40150, "adres"),
 "The Irish Times Pub": ("Grote Markt 38", 51.22100, 4.39900, "adres"),
 "Café au lait": ("Oude Beurs 8", 51.22230, 4.40080, "adres"),
 "Den Engel": ("Grote Markt 3", 51.22140, 4.39980, "adres"),
 "Barries": ("Reyndersstraat 21", 51.21900, 4.39870, "adres"),
 "Het Souke": ("Hoogstraat 59", 51.21900, 4.39650, "adres"),
 "Café Beveren": ("Vlasmarkt 2", 51.21990, 4.39760, "adres"),
 "De Ware Jacob": ("Vlasmarkt 19", 51.21960, 4.39830, "adres"),
 "Café de Vischmijn": ("Riemstraat 20", 51.21300, 4.39150, "adres"),
 "In de Roscam": ("Vrijdagmarkt 12", 51.218131, 4.399003, "gps"),
 "Corso": ("Vrijdagmarkt 17", 51.21830, 4.39940, "adres"),
 "De 7 Schaken": ("Lange Beeldekensstraat 50", 51.22070, 4.42650, "adres"),
 "Café Pelikaan": ("Melkmarkt 14", 51.22055, 4.40260, "adres"),
 "De Muze": ("Melkmarkt 15", 51.22070, 4.40270, "adres"),
 "Beautiful Planet": ("De Coninckplein 12", 51.22170, 4.42080, "adres"),
 "Beerlovers bar": ("Rotterdamstraat 105", 51.22400, 4.42250, "adres"),
 "Kiebooms": ("De Coninckplein 18", 51.22160, 4.42120, "adres"),
 "Plaza Real": ("Kattenberg 89, Borgerhout", 51.21330, 4.43850, "adres"),
 "De Kroon": ("Kerkstraat 91", 51.22130, 4.42550, "adres"),
 "De Klamper": ("Offerandestraat 21", 51.22300, 4.42850, "adres"),
 "De Seefhoek": ("Diepestraat 170", 51.22550, 4.43000, "adres"),
 "BarBob": ("Kroonstraat 80, Borgerhout", 51.21900, 4.43400, "adres"),
 "Café Mombasa": ("Moorkensplein 37, Borgerhout", 51.21630, 4.43680, "adres"),
 "In de stad Aalst": ("Carnotstraat 16", 51.218641, 4.422931, "gps"),
 "Bar Bakeliet": ("Laar 11, Borgerhout", 51.21680, 4.43950, "adres"),
 "Bar Leon": ("Reuzenstraat 23, Borgerhout", 51.21550, 4.43850, "adres"),
 "Multatuli": ("Lange Vlierstraat 9", 51.21680, 4.39950, "adres"),
 "Beestenbos": ("Sint-Andriesplaats 17", 51.21630, 4.39850, "adres"),
 "Dansing Chocola": ("Kloosterstraat 159", 51.213219, 4.394098, "gps"),
 "Heilig Huisken": ("Kloosterstraat 155", 51.21340, 4.39430, "adres"),
 "De Arme Duivel": ("Armeduivelstraat 1", 51.21580, 4.40700, "adres"),
 "De Varkenspoot": ("Graanmarkt 3", 51.21615, 4.41150, "adres"),
 "Cabardouche Taproom": ("Engelselei 254, Borgerhout", 51.22400, 4.43700, "adres"),
 "Café Welkom": ("Noordschippersdok 21", 51.22750, 4.41700, "adres"),
 "Moby Dick": ("Bredastraat 4", 51.23206, 4.421504, "gps"),
 "Zeppelin": ("Damplein 13", 51.23120, 4.42050, "adres"),
 "ZIGZAG": ("Ellermanstraat 58", 51.23000, 4.41300, "adres"),
 "Paloma": ("Van Schoonbekeplein 19", 51.22700, 4.40500, "adres"),
 "Dr. Beer": ("Adriaan Brouwerstraat 31", 51.2276875, 4.4045625, "gps"),
 "Den Tros": ("Napoleonkaai 55", 51.22860, 4.40970, "adres"),
 "Bar du Port": ("Napoleonkaai 53", 51.22850, 4.40950, "adres"),
 "'t Licht der Dokken": ("Verbindingsdok-Westkaai 2", 51.231016, 4.406498, "gps"),
 "Batavier": ("Sint-Laureiskaai 13", 51.2298125, 4.4050625, "gps"),
 "Boekowski": ("Bolivarplaats 4", 51.20450, 4.39150, "adres"),
 "De Nieuwe Linde": ("Pacificatiestraat 49", 51.20580, 4.40050, "adres"),
 "De Rui": ("Oudevaartplaats 60", 51.21420, 4.40950, "adres"),
 "The Geeky Cauldron": ("Sint-Jacobsmarkt 88", 51.22050, 4.41380, "adres"),
 "Borze café": ("Borzestraat 30", 51.2199375, 4.4060625, "gps"),
 "De Prof": ("Vekestraat 51", 51.22030, 4.41050, "adres"),
 "Dogma": ("Wijngaardstraat 5", 51.22190, 4.40470, "adres"),
 "The Northerner": ("Wijngaardstraat 7", 51.22200, 4.40490, "adres"),
 "Paters Vaetje": ("Blauwmoezelstraat 1", 51.22080, 4.40120, "adres"),
 "Witzli-Poetzli": ("Blauwmoezelstraat 8", 51.22110, 4.40170, "adres"),
 "Marmite": ("Torfbrug 8", 51.22100, 4.40140, "adres"),
 "Quinten Matsijs": ("Moriaanstraat 17", 51.22200, 4.40220, "adres"),
 "De Zwaan": ("Hendrik Conscienceplein 15", 51.22130, 4.40570, "adres"),
 "Café de Zwoele Zwaluw": ("Veemarkt 4", 51.22270, 4.40080, "adres"),
 "Café Ernst": ("Ernest Van Dijckkaai 18", 51.22050, 4.39550, "adres"),
 "Bar Lucy": ("Koepoortbrug 4", 51.22500, 4.40420, "adres"),
 "De Vuile Was": ("Grote Pieter Potstraat 16", 51.22030, 4.39770, "adres"),
 "Fetish Café": ("Kleine Pieter Potstraat 8", 51.22080, 4.39750, "adres"),
 "CUT": ("Grote Pieter Potstraat 21", 51.22020, 4.39750, "adres"),
 "Barracuda": ("Ossenmarkt 1", 51.22130, 4.41280, "adres"),
 "Kassa 4": ("Ossenmarkt 21", 51.22180, 4.41380, "adres"),
 "Papa Jos": ("Blindestraat 39", 51.22280, 4.41120, "adres"),
 "'t Lastig Portret": ("Blindestraat 1", 51.22200, 4.41220, "adres"),
 "Apropos": ("Schermersstraat 33", 51.21500, 4.40620, "adres"),
 "Barbossa": ("Sint-Jorispoort 2", 51.21380, 4.40720, "adres"),
 "Korsakov": ("Sint-Jorispoort 1", 51.21370, 4.40700, "adres"),
 "Hypothalamus": ("Mechelseplein 19", 51.21430, 4.40530, "adres"),
 "De Pallieter": ("Mechelseplein 17", 51.21440, 4.40520, "adres"),
 "Café Kamiel": ("Markgravelei 90", 51.20300, 4.40450, "adres"),
 "Den Tweede zit": ("Bolivarplaats 6", 51.20460, 4.39180, "adres"),
 "La Dolce Vita": ("Stadswaag 11", 51.22380, 4.40520, "adres"),
 "Klimax": ("Stadswaag 19", 51.22400, 4.40480, "adres"),
 "'t Waagstuk": ("Stadswaag 20", 51.22410, 4.40460, "adres"),
 "De Fonkelarij": ("Koepoortbrug 4", 51.22510, 4.40440, "adres"),
 "De Kat": ("Wolstraat 22", 51.22250, 4.40300, "adres"),
 "Spéciale Belge taproom": ("Regine Beerplein 1", None, None, "adres-geschat"),
 "Café Clodette": ("Hoogstraat 22", 51.21960, 4.39740, "adres"),
}

L = json.load(open('lines.json'))
# rename cut-off names
for k in ('lichtgroen', 'bordeaux'):
    L[k]['stations'].append("Bar Leon")
L['geel']['stations'].insert(0, "Café Clodette")

names = []
for v in L.values():
    for s in v['stations']:
        if s not in names:
            names.append(s)

coords = {n: (A[n][1], A[n][2]) for n in names if n in A and A[n][1] is not None}

def interp(n):
    for key, v in L.items():
        st = v['stations']
        if n not in st:
            continue
        i = st.index(n)
        prev = next(((j, st[j]) for j in range(i - 1, -1, -1) if st[j] in coords), None)
        nxt = next(((j, st[j]) for j in range(i + 1, len(st)) if st[j] in coords), None)
        if prev and nxt:
            t = (i - prev[0]) / (nxt[0] - prev[0])
            a, b = coords[prev[1]], coords[nxt[1]]
            return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
    return None

missing = [n for n in names if n not in coords]
# iterate until all filled
for _ in range(5):
    for n in list(missing):
        p = interp(n)
        if p:
            coords[n] = p
            missing.remove(n)
print("still missing:", missing)

out = []
for n in names:
    lines = [k for k, v in L.items() if n in v['stations']]
    if n in A:
        addr, _, _, q = A[n]
        if q == "adres-geschat":
            q = "geschat"
    else:
        addr, q = None, "geschat"
    out.append({"n": n, "lat": round(coords[n][0], 6), "lon": round(coords[n][1], 6),
                "a": addr, "q": q, "l": lines})

hubs = ["Café Jozef", "Café Des Arts", "De Duifkens", "Bar Brul", "Boer van Tienen", "Izzy Maze",
        "Tram 3", "Cabron", "Kid's", "De Muze", "Quinten Matsijs", "ABC"]
for o in out:
    o["h"] = o["n"] in hubs
lines_out = [{"id": k, "c": v["color"], "s": v["stations"]} for k, v in L.items()]
json.dump({"stations": out, "lines": lines_out}, open('data.json', 'w'), ensure_ascii=False)
from collections import Counter
print(len(out), Counter(o['q'] for o in out))
print([o['n'] for o in out if o['q'] == 'geschat'])
