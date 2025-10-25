import os
import joblib
from typing import Dict, Any
from .schema import HeartInput

FEATURE_ORDER = [
    "age","sex","cp","trestbps","chol","fbs","restecg","thalach","exang","oldpeak","slope","ca","thal"
]

def load_model(model_path: str = None):
    model_path = model_path or os.getenv("MODEL_PATH", "model/heart_model.joblib")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}")
    return joblib.load(model_path)

def to_feature_vector(payload: HeartInput):
    # Return in consistent order expected by model
    values = [getattr(payload, k) for k in FEATURE_ORDER]
    return [values]  # 2D for sklearn
