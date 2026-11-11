import json
exec(open('blurbs.py').read().split("def buurt")[0])  # B: well-known notes
F = {
 "Jones&Co": "Cocktailbar uit 2014 in de Pelgrimstraat, met de kathedraaltoren recht voor je neus. Sport op scherm en een uitgesproken LGBTQ+-vriendelijke sfeer.",
 "Izzy Maze": "Nachtbar aan de Leopoldplaats die pas laat op gang komt: open van donderdag tot zaterdag, van 21 tot 5 uur, met muziek die het personeel zelf kiest.",
 "Café Plastron": "Café-bar aan de Troonplaats, bekend om zijn Belgische bieren én zijn pastaschotels. Doordeweeks open, in het weekend dicht.",
 "Ons Huis": "Rasecht Berchems buurtcafé met een biljarttafel en sport op tv, elke dag open vanaf half tien 's ochtends.",
 "Repos": "Van ontbijt tot cocktails: café in Berchem met vegetarische en vegan gerechten, craftbier en een zonnig, deels overdekt terras.",
 "Café Moeskop": "Vaste waarde op de Dageraadplaats met thee, koffie en bier aan zachte prijzen, en een terras dat tot een uur of twee bezet blijft.",
 "Barries": "Bruin café in de Reyndersstraat, een paar stappen van de Groenplaats, waar bier de hoofdrol speelt.",
 "Corso": "Laat café aan de Vrijdagmarkt, open tot 2 à 3 uur, waar je met minder dan tien euro per drankje buitenwandelt.",
 "De Nieuwe Linde": "Café-bar bekend om zijn spaghetti, met vegan opties, een terras en een uitgesproken LGBTQ+-vriendelijk publiek.",
 "Apropos": "Café in de Schermersstraat met budgetvriendelijke prijzen en een terras, tot 1 uur open van donderdag tot zaterdag.",
 "Den Tweede zit": "Eenvoudig café tegenover het justitiepaleis voor een omelet of een kaasplankje. Op zaterdag gesloten.",
 "Café Welkom": "Gezellig café aan het Noordschippersdok met kaasplanken en cocktails. Je kunt er het hele café afhuren voor een feest.",
 "Den Tros": "Havencafé aan de Napoleonkaai met zicht op het MAS. Bitterballen, kriek en pizza, en in het weekend open tot 4 uur.",
 "ZIGZAG": "Café op het Eilandje met kaas als specialiteit, aangevuld met wijn, cocktails en vegetarische en biologische opties.",
 "Cousteau": "Café aan de Paardenmarkt met brunchbroodjes en cocktails. Je kunt er een 'hartje' kopen: een drankje dat klaarstaat voor iemand die het nodig heeft.",
 "ZeeZicht": "Een van de populairste adressen van Zurenborg, met meer dan 1.400 Google-reviews. Belgische bieren, creatieve cocktails, een geliefde visschotel en af en toe live muziek.",
 "De Zure": "Café met live muziek, lasagne en pasta op de kaart, en in het weekend open tot 3 uur.",
 "Café de Vischmijn": "Volks café met lokale bieren, aperitieven en grote schermen voor de match. LGBTQ+-vriendelijk.",
 "Café Clodette": "Café in de Hoogstraat met Belgische en vegetarische tapas, een zorgvuldig gekozen drankkaart en geregeld live muziek.",
 "De Vuile Was": "Cocktailbar met live muziek, alleen open van donderdag tot zaterdag.",
 "Café Mombasa": "Buurtcafé op het Moorkensplein met een interieur vol wielrennen, een opvallend aanbod alcoholvrije en lichte bieren, en de grote matchen op scherm.",
 "Papa Jos": "Bekend om de huisspaghetti 'Papa Jos' en de zelfgemaakte broodpudding, met af en toe live muziek.",
 "Bar Brul": "Bar aan de Karel de Preterlei met geregeld live muziek, een terras en drankjes aan kleine prijzen.",
 "Den Draak": "Het café van Het Roze Huis, het LGBTQ+-huis van Antwerpen aan de Draakplaats. Ruim terras, live muziek en een happy hour.",
 "Beerlovers bar": "Bierbar met zo'n 200 internationale bieren en 12 wisselende kranen. Achter de tap staat een teddybeer om je te verwelkomen.",
 "Cantaloop": "Populair Berchems café met tapbier, vleesgerechten en een terras, en een vaste stek om voetbal te kijken.",
 "Cabagine": "Koffie- en lunchbar aan een rustig, groen pleintje in Berchem. Eigenares Anke kookt zelf en verzint elke week een nieuwe lunch. Probeer de alcoholvrije Curaçao latte.",
 "Baron": "Terrascafé op de Marnixplaats voor een Aperol Spritz, lokale bieren of tapas, met zicht op het pleinleven.",
 "Vitrin": "Cocktail- en wijnbar met een terras op de Marnixplaats. Hier kom je voor een glas, niet om te eten: er zijn alleen hapjes.",
 "Hessenhuis": "LGBTQ+-vriendelijke bar naast het historische Hessenhuis, een 16e-eeuws pakhuis, met cocktails, eten en geregeld optredens.",
 "Bobby": "Kleine bar met een terrasje aan de Isabellalei. Spaghetti en nacho's om te delen, en veel lof voor de vriendelijke bediening.",
 "Foxy": "Borgerhoutse bar met klassieke cocktails en een spaghetti die naam heeft gemaakt.",
 "'t Vervolg": "Bar op de Melkmarkt met cocktails en een terras die op vrijdag en zaterdag doorgaat tot 4 uur.",
 "Café au lait": "Cocktailbar die zo'n twintig jaar geleden werd opgericht om mensen van elke afkomst samen te brengen. Exotische cocktails, themafeestjes en internationale streetfood.",
 "Het Souke": "Gezellige kroeg in de Hoogstraat met lokale bieren, hapjes, af en toe een optreden en een open, LGBTQ+-vriendelijke sfeer.",
 "De Ware Jacob": "Café met een maritiem interieur uit het begin van de 20e eeuw, zo'n 110 bieren en jazz, blues en rock op de achtergrond.",
 "Kiebooms": "Café aan het De Coninckplein met Belgische klassiekers als steak-friet en live muziek van woensdag tot vrijdag vanaf 21 uur.",
 "Plaza Real": "Borgerhouts nachtcafé met live muziek, cocktails en taart, tot 3 à 5 uur open van donderdag tot zaterdag. Alleen cash.",
 "De Kroon": "Bruin café met meer dan een eeuw geschiedenis: goedkoop bier, live muziek op de meeste vrijdagavonden en een terras aan het kerkplein.",
 "De Klamper": "Volks café in de Offerandestraat, elke dag open van 9 tot 1 uur, met lage prijzen en een feestelijk kerstdecor rond de feestdagen.",
 "BarBob": "Bar in de Kroonstraat met lokale bieren, maar ook limonade en lattes, en een terras.",
 "Bar Bakeliet": "Bar met een vintage interieur en live muziek aan het Laar, met 4,6 sterren op ruim 500 Google-reviews.",
 "Bar Leon": "Herkenbaar aan de zilveren discobal. Populair voor zondagsbrunch, met een speeltuin voor de deur en verrassend goedkoop streekbier.",
 "Beestenbos": "Verrassend rustig voor een plein in het centrum. Elke zondag live concerten van Belgische muzikanten en een grotendeels zelfgemaakte zondagsbrunch.",
 "Café Kamiel": "Café naast het park Hof van Leysen met een speeltuin aan de overkant, dus ideaal met kinderen. Op donderdag all-you-can-eat spaghetti.",
 "Gorillaz": "Café op de Dageraadplaats voor koffie overdag en bier of cocktails 's avonds, met een terras en sport op scherm.",
 "Gitanes": "Bar met live muziek en een overdekt terras met warmtelampen. 's Ochtends croissants, 's avonds cocktails.",
 "The Irish Times Pub": "Ierse pub op de Grote Markt met darts, biljart en live muziek. Volgens recente bronnen is hij mogelijk gesloten, dus check even vooraf.",
 "Beautiful Planet": "Kroeg aan het De Coninckplein met live muziek, die op vrijdag doorgaat tot 5 uur. Naast bier ook warme chocolademelk.",
 "Multatuli": "Klein café in Sint-Andries, alleen 's avonds open van dinsdag tot zaterdag, met prijzen onder de tien euro.",
 "Paloma": "Wijnbar en café naast het MAS, met eten en een terras. Op dinsdag en woensdag gesloten.",
 "De Rui": "Het café om te spelen: flipperkast, darts en pool, aan zachte prijzen.",
 "The Northerner": "Pub met meer dan honderd bieren, waaronder veel craftbier.",
 "Café de Zwoele Zwaluw": "Café aan de Veemarkt met een uitgebreide Belgische bierkaart en een groot scherm voor de match, met 4,7 sterren op Google.",
 "Café Ernst": "Pub aan de Scheldekaaien die bekendstaat om craftbier en natuurwijn, met pasta en nacho's.",
 "Barracuda": "Studentenkroeg op de Ossenmarkt met goedkope shots en cocktails, open tot 3 uur.",
 "Hypothalamus": "Avondbar aan het Mechelseplein met live muziek, open van dinsdag tot zaterdag.",
 "De Pallieter": "Café aan het Mechelseplein met tapbier, een terras en voetbal op tv.",
 "Klimax": "Nachtcafé aan de Stadswaag dat tot 5 uur openblijft, met een terras om mensen te kijken.",
 "La Dolce Vita": "Studentenbar met een feestkelder en DJ's. Elke eerste donderdag van de maand is het Bako-avond.",
 "Cabron": "Bar aan de Kaasrui met live optredens doordeweeks en DJ's in het weekend. Elke dag open van 13 tot 3 uur.",
 # streets / setting (no description found)
 "Café Jozef": "Café aan het Koningin Astridplein, tegenover Centraal Station en naast de Zoo. Ideaal als eerste of laatste halte als je met de trein komt.",
 "Philly's": "Bar in de Grote Pieter Potstraat, het steegje achter de Grote Markt waar CUT en De Vuile Was om de hoek liggen.",
 "Chatleroi": "Café in de Graaf van Hoornestraat, op een zucht van de terrassen van de Marnixplaats.",
 "Bar d'Henri": "Bar in de Montignystraat, aan de rustigere rand van het Zuid.",
 "Pamela": "Café aan de Marnixplaats, het ronde plein rond het Neptunusbeeld waar de terrassen op elkaar aansluiten.",
 "De Buis": "Buurtcafé aan de Marie-Josélaan, ver van het toeristische centrum in het zuiden van Berchem.",
 "Tram 3": "Café aan de Oude Koornmarkt, de oude winkelstraat tussen de Grote Markt en de Groenplaats.",
 "In de Roscam": "Café aan de Vrijdagmarkt, hetzelfde plein als het Museum Plantin-Moretus, een van de oudste drukkerijen ter wereld.",
 "In de stad Aalst": "Café in de Carnotstraat, de drukke multiculturele winkelstraat tussen het Astridplein en Borgerhout.",
 "Heilig Huisken": "Café in de Kloosterstraat, de straat van de antiek- en vintagewinkels. Handig na een namiddag snuffelen.",
 "De Arme Duivel": "Café dat dezelfde naam draagt als zijn straat, de Armeduivelstraat, vlak bij de Meir.",
 "Moby Dick": "Café in de Bredastraat aan de rand van Park Spoor Noord, ideaal na een wandeling in het park.",
 "Zeppelin": "Café aan het Damplein, het pleintje in het hart van de Dambuurt.",
 "Bar du Port": "Havenbar aan de Napoleonkaai, buur van Den Tros, met zicht op de dokken.",
 "Batavier": "Café-restaurant aan de Sint-Laureiskaai, met het water van het Eilandje recht voor de deur.",
 "Boekowski": "Café aan de Bolivarplaats op het Nieuw Zuid, met het justitiepaleis en zijn vlinderdaken als decor.",
 "Borze café": "Café in de Borzestraat, een rustig straatje achter de Lange Nieuwstraat, dicht bij het Hendrik Conscienceplein.",
 "De Prof": "Toepasselijke naam voor een café in de Vekestraat, midden in de buurt van de studenten van de Stadscampus.",
 "Marmite": "Café aan de Torfbrug, het straatje net achter de kathedraal, buur van 't Elfde Gebod.",
 "Bar Lucy": "Bar aan de Koepoortbrug, waar vroeger de Koepoort de stad afsloot, op een paar stappen van de Stadswaag.",
 "De Fonkelarij": "Staat in het bedrijvenregister op hetzelfde adres aan de Koepoortbrug als Bar Lucy.",
 "Kassa 4": "Studentencafé op de Ossenmarkt, midden in de universiteitsbuurt, buur van Barracuda.",
 "'t Lastig Portret": "Café aan het begin van de Blindestraat, de toegangspoort tot de studentenbuurt.",
 "Barbossa": "Café aan de Sint-Jorispoort, buur van Korsakov, voor wie het nachtleven van het Mechelseplein wil verderzetten.",
 "De Kat": "Café in de Wolstraat, het straatje dat de Grote Markt met de Stadswaag verbindt.",
}

