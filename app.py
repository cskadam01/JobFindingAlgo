from app import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path
import json

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
LABELS_PATH = DATA_DIR / "labels.json"


def load_labels() -> dict:
    if not LABELS_PATH.exists():
        return {}
    return json.loads(LABELS_PATH.read_text(encoding="utf-8"))


def save_labels(labels: dict) -> None:
    LABELS_PATH.write_text(json.dumps(labels, ensure_ascii=False, indent=2), encoding="utf-8")


@app.get("/")
def root():
    return {"status": "ok", "service": "jobfinding-backend"}


@app.get("/label", response_class=HTMLResponse)
def label(job_id: str, label: int):
    # label: 1 = érdekel, 0 = nem érdekel
    labels_db = load_labels()
    labels_db[job_id] = label
    save_labels(labels_db)

    return f"""
    <h3>Köszi!</h3>
    <p>Mentve: job_id=<b>{job_id}</b>, label=<b>{label}</b></p>
    """