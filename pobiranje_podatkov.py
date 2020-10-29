import orodja
import re

bi_res_prenesel_strani = False
bi_res_poiskal_podatke = False

json_datoteka = "url.json"
mapa_podatkov = "zajeti_podatki_igre"

# Definiramo funkcije

def prenos_strani(id, url_rep, mapa):
    url = 'https://www.metacritic.com' + url_rep
    orodja.url_v_html(url, mapa, f"{id}.html")

def jedro_iz_strani(stran):
    '''Vrne le del strani, kjer se nahajajo podatki.'''
    vzorec = re.compile(r'<h1>.*?</div>\s+</div>\s+</div>\s+</div>\s+<div class="summary_trailer">', re.DOTALL)
    return re.search(vzorec, stran).group(0)

# <h1>(?P<naslov>(.*?))</h1>.*?<span class="platform">\s*(?P<platforma>(.*?))\n.*?<a href.*?>\s*?(?P<razvijalec>(\w*?))\s*    

# prenos_strani("108362", "/game/playstation-3/grand-theft-auto-iv", mapa_podatkov)

# print(jedro_iz_strani(orodja.vsebina_datoteke(mapa_podatkov, "108362.html")))