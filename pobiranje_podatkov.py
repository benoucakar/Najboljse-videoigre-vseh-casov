import orodja
import re

bi_res_prenesel_strani = False
bi_res_poiskal_podatke = False

json_datoteka = "url.json"
mapa_podatkov = "zajeti_podatki_igre"

# Definiramo funkcije

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

vzorec_opis = re.compile(
    r'<span class="blurb blurb_expanded">(?P<opis>(.*?))</span>',
    flags=re.DOTALL
)

vzorec_zanri = re.compile(
    r'<span class="label">Genre\(s\): </span>(?P<zanri>(.*?))</li>',
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
        if znak == "[":
            flag = False
        elif znak == "]":
            flag = True
        elif flag:
            cisti_niz += znak
    return cisti_niz.rstrip().lstrip()




def igra_iz_jedra(stran):
    jedro_strani = jedro_iz_strani(stran)
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
    igra["oznaka"] = vzorec_oznaka.search(jedro_strani).group("oznaka")
    igra["st_igralcev"] = ciscenje_st_igralcev(vzorec_st_igralcev.search(jedro_strani).group("st_igralcev"))
    igra["opis"] = ciscenje_opisa(vzorec_opis.search(jedro_strani).group("opis"))
    return igra

# prenos_strani("108362", "/game/playstation-3/grand-theft-auto-iv", mapa_podatkov)

# print(jedro_iz_strani(orodja.vsebina_datoteke(mapa_podatkov, "108362.html")))

# print(igra_iz_jedra(jedro_iz_strani(orodja.vsebina_datoteke(mapa_podatkov, "108362.html"))))
# 108362
# 108363
# 160692
# 160751
# 160779


# print(igra_iz_jedra(jedro_iz_strani(orodja.vsebina_datoteke(mapa_podatkov, "160751.html"))))