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

    new_df = pd.DataFrame(jobs)

    if EXCEL_PATH.exists():
        old_df = pd.read_excel(EXCEL_PATH)

        # merge + drop duplicates by link
        combined_df = pd.concat([old_df, new_df], ignore_index=True)
        combined_df.drop_duplicates(subset="link", inplace=True)
    else:
        combined_df = new_df

    combined_df.to_excel(EXCEL_PATH, index=False)

    print(f"Exported {len(new_df)} new jobs")
    print(f"Total jobs in file: {len(combined_df)}")