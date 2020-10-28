import orodja
import re

json_datoteka = "url.json"
mapa_podatkov = "zajeti_podatki_url"

test_url = "https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?view=detailed&page=1"

# orodja.url_v_html(test_url, mapa_podatkov, "test.html")

def blok_iz_strani(stran):
    vzorec = re.compile(r'<input type="checkbox".*?</td>', re.DOTALL)
    return re.findall(vzorec, stran)

def slovar_iz_bloka(blok):
    vzorec = re.compile(r'<input type="checkbox" id="(?P<id>(\d*))".*?<a href="(?P<url_rep>([/\w-]*))', re.DOTALL)
    return re.search(vzorec, blok).groupdict()

# print(blok_iz_strani(orodja.vsebina_datoteke(mapa_podatkov, "test.html"))[0])
# print(slovar_iz_bloka(blok_iz_strani(orodja.vsebina_datoteke(mapa_podatkov, "test.html"))[1]))