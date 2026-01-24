from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path
import json
from database.config import engine, Base
import database.models
from fastapi import Depends
from sqlalchemy.orm import Session
from database.config import get_db
from database.models import Label
from fastapi import HTTPException

Base.metadata.create_all(bind=engine)

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
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
def label(job_id: int, label: int, db: Session = Depends(get_db)):
    # label: 1 = érdekel, 0 = nem érdekel
    if label not in (0, 1):
        raise HTTPException(status_code=400, detail="label must be 0 or 1")

    # van már címke ehhez a jobhoz?
    existing = db.query(Label).filter(Label.job_id == job_id).order_by(Label.id.desc()).first()

    if existing:
        existing.label = label
    else:
        db.add(Label(job_id=job_id, label=label))

    db.commit()

    return f"""
    <h3>Köszi!</h3>
    <p>Mentve DB-be: job_id=<b>{job_id}</b>, label=<b>{label}</b></p>
    """
