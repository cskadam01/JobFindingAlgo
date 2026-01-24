import pandas as pd
from pathlib import Path
from database.config import SessionLocal
from sqlalchemy.orm import Session
from database.models import Job, Label
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "jobs.xlsx"
MODEL_PATH = BASE_DIR / "ai" / "model.pkl"
VECTORIZER_PATH = BASE_DIR / "ai" / "vectorizer.pkl"

def load_training_data():

   

    db: Session = SessionLocal()
    try:
        rows = db.query(Job, Label ).join(Label, Job.id == Label.job_id).all()
        X = []
        y = []
        for job, label in rows:
            title = job.title or ""
            desc = job.desc or ""
            text = title + " " + desc 
            text = text.lower()
            text = text.strip()
            X.append(text)         
            y.append(int(label.label))

        print("0.", X[0][:200])
        print("1.", len(X))
        print(set(y))
        print("pos", sum(v==1 for v in y), "neg", sum(v==0 for v in y))
        print("\n \n \n")
        
        return X, y



    except Exception as e:
        print("Hiba a tanulási db connectionel", e)

    

def build_tfidf(X):
    vectorizer = TfidfVectorizer()
    X_vec = vectorizer.fit_transform(X)
    print("TF-IDF mátrix mérete:", X_vec.shape)
    return vectorizer, X_vec

if __name__ == "__main__":
    X, y = load_training_data()
    vectorizer, X_vec = build_tfidf(X)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_vec, y)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    print("Saved:", MODEL_PATH.name, "and", VECTORIZER_PATH.name)

    # === TESZT: betöltés és egy új szöveg pontozása ===
    loaded_model = joblib.load(MODEL_PATH)
    loaded_vectorizer = joblib.load(VECTORIZER_PATH)

    test_text = ["junior python backend fastapi sql"]
    test_vec = loaded_vectorizer.transform(test_text)

    prob = loaded_model.predict_proba(test_vec)[0][1]
    print("Teszt szöveg relevancia valószínűség:", prob)
    print("Ajánlási pontszám (1–10):", round(prob * 10))

    train_probs = model.predict_proba(X_vec)[:, 1]
    print("Pozitív minták átlag prob:", train_probs[y == 1].mean())
    print("Negatív minták átlag prob:", train_probs[y == 0].mean())

    print("Model trained!")