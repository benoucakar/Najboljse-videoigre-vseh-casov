# Prirejeno po datotekah iz predavanj in vaj.

import csv
import json
import os
import requests

default_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


# Prenos spletne strani


def url_v_html(url, mapa, ime_datoteke, headers=default_headers):
    '''Sprejme url in v dano destinacijo shrani HTML datoteko.'''
    try:
        page_content = requests.get(url, headers=headers) 
    except requests.exceptions.ConnectionError:
        print(f"Napaka pri povezovanju na {url}")
        return None
    if page_content.status_code == requests.codes.ok:
        os.makedirs(mapa, exist_ok=True)
        path = os.path.join(mapa, ime_datoteke)
        with open(path, 'w', encoding='utf-8') as file_out:
            file_out.write(page_content.text)
    else:
        print(f"Napaka pri prenosu strani {url}")
        return None


# Pisanje in odpiranje


def vsebina_datoteke(mapa, ime_datoteke):
    '''Vrne niz z vsebino dane datoteke.'''
    with open(os.path.join(mapa, ime_datoteke), encoding='utf-8') as datoteka:
        return datoteka.read()


def zapisi_csv(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    with open(ime_datoteke, 'w', encoding='utf-8') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)


def zapisi_json(objekt, ime_datoteke):
    '''Iz danega objekta ustvari JSON datoteko.'''
    with open(ime_datoteke, 'w', encoding='utf-8') as json_datoteka:
        json.dump(objekt, json_datoteka, indent=4, ensure_ascii=False)


def odpri_json(ime_datoteke):
    '''Odpre dano JSON datoteko.'''
    with open(ime_datoteke, 'r', encoding='utf-8') as json_datoteka: 
            return json.load(json_datoteka)