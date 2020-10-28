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

# prenos_strani("160692", "/game/nintendo-64/the-legend-of-zelda-ocarina-of-time", mapa_podatkov)