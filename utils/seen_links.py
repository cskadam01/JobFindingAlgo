from pathlib import Path

# Project root directory (JobFindingAlgo)
BASE_DIR = Path(__file__).resolve().parent.parent

# Data directory where seen links are stored
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


def _get_file_path(filename="seen_jobs.txt"):
    return DATA_DIR / filename


def load_seen_links(filename="seen_jobs.txt"):
    file_path = _get_file_path(filename)
    try:
        with file_path.open("r", encoding="utf-8") as f:
            lines = f.read().splitlines()
            return set(lines)
    except FileNotFoundError:
        return set()


def append_seen_link(relative_link, filename="seen_jobs.txt"):
    file_path = _get_file_path(filename)
    with file_path.open("a", encoding="utf-8") as f:
        f.write(relative_link + "\n")