F.update({
 "Stan Lee": "Café in de Statiestraat, de levendige winkelstraat van Berchem richting het station.",
 "Villegas": "Café in de Uitbreidingstraat in Berchem, een eind van de drukte van het centrum.",
 "De Valk": "Café in de Seefhoek, een paar straten van de Kerkstraat.",
 "'t Werkhuys": "Café in Borgerhout extra muros, voorbij de Ring.",
 "Den Dammer": "Café aan het Damplein, met Zeppelin als directe buur.",
 "Bato Batu": "Café vlak bij de Lange Nieuwstraat, naast het Borze café.",
 "Zorro": "Bar aan het Hendrik Conscienceplein, schuin tegenover De Zwaan.",
 "Spoor 8": "Studentenbar op de Ossenmarkt, tussen Kassa 4 en Barracuda.",
 "Copain": "Café op de Ossenmarkt, het derde studentencafé op hetzelfde plein.",
 "ABC": "Zaak aan het De Coninckplein in de Seefhoek, op de poster een groot knooppunt."})
d = json.load(open('data.json'))
L = {l['id']: l['s'] for l in d['lines']}
missing = []
for s in d['stations']:
    n = s['n']
    if n in F: s['t'] = F[n]
    elif n in B: s['t'] = B[n]
    elif not s['a']:
        seq = L[s['l'][0]]; i = seq.index(n)
        nb = [seq[j] for j in (i-1, i+1) if 0 <= j < len(seq) and st_ok(seq[j])] if False else [seq[j] for j in (i-1, i+1) if 0 <= j < len(seq)]
        s['t'] = f"Van {n} vond ik online geen adres of beschrijving, dus de plek op de kaart is geschat tussen {' en '.join(dict.fromkeys(nb))}."
    else:
        missing.append(n); s['t'] = None
