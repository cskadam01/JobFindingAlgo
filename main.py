from sites.schonherz import read_schonherz
from sites.muisz import read_muisz
from utils.converter import convert_to_xlsx
from utils.email_utils import send_job_email
from ai.scorer import score_jobs
import json
from pathlib import Path
import re
from sqlalchemy.orm import Session
from database.models import Label
from database.config import SessionLocal


def emoji_newlines(text: str) -> str:
    # minden emoji elé sortörést tesz (ha nincs)
    return re.sub(r'([\U00010000-\U0010ffff])', r'\n\1', text)

# --- Simple persistent labeling (stored in data/labels.json) ---
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
LABELS_PATH = DATA_DIR / "labels.json"


def load_labels() -> dict:
    if not LABELS_PATH.exists():
        return {}
    try:
        return json.loads(LABELS_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_labels(labels: dict) -> None:
    LABELS_PATH.write_text(json.dumps(labels, ensure_ascii=False, indent=2), encoding="utf-8")


def save_to_db(job: dict, db: Session) -> int:
    from database.models import Job

    allowed = {
        "source", "title", "link", "place", "wage", "desc",
        "ai_score", "ai_feedback"
    }

    data = {k: v for k, v in job.items() if k in allowed}

    existing = db.query(Job).filter(Job.link == data["link"]).first()

    if existing:
        for key, value in data.items():
            setattr(existing, key, value)
        db.commit()
        return existing.id
    else:
        new_job = Job(**data)
        db.add(new_job)
        db.commit()
        db.refresh(new_job)
        return new_job.id


def main():
    all_jobs = []

    all_jobs.extend(read_schonherz())
    all_jobs.extend(read_muisz())

    # 1) Only proceed if we actually collected new jobs
    if not all_jobs:
        print("Nincs új állás.")
        return

    # 2) Score the NEW jobs first (so ai_feedback / ai_recommendation columns get values)
    scored_jobs = score_jobs(all_jobs)


    

    # Map the scorer outputs into the Excel columns you want.
    # Your scorer currently fills ml_score / ml_prob, so we copy them into:
    # - ai_recommendation_1_10 (1-10)
    # - ai_feedback (short text)
    for job in scored_jobs:
        # Fill recommendation (1-10) if missing
        if job.get("ai_recommendation_1_10") is None:
            ms = job.get("ml_score")
            mp = job.get("ml_prob")

            # Prefer ml_score if available, otherwise ml_prob
            raw = ms if ms is not None else mp

            if raw is not None:
                # If it's a 0..1 score, scale to 1..10
                if isinstance(raw, (int, float)) and 0 <= raw <= 1:
                    job["ai_recommendation_1_10"] = int(round(raw * 10))
                # If it's already 0..10, keep it
                elif isinstance(raw, (int, float)) and 0 <= raw <= 10:
                    job["ai_recommendation_1_10"] = int(round(raw))
                else:
                    # Unknown scale -> keep as-is (you can refine later)
                    job["ai_recommendation_1_10"] = raw

        # Fill feedback text if missing
        if job.get("ai_feedback") is None:
            parts = []
            if job.get("ml_score") is not None:
                parts.append(f"ml_score={job.get('ml_score')}")
            if job.get("ml_prob") is not None:
                parts.append(f"ml_prob={job.get('ml_prob')}")
            job["ai_feedback"] = ", ".join(parts) if parts else None

        db = SessionLocal()
        try:
            for job in scored_jobs:
                job_id = save_to_db(job, db)
                job["job_id"] = job_id
        finally:
            db.close()
        



    # 3) Export AFTER scoring so Excel receives the filled AI fields
    convert_to_xlsx(scored_jobs)

    print("ez most ami kell \n", scored_jobs)

    # Send email for each new scored job
    for job in scored_jobs:
        send_job_email(job)
    print("Összes új állás:", len(all_jobs))







if __name__ == "__main__":
    main()