import orodja
import re

bi_res_prenesel_strani = False
stevilo_strani = 100
json_datoteka = "url.json"
mapa_podatkov = "zajeti_podatki_url"

def prenos_strani(bi_res_prenesel_strani, stevilo_strani):
    if bi_res_prenesel_strani:
        for i in range(stevilo_strani):
            orodja.url_v_html(f"https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?view=detailed&page={i}", mapa_podatkov, f"igre_od_{i * 100 + 1}_do_{(i + 1) * 100}.html")
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

# print(blok_iz_strani(orodja.vsebina_datoteke(mapa_podatkov, "test.html"))[0])
# print(slovar_iz_bloka(blok_iz_strani(orodja.vsebina_datoteke(mapa_podatkov, "test.html"))[1]))

prenos_strani(bi_res_prenesel_strani, stevilo_strani)

# orodja.zapisi_json([1,2,3], "", json_datoteka)

print(pridobivanje_podatkov_s_strani(mapa_podatkov, "igre_od_0_do_99.html") * 100)