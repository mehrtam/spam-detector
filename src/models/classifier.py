# src/models/classifier.py
import pickle
from pathlib import Path
from src.features.preprocessing import clean_text


class SpamClassifier:
    def __init__(self, model, vectorizer):
        self.model = model
        self.vectorizer = vectorizer

    @classmethod
    def load(cls, path: str | Path) -> "SpamClassifier":
        with open(path, 'rb') as f:
            data = pickle.load(f)
        return cls(data["model"], data["vectorizer"])

    def predict(self, text: str) -> dict:
        cleaned = clean_text(text)
        features = self.vectorizer.transform([cleaned])
        label = bool(self.model.predict(features[0]))
        probability = float(self.model.predict_proba(features)[0][1])

        return {"label": label, "probability": probability}
