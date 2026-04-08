# src/api/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.models.classifier import SpamClassifier
from src.api.schemas import PredictRequest, PredictResponse
from config.settings import MODEL_PATH

# این dictionary model رو در memory نگه می‌داره
# چرا dictionary؟ چون Python closure با مقدار ساده مشکل داره
ml_model = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── startup ──────────────────────────────────────
    # فقط یه بار اجرا می‌شه — موقع start شدن سرور
    # نه هر بار که request میاد!
    ml_model["classifier"] = SpamClassifier.load(MODEL_PATH)
    print("✅ Model loaded")

    yield  # ← سرور اینجا منتظر request می‌مونه

    # ── shutdown ─────────────────────────────────────
    # موقعی که سرور می‌بندیم، cleanup
    ml_model.clear()
    print("Model unloaded")


app = FastAPI(title="Spam Detector API", lifespan=lifespan)


@app.get("/health")
def health():
    # Docker و load balancer این رو چک می‌کنن
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    # request.text اینجا حتماً valid و clean هست
    # چون Pydantic قبلاً چک کرده
    result = ml_model["classifier"].predict(request.text)

    return PredictResponse(
        is_spam=result["label"],
        confidence=result["probability"],
        model_version="1.0.0",
    )
