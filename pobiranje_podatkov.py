import orodja
import re

bi_res_prenesel_strani = False
bi_res_poiskal_podatke = True

json_datoteka = "url.json"
mapa_podatkov = "zajeti_podatki_igre"
csv_datoteka_igre = "igre.csv"
csv_datoteka_zanri = "zanri.csv"

# Vzorci za regularne izraze

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

vzorec_studio_ob_imenu = re.compile(
    r'<a href="[\!\w/-]*?"  >\s+?(?P<studio>(\S.*?))\s*?</a>',
    flags=re.DOTALL
)

vzorec_studio_na_strani = re.compile(
    r'<span class="label">Developer:</span>.+?<span class="data">.+?(?P<studio>(\S.*?))\s{2}',
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

# Pomožne funkcije

def prenos_strani(indeks, url_rep, mapa_podatkov):
    url = 'https://www.metacritic.com' + url_rep
    orodja.url_v_html(url, mapa_podatkov, f"{indeks}.html")

def prenesi_strani_s_spleta(potrditev_prenosov_strani, json_datoteka, mapa_podatkov, do, od = 0):
    indeksi_in_url = orodja.odpri_json(json_datoteka)
    if potrditev_prenosov_strani:
        for i in range(od, do):
            url_rep = indeksi_in_url[i]["url_rep"]
            prenos_strani(i, url_rep, mapa_podatkov)
        print("Končano!")
            
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
        lep_kand = kand.replace("+", "")
        stevila += lep_kand.split("-")
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
    cisti_niz = re.sub(r'(\*|\\n)', " ", cisti_niz)
    return " ".join(cisti_niz.split())

def igra_iz_jedra(jedro_strani):
    igra = {}
    igra["id"] = int(vzorec_id.search(jedro_strani).group("id"))
    igra["naslov"] = vzorec_naslov.search(jedro_strani).group("naslov")
    igra["platforma"] = vzorec_platforma.search(jedro_strani).group("platforma")

    studio_ob_imenu = vzorec_studio_ob_imenu.search(jedro_strani)
    if studio_ob_imenu:
        igra["studio"] = studio_ob_imenu.group("studio")
    else:
        igra["studio"] = vzorec_studio_na_strani.search(jedro_strani).group("studio")


    igra["mesec"] = vzorec_mesec_in_leto.search(jedro_strani).group("mesec")
    igra["leto"] = int(vzorec_mesec_in_leto.search(jedro_strani).group("leto"))

    metascore = vzorec_metascore.search(jedro_strani)
    if metascore:
        igra["metascore"] = int(metascore.group("metascore"))
    else:
        igra["metascore"] = None
    
    st_glasov_metascore = vzorec_st_glasov_metascore.search(jedro_strani)
    if st_glasov_metascore:
        igra["st_glasov_metascore"] = int(st_glasov_metascore.group("st_glasov_metascore"))
    else:
        igra["st_glasov_metascore"] = None

    userscore = vzorec_userscore.search(jedro_strani)
    if userscore:
        igra["userscore"] = float(userscore.group("userscore"))
    else:
        igra["userscore"] = None
    
    st_glasov_userscore = vzorec_st_glasov_userscore.search(jedro_strani)
    if st_glasov_userscore:
        igra["st_glasov_userscore"] = int(st_glasov_userscore.group("st_glasov_userscore"))
    else:
        igra["st_glasov_userscore"] = None
    
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
        kratek_opis = vzorec_opis_kratek.search(jedro_strani)
        if kratek_opis:
            igra["opis"] = ciscenje_opisa(kratek_opis.group("opis"))
        else:
            igra["opis"] = None

    return igra

def zanri_iz_jedra(jedro_strani):
    id_ = int(vzorec_id.search(jedro_strani).group("id"))
    zanri = re.findall(vzorec_zanri_fini, vzorec_zanri_grobi.search(jedro_strani).group(0))
    zanri_brez_ponovitve = []
    for zanr in zanri:
        if zanr not in zanri_brez_ponovitve:
            zanri_brez_ponovitve.append(zanr)
    return [{"id": id_, "zanr": zanr} for zanr in zanri_brez_ponovitve]

def igre_in_zanri_iz_strani(potrditev_iskanja_podatkov, mapa_podatkov, do, od=0, interval_obvestila = 250):
    if potrditev_iskanja_podatkov:
        igre = []
        zanri = []
        for i in range(od, do):
            if i > 0 and i % interval_obvestila == 0: print(f"Obdelanij je bilo {i} strani.")
            try:
                jedro = jedro_iz_strani(orodja.vsebina_datoteke(mapa_podatkov, f"{i}.html"))
                igre.append(igra_iz_jedra(jedro))
                zanri += zanri_iz_jedra(jedro)
            except Exception:
                print(f"Napaka pri iskanju podatkov v {i}.html")
        
        orodja.zapisi_csv(
            igre,
            ["id", "naslov", "platforma", "studio", "mesec", "leto", "metascore", "st_glasov_metascore",
            "userscore", "st_glasov_userscore", "oznaka", "st_igralcev", "opis"],
            csv_datoteka_igre
        )
        orodja.zapisi_csv(zanri, ["id", "zanr"], csv_datoteka_zanri)
        print("Podatki so bili uspešno pridobljeni!")

# Skripta

prenesi_strani_s_spleta(bi_res_prenesel_strani, json_datoteka, mapa_podatkov, 10000)

igre_in_zanri_iz_strani(bi_res_poiskal_podatke, mapa_podatkov, 1000)


#print(igra_iz_jedra(jedro_iz_strani(orodja.vsebina_datoteke(mapa_podatkov, "1283.html"))))
#prenos_strani(1813, "/game/pc/star-wars-the-old-republic", mapa_podatkov)
#print(jedro_iz_strani(orodja.vsebina_datoteke(mapa_podatkov, "5995.html")))