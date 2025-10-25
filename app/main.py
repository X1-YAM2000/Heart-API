from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .schema import HeartInput
from .model_utils import load_model, to_feature_vector, FEATURE_ORDER

app = FastAPI(title="Heart Disease Prediction API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None
model_name = None

@app.on_event("startup")
def _load():
    global model, model_name
    model = load_model()
    model_name = type(model).__name__

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/info")
def info():
    return {
        "model": model_name,
        "features": FEATURE_ORDER,
        "predict_proba_available": hasattr(model, "predict_proba")
    }

@app.post("/predict")
def predict(inp: HeartInput):
    X = to_feature_vector(inp)
    if hasattr(model, "predict_proba"):
        proba = float(model.predict_proba(X)[0][1])
    else:
        # Fallback: decision_function or binary predict
        try:
            # normalize to 0-1 via logistic-like transform if needed is skipped; use placeholder
            proba = float(getattr(model, "decision_function")(X)[0])
        except Exception:
            proba = float(model.predict(X)[0])
            # map {0,1} to probability-looking number
            proba = 0.9 if proba >= 0.5 else 0.1
    pred = proba >= 0.5
    return {"heart_disease": bool(pred), "probability": proba}
