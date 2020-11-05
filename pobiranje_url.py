import orodja
import re

bi_res_prenesel_strani = True
bi_res_poiskal_podatke = True

stevilo_strani = 100
json_datoteka = "url.json"
mapa_podatkov = "zajeti_podatki_url"


# Pomožne funkcije


def prenos_strani(potrditev_prenosa_strani, stevilo_strani):
    '''Pobere izbrano število spletnih strani in jih shrani v HTML.'''
    if potrditev_prenosa_strani:
        for i in range(stevilo_strani):
            orodja.url_v_html(
                f"https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?view=detailed&page={i}",
                 mapa_podatkov, f"igre_od_{i * 100}_do_{i * 100 + 99}.html"
                 )
        print("Končano!")


def bloki_s_strani(stran):
    '''Stran razbije na bloke in jih shrani v seznam.'''
    vzorec = re.compile(r'<input type="checkbox".*?</td>', re.DOTALL)
    return re.findall(vzorec, stran)


def slovar_iz_bloka(blok):
    '''Iz bloka pobere podatke in jih vrne v obliki slovarja.''' 
    vzorec = re.compile(r'<input type="checkbox" id="(?P<id>(\d*))".*?<a href="(?P<url_rep>([\(\)!\+/\w-]*))', re.DOTALL)
    return re.search(vzorec, blok).groupdict()


def podatki_s_strani(mapa_podatkov, stran):
    '''Iz prenešene strani izlušči podatke.'''
    seznam_blokov = bloki_s_strani(orodja.odpri_html(mapa_podatkov, stran))
    return [slovar_iz_bloka(blok) for blok in seznam_blokov]


def podatki_v_json(potrditev_iskanja_podatkov, stevilo_strani, mapa_podatkov, ime_json_datoteke):
    '''Izlušči podatke iz vseh prenešenih strani in jih shrani v JSON datoteko.'''
    if potrditev_iskanja_podatkov:
        seznam_podatkov = []
        for i in range(stevilo_strani):
            podatki = podatki_s_strani(mapa_podatkov, f"igre_od_{i * 100}_do_{i * 100 + 99}.html")
            seznam_podatkov += podatki
        orodja.zapisi_json(seznam_podatkov, ime_json_datoteke)
        print("Podatki so bili uspešno pridobljeni!")


# Skripta


prenos_strani(bi_res_prenesel_strani, stevilo_strani)

podatki_v_json(bi_res_poiskal_podatke, stevilo_strani, mapa_podatkov, json_datoteka)