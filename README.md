# Najboljše videoigre vseh časov
V okviru predmeta Programiranje 1 sem preučil najbolj priljubljene videoigre.

## Navodila za snemanje podatkov
Najprej poženite `pobiranje_url.py`, da snamete in preiščete razporede iger.
Strani se bodo prenesele in podatki o url-jih se bodo shranili v `url.json` datoteko.

Nato poženite `pobiranje_podatkov.py`, da snamete in preiščete posamezne igre.
Strani se bodo prenesle in podatki o igrah in žanrih se bodo shranili v `igre.csv` in `zanri.csv` datoteki.

## O podatkih
Podatke o videoigrah sem zajel s spletne strani [Metacritic](https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?view=detailed).
Preučil sem prvih 10.000, razvrščenih po oceni *metascore* na strani.

Za vsako videoigro sem zajel:
- id, naslov, platformo in studio
- mesec in leto izida
- opis in žanre
- oznako in število igralcev
- metascore in število glasov za metascore
- userscore in število glasov za userscore

## O analizi
Analiziral sem podatke, ki so bili sneti 5. 11. 2020.  

Najprej sem naredil lastno metriko, ki upošteva tako mnenja strokovnjakov kot uporabnikov o kvaliteti videoiger.
S tem glavnim orodjem sem nato preučil pojave v podatkih in preverjal razne hipoteze.

Med drugim sem odgovoril na naslednja vprašanja:
* Koliko se razlikujeta mnenji ljudstva in "strokovnjakov"?
* Kateri studii in katere platforme so imeli največ uspešnic?
* Ali leto in mesec izzida vplivata na uspeh igre? 
* Kako žanr in oznaka vplivata na uspeh igre?
* So bolj uspešne enoigralske ali večigralske igre?

Nazadnje sem spisal še program, ki sprejme igre, ki si jih že igral, in ti na podlagi teh vrne priporočilo, katere igre bi te morda zanimale.
