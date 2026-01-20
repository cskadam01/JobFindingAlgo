# Convert collected job data to Excel
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

EXCEL_PATH = DATA_DIR / "jobs.xlsx"


def convert_to_xlsx(jobs):
    # if no new jobs, do nothing
    if not jobs:
        print("No new jobs to export")
        return
    
    for job in jobs:
        # Optional manual label (you may fill this later)
        job.setdefault("is_relevant", None)

        # Ensure AI columns exist
        job.setdefault("ai_feedback", None)
        job.setdefault("ai_recommendation_1_10", None)

        # If your scorer wrote results under other keys (e.g. ml_score / ml_prob),
        # copy them into the Excel columns so they actually get exported.
        ms = job.get("ml_score")
        mp = job.get("ml_prob")

        # Fill recommendation (1–10) if missing
        if job.get("ai_recommendation_1_10") is None:
            raw = ms if ms is not None else mp
            if raw is not None:
                # If it's a 0..1 value, scale to 1..10
                if isinstance(raw, (int, float)) and 0 <= raw <= 1:
                    job["ai_recommendation_1_10"] = int(round(raw * 10))
                # If it's already 0..10, keep it
                elif isinstance(raw, (int, float)) and 0 <= raw <= 10:
                    job["ai_recommendation_1_10"] = int(round(raw))
                else:
                    job["ai_recommendation_1_10"] = raw

        # Fill feedback text if missing
        if job.get("ai_feedback") is None:
            parts = []
            if ms is not None:
                parts.append(f"ml_score={ms}")
            if mp is not None:
                parts.append(f"ml_prob={mp}")
            job["ai_feedback"] = ", ".join(parts) if parts else None

    new_df = pd.DataFrame(jobs)

    # Ensure consistent columns even if some rows are missing them
    required_cols = ["ai_feedback", "ai_recommendation_1_10", "is_relevant"]
    for col in required_cols:
        if col not in new_df.columns:
            new_df[col] = None


    if EXCEL_PATH.exists():
        old_df = pd.read_excel(EXCEL_PATH)

        # Backfill columns into existing Excel if the file was created before these fields existed
        for col in ["ai_feedback", "ai_recommendation_1_10", "is_relevant"]:
            if col not in old_df.columns:
                old_df[col] = None

        # merge + drop duplicates by link
        combined_df = pd.concat([old_df, new_df], ignore_index=True)
        combined_df.drop_duplicates(subset="link", keep="last", inplace=True)
    else:
        combined_df = new_df

    combined_df.to_excel(EXCEL_PATH, index=False)

    print(f"Exported {len(new_df)} new jobs")
    print(f"Total jobs in file: {len(combined_df)}")

    return jobs