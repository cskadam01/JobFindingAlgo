import pandas as pd
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "jobs.xlsx"
MODEL_PATH = BASE_DIR / "ai" / "model.pkl"
VECTORIZER_PATH = BASE_DIR / "ai" / "vectorizer.pkl"

def load_training_data():
    # 1) Excel beolvasása
    df = pd.read_excel(DATA_PATH)

    # 2) Csak azokat a sorokat tartjuk meg, ahol van címke (0 vagy 1)
    df = df.dropna(subset=["is_relevant"])

    # 3) Itt fűzzük össze a title + desc mezőket egyetlen szöveggé
    df["text"] = (
        df["title"].fillna("") + " " +
        df["desc"].fillna("")
    )

    # 4) Biztosítjuk, hogy string legyen, különben a .str műveletek hibázhatnak
    df["text"] = df["text"].astype(str)

    # 5) kisbetűsítés – Python == python
    df["text"] = df["text"].str.lower()

    # 6) felesleges szóközök levágása
    df["text"] = df["text"].str.strip()

    # 7) több szóköz / sortörés → egy szóköz
    df["text"] = df["text"].str.replace(r"\s+", " ", regex=True)

    # 8) X (szöveg) és y (címke) előkészítése
    X = df["text"]
    y = df["is_relevant"].astype(int)

    print("Tanító minták száma:", len(df))
    print("Pozitív minták:", (y == 1).sum())
    print("Negatív minták:", (y == 0).sum())

    return X, y

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