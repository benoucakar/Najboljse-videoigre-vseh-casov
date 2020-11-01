import orodja
import re

bi_res_prenesel_strani = False
bi_res_poiskal_podatke = False

json_datoteka = "url.json"
mapa_podatkov = "zajeti_podatki_igre"

# Definiramo funkcije

class Igra():
    def __init__(self):
        self.id = 0
        self.naslov = ""
        self.platforma = ""
        self.studio = ""
        self.mesec_izida = ""
        self.leto_izida = ""
        self.metascore = 0
        self.st_glasov_metascore = 0
        self.userscore = 0
        self.st_glasov_userscore = 0
        self.opis = ""
        self.zanri = []
        self.oznaka = ""
        self.st_igralcev = ""

def prenos_strani(id, url_rep, mapa):
    url = 'https://www.metacritic.com' + url_rep
    orodja.url_v_html(url, mapa, f"{id}.html")

def jedro_iz_strani(stran):
    '''Vrne le del strani, kjer se nahajajo podatki.'''
    vzorec = re.compile(r'<h1>.*?</div>\s+</div>\s+</div>\s+</div>\s+<div class="summary_trailer">', re.DOTALL)
    return re.search(vzorec, stran).group(0)

# prenos_strani("108362", "/game/playstation-3/grand-theft-auto-iv", mapa_podatkov)

# print(jedro_iz_strani(orodja.vsebina_datoteke(mapa_podatkov, "108362.html")))