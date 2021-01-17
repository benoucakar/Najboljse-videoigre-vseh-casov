# Najboljše videoigre vseh časov
V okviru predmeta programiranje 1 sem preučil najbolj priljubljene videoigre.

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
- mesec in leto izzida
- opis in žanre
- oznako in število igralcev
- metascore in število glasov za metascore
- userscore in število glasov za userscore

## O analizi
Analiziral sem podatke, ki so bili sneti 5. 11. 2020.
S pomočjo zajetih podatkov sem skušal odgovoriti na naslednja vprašanja:
- Kateri žanri so najbolj priljubljeni?
- So bolj uspešne enoigralske ali večigralske igre?
- Kateri studii in katere platforme so imeli največ uspešnic in ali tu obstaja kakšna povezava?
- Koliko se razlikujeta mnenji ljudstva in "strokovnjakov"?
- Kaj je bolje, XBOX ONE ali PS4?
- Ali so igre, ki so meni všeč, všeč tudi drugim?

In ogromno drugih vprašanj, ki se jih bom sproti spomnil.