texts = [s['t'] for s in d['stations']]
print("missing", missing, "| unique", len(set(texts)), "/", len(texts))
import re
sent = [x.strip() for t in texts if t for x in re.split(r'(?<=[.!?])\s+', t)]
from collections import Counter
print("repeated sentences:", [x for x, c in Counter(sent).items() if c > 1])
print("line mentions:", [s['n'] for s in d['stations'] if s['t'] and re.search(r'\blijn', s['t'])])
json.dump(d, open('data.json', 'w'), ensure_ascii=False)
# feature tags from the researched texts
import re as _re
TAGS = {"terras":r"terras","muziek":r"live muziek|jazz|optred|concert|DJ","bier":r"bier|tap|brouw|craft|jenever","cocktails":r"cocktail","laat":r"tot [2-6] uur|nacht|laat","eten":r"spaghetti|pasta|tapas|lunch|brunch|steak|pizza|kaas|omelet|eten|lasagne|nacho|bitterbal|croissant","student":r"student"}
for s in d['stations']:
    t = s['t'] or ''
    s['f'] = [k for k, rx in TAGS.items() if _re.search(rx, t, _re.I)]
json.dump(d, open('data.json', 'w'), ensure_ascii=False)
from collections import Counter as _C
print(_C(f for s in d['stations'] for f in s['f']))
