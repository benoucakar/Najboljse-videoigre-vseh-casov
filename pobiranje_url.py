import orodja
import re

bi_res_prenesel_strani = False
bi_res_poiskal_podatke = False

stevilo_strani = 100
json_datoteka = "url.json"
mapa_podatkov = "zajeti_podatki_url"

def prenos_strani(bi_res_prenesel_strani, stevilo_strani):
    if bi_res_prenesel_strani:
        for i in range(stevilo_strani):
            orodja.url_v_html(f"https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?view=detailed&page={i}", mapa_podatkov, f"igre_od_{i * 100}_do_{i * 100 + 99}.html")
        print("Končano!")

def bloki_iz_strani(stran):
    vzorec = re.compile(r'<input type="checkbox".*?</td>', re.DOTALL)
    return re.findall(vzorec, stran)

def slovar_iz_bloka(blok):
    vzorec = re.compile(r'<input type="checkbox" id="(?P<id>(\d*))".*?<a href="(?P<url_rep>([/\w-]*))', re.DOTALL)
    return re.search(vzorec, blok).groupdict()

def pridobivanje_podatkov_s_strani(mapa_podatkov, stran):
    seznam_blokov = bloki_iz_strani(orodja.vsebina_datoteke(mapa_podatkov, stran))
    return [slovar_iz_bloka(blok) for blok in seznam_blokov]

def podatki_v_json(bi_res_poiskal_podatke, stevilo_strani, mapa_podatkov, ime_json_datoteke):
    if bi_res_poiskal_podatke:
        seznam_podatkov = []
        for i in range(stevilo_strani):
            podatki = pridobivanje_podatkov_s_strani(mapa_podatkov, f"igre_od_{i * 100}_do_{i * 100 + 99}.html")
            seznam_podatkov += podatki
        orodja.zapisi_json(seznam_podatkov, ime_json_datoteke)

prenos_strani(bi_res_prenesel_strani, stevilo_strani)

podatki_v_json(bi_res_poiskal_podatke, 100, mapa_podatkov, json_datoteka)