import math
import joblib
from pathlib import Path

# Projekt gyökér mappa (…/JobFindingAlgo)
BASE_DIR = Path(__file__).resolve().parent.parent

# A mentett ML fájlok helye (ezeket a train_model.py hozta létre)
MODEL_PATH = BASE_DIR / "ai" / "model.pkl"
VECTORIZER_PATH = BASE_DIR / "ai" / "vectorizer.pkl"


def score_jobs(jobs):
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)

    for job in jobs:
        title = job.get("title") or ""
        desc = job.get("desc") or ""
        text = f"{title} {desc}".strip()

        vec = vectorizer.transform([text])
        print("vec shape:", vec.shape)
        prob = model.predict_proba(vec)[0][1]
        score = max(1, min(10, math.ceil(prob * 10)))
        print(f" {job.get("title")} AI: {score}/10 (prob={prob:.2f})")
        job["ml_prob"] = float(prob)
        job["ml_score"] = int(score)
    return jobs