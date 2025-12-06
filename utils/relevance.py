# Egyszerű szabály alapú relevancia szűrő

def is_relevant(job: dict) -> bool:
    """
    Eldönti, hogy egy állás "neked való-e" nagyon egyszerű szabályok alapján.
    Ezt később finomíthatod.
    """
    lang = (job.get("lang") or "").lower()
    title = (job.get("title") or "").lower()
    desc = (job.get("desc") or "").lower()
    place = (job.get("place") or "").lower()

    text = title + " " + desc

    # Pozitív kulcsszavak (amik érdekelnek)
    must_have_any = [
        "python",
        "backend",
        "fejlesztő",
        "developer",
        "full-stack",
        "szoftverfejlesztő",
        "it gyakornok",
        "junior",
        "react",
        "fastapi",
        "flask",
        "sql",
        "ml",
        "typescript",
        "javascirpt"


    ]

    # Egyszerű helyszín szűrés
    if "budapest" not in place and "remote" not in text and "home office" not in text:
        return False



    # Ha egy pozitív kulcsszó sincs benne, akkor nem érdekes
    if not any(keyword in text for keyword in must_have_any):
        return False
    
    

    return True