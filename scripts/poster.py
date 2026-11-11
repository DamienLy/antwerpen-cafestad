"""Station positions on the original poster (pixels in the 180°-rotated 1600x1200 photo), read off a grid overlay."""
import json
PP = {
 "ABC":(1027,267),"Quinten Matsijs":(578,430),"De Muze":(855,436),"Kid's":(318,540),"Cabron":(578,540),"Tram 3":(742,543),
 "Boer van Tienen":(578,632),"Bar Brul":(810,630),"De Duifkens":(707,738),"Café Des Arts":(888,738),"Izzy Maze":(330,885),"Café Jozef":(1333,690),
 "BAS":(376,232),"Batavier":(430,236),"'t Licht der Dokken":(481,240),"Bar du Port":(532,244),"Den Tros":(581,248),"Dr. Beer":(630,252),
 "Paloma":(678,255),"ZIGZAG":(724,258),"Den Dammer":(771,261),"Zeppelin":(817,264),"Moby Dick":(862,265),"Café Welkom":(908,266),"Cabardouche Taproom":(954,266),
 "Cousteau":(316,186),"Hessenhuis":(316,138),"Bosbar":(316,93),
 "De Kroon":(1115,268),"De Klamper":(1159,270),"De Valk":(1202,272),"De Seefhoek":(1245,276),"BarBob":(1284,308),"Café Mombasa":(1286,348),
 "In de stad Aalst":(1287,389),"'t Werkhuys":(1310,432),"Bar Bakeliet":(1355,432),"Bar Leon":(1400,432),
 "La Dolce Vita":(748,347),"Klimax":(702,345),"'t Waagstuk":(654,343),"De Fonkelarij":(605,340),"De Kat":(573,372),
 "The Geeky Cauldron":(1228,436),"Bato Batu":(1187,436),"Borze café":(1144,436),"De Prof":(1100,436),"Dogma":(1025,428),"The Northerner":(967,434),
 "CUT":(1022,474),"Fetish Café":(1048,532),"De Vuile Was":(1049,570),
 "Barracuda":(1282,650),"Spoor 8":(1250,618),"Kassa 4":(1218,587),"Copain":(1186,552),"Papa Jos":(1153,520),"'t Lastig Portret":(1117,487),
 "Paters Vaetje":(762,432),"Witzli-Poetzli":(708,432),"Marmite":(655,432),
 "Zorro":(456,390),"De Zwaan":(456,342),"Café de Zwoele Zwaluw":(281,288),"Dam 12":(172,330),"Café Ernst":(172,380),"Bar Lucy":(252,425),
 "Café au lait":(255,540),"Den Engel":(180,540),"Dos Cervezas":(108,540),"De 7 Schaken":(48,515),"Café Clodette":(-12,505),
 "The Irish Times Pub":(384,540),"Cinq":(450,540),"11e Gebod":(517,540),"'t Vervolg":(655,540),
 "Café Pelikaan":(795,497),"Beautiful Planet":(905,383),"Beerlovers bar":(936,350),"Kiebooms":(966,320),"Plaza Real":(1063,210),
 "Corso":(870,553),"In de Roscam":(907,553),"Café de Vischmijn":(957,578),"De Ware Jacob":(993,614),"Café Beveren":(1030,650),
 "Het Souke":(1068,686),"Barries":(1106,722),"Philly's":(1131,758),"De Vagant":(1160,790),"Jones&Co":(1188,822),
 "Kelly's Irish Pub":(1248,790),"Bier Central":(1278,757),"Stan Lee":(1030,744),"Cantaloop":(989,744),"Rood-Wit":(948,744),
 "Cabagine":(821,738),"Café Tati":(776,738),"Oud Arsenaal":(624,673),"K. Zeppos":(506,630),"Kulminator":(459,630),"The Joker":(412,630),
 "Baron":(320,680),"Vitrin":(320,718),"Hopper":(320,758),"Chatleroi":(320,798),"Café Plastron":(278,938),"Bar d'Henri":(234,982),"Pamela":(192,1023),
 "Ons Huis":(998,998),"Repos":(998,962),"De Buis":(998,925),"Villegas":(996,888),"Den Draak":(995,840),"Gitanes":(967,810),"Spéciale Belge taproom":(938,778),
 "Café Moeskop":(1165,997),"ZeeZicht":(1128,962),"Gorillaz":(1092,925),"De Zure":(1055,887),"Bobby":(860,692),"Foxy":(838,668),
 "Apropos":(538,690),"Barbossa":(497,728),"Korsakov":(459,768),"Hypothalamus":(418,802),"De Pallieter":(382,843),"Café Kamiel":(329,936),"Den Tweede zit":(329,972),
 "De Varkenspoot":(661,792),"De Arme Duivel":(624,828),"De Rui":(550,892),"De Nieuwe Linde":(513,930),"Boekowski":(476,968),
 "Heilig Huisken":(637,889),"Dansing Chocola":(672,927),"Beestenbos":(709,964),"Multatuli":(746,1000),
}
d = json.load(open('data.json'))
names = {s['n'] for s in d['stations']}
print('missing', sorted(names - set(PP)), 'extra', sorted(set(PP) - names), len(PP))
for s in d['stations']:
    s['pp'] = list(PP[s['n']])
json.dump(d, open('data.json', 'w'), ensure_ascii=False)
