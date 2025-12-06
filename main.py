from sites.schonherz import read_schonherz
from sites.muisz import read_muisz
from utils.converter import convert_to_xlsx
from utils.relevance import is_relevant

def main():
    all_jobs = []

    all_jobs.extend(read_schonherz())
    all_jobs.extend(read_muisz())

    convert_to_xlsx(all_jobs)

    

    relevant_jobs = [job for job in all_jobs if is_relevant(job)]

    print("Összes új állás:", len(all_jobs))
    print("Releváns új állások:", len(relevant_jobs))

    # Debug: nézzük meg a relevánsakat
    for job in relevant_jobs:
        print(f"- {job['source']} | {job['title']} -> {job['link']}")




if __name__ == "__main__":
    main()