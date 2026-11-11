import json, re

# Short notes: only things that are well known or came up in the sources. Others get a neighbourhood line.
B = {
 "Kulminator": "Legendarisch biercafé met een van de grootste kaarten van gerijpte en vintage bieren ter wereld. Bierliefhebbers reizen er speciaal voor naar Antwerpen.",
 "Paters Vaetje": "Piepklein café aan de voet van de kathedraal, met een lange bierkaart en een terras met zicht op de toren.",
 "Den Engel": "Eén van de bekendste bruine cafés van de stad, op de Grote Markt. Hét adres voor een bolleke De Koninck, met een publiek dat van advocaat tot havenarbeider gaat.",
 "11e Gebod": "Het café vol heiligenbeelden en religieuze kitsch, vlak naast de kathedraal. Je drinkt er letterlijk tussen honderden beelden.",
 "De Duifkens": "Klassiek bruin café aan de Graanmarkt, vlak bij de theaters. Een vaste stek voor acteurs en theaterpubliek.",
 "De Varkenspoot": "Buur van De Duifkens aan de Graanmarkt. Samen vormen ze een klein stukje cafégeschiedenis vlak bij het theaterplein.",
 "Café Pelikaan": "Bruin café op de Melkmarkt, tussen de Grote Markt en de kathedraal. Een vaste waarde die tot laat open blijft.",
 "De Muze": "Jazzcafé op de Melkmarkt met regelmatig live jazz, schuin tegenover Pelikaan.",
 "Quinten Matsijs": "Gaat door als het oudste café van Antwerpen, met een geschiedenis die tot in de 16e eeuw teruggaat.",
 "Boer van Tienen": "Bruin café op het Mechelseplein, al decennia een vaste stek voor studenten en artiesten. Het plein ligt vol terrassen.",
 "De Pallieter": "Eén van de cafés rond het Mechelseplein, waar de terrassen naast elkaar liggen.",
 "Hypothalamus": "Café aan het Mechelseplein, buur van Boer van Tienen en De Pallieter.",
 "Hopper": "Jazzcafé op het Zuid met geregeld live jazz, vlak bij het KMSKA.",
 "Café Beveren": "Volks bruin café aan de Vlasmarkt met een werkend dansorgel. Als het orgel speelt, wordt er gedanst.",
 "De Vagant": "Jenevercafé met een indrukwekkende kaart aan Belgische en Nederlandse jenevers.",
 "Dr. Beer": "Craftbeerbar op het Eilandje, met tapbier dat regelmatig wisselt.",
 "Bier Central": "Biercafé vlak bij Centraal Station met honderden Belgische bieren op de kaart.",
 "Kelly's Irish Pub": "Ierse pub op De Keyserlei, een vaste waarde voor voetbal op tv en Guinness.",
 "The Irish Times Pub": "Ierse pub op de Grote Markt.",
 "Witzli-Poetzli": "Eigenzinnig café achter de kathedraal dat vooral bij locals geliefd is.",
 "Oud Arsenaal": "Ouderwets bruin café met vriendelijke prijzen en een degelijke bierkaart, een paar stappen van de Meir.",
 "K. Zeppos": "Café-brasserie op het Vleminckveld, genoemd naar de tv-held Kapitein Zeppos.",
 "Kassa 4": "Studentencafé op de Ossenmarkt, midden in de universiteitsbuurt.",
 "Barracuda": "Studentencafé op de Ossenmarkt.",
 "Papa Jos": "Café in de Blindestraat, in de studentenbuurt rond de Ossenmarkt.",
 "Dansing Chocola": "Café-brasserie op de Kloosterstraat met een eclectisch interieur en een populair terras.",
 "ZeeZicht": "Café op de Dageraadplaats in Zurenborg, met een groot terras op het plein.",
 "Gorillaz": "Café op de Dageraadplaats, het levendige pleintje van Zurenborg.",
 "De Zure": "Café op de Dageraadplaats in Zurenborg.",
 "Café Moeskop": "Café op de Dageraadplaats, waar je op een zomeravond van terras naar terras kan wandelen.",
 "Den Draak": "Buurtcafé op de Draakplaats in Zurenborg.",
 "The Joker": "Comedycafé op de Kleine Markt, al twintig jaar een podium voor stand-upcomedy.",
 "CUT": "Bar in de Grote Pieter Potstraat die zich profileert als female safe space.",
 "Fetish Café": "LGBTQ+-bar in de Kleine Pieter Potstraat.",
 "Hessenhuis": "Café Hessenhuis aan de Falconrui, vlak bij het historische Hessenhuis.",
 "Cabardouche Taproom": "Taproom van Brouwerij Cabardouche: de bieren van het huis vers van de tap.",
 "Spéciale Belge taproom": "Taproom met een focus op Belgische speciaalbieren.",
 "De Seefhoek": "Brouwerijcafé in de Seefhoek, waar het eigen bier gebrouwen wordt.",
 "Beerlovers bar": "Bierbar in de Seefhoek. De naam zegt het al.",
 "Dogma": "Cocktailbar in de Wijngaardstraat, bekend om zijn uitgebreide cocktails.",
 "'t Waagstuk": "Biercafé aan de Stadswaag met een terras op het plein.",
 "Korsakov": "Alternatieve kroeg aan de Sint-Jorispoort die tot laat open blijft.",
 "Bosbar": "De bar van Het Bos, een cultuurplek aan de Ankerrui. Van koffie tot soep en Bosbier.",
 "Café Des Arts": "Café in Berchem waar ook concerten plaatsvinden.",
 "Café Tati": "Buurtcafé in Berchem dat in de Brussels Times-reeks 'Hidden Belgium' werd uitgelicht.",
 "Rood-Wit": "Café in Berchem. De naam verwijst naar de clubkleuren van Royal Antwerp FC.",
 "De 7 Schaken": "Buurtrestaurant en café in de Lange Beeldekensstraat.",
 "Kid's": "Kid's Rhythm 'n' Blues, een muziekbar op de Grote Markt.",
 "Cinq": "Aperobar aan de Torfbrug, achter de kathedraal.",
 "The Geeky Cauldron": "Themabar voor geeks op de Sint-Jacobsmarkt.",
 "Café Mombasa": "Geliefd buurtcafé op het Moorkensplein in Borgerhout.",
 "De Zwaan": "Café op het Hendrik Conscienceplein, een van de mooiste pleintjes van de stad, voor de Sint-Carolus Borromeuskerk.",
 "'t Licht der Dokken": "Café aan het water op het Eilandje, met een terras langs het dok.",
 "Batavier": "Café-restaurant aan de Sint-Laureiskaai op het Eilandje.",
 "Vitrin": "Café op de Marnixplaats, het terrassenplein van het Zuid rond het Neptunusbeeld.",
 "Pamela": "Café op de Marnixplaats op het Zuid.",
 "Baron": "Café op de Marnixplaats op het Zuid.",
 "Den Tweede zit": "Café op de Bolivarplaats, tegenover het justitiepaleis.",
 "Boekowski": "Café op de Bolivarplaats, vlak bij het justitiepaleis op het Nieuw Zuid.",
}

