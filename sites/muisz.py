import requests
from bs4 import BeautifulSoup
from utils.seen_links import *

BASE_URL = "https://muisz.hu"


def read_muisz_detail(relativelink):
    full_url = BASE_URL + relativelink
    response = requests.get(full_url)

    soup = BeautifulSoup(response.text, "html.parser")

    content_col = soup.find("article", class_="ContentColumn")
    if content_col is not None:
        job_desc = content_col.get_text(" ", strip=True)
    else:
        job_desc = ""

    
    details = soup.find("div", class_="JobDetails")
    job_place = ""
    job_lang = ""
    job_wage = ""

    if details is not None:
        rows = details.find_all("div", class_="JobInfoRow")
        for row in rows:
            title_div = row.find("div", class_="JobPropertyTitle")
            value_div = row.find("div", class_="JobPropertyValue")
            if not title_div or not value_div:
                continue

            title_text = title_div.get_text(" ", strip=True)
            value_text = value_div.get_text(" ", strip=True)

            if title_text.startswith("Helyszín"):
                job_place = value_text
            elif title_text.startswith("Elvárt nyelvtudás"):
                job_lang = value_text
            elif title_text.startswith("Bérezés"):
                job_wage = value_text

    return {
        "job_desc": job_desc,
        "job_place": job_place,
        "job_lang": job_lang,
        "job_wage": job_wage,
    }






def read_muisz ():
    link = BASE_URL + "/diakmunkaink?locations=10&categories=3"

    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = soup.find_all("div", class_="col-12 col-md-6 col-lg-4")

    seen_links = load_seen_links("seen_jobs_muisz.txt")
    jobs_collected = []

    for job in jobs:
        title_cont = job.find("div", class_="JobDetails")
        if title_cont is None:
            continue
        title_header = title_cont.find("h6")
        if title_header is None:
            continue
        title = title_header.get_text(strip=True)

                # Megnézem gomb linkje
        link_tag = title_cont.find("a", class_="link-button")
        if link_tag is None:
            continue

        relative_link = link_tag.get("href")
        if relative_link is None:
            continue

        if relative_link in seen_links:
            continue

        desc = read_muisz_detail(relative_link)

        job_data = {
            "source": "muisz",
            "title": title,
            "link": BASE_URL + relative_link,
            "desc": desc["job_desc"],
            "lang": desc["job_lang"],
            "place": desc["job_place"],
            "wage": desc["job_wage"],
        }

        jobs_collected.append(job_data)

        append_seen_link(relative_link, "seen_jobs_muisz.txt")
        seen_links.add(relative_link)

    return jobs_collected
