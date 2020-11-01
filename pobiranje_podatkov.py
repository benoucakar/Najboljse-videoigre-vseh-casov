import orodja
import re

bi_res_prenesel_strani = False
bi_res_poiskal_podatke = False

json_datoteka = "url.json"
mapa_podatkov = "zajeti_podatki_igre"

# Definiramo funkcije

vzorec_naslov = re.compile(
    r'<h1>(?P<naslov>(.*?))</h1>',
    flags=re.DOTALL
)

vzorec_platforma = re.compile(
    r'<span class="platform">\s+?<a href="[\w/-]*">\s+(?P<platforma>(\S.*?))\s+?</a>',
    flags=re.DOTALL
)

vzorec_studio = re.compile(
    r'<a href="[\w/-]*?"  >\s+?(?P<studio>(\S.*?))\s*?</a>',
    flags=re.DOTALL
)

vzorec_mesec_in_leto = re.compile(
    r'<span class="data" >((?P<mesec>)(\w{3})) \d{2}, (?P<leto>(\d{4}))</span>',
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
    r'<div class="metascore_w user large game positive">(?P<userscore>(\d\.?\d))</div>',
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
    vzorec = re.compile(r'<h1>.*?</div>\s+</div>\s+</div>\s+</div>\s+<div class="summary_trailer">', re.DOTALL)
    return re.search(vzorec, stran).group(0)

# prenos_strani("108362", "/game/playstation-3/grand-theft-auto-iv", mapa_podatkov)

# print(jedro_iz_strani(orodja.vsebina_datoteke(mapa_podatkov, "108362.html")))