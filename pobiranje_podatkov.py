import orodja
import re

bi_res_prenesel_strani = False
bi_res_poiskal_podatke = False

json_datoteka = "url.json"
mapa_podatkov = "zajeti_podatki_igre"


vzorec_id = re.compile(
    r'id=(?P<id>(\d{6}))',
    flags=re.DOTALL
)

vzorec_naslov = re.compile(
    r'<h1>(?P<naslov>(.*?))</h1>',
    flags=re.DOTALL
)

vzorec_platforma = re.compile(
    r'<span class="platform">.*?    (?P<platforma>(\S[^/]*?))\s{2}',
    flags=re.DOTALL
)

vzorec_studio = re.compile(
    r'<a href="[\w/-]*?"  >\s+?(?P<studio>(\S.*?))\s*?</a>',
    flags=re.DOTALL
)

vzorec_mesec_in_leto = re.compile(
    r'<span class="data" >(?P<mesec>(\w{3})).*?(?P<leto>(\d{4}))</span>',
    flags=re.DOTALL
)

vzorec_metascore = re.compile(
    r'<span>(?P<metascore>(\d+))</span></div>',
    flags=re.DOTALL
)

vzorec_st_glasov_metascore = re.compile(
    r'>\s+?(?P<st_glasov_metascore>(\d+))\s+?</span> Critic Reviews',
    flags=re.DOTALL
)

vzorec_userscore = re.compile(
    r'<div class="metascore_w user.*?">(?P<userscore>(\d\.?\d))</div>',
    flags=re.DOTALL
)

vzorec_st_glasov_userscore = re.compile(
    r'/user-reviews">(?P<st_glasov_userscore>(\d+?)) Ratings',
    flags=re.DOTALL
)

vzorec_opis_dolg = re.compile(
    r'<span class="blurb blurb_expanded">(?P<opis>(.*?))</span>',
    flags=re.DOTALL
)

vzorec_opis_kratek = re.compile(
    r'<span class="data">\s+?<span>(?P<opis>(.*?))</span>',
    flags=re.DOTALL
)

vzorec_zanri_grobi = re.compile(
    r'<span class="label">Genre\(s\): </span>(?P<zanri>(.*?))</li>',
    flags=re.DOTALL
)

vzorec_zanri_fini = re.compile(
    r' >(.*?)</span>',
    flags=re.DOTALL
)

vzorec_oznaka = re.compile(
    r'<span class="label">Rating:</span>.*?>(?P<oznaka>(.*?))</span>',
    flags=re.DOTALL
)

vzorec_st_igralcev = re.compile(
    r'<span class="label"># of players:</span>.*?>(?P<st_igralcev>(.*?))</span>',
    flags=re.DOTALL
)

def prenos_strani(indeks, url_rep, mapa):
    url = 'https://www.metacritic.com' + url_rep
    orodja.url_v_html(url, mapa, f"{indeks}.html")

def jedro_iz_strani(stran):
    '''Vrne le del strani, kjer se nahajajo podatki.'''
    vzorec = re.compile(r'<h1>.*?More Details and Credits', re.DOTALL)
    return re.search(vzorec, stran).group(0)

def ciscenje_st_igralcev(niz):
    kandidati = [kand for kand in niz.split() if not kand.isalpha()]
    if not kandidati:
        return 1
    stevila = []
    for kand in kandidati:
        stevila += kand.split("-")
    return max([int(s) for s in stevila])

def ciscenje_opisa(niz):
    flag = True
    cisti_niz = ""
    for znak in niz:
        if znak in "[<":
            flag = False
        elif znak in "]>":
            flag = True
        elif flag:
            cisti_niz += znak
    return cisti_niz.rstrip().lstrip()

def igra_iz_jedra(jedro_strani):
    igra = {}
    igra["id"] = int(vzorec_id.search(jedro_strani).group("id"))
    igra["naslov"] = vzorec_naslov.search(jedro_strani).group("naslov")
    igra["platforma"] = vzorec_platforma.search(jedro_strani).group("platforma")
    igra["studio"] = vzorec_studio.search(jedro_strani).group("studio")
    igra["mesec"] = vzorec_mesec_in_leto.search(jedro_strani).group("mesec")
    igra["leto"] = int(vzorec_mesec_in_leto.search(jedro_strani).group("leto"))
    igra["metascore"] = int(vzorec_metascore.search(jedro_strani).group("metascore"))
    igra["st_glasov_metascore"] = int(vzorec_st_glasov_metascore.search(jedro_strani).group("st_glasov_metascore"))
    igra["userscore"] = float(vzorec_userscore.search(jedro_strani).group("userscore"))
    igra["st_glasov_userscore"] = int(vzorec_st_glasov_userscore.search(jedro_strani).group("st_glasov_userscore"))
    
    oznaka = vzorec_oznaka.search(jedro_strani)
    if oznaka:
        igra["oznaka"] = oznaka.group("oznaka")
    else:
        igra["oznaka"] = None

    stevilo_igralcev = vzorec_st_igralcev.search(jedro_strani)
    if stevilo_igralcev:
        igra["st_igralcev"] = ciscenje_st_igralcev(stevilo_igralcev.group("st_igralcev"))
    else:
        igra["st_igralcev"] = None

    dolg_opis = vzorec_opis_dolg.search(jedro_strani)
    if dolg_opis:
        igra["opis"] = ciscenje_opisa(dolg_opis.group("opis"))
    else:
        igra["opis"] = ciscenje_opisa(vzorec_opis_kratek.search(jedro_strani).group("opis"))

    return igra

def zanri_iz_jedra(jedro_strani):
    id_ = int(vzorec_id.search(jedro_strani).group("id"))
    zanri = re.findall(vzorec_zanri_fini, vzorec_zanri_grobi.search(jedro_strani).group(0))
    zanri_brez_ponovitve = []
    for zanr in zanri:
        if zanr not in zanri_brez_ponovitve:
            zanri_brez_ponovitve.append(zanr)
    return [{"id": id_, "zanr": zanr} for zanr in zanri_brez_ponovitve]

#urlji = orodja.odpri_json(json_datoteka)
#for i in range(316, 317):
#    prenos_strani(i, urlji[i]["url_rep"],mapa_podatkov)
#    print(igra_iz_jedra(jedro_iz_strani(orodja.vsebina_datoteke(mapa_podatkov, f"{i}" + ".html"))))
#    print(" ")

# prenos_strani("108362", "/game/playstation-3/grand-theft-auto-iv", mapa_podatkov)

# print(jedro_iz_strani(orodja.vsebina_datoteke(mapa_podatkov, "160751.html")))

# print(igra_iz_jedra(jedro_iz_strani(orodja.vsebina_datoteke(mapa_podatkov, "108362.html"))))

# print(igra_iz_jedra(jedro_iz_strani(orodja.vsebina_datoteke(mapa_podatkov, "108362.html"))))

# print(zanri_iz_jedra(jedro_iz_strani(orodja.vsebina_datoteke(mapa_podatkov, "316.html"))))