def buurt(a, n):
    if not a: return None
    if "Berchem" in a: return "Berchem"
    if "Borgerhout" in a: return "Borgerhout"
    z = ["Dageraadplaats", "Draakplaats", "Tramplein", "Isabellalei"]
    if any(s in a for s in z): return "Zurenborg"
    zu = ["Marnixplaats", "Leopold De Waelstraat", "Graaf van Hoornestraat", "Bolivarplaats", "Montignystraat", "Pacificatiestraat", "Kloosterstraat", "Riemstraat", "Troonplaats", "Markgravelei"]
    if any(s in a for s in zu): return "Zuid"
    e = ["Napoleonkaai", "Van Schoonbekeplein", "Adriaan Brouwerstraat", "Verbindingsdok", "Sint-Laureiskaai", "Ankerrui", "Falconrui"]
    if any(s in a for s in e): return "Eilandje"
    d = ["Damplein", "Bredastraat", "Noordschippersdok", "Ellermanstraat"]
    if any(s in a for s in d): return "Dam"
    s2 = ["Kerkstraat", "Offerandestraat", "Diepestraat", "Rotterdamstraat", "De Coninckplein", "Carnotstraat", "Lange Beeldekensstraat"]
    if any(s in a for s in s2): return "Seefhoek"
    if any(s in a for s in ["Sint-Andriesplaats", "Lange Vlierstraat"]): return "Sint-Andries"
    if any(s in a for s in ["Ossenmarkt", "Blindestraat", "Sint-Jacobsmarkt", "Vekestraat"]): return "Studentenbuurt"
    if any(s in a for s in ["Astridplein", "Keyserlei"]): return "Stationsbuurt"
    if any(s in a for s in ["Mechelseplein", "Vleminckveld", "Sint-Jorispoort", "Leopoldplaats", "Schermersstraat", "Armeduivelstraat", "Graanmarkt", "Pijpelincx", "Oudevaartplaats", "Kleine Markt"]): return "Theaterbuurt"
    return "Centrum"

d = json.load(open('data.json'))
for s in d['stations']:
    s['b'] = buurt(s['a'], s['n'])
    s['t'] = B.get(s['n'])
json.dump(d, open('data.json', 'w'), ensure_ascii=False)
print(sum(1 for s in d['stations'] if s['t']), "met uitleg van", len(d['stations']))
