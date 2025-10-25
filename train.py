import os
import joblib
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

FEATURES = ["age","sex","cp","trestbps","chol","fbs","restecg","thalach","exang","oldpeak","slope","ca","thal"]

def load_data(csv_path: str):
    df = pd.read_csv(csv_path)
    # Try common target names
    target_candidates = ["target", "num", "presence", "outcome"]
    y = None
    for c in target_candidates:
        if c in df.columns:
            y = df[c]
            break
    if y is None:
        raise ValueError(f"Could not find target column among {target_candidates}")
    # Ensure all required features exist
    missing = [c for c in FEATURES if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required feature columns: {missing}")
    X = df[FEATURES].copy()
    return X, y

def generate_synthetic(n=500, seed=42):
    rng = np.random.default_rng(seed)
    X = pd.DataFrame({
        "age": rng.normal(54, 9, n),
        "sex": rng.integers(0, 2, n),
        "cp": rng.integers(0, 4, n),
        "trestbps": rng.normal(130, 17, n),
        "chol": rng.normal(245, 50, n),
        "fbs": rng.integers(0, 2, n),
        "restecg": rng.integers(0, 3, n),
        "thalach": rng.normal(149, 22, n),
        "exang": rng.integers(0, 2, n),
        "oldpeak": rng.normal(1.0, 1.1, n),
        "slope": rng.integers(0, 3, n),
        "ca": rng.integers(0, 5, n),
        "thal": rng.integers(0, 4, n),
    })
    # True model (synthetic)
    logits = (
        -3.0 + 0.02*X["age"] + 0.6*X["sex"] + 0.4*X["cp"]
        + 0.01*X["trestbps"] + 0.005*X["chol"] - 0.015*X["thalach"]
        + 0.7*X["exang"] + 0.4*X["oldpeak"] + 0.2*X["slope"] + 0.3*X["ca"]
    )
    probs = 1/(1+np.exp(-logits))
    y = (probs > 0.5).astype(int)
    return X, y

def main():
    out_path = os.environ.get("MODEL_OUT", "model/heart_model.joblib")
    data_csv = os.environ.get("DATA_CSV", "data/heart.csv")
    try:
        if os.path.exists(data_csv):
            print(f"Loading real data from {data_csv}")
            X, y = load_data(data_csv)
        else:
            print("No data/heart.csv found. Training a demo model on synthetic data...")
            X, y = generate_synthetic()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        pipe = Pipeline([
            ("scaler", StandardScaler(with_mean=False)),  # sparse-safe; harmless for dense
            ("clf", LogisticRegression(max_iter=1000))
        ])
        pipe.fit(X_train, y_train)
        joblib.dump(pipe, out_path)
        print(f"Saved model to {out_path}")
    except Exception as e:
        raise

if __name__ == "__main__":
    main()
