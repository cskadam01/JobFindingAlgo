import requests
from bs4 import BeautifulSoup
from utils.seen_links import *

BASE_URL = "https://schonherz.hu"

def read_schonherz_detail(relative_link):
    full_url = BASE_URL + relative_link
    response = requests.get(full_url)
    soup = BeautifulSoup(response.text, "html.parser")

    details = soup.find("div", id="ad-details")
    if details is None:
        return {
            "job_desc": "",
            "job_lang": "",
            "job_place" : ""
        }

    # 1) Leírás (első span)
    desc_span = details.find("span")
    if desc_span is not None:
        job_desc = desc_span.get_text(" ", strip=True)
    else:
        job_desc = ""

    # 2) Szükséges nyelvtudás (h4 + utána span)
    lang_header = details.find("h4", string="Szükséges nyelvtudás")
    if lang_header is not None:
        lang_span = lang_header.find_next_sibling("span")
        if lang_span is not None:
            job_lang = lang_span.get_text(" ", strip=True)
        else:
            job_lang = ""
    else:
        job_lang = ""

    place_header = details.find("h4", string="Munkavégzés helye")
    if place_header is not None:
        place_span = place_header.find_next_sibling("span")
        if place_span is not None:
            job_place = place_span.get_text(" ", strip=True)
        else:
            job_place = ""
    else:
        job_place = ""
        
    
    wage_header = details.find("h4", string="Fizetés")
    if wage_header is not None:
        wage_span = wage_header.find_next_sibling("span")
        if wage_span is not None:
            job_wage = wage_span.get_text(" ", strip=True)
        else:
            job_wage = ""
    else:
        job_wage = ""
    

    return {
        "job_desc": job_desc,
        "job_lang": job_lang,
        "job_place": job_place,
        "job_wage": job_wage
    }

def read_schonherz():
    # Kivesszük a schonherz URL-t a dictionaryből
    link = BASE_URL + "/diakmunkak/budapest/fejleszto---tesztelo"

    # HTTP GET a listázó oldalra
    response = requests.get(link)

    # HTML → BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Összes álláskártya (div.col-md-8)
    jobs = soup.find_all("div", class_="col-md-8")

    seen_links = load_seen_links()

    jobs_collected = []  


    # Végigmegyünk az összes kártyán
    for job in jobs:
        # Megkeressük benne a h4 taget
        title_container = job.find("h4")
        if title_container is None:
            continue

        # h4-en belüli a tag (cím + link)
        a_tag = title_container.find("a")
        if a_tag is None:
            continue

        # Cím
        title = a_tag.get_text(strip=True)

        # Relatív link a részletes oldalra
        relative_link = a_tag.get("href")
        if relative_link is None:
            continue

        # Ha már láttuk ezt az állást korábban, átugorjuk
        if relative_link in seen_links:
            continue

        # INNENTŐL EZ EGY ÚJ ÁLLÁS
       

        # Részletes oldal szövegének lekérése
        desc = read_schonherz_detail(relative_link)

        job_data = {
            "source": "schonherz",
            "title": title,
            "link": BASE_URL + relative_link,
            "desc": desc["job_desc"],
            "lang": desc["job_lang"],
            "place": desc["job_place"],
            "wage": desc["job_wage"],
        }
        jobs_collected.append(job_data)


        # Elmentjük, hogy ezt az állást már láttuk
        append_seen_link(relative_link, "seen_jobs_schonherz.txt")
        seen_links.add(relative_link)
    
    return jobs_collected


