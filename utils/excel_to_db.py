import pandas as pd
from sqlalchemy.orm import Session
from database.config import SessionLocal
from database.models import Job, Label

def to_none(x):
    if pd.isna(x):
        return None
    return x

def main():
    df = pd.read_excel("data/jobs.xlsx")

    print("Oszlopok:", list(df.columns))
    print(df.head(3))

    db: Session = SessionLocal()
    try:
        inserted, updated = 0, 0
        labels_inserted, labels_updated = 0, 0

        for _, row in df.iterrows():
            data = {
                "source": to_none(row.get("source")),
                "title": to_none(row.get("title")),
                "link": to_none(row.get("link")),
                "place": to_none(row.get("place")),
                "wage": to_none(row.get("wage")),
                "desc": to_none(row.get("desc")),
                "ai_score": to_none(row.get("ml_score")),
                "ai_feedback": to_none(row.get("ai_feedback")),
            }

            if not data["link"] or not data["title"]:
                continue

            # --- JOB upsert (link alapján) ---
            existing = db.query(Job).filter(Job.link == data["link"]).first()
            if existing:
                for k, v in data.items():
                    if v is not None:
                        setattr(existing, k, v)
                job_row = existing
                updated += 1
            else:
                job_row = Job(**data)
                db.add(job_row)
                db.flush()  # <<< itt kap ID-t (job_row.id)
                inserted += 1

            # --- LABEL import (Excel oszlop: is_relevant) ---
            is_rel = to_none(row.get("is_relevant"))

            # csak akkor mentünk labelt, ha 0 vagy 1
            if is_rel in (0, 1):
                job_id = job_row.id

                existing_label = (
                    db.query(Label)
                    .filter(Label.job_id == job_id)
                    .order_by(Label.id.desc())
                    .first()
                )

                if existing_label:
                    existing_label.label = int(is_rel)
                    labels_updated += 1
                else:
                    db.add(Label(job_id=job_id, label=int(is_rel)))
                    labels_inserted += 1

        db.commit()
        print(f"Kész. jobs: inserted={inserted}, updated={updated}")
        print(f"Kész. labels: inserted={labels_inserted}, updated={labels_updated}")

    finally:
        db.close()

if __name__ == "__main__":
    main